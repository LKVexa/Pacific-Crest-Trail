"""Independent, read-only checks of daily satellite map geometry and imagery.

Uses the frozen original route reference and official tile matrix. No publisher
imports, downloads, image edits, private-history reads, or map changes occur.
"""
from __future__ import annotations

import argparse
import base64
from copy import deepcopy
import importlib.util
import io
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

_SPEC = importlib.util.spec_from_file_location("independent_topographic_checks", Path(__file__).with_name("Verify-Topographic-Maps.py"))
T = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(T)
RADIUS = 6378137.0
SERVICE = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer"
NS = T.NS
sha = T.sha


def inverse(x, y):
    return math.degrees(x / RADIUS), math.degrees(math.atan(math.sinh(y / RADIUS)))


def tile_geometry(authority, level, row, column):
    lod = next(v for v in authority["lods"] if v["level"] == level)
    width, height, resolution = authority["cols"], authority["rows"], lod["resolution"]
    x = authority["origin"]["x"] + column * width * resolution
    top = authority["origin"]["y"] - row * height * resolution
    right, bottom = x + width * resolution, top - height * resolution
    return [*inverse(x, bottom), *inverse(right, top)], [x, bottom, right, top]


def tile_cell(authority, level, lon, lat):
    lod = next(v for v in authority["lods"] if v["level"] == level)
    x = RADIUS * math.radians(lon)
    y = RADIUS * math.asinh(math.tan(math.radians(lat)))
    return (math.floor((authority["origin"]["y"] - y) / (authority["rows"] * lod["resolution"])),
            math.floor((x - authority["origin"]["x"]) / (authority["cols"] * lod["resolution"])))


def interpolation_error(bounds, native, project):
    """Exact interior extremum of inverse-Mercator latitude vs linear placement.

    The derivative vanishes where cos(latitude) equals the ratio of endpoint
    latitude change to native Mercator height. Evaluate both possible latitudes
    plus endpoints; longitude is affine in both coordinate systems.
    """
    west, south, east, north = bounds
    north_y, south_y = native[3], native[1]
    delta_y = south_y - north_y
    delta_lat = math.radians(south - north)
    ratio = delta_lat * RADIUS / delta_y
    candidates = [0.0, 1.0]
    if 0 < ratio <= 1:
        latitude = math.acos(ratio)
        for phi in (latitude, -latitude):
            native_y = RADIUS * math.asinh(math.tan(phi))
            fraction = (native_y - north_y) / delta_y
            if 0 < fraction < 1:
                candidates.append(fraction)
    top, bottom = project(west, north)[1], project(west, south)[1]
    return max(abs(project(west, inverse(0, north_y + f * delta_y)[1])[1] - (top + f * (bottom - top))) for f in candidates)


class TileReader:
    def __init__(self, root):
        self.root, self.cache = root, {}

    def read(self, info):
        key = info["path"], info["metadata_path"]
        if key not in self.cache:
            raw = T.safe_path(self.root, key[0]).read_bytes()
            metadata_raw = T.safe_path(self.root, key[1]).read_bytes()
            if T.Image is None:
                raise ValueError("Pillow is required to decode original satellite raster bytes")
            with T.Image.open(io.BytesIO(raw)) as image:
                image.load()
                mime = {"JPEG": "image/jpeg", "PNG": "image/png"}.get(image.format)
                dimensions = list(image.size)
            self.cache[key] = raw, metadata_raw, json.loads(metadata_raw), mime, dimensions
        return self.cache[key]


