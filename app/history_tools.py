"""Private history export and verified SQLite backup/restore.

No reset, overwrite, schema migration, process termination, or browser-state
import is performed. Backups include the pinned route/content snapshot.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sqlite3
import struct
import time
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlsplit
import uuid
import xml.etree.ElementTree as ET

SCHEMA_VERSION = 1
FORMAT_VERSION = 1
APPLICATION = "pct-daily-dossiers"
OPTIONAL_PUBLICATIONS = frozenset(("content/topography.json", "content/satellite.json", "content/visuals.json", "content/leg_photo_manifest.json", "content/sources/visual_curation/manifest.json"))


class HistoryError(RuntimeError):
    pass


class TopographyError(HistoryError):
    def __init__(self, message, code="topography_invalid"):
        super().__init__(message)
        self.code = code


class LegPhotoError(HistoryError):
    def __init__(self, message, code="leg_photos_invalid"):
        super().__init__(message)
        self.code = code


class SatelliteError(HistoryError):
    def __init__(self, message, code="satellite_invalid"):
        super().__init__(message)
        self.code = code


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def read_json(path, limit=16 * 1024 * 1024):
    if not path.is_file() or path.stat().st_size > limit:
        raise HistoryError("A required manifest is missing or exceeds its size limit.")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as error:
        raise HistoryError("A required manifest is invalid UTF-8 JSON.") from error
    if not isinstance(value, dict):
        raise HistoryError("A required manifest must be a JSON object.")
    return value


def member(root, relative):
    if not isinstance(relative, str) or relative.startswith(("/", "\\")) or "\\" in relative or ":" in relative or any(part in ("", ".", "..") for part in relative.split("/")):
        raise HistoryError("A snapshot member path is unsafe.")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise HistoryError("A snapshot member is missing or lies outside its root.")
    return path


def repository_manifest(root):
    path = member(root, "content/itinerary.json")
    value = read_json(path)
    stages = value.get("stages")
    if not isinstance(stages, list) or not stages:
        raise HistoryError("The repository itinerary has no sections.")
    ids = []
    end = 0
    for number, stage in enumerate(stages, 1):
        if stage.get("day_number") != number or not isinstance(stage.get("id"), str) or stage["id"] in ids:
            raise HistoryError("The itinerary sequence or identities are inconsistent.")
        ids.append(stage["id"])
        if stage.get("mile_start") != end or stage.get("mile_end", 0) <= end:
            raise HistoryError("The itinerary has a gap or overlapping range.")
        end = stage["mile_end"]
        for key, directory, suffix in (("map_path", "maps", ".svg"), ("dossier_path", "dossiers", ".html"), ("geometry_path", "routes", ".geojson")):
            if stage.get(key) != f"content/{directory}/{stage['id']}{suffix}":
                raise HistoryError("A published section path is incompatible.")
            member(root, stage[key])
    return value, digest(path)


def connection(path):
    if not path.is_file():
        raise HistoryError("The authoritative database does not exist; no empty campaign was created.")
    db = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, isolation_level=None, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def experience_history(db, campaign_id, expected_day_ids=None):
    """Export all version-one domain revisions through explicit field lists."""
    names = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "experience_schema" not in names:
        if any(name.startswith("experience_") for name in names):
            raise HistoryError("The experience schema is incomplete.")
        return None
    versions = db.execute("SELECT singleton,version FROM experience_schema").fetchall()
    if len(versions) != 1 or versions[0][0] != 1 or versions[0][1] != 1:
        raise HistoryError("The experience schema is unsupported; no downgrade was attempted.")
    fields = {
        "assignments": ("experience_assignment", "assignment_id,campaign_id,day_id,version,activity_category,title,duration_minutes,distance,distance_unit,distance_meters,activity_date,timezone,notes,origin,accepted_at,operation_id", "day_id,version"),
        "workouts": ("experience_workout", "workout_id,campaign_id,day_id,assignment_id,distance,distance_unit,distance_meters,duration_minutes,purpose,notes,activity_date,timezone,source,recorded_at,operation_id", "recorded_at,workout_id"),
        "preparation": ("experience_preparation", "campaign_id,day_id,reviewed_at,content_version,operation_id", "day_id"),
        "decisions": ("experience_decision", "campaign_id,day_id,option_id,deferred,scenario_version,outcome_json,decided_at,operation_id", "day_id"),
        "resources": ("experience_resource", "transaction_id,campaign_id,day_id,operation_id,resource,delta,rule_version,cause,recorded_at", "recorded_at,transaction_id"),
        "journal_revisions": ("experience_journal", "campaign_id,day_id,revision,text,acknowledge_empty,recorded_at,operation_id", "day_id,revision"),
    }
    try:
        states = db.execute("SELECT campaign_id,revision,rules_version FROM experience_state").fetchall()
        if len(states) != 1 or states[0]["campaign_id"] != campaign_id:
            raise HistoryError("The experience campaign authority is inconsistent.")
        result = {"schema_version": 1, "state": dict(states[0])}
        snapshots = [dict(row) for row in db.execute("SELECT campaign_id,day_id,rules_version,payload_json,sha256 FROM experience_scenario ORDER BY day_id")]
        for key, (table, columns, order) in fields.items():
            result[key] = [dict(row) for row in db.execute(f"SELECT {columns} FROM {table} ORDER BY {order}")]
        receipts = [dict(row) for row in db.execute("SELECT operation_id,campaign_id,day_id,action,payload_sha256,receipt_json,committed_at FROM experience_receipt ORDER BY committed_at,operation_id")]
    except sqlite3.Error as error:
        raise HistoryError("The experience schema is missing required version-one records.") from error
    if result["state"]["revision"] != len(receipts):
        raise HistoryError("Experience revision and committed operation count disagree.")
    scenario_fields = {"id", "version", "classification", "title", "assumptions", "lesson_prompt", "training_reference", "reflection_prompt", "defer_allowed"}
    option_fields = {"id", "label", "cost_planning_tokens", "insight_stamps", "outcome"}
    for snapshot in snapshots:
        try:
            raw_text = snapshot.pop("payload_json")
            if snapshot["campaign_id"] != campaign_id or hashlib.sha256(raw_text.encode("utf-8")).hexdigest() != snapshot["sha256"]:
                raise HistoryError("A saved scenario snapshot has an invalid campaign or checksum.")
            raw = json.loads(raw_text)
            if not isinstance(raw, dict) or raw.get("id") != "scenario-" + snapshot["day_id"] or raw.get("version") != snapshot["rules_version"] or raw.get("classification") != "fictional" or not isinstance(raw.get("options"), list):
                raise HistoryError("A saved scenario snapshot has an incompatible identity or classification.")
            snapshot["payload"] = {key: raw[key] for key in sorted(scenario_fields) if key in raw}
            snapshot["payload"]["options"] = [{key: option[key] for key in sorted(option_fields) if key in option} for option in raw["options"]]
        except (ValueError, KeyError, TypeError) as error:
            raise HistoryError("A saved scenario snapshot cannot be validated.") from error
    if expected_day_ids is not None and {row["day_id"] for row in snapshots} != set(expected_day_ids):
        raise HistoryError("The saved scenario inventory differs from the pinned daily itinerary.")
    result["scenario_snapshots"] = snapshots
    allowed_receipt_fields = {"operation_id", "action", "day_id", "resulting_experience_revision", "assignment_id", "assignment_version", "workout_id", "journal_revision"}
    received_revisions = set()
    for receipt in receipts:
        try:
            raw = json.loads(receipt.pop("receipt_json"))
            if not isinstance(raw, dict) or raw["operation_id"] != receipt["operation_id"] or raw["action"] != receipt["action"] or raw["day_id"] != receipt["day_id"]:
                raise HistoryError("An experience receipt disagrees with its immutable operation identity.")
            revision = raw["resulting_experience_revision"]
            if isinstance(revision, bool) or not isinstance(revision, int) or revision in received_revisions:
                raise HistoryError("Experience receipt revisions are invalid or duplicated.")
            received_revisions.add(revision)
            receipt["result"] = {key: raw[key] for key in sorted(allowed_receipt_fields) if key in raw}
        except (ValueError, KeyError, TypeError) as error:
            raise HistoryError("An experience receipt cannot be validated.") from error
    if received_revisions != set(range(1, len(receipts) + 1)):
        raise HistoryError("Experience operation revisions have a gap.")
    receipts.sort(key=lambda item: item["result"]["resulting_experience_revision"])
    operation_ids = {receipt["operation_id"] for receipt in receipts}
    for key in fields:
        for row in result[key]:
            if row["campaign_id"] != campaign_id or row["operation_id"] not in operation_ids:
                raise HistoryError("An experience record has an orphaned operation or campaign identity.")
    for row in result["decisions"]:
        try:
            raw = json.loads(row.pop("outcome_json"))
            if not isinstance(raw, dict) or not isinstance(raw.get("text"), str) or raw.get("classification") != "fictional":
                raise HistoryError("A decision outcome is not a supported authored fictional result.")
            row["outcome"] = {"text": raw["text"], "classification": "fictional"}
        except (ValueError, KeyError, TypeError) as error:
            raise HistoryError("A decision outcome cannot be validated.") from error
    result["receipts"] = receipts
    return result


def validate_database(db, manifest, manifest_sha):
    if db.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
        raise HistoryError("The database schema is unsupported; migration or replacement was not attempted.")
    if [row[0] for row in db.execute("PRAGMA integrity_check")] != ["ok"] or db.execute("PRAGMA foreign_key_check").fetchall():
        raise HistoryError("Database integrity or foreign-key validation failed.")
    try:
        campaigns = db.execute("SELECT * FROM campaign").fetchall()
        days = db.execute("SELECT * FROM hike_day ORDER BY day_number").fetchall()
        completions = db.execute("SELECT * FROM completion ORDER BY day_number").fetchall()
        db.execute("SELECT launch_id,started_at,local_started_at,action,selected_day_id,stopped_at,outcome FROM run LIMIT 1").fetchall()
    except sqlite3.Error as error:
        raise HistoryError("The database is missing required version-one history structures.") from error
    if len(campaigns) != 1 or campaigns[0]["singleton"] != 1:
        raise HistoryError("Exactly one campaign is required.")
    campaign = dict(campaigns[0])
    if campaign["manifest_sha256"] != manifest_sha:
        raise HistoryError("The database route pin differs from the repository itinerary.")
    stages = manifest["stages"]
    count = len(completions)
    if count > len(stages) or campaign["revision"] != count or campaign["next_day_number"] != count + 1:
        raise HistoryError("The campaign revision and continuation pointer disagree with committed completions.")
    expected_days = count + (count < len(stages))
    if len(days) != expected_days:
        raise HistoryError("The day reservation sequence is inconsistent.")
    for number, day in enumerate(days, 1):
        completed = number <= count
        if day["day_number"] != number or day["day_id"] != stages[number - 1]["id"] or day["status"] != ("completed" if completed else "active") or bool(day["completed_at"]) != completed:
            raise HistoryError("A stored day identity or completion state is inconsistent.")
    for number, row in enumerate(completions, 1):
        if row["day_number"] != number or row["day_id"] != stages[number - 1]["id"] or row["expected_revision"] != number - 1 or row["resulting_revision"] != number:
            raise HistoryError("The immutable completion sequence is inconsistent.")
        try:
            receipt = json.loads(row["receipt_json"])
            state = receipt["state"]
            expected_active = stages[number]["id"] if number < len(stages) else None
            if receipt["operation_id"] != row["operation_id"] or receipt["day_id"] != row["day_id"] or receipt["completed_at"] != row["completed_at"] or state["revision"] != number or state["campaign_id"] != campaign["campaign_id"] or state["manifest_sha256"] != manifest_sha or state["current_day_id"] != expected_active or state["next_day_number"] != number + 1 or state["completed_day_ids"] != [stage["id"] for stage in stages[:number]]:
                raise HistoryError("A stored receipt disagrees with its committed completion.")
        except (ValueError, KeyError, TypeError) as error:
            raise HistoryError("A stored receipt cannot be validated.") from error
    experience = experience_history(db, campaign["campaign_id"], [stage["id"] for stage in stages])
    return {"campaign_id": campaign["campaign_id"], "revision": count, "next_day_number": count + 1,
            "completed_days": count, "total_days": len(stages), "schema_version": SCHEMA_VERSION,
            "manifest_sha256": manifest_sha, "route_release": manifest.get("metadata", {}).get("route_release"),
            "experience_schema_version": experience["schema_version"] if experience else None,
            "experience_revision": experience["state"]["revision"] if experience else None}


def topography_publication(root, manifest, manifest_sha, verify_files=False):
    """Read the optional version-one publication without campaign access.

    GET validates JSON, route identity and contained, exact source member paths.
    Backups additionally verify every declared checksum and export relationship.
    Nothing is discovered recursively or fetched from the network.
    """
    root = Path(root).resolve()
    publication_path = root / "content/topography.json"
    if not publication_path.exists() and not publication_path.is_symlink():
        return None

    def refuse(message):
        raise TopographyError(message)

    def hash_value(value):
        return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None

    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                refuse("The topographic publication contains duplicate JSON keys.")
            value[key] = item
        return value

    def finite_number(value):
        return type(value) in (int, float) and math.isfinite(value)

    def finite_float(literal):
        value = float(literal)
        if not math.isfinite(value):
            refuse("Topographic JSON must contain finite numbers.")
        return value

    def numeric_extent(value):
        return isinstance(value, dict) and all(finite_number(value.get(key)) for key in ("xmin", "ymin", "xmax", "ymax")) and -180 <= value["xmin"] < value["xmax"] <= 180 and -90 <= value["ymin"] < value["ymax"] <= 90 and isinstance(value.get("spatialReference"), dict) and value["spatialReference"].get("wkid") == 4326

    def checked_member(relative, expected):
        if relative != expected:
            refuse("A topographic source member has an unsupported publication path.")
        return member(root, relative)

    try:
        path = member(root, "content/topography.json")
        if not path.is_relative_to((root / "content").resolve()) or path.stat().st_size > 16 * 1024 * 1024:
            refuse("The topographic publication is outside its content root or exceeds its size limit.")
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object,
                           parse_float=finite_float,
                           parse_constant=lambda _: refuse("Topographic JSON must contain finite numbers."))
        if not isinstance(value, dict) or type(value.get("version")) is not int or value["version"] != 1:
            refuse("The topographic publication version is unsupported.")
        if value.get("route_release") != manifest.get("metadata", {}).get("route_release") or value.get("itinerary_sha256") != manifest_sha:
            raise TopographyError("The topographic publication belongs to a different pinned itinerary.", "topography_route_mismatch")
        sources, days = value.get("sources"), value.get("days")
        if not isinstance(sources, list) or len(sources) != 1 or not isinstance(days, list):
            refuse("The topographic source and daily inventories are invalid.")
        if type(value.get("coverage_count")) is not int or value["coverage_count"] != len(days):
            refuse("The topographic coverage count disagrees with its daily inventory.")
        if not isinstance(value.get("map_revision"), str) or re.fullmatch(r"[0-9a-f]{16}", value["map_revision"]) is None:
            refuse("The topographic map revision is invalid.")
        source = sources[0]
        service_url = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer"
        if not isinstance(source, dict) or source.get("id") != "usgs-topo" or source.get("url") != service_url or not all(isinstance(source.get(key), str) and source[key] for key in ("title", "attribution")) or not hash_value(source.get("service_metadata_sha256")):
            refuse("The version-one USGS topographic source identity is invalid.")
        service_path = checked_member(source.get("service_metadata_path"), "content/sources/topography/service.json")
        relative = {"content/topography.json", source["service_metadata_path"]}
        if verify_files and digest(service_path) != source["service_metadata_sha256"]:
            refuse("The topographic service metadata differs from its source checksum.")
        expected_days = {stage["id"]: stage for stage in manifest["stages"]}
        identities, map_hashes = set(), []
        for row in days:
            if not isinstance(row, dict) or not isinstance(row.get("day_id"), str) or row["day_id"] not in expected_days or row["day_id"] in identities or row.get("topographic") is not True:
                refuse("A topographic daily section identity is invalid or duplicated.")
            day_id = row["day_id"]
            identities.add(day_id)
            if row.get("source_ids") != ["usgs-topo"] or not all(hash_value(row.get(key)) for key in ("image_sha256", "published_map_sha256", "route_path_sha256", "baseline_sha256")):
                refuse("A topographic daily source reference or checksum is invalid.")
            if row.get("map_revision") != row["published_map_sha256"][:16] or not all(isinstance(row.get(key), str) and row[key] for key in ("source_date", "contour_note", "terrain_note")) or row.get("elevation_unit") not in (None, "ft", "m"):
                refuse("A topographic daily revision or description is invalid.")
            extent, bbox, size = row.get("export_extent"), row.get("requested_bbox"), row.get("image_size")
            if not numeric_extent(extent) or not isinstance(bbox, list) or len(bbox) != 4 or not all(finite_number(v) for v in bbox) or not (-180 <= bbox[0] < bbox[2] <= 180 and -90 <= bbox[1] < bbox[3] <= 90) or not isinstance(size, list) or len(size) != 2 or not all(type(v) is int and 1 <= v <= 4096 for v in size):
                refuse("A topographic raster extent or image size is invalid.")
            locations = (
                ("map_path", expected_days[day_id]["map_path"], "published_map_sha256"),
                ("baseline_path", f"content/sources/topography/route-only/{day_id}.svg", "baseline_sha256"),
                ("source_image_path", f"content/sources/topography/{day_id}.png", "image_sha256"),
                ("export_metadata_path", f"content/sources/topography/{day_id}.json", "export_metadata_sha256"))
            members = {}
            for field, expected, pin in locations:
                candidate = checked_member(row.get(field), expected)
                relative.add(expected)
                members[field] = candidate
                expected_hash = row.get(pin)
                # Earlier v1 publications do not carry an export-JSON hash;
                # their JSON is still cross-checked and hashed in backup.json.
                if pin == "export_metadata_sha256" and expected_hash is None:
                    continue
                if not hash_value(expected_hash) or verify_files and digest(candidate) != expected_hash:
                    refuse("A topographic artifact differs from its declared source checksum.")
            if verify_files:
                with members["source_image_path"].open("rb") as stream:
                    header = stream.read(24)
                if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR" or list(struct.unpack(">II", header[16:24])) != size:
                    refuse("The cached topographic PNG dimensions disagree with the publication.")
                exported = read_json(members["export_metadata_path"], 2 * 1024 * 1024)
                response, request = exported.get("response"), exported.get("request")
                if not isinstance(response, dict) or not isinstance(request, dict) or exported.get("image_sha256") != row["image_sha256"] or exported.get("retrieved_utc") != row["source_date"] or response.get("extent") != extent or [response.get("width"), response.get("height")] != size or request.get("bbox") != bbox:
                    refuse("The cached topographic export metadata disagrees with its publication.")
                parsed = urlsplit(request.get("url", ""))
                parameters = parse_qs(parsed.query)
                if parsed.scheme != "https" or parsed.netloc != "basemap.nationalmap.gov" or parsed.path != "/arcgis/rest/services/USGSTopo/MapServer/export" or parsed.fragment or parameters.get("bboxSR") != ["4326"] or parameters.get("imageSR") != ["4326"]:
                    refuse("The cached topographic export request is not the approved geographic USGS source.")
            map_hashes.append(row["published_map_sha256"])
        if hashlib.sha256("".join(map_hashes).encode()).hexdigest()[:16] != value["map_revision"]:
            refuse("The topographic publication revision disagrees with its map checksums.")
        return value, raw, relative
    except TopographyError:
        raise
    except (HistoryError, OSError, ValueError, UnicodeError, KeyError, TypeError, AttributeError, OverflowError) as error:
        raise TopographyError("The topographic publication or its listed source files cannot be validated.") from error


def strict_publication_json(root, relative, limit=16 * 1024 * 1024):
    """Bounded, finite, duplicate-free JSON for optional publications."""
    path = member(root, relative)
    if not path.is_relative_to((root / "content").resolve()) or path.stat().st_size > limit:
        raise HistoryError("An optional publication is outside its content root or exceeds its size limit.")
    def object_value(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise HistoryError("An optional publication contains duplicate JSON keys.")
            value[key] = item
        return value
    def invalid_number(_):
        raise HistoryError("An optional publication contains a non-finite number.")
    def finite_float(literal):
        value = float(literal)
        if not math.isfinite(value):
            invalid_number(literal)
        return value
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise HistoryError("An optional publication exceeds its bounded JSON size.")
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=object_value, parse_constant=invalid_number, parse_float=finite_float)
    if not isinstance(value, dict):
        raise HistoryError("An optional publication must be a JSON object.")
    return value, raw


def cached_tile_extent(tile, service_document, required_level):
    """Derive geographic tile bounds from a pinned Web Mercator matrix."""
    def fail():
        raise HistoryError("Cached imagery tile coordinates disagree with the pinned service matrix.")
    if not isinstance(tile, dict) or type(tile.get("level")) is not int or tile["level"] != required_level or not all(type(tile.get(k)) is int and 0 <= tile[k] < 2 ** required_level for k in ("row", "column")):
        fail()
    info = service_document.get("tileInfo")
    if not isinstance(info, dict) or info.get("spatialReference", {}).get("wkid") not in (3857, 102100):
        fail()
    width, height, origin = info.get("cols"), info.get("rows"), info.get("origin")
    lods = info.get("lods")
    if type(width) is not int or type(height) is not int or width != 256 or height != 256 or not isinstance(origin, dict) or not isinstance(lods, list):
        fail()
    candidates = [lod for lod in lods if isinstance(lod, dict) and lod.get("level") == required_level]
    if len(candidates) != 1:
        fail()
    lod = candidates[0]
    if not all(type(value) in (int, float) and math.isfinite(value) for value in (origin.get("x"), origin.get("y"), lod.get("resolution"), lod.get("scale"))) or lod["resolution"] <= 0 or lod["scale"] <= 0:
        fail()
    for key, expected in (("width", width), ("height", height), ("resolution", lod["resolution"]), ("scale", lod["scale"])):
        actual = tile.get(key)
        if type(actual) not in (int, float) or not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-8):
            fail()
    if tile.get("origin") != origin:
        fail()
    xmin = origin["x"] + tile["column"] * width * lod["resolution"]
    ymax = origin["y"] - tile["row"] * height * lod["resolution"]
    xmax, ymin = xmin + width * lod["resolution"], ymax - height * lod["resolution"]
    native = tile.get("native_extent")
    if not isinstance(native, dict) or native.get("spatialReference", {}).get("wkid") not in (3857, 102100):
        fail()
    for key, expected in zip(("xmin", "ymin", "xmax", "ymax"), (xmin, ymin, xmax, ymax)):
        actual = native.get(key)
        if type(actual) not in (int, float) or not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-6):
            fail()
    longitude = lambda x: math.degrees(x / 6378137.0)
    latitude = lambda y: math.degrees(math.atan(math.sinh(y / 6378137.0)))
    return {"xmin": longitude(xmin), "ymin": latitude(ymin), "xmax": longitude(xmax), "ymax": latitude(ymax), "spatialReference": {"wkid": 4326}}


def matching_geographic_extent(actual, expected):
    return isinstance(actual, dict) and isinstance(actual.get("spatialReference"), dict) and actual["spatialReference"].get("wkid") == 4326 and all(type(actual.get(key)) in (int, float) and math.isfinite(actual[key]) and math.isclose(actual[key], expected[key], rel_tol=0, abs_tol=1e-7) for key in ("xmin", "ymin", "xmax", "ymax"))


def service_tile_extent(level, row, column, service):
    """Apply the same pinned matrix checks to a lean satellite tile row."""
    info = service.get("tileInfo", {})
    lods = [value for value in info.get("lods", []) if isinstance(value, dict) and value.get("level") == level]
    if len(lods) != 1 or not isinstance(info.get("origin"), dict):
        raise HistoryError("A satellite tile has no unique source matrix level.")
    lod, origin = lods[0], info["origin"]
    if type(row) is not int or type(column) is not int or not all(type(value) in (int, float) and math.isfinite(value) for value in (origin.get("x"), origin.get("y"), lod.get("resolution"))):
        raise HistoryError("A satellite tile coordinate or matrix is invalid.")
    span = 256 * lod["resolution"]
    west, north = origin["x"] + column * span, origin["y"] - row * span
    complete = {"level": level, "row": row, "column": column, "origin": origin,
                "resolution": lod["resolution"], "scale": lod.get("scale"), "width": 256, "height": 256,
                "native_extent": {"xmin": west, "ymin": north-span, "xmax": west+span, "ymax": north, "spatialReference": {"wkid": 3857}}}
    return cached_tile_extent(complete, service, level)


def satellite_publication(root, manifest, manifest_sha, verify_files=False):
    """Validate an optional satellite edition and its exact listed sources."""
    root = Path(root).resolve()
    if not (root / "content/satellite.json").exists() and not (root / "content/satellite.json").is_symlink():
        return None
    def refuse(message):
        raise SatelliteError(message)
    def valid_hash(value):
        return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None
    def matching_bounds(actual, expected):
        values = [expected[k] for k in ("xmin", "ymin", "xmax", "ymax")]
        return isinstance(actual, list) and len(actual) == 4 and all(type(a) in (int, float) and math.isfinite(a) and math.isclose(a, b, rel_tol=0, abs_tol=1e-7) for a, b in zip(actual, values))
    def source_member(relative, prefix):
        candidate = member(root, relative)
        if not candidate.is_relative_to((root / prefix).resolve()):
            refuse("A satellite source member lies outside its approved content root.")
        return candidate
    try:
        value, raw = strict_publication_json(root, "content/satellite.json")
        if type(value.get("version")) is not int or value["version"] != 1:
            refuse("The satellite publication version is unsupported.")
        if value.get("route_release") != manifest.get("metadata", {}).get("route_release") or value.get("itinerary_sha256") != manifest_sha:
            raise SatelliteError("The satellite publication belongs to a different pinned itinerary.", "satellite_route_mismatch")
        sources, days = value.get("sources"), value.get("days")
        if not isinstance(sources, list) or len(sources) != 1 or not isinstance(sources[0], dict) or not isinstance(days, list) or len(days) > len(manifest["stages"]) or type(value.get("coverage_count")) is not int or value["coverage_count"] != len(days):
            refuse("The satellite daily coverage or source inventory is invalid.")
        source = sources[0]
        service_url = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer"
        if source.get("id") != "usgs-imagery" or source.get("url") != service_url or not all(isinstance(source.get(k), str) and source[k] for k in ("title", "attribution")) or source.get("metadata_path") != "content/sources/leg_photos/service.json" or not valid_hash(source.get("metadata_sha256")):
            refuse("The satellite edition does not name its approved imagery source.")
        service_path = source_member(source["metadata_path"], "content/sources/leg_photos")
        if digest(service_path) != source["metadata_sha256"]:
            refuse("The satellite service metadata differs from its pinned checksum.")
        service, _ = strict_publication_json(root, source["metadata_path"])
        relative = {"content/satellite.json", source["metadata_path"]}
        day_ids = {stage["id"] for stage in manifest["stages"]}
        seen = set()
        for day in days:
            if not isinstance(day, dict) or not isinstance(day.get("day_id"), str) or day["day_id"] not in day_ids or day["day_id"] in seen:
                refuse("A satellite section identity is invalid or duplicated.")
            seen.add(day["day_id"])
            if day.get("source_ids") != ["usgs-imagery"] or day.get("map_path") != f"content/maps/satellite-{day['day_id']}.svg" or day.get("baseline_path") != f"content/sources/topography/route-only/{day['day_id']}.svg" or not all(valid_hash(day.get(k)) for k in ("published_map_sha256", "baseline_sha256", "route_path_sha256")) or day.get("map_revision") != day["published_map_sha256"][:16]:
                refuse("A satellite map path, route source or revision is invalid.")
            # Maps are checked when served; source tiles remain embedded in
            # those maps. Resolving every tile on an ordinary metadata GET
            # would perform tens of thousands of filesystem operations.
            map_path = source_member(day["map_path"], "content/maps") if verify_files else root / day["map_path"]
            baseline_path = source_member(day["baseline_path"], "content/sources/topography/route-only") if verify_files else root / day["baseline_path"]
            relative.update((day["map_path"], day["baseline_path"]))
            tiles = day.get("tiles")
            if not isinstance(tiles, list) or not 1 <= len(tiles) <= 2000:
                refuse("A satellite map has no bounded geographic tile inventory.")
            slots = set()
            for tile in tiles:
                if not isinstance(tile, dict) or type(tile.get("level")) is not int or not 8 <= tile["level"] <= 14:
                    refuse("A satellite source tile level is unsupported.")
                level, row, column = tile["level"], tile.get("row"), tile.get("column")
                extent = service_tile_extent(level, row, column, service)
                key = f"z{level}-{row}-{column}"
                mime = tile.get("mime")
                extension = {"image/jpeg": "jpg", "image/png": "png"}.get(mime)
                if extension is None or tile.get("path") != f"content/sources/satellite/{key}.{extension}" or tile.get("metadata_path") != f"content/sources/satellite/{key}.json" or not valid_hash(tile.get("sha256")) or type(tile.get("bytes")) is not int or not 1 <= tile["bytes"] <= 8*1024*1024 or tile.get("pixel_dimensions") != [256, 256] or not matching_bounds(tile.get("bounds"), extent) or tile.get("url") != f"{service_url}/tile/{level}/{row}/{column}":
                    refuse("A satellite tile disagrees with its exact official matrix, path or image identity.")
                if "metadata_sha256" in tile and not valid_hash(tile["metadata_sha256"]):
                    refuse("A satellite tile metadata checksum is invalid.")
                requested_row, requested_column = tile.get("requested_row"), tile.get("requested_column")
                if tile.get("requested_level") != 14 or type(requested_row) is not int or type(requested_column) is not int or (requested_row, requested_column) in slots:
                    refuse("A satellite map slot is invalid or duplicated.")
                slots.add((requested_row, requested_column))
                slot_extent = service_tile_extent(14, requested_row, requested_column, service)
                shift = 2 ** (14-level)
                if row != requested_row // shift or column != requested_column // shift or not matching_bounds(tile.get("slot_bounds"), slot_extent):
                    refuse("A satellite fallback tile does not cover its requested matrix slot.")
                image_path = source_member(tile["path"], "content/sources/satellite") if verify_files else root / tile["path"]
                metadata_path = source_member(tile["metadata_path"], "content/sources/satellite") if verify_files else root / tile["metadata_path"]
                relative.update((tile["path"], tile["metadata_path"]))
                if verify_files:
                    verify_leg_photo(image_path, tile)
                    if "metadata_sha256" in tile and digest(metadata_path) != tile["metadata_sha256"]:
                        refuse("A satellite tile metadata file differs from its pinned checksum.")
                    metadata, _ = strict_publication_json(root, tile["metadata_path"])
                    for field in ("level", "row", "column", "path", "metadata_path", "sha256", "bytes", "mime", "bounds", "url", "pixel_dimensions"):
                        if metadata.get(field) != tile[field]:
                            refuse("A satellite tile source record disagrees with its publication.")
            if verify_files:
                if digest(baseline_path) != day["baseline_sha256"]:
                    refuse("A satellite map baseline differs from its pinned route source.")
                verify_satellite_map(map_path, day)
                baseline = ET.fromstring(baseline_path.read_bytes())
                plot = next((group for group in baseline.iter("{http://www.w3.org/2000/svg}g") if group.get("clip-path") == "url(#plot)"), None)
                routes = [] if plot is None else [path.get("d") for path in plot.iter("{http://www.w3.org/2000/svg}path") if path.get("stroke") == "#70e9eb"]
                if len(routes) != 1 or hashlib.sha256(routes[0].encode()).hexdigest() != day["route_path_sha256"]:
                    refuse("A satellite route does not match the unchanged baseline path.")
        expected_revision = hashlib.sha256("".join(day["published_map_sha256"] for day in days).encode()).hexdigest()[:16]
        if value.get("map_revision") != expected_revision:
            refuse("The satellite publication revision disagrees with its maps.")
        return value, raw, relative
    except SatelliteError:
        raise
    except (HistoryError, OSError, ValueError, UnicodeError, KeyError, TypeError, AttributeError, OverflowError, ET.ParseError) as error:
        raise SatelliteError("The satellite publication or its listed sources cannot be validated.") from error


def verify_satellite_map(path, day):
    """Check published SVG identity on each GET; never fetch tile sources."""
    if not 1 <= path.stat().st_size <= 64*1024*1024:
        raise SatelliteError("A satellite map exceeds its bounded publication size.")
    with path.open("rb") as stream:
        raw = stream.read(64*1024*1024 + 1)
    if len(raw) > 64*1024*1024 or hashlib.sha256(raw).hexdigest() != day["published_map_sha256"]:
        raise SatelliteError("A satellite map differs from its published checksum.")
    svg = ET.fromstring(raw)
    if svg.tag != "{http://www.w3.org/2000/svg}svg":
        raise SatelliteError("A satellite map is not a supported SVG publication.")
    plot = next((group for group in svg.iter("{http://www.w3.org/2000/svg}g") if group.get("clip-path") == "url(#plot)"), None)
    routes = [] if plot is None else [element.get("d") for element in plot.iter("{http://www.w3.org/2000/svg}path") if element.get("stroke") == "#70e9eb"]
    if len(routes) != 1 or not isinstance(routes[0], str) or hashlib.sha256(routes[0].encode()).hexdigest() != day["route_path_sha256"]:
        raise SatelliteError("A satellite map route differs from its unchanged route path.")
    images = list(svg.iter("{http://www.w3.org/2000/svg}image"))
    if len(images) != len(day["tiles"]):
        raise SatelliteError("A satellite map image inventory differs from its listed source tiles.")
    for number, (element, tile) in enumerate(zip(images, day["tiles"]), 1):
        prefix = f"data:{tile['mime']};base64,"
        href = element.get("href", "")
        if element.get("id") != f"satellite-tile-{number}" or not href.startswith(prefix):
            raise SatelliteError("A satellite map has an unsupported external image reference.")
        embedded = base64.b64decode(href[len(prefix):], validate=True)
        if len(embedded) != tile["bytes"] or hashlib.sha256(embedded).hexdigest() != tile["sha256"]:
            raise SatelliteError("A satellite map image differs from its original pinned source tile.")
    return raw


def leg_photo_publication(root, manifest, manifest_sha, verify_files=False):
    """Only explicit route-pinned aerial and licensed ground files are served."""
    root = Path(root).resolve()
    path = root / "content/leg_photo_manifest.json"
    if not path.exists() and not path.is_symlink():
        return None
    def refuse(message):
        raise LegPhotoError(message)
    def valid_hash(value):
        return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None
    def valid_dimensions(value):
        return isinstance(value, list) and len(value) == 2 and all(type(v) is int and 1 <= v <= 4096 for v in value)
    def valid_extent(value):
        return isinstance(value, dict) and all(type(value.get(k)) in (int, float) and math.isfinite(value[k]) for k in ("xmin", "ymin", "xmax", "ymax")) and -180 <= value["xmin"] < value["xmax"] <= 180 and -90 <= value["ymin"] < value["ymax"] <= 90 and isinstance(value.get("spatialReference"), dict) and value["spatialReference"].get("wkid") == 4326
    try:
        value, raw = strict_publication_json(root, "content/leg_photo_manifest.json")
        if type(value.get("version")) is not int or value["version"] != 1:
            refuse("The daily photograph publication version is unsupported.")
        if value.get("route_release") != manifest.get("metadata", {}).get("route_release") or value.get("itinerary_sha256") != manifest_sha:
            raise LegPhotoError("The daily photograph publication belongs to a different pinned itinerary.", "leg_photos_route_mismatch")
        if type(value.get("minimum_photos_per_leg")) is not int or value["minimum_photos_per_leg"] != 10 or not valid_hash(value.get("visuals_sha256")):
            refuse("The daily photograph coverage policy or visual publication pin is invalid.")
        visuals_path = member(root, "content/visuals.json")
        if digest(visuals_path) != value["visuals_sha256"]:
            refuse("The daily photograph collection differs from its pinned visual publication.")
        files, days = value.get("files"), value.get("days")
        if not isinstance(files, dict) or len(files) > 10000 or not isinstance(days, list):
            refuse("The daily photograph file or section inventory is invalid.")
        expected_days = {stage["id"] for stage in manifest["stages"]}
        seen = set()
        declared_ids, day_rows = set(), {}
        for row in days:
            if not isinstance(row, dict) or not isinstance(row.get("day_id"), str) or row["day_id"] not in expected_days or row["day_id"] in seen:
                refuse("A daily photograph section identity is invalid or duplicated.")
            seen.add(row["day_id"])
            day_rows[row["day_id"]] = row
            if "photo_ids" in row:
                ids = row["photo_ids"]
                if not isinstance(ids, list) or not all(isinstance(ident, str) and ident for ident in ids) or len(ids) != len(set(ids)) or declared_ids.intersection(ids):
                    refuse("Daily photograph source identities are invalid or assigned more than once.")
                declared_ids.update(ids)
                if "photo_count" in row and (type(row["photo_count"]) is not int or row["photo_count"] != len(ids)):
                    refuse("A daily photograph count disagrees with its source identities.")
                if "minimum_met" in row and (type(row["minimum_met"]) is not bool or row["minimum_met"] != (len(ids) >= 10)):
                    refuse("A daily photograph coverage claim disagrees with its declared minimum.")
        relative = {"content/leg_photo_manifest.json", "content/visuals.json"}
        sources = value.get("sources")
        if not isinstance(sources, list) or not sources:
            refuse("The daily aerial photograph collection has no source service inventory.")
        source_ids, imagery_documents = set(), []
        for source in sources:
            if not isinstance(source, dict):
                refuse("A daily aerial photograph service identity is invalid.")
            source_hash = source.get("metadata_sha256", source.get("service_metadata_sha256"))
            if not isinstance(source.get("id"), str) or not source["id"] or source["id"] in source_ids or not valid_hash(source_hash):
                refuse("A daily aerial photograph service identity or checksum is invalid.")
            source_ids.add(source["id"])
            name = source.get("metadata_path", source.get("service_metadata_path"))
            if "metadata_path" in source and "service_metadata_path" in source and source["metadata_path"] != source["service_metadata_path"] or "metadata_sha256" in source and "service_metadata_sha256" in source and source["metadata_sha256"] != source["service_metadata_sha256"]:
                refuse("The daily photograph service metadata aliases disagree.")
            if not isinstance(name, str) or re.fullmatch(r"content/sources/leg_photos/[A-Za-z0-9_-]+\.json", name) is None:
                refuse("A daily aerial photograph service metadata path is unsafe.")
            candidate = member(root, name)
            if not candidate.is_relative_to((root / "content/sources/leg_photos").resolve()):
                refuse("Daily photograph source metadata lies outside its approved root.")
            relative.add(name)
            if verify_files and digest(candidate) != source_hash:
                refuse("Daily photograph service metadata differs from its pinned source checksum.")
            if verify_files and source.get("url") == "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer":
                imagery_documents.append(strict_publication_json(root, name, 2 * 1024 * 1024)[0])
        ground_sources, seen_photo_ids = None, set()
        file_ids = {day_id: set() for day_id in seen}
        for name, info in files.items():
            aerial_match = re.fullmatch(r"content/media/aerial-(day-[0-9]{3})-[0-9]{2}\.(jpg|png)", name)
            ground_match = re.fullmatch(r"content/media/commons-([1-9][0-9]*)\.(jpg|png|webp)", name)
            ground = ground_match is not None
            if not isinstance(info, dict) or aerial_match is None and ground_match is None:
                refuse("A daily photograph path or source identity is invalid.")
            day_id = info.get("day_id") if ground else aerial_match.group(1)
            extension = ground_match.group(2) if ground else aerial_match.group(2)
            expected_mime = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}[extension]
            if day_id not in seen or info.get("mime") != expected_mime or not isinstance(info.get("sha256"), str) or re.fullmatch(r"[0-9a-f]{64}", info["sha256"]) is None or type(info.get("bytes")) is not int or not 1 <= info["bytes"] <= 32 * 1024 * 1024:
                refuse("A daily photograph path, source identity, MIME type, byte count or checksum is invalid.")
            candidate = member(root, name)
            if not candidate.is_relative_to((root / "content/media").resolve()):
                refuse("A daily photograph lies outside the approved media root.")
            relative.add(name)
            metadata_name = "content/sources/leg_photos/" + Path(name).stem + ".json"
            if info.get("day_id") != day_id or not isinstance(info.get("photo_id"), str) or not info["photo_id"] or info.get("metadata_path") != metadata_name or not valid_hash(info.get("metadata_sha256")) or not valid_dimensions(info.get("pixel_dimensions")):
                refuse("A daily photograph source reference, dimensions or section identity is invalid.")
            if info["photo_id"] in seen_photo_ids or "photo_ids" in day_rows[day_id] and info["photo_id"] not in day_rows[day_id]["photo_ids"]:
                refuse("A local photograph is duplicated or assigned to a different daily inventory.")
            seen_photo_ids.add(info["photo_id"])
            file_ids[day_id].add(info["photo_id"])
            if ground:
                parsed_source = urlsplit(info.get("source_url", ""))
                if info.get("media_kind") != "ground" or info["photo_id"] != "commons-" + ground_match.group(1) or parsed_source.scheme != "https" or parsed_source.netloc not in ("upload.wikimedia.org", "thumb.wikimedia.org") or parsed_source.fragment:
                    refuse("A local ground photograph has an unsupported Commons source identity.")
            elif info["photo_id"] != Path(name).stem or not valid_extent(info.get("actual_extent")) or info.get("media_kind", "aerial") != "aerial":
                refuse("A daily aerial photograph extent or source classification is invalid.")
            metadata_path = member(root, metadata_name)
            if not metadata_path.is_relative_to((root / "content/sources/leg_photos").resolve()):
                refuse("A daily aerial photograph export lies outside its approved source root.")
            relative.add(metadata_name)
            if verify_files:
                verify_leg_photo(candidate, info)
                if digest(metadata_path) != info["metadata_sha256"]:
                    refuse("A daily aerial photograph export differs from its pinned source checksum.")
                exported, _ = strict_publication_json(root, metadata_name, 2 * 1024 * 1024)
                response = exported.get("provider_response")
                if exported.get("day_id") != info["day_id"] or exported.get("photo_id") != info["photo_id"] or exported.get("image_sha256") != info["sha256"] or exported.get("image_bytes") != info["bytes"] or exported.get("decoded_dimensions") != info["pixel_dimensions"] or not isinstance(response, dict):
                    refuse("A daily photograph source record disagrees with its image publication.")
                parsed = urlsplit(exported.get("request_url", ""))
                if ground:
                    if exported.get("provider_type") != "commons-thumbnail" or exported.get("request_url") != info["source_url"] or response.get("http_status") != 200 or response.get("mime") != info["mime"]:
                        refuse("A local ground photograph disagrees with its Commons retrieval record.")
                    source_page = urlsplit(exported.get("source_url", ""))
                    if source_page.scheme != "https" or source_page.netloc != "commons.wikimedia.org" or source_page.fragment:
                        refuse("A local ground photograph has no approved Commons attribution page.")
                    original = urlsplit(exported.get("original_url", ""))
                    if original.scheme != "https" or original.netloc not in ("upload.wikimedia.org", "thumb.wikimedia.org") or original.fragment:
                        refuse("A local ground photograph has no approved original Commons image reference.")
                    provenance = exported.get("provenance")
                    if not isinstance(provenance, dict) or type(provenance.get("commons_pageid")) is not int or provenance["commons_pageid"] != int(ground_match.group(1)):
                        refuse("A local ground photograph has no matching provider page identity.")
                    if ground_sources is None:
                        relative.update(visual_source_members(root))
                        archive_manifest, _ = strict_publication_json(root, "content/sources/visual_curation/manifest.json")
                        ground_sources = {record["archive_path"]: record["source_sha256"] for record in archive_manifest["records"]}
                    for prefix in ("geotag", "image_metadata"):
                        source_name = provenance.get(prefix + "_source_path")
                        if source_name not in ground_sources or provenance.get(prefix + "_source_sha256") != ground_sources[source_name]:
                            refuse("A local ground photograph does not name its pinned public provider metadata.")
                    continue
                if parsed.scheme != "https" or parsed.netloc != "basemap.nationalmap.gov" or parsed.fragment:
                    refuse("A daily aerial photograph does not use the approved imagery source.")
                if exported.get("provider_type") == "cached-tile":
                    tile = exported.get("tile")
                    if len(imagery_documents) != 1 or not isinstance(tile, dict):
                        refuse("A cached daily photograph has no unambiguous service matrix.")
                    expected_extent = cached_tile_extent(tile, imagery_documents[0], 16)
                    if parsed.path != f"/arcgis/rest/services/USGSImageryOnly/MapServer/tile/16/{tile['row']}/{tile['column']}" or parsed.query or not matching_geographic_extent(tile.get("geographic_extent"), expected_extent) or not matching_geographic_extent(info["actual_extent"], expected_extent) or info["pixel_dimensions"] != [256, 256] or response.get("http_status") != 200 or response.get("mime") != info["mime"]:
                        refuse("A cached daily photograph disagrees with its exact USGS tile identity.")
                    for key, expected in (("center_longitude", (expected_extent["xmin"] + expected_extent["xmax"])/2), ("center_latitude", (expected_extent["ymin"] + expected_extent["ymax"])/2)):
                        if type(exported.get(key)) not in (int, float) or not math.isfinite(exported[key]) or not math.isclose(exported[key], expected, rel_tol=0, abs_tol=1e-7):
                            refuse("A cached aerial photograph center is not its actual tile center.")
                    if "response_sha256" in exported and not valid_hash(exported["response_sha256"]):
                        refuse("A cached aerial photograph has an invalid response checksum declaration.")
                elif exported.get("provider_type") in (None, "export"):
                    params = parse_qs(parsed.query)
                    if parsed.path != "/arcgis/rest/services/USGSImageryOnly/MapServer/export" or params.get("bboxSR") != ["4326"] or params.get("imageSR") != ["4326"] or response.get("extent") != info["actual_extent"] or [response.get("width"), response.get("height")] != info["pixel_dimensions"] or not valid_hash(exported.get("response_sha256")):
                        refuse("A daily aerial photograph export disagrees with its geographic source identity.")
                else:
                    refuse("The aerial photograph provider mode is unsupported.")
                if not isinstance(exported.get("source_date"), str) or not exported["source_date"]:
                    refuse("A daily aerial photograph export has invalid retrieval provenance.")
        for day_id, row in day_rows.items():
            if "photo_ids" in row and set(row["photo_ids"]) != file_ids[day_id]:
                refuse("A daily photograph inventory includes uncached or missing source files.")
        return value, raw, relative
    except LegPhotoError:
        raise
    except (HistoryError, OSError, ValueError, UnicodeError, KeyError, TypeError, AttributeError, OverflowError) as error:
        raise LegPhotoError("The daily photograph publication or its listed files cannot be validated.") from error


def verify_leg_photo(path, info):
    """Check the actual bytes on every image GET and before backup."""
    if path.stat().st_size != info["bytes"]:
        raise LegPhotoError("A cached daily photograph differs from its published byte count.")
    with path.open("rb") as stream:
        raw = stream.read(info["bytes"] + 1)
    if len(raw) != info["bytes"] or hashlib.sha256(raw).hexdigest() != info["sha256"]:
        raise LegPhotoError("A cached daily photograph differs from its published byte identity.")
    mime = info.get("mime")
    jpeg = len(raw) >= 4 and raw[:3] == b"\xff\xd8\xff" and raw[-2:] == b"\xff\xd9"
    png = len(raw) >= 33 and raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR" and list(struct.unpack(">II", raw[16:24])) == info.get("pixel_dimensions")
    webp = len(raw) >= 20 and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP" and struct.unpack("<I", raw[4:8])[0] + 8 == len(raw) and raw[12:16] in (b"VP8 ", b"VP8L", b"VP8X")
    if not {"image/jpeg": jpeg, "image/png": png, "image/webp": webp}.get(mime, False):
        raise LegPhotoError("A cached daily photograph disagrees with its published image format.")
    return raw


def visual_publication_members(root, manifest, manifest_sha):
    path = root / "content/visuals.json"
    if not path.exists() and not path.is_symlink():
        return set()
    value, _ = strict_publication_json(root, "content/visuals.json")
    if type(value.get("version")) is not int or value["version"] != 1 or value.get("route_release") != manifest.get("metadata", {}).get("route_release") or "itinerary_sha256" in value and value["itinerary_sha256"] != manifest_sha:
        raise HistoryError("The optional visual collection belongs to an unsupported or different route publication.")
    days = value.get("days")
    valid_ids, seen = {stage["id"] for stage in manifest["stages"]}, set()
    if not isinstance(days, list):
        raise HistoryError("The optional visual collection has no daily inventory.")
    for row in days:
        if not isinstance(row, dict) or row.get("day_id") not in valid_ids or row["day_id"] in seen:
            raise HistoryError("The optional visual collection has an invalid daily identity.")
        seen.add(row["day_id"])
    # Existing visual cards refer to their original hosts; no remote media is
    # downloaded or recursively included in a private history backup.
    return {"content/visuals.json"}


def visual_source_members(root):
    """Capture only listed public provider metadata, with both gzip pins."""
    relative = "content/sources/visual_curation/manifest.json"
    path = root / relative
    if not path.exists() and not path.is_symlink():
        return set()
    value, _ = strict_publication_json(root, relative)
    records = value.get("records")
    if type(value.get("version")) is not int or value["version"] != 1 or not isinstance(records, list) or len(records) > 10000:
        raise HistoryError("The public visual-source archive inventory is invalid.")
    members = {relative}
    for record in records:
        if not isinstance(record, dict):
            raise HistoryError("A public visual-source archive record is invalid.")
        name = record.get("archive_path")
        if not isinstance(name, str) or re.fullmatch(r"content/sources/visual_curation/[A-Za-z0-9_.-]+\.json\.gz", name) is None or name in members:
            raise HistoryError("A public visual-source archive path is unsafe or duplicated.")
        if not all(isinstance(record.get(key), str) and re.fullmatch(r"[0-9a-f]{64}", record[key]) for key in ("source_sha256", "archive_sha256")) or not all(type(record.get(key)) is int and 1 <= record[key] <= 16 * 1024 * 1024 for key in ("uncompressed_bytes", "compressed_bytes")):
            raise HistoryError("A public visual-source archive size or checksum is invalid.")
        archived = member(root, name)
        if not archived.is_relative_to((root / "content/sources/visual_curation").resolve()) or archived.stat().st_size != record["compressed_bytes"] or digest(archived) != record["archive_sha256"]:
            raise HistoryError("A public visual-source archive differs from its pinned compressed identity.")
        result, size = hashlib.sha256(), 0
        with gzip.open(archived, "rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(block)
                if size > 16 * 1024 * 1024 or size > record["uncompressed_bytes"]:
                    raise HistoryError("A public visual-source archive exceeds its declared size.")
                result.update(block)
        if size != record["uncompressed_bytes"] or result.hexdigest() != record["source_sha256"]:
            raise HistoryError("A public visual-source archive differs from its pinned source payload.")
        members.add(name)
    return members


def snapshot_members(root, manifest, optional_publications=None):
    relative = {"content/itinerary.json", "content/sources/source_manifest.json"}
    for stage in manifest["stages"]:
        relative.update(stage[key] for key in ("map_path", "dossier_path", "geometry_path"))
    overview = manifest.get("metadata", {}).get("overview_map_path")
    if overview:
        relative.add(overview)
    for optional in ("content/daily_sections.csv", "content/validation_report.json"):
        if (root / optional).is_file():
            relative.add(optional)
    source_manifest = read_json(member(root, "content/sources/source_manifest.json"))
    downloads = source_manifest.get("downloads")
    if not isinstance(downloads, list) or not downloads:
        raise HistoryError("The source snapshot has no download inventory.")
    centerline_sha = manifest.get("metadata", {}).get("centerline_sha256")
    source_sha = None
    for item in downloads:
        name, expected = item.get("file"), item.get("sha256")
        if not isinstance(name, str) or Path(name).name != name or not isinstance(expected, str) or len(expected) != 64:
            raise HistoryError("The source download inventory contains invalid identities or checksums.")
        archived = f"content/sources/{name}.gz"
        path = member(root, archived)
        result, size = hashlib.sha256(), 0
        with gzip.open(path, "rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(block)
                if size > 256 * 1024 * 1024:
                    raise HistoryError("A decompressed source member exceeds its size limit.")
                result.update(block)
        if result.hexdigest() != expected:
            raise HistoryError("A source archive differs from its pinned download checksum.")
        if name == "centerline_batch_000.json":
            source_sha = expected
        relative.add(archived)
    if not centerline_sha or centerline_sha != source_sha:
        raise HistoryError("The route centerline pin and source snapshot disagree.")
    manifest_sha = digest(member(root, "content/itinerary.json"))
    selected = OPTIONAL_PUBLICATIONS if optional_publications is None else set(optional_publications)
    if not selected <= OPTIONAL_PUBLICATIONS:
        raise HistoryError("An optional snapshot publication is unsupported.")
    if "content/topography.json" in selected:
        topography = topography_publication(root, manifest, manifest_sha, verify_files=True)
        if topography is not None:
            relative.update(topography[2])
    if "content/satellite.json" in selected:
        satellite = satellite_publication(root, manifest, manifest_sha, verify_files=True)
        if satellite is not None:
            relative.update(satellite[2])
    if "content/leg_photo_manifest.json" in selected:
        photos = leg_photo_publication(root, manifest, manifest_sha, verify_files=True)
        if photos is not None:
            relative.update(photos[2])
    if "content/visuals.json" in selected:
        relative.update(visual_publication_members(root, manifest, manifest_sha))
    if "content/sources/visual_curation/manifest.json" in selected:
        relative.update(visual_source_members(root))
    return [{"path": name, "size_bytes": member(root, name).stat().st_size, "sha256": digest(member(root, name))} for name in sorted(relative)]


def new_destination(path, protected):
    path = path.resolve()
    if path.exists() or path.is_symlink():
        raise HistoryError("The destination already exists. Choose a new path; existing data is never overwritten.")
    if any(path == area or path.is_relative_to(area) for area in protected):
        raise HistoryError("The destination overlaps active data or published content.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def publish_directory(staging, destination):
    if destination.exists():
        raise HistoryError("The destination appeared during preparation; it was preserved.")
    os.rename(staging, destination)


def export_history(repository_root, data_dir, output_path, output_format="json"):
    root, data = Path(repository_root).resolve(), Path(data_dir).resolve()
    target = new_destination(Path(output_path), (data, root / "content"))
    if output_format not in ("json", "jsonl"):
        raise HistoryError("Export format must be json or jsonl.")
    manifest, manifest_sha = repository_manifest(root)
    db = connection(data / "hike.sqlite")
    try:
        db.execute("BEGIN")
        state = validate_database(db, manifest, manifest_sha)
        campaign = dict(db.execute("SELECT campaign_id,manifest_sha256,revision,next_day_number,created_at FROM campaign").fetchone())
        days = [dict(row) for row in db.execute("SELECT day_number,day_id,status,created_at,completed_at FROM hike_day ORDER BY day_number")]
        completions = [dict(row) for row in db.execute("SELECT operation_id,day_id,day_number,completed_at,expected_revision,resulting_revision FROM completion ORDER BY day_number")]
        # Allowlisted export fields omit nonce, service ownership, instance_id,
        # arbitrary receipt JSON, paths, runtime output and diagnostic payloads.
        run_columns = "launch_id,started_at,local_started_at,action,selected_day_id,stopped_at,outcome"
        if "reconciled_at" in {row[1] for row in db.execute("PRAGMA table_info(run)")}:
            run_columns += ",reconciled_at"
        runs = [dict(row) for row in db.execute(f"SELECT {run_columns} FROM run ORDER BY started_at,launch_id")]
        value = {"format_version": FORMAT_VERSION, "kind": "private_hike_history", "created_at": now(),
                 "state": state, "campaign": campaign, "days": days, "completions": completions, "runs": runs}
        value["experience"] = experience_history(db, campaign["campaign_id"], [stage["id"] for stage in manifest["stages"]])
        db.commit()
    finally:
        db.close()
    if output_format == "json":
        raw = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")
    else:
        records = [{"type": "metadata", **{key: value[key] for key in ("format_version", "kind", "created_at", "state", "campaign")}}]
        records.extend({"type": kind, "record": row} for kind, rows in (("day", days), ("completion", completions), ("run", runs)) for row in rows)
        if value["experience"] is not None:
            records.append({"type": "experience_metadata", "schema_version": value["experience"]["schema_version"], "state": value["experience"]["state"]})
            records.extend({"type": "experience_" + key, "record": row} for key in ("scenario_snapshots", "assignments", "workouts", "preparation", "decisions", "resources", "journal_revisions", "receipts") for row in value["experience"][key])
        raw = ("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in records) + "\n").encode("utf-8")
    staging = target.with_name(target.name + ".staging-" + str(uuid.uuid4()))
    with staging.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    # An exclusive hard-link publication prevents an existing export from being
    # replaced even if it appears between the initial check and publication.
    os.link(staging, target)
    staging.unlink()
    return {"output_path": str(target), "sha256": digest(target), "format": output_format, "state": state}


def create_backup(repository_root, data_dir, destination, timeout_seconds=30):
    root, data = Path(repository_root).resolve(), Path(data_dir).resolve()
    target = new_destination(Path(destination), (data, root / "content"))
    manifest, manifest_sha = repository_manifest(root)
    inventory = snapshot_members(root, manifest)
    staging = target.with_name(target.name + ".staging-" + str(uuid.uuid4()))
    staging.mkdir()
    source, copied = connection(data / "hike.sqlite"), None
    try:
        source.execute("BEGIN")
        state = validate_database(source, manifest, manifest_sha)
        copied = sqlite3.connect(staging / "hike.sqlite", isolation_level=None)
        deadline = time.monotonic() + timeout_seconds
        def progress(*_):
            if time.monotonic() >= deadline:
                raise HistoryError("The consistent database snapshot exceeded its time limit; no backup was published.")
        source.backup(copied, pages=128, progress=progress, sleep=0.05)
        # The independent snapshot uses a self-contained main database, even
        # when the active campaign uses WAL. This does not change source mode.
        copied.execute("PRAGMA journal_mode=DELETE")
        copied.close()
        copied = None
        source.commit()
    finally:
        if copied:
            copied.close()
        source.close()
    for item in inventory:
        destination_file = staging / item["path"]
        destination_file.parent.mkdir(parents=True, exist_ok=True)
        source_file = member(root, item["path"])
        shutil.copyfile(source_file, destination_file)
        if digest(source_file) != item["sha256"] or digest(destination_file) != item["sha256"]:
            raise HistoryError("Published content changed during backup; the incomplete staging folder was preserved, not published.")
    copied = connection(staging / "hike.sqlite")
    try:
        copied.execute("BEGIN")
        if validate_database(copied, manifest, manifest_sha) != state:
            raise HistoryError("The copied database differs from its consistent source snapshot.")
        copied.commit()
    finally:
        copied.close()
    record = {"format_version": FORMAT_VERSION, "application": APPLICATION, "kind": "private_consistent_backup",
              "created_at": now(), "database": {"path": "hike.sqlite", "sha256": digest(staging / "hike.sqlite")},
              "state": state, "content_inventory": inventory,
              "compatibility": {"protocol_version": 1, "schema_version": SCHEMA_VERSION,
                                "experience_schema_version": state["experience_schema_version"]},
              "validation": {"sqlite_integrity_check": "ok", "foreign_key_check": "no_violations",
                             "source_download_checksums": "verified", "content_checksums": "verified"},
              "publication_rule": "A completed backup.json manifest and all checksums must validate before recovery."}
    with (staging / "backup.json").open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    publish_directory(staging, target)
    return {"backup_directory": str(target), "state": state, "content_files": len(inventory)}


def restore_backup(repository_root, backup_dir, data_dir):
    root, backup = Path(repository_root).resolve(), Path(backup_dir).resolve()
    target = new_destination(Path(data_dir), (backup, root / "content"))
    record = read_json(member(backup, "backup.json"))
    if record.get("format_version") != FORMAT_VERSION or record.get("application") != APPLICATION or record.get("kind") != "private_consistent_backup":
        raise HistoryError("The backup format or application identity is unsupported.")
    manifest, manifest_sha = repository_manifest(backup)
    recorded_inventory = record.get("content_inventory")
    if not isinstance(recorded_inventory, list) or not all(isinstance(item, dict) and isinstance(item.get("path"), str) for item in recorded_inventory):
        raise HistoryError("The backup content inventory is invalid.")
    selected_publications = {item["path"] for item in recorded_inventory} & OPTIONAL_PUBLICATIONS
    inventory = snapshot_members(backup, manifest, optional_publications=selected_publications)
    if inventory != record.get("content_inventory"):
        raise HistoryError("The backup content inventory or source snapshot does not match its manifest.")
    live_manifest, live_sha = repository_manifest(root)
    if live_sha != manifest_sha or snapshot_members(root, live_manifest, optional_publications=selected_publications) != inventory:
        raise HistoryError("The target repository differs from the backup's pinned route/content/source snapshot. Restore the matching application content first.")
    if record.get("database", {}).get("path") != "hike.sqlite" or digest(member(backup, "hike.sqlite")) != record["database"].get("sha256"):
        raise HistoryError("The backup database checksum does not match.")
    source = connection(backup / "hike.sqlite")
    try:
        source.execute("BEGIN")
        state = validate_database(source, manifest, manifest_sha)
        source.commit()
    finally:
        source.close()
    if state != record.get("state"):
        raise HistoryError("The backup revision, campaign, or continuation state differs from its manifest.")
    staging = target.with_name(target.name + ".staging-" + str(uuid.uuid4()))
    staging.mkdir()
    shutil.copyfile(backup / "hike.sqlite", staging / "hike.sqlite")
    if digest(staging / "hike.sqlite") != record["database"]["sha256"]:
        raise HistoryError("The backup database changed during recovery; no restored data was published.")
    restored = connection(staging / "hike.sqlite")
    try:
        restored.execute("BEGIN")
        if validate_database(restored, live_manifest, live_sha) != state:
            raise HistoryError("The restored database cannot reproduce the saved continuation state.")
        restored.commit()
    finally:
        restored.close()
    with (staging / "restore_receipt.json").open("x", encoding="utf-8") as stream:
        json.dump({"restored_at": now(), "backup_manifest_sha256": digest(backup / "backup.json"), "state": state}, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    publish_directory(staging, target)
    return {"data_directory": str(target), "state": state, "source_checksums_verified": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export")
    export.add_argument("--data-dir", required=True, type=Path)
    export.add_argument("--output", required=True, type=Path)
    export.add_argument("--format", choices=("json", "jsonl"), default="json")
    backup = commands.add_parser("backup")
    backup.add_argument("--data-dir", required=True, type=Path)
    backup.add_argument("--destination", required=True, type=Path)
    restore = commands.add_parser("restore")
    restore.add_argument("--backup-dir", required=True, type=Path)
    restore.add_argument("--data-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "export":
            result = export_history(args.repository_root, args.data_dir, args.output, args.format)
        elif args.command == "backup":
            result = create_backup(args.repository_root, args.data_dir, args.destination)
        else:
            result = restore_backup(args.repository_root, args.backup_dir, args.data_dir)
        print(json.dumps(result, indent=2))
        return 0
    except (HistoryError, OSError, sqlite3.Error, ValueError, KeyError) as error:
        print(json.dumps({"error": "history_operation_refused", "message": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
