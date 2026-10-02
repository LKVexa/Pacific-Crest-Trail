"""Publish a separately sourced USGS topographic edition of the pinned daily maps.

Uses only Python's standard library. No itinerary, route or campaign writes.
Run with --download to acquire official exports; rerun offline using the cache.
The server's returned geographic extent, not the requested extent, locates pixels.
"""
import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SERVICE = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
BOX = (45, 78, 740, 490)
HEADERS = {'User-Agent': 'TrailDossier/1.0 local-training-topographic-cache'}
CONTOURS = 'Contour detail and interval vary with location and zoom; raster elevation-label units are not independently verified.'
TERRAIN = 'Cached topographic context, not live conditions or a measured elevation profile. Virtual checkpoints are not verified stopping places.'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def atomic(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.topography.tmp')
    temporary.write_bytes(raw)
    os.replace(temporary, path)


def write_json(path, data):
    atomic(path, (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())


def fetch(url, maximum=24 * 1024 * 1024):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'basemap.nationalmap.gov':
        raise ValueError('Only the official USGS export host may be downloaded')
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=90) as response:
                final = urllib.parse.urlsplit(response.geturl())
                if final.scheme != 'https' or final.hostname != parsed.hostname:
                    raise ValueError('Unexpected export redirect')
                raw = response.read(maximum + 1)
                if len(raw) > maximum:
                    raise ValueError('Export exceeds size limit')
                return raw
        except (OSError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def projection(points):
    xmin, xmax = min(p[0] for p in points), max(p[0] for p in points)
    ymin, ymax = min(p[1] for p in points), max(p[1] for p in points)
    midx, midy = (xmin + xmax) / 2, (ymin + ymax) / 2
    cosine = math.cos(math.radians(midy))
    factor = min(BOX[2] / max((xmax - xmin) * cosine, .003), BOX[3] / max(ymax - ymin, .003)) * .86

    def project(lon, lat):
        return BOX[0] + BOX[2] / 2 + (lon - midx) * cosine * factor, BOX[1] + BOX[3] / 2 - (lat - midy) * factor

    bbox = [midx - BOX[2] / 2 / factor / cosine, midy - BOX[3] / 2 / factor,
            midx + BOX[2] / 2 / factor / cosine, midy + BOX[3] / 2 / factor]
    return project, bbox


def png_size(raw):
    if raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
        raise ValueError('Source is not a PNG image')
    width, height = struct.unpack('>II', raw[16:24])
    if not 1 <= width <= 4096 or not 1 <= height <= 4096:
        raise ValueError('PNG dimensions exceed service limits')
    return width, height


def acquire(root, stage, download):
    points = json.loads((root / stage['geometry_path']).read_text(encoding='utf-8'))['geometry']['coordinates']
    project, bbox = projection(points)
    # The geographic image has degree-aspect pixels; its affine placement converts
    # longitude to the existing local cosine-corrected map coordinate system.
    height = 980
    width = max(1, min(4096, round(height * (bbox[2] - bbox[0]) / (bbox[3] - bbox[1]))))
    size = [width, height]
    source_dir = root / 'content/sources/topography'
    image_path = source_dir / (stage['id'] + '.png')
    metadata_path = source_dir / (stage['id'] + '.json')
    params = {'bbox': ','.join(format(v, '.14f') for v in bbox), 'bboxSR': '4326', 'imageSR': '4326',
              'size': f'{width},{height}', 'format': 'png32', 'transparent': 'false', 'dpi': '96', 'f': 'json'}
    url = SERVICE + '/export?' + urllib.parse.urlencode(params)
    if metadata_path.exists() and image_path.exists():
        record = json.loads(metadata_path.read_text(encoding='utf-8'))
        if record['request']['url'] != url:
            raise ValueError(stage['id'] + ': cached export belongs to different bounds; retain old cache and use a separate output directory')
        raw = image_path.read_bytes()
        if sha(raw) != record['image_sha256']:
            raise ValueError(stage['id'] + ': cached PNG checksum mismatch')
    else:
        if not download:
            raise ValueError(stage['id'] + ': no verified cache; use --download')
        response = json.loads(fetch(url))
        if response.get('error'):
            raise ValueError(str(response['error']))
        extent = response['extent']
        if extent.get('spatialReference', {}).get('wkid') != 4326:
            raise ValueError('Export did not return WGS84 geographic coordinates')
        raw = fetch(response['href'])
        record = {'request': {'url': url, 'bbox': bbox, 'size': size}, 'response': response,
                  'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'image_sha256': sha(raw)}
        if list(png_size(raw)) != [response['width'], response['height']]:
            raise ValueError('Export image dimensions disagree with server metadata')
        atomic(image_path, raw)
        write_json(metadata_path, record)
        time.sleep(.25)
    response = record['response']
    extent = response['extent']
    # Rounding can move a bbox boundary by a fraction of a raster pixel.
    tolerance = max(bbox[2] - bbox[0], bbox[3] - bbox[1]) / min(size) * .51
    if extent['xmin'] > bbox[0] + tolerance or extent['ymin'] > bbox[1] + tolerance or extent['xmax'] < bbox[2] - tolerance or extent['ymax'] < bbox[3] - tolerance:
        raise ValueError('Returned extent does not cover the daily map')
    if list(png_size(raw)) != [response['width'], response['height']]:
        raise ValueError('Invalid cached image dimensions')
    return stage, project, bbox, raw, record


def publish_map(root, acquired):
    stage, project, bbox, raw, record = acquired
    map_path = root / stage['map_path']
    baseline_path = root / 'content/sources/topography/route-only' / (stage['id'] + '.svg')
    if not baseline_path.exists():
        original = map_path.read_bytes()
        if b'id="usgs-topography"' in original:
            raise ValueError('Cannot use an already published topographic map as route-only baseline')
        atomic(baseline_path, original)
    original = baseline_path.read_bytes()
    svg = ET.fromstring(original)
    plot = next(g for g in svg.findall(f'{{{NS}}}g') if g.get('clip-path') == 'url(#plot)')
    route = next(p for p in plot.findall(f'{{{NS}}}path') if p.get('stroke') == '#70e9eb')
    route_digest = sha(route.attrib['d'].encode())
    extent = record['response']['extent']
    x, y = project(extent['xmin'], extent['ymax'])
    right, bottom = project(extent['xmax'], extent['ymin'])
    raster = ET.Element(f'{{{NS}}}image', {'id': 'usgs-topography', 'x': f'{x:.6f}', 'y': f'{y:.6f}',
                       'width': f'{right-x:.6f}', 'height': f'{bottom-y:.6f}', 'preserveAspectRatio': 'none',
                       'href': 'data:image/png;base64,' + base64.b64encode(raw).decode()})
    # Preserve filled regional boundaries beneath the raster and all route overlays above it.
    insertion = next((i for i, child in enumerate(plot) if child.get('fill') != '#0d2435'), len(plot))
    plot.insert(insertion, raster)
    # Dark halo makes the cyan trail and checkpoints legible against natural topo colors.
    halo = ET.Element(f'{{{NS}}}path', dict(route.attrib))
    halo.set('id', 'topography-route-halo')
    halo.set('stroke', '#071e2c')
    halo.set('stroke-width', '7.8')
    plot.insert(list(plot).index(route), halo)
    for child in plot:
        if child.get('stroke-width') in ('.6', '0.6'):
            child.set('stroke-opacity', '.22')
        if child.tag == f'{{{NS}}}circle' and child.get('fill') == '#70e9eb':
            child.set('stroke', '#071e2c')
        if child.tag == f'{{{NS}}}rect' and child.get('fill') == '#f5b867':
            child.set('stroke', '#071e2c')
    # Scale and north arrow are outside the clipped plot group in the baseline.
    for child in svg:
        if child.tag == f'{{{NS}}}path' and child.get('stroke') == '#eaf7ff':
            child.set('stroke', '#071e2c')
        if child.tag == f'{{{NS}}}text' and child.get('fill') == '#eaf7ff' and float(child.get('y', '0')) > 78 and float(child.get('x', '0')) < 785:
            child.set('fill', '#071e2c')
    description = svg.find(f'{{{NS}}}desc')
    description.text = 'North-up USGS topographic map with contour lines, shaded relief and the sourced daily trail overlay. Cyan route, circular start, square finish, whole-mile points and regional locator. ' + CONTOURS + ' ' + TERRAIN
    svg.set('height', '710')
    svg.set('viewBox', '0 0 1120 710')
    background = svg.find(f'{{{NS}}}rect')
    background.set('height', '710')
    for y_pos, caption in [(676, 'Topography: USGS / The National Map · Cached official USGSTopo export · Contour detail and interval vary with location and zoom.'),
                           (695, 'Topographic context only · No route elevation gain or treadmill incline is inferred · Cached ' + record['retrieved_utc'][:10])]:
        credit = ET.SubElement(svg, f'{{{NS}}}text', {'x': '45', 'y': str(y_pos), 'font-family': 'Segoe UI,Arial', 'font-size': '11', 'fill': '#a5c5d7'})
        credit.text = caption
    published = ET.tostring(svg, encoding='utf-8') + b'\n'
    atomic(map_path, published)
    return {'day_id': stage['id'], 'map_path': stage['map_path'], 'topographic': True, 'map_revision': sha(published)[:16],
            'source_ids': ['usgs-topo'], 'source_date': record['retrieved_utc'], 'elevation_unit': None,
            'contour_note': CONTOURS, 'terrain_note': TERRAIN, 'requested_bbox': bbox, 'export_extent': extent,
            'image_size': list(png_size(raw)), 'image_sha256': sha(raw), 'published_map_sha256': sha(published),
            'route_path_sha256': route_digest, 'baseline_sha256': sha(original),
            'baseline_path': baseline_path.relative_to(root).as_posix(),
            'source_image_path': f"content/sources/topography/{stage['id']}.png",
            'export_metadata_path': f"content/sources/topography/{stage['id']}.json",
            'export_metadata_sha256': sha((root / f"content/sources/topography/{stage['id']}.json").read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--download', action='store_true', help='Acquire missing official USGS exports over HTTPS')
    parser.add_argument('--days', help='Comma-separated day numbers for a preview; publish full edition without this option')
    args = parser.parse_args()
    root = args.root.resolve()
    itinerary_raw = (root / 'content/itinerary.json').read_bytes()
    itinerary = json.loads(itinerary_raw)
    stages = itinerary['stages']
    if args.days:
        numbers = {int(number) for number in args.days.split(',')}
        stages = [s for s in stages if s['day_number'] in numbers]
    source_dir = root / 'content/sources/topography'
    metadata_path = source_dir / 'service.json'
    if not metadata_path.exists():
        if not args.download:
            raise ValueError('Missing official service metadata; use --download')
        atomic(metadata_path, fetch(SERVICE + '?f=pjson', 2 * 1024 * 1024))
    rows = []
    # Two in-flight exports at most; retry/backoff and verified cache make reruns gentle.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(acquire, root, stage, args.download): stage for stage in stages}
        for future in concurrent.futures.as_completed(futures):
            row = publish_map(root, future.result())
            rows.append(row)
            print(f"{row['day_id']}: official topo cached and geographically aligned ({len(rows)}/{len(stages)})", flush=True)
    rows.sort(key=lambda r: r['day_id'])
    previous_path = root / 'content/topography.json'
    if previous_path.exists():
        previous = json.loads(previous_path.read_text(encoding='utf-8'))
        if previous.get('itinerary_sha256') != sha(itinerary_raw):
            raise ValueError('Previous publication belongs to another itinerary')
        by_day = {r['day_id']: r for r in previous['days']}
        by_day.update({r['day_id']: r for r in rows})
        rows = sorted(by_day.values(), key=lambda r: r['day_id'])
    revision = sha(''.join(row['published_map_sha256'] for row in rows).encode())[:16]
    service = json.loads(metadata_path.read_text(encoding='utf-8'))
    publication = {'version': 1, 'route_release': itinerary['metadata']['route_release'], 'itinerary_sha256': sha(itinerary_raw),
                   'map_revision': revision, 'published_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'projection': 'Existing local equirectangular route coordinates; USGS WGS84 export georeferenced using its returned extent',
                   'sources': [{'id': 'usgs-topo', 'title': 'USGS / The National Map — USGSTopo', 'url': SERVICE,
                                'attribution': service.get('copyrightText') or 'USGS / The National Map',
                                'service_metadata_path': 'content/sources/topography/service.json', 'service_metadata_sha256': sha(metadata_path.read_bytes())}],
                   'coverage_count': len(rows), 'days': rows}
    if (root / 'content/itinerary.json').read_bytes() != itinerary_raw:
        raise ValueError('Itinerary changed during topographic publication')
    write_json(previous_path, publication)
    # Route inventory keeps exactly its established members; new source assets have
    # their own individually hashed sidecar instead of changing route identity.
    inventory_path = root / 'content/asset_manifest.json'
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    for row in rows:
        content = (root / row['map_path']).read_bytes()
        inventory['files'][row['map_path']] = {'sha256': sha(content), 'bytes': len(content)}
        dossier_path = root / f"content/dossiers/{row['day_id']}.html"
        dossier = dossier_path.read_text(encoding='utf-8')
        dossier = dossier.replace('alt="North-up mapped trail section with start and finish checkpoints and full-trail locator"',
                                  'alt="North-up USGS topographic trail section with contour lines, shaded relief, start and finish checkpoints and full-trail locator"')
        dossier = dossier.replace('The map does not verify campsites, water, elevation, or current trail conditions.',
                                  'The cached USGS topographic map shows contour lines and shaded relief. Contour detail and interval vary with location and map scale. It does not verify campsites, water, or current trail conditions, and it does not supply a measured route elevation profile.')
        if 'id="topography-credit"' not in dossier:
            dossier = dossier.replace('</small></footer>', '<br><span id="topography-credit">Topography: <a href="' + SERVICE + '">U.S. Geological Survey / The National Map — USGSTopo</a>. Cached official export; raster elevation-label units not independently verified. Full source attribution and retrieval details: <a href="/api/topography">topographic publication record</a>.</span></small></footer>')
        dossier_raw = dossier.encode('utf-8')
        atomic(dossier_path, dossier_raw)
        inventory['files'][dossier_path.relative_to(root).as_posix()] = {'sha256': sha(dossier_raw), 'bytes': len(dossier_raw)}
    write_json(inventory_path, inventory)
    print(f'Published {len(rows)} topographic days. Pinned itinerary and campaign data unchanged.', flush=True)


if __name__ == '__main__':
    main()
