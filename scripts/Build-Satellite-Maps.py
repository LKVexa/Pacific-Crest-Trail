"""Cache official imagery tiles and publish a satellite/aerial map edition.

Route geometry and campaign history are unchanged. Source photographs are not
stitched, cropped or resampled: SVG places each original source tile by its
geographic bounds. Small geographic-vs-Mercator interpolation is measured below.
Pillow is used to validate image decoding, never to edit imagery.
"""
import argparse, base64, concurrent.futures, hashlib, importlib.util, io, json, math, os, threading, time, uuid
from pathlib import Path
import urllib.error, urllib.request
import xml.etree.ElementTree as ET

SERVICE = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
LEVEL = 14
WORLD = 20037508.342787
RADIUS = 6378137.0


def sha(raw): return hashlib.sha256(raw).hexdigest()


def atomic(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_name(path.name + '.satellite-' + uuid.uuid4().hex)
    staged.write_bytes(raw)
    os.replace(staged, path)


def save_json(path, value): atomic(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def inverse(x, y): return math.degrees(x/RADIUS), math.degrees(2*math.atan(math.exp(y/RADIUS))-math.pi/2)


def tile_bounds(level, row, column):
    span = 2 * WORLD / (2**level)
    west, north = -WORLD + column*span, WORLD-row*span
    east, south = west+span, north-span
    return [*inverse(west,south), *inverse(east,north)]


def tile_at(level, lon, lat):
    n = 2**level
    return int((1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n), int((lon+180)/360*n)


def download(url):
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent':'TrailDossier/1.0 local official imagery map cache'})
            with urllib.request.urlopen(request, timeout=25) as response:
                if not response.geturl().startswith(SERVICE + '/tile/'):
                    raise ValueError('Unexpected official imagery redirect')
                raw = response.read(8*1024*1024 + 1)
            if len(raw)>8*1024*1024: raise ValueError('Imagery tile exceeds size limit')
            return raw
        except urllib.error.HTTPError as error:
            if error.code==404: return None
            # A valid cached parent tile supplies honest lower-resolution context
            # when a high-resolution cache node stays temporarily unavailable.
            if error.code in (500,502,503,504) and attempt>=2: return None
            if attempt==3: raise
        except OSError:
            if attempt==3: raise
        time.sleep(2**attempt)


def decode(raw):
    from PIL import Image
    with Image.open(io.BytesIO(raw)) as image:
        image.load()
        if image.size!=(256,256) or image.format not in ('JPEG','PNG'): raise ValueError('Unexpected cached tile format or dimensions')
        return ('jpg','image/jpeg') if image.format=='JPEG' else ('png','image/png')


class Cache:
    def __init__(self, root, offline):
        self.root,self.offline=root,offline
        self.lock=threading.Lock();self.locks={}
    def get(self, level, row, column):
        key=f'z{level}-{row}-{column}'
        with self.lock: lock=self.locks.setdefault(key,threading.Lock())
        with lock:
            metadata_path=self.root/'content/sources/satellite'/(key+'.json')
            if metadata_path.exists():
                info=json.loads(metadata_path.read_text(encoding='utf-8'));raw=(self.root/info['path']).read_bytes()
                if sha(raw)!=info['sha256'] or decode(raw)[1]!=info['mime']: raise ValueError('Cached tile integrity mismatch')
                return {**info,'metadata_sha256':sha(metadata_path.read_bytes())},raw
            if self.offline: raise ValueError('Missing cached imagery tile: '+key)
            url=f'{SERVICE}/tile/{level}/{row}/{column}'
            raw=download(url)
            if raw is None: return None
            extension,mime=decode(raw)
            relative=f'content/sources/satellite/{key}.{extension}'
            atomic(self.root/relative,raw)
            info={'level':level,'row':row,'column':column,'path':relative,'metadata_path':metadata_path.relative_to(self.root).as_posix(),
                  'sha256':sha(raw),'bytes':len(raw),'mime':mime,'bounds':tile_bounds(level,row,column),'url':url,'pixel_dimensions':[256,256]}
            save_json(metadata_path,info)
            return {**info,'metadata_sha256':sha(metadata_path.read_bytes())},raw
    def slot(self, row, column):
        for level in range(LEVEL,7,-1):
            shift=LEVEL-level
            result=self.get(level,row//(2**shift),column//(2**shift))
            if result is not None:
                info,raw=result
                return {'requested_level':LEVEL,'requested_row':row,'requested_column':column,'slot_bounds':tile_bounds(LEVEL,row,column),**info},raw
        raise ValueError('No official imagery source covers requested map tile')


def publish_day(root, stage, project, bbox, slots):
    baseline=root/'content/sources/topography/route-only'/f"{stage['id']}.svg"
    original=baseline.read_bytes();svg=ET.fromstring(original)
    plot=next(group for group in svg.findall(f'{{{NS}}}g') if group.get('clip-path')=='url(#plot)')
    route=next(p for p in plot.findall(f'{{{NS}}}path') if p.get('stroke')=='#70e9eb')
    insertion=next(i for i,c in enumerate(plot) if c.get('fill')!='#0d2435')
    defs=svg.find(f'{{{NS}}}defs');tiles=[];deviations=[]
    for number,(info,raw) in enumerate(slots,1):
        west,south,east,north=info['bounds'];x,y=project(west,north);right,bottom=project(east,south)
        sw,ss,se,sn=info['slot_bounds'];sx,sy=project(sw,sn);sr,sb=project(se,ss)
        clip=f'imagery-slot-{number}'
        clipping=ET.SubElement(defs,f'{{{NS}}}clipPath',{'id':clip})
        ET.SubElement(clipping,f'{{{NS}}}rect',{'x':f'{sx:.6f}','y':f'{sy:.6f}','width':f'{sr-sx:.6f}','height':f'{sb-sy:.6f}'})
        group=ET.Element(f'{{{NS}}}g',{'clip-path':f'url(#{clip})'})
        ET.SubElement(group,f'{{{NS}}}image',{'id':f'satellite-tile-{number}','x':f'{x:.6f}','y':f'{y:.6f}',
          'width':f'{right-x:.6f}','height':f'{bottom-y:.6f}','preserveAspectRatio':'none','href':f"data:{info['mime']};base64,"+base64.b64encode(raw).decode()})
        plot.insert(insertion,group);insertion+=1
        # Bound the native Mercator image's latitude interpolation error in this
        # small local equirectangular map; keep it below .25 displayed pixels.
        north_y=RADIUS*math.log(math.tan(math.pi/4+math.radians(north)/2))
        south_y=RADIUS*math.log(math.tan(math.pi/4+math.radians(south)/2))
        maximum=0
        for fraction in (.25,.5,.75):
            actual_lat=inverse(0,north_y+fraction*(south_y-north_y))[1]
            actual_pixel=project(west,actual_lat)[1]
            maximum=max(maximum,abs(actual_pixel-(y+fraction*(bottom-y))))
        if maximum>.25: raise ValueError('Tile reprojection approximation exceeds quarter-pixel limit')
        deviations.append(maximum);tiles.append(info)
    halo=ET.Element(f'{{{NS}}}path',dict(route.attrib));halo.set('id','satellite-route-halo');halo.set('stroke','#03101a');halo.set('stroke-width','7.8')
    plot.insert(list(plot).index(route),halo)
    for child in plot:
        if child.get('stroke-width') in ('.6','0.6'): child.set('stroke-opacity','.22');child.set('stroke','#a5c5d7')
    svg.set('height','710');svg.set('viewBox','0 0 1120 710');svg.find(f'{{{NS}}}rect').set('height','710')
    svg.find(f'{{{NS}}}desc').text='Satellite/aerial geographic imagery from official USGS cached tiles, with unchanged sourced daily route and virtual checkpoint overlays. Historical orthoimagery, not a live image or proof of current trail conditions.'
    for y,copy in [(676,'Satellite / aerial imagery: USDA, USGS The National Map · Historical orthoimagery · Route and virtual checkpoints unchanged.'),
                   (695,'Images positioned from the official Web Mercator tile matrix · This map does not verify current conditions or stopping places.')]:
        label=ET.SubElement(svg,f'{{{NS}}}text',{'x':'45','y':str(y),'font-family':'Segoe UI,Arial','font-size':'11','fill':'#a5c5d7'});label.text=copy
    raw=ET.tostring(svg,encoding='utf-8')+b'\n';relative=f"content/maps/satellite-{stage['id']}.svg";atomic(root/relative,raw)
    return {'day_id':stage['id'],'map_path':relative,'map_revision':sha(raw)[:16],'source_ids':['usgs-imagery'],
      'published_map_sha256':sha(raw),'baseline_path':baseline.relative_to(root).as_posix(),'baseline_sha256':sha(original),
      'route_path_sha256':sha(route.get('d').encode()),'requested_bbox':bbox,'maximum_reprojection_error_pixels':max(deviations),'tiles':tiles}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--offline',action='store_true');parser.add_argument('--days');args=parser.parse_args()
    root=args.root.resolve();spec=importlib.util.spec_from_file_location('topographic_builder',root/'scripts/Build-Topographic-Maps.py');topo=importlib.util.module_from_spec(spec);spec.loader.exec_module(topo)
    original=(root/'content/itinerary.json').read_bytes();itinerary=json.loads(original);stages=itinerary['stages']
    if args.days: numbers={int(n) for n in args.days.split(',')};stages=[s for s in stages if s['day_number'] in numbers]
    service_path=root/'content/sources/leg_photos/service.json'
    if not service_path.exists(): raise ValueError('Cache official USGS imagery service metadata with Expand-Leg-Photos first')
    service_raw=service_path.read_bytes();service=json.loads(service_raw)
    lod=next(lod for lod in service['tileInfo']['lods'] if lod['level']==LEVEL)
    if abs(lod['resolution']-2*WORLD/(256*2**LEVEL))>1e-8 or service['tileInfo']['rows']!=256: raise ValueError('Official tile matrix changed')
    cache=Cache(root,args.offline);plans=[];slots=set()
    for stage in stages:
        points=json.loads((root/stage['geometry_path']).read_bytes())['geometry']['coordinates'];project,bbox=topo.projection(points)
        rmin,cmin=tile_at(LEVEL,bbox[0],bbox[3]);rmax,cmax=tile_at(LEVEL,bbox[2],bbox[1]);day_slots=[(r,c) for r in range(rmin,rmax+1) for c in range(cmin,cmax+1)]
        plans.append((stage,project,bbox,day_slots));slots.update(day_slots)
    print(f'Acquire {len(slots)} unique official imagery tile slots for {len(stages)} maps.',flush=True)
    acquired={}
    failures=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pending={pool.submit(cache.slot,*slot):slot for slot in sorted(slots)}
        for future in concurrent.futures.as_completed(pending):
            try: acquired[pending[future]]=future.result()
            except Exception as error:
                failures.append({'slot':pending[future],'error':str(error)})
            if len(acquired)%100==0: print(f'{len(acquired)}/{len(slots)} geographic tile slots cached',flush=True)
    if failures:
        save_json(root/'content/sources/satellite/acquisition_failures.json',failures)
        raise ValueError(f'{len(failures)} imagery slots unavailable; verified cache retained for resumption')
    rows=[publish_day(root,stage,project,bbox,[acquired[slot] for slot in day_slots]) for stage,project,bbox,day_slots in plans]
    path=root/'content/satellite.json'
    if path.exists():
        previous=json.loads(path.read_bytes())
        if previous.get('itinerary_sha256')!=sha(original): raise ValueError('Existing satellite edition belongs to a different route')
        combined={r['day_id']:r for r in previous['days']};combined.update({r['day_id']:r for r in rows});rows=sorted(combined.values(),key=lambda row:row['day_id'])
    publication={'version':1,'itinerary_sha256':sha(original),'route_release':itinerary['metadata']['route_release'],
      'map_revision':sha(''.join(r['published_map_sha256'] for r in rows).encode())[:16],'days':rows,'coverage_count':len(rows),
      'sources':[{'id':'usgs-imagery','title':'USGS / The National Map satellite and aerial orthoimagery','url':SERVICE,'attribution':service['copyrightText'],
                  'metadata_path':service_path.relative_to(root).as_posix(),'metadata_sha256':sha(service_raw)}]}
    if (root/'content/itinerary.json').read_bytes()!=original: raise ValueError('Pinned itinerary changed')
    save_json(path,publication);print(f'Published {len(rows)} satellite/aerial maps; route and saved history unchanged.',flush=True)


if __name__=='__main__':main()
