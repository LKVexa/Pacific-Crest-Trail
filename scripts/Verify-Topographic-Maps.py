"""Read-only, independent checks of every published daily topographic map.

Uses the pre-publication fixture plus retained route-only SVGs. It does not
import the publisher, fetch a provider, update assets, or inspect private history.
"""
from __future__ import annotations

import argparse
import base64
from copy import deepcopy
import hashlib
import io
import json
import math
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urlparse
import zlib

NS = {"svg": "http://www.w3.org/2000/svg"}
XLINK = "{http://www.w3.org/1999/xlink}href"
GEOMETRY_TAGS = {"path", "circle", "rect", "ellipse", "line", "polyline", "polygon"}
GEOMETRY_ATTRIBUTES = ("d", "cx", "cy", "x", "y", "width", "height", "r", "rx", "ry", "x1", "y1", "x2", "y2", "points", "transform")
PIXEL_TOLERANCE = 0.02  # original SVG coordinates have two-decimal display rounding
GEO_TOLERANCE = 1e-8
try:
    from PIL import Image
except ImportError:
    Image = None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name:
        raise ValueError("asset path is missing")
    result = (root / name).resolve()
    if root.resolve() not in result.parents or not result.is_file():
        raise ValueError(f"asset missing or outside project: {name}")
    return result


def group(svg: ET.Element, clip_id: str) -> ET.Element:
    result = [e for e in svg.iter() if local_name(e) == "g" and e.get("clip-path") == f"url(#{clip_id})"]
    if len(result) != 1:
        raise ValueError(f"expected one {clip_id} group")
    return result[0]


def route(svg: ET.Element) -> ET.Element:
    matches = [e for e in group(svg, "plot").iter() if local_name(e) == "path" and e.get("stroke") == "#70e9eb" and e.get("stroke-width") == "4.2" and e.get("id") != "topography-route-halo"]
    if len(matches) != 1:
        raise ValueError("expected exactly one original cyan daily route")
    return matches[0]


def geometry(svg: ET.Element) -> list:
    return [[local_name(e), [[k, e.get(k)] for k in GEOMETRY_ATTRIBUTES if k in e.attrib]] for e in svg.iter() if local_name(e) in GEOMETRY_TAGS and e.get("id") != "topography-route-halo"]


def element_digest(element: ET.Element) -> str:
    # Namespace prefix, formatting and attribute order do not change the meaning.
    def canonical(e):
        return [e.tag, sorted(e.attrib.items()), e.text or "", [canonical(c) for c in e]]
    return sha(json.dumps(canonical(element), ensure_ascii=False, separators=(",", ":")).encode())


