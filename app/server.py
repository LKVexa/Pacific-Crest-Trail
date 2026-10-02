"""Local PCT daily dossier service. Python standard library only.

Daily section completion is a deliberate virtual-itinerary acknowledgement.
It does not record, measure, prescribe, or certify physical exercise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import secrets
import signal
import sqlite3
import sys
import threading
import time
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import experience
import history_tools

APPLICATION = "pct-daily-dossiers"
PROTOCOL_VERSION = 1
SCHEMA_VERSION = 1
MAX_BODY_BYTES = 16_384
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
DEFAULT_PORT = 8765


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class ApiError(Exception):
    def __init__(self, status, code, message, state=None):
        super().__init__(message)
        self.status, self.code, self.message, self.state = status, code, message, state


class RepositoryLock:
    """An OS-held file lock, released by the OS even after an abrupt exit."""
    def __init__(self, path):
        self.handle = path.open("a+b")
        self.handle.seek(0)
        if not self.handle.read(1):
            self.handle.write(b"0")
            self.handle.flush()
        self.handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.handle.close()
            raise RuntimeError("This repository already has an active service. Reuse its verified local instance.")

    def close(self):
        if not self.handle.closed:
            self.handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle, fcntl.LOCK_UN)
            self.handle.close()


def load_itinerary(root):
    path = root / "content" / "itinerary.json"
    raw = path.read_bytes()
    if len(raw) > 16_777_216:
        raise RuntimeError("The itinerary exceeds the supported manifest size.")
    value = json.loads(raw.decode("utf-8-sig"))
    stages = value.get("stages")
    if not isinstance(stages, list) or not 1 <= len(stages) <= 1000:
        raise RuntimeError("The itinerary must contain between 1 and 1000 daily sections.")
    ids, approved_files = set(), {"/content/itinerary.json": path}
    metadata = value.get("metadata", {})
    if not isinstance(metadata, dict):
        raise RuntimeError("The itinerary metadata must be an object.")
    overview = metadata.get("overview_map_path")
    if overview is not None:
        if overview != "content/maps/overview.svg":
            raise RuntimeError("The whole-trail overview has an unsupported publication path.")
        overview_file = (root / overview).resolve()
        if not overview_file.is_relative_to((root / "content" / "maps").resolve()) or not overview_file.is_file():
            raise RuntimeError("The published whole-trail overview is missing.")
        approved_files["/" + overview] = overview_file
    previous_end = None
    for number, stage in enumerate(stages, 1):
        day_id = stage.get("id", "")
        if not isinstance(day_id, str) or not ID_PATTERN.fullmatch(day_id) or day_id in ids:
            raise RuntimeError("Daily section identities must be unique, stable, and path-safe.")
        if stage.get("day_number") != number:
            raise RuntimeError("The daily section numbers must be consecutive, starting at 1.")
        ids.add(day_id)
        for field, directory, suffix in (("map_path", "maps", ".svg"), ("dossier_path", "dossiers", ".html"), ("geometry_path", "routes", ".geojson")):
            relative = stage.get(field)
            expected = f"content/{directory}/{day_id}{suffix}"
            if relative != expected:
                raise RuntimeError(f"{day_id} has an unsupported {field}; expected {expected}.")
            candidate = (root / relative).resolve()
            if not candidate.is_relative_to((root / "content" / directory).resolve()) or not candidate.is_file():
                raise RuntimeError(f"{day_id} is missing its published {field}.")
            approved_files["/" + relative] = candidate
        start, end, distance = (stage.get(k) for k in ("mile_start", "mile_end", "distance_miles"))
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in (start, end, distance)):
            raise RuntimeError(f"{day_id} has invalid chainage values.")
        if start < 0 or end <= start or distance <= 0 or abs((end - start) - distance) > 0.03:
            raise RuntimeError(f"{day_id} has inconsistent start, end, or distance values.")
        if previous_end is not None and abs(start - previous_end) > 0.03:
            raise RuntimeError(f"{day_id} does not connect to the previous daily section.")
        previous_end = end
    return value, raw, hashlib.sha256(raw).hexdigest(), approved_files


class Service:
    def __init__(self, root, data_dir, port, instance_id, launch_id):
        self.root = root
        self.data_dir = data_dir
        self.instance_id = instance_id
        self.launch_id = launch_id
        self.nonce = secrets.token_urlsafe(32)
        self.port = port
        self.origin = f"http://127.0.0.1:{port}"
        self.repository_id = hashlib.sha256(os.path.normcase(str(root)).encode("utf-8")).hexdigest()
        self.itinerary, self.itinerary_raw, self.manifest_sha, self.approved_files = load_itinerary(root)
        self.stages = self.itinerary["stages"]
        self.db_path = data_dir / "hike.sqlite"
        self.metadata_path = data_dir / "service.json"
        self.ready = False
        self.shutting_down = False
        self.server = None
        self.publication_cache = {}
        self.publication_cache_lock = threading.RLock()
        self.initialize_database()

    def publication_bytes(self, relative, limit):
        """Read a bounded public dependency, rechecking resolved containment."""
        path = history_tools.member(self.root, relative)
        prefix = "content/sources/leg_photos" if relative.startswith("content/sources/leg_photos/") else "content"
        if not path.is_relative_to((self.root / prefix).resolve()) or path.stat().st_size > limit:
            raise history_tools.HistoryError("A published collection dependency is outside its approved root or exceeds its size limit.")
        with path.open("rb") as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise history_tools.HistoryError("A published collection dependency exceeds its bounded size.")
        return raw

    def read_publication(self, kind):
        """Reuse validated metadata; actual bytes invalidate cached editions.

        Only metadata is cached. Every request rechecks the sidecar and its
        pinned service/visual dependencies; requested image/map bytes still
        pass their existing containment, MIME and checksum checks.
        """
        if kind == "leg-photos":
            relative, loader, error_type = "content/leg_photo_manifest.json", history_tools.leg_photo_publication, history_tools.LegPhotoError
        elif kind == "satellite":
            relative, loader, error_type = "content/satellite.json", history_tools.satellite_publication, history_tools.SatelliteError
        else:
            raise ValueError("This publication type does not support metadata caching.")
        try:
            with self.publication_cache_lock:
                sidecar = self.root / relative
                if not sidecar.exists() and not sidecar.is_symlink():
                    self.publication_cache.pop(kind, None)
                    return None
                raw = self.publication_bytes(relative, 16 * 1024 * 1024)
                signature = hashlib.sha256(raw).hexdigest()
                cached = self.publication_cache.get(kind)
                if cached is not None and cached[0] == signature:
                    publication = cached[1]
                else:
                    self.publication_cache.pop(kind, None)
                    publication = loader(self.root, self.itinerary, self.manifest_sha)
                    if publication is None:
                        return None
                    if publication[1] != raw:
                        raise error_type("The published collection changed during validation. Reload once publication has finished.")
                for source in publication[0]["sources"]:
                    name = source.get("metadata_path", source.get("service_metadata_path"))
                    expected = source.get("metadata_sha256", source.get("service_metadata_sha256"))
                    if hashlib.sha256(self.publication_bytes(name, 2 * 1024 * 1024)).hexdigest() != expected:
                        raise error_type("The published collection service metadata differs from its pinned checksum.")
                if kind == "leg-photos" and hashlib.sha256(self.publication_bytes("content/visuals.json", 16 * 1024 * 1024)).hexdigest() != publication[0]["visuals_sha256"]:
                    raise error_type("The photograph collection differs from its pinned visual publication.")
                self.publication_cache[kind] = (signature, publication)
                return publication
        except (history_tools.HistoryError, OSError, ValueError, TypeError, KeyError) as error:
            self.publication_cache.pop(kind, None)
            if isinstance(error, error_type):
                raise
            raise error_type("The published collection or its approved dependencies cannot be validated.") from error

    def connect(self):
        connection = sqlite3.connect(self.db_path, timeout=5.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    def initialize_database(self):
        db = self.connect()
        try:
            schema = db.execute("PRAGMA user_version").fetchone()[0]
            if schema not in (0, SCHEMA_VERSION):
                raise RuntimeError(f"Database schema {schema} is unsupported; preserve the data directory and use a compatible application.")
            db.execute("PRAGMA journal_mode=WAL")
            has_campaign = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='campaign'").fetchone()
            has_experience = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='experience_schema'").fetchone()
            if has_campaign and not has_experience:
                backup_name = "before-experience-v1-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
                backup_root = self.root / "backups" if self.data_dir == self.root / "data" else self.data_dir.parent / (self.data_dir.name + "-backups")
                history_tools.create_backup(self.root, self.data_dir, backup_root / backup_name)
            db.executescript("""
                CREATE TABLE IF NOT EXISTS campaign (
                  singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                  campaign_id TEXT NOT NULL UNIQUE, manifest_sha256 TEXT NOT NULL,
                  revision INTEGER NOT NULL CHECK(revision>=0),
                  next_day_number INTEGER NOT NULL CHECK(next_day_number>=1),
                  created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS hike_day (
                  day_number INTEGER PRIMARY KEY, day_id TEXT NOT NULL UNIQUE,
                  status TEXT NOT NULL CHECK(status IN ('active','completed')),
                  created_at TEXT NOT NULL, completed_at TEXT);
                CREATE UNIQUE INDEX IF NOT EXISTS one_active_day ON hike_day ((1)) WHERE status='active';
                CREATE TABLE IF NOT EXISTS completion (
                  operation_id TEXT PRIMARY KEY, day_id TEXT NOT NULL UNIQUE,
                  day_number INTEGER NOT NULL UNIQUE REFERENCES hike_day(day_number),
                  completed_at TEXT NOT NULL, expected_revision INTEGER NOT NULL,
                  resulting_revision INTEGER NOT NULL, receipt_json TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS run (
                  launch_id TEXT PRIMARY KEY, instance_id TEXT NOT NULL,
                  started_at TEXT NOT NULL, local_started_at TEXT NOT NULL,
                  action TEXT NOT NULL CHECK(action IN ('start','reuse')),
                  selected_day_id TEXT, stopped_at TEXT, outcome TEXT NOT NULL);
            """)
            db.execute("BEGIN IMMEDIATE")
            if "reconciled_at" not in {column[1] for column in db.execute("PRAGMA table_info(run)")}:
                db.execute("ALTER TABLE run ADD COLUMN reconciled_at TEXT")
            row = db.execute("SELECT * FROM campaign WHERE singleton=1").fetchone()
            if row is None:
                db.execute("INSERT INTO campaign VALUES (1,?,?,0,1,?)", (str(uuid.uuid4()), self.manifest_sha, utc_now()))
                first = self.stages[0]
                db.execute("INSERT INTO hike_day VALUES (?,?,'active',?,NULL)", (1, first["id"], utc_now()))
            elif row["manifest_sha256"] != self.manifest_sha:
                raise RuntimeError("The itinerary differs from the manifest pinned to this hike. Restore the original content or start a separate campaign in a separate data directory; history was preserved.")
            existing_days = db.execute("SELECT * FROM hike_day ORDER BY day_number").fetchall()
            for row in existing_days:
                if row["day_number"] > len(self.stages) or self.stages[row["day_number"] - 1]["id"] != row["day_id"]:
                    raise RuntimeError("Stored day identities do not match the pinned itinerary. Preserve the database for repair.")
            campaign = db.execute("SELECT * FROM campaign WHERE singleton=1").fetchone()
            active = [r for r in existing_days if r["status"] == "active"]
            if campaign["next_day_number"] <= len(self.stages):
                if len(active) != 1 or active[0]["day_number"] != campaign["next_day_number"]:
                    raise RuntimeError("The saved continuation pointer and active day disagree. Preserve the database for repair.")
            elif active or campaign["next_day_number"] != len(self.stages) + 1:
                raise RuntimeError("The saved endpoint state is inconsistent. Preserve the database for repair.")
            db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            experience.ensure_schema(db, day_count=len(self.stages))
            # An earlier process may have died before it could record a shutdown outcome.
            db.execute("UPDATE run SET outcome='interrupted',stopped_at=NULL,reconciled_at=? WHERE outcome='running'", (utc_now(),))
            self._add_run(db, self.launch_id, "start")
            db.commit()
        except BaseException:
            if db.in_transaction:
                db.rollback()
            raise
        finally:
            db.close()

    def _state(self, db):
        campaign = db.execute("SELECT * FROM campaign WHERE singleton=1").fetchone()
        active = db.execute("SELECT day_id,day_number FROM hike_day WHERE status='active'").fetchone()
        completed = [r[0] for r in db.execute("SELECT day_id FROM hike_day WHERE status='completed' ORDER BY day_number")]
        return {"campaign_id": campaign["campaign_id"], "revision": campaign["revision"],
                "current_day_id": active["day_id"] if active else None,
                "current_day_number": active["day_number"] if active else None,
                "next_day_number": campaign["next_day_number"], "completed_day_ids": completed,
                "run_count": db.execute("SELECT COUNT(*) FROM run").fetchone()[0],
                "expedition_complete": active is None, "total_days": len(self.stages),
                "manifest_sha256": self.manifest_sha}

    def state(self):
        db = self.connect()
        try:
            db.execute("BEGIN")
            result = self._state(db)
            db.commit()
            return result
        finally:
            db.close()

    def _add_run(self, db, launch_id, action):
        selected = db.execute("SELECT day_id FROM hike_day WHERE status='active'").fetchone()
        db.execute("INSERT OR IGNORE INTO run (launch_id,instance_id,started_at,local_started_at,action,selected_day_id,stopped_at,outcome) VALUES (?,?,?,?,?,?,NULL,'running')",
                   (launch_id, self.instance_id, utc_now(), datetime.now().astimezone().isoformat(timespec="milliseconds"), action, selected[0] if selected else None))

    def record_launch(self, body):
        if set(body) != {"launch_id"} or not valid_id(body["launch_id"]):
            raise ApiError(400, "invalid_launch", "A valid launch_id is required.")
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._add_run(db, body["launch_id"], "reuse")
            result = {"ok": True, "launch_id": body["launch_id"], "state": self._state(db)}
            db.commit()
            return result
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def operation(self, operation_id):
        if not valid_id(operation_id):
            raise ApiError(400, "invalid_operation", "The operation identity is invalid.")
        db = self.connect()
        try:
            db.execute("BEGIN")
            receipt = db.execute("SELECT receipt_json FROM completion WHERE operation_id=?", (operation_id,)).fetchone()
            if receipt is None:
                result = experience.lookup_operation(db, self._state(db), operation_id)
                if result is None:
                    raise ApiError(404, "operation_not_found", "No committed operation exists for this identity.")
                return result
            return dict(json.loads(receipt[0]), replayed=True)
        finally:
            db.close()

    def complete(self, body):
        if set(body) != {"day_id", "expected_revision", "operation_id"}:
            raise ApiError(400, "invalid_completion", "Supply day_id, expected_revision and operation_id only.")
        day_id, expected, operation_id = (body[k] for k in ("day_id", "expected_revision", "operation_id"))
        if not valid_id(day_id) or not valid_id(operation_id) or isinstance(expected, bool) or not isinstance(expected, int) or expected < 0:
            raise ApiError(400, "invalid_completion", "The completion fields have invalid types or values.")
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT * FROM completion WHERE operation_id=?", (operation_id,)).fetchone()
            if previous:
                if previous["day_id"] != day_id or previous["expected_revision"] != expected:
                    raise ApiError(409, "operation_conflict", "This operation identity already belongs to a different request.", self._state(db))
                result = dict(json.loads(previous["receipt_json"]), replayed=True)
                db.commit()
                return result
            if db.execute("SELECT 1 FROM experience_receipt WHERE operation_id=?", (operation_id,)).fetchone():
                raise ApiError(409, "operation_conflict", "This identity already belongs to another saved action.")
            state = self._state(db)
            if expected != state["revision"]:
                raise ApiError(409, "revision_conflict", "The saved hike changed. Refresh it before completing a section.", state)
            if day_id != state["current_day_id"]:
                raise ApiError(409, "day_conflict", "Only the current unfinished section can be completed.", state)
            try:
                experience.require_eligible(db, state, day_id)
            except experience.ExperienceError as error:
                raise ApiError(error.status, error.code, error.message, state) from error
            number, completed_at = state["current_day_number"], utc_now()
            db.execute("UPDATE hike_day SET status='completed',completed_at=? WHERE day_number=? AND status='active'", (completed_at, number))
            next_number = number + 1
            if next_number <= len(self.stages):
                db.execute("INSERT INTO hike_day VALUES (?,?,'active',?,NULL)", (next_number, self.stages[next_number - 1]["id"], completed_at))
            db.execute("UPDATE campaign SET next_day_number=?,revision=revision+1 WHERE singleton=1", (next_number,))
            result = {"ok": True, "operation_id": operation_id, "day_id": day_id,
                      "completed_at": completed_at, "replayed": False, "state": self._state(db)}
            db.execute("INSERT INTO completion VALUES (?,?,?,?,?,?,?)", (operation_id, day_id, number, completed_at, expected, result["state"]["revision"], json_bytes(result).decode("utf-8")))
            db.commit()
            return result
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def daily_experience(self, day_id):
        if day_id not in {stage["id"] for stage in self.stages}:
            raise ApiError(404, "day_not_found", "The requested daily section does not exist.")
        db = self.connect()
        try:
            db.execute("BEGIN")
            result = experience.get_experience(db, self._state(db), day_id)
            db.commit()
            return result
        except experience.ExperienceError as error:
            raise ApiError(error.status, error.code, error.message) from error
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def mutate_experience(self, action, body):
        db = self.connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            operation_id = body.get("operation_id")
            if isinstance(operation_id, str) and db.execute("SELECT 1 FROM completion WHERE operation_id=?", (operation_id,)).fetchone():
                raise ApiError(409, "operation_conflict", "This operation identity already belongs to a completion.")
            result = experience.mutate(db, self._state(db), action, body)
            db.commit()
            return result
        except experience.ExperienceError as error:
            raise ApiError(error.status, error.code, error.message) from error
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def history_action(self, action, body):
        if set(body) != {"operation_id"} or not valid_id(body["operation_id"]):
            raise ApiError(400, "invalid_history_action", "Supply a valid operation identity only.")
        base = self.root if self.data_dir == self.root / "data" else self.data_dir.parent / (self.data_dir.name + "-history")
        try:
            if action == "export":
                destination = base / "exports" / (body["operation_id"] + ".json")
                result = history_tools.export_history(self.root, self.data_dir, destination)
                return {"ok": True, "operation_id": body["operation_id"], "sha256": result["sha256"], "history": json.loads(destination.read_text(encoding="utf-8"))}
            destination = base / "backups" / body["operation_id"]
            result = history_tools.create_backup(self.root, self.data_dir, destination)
            return {"ok": True, "operation_id": body["operation_id"], "state": result["state"], "content_files": result["content_files"], "backup_directory": str(destination)}
        except history_tools.HistoryError as error:
            raise ApiError(409, "history_action_refused", str(error)) from error

    def publish_metadata(self):
        value = {"application": APPLICATION, "protocol_version": PROTOCOL_VERSION,
                 "instance_id": self.instance_id, "repository_id": self.repository_id,
                 "port": self.port, "url": self.origin, "started_at": utc_now(),
                 "process_id": os.getpid()}
        temporary = self.metadata_path.with_suffix(".json.tmp")
        with temporary.open("wb") as handle:
            handle.write(json_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, self.metadata_path)

    def finish(self, outcome):
        self.ready = False
        try:
            db = self.connect()
            try:
                db.execute("UPDATE run SET stopped_at=?,outcome=? WHERE instance_id=? AND outcome='running'", (utc_now(), outcome, self.instance_id))
            finally:
                db.close()
        finally:
            if self.metadata_path.is_file():
                try:
                    if json.loads(self.metadata_path.read_text(encoding="utf-8"))["instance_id"] == self.instance_id:
                        self.metadata_path.unlink()
                except (OSError, ValueError, KeyError):
                    pass


def valid_id(value):
    return isinstance(value, str) and ID_PATTERN.fullmatch(value) is not None


class Handler(BaseHTTPRequestHandler):
    server_version = "PCTLocal/1"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    @property
    def service(self):
        return self.server.service

    def log_message(self, *_):
        # Avoid recording arbitrary URLs, user text, tokens, or request bodies.
        return

    def send_payload(self, status, payload, content_type="application/json; charset=utf-8", etag=None):
        raw = json_bytes(payload) if not isinstance(payload, bytes) else payload
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://upload.wikimedia.org https://thumb.wikimedia.org; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self'")
        if etag:
            self.send_header("ETag", '"' + etag + '"')
        try:
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # A cancelled image request is a disconnected viewer, not a storage
            # failure. Do not attempt a second response on the closed socket.
            self.close_connection = True

    def send_error_json(self, error):
        payload = {"error": {"code": error.code, "message": error.message}}
        if error.state is not None:
            payload["state"] = error.state
        self.send_payload(error.status, payload)

    def validated_path(self):
        if self.headers.get_all("Host", []) != [f"127.0.0.1:{self.service.port}"]:
            raise ApiError(403, "invalid_host", "Only this service's explicit loopback host is accepted.")
        origin = self.headers.get("Origin")
        if origin is not None and origin != self.service.origin:
            raise ApiError(403, "invalid_origin", "The request origin is not this local application.")
        parsed = urlsplit(self.path)
        if parsed.scheme or parsed.netloc:
            raise ApiError(400, "invalid_path", "Absolute request URLs are unsupported.")
        path = unquote(parsed.path)
        if "\\" in path or "\x00" in path or ":" in path or "%" in path or any(part in (".", "..") for part in path.split("/")):
            raise ApiError(400, "invalid_path", "The requested path is invalid.")
        return path

    def do_GET(self):
        self.handle_get()

    def do_HEAD(self):
        self.handle_get()

    def handle_get(self):
        try:
            path = self.validated_path()
            if path == "/api/health":
                return self.send_payload(200, {"application": APPLICATION, "protocol_version": PROTOCOL_VERSION,
                                              "instance_id": self.service.instance_id, "repository_id": self.service.repository_id,
                                              "port": self.service.port, "ready": self.service.ready and not self.service.shutting_down})
            if path == "/api/state":
                return self.send_payload(200, self.service.state())
            if path == "/api/bootstrap":
                return self.send_payload(200, dict(self.service.state(), nonce=self.service.nonce, instance_id=self.service.instance_id))
            if path == "/api/itinerary":
                return self.send_payload(200, self.service.itinerary_raw, etag=self.service.manifest_sha)
            if path == "/api/experience":
                query = parse_qs(urlsplit(self.path).query, keep_blank_values=True)
                if set(query) != {"day"} or len(query["day"]) != 1:
                    raise ApiError(400, "day_required", "Choose one daily section identity.")
                return self.send_payload(200, self.service.daily_experience(query["day"][0]))
            if path == "/api/controls":
                control_path = (self.service.root / "content" / "controls.json").resolve()
                if not control_path.is_relative_to(self.service.root / "content") or not control_path.is_file():
                    raise ApiError(404, "controls_unavailable", "The implementation control assessment is not published yet.")
                raw = control_path.read_bytes()
                return self.send_payload(200, raw, "application/json; charset=utf-8", hashlib.sha256(raw).hexdigest())
            if path == "/api/visuals":
                # Visual curation is an independent publication, never hike-state authority.
                visual_path = (self.service.root / "content" / "visuals.json").resolve()
                if not visual_path.is_relative_to(self.service.root / "content") or not visual_path.is_file():
                    raise ApiError(404, "visuals_unavailable", "The visual collection has not been published yet.")
                raw = visual_path.read_bytes()
                return self.send_payload(200, raw, "application/json; charset=utf-8", hashlib.sha256(raw).hexdigest())
            if path == "/api/topography":
                # A sourced map edition is a read-only publication, never
                # authority for workouts, eligibility, or campaign progress.
                try:
                    publication = history_tools.topography_publication(self.service.root, self.service.itinerary, self.service.manifest_sha)
                except history_tools.TopographyError as error:
                    status = 409 if error.code == "topography_route_mismatch" else 503
                    raise ApiError(status, error.code, str(error)) from error
                if publication is None:
                    raise ApiError(404, "topography_unavailable", "The topographic map edition has not been published yet.")
                raw = publication[1]
                return self.send_payload(200, raw, "application/json; charset=utf-8", hashlib.sha256(raw).hexdigest())
            if path == "/api/satellite" or path.startswith("/content/maps/satellite-"):
                try:
                    publication = self.service.read_publication("satellite")
                    if publication is None:
                        if path == "/api/satellite":
                            raise ApiError(404, "satellite_unavailable", "The satellite map edition has not been published yet.")
                        raise ApiError(404, "not_found", "This published satellite map was not found.")
                    if path == "/api/satellite":
                        raw = publication[1]
                        return self.send_payload(200, raw, "application/json; charset=utf-8", hashlib.sha256(raw).hexdigest())
                    relative = path.lstrip("/")
                    day = next((day for day in publication[0]["days"] if day["map_path"] == relative), None)
                    if day is None:
                        raise ApiError(404, "not_found", "This map is not listed in the approved satellite edition.")
                    candidate = history_tools.member(self.service.root, relative)
                    if not candidate.is_relative_to((self.service.root / "content/maps").resolve()):
                        raise ApiError(403, "private_asset", "The map lies outside the approved map root.")
                    raw = history_tools.verify_satellite_map(candidate, day)
                    return self.send_payload(200, raw, "image/svg+xml", day["published_map_sha256"])
                except history_tools.SatelliteError as error:
                    status = 409 if error.code == "satellite_route_mismatch" else 503
                    raise ApiError(status, error.code, str(error)) from error
                except (history_tools.HistoryError, ET.ParseError, ValueError, TypeError):
                    raise ApiError(503, "satellite_invalid", "The satellite map edition cannot be verified.")
            if path == "/api/leg-photos" or path.startswith("/content/media/"):
                try:
                    publication = self.service.read_publication("leg-photos")
                    if publication is None:
                        if path == "/api/leg-photos":
                            raise ApiError(404, "leg_photos_unavailable", "The daily photograph collection has not been published yet.")
                        raise ApiError(404, "not_found", "This published daily photograph was not found.")
                    if path == "/api/leg-photos":
                        raw = publication[1]
                        return self.send_payload(200, raw, "application/json; charset=utf-8", hashlib.sha256(raw).hexdigest())
                    relative = path.lstrip("/")
                    info = publication[0]["files"].get(relative)
                    if info is None:
                        raise ApiError(404, "not_found", "This photograph is not listed in the approved daily collection.")
                    candidate = history_tools.member(self.service.root, relative)
                    if not candidate.is_relative_to((self.service.root / "content/media").resolve()):
                        raise ApiError(403, "private_asset", "The photograph lies outside the approved media root.")
                    raw = history_tools.verify_leg_photo(candidate, info)
                    return self.send_payload(200, raw, info["mime"], info["sha256"])
                except history_tools.LegPhotoError as error:
                    status = 409 if error.code == "leg_photos_route_mismatch" else 503
                    raise ApiError(status, error.code, str(error)) from error
                except history_tools.HistoryError:
                    raise ApiError(503, "leg_photos_invalid", "This cached daily photograph cannot be verified.")
            if path.startswith("/api/operations/"):
                return self.send_payload(200, self.service.operation(path.removeprefix("/api/operations/")))
            if path.startswith("/api/"):
                raise ApiError(404, "not_found", "The API endpoint does not exist.")
            candidate = self.service.approved_files.get(path)
            if path == "/":
                candidate = self.service.root / "web" / "index.html"
            elif path.startswith("/web/"):
                web_root = (self.service.root / "web").resolve()
                candidate = (web_root / path.removeprefix("/web/")).resolve()
                if not candidate.is_relative_to(web_root) or candidate.suffix.lower() not in (".html", ".css", ".js", ".svg", ".png", ".jpg", ".webp", ".ico"):
                    candidate = None
            elif path in ("/app.js", "/styles.css", "/favicon.ico"):
                candidate = self.service.root / "web" / path.lstrip("/")
            if candidate is None or not candidate.is_file():
                raise ApiError(404, "not_found", "This published local asset was not found.")
            # Recheck resolved containment on every request, including replacement links.
            resolved = candidate.resolve()
            if not resolved.is_relative_to(self.service.root / "web") and not resolved.is_relative_to(self.service.root / "content"):
                raise ApiError(403, "private_asset", "The asset lies outside the published content roots.")
            raw = resolved.read_bytes()
            content_type = {".svg": "image/svg+xml", ".geojson": "application/geo+json", ".html": "text/html", ".js": "text/javascript", ".css": "text/css"}.get(resolved.suffix.lower(), mimetypes.guess_type(resolved.name)[0] or "application/octet-stream")
            if content_type.startswith("text/") or "json" in content_type:
                content_type += "; charset=utf-8"
            return self.send_payload(200, raw, content_type, hashlib.sha256(raw).hexdigest())
        except ApiError as error:
            self.send_error_json(error)
        except (sqlite3.Error, OSError):
            self.send_error_json(ApiError(503, "storage_unavailable", "The saved hike or published content is temporarily unavailable. Progress was not advanced."))

    def read_body(self):
        if self.headers.get("Transfer-Encoding") is not None:
            raise ApiError(400, "invalid_body", "Chunked request bodies are unsupported.")
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise ApiError(415, "invalid_content_type", "Local mutations require application/json.")
        lengths = self.headers.get_all("Content-Length", [])
        if len(lengths) != 1 or not lengths[0].isdigit():
            raise ApiError(411, "length_required", "A single valid Content-Length is required.")
        size = int(lengths[0])
        if size > MAX_BODY_BYTES:
            raise ApiError(413, "body_too_large", "The request exceeds the local mutation size limit.")
        try:
            body = json.loads(self.rfile.read(size).decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise ApiError(400, "invalid_json", "The request body is not valid UTF-8 JSON.")
        if not isinstance(body, dict):
            raise ApiError(400, "invalid_json", "The request body must be a JSON object.")
        return body

    def do_POST(self):
        try:
            path = self.validated_path()
            if self.headers.get("Origin") != self.service.origin:
                raise ApiError(403, "origin_required", "Local mutations require this service's origin.")
            nonce = self.headers.get("X-PCT-Nonce", "")
            if not secrets.compare_digest(nonce, self.service.nonce):
                raise ApiError(403, "invalid_nonce", "This browser or launcher must reload the current local instance.")
            if self.service.shutting_down:
                raise ApiError(503, "shutting_down", "The local service is closing. Relaunch to continue your saved hike.")
            body = self.read_body()
            if path == "/api/complete":
                return self.send_payload(200, self.service.complete(body))
            if path in ("/api/assignment", "/api/workout", "/api/preparation", "/api/decision", "/api/journal"):
                return self.send_payload(200, self.service.mutate_experience(path.removeprefix("/api/"), body))
            if path in ("/api/export", "/api/backup"):
                return self.send_payload(200, self.service.history_action(path.removeprefix("/api/"), body))
            if path == "/api/launch":
                return self.send_payload(200, self.service.record_launch(body))
            if path == "/api/shutdown":
                if body != {"instance_id": self.service.instance_id}:
                    raise ApiError(409, "instance_conflict", "Shutdown must name the verified local instance.")
                self.service.shutting_down = True
                self.send_payload(200, {"ok": True, "instance_id": self.service.instance_id})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            raise ApiError(404, "not_found", "The API endpoint does not exist.")
        except ApiError as error:
            self.close_connection = True
            self.send_error_json(error)
        except (sqlite3.Error, OSError):
            self.close_connection = True
            self.send_error_json(ApiError(503, "storage_unavailable", "The operation could not be confirmed. Preserve its operation_id and retry or look up its committed receipt."))

    def do_OPTIONS(self):
        self.send_error_json(ApiError(405, "method_not_allowed", "Cross-origin access and preflight requests are unsupported."))

    def do_PUT(self):
        self.send_error_json(ApiError(405, "method_not_allowed", "Use the documented local API methods."))

    do_DELETE = do_PUT
    do_PATCH = do_PUT

    def setup(self):
        super().setup()
        self.connection.settimeout(10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--instance-id", default=str(uuid.uuid4()))
    parser.add_argument("--launch-id", default=str(uuid.uuid4()))
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or not valid_id(args.instance_id) or not valid_id(args.launch_id):
        parser.error("port must be 1..65535 and instance/launch identities must be path-safe.")
    root = args.root.resolve()
    data_dir = (args.data_dir or root / "data").resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    lock, server, service = None, None, None
    outcome = "startup_failed"
    try:
        lock = RepositoryLock(data_dir / "service.lock")
        # Binding occurs before state initialization, so a port conflict cannot advance history.
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
        server.daemon_threads = False
        service = Service(root, data_dir, args.port, args.instance_id, args.launch_id)
        service.server = server
        server.service = service
        service.ready = True
        service.publish_metadata()
        def request_stop(*_):
            service.shutting_down = True
            threading.Thread(target=server.shutdown, daemon=True).start()
        signal.signal(signal.SIGINT, request_stop)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, request_stop)
        print(json.dumps({"ready": True, "url": service.origin, "instance_id": service.instance_id}), flush=True)
        outcome = "interrupted"
        server.serve_forever(poll_interval=0.2)
        outcome = "closed"
        return 0
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(f"PCT startup failed: {error}", file=sys.stderr, flush=True)
        return 1
    finally:
        if server:
            server.server_close()
        if service:
            service.finish(outcome)
        if lock:
            lock.close()


if __name__ == "__main__":
    raise SystemExit(main())
