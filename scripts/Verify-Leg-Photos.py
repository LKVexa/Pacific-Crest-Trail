"""Independently verify minimum photo counts and geographic leg assignment.

Reads only public content/source assets. Uses spherical nearest-segment geometry
and the pre-topography route/itinerary reference, never the publisher's geometry
functions or private campaign history. Does not download or change pictures.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import html
import json
import math
from pathlib import Path
import re
from urllib.parse import urlparse

try:
    from PIL import Image
except ImportError:
    Image = None

EARTH_RADIUS = 6371008.8
GRID_SIZE = .025
DISTANCE_TOLERANCE_METERS = 2.0


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, name):
    if not isinstance(name, str) or not name:
        raise ValueError("missing asset path")
    path = (root / name).resolve()
    if root.resolve() not in path.parents or not path.is_file():
        raise ValueError(f"missing/outside-project asset: {name}")
    return path


def vector(point):
    lon, lat = map(math.radians, point)
    return math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]


def norm(value):
    return math.sqrt(dot(value, value))


def angle(a, b):
    return math.atan2(norm(cross(a, b)), dot(a, b))


def distance(a, b):
    return angle(vector(a), vector(b)) * EARTH_RADIUS


def closest_segment(point, start, end):
    """Closest point on the short great-circle arc, with along-arc fraction."""
    p, a, b = vector(point), vector(start), vector(end)
    arc = angle(a, b)
    if arc < 1e-12:
        return angle(p, a) * EARTH_RADIUS, 0.0
    n = cross(a, b)
    magnitude = norm(n)
    n = tuple(v / magnitude for v in n)
    projected = tuple(p[i] - dot(p, n) * n[i] for i in range(3))
    projected_norm = norm(projected)
    if projected_norm > 1e-12:
        q = tuple(v / projected_norm for v in projected)
        along = angle(a, q)
        if abs(along + angle(q, b) - arc) <= 1e-9:
            return angle(p, q) * EARTH_RADIUS, max(0.0, min(1.0, along / arc))
    to_start, to_end = angle(p, a), angle(p, b)
    return (to_start * EARTH_RADIUS, 0.0) if to_start <= to_end else (to_end * EARTH_RADIUS, 1.0)


class RouteIndex:
    def __init__(self, routes):
        self.routes = routes
        self.lengths, self.cumulative = {}, {}
        self.grid = defaultdict(list)
        for ident, points in routes.items():
            lengths = [distance(a, b) for a, b in zip(points, points[1:])]
            cumulative = [0.0]
            for length in lengths:
                cumulative.append(cumulative[-1] + length)
            self.lengths[ident], self.cumulative[ident] = lengths, cumulative
            for i, (a, b) in enumerate(zip(points, points[1:])):
                min_x, max_x = sorted((math.floor(a[0] / GRID_SIZE), math.floor(b[0] / GRID_SIZE)))
                min_y, max_y = sorted((math.floor(a[1] / GRID_SIZE), math.floor(b[1] / GRID_SIZE)))
                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        self.grid[(x, y)].append((ident, i))

    def assigned(self, point, ident):
        best = (float("inf"), 0.0)
        points, lengths, cumulative = self.routes[ident], self.lengths[ident], self.cumulative[ident]
        for i, (a, b) in enumerate(zip(points, points[1:])):
            offset, segment_fraction = closest_segment(point, a, b)
            if offset < best[0]:
                best = offset, (cumulative[i] + segment_fraction * lengths[i]) / cumulative[-1]
        return best

    def global_closest(self, point):
        # For PCT latitude32–49, a one-cell neighborhood extends >1km in both
        # geographic axes. Every eligible point therefore includes its nearest arc.
        x, y = math.floor(point[0] / GRID_SIZE), math.floor(point[1] / GRID_SIZE)
        best = (float("inf"), None)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for ident, i in self.grid.get((x + dx, y + dy), []):
                    points = self.routes[ident]
                    offset, _ = closest_segment(point, points[i], points[i + 1])
                    if offset < best[0]:
                        best = offset, ident
        return best

    def at_fraction(self, ident, fraction):
        points, lengths, cumulative = self.routes[ident], self.lengths[ident], self.cumulative[ident]
        wanted = fraction * cumulative[-1]
        for i, length in enumerate(lengths):
            if wanted <= cumulative[i + 1] or i == len(lengths) - 1:
                f = 0.0 if length == 0 else (wanted - cumulative[i]) / length
                a, b = vector(points[i]), vector(points[i + 1])
                theta = angle(a, b)
                if theta < 1e-12:
                    return points[i]
                q = tuple((math.sin((1 - f) * theta) * a[j] + math.sin(f * theta) * b[j]) / math.sin(theta) for j in range(3))
                return math.degrees(math.atan2(q[1], q[0])), math.degrees(math.atan2(q[2], math.hypot(q[0], q[1])))
        raise ValueError("route interpolation failed")


def dictionaries(value):
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from dictionaries(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from dictionaries(nested)


class PublicSourceReader:
    def __init__(self, root):
        self.root = root
        self.digests, self.documents = {}, {}
        archive_manifest = root / "content" / "sources" / "visual_curation" / "manifest.json"
        self.archives = {r["archive_path"]: r for r in json.loads(archive_manifest.read_text(encoding="utf-8"))["records"]} if archive_manifest.is_file() else {}

    def read(self, name, expected_digest):
        if name not in self.digests:
            path = safe_path(self.root, name)
            raw = path.read_bytes()
            decoded = gzip.decompress(raw) if path.suffix == ".gz" else raw
            if path.suffix == ".gz":
                record = self.archives.get(name)
                if not record or record["archive_sha256"] != sha(raw) or record["source_sha256"] != sha(decoded) or record["compressed_bytes"] != len(raw) or record["uncompressed_bytes"] != len(decoded):
                    raise ValueError(f"compressed public source archive is not pinned by provenance manifest: {name}")
            self.digests[name] = sha(decoded)
            self.documents[name] = json.loads(decoded)
        if self.digests[name] != expected_digest:
            raise ValueError(f"public provenance source checksum mismatch: {name}")
        return self.documents[name]


def page_candidates(document, page_id):
    for record in dictionaries(document):
        if str(record.get("pageid", "")) == str(page_id):
            yield record
        keyed = record.get(str(page_id))
        if isinstance(keyed, dict):
            yield keyed


def documented_geotag(document, page_id, point):
    for page in page_candidates(document, page_id):
        for record in dictionaries(page):
            lat, lon = record.get("lat", record.get("latitude")), record.get("lon", record.get("longitude"))
            if lat is not None and lon is not None and abs(float(lat) - point[1]) <= 1e-6 and abs(float(lon) - point[0]) <= 1e-6:
                return True
    return False


def extent_values(extent):
    values = [float(extent[k]) for k in ("xmin", "ymin", "xmax", "ymax")]
    if not all(math.isfinite(v) for v in values) or values[0] >= values[2] or values[1] >= values[3]:
        raise ValueError("invalid geographic imagery extent")
    if extent.get("spatialReference", {}).get("latestWkid", extent.get("spatialReference", {}).get("wkid")) != 4326:
        raise ValueError("imagery extent is not EPSG:4326")
    return values


def mercator_inverse(x, y):
    radius = 6378137.0
    return math.degrees(x / radius), math.degrees(math.atan(math.sinh(y / radius)))


def mercator_forward(lon, lat):
    radius = 6378137.0
    return radius * math.radians(lon), radius * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def verify_cached_tile(root, photo, ident, point, assignment, metadata, dimensions, index, sources, require):
    """Derive all raster geography from the pinned official tile matrix."""
    tile = metadata["tile"]
    service_path = metadata.get("service_metadata_path", "content/sources/leg_photos/service.json")
    service = sources.read(service_path, metadata["service_metadata_sha256"])
    authority = service["tileInfo"]
    level, row, column = tile["level"], tile["row"], tile["column"]
    require(all(isinstance(v, int) and v >= 0 for v in (level, row, column)) and level == 16, "aerial_tile_identity", "cached tile does not identify the approved level16 matrix cell")
    lod = next((lod for lod in authority["lods"] if lod["level"] == level), None)
    if lod is None:
        raise ValueError("tile level is absent from the pinned source matrix")
    resolution = float(lod["resolution"])
    width, height = authority["cols"], authority["rows"]
    origin = authority["origin"]
    left = float(origin["x"]) + column * width * resolution
    right = left + width * resolution
    top = float(origin["y"]) - row * height * resolution
    bottom = top - height * resolution
    expected_native = [left, bottom, right, top]
    native = tile["native_extent"]
    actual_native = [float(native[k]) for k in ("xmin", "ymin", "xmax", "ymax")]
    require(native["spatialReference"].get("latestWkid", native["spatialReference"].get("wkid")) in (3857, 102100) and authority["spatialReference"].get("latestWkid", authority["spatialReference"].get("wkid")) in (3857, 102100), "aerial_native_reference", "tile matrix/native image bounds are not Web Mercator")
    require(all(abs(a - b) <= .001 for a, b in zip(actual_native, expected_native)) and tile["origin"] == origin and abs(float(tile["resolution"]) - resolution) <= 1e-12 and abs(float(tile["scale"]) - float(lod["scale"])) <= 1e-6 and dimensions == [width, height] == [tile["width"], tile["height"]], "aerial_tile_matrix_bounds", "cached tile bounds/dimensions/origin/resolution/scale differ from official source matrix")
    southwest, northeast = mercator_inverse(left, bottom), mercator_inverse(right, top)
    expected_bounds = [southwest[0], southwest[1], northeast[0], northeast[1]]
    require(all(abs(a - b) <= 1e-8 for a, b in zip(extent_values(tile["geographic_extent"]), expected_bounds)) and all(abs(a - b) <= 1e-8 for a, b in zip(extent_values(photo["actual_extent"]), expected_bounds)), "aerial_tile_geographic_bounds", "published geographic extent does not derive from the native tile matrix")
    expected_center = mercator_inverse((left + right) / 2, (bottom + top) / 2)
    require(distance(point, expected_center) <= .05, "aerial_tile_pixel_center", "card coordinates do not identify the uncropped tile's actual center pixel")
    offset, fraction = index.assigned(point, ident)
    closest_offset, closest_ident = index.global_closest(point)
    require(offset <= 500 + .1 and offset <= closest_offset + DISTANCE_TOLERANCE_METERS, "aerial_tile_nearest_leg", f"tile center is not within500m of its globally nearest leg (nearest {closest_ident})")
    require(abs(float(assignment["distance_meters"]) - offset) <= DISTANCE_TOLERANCE_METERS and abs(float(photo["distance_to_section_meters"]) - offset) <= DISTANCE_TOLERANCE_METERS, "aerial_tile_measured_offset", "tile-center offset must record its measured distance to the route")
    require(abs(float(assignment["route_fraction"]) - fraction) * index.cumulative[ident][-1] <= DISTANCE_TOLERANCE_METERS, "aerial_tile_route_fraction", "tile's route mile/fraction does not identify its nearest route witness")
    witness = metadata["route_witness"]
    witness_point = float(witness["longitude"]), float(witness["latitude"])
    expected_witness = index.at_fraction(ident, fraction)
    wx, wy = mercator_forward(*witness_point)
    require(distance(witness_point, expected_witness) <= DISTANCE_TOLERANCE_METERS and left - .001 <= wx <= right + .001 and bottom - .001 <= wy <= top + .001, "aerial_trail_witness_inside_tile", "nearest route witness is absent from the actual tile image bounds")
    request_url = urlparse(metadata["request_url"])
    expected_suffix = f"/USGSImageryOnly/MapServer/tile/{level}/{row}/{column}"
    require(request_url.scheme == "https" and request_url.hostname == "basemap.nationalmap.gov" and request_url.path.endswith(expected_suffix) and not request_url.query and not request_url.fragment, "aerial_official_tile_request", "cached raster request does not identify this exact official USGS imagery tile")
    response = metadata["provider_response"]
    require(response["http_status"] == 200 and response["mime"].lower().split(";", 1)[0] in ("image/jpeg", "image/png"), "aerial_tile_response", "cached tile has no recorded successful original JPEG/PNG response")
    require(assignment["coordinate_role"] == "imagery_tile_center" and "aerial" in photo["title"].lower() and assignment["route_witness"] == witness, "aerial_tile_label", "overhead tile must be explicitly labeled as aerial context with the recorded route witness")
    require(photo["source_tile"] == {"level": level, "row": row, "column": column} and photo["source_url"] == metadata["request_url"], "aerial_card_source_tile", "card source link/identity does not identify the actual requested tile")


def verify_ground_cache(root, photo, ident, sources, files, require):
    parsed = urlparse(photo["thumbnail_url"])
    require(not parsed.scheme and not parsed.netloc and not parsed.query and not parsed.fragment and parsed.path.startswith("/content/media/"), "local_ground_asset", "a counted ground picture must use its project-local cached bytes")
    relative = parsed.path.lstrip("/")
    record = files[relative]
    raw = safe_path(root, relative).read_bytes()
    require(record["media_kind"] == "ground" and record["day_id"] == ident and record["photo_id"] == photo["id"] and sha(raw) == record["sha256"] == photo["image_sha256"] and len(raw) == record["bytes"], "ground_cache_identity", "cached ground bytes/manifest are not this picture and leg")
    require(record["metadata_path"] == photo["source_metadata_path"] and record["pixel_dimensions"] == photo["pixel_dimensions"], "ground_cache_metadata_reference", "ground cache/card metadata or dimensions differ")
    metadata = sources.read(record["metadata_path"], record["metadata_sha256"])
    require(metadata["provider_type"] == "commons-thumbnail" and metadata["day_id"] == ident and metadata["photo_id"] == photo["id"] and metadata["image_path"] == relative and metadata["image_sha256"] == photo["image_sha256"] and metadata["image_bytes"] == len(raw), "ground_cached_source_identity", "cached source response does not identify this image")
    remote = urlparse(photo["remote_thumbnail_url"])
    require(remote.scheme == "https" and remote.hostname in ("upload.wikimedia.org", "thumb.wikimedia.org") and metadata["request_url"] == metadata["remote_thumbnail_url"] == record["source_url"] == photo["remote_thumbnail_url"], "ground_cached_provider_request", "cached ground picture lacks the original licensed provider thumbnail reference")
    require(metadata["provider_response"] == {"http_status": 200, "mime": record["mime"]} and metadata["mime"] == record["mime"], "ground_cached_http_facts", "ground cache lacks a recorded successful response matching its original MIME")
    require(all(metadata[k] == photo[k] for k in ("provenance", "latitude", "longitude", "assignment", "author", "license", "license_url", "title", "original_url", "source_url")), "ground_cached_provenance_identity", "cached response has a different source/coordinate/assignment/credit than its card")
    if Image is None:
        raise ValueError("Pillow is required to decode cached ground pictures")
    with Image.open(safe_path(root, relative)) as image:
        image.load()
        decoded_mime = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}.get(image.format)
        require(decoded_mime is not None and decoded_mime == record["mime"] and list(image.size) == metadata["decoded_dimensions"] == photo["pixel_dimensions"] and min(image.size) >= 120, "decoded_ground_dimensions", "decoded ground picture format/dimensions do not match its cache publication")


def verify_photo(root, photo, ident, stage, index, sources, files, require_local=True):
    checks, failures = [], []
    def require(condition, name, detail):
        checks.append(name)
        if not condition:
            failures.append(f"{name}: {detail}")
    photo_id = photo.get("id", "unknown")
    try:
        kind = photo["media_kind"]
        point = float(photo["longitude"]), float(photo["latitude"])
        require(all(math.isfinite(v) for v in point) and -180 <= point[0] <= 180 and -90 <= point[1] <= 90, "geographic_coordinates", "photo coordinates are invalid")
        assignment = photo["assignment"]
        fraction = float(assignment["route_fraction"])
        require(assignment["day_id"] == ident and 0 <= fraction <= 1, "assigned_leg", "photo is assigned to a different leg or invalid route fraction")
        mile = float(photo["route_mile"])
        require(stage["mile_start"] <= mile <= stage["mile_end"] and abs(mile - (stage["mile_start"] + stage["distance_miles"] * fraction)) <= .011, "bounded_route_mile", "photo mile is outside this leg or differs from its geographic route fraction")
        offset, measured_fraction = index.assigned(point, ident)
        if kind == "ground":
            require(offset <= 1000 + .1, "ground_distance_limit", "ground provider geotag lies more than1km from its assigned route")
            globally_nearest, nearest_day = index.global_closest(point)
            require(offset <= globally_nearest + DISTANCE_TOLERANCE_METERS, "globally_nearest_leg", f"closer leg {nearest_day} is {globally_nearest:.2f}m away, assigned leg is {offset:.2f}m away")
            require(abs(float(assignment["distance_meters"]) - offset) <= DISTANCE_TOLERANCE_METERS and abs(float(photo["distance_to_section_meters"]) - offset) <= DISTANCE_TOLERANCE_METERS, "ground_offset_value", "recorded ground offset differs from independent spherical nearest arc")
            require(abs(measured_fraction - fraction) * index.cumulative[ident][-1] <= DISTANCE_TOLERANCE_METERS, "ground_along_route_location", "recorded route fraction differs from independently projected source geotag")
            require(assignment["coordinate_role"] == "provider_geotag_camera_unverified", "ground_location_qualification", "ground geotag must retain camera/subject uncertainty")
            provenance = photo["provenance"]
            geotags = sources.read(provenance["geotag_source_path"], provenance["geotag_source_sha256"])
            metadata = sources.read(provenance["image_metadata_source_path"], provenance["image_metadata_source_sha256"])
            if not photo_id.startswith("commons-"):
                raise ValueError("ground photograph lacks a Commons source pageid")
            page_id = photo_id.removeprefix("commons-")
            require(str(provenance["commons_pageid"]) == page_id, "ground_provider_identity", "ground source pageid does not match its card ID")
            require(documented_geotag(geotags, page_id, point), "provider_geotag_evidence", "public source archive does not contain matching pageid/coordinates")
            pages = list(page_candidates(metadata, page_id))
            require(bool(pages), "provider_image_metadata", "public image-metadata archive does not contain this source pageid")
            infos = [p["imageinfo"][0] for p in pages if p.get("imageinfo")]
            require(any(html.unescape(info.get("url", "")) == photo.get("original_url") for info in infos), "ground_original_image_reference", "ground original image URL does not match archived provider image metadata")
            require(bool(photo.get("author")) and bool(photo.get("license")) and bool(photo.get("license_url")), "ground_attribution", "ground photograph lacks recorded author/license links")
            if require_local:
                verify_ground_cache(root, photo, ident, sources, files, require)
        elif kind == "aerial":
            require(re.fullmatch(rf"aerial-{re.escape(ident)}-\d{{2}}", photo_id) is not None, "aerial_identity", "aerial frame ID does not identify its assigned leg and numbered frame")
            bounds = extent_values(photo["actual_extent"])
            dimensions = photo["pixel_dimensions"]
            require(len(dimensions) == 2 and all(isinstance(v, int) and 0 < v <= 8192 for v in dimensions), "aerial_pixel_dimensions", "aerial pixel dimensions are invalid")
            parsed = urlparse(photo["thumbnail_url"])
            require(not parsed.scheme and not parsed.netloc and not parsed.query and not parsed.fragment and parsed.path.startswith("/content/media/"), "local_aerial_asset", "aerial card does not reference a project-local cached image")
            relative = parsed.path.lstrip("/")
            record = files[relative]
            raw = safe_path(root, relative).read_bytes()
            require(sha(raw) == photo["image_sha256"] == record["sha256"] and len(raw) == record["bytes"], "aerial_image_hash", "cached aerial image/card/manifest checksums or byte counts differ")
            require(record["day_id"] == ident and record["photo_id"] == photo_id and record["pixel_dimensions"] == dimensions and record["actual_extent"] == photo["actual_extent"], "aerial_manifest_identity", "cached image manifest has a different leg/photo/dimensions/extent")
            require(record["media_kind"] == "aerial" and record["source_tile"] == photo["source_tile"], "aerial_manifest_classification", "cached tile manifest is misclassified or identifies a different cell")
            require(record["metadata_path"] == photo["source_metadata_path"], "aerial_metadata_reference", "card and file manifest reference different source metadata")
            metadata = sources.read(record["metadata_path"], record["metadata_sha256"])
            require(metadata["provider_type"] == record["provider_type"] == "cached-tile", "aerial_cached_source_type", "aerial picture lacks the current official cached-tile provenance")
            require(metadata["day_id"] == ident and metadata["photo_id"] == photo_id and abs(float(metadata["center_longitude"]) - point[0]) <= 1e-7 and abs(float(metadata["center_latitude"]) - point[1]) <= 1e-7 and abs(float(metadata["route_fraction"]) - fraction) <= 1e-9 and metadata["decoded_dimensions"] == dimensions and metadata["image_sha256"] == photo["image_sha256"] and metadata["image_bytes"] == len(raw), "aerial_request_identity", "cached tile belongs to a different route point/fraction/image")
            verify_cached_tile(root, photo, ident, point, assignment, metadata, dimensions, index, sources, require)
            if Image is None:
                raise ValueError("Pillow is required to independently decode cached photographs")
            with Image.open(safe_path(root, relative)) as image:
                image.load()
                decoded_mime = {"JPEG": "image/jpeg", "PNG": "image/png"}.get(image.format)
                require(decoded_mime is not None and record["mime"] == decoded_mime and metadata["provider_response"]["mime"] == decoded_mime and list(image.size) == dimensions, "decoded_aerial_dimensions", "decoded original image format/dimensions differ from publication metadata")
                sample = image.convert("RGB")
                sample.thumbnail((96, 96))
                pixels = sample.get_flattened_data() if hasattr(sample, "get_flattened_data") else sample.getdata()
                require(len(set(pixels)) >= 32, "aerial_nonblank_pixels", "aerial photograph is blank or nearly uniform")
        else:
            raise ValueError("photo has neither explicit ground nor aerial classification")
    except (KeyError, ValueError, TypeError, OSError, ZeroDivisionError) as exc:
        failures.append(f"photo verification could not complete: {type(exc).__name__}: {exc}")
    return {"photo_id": photo_id, "media_kind": photo.get("media_kind"), "passed": not failures, "local_cache_required": require_local, "checks": checks, "failures": failures}


def verify_project(root):
    root = root.resolve()
    manifest = json.loads((root / "content" / "leg_photo_manifest.json").read_text(encoding="utf-8"))
    visuals_raw = (root / "content" / "visuals.json").read_bytes()
    visuals = json.loads(visuals_raw)
    itinerary_raw = (root / "content" / "itinerary.json").read_bytes()
    itinerary = json.loads(itinerary_raw)
    frozen = json.loads((root / "tests" / "fixtures" / "topography_baseline.json").read_text(encoding="utf-8"))
    failures = []
    if manifest["itinerary_sha256"] != sha(itinerary_raw) or sha(itinerary_raw) != frozen["itinerary_sha256"]:
        failures.append("Photo edition itinerary differs from independent frozen original")
    if manifest["route_release"] != itinerary["metadata"]["route_release"] or manifest["route_release"] != frozen["route_release"]:
        failures.append("Photo edition route release differs from frozen route authority")
    if manifest["visuals_sha256"] != sha(visuals_raw):
        failures.append("Photo edition does not hash current visual cards")
    if manifest["minimum_photos_per_leg"] != 10:
        failures.append("Photo edition does not declare the requested ten-picture minimum")
    stages = {s["id"]: s for s in itinerary["stages"]}
    expected_ids = {f"day-{i:03d}" for i in range(1, 267)}
    rows = manifest["days"]
    if len(rows) != 266 or {r["day_id"] for r in rows} != expected_ids:
        failures.append("Photo manifest does not contain all266 unique day IDs")
    cards = {r["day_id"]: r for r in visuals["days"]}
    routes = {}
    for ident, stage in stages.items():
        raw = safe_path(root, stage["geometry_path"]).read_bytes()
        if sha(raw) != frozen["days"][ident]["geojson_sha256"]:
            failures.append(f"Photo assignment source route changed: {ident}")
        routes[ident] = json.loads(raw)["geometry"]["coordinates"]
    index, sources = RouteIndex(routes), PublicSourceReader(root)
    seen_ids, seen_ground_urls, seen_aerial_centers, seen_aerial_extents, seen_aerial_hashes, seen_all_cached_hashes = set(), set(), set(), set(), set(), set()
    used_files = set()
    results = []
    for row in rows:
        ident = row["day_id"]
        photos = cards[ident]["photos"]
        day_failures = []
        ground = sum(p.get("media_kind") == "ground" for p in photos)
        aerial = sum(p.get("media_kind") == "aerial" for p in photos)
        if len(photos) < 10 or row["photo_count"] != len(photos) or row["ground_photo_count"] != ground or row["aerial_photo_count"] != aerial or row["photo_ids"] != [p["id"] for p in photos] or row["minimum_met"] is not True or row.get("gap_reason") is not None:
            day_failures.append("Actual photo cards and declared ten-picture/count/ID coverage disagree")
        photo_results = []
        for photo in photos:
            photo_id = photo["id"]
            if photo_id in seen_ids:
                day_failures.append(f"Photo ID reused across legs: {photo_id}")
            seen_ids.add(photo_id)
            if photo.get("media_kind") == "ground":
                source_url = photo.get("original_url")
                if source_url in seen_ground_urls:
                    day_failures.append(f"Ground original source URL reused: {source_url}")
                seen_ground_urls.add(source_url)
            elif photo.get("media_kind") == "aerial":
                center = round(float(photo["longitude"]), 7), round(float(photo["latitude"]), 7)
                frame = tuple(round(v, 9) for v in extent_values(photo["actual_extent"]))
                digest = photo["image_sha256"]
                if center in seen_aerial_centers or frame in seen_aerial_extents or digest in seen_aerial_hashes:
                    day_failures.append(f"Aerial center/frame/image duplicates another published picture: {photo_id}")
                seen_aerial_centers.add(center)
                seen_aerial_extents.add(frame)
                seen_aerial_hashes.add(digest)
            if photo.get("media_kind") in ("ground", "aerial"):
                used_files.add(urlparse(photo["thumbnail_url"]).path.lstrip("/"))
                digest = photo.get("image_sha256")
                if digest in seen_all_cached_hashes:
                    day_failures.append(f"Byte-identical picture reused in catalog: {photo_id}")
                seen_all_cached_hashes.add(digest)
            photo_results.append(verify_photo(root, photo, ident, stages[ident], index, sources, manifest["files"]))
        results.append({"day_id": ident, "photo_count": len(photos), "ground_photo_count": ground, "aerial_photo_count": aerial, "passed": not day_failures and all(p["passed"] for p in photo_results), "failures": day_failures, "photos": photo_results})
    if used_files != set(manifest["files"]):
        failures.append("Photo file manifest contains missing/unreferenced cached images")
    return {"passed": not failures and len(results) == 266 and all(r["passed"] for r in results), "checked_days": len(results), "passed_days": sum(r["passed"] for r in results), "checked_photos": sum(r["photo_count"] for r in results), "ground_photo_count": sum(r["ground_photo_count"] for r in results), "aerial_photo_count": sum(r["aerial_photo_count"] for r in results), "global_failures": failures, "days": results, "scope": "Minimum ten distinct geographically assigned locally decoded pictures for every immutable leg; provider-geotag/nearest-leg evidence and cached original thumbnail integrity for ground photos, official tile-matrix/center/nearest-leg/trail-witness registration and cached original JPEG/PNG integrity for explicitly labeled aerial context. Does not claim all images are ground photography, photographed trail visibility, field verification, live conditions, or comprehensive rights compliance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = verify_project(args.root)
    except (KeyError, ValueError, TypeError, OSError) as exc:
        report = {"passed": False, "global_failures": [f"Verification input is unavailable/invalid: {type(exc).__name__}: {exc}"]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "days"}, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