def verify_day(root, row, frozen, stage, service, reader=None):
    checks, failures, tiles = [], [], []
    def require(condition, name, detail):
        checks.append(name)
        if not condition:
            failures.append(f"{name}: {detail}")
    ident = row.get("day_id", "unknown")
    reader = reader or TileReader(root)
    try:
        raw = T.safe_path(root, row["map_path"]).read_bytes()
        original_raw = T.safe_path(root, row["baseline_path"]).read_bytes()
        route_raw = T.safe_path(root, stage["geometry_path"]).read_bytes()
        svg, original = ET.fromstring(raw), ET.fromstring(original_raw)
        geojson = json.loads(route_raw)
        coordinates = geojson["geometry"]["coordinates"]
        require(row["map_path"] == f"content/maps/satellite-{ident}.svg" and row["source_ids"] == ["usgs-imagery"], "satellite_map_identity", "map path/source does not identify this daily satellite edition")
        require(sha(raw) == row["published_map_sha256"] and row["map_revision"] == sha(raw)[:16], "published_hash", "satellite SVG/revision is not the published byte sequence")
        require(sha(original_raw) == row["baseline_sha256"] == frozen["map_sha256"] and sha(route_raw) == frozen["geojson_sha256"], "frozen_original_sources", "retained original SVG or daily GeoJSON differs from independent frozen reference")
        require(geojson["geometry"]["type"] == "LineString" and geojson["properties"]["stage_id"] == ident, "daily_route_identity", "source geometry belongs to a different daily leg")
        route, original_route = T.route(svg), T.route(original)
        require(route.get("d") == original_route.get("d") and sha(route.get("d").encode()) == row["route_path_sha256"] == frozen["route_path_sha256"], "exact_original_route", "displayed cyan route was changed")
        plot = T.group(svg, "plot")
        original_plot = T.group(original, "plot")
        image_groups = [e for e in plot if e.get("clip-path", "").startswith("url(#imagery-slot-")]
        images = [e for e in svg.iter() if T.local_name(e) == "image"]
        require(len(images) == len(image_groups) == len(row["tiles"]), "tile_image_count", "tile records, embedded images, and slot groups differ")
        require(svg.get("transform") == original.get("transform") and plot.get("transform") == original_plot.get("transform"), "original_projection_transform", "an added canvas or plot transform moves route registration")
        halo = [e for e in plot if e.get("id") == "satellite-route-halo"]
        require(len(halo) == 1 and halo[0].get("d") == original_route.get("d") and list(plot).index(halo[0]) < list(plot).index(route) and all(list(plot).index(g) < list(plot).index(halo[0]) for g in image_groups), "route_halo_layer_order", "imagery must precede a matching route halo and original route")
        comparable = deepcopy(svg)
        comparable_plot = T.group(comparable, "plot")
        for child in list(comparable_plot):
            if child.get("clip-path", "").startswith("url(#imagery-slot-") or child.get("id") == "satellite-route-halo":
                comparable_plot.remove(child)
        definitions = comparable.find("svg:defs", NS)
        for child in list(definitions):
            if child.get("id", "").startswith("imagery-slot-"):
                definitions.remove(child)
        background = comparable.find("svg:rect", NS)
        background.set("height", original.find("svg:rect", NS).get("height"))
        require(T.geometry(comparable) == T.geometry(original) and sha(json.dumps(T.geometry(original), separators=(",", ":")).encode()) == frozen["geometry_sha256"], "original_checkpoint_overlay_geometry", "original checkpoint, grid, scale, arrow, clip or route geometry changed")
        require(T.element_digest(T.group(svg, "locator")) == T.element_digest(T.group(original, "locator")) == frozen["locator_sha256"], "original_locator", "the original locator subtree changed")
        ov, pv = [float(v) for v in original.get("viewBox").split()], [float(v) for v in svg.get("viewBox").split()]
        require(pv[:3] == ov[:3] and pv[3] == ov[3] + 40 and svg.get("width") == original.get("width") and float(svg.get("height")) == pv[3] and float(svg.find("svg:rect", NS).get("height")) == pv[3], "attribution_canvas_extension", "satellite publication changed the map canvas beyond the forty-pixel credit footer")
        clip = original.find("svg:defs/svg:clipPath[@id='plot']/svg:rect", NS)
        project, expected_bbox = T.independent_projection(coordinates, clip)
        require(T.numeric_close(row["requested_bbox"], expected_bbox), "original_full_plot_bounds", "declared imagery coverage differs from the original projected plot")
        authority = service["tileInfo"]
        require(authority["rows"] == authority["cols"] == 256 and authority["spatialReference"].get("latestWkid", authority["spatialReference"].get("wkid")) in (3857, 102100), "official_tile_matrix", "pinned source is not the expected 256-pixel Web Mercator matrix")
        rmin, cmin = tile_cell(authority, 14, expected_bbox[0], expected_bbox[3])
        rmax, cmax = tile_cell(authority, 14, expected_bbox[2], expected_bbox[1])
        expected_slots = {(r, c) for r in range(rmin, rmax + 1) for c in range(cmin, cmax + 1)}
        slots = [(i["requested_row"], i["requested_column"]) for i in row["tiles"]]
        require(len(slots) == len(set(slots)) and set(slots) == expected_slots, "complete_plot_tile_union", "unique requested slots do not cover every tile intersecting the full original plot")
        maximum = 0.0
        for number, info in enumerate(row["tiles"], 1):
            prefix = f"tile_{number}"
            level, r, c = info["level"], info["row"], info["column"]
            rr, rc = info["requested_row"], info["requested_column"]
            require(all(type(v) is int and v >= 0 for v in (level, r, c, rr, rc)) and info["requested_level"] == 14 and 8 <= level <= 14 and r == rr // (2 ** (14 - level)) and c == rc // (2 ** (14 - level)), prefix + "_source_parent", "source tile does not equal or ancestrally cover the declared level14 slot")
            bounds, native = tile_geometry(authority, level, r, c)
            slot_bounds, _ = tile_geometry(authority, 14, rr, rc)
            require(T.numeric_close(info["bounds"], bounds) and T.numeric_close(info["slot_bounds"], slot_bounds) and T.bbox_covered(slot_bounds, bounds), prefix + "_official_bounds", "source or requested-slot geographic bounds differ from the official tile matrix")
            source_raw, metadata_raw, metadata, mime, dimensions = reader.read(info)
            require(sha(source_raw) == info["sha256"] and len(source_raw) == info["bytes"] and sha(metadata_raw) == info["metadata_sha256"] and all(info[k] == metadata[k] for k in metadata), prefix + "_source_checksums", "tile bytes/metadata do not match the published original-source record")
            parsed = urlparse(info["url"])
            require(info["url"] == f"{SERVICE}/tile/{level}/{r}/{c}" and parsed.scheme == "https", prefix + "_official_request", "source URL does not identify this exact official imagery tile")
            require(mime == info["mime"] and dimensions == info["pixel_dimensions"] == [256, 256], prefix + "_decoded_source", "source raster is not an original decoded 256-pixel JPEG/PNG with its declared MIME")
            group = T.group(svg, f"imagery-slot-{number}")
            image = next(e for e in group if T.local_name(e) == "image")
            require(list(group) == [image] and group in image_groups and group.get("transform") in (None, "") and image.get("id") == f"satellite-tile-{number}", prefix + "_slot_group", "tile slot has unexpected content, transform or image identity")
            uri = image.get("href", image.get(T.XLINK, ""))
            expected_prefix = f"data:{mime};base64,"
            require(uri.startswith(expected_prefix) and base64.b64decode(uri.split(",", 1)[1], validate=True) == source_raw, prefix + "_embedded_original_bytes", "embedded raster bytes differ from the original cached source tile")
            x, y = project(bounds[0], bounds[3])
            right, bottom = project(bounds[2], bounds[1])
            require(T.numeric_close([image.get(k) for k in ("x", "y", "width", "height")], [x, y, right - x, bottom - y], .000005) and image.get("preserveAspectRatio") == "none" and image.get("transform") in (None, ""), prefix + "_geographic_image_placement", "source tile corners are displaced or letterboxed in the original affine projection")
            slot_clip = svg.find(f"svg:defs/svg:clipPath[@id='imagery-slot-{number}']", NS)
            slot_rect = slot_clip.find("svg:rect", NS)
            sx, sy = project(slot_bounds[0], slot_bounds[3])
            sr, sb = project(slot_bounds[2], slot_bounds[1])
            require(list(slot_clip) == [slot_rect] and slot_clip.get("clipPathUnits", "userSpaceOnUse") == "userSpaceOnUse" and slot_clip.get("transform") in (None, "") and slot_rect.get("transform") in (None, "") and T.numeric_close([slot_rect.get(k) for k in ("x", "y", "width", "height")], [sx, sy, sr - sx, sb - sy], .000005), prefix + "_geographic_slot_clip", "slot clip geometry does not match the requested level14 footprint")
            error = interpolation_error(bounds, native, project)
            maximum = max(maximum, error)
            require(error <= .25 + 1e-6, prefix + "_true_reprojection_error", "actual inverse-Mercator/affine latitude interpolation exceeds quarter of a displayed pixel")
            tiles.append({"number": number, "requested_slot": [14, rr, rc], "source_tile": [level, r, c], "true_maximum_error_pixels": error})
        require(0 <= row["maximum_reprojection_error_pixels"] <= .25 and row["maximum_reprojection_error_pixels"] <= maximum + 1e-6 and maximum - row["maximum_reprojection_error_pixels"] < .001, "declared_reprojection_error", "declared sample bound differs materially from independently derived true maximum")
    except (KeyError, ValueError, TypeError, OSError, ET.ParseError, IndexError, StopIteration, ZeroDivisionError) as exc:
        failures.append(f"satellite verification could not complete: {type(exc).__name__}: {exc}")
    return {"day_id": ident, "passed": not failures, "checks": checks, "failures": failures, "tiles": tiles}


def verify_project(root):
    root = root.resolve()
    publication = json.loads((root / "content/satellite.json").read_bytes())
    frozen = json.loads((root / "tests/fixtures/topography_baseline.json").read_bytes())
    itinerary_raw = (root / "content/itinerary.json").read_bytes()
    itinerary = json.loads(itinerary_raw)
    expected = {f"day-{i:03d}" for i in range(1, 267)}
    rows = publication["days"]
    failures = []
    if sha(itinerary_raw) != frozen["itinerary_sha256"] or publication["itinerary_sha256"] != frozen["itinerary_sha256"] or publication["route_release"] != frozen["route_release"] or itinerary["metadata"]["route_release"] != frozen["route_release"]:
        failures.append("Satellite edition itinerary/release differs from independent frozen route authority")
    if len(rows) != 266 or {r["day_id"] for r in rows} != expected or publication["coverage_count"] != 266:
        failures.append("Satellite edition does not publish all266 unique daily maps")
    sources = publication["sources"]
    if len(sources) != 1 or sources[0]["id"] != "usgs-imagery" or sources[0]["url"] != SERVICE:
        failures.append("Satellite source authority does not identify the official imagery service")
    provider = sources[0]
    service_raw = T.safe_path(root, provider["metadata_path"]).read_bytes()
    if sha(service_raw) != provider["metadata_sha256"]:
        failures.append("Official source matrix metadata checksum mismatch")
    service = json.loads(service_raw)
    stages = {s["id"]: s for s in itinerary["stages"]}
    reader = TileReader(root)
    results = [verify_day(root, row, frozen["days"].get(row["day_id"], {}), stages.get(row["day_id"], {}), service, reader) for row in rows]
    maximum = max((t["true_maximum_error_pixels"] for d in results for t in d["tiles"]), default=0)
    return {"passed": not failures and len(results) == 266 and all(d["passed"] for d in results), "checked_days": len(results), "passed_days": sum(d["passed"] for d in results), "checked_tile_placements": sum(len(d["tiles"]) for d in results), "unique_decoded_source_tiles": len(reader.cache), "true_maximum_reprojection_error_pixels": maximum, "global_failures": failures, "days": results, "scope": "Read-only source-byte/decode, exact original route/checkpoint/locator, official source/slot geographic matrix, embedded original raster placement and clipping, full plot slot coverage, and analytic interpolation-error verification. Historical imagery does not establish photographed trail visibility or current conditions; this does not mark all application controls complete."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = verify_project(args.root)
    except (KeyError, ValueError, TypeError, OSError) as exc:
        report = {"passed": False, "global_failures": [f"Satellite inputs unavailable/invalid: {type(exc).__name__}: {exc}"]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "days"}, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
