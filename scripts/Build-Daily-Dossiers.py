from __future__ import annotations

import argparse
import bisect
import csv
import gzip
import hashlib
import html
import json
import math
import shutil
import time
from array import array
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Rebuild the pinned 266-day route content into an empty output directory, preserving the running application.')
parser.add_argument('--output-dir', required=True, type=Path)
arguments = parser.parse_args()
REPO = arguments.output_dir.resolve()
if REPO == ROOT or (REPO.exists() and any(REPO.iterdir())):
    raise SystemExit('Choose an empty output directory; existing app content and saved hike history are never overwritten.')
SOURCE = REPO / '_source_work'
SOURCE.mkdir(parents=True, exist_ok=True)
for archived in (ROOT / 'content' / 'sources').glob('*.json.gz'):
    with gzip.open(archived, 'rb') as stream:
        (SOURCE / archived.name[:-3]).write_bytes(stream.read())
for name in ('centerline','markers_2026'):
    meta = json.loads((SOURCE / (name + '_metadata.json')).read_text(encoding='utf-8'))
    features = []
    for batch in sorted(SOURCE.glob(name + '_batch_*.json')):
        features.extend(json.loads(batch.read_text(encoding='utf-8'))['features'])
    (SOURCE / (name + '_combined.json')).write_text(json.dumps({'metadata':meta,'features':features},separators=(',',':')),encoding='utf-8')
CONTENT = REPO / 'content'
TOTAL = 2655.84
TARGET = 10.0
RADIUS = 6371008.8
METRES_PER_MILE = 1609.344
SOURCE_PAGE = 'https://www.pcta.org/discover-the-trail/maps/pct-data/'
for folder in ('maps','routes','dossiers','sources'):
    (CONTENT / folder).mkdir(parents=True, exist_ok=True)