def read_png(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("source/embedded image is not a PNG")
    offset = 8
    dimensions = None
    ended = False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("PNG chunk is truncated")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk = data[offset + 8:offset + 8 + length]
        if len(chunk) != length or offset + length + 12 > len(data):
            raise ValueError("PNG chunk payload is truncated")
        actual_crc = struct.unpack(">I", data[offset + length + 8:offset + length + 12])[0]
        if zlib.crc32(chunk_type + chunk) & 0xFFFFFFFF != actual_crc:
            raise ValueError("PNG chunk checksum mismatch")
        if dimensions is None:
            if chunk_type != b"IHDR" or length != 13:
                raise ValueError("PNG first chunk is not a valid IHDR")
            dimensions = struct.unpack(">II", chunk[:8])
            if not all(0 < v <= 8192 for v in dimensions):
                raise ValueError("PNG dimensions outside verification bounds")
        offset += length + 12
        if chunk_type == b"IEND":
            if length or offset != len(data):
                raise ValueError("PNG contains invalid terminal chunk/trailing data")
            ended = True
            break
    if not ended:
        raise ValueError("PNG lacks a complete IEND")
    return dimensions


def independent_projection(coordinates: list, clip: ET.Element):
    """Reconstruct the original map specification, without publisher code."""
    west, east = min(p[0] for p in coordinates), max(p[0] for p in coordinates)
    south, north = min(p[1] for p in coordinates), max(p[1] for p in coordinates)
    x, y, width, height = [float(clip.get(k)) for k in ("x", "y", "width", "height")]
    cosine = math.cos(math.radians((south + north) / 2))
    scale = min(width / max((east - west) * cosine, .003), height / max(north - south, .003)) * .86
    center_x, center_y = x + width / 2, y + height / 2
    center_lon, center_lat = (west + east) / 2, (south + north) / 2
    def project(lon, lat):
        return center_x + (lon - center_lon) * cosine * scale, center_y - (lat - center_lat) * scale
    expected_bbox = [center_lon - width / (2 * cosine * scale), center_lat - height / (2 * scale), center_lon + width / (2 * cosine * scale), center_lat + height / (2 * scale)]
    return project, expected_bbox


def numeric_close(actual, expected, tolerance=GEO_TOLERANCE):
    return len(actual) == len(expected) and all(math.isfinite(float(a)) and abs(float(a) - float(b)) <= tolerance for a, b in zip(actual, expected))


def bbox_covered(inner, outer):
    return outer[0] <= inner[0] + GEO_TOLERANCE and outer[1] <= inner[1] + GEO_TOLERANCE and outer[2] >= inner[2] - GEO_TOLERANCE and outer[3] >= inner[3] - GEO_TOLERANCE


def verify_day(root: Path, row: dict, frozen: dict, stage: dict) -> dict:
    checks, failures, notes = [], [], []
    def require(condition, name, detail):
        checks.append(name)
        if not condition:
            failures.append(f"{name}: {detail}")
    ident = row.get("day_id", "unknown")
    try:
        published_path = safe_path(root, row["map_path"])
        baseline_path = safe_path(root, row["baseline_path"])
        image_path = safe_path(root, row["source_image_path"])
        export_path = safe_path(root, row["export_metadata_path"])
        route_path = safe_path(root, stage["geometry_path"])
        published_bytes, baseline_bytes, image_bytes = published_path.read_bytes(), baseline_path.read_bytes(), image_path.read_bytes()
        svg, original = ET.fromstring(published_bytes), ET.fromstring(baseline_bytes)
        source = json.loads(export_path.read_text(encoding="utf-8"))
        geojson = json.loads(route_path.read_text(encoding="utf-8"))
        require(row["map_path"] == stage["map_path"], "map_path", "published map does not match its itinerary stage")
        require(sha(published_bytes) == row["published_map_sha256"], "published_hash", "published SVG hash does not match sidecar")
        require(sha(baseline_bytes) == row["baseline_sha256"] == frozen["map_sha256"], "frozen_original", "retained original SVG differs from independent pre-publication baseline")
        require(sha(route_path.read_bytes()) == frozen["geojson_sha256"], "immutable_route_data", "original source route GeoJSON changed")
        original_route, published_route = route(original), route(svg)
        original_d, published_d = original_route.get("d", ""), published_route.get("d", "")
        require(original_d == published_d and sha(published_d.encode()) == row["route_path_sha256"] == frozen["route_path_sha256"], "exact_route_path", "cyan route d is not byte-identical to frozen original")
        # The publisher appends a forty-pixel attribution footer. Its full-canvas
        # background alone grows; the original map/locator coordinates stay fixed.
        comparable_svg = deepcopy(svg)
        original_background = original.find("svg:rect", NS)
        published_background = svg.find("svg:rect", NS)
        comparable_background = comparable_svg.find("svg:rect", NS)
        if original_background is None or published_background is None or comparable_background is None:
            raise ValueError("map canvas background is missing")
        comparable_background.set("height", original_background.get("height"))
        require(geometry(comparable_svg) == geometry(original) and sha(json.dumps(geometry(original), separators=(",", ":")).encode()) == frozen["geometry_sha256"], "original_overlay_geometry", "original path, marker, grid, arrow, scale or clip geometry changed")
        require(element_digest(group(svg, "locator")) == element_digest(group(original, "locator")) == frozen["locator_sha256"], "locator_unchanged", "locator subtree changed")
        original_viewbox = [float(v) for v in original.get("viewBox", "").split()]
        published_viewbox = [float(v) for v in svg.get("viewBox", "").split()]
        require(len(original_viewbox) == 4 and len(published_viewbox) == 4 and published_viewbox[:3] == original_viewbox[:3] and published_viewbox[3] == original_viewbox[3] + 40 and svg.get("width") == original.get("width") and float(svg.get("height")) == published_viewbox[3] and float(published_background.get("height")) == published_viewbox[3], "canvas_with_attribution_footer", "only the intended forty-pixel footer/background extension is permitted")
        require(svg.get("transform") == original.get("transform") and group(svg, "plot").get("transform") == group(original, "plot").get("transform"), "original_projection_transform", "an added canvas/plot transform moves the original map")
        images = [e for e in svg.iter() if local_name(e) == "image"]
        require(len(images) == 1 and images[0].get("id") == "usgs-topography", "single_embedded_image", "expected one identifiable topographic raster")
        image = images[0]
        uri = image.get("href", image.get(XLINK, ""))
        if not uri.startswith("data:image/png;base64,"):
            raise ValueError("topographic raster is not embedded PNG data")
        embedded = base64.b64decode(uri.split(",", 1)[1], validate=True)
        require(embedded == image_bytes and sha(embedded) == row["image_sha256"] == source["image_sha256"], "raster_hash", "embedded PNG/cache/sidecar hashes do not agree")
        dimensions = read_png(embedded)
        response = source["response"]
        require(list(dimensions) == row["image_size"] == [response["width"], response["height"]], "raster_dimensions", "PNG dimensions differ from provider response or sidecar")
        require(image.get("preserveAspectRatio") == "none" and image.get("transform") in (None, ""), "affine_raster_sampling", "raster must follow the geographic affine transform without extra transform or aspect-ratio letterboxing")
        plot = group(svg, "plot")
        plot_children = list(plot)
        halo = [e for e in plot.iter() if e.get("id") == "topography-route-halo"]
        require(image in plot_children and plot_children.index(image) < plot_children.index(published_route), "raster_layer_order", "raster is not clipped behind the original route")
        require(len(halo) == 1 and halo[0].get("d") == original_d and plot_children.index(image) < plot_children.index(halo[0]) < plot_children.index(published_route), "halo_geometry_and_order", "contrast halo must exactly follow and precede original route")
        clip = original.find("svg:defs/svg:clipPath[@id='plot']/svg:rect", NS)
        if clip is None:
            raise ValueError("original map has no plot clip rectangle")
        coordinates = geojson["geometry"]["coordinates"]
        require(geojson["geometry"]["type"] == "LineString" and geojson["properties"]["stage_id"] == ident, "source_route_identity", "source route is not this day's LineString")
        project, expected_bbox = independent_projection(coordinates, clip)
        requested_bbox = row["requested_bbox"]
        require(numeric_close(requested_bbox, expected_bbox), "requested_geographic_bounds", "requested bbox does not cover the original projection's entire plot")
        cached_bbox = source["request"]["bbox"]
        if isinstance(cached_bbox, str):
            cached_bbox = [float(v) for v in cached_bbox.split(",")]
        require(numeric_close(cached_bbox, requested_bbox), "cached_request_bounds", "cached provider request bbox differs from sidecar")
        extent = row["export_extent"]
        provider_extent = response["extent"]
        bounds = [extent[k] for k in ("xmin", "ymin", "xmax", "ymax")]
        require(numeric_close(bounds, [provider_extent[k] for k in ("xmin", "ymin", "xmax", "ymax")]), "provider_extent", "published extent differs from actual provider export extent")
        require(extent["spatialReference"].get("latestWkid", extent["spatialReference"].get("wkid")) == 4326 and provider_extent["spatialReference"].get("latestWkid", provider_extent["spatialReference"].get("wkid")) == 4326, "geographic_spatial_reference", "export extent is not longitude/latitude EPSG:4326")
        require(bounds[0] < bounds[2] and bounds[1] < bounds[3] and bbox_covered(requested_bbox, bounds), "full_plot_coverage", "provider image omits a requested plot boundary")
        route_bounds = [min(p[0] for p in coordinates), min(p[1] for p in coordinates), max(p[0] for p in coordinates), max(p[1] for p in coordinates)]
        require(bbox_covered(route_bounds, bounds), "route_coverage", "provider image omits source route coordinates")
        left, top = project(bounds[0], bounds[3])
        right, bottom = project(bounds[2], bounds[1])
        expected_placement = [left, top, right - left, bottom - top]
        require(numeric_close([image.get(k) for k in ("x", "y", "width", "height")], expected_placement, PIXEL_TOLERANCE), "geographic_affine_placement", "raster corners do not match actual provider extent in original map projection")
        path_points = [(float(x), float(y)) for x, y in re.findall(r"[ML](-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", original_d)]
        require(len(path_points) == len(coordinates) and all(numeric_close(xy, project(*point), PIXEL_TOLERANCE) for xy, point in zip(path_points, coordinates)), "route_registration", "reconstructed source geometry does not register with the preserved displayed route")
        url = urlparse(source["request"]["url"])
        require(url.scheme == "https" and url.hostname is not None and (url.hostname.endswith(".nationalmap.gov") or url.hostname.endswith(".usgs.gov")) and "USGSTopo/MapServer/export" in url.path, "official_provider", "cache request is not the official HTTPS USGS Topo export service")
        query = parse_qs(url.query)
        require(query.get("bboxSR") == ["4326"] and query.get("imageSR") == ["4326"], "requested_spatial_reference", "provider request does not explicitly use geographic bbox/image coordinates")
        require(row.get("topographic") is True and row.get("source_ids") == ["usgs-topo"], "publication_classification", "map is not explicitly assigned to its USGS topographic source")
        require(bool(source.get("retrieved_utc")), "retrieval_provenance", "provider export has no recorded retrieval timestamp")
        if Image is not None:
            with Image.open(io.BytesIO(embedded)) as png:
                png.load()
                sample = png.convert("RGB")
                sample.thumbnail((128, 128))
                pixels = sample.get_flattened_data() if hasattr(sample, "get_flattened_data") else sample.getdata()
                require(len(set(pixels)) >= 16, "raster_color_variation", "topographic raster appears blank or nearly uniform")
        else:
            notes.append("Pillow unavailable: decoded color-variation check not executed; PNG chunk checks/dimensions still checked")
    except (KeyError, ValueError, TypeError, OSError, ET.ParseError, IndexError, struct.error) as exc:
        failures.append(f"map verification could not complete: {type(exc).__name__}: {exc}")
    return {"day_id": ident, "passed": not failures, "checks": checks, "failures": failures, "notes": notes}


def verify_project(root: Path, fixture_path: Path | None = None) -> dict:
    root = root.resolve()
    fixture_path = fixture_path or root / "tests" / "fixtures" / "topography_baseline.json"
    frozen = json.loads(fixture_path.read_text(encoding="utf-8"))
    sidecar = json.loads((root / "content" / "topography.json").read_text(encoding="utf-8"))
    itinerary_bytes = (root / "content" / "itinerary.json").read_bytes()
    itinerary = json.loads(itinerary_bytes)
    rows = sidecar["days"]
    if isinstance(rows, dict):
        rows = list(rows.values())
    expected = [f"day-{n:03d}" for n in range(1, 267)]
    failures = []
    metadata = sidecar.get("metadata", sidecar)
    if sha(itinerary_bytes) != frozen["itinerary_sha256"] or metadata["itinerary_sha256"] != frozen["itinerary_sha256"]:
        failures.append("Itinerary bytes changed from independent pre-publication baseline")
    if metadata["route_release"] != itinerary["metadata"]["route_release"] or frozen["route_release"] != itinerary["metadata"]["route_release"]:
        failures.append("Route release does not match original itinerary and sidecar")
    ids = [row.get("day_id") for row in rows]
    if len(ids) != 266 or len(set(ids)) != 266 or sorted(ids) != expected:
        failures.append("Topographic sidecar must contain exactly the 266 original day IDs once each")
    if sidecar.get("coverage_count") != len(rows):
        failures.append("Topographic coverage count does not match actual publication rows")
    stages = {stage["id"]: stage for stage in itinerary["stages"]}
    if sorted(stages) != expected or sorted(frozen["days"]) != expected:
        failures.append("Itinerary/frozen baseline does not contain exactly 266 day IDs")
    results = [verify_day(root, row, frozen["days"].get(row.get("day_id"), {}), stages.get(row.get("day_id"), {})) for row in rows]
    asset_manifest = json.loads((root / "content" / "asset_manifest.json").read_text(encoding="utf-8"))
    for row in rows:
        name = row["map_path"]
        record = asset_manifest["files"].get(name)
        if not record or record["sha256"] != row["published_map_sha256"] or record["bytes"] != safe_path(root, name).stat().st_size:
            failures.append(f"Route asset inventory does not match published map: {name}")
    for provider in sidecar.get("sources", []):
        raw = safe_path(root, provider["service_metadata_path"]).read_bytes()
        if sha(raw) != provider["service_metadata_sha256"]:
            failures.append("Provider service metadata checksum mismatch")
    return {"passed": not failures and len(results) == 266 and all(r["passed"] for r in results), "checked_days": len(results), "passed_days": sum(r["passed"] for r in results), "itinerary_sha256": sha(itinerary_bytes), "pillow_color_verification": Image is not None, "global_failures": failures, "days": results, "verification_scope": "Published map/inventory integrity, unchanged original route/overlay geometry/locator/itinerary, embedded PNG integrity/dimensions/nonuniformity, provider bounds and affine geographic registration. This does not assess contour accuracy, live trail conditions, visual readability of every map, private history, or completion of all application controls."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = verify_project(args.root, args.baseline)
    except (KeyError, ValueError, TypeError, OSError, ET.ParseError) as exc:
        report = {"passed": False, "global_failures": [f"Verification inputs unavailable/invalid: {type(exc).__name__}: {exc}"]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "days"}, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