def haversine(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return RADIUS * 2 * math.asin(min(1.0, math.sqrt(h)))

raw = json.loads((SOURCE / 'centerline_combined.json').read_text(encoding='utf-8'))
paths = [path for feature in raw['features'] for path in feature['geometry']['paths']]
assert len(paths) == 1, 'Multipart route requires explicit connection review'
coordinates = [p[:2] for p in paths[0]]
assert all(math.isfinite(v) for p in coordinates for v in p)
assert coordinates[0][1] < 33 and coordinates[-1][1] > 48.99
cumulative = array('d', [0.0])
maximum_segment = (0.0, 0)
for i, (a,b) in enumerate(zip(coordinates, coordinates[1:])):
    length = haversine(a,b)
    cumulative.append(cumulative[-1] + length)
    if length > maximum_segment[0]: maximum_segment = (length,i)
assert maximum_segment[0] < 1000, ('Unreviewed route discontinuity',maximum_segment)

# The grid indexes route segments in blocks of eight original vertices. Projection
# is refined against every original segment in the winning neighborhood.
CELL = 0.01
BLOCK = 8
grid = defaultdict(list)
for start in range(0,len(coordinates)-1,BLOCK):
    points = coordinates[start:min(start+BLOCK+1,len(coordinates))]
    xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
    ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
    for gx in range(math.floor(xmin/CELL), math.floor(xmax/CELL)+1):
        for gy in range(math.floor(ymin/CELL), math.floor(ymax/CELL)+1):
            grid[(gx,gy)].append(start)

def project_marker(point, previous_distance):
    gx, gy = math.floor(point[0]/CELL), math.floor(point[1]/CELL)
    blocks = set()
    for dx in (-1,0,1):
        for dy in (-1,0,1): blocks.update(grid.get((gx+dx,gy+dy),()))
    cx = math.cos(math.radians(point[1]))
    best = (float('inf'),None,None,None)
    for start in blocks:
        if cumulative[min(start+BLOCK,len(coordinates)-1)] < previous_distance-1500: continue
        for i in range(start,min(start+BLOCK,len(coordinates)-1)):
            a,b = coordinates[i],coordinates[i+1]
            ax,ay=(a[0]-point[0])*cx,a[1]-point[1]
            bx,by=(b[0]-point[0])*cx,b[1]-point[1]
            dx,dy=bx-ax,by-ay
            denominator=dx*dx+dy*dy
            t=max(0,min(1,-(ax*dx+ay*dy)/denominator)) if denominator else 0
            ex,ey=ax+t*dx,ay+t*dy
            squared=ex*ex+ey*ey
            pos=cumulative[i]+t*(cumulative[i+1]-cumulative[i])
            if pos <= previous_distance: continue
            if squared < best[0]: best=(squared,pos,i,t)
    assert best[1] is not None, ('Marker cannot be resolved monotonically',point)
    pos,i,t=best[1:]
    a,b=coordinates[i],coordinates[i+1]
    projected=[a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]
    return pos,projected,haversine(point,projected)

marker_raw = json.loads((SOURCE / 'markers_2026_combined.json').read_text(encoding='utf-8'))
excluded = []
markers = []
for feature in marker_raw['features']:
    attrs=feature['attributes']
    geom=feature.get('geometry')
    if not geom or geom.get('x') is None or geom.get('y') is None:
        excluded.append({'object_id':attrs['OBJECTID'],'mile':attrs['Mile'],'reason':'No spatial geometry; unusable for route calibration'})
        continue
    assert attrs['RouteID']=='PCT'
    markers.append((float(attrs['Mile']),[geom['x'],geom['y']],attrs['OBJECTID']))
markers.sort()
assert len(markers)==5311 and markers[-1][0]==2655.5
assert [m[0] for m in markers] == [i/2 for i in range(1,5312)]
anchors=[(0.0,0.0,coordinates[0],0.0)]
previous=-1.0
max_offset=0.0
for number,(mile,point,oid) in enumerate(markers):
    distance,projected,offset=project_marker(point,previous)
    assert offset < 100, ('Marker too far from centerline',mile,offset)
    max_offset=max(max_offset,offset)
    anchors.append((mile,distance,projected,offset))
    previous=distance
    if number % 1000 == 0: print('Calibrated markers',number+1,flush=True)
anchors.append((TOTAL,cumulative[-1],coordinates[-1],0.0))
assert all(a[1]<b[1] and a[0]<b[0] for a,b in zip(anchors,anchors[1:]))
anchor_miles=[a[0] for a in anchors]

def locate_mile(mile):
    n=bisect.bisect_left(anchor_miles,mile)
    if n<len(anchors) and abs(anchors[n][0]-mile)<1e-8:
        return anchors[n][1],anchors[n][2]
    left,right=anchors[n-1],anchors[n]
    fraction=(mile-left[0])/(right[0]-left[0])
    distance=left[1]+fraction*(right[1]-left[1])
    i=min(bisect.bisect_right(cumulative,distance)-1,len(coordinates)-2)
    a,b=coordinates[i],coordinates[i+1]
    length=cumulative[i+1]-cumulative[i]
    t=(distance-cumulative[i])/length if length else 0
    return distance,[a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]

def clip_route(start_mile,end_mile):
    da,pa=locate_mile(start_mile)
    db,pb=locate_mile(end_mile)
    first=bisect.bisect_right(cumulative,da)
    last=bisect.bisect_left(cumulative,db)
    return [pa]+coordinates[first:last]+[pb]

def simplify(points,tolerance=4.0):
    # Iterative Douglas-Peucker in local metre coordinates; endpoints never move.
    coslat=math.cos(math.radians(sum(p[1] for p in points)/len(points)))
    factor=RADIUS*math.pi/180
    xys=[(p[0]*factor*coslat,p[1]*factor) for p in points]
    keep={0,len(points)-1}
    pending=[(0,len(points)-1)]
    limit=tolerance*tolerance
    while pending:
        lo,hi=pending.pop()
        if hi<=lo+1: continue
        ax,ay=xys[lo]; bx,by=xys[hi]
        dx,dy=bx-ax,by-ay; denominator=dx*dx+dy*dy
        worst=-1; selected=None
        for i in range(lo+1,hi):
            px,py=xys[i]
            t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/denominator)) if denominator else 0
            error=(px-ax-t*dx)**2+(py-ay-t*dy)**2
            if error>worst: worst,selected=error,i
        if worst>limit:
            keep.add(selected); pending.extend(((lo,selected),(selected,hi)))
    return [points[i] for i in sorted(keep)]

topology=json.loads((SOURCE/'states_2017_us_atlas_3_0_1.json').read_text())
scale,translate=topology['transform']['scale'],topology['transform']['translate']
decoded=[]
for arc in topology['arcs']:
    x=y=0; points=[]
    for dx,dy in arc:
        x+=dx; y+=dy; points.append([x*scale[0]+translate[0],y*scale[1]+translate[1]])
    decoded.append(points)

def ring_from_arcs(indices):
    ring=[]
    for value in indices:
        arc=decoded[value] if value>=0 else list(reversed(decoded[~value]))
        ring.extend(arc if not ring else arc[1:])
    return ring

states={}
for geom in topology['objects']['states']['geometries']:
    if geom['id'] not in ('06','41','53'): continue
    polygons=geom['arcs'] if geom['type']=='MultiPolygon' else [geom['arcs']]
    states[geom['properties']['name']]=[[ring_from_arcs(r) for r in polygon] for polygon in polygons]

def point_in_ring(point,ring):
    x,y=point; inside=False
    for a,b in zip(ring,ring[1:]+ring[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: inside=not inside
    return inside

def state_at(point):
    for name,polygons in states.items():
        for polygon in polygons:
            if point_in_ring(point,polygon[0]) and not any(point_in_ring(point,r) for r in polygon[1:]): return name
    return None

def coordinate_record(p): return {'latitude':round(p[1],7),'longitude':round(p[0],7),'kind':'virtual_checkpoint'}

OVERVIEW=simplify(coordinates,300)
def projection(points,box):
    xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
    ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
    midlat=(ymin+ymax)/2
    coslat=math.cos(math.radians(midlat))
    xspan=max((xmax-xmin)*coslat,.003)
    yspan=max(ymax-ymin,.003)
    factor=min(box[2]/xspan,box[3]/yspan)*.86
    midx,midy=(xmin+xmax)/2,(ymin+ymax)/2
    def project(p): return (box[0]+box[2]/2+(p[0]-midx)*coslat*factor,box[1]+box[3]/2-(p[1]-midy)*factor)
    return project,factor,coslat,(xmin,xmax,ymin,ymax)

def svg_path(points,project):
    return ' '.join(('M' if i==0 else 'L')+f'{project(p)[0]:.2f},{project(p)[1]:.2f}' for i,p in enumerate(points))

def svg_states(project):
    result=[]
    for name,polygons in states.items():
        d=' '.join(svg_path(r,project)+' Z' for polygon in polygons for r in polygon)
        result.append(f'<path d="{d}" fill="#0d2435" stroke="#355b75" stroke-width="0.7" fill-rule="evenodd"/>')
    return ''.join(result)

def fmtmile(value): return f'{value:,.2f}'.rstrip('0').rstrip('.')

def build_map(stage,points,context):
    box=(45,78,740,490)
    project,factor,coslat,bounds=projection(points,box)
    west,east,south,north=bounds
    inverse_lon=lambda pixel: (pixel-(box[0]+box[2]/2))/factor/coslat+(west+east)/2
    inverse_lat=lambda pixel: -(pixel-(box[1]+box[3]/2))/factor+(south+north)/2
    xmin,xmax=inverse_lon(box[0]),inverse_lon(box[0]+box[2])
    ymin,ymax=inverse_lat(box[1]+box[3]),inverse_lat(box[1])
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="670" viewBox="0 0 1120 670" role="img" aria-labelledby="title desc"><title id="title">Day {stage["day_number"]}: Trail miles {fmtmile(stage["mile_start"])} to {fmtmile(stage["mile_end"])}</title><desc id="desc">North-up map of the sourced trail section. Cyan route, circular start, square finish, whole-mile points, neighboring trail and regional locator. Virtual checkpoints; no campsite or elevation claims.</desc>',
         '<defs><clipPath id="plot"><rect x="45" y="78" width="740" height="490" rx="8"/></clipPath><clipPath id="locator"><rect x="820" y="95" width="260" height="450" rx="8"/></clipPath></defs>',
         '<rect width="1120" height="670" fill="#06121c"/>',
         f'<text x="45" y="35" font-family="Segoe UI,Arial" font-size="23" fill="#eaf7ff" font-weight="600">DAY {stage["day_number"]:03d} / {html.escape(stage["region"])} </text>',
         f'<text x="45" y="60" font-family="Segoe UI,Arial" font-size="16" fill="#a5c5d7">Trail miles {fmtmile(stage["mile_start"])}–{fmtmile(stage["mile_end"])} · {fmtmile(stage["distance_miles"])} virtual trail miles</text>',
         '<rect x="45" y="78" width="740" height="490" rx="8" fill="#0a1c2b"/>',
         '<g clip-path="url(#plot)">',svg_states(project)]
    for i in range(1,5):
        x=box[0]+i*box[2]/5; y=box[1]+i*box[3]/5
        svg.append(f'<path d="M{x:.1f} 78 V568 M45 {y:.1f} H785" stroke="#17364b" stroke-width="0.6"/>')
    svg += [f'<path d="{svg_path(context,project)}" fill="none" stroke="#4b6f87" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{svg_path(points,project)}" fill="none" stroke="#70e9eb" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>']
    for mile in range(math.ceil(stage['mile_start']),math.floor(stage['mile_end'])+1):
        _,position=locate_mile(float(mile)); x,y=project(position)
        if stage['mile_start']<mile<stage['mile_end']:
            svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="#0a1c2b" stroke="#70e9eb" stroke-width="1.4"/>')
    sx,sy=project(points[0]); ex,ey=project(points[-1])
    svg += [f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="7" fill="#70e9eb" stroke="#eaf7ff" stroke-width="2"/>',
            f'<rect x="{ex-7:.2f}" y="{ey-7:.2f}" width="14" height="14" fill="#f5b867" stroke="#eaf7ff" stroke-width="2"/>','</g>']
    for i in (0,2,4):
        x=box[0]+i*box[2]/4; y=box[1]+i*box[3]/4
        svg.append(f'<text x="{x:.1f}" y="588" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" fill="#a5c5d7">{abs(inverse_lon(x)):.3f}°W</text>')
        svg.append(f'<text x="12" y="{y+4:.1f}" font-family="Segoe UI,Arial" font-size="11" fill="#a5c5d7" transform="rotate(-90 12 {y+4:.1f})" text-anchor="middle">{inverse_lat(y):.3f}°N</text>')
    svg += ['<path d="M751 136 V102 M743 113 L751 102 L759 113" fill="none" stroke="#eaf7ff" stroke-width="2"/><text x="751" y="96" text-anchor="middle" font-family="Segoe UI,Arial" font-size="14" fill="#eaf7ff">N</text>']
    metres_per_pixel=(math.pi/180*RADIUS)/factor
    scale_miles=1.0 if 1*METRES_PER_MILE/metres_per_pixel<180 else .5
    bar=scale_miles*METRES_PER_MILE/metres_per_pixel
    svg.append(f'<path d="M66 540 V549 H{66+bar:.1f} V540" fill="none" stroke="#eaf7ff" stroke-width="2"/><text x="66" y="531" font-family="Segoe UI,Arial" font-size="13" fill="#eaf7ff">≈ {scale_miles:g} geographic mile</text>')
    svg += ['<rect x="820" y="95" width="260" height="450" rx="8" fill="#0a1c2b"/>','<g clip-path="url(#locator)">']
    locator,_,_,_=projection([[-124.7,32.4],[-116,49.15]],(825,105,250,430))
    svg += [svg_states(locator),f'<path d="{svg_path(OVERVIEW,locator)}" fill="none" stroke="#456c84" stroke-width="1.4"/>',f'<path d="{svg_path(points,locator)}" fill="none" stroke="#70e9eb" stroke-width="3.5"/>']
    mx,my=locator(points[len(points)//2]); svg += [f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="5" fill="#f5b867" stroke="#eaf7ff" stroke-width="1.5"/>','</g>']
    for name,position in [('California',[-120,36.6]),('Oregon',[-121,44.3]),('Washington',[-121,47.4])]:
        x,y=locator(position); svg.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Segoe UI,Arial" font-size="13" fill="#a5c5d7">{name}</text>')
    svg += ['<text x="820" y="78" font-family="Segoe UI,Arial" font-size="15" fill="#eaf7ff">Your place on the whole trail</text>',
            '<circle cx="53" cy="615" r="5" fill="#70e9eb"/><text x="67" y="620" font-family="Segoe UI,Arial" font-size="14" fill="#a5c5d7">Start checkpoint</text>',
            '<rect x="252" y="610" width="10" height="10" fill="#f5b867"/><text x="273" y="620" font-family="Segoe UI,Arial" font-size="14" fill="#a5c5d7">Finish checkpoint</text>',
            '<path d="M465 615 H495" stroke="#4b6f87" stroke-width="3"/><text x="505" y="620" font-family="Segoe UI,Arial" font-size="14" fill="#a5c5d7">Neighboring trail</text>',
            '<text x="45" y="648" font-family="Segoe UI,Arial" font-size="12" fill="#a5c5d7">Route: Pacific Crest Trail Association, 2026 snapshot · CC BY 4.0 · Segmented and simplified for this training dossier.</text>',
            '<text x="820" y="565" font-family="Segoe UI,Arial" font-size="11" fill="#a5c5d7">Locator: Census 2017 / us-atlas 3.0.1</text>','</svg>']
    return ''.join(svg)

FOCUS=[
    'Find the start and finish symbols. Follow the route northbound and describe the largest change in direction.',
    'Use the geographic scale bar to compare straight-line separation with the winding trail path.',
    'Read the latitude and longitude grid. Identify which side of the map is north before tracing the section.',
    'Compare the local map with the whole-trail locator. Describe how this section connects to the previous day.',
    'Identify several bends or switchbacks in the mapped line. The route shape alone does not establish steepness.',
    'Locate the mile points along the route. Explain why a mile on a winding trail is longer than the separation of its endpoints.',
]
stages=[]
for day in range(1,math.ceil(TOTAL/TARGET)+1):
    start_mile=(day-1)*TARGET; end_mile=min(day*TARGET,TOTAL)
    original=clip_route(start_mile,end_mile)
    points=simplify(original,4)
    context=simplify(clip_route(max(0,start_mile-3),min(TOTAL,end_mile+3)),8)
    names=[]
    for mile in [start_mile+.1,(start_mile+end_mile)/2,end_mile-.1]:
        name=state_at(locate_mile(mile)[1])
        if name and name not in names:names.append(name)
    assert names,('Unresolved state region',day)
    region=' / '.join(names)
    ident=f'day-{day:03d}'
    stage={'id':ident,'day_number':day,'title':f'Day {day:03d} · PCT miles {fmtmile(start_mile)}–{fmtmile(end_mile)}',
        'mile_start':start_mile,'mile_end':end_mile,'distance_miles':round(end_mile-start_mile,2),'region':region,
        'start':coordinate_record(original[0]),'end':coordinate_record(original[-1]),
        'map_path':f'content/maps/{ident}.svg','dossier_path':f'content/dossiers/{ident}.html','geometry_path':f'content/routes/{ident}.geojson',
        'summary':f'Follow the mapped PCT northbound through {region}, from trail mile {fmtmile(start_mile)} to {fmtmile(end_mile)}.',
        'briefing':[f'This dossier covers {fmtmile(end_mile-start_mile)} virtual trail miles. Your treadmill workout distance is chosen separately.',
                    'The map follows the PCTA route. Start and finish symbols identify virtual checkpoints, not verified campsites.',
                    'Study the route, choose your own training session, and return to this same section until you deliberately complete it.'],
        'orientation_prompt':FOCUS[(day-1)%len(FOCUS)],
        'physical_training_target':None,'elevation_gain':None,'elevation_loss':None,'verified_campsite':None,
        'original_vertex_count':len(original),'map_vertex_count':len(points),'display_simplification_tolerance_metres':4.0,
        'geographic_distance_method':'PCTA 2026 marker-calibrated route mileage; published full-length endpoint 2655.84',
        'previous_day_id':f'day-{day-1:03d}' if day>1 else None,'next_day_id':f'day-{day+1:03d}' if end_mile<TOTAL else None}
    feature={'type':'Feature','properties':{'stage_id':ident,'mile_start':start_mile,'mile_end':end_mile,'source':SOURCE_PAGE,'license':'CC BY 4.0','simplification_metres':4},'geometry':{'type':'LineString','coordinates':[[round(p[0],7),round(p[1],7)] for p in points]}}
    (CONTENT/'routes'/f'{ident}.geojson').write_text(json.dumps(feature,separators=(',',':')),encoding='utf-8')
    (CONTENT/'maps'/f'{ident}.svg').write_text(build_map(stage,points,context),encoding='utf-8')
    stages.append(stage)
    if day % 50==0:print('Generated daily maps',day,flush=True)

assert len(stages)==266
assert stages[0]['mile_start']==0 and stages[-1]['mile_end']==TOTAL
assert all(a['mile_end']==b['mile_start'] and a['end']==b['start'] for a,b in zip(stages,stages[1:]))
assert abs(sum(s['distance_miles'] for s in stages)-TOTAL)<1e-6

# Full-trail locator map uses generalized boundaries and the actual PCTA line.
overview_project,_,_,_=projection([[-124.7,32.4],[-116,49.15]],(35,80,630,710))
overview=['<svg xmlns="http://www.w3.org/2000/svg" width="740" height="880" viewBox="0 0 740 880" role="img" aria-labelledby="title desc"><title id="title">TrailDossier: 266 virtual daily sections</title><desc id="desc">North-up sourced route through California, Oregon, and Washington, from the southern to northern terminus.</desc><rect width="740" height="880" fill="#06121c"/>',
          '<text x="35" y="38" font-family="Segoe UI,Arial" font-size="26" fill="#eaf7ff">FULL ROUTE SCAN</text><text x="35" y="65" font-family="Segoe UI,Arial" font-size="17" fill="#a5c5d7">266 dossiers · 10 virtual miles per section · 2,655.84 trail miles</text>',svg_states(overview_project),
          f'<path d="{svg_path(OVERVIEW,overview_project)}" fill="none" stroke="#70e9eb" stroke-width="3" stroke-linejoin="round"/>']
for name,point in [('California',[-120.5,36.7]),('Oregon',[-122,44]),('Washington',[-122,47.5])]:
    x,y=overview_project(point); overview.append(f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial" font-size="22" fill="#a5c5d7">{name}</text>')
for number in (1,50,100,150,200,250,266):
    stage=stages[number-1]; p=[stage['start']['longitude'],stage['start']['latitude']]; x,y=overview_project(p)
    overview.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#f5b867"/><text x="{x+12}" y="{y+4}" font-family="Segoe UI,Arial" font-size="14" fill="#eaf7ff">Day {number}</text>')
overview += ['<text x="35" y="830" font-family="Segoe UI,Arial" font-size="12" fill="#a5c5d7">Route: Pacific Crest Trail Association · 2026 snapshot · CC BY 4.0</text>', '<text x="35" y="851" font-family="Segoe UI,Arial" font-size="12" fill="#a5c5d7">Context: generalized Census 2017 boundaries / us-atlas 3.0.1. Training geography.</text>','</svg>']
(CONTENT/'maps'/'overview.svg').write_text(''.join(overview),encoding='utf-8')

manifest=json.loads((SOURCE/'manifest.json').read_text())
centerline_hash=hashlib.sha256((SOURCE/'centerline_batch_000.json').read_bytes()).hexdigest()
route_release='pcta-2026-'+centerline_hash[:12]
metadata={'route_release':route_release,'direction':'northbound','total_miles':TOTAL,'daily_target_miles':TARGET,'stage_count':len(stages),
          'source_url':SOURCE_PAGE,'source_organization':'Pacific Crest Trail Association','source_license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/',
          'retrieved_utc':manifest['retrieved_utc'],'centerline_sha256':centerline_hash,'centerline_source_vertex_count':len(coordinates),
          'centerline_data_last_edit_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(raw['metadata']['editingInfo']['dataLastEditDate']/1000)),
          'total_length_basis':'PCTA published January 2026 full-trail estimate; daily mile boundaries calibrated to spatial half-mile markers',
          'overview_map_path':'content/maps/overview.svg','training_target_policy':'Virtual section distance is not a required treadmill distance. One dossier may span multiple training sessions.',
          'stage_endpoint_policy':'Virtual checkpoints, not verified campsites, access points, or stopping recommendations',
          'completion_policy':'Deliberate manual completion of the current virtual dossier; no measured physical activity inferred',
          'map_projection':'Local equirectangular north-up projection; approximate geographic scale; locator boundaries generalized',
          'map_scope':'Route geography only; no elevation, terrain contours, current closures, water or campsite availability represented',
          'context_source':'Generalized US Census 2017 state boundaries redistributed in us-atlas 3.0.1',
          'source_exceptions':[{'kind':'nonspatial_markers','count':len(excluded),'mile_range':[2656,2660],'disposition':'Retained in source audit, excluded from spatial calibration'},
                               {'kind':'stale_service_description','disposition':'Service prose says 2025; geometry data edit date and PCTA publication are January 2026. Exact downloaded bytes pinned by hash.'}],
          'modifications':['Northbound mile-calibrated daily segmentation','4-metre display simplification preserving section endpoints','SVG map rendering and generalized state locator'],
          'physical_workout_records_created_by_generation':0}
(CONTENT/'itinerary.json').write_text(json.dumps({'metadata':metadata,'stages':stages},indent=2),encoding='utf-8')

for stage in stages:
    nav=[]
    if stage['previous_day_id']:nav.append(f'<a href="{stage["previous_day_id"]}.html">Previous section</a>')
    nav.append('<a href="/">Open TrailDossier</a>')
    if stage['next_day_id']:nav.append(f'<a href="{stage["next_day_id"]}.html">Next section</a>')
    display_title = stage['title'].replace('PCT miles', 'Trail miles')
    display_summary = stage['summary'].replace('mapped PCT northbound', 'mapped route northbound')
    display_briefing = [item.replace('The map follows the PCTA route.', 'The map follows the sourced route.') for item in stage['briefing']]
    doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TrailDossier · {html.escape(display_title)}</title><style>
html{{color-scheme:dark}}body{{margin:0;background:#06121c;color:#eaf7ff;font:17px/1.6 'Segoe UI',Arial,sans-serif;background-image:radial-gradient(ellipse at 90% 0%,rgba(112,233,235,.08),transparent 38%)}}main{{max-width:1120px;margin:auto;padding:30px 28px 60px}}nav{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:30px;padding:14px;background:#0a1c2b;border:1px solid #234c65;border-radius:12px}}a{{color:#70e9eb;text-underline-offset:4px}}nav a{{padding:7px 13px;border:1px solid #355b75;border-radius:7px;text-decoration:none;font-size:15px}}a:hover{{color:#b8fcff}}a:focus-visible{{outline:3px solid #f5b867;outline-offset:4px}}h1{{font-size:clamp(27px,4vw,42px);line-height:1.22;margin:10px 0 20px}}h2{{color:#70e9eb;font-size:23px;margin-top:32px;padding-top:22px;border-top:1px solid #234c65}}img{{width:100%;height:auto;border:1px solid #234c65;border-radius:12px;background:#0a1c2b}}.eyebrow{{font:13px/1.5 Consolas,monospace;letter-spacing:.15em;color:#70e9eb}}.facts{{display:flex;gap:28px;flex-wrap:wrap;padding:10px 24px;margin:24px 0;background:#0a1c2b;border:1px solid #234c65;border-radius:12px}}.facts strong{{color:#b8fcff}}li{{margin:.6em 0}}footer{{margin-top:35px;padding:22px;background:#0a1c2b;border:1px solid #234c65;border-radius:12px;color:#a5c5d7}}small{{font-size:14px}}@media(max-width:700px){{main{{padding:22px 16px 45px}}.facts{{gap:8px 22px;padding:10px 18px}}nav{{gap:8px}}}}@media print{{body{{background:white;color:#182c3c}}nav{{display:none}}main{{padding:0}}h2{{color:#184659}}a{{color:#184659}}.facts,footer{{background:#eef3f6;border-color:#bbcbd6;color:#182c3c}}img{{border-color:#bbcbd6}}}}
</style></head><body><main><nav>{' '.join(nav)}</nav><p class="eyebrow">TRAILDOSSIER / NORTHBOUND</p><h1>{html.escape(display_title)}</h1><p>{html.escape(display_summary)}</p><div class="facts"><p><strong>Section:</strong> {fmtmile(stage['distance_miles'])} virtual miles</p><p><strong>Region:</strong> {html.escape(stage['region'])}</p><p><strong>Physical workout target:</strong> chosen separately</p></div><img src="../maps/{stage['id']}.svg" alt="North-up mapped trail section with start and finish checkpoints and full-trail locator"><h2>Today’s map briefing</h2><ul>{''.join('<li>'+html.escape(s)+'</li>' for s in display_briefing)}</ul><h2>Preparation focus</h2><p>{html.escape(stage['orientation_prompt'])}</p><h2>Checkpoint coordinates</h2><p>Start: {stage['start']['latitude']:.7f}, {stage['start']['longitude']:.7f}<br>Finish: {stage['end']['latitude']:.7f}, {stage['end']['longitude']:.7f}</p><p>These are virtual section boundaries. The map does not verify campsites, water, elevation, or current trail conditions.</p><p><a href="../routes/{stage['id']}.geojson">Section geometry</a> · <a href="../maps/{stage['id']}.svg">Full-size map</a></p><footer><small>Route data © Pacific Crest Trail Association, 2026 snapshot, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Source: <a href="{SOURCE_PAGE}">PCTA route data</a>. Changes: daily segmentation, display simplification, and map rendering. Regional context: Census 2017 / us-atlas 3.0.1. Route release: {route_release}.</small></footer></main></body></html>'''
    (CONTENT/'dossiers'/f'{stage["id"]}.html').write_text(doc,encoding='utf-8')

with (CONTENT/'daily_sections.csv').open('w',encoding='utf-8',newline='') as stream:
    writer=csv.writer(stream); writer.writerow(['day','stage_id','region','mile_start','mile_end','virtual_miles','start_lat','start_lon','end_lat','end_lon','map','dossier'])
    for s in stages:writer.writerow([s['day_number'],s['id'],s['region'],s['mile_start'],s['mile_end'],s['distance_miles'],s['start']['latitude'],s['start']['longitude'],s['end']['latitude'],s['end']['longitude'],s['map_path'],s['dossier_path']])

for path in sorted(SOURCE.glob('*.json')):
    if path.name.endswith('_combined.json'):continue
    with (CONTENT/'sources'/(path.name+'.gz')).open('wb') as output:
        with gzip.GzipFile(fileobj=output,mode='wb',mtime=0) as compressor:compressor.write(path.read_bytes())
shutil.copyfile(SOURCE/'manifest.json',CONTENT/'sources'/'source_manifest.json')
validation={'stages':len(stages),'route_source_vertices':len(coordinates),'usable_mile_markers':len(markers),'excluded_nonspatial_markers':excluded,
            'total_marker_referenced_miles':TOTAL,'raw_haversine_geometry_miles':cumulative[-1]/METRES_PER_MILE,
            'maximum_original_segment_metres':maximum_segment[0],'maximum_marker_projection_offset_metres':max_offset,
            'all_marker_positions_strictly_increasing':True,'all_adjacent_stage_endpoints_identical':True,'all_route_miles_covered_once':True,
            'nominal_stage_count':265,'nominal_stage_miles':10,'final_stage_miles':5.84,'published_maps':len(stages)+1,'published_daily_dossiers':len(stages),
            'elevation_available':False,'generation_creates_workouts':False,'route_release':route_release,
            'original_source_sha256':centerline_hash,'display_simplification_metres':4,
            'source_metadata_discrepancy':'Service description says 2025; data edit date is January 2026; source hash is pinned',
            'map_coverage':'Local route line, neighbor route, degree grid, approximate scale, direction, exact stage checkpoints and sourced regional locator'}
(CONTENT/'validation_report.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2))
