"""Ground-photo assignment and licensed, route-centered aerial gap coverage.

Generator dependency: Pillow. The application service needs only its standard
library. No treadmill, campaign, activity or journal record is read or changed.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import gzip
import hashlib
import html
import io
import json
import math
import os
from pathlib import Path
import re
import threading
import time
import urllib.parse
import urllib.request
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone

REPO=Path(__file__).resolve().parents[1]
SERVICE='https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer'
RIGHTS_URL='https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits'
NAIP_URL='https://data.usgs.gov/datacatalog/data/USGS:EROS5e83a340bf820c39'
UA='TrailDossier/1.0 (personal local trail preparation; public cached imagery)'
MINIMUM=10
MAX_OFFSET=1000.0
MIN_SCALE=9027.977411
TILE_LEVEL=16
AERIAL_MAX_OFFSET=500.0
MERCATOR_RADIUS=6378137.0
DISCOVERY_STEP_METERS=150.0
MAX_BYTES=8*1024*1024
CELL=.02
CONUS=(-126.0,24.0,-66.0,50.0)
GROUND_BREAKER=threading.Event()

def now():return datetime.now(timezone.utc).isoformat()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8')
def plain(value):return re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',html.unescape(str(value)))).strip()
def meta(info,key):return info.get('extmetadata',{}).get(key,{}).get('value','')

def member(relative):
    if not isinstance(relative,str) or '\\' in relative or relative.startswith('/') or '..' in relative.split('/'):
        raise ValueError('Unsafe repository-relative public source path')
    path=(REPO/relative).resolve()
    if not path.is_relative_to(REPO.resolve()):raise ValueError('Public source escapes this repository')
    return path

def atomic_bytes(path,raw,expected_hash=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    staging=path.with_name(path.name+'.staging-'+uuid.uuid4().hex)
    try:
        with staging.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        if digest(staging.read_bytes())!=digest(raw):raise ValueError('Staged bytes failed verification')
        if expected_hash is not None and (digest(path.read_bytes()) if path.exists() else 'absent')!=expected_hash:
            raise ValueError('Published content changed; preserve the new content and review this proposal')
        os.replace(staging,path)
    finally:staging.unlink(missing_ok=True)

def atomic_json(path,value,expected_hash=None):atomic_bytes(path,canonical(value),expected_hash)

class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self,hosts):self.hosts=hosts
    def redirect_request(self,request,fp,code,msg,headers,newurl):
        parsed=urllib.parse.urlparse(newurl)
        if parsed.scheme!='https' or parsed.hostname not in self.hosts:raise ValueError('Unexpected image redirect host')
        return super().redirect_request(request,fp,code,msg,headers,newurl)

def fetch(url,json_response=False):
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!='https' or parsed.hostname!='basemap.nationalmap.gov':raise ValueError('Unexpected imagery host')
    last=None
    for attempt in range(5):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json' if json_response else 'image/jpeg'})
            opener=urllib.request.build_opener(RestrictedRedirect({'basemap.nationalmap.gov'}))
            with opener.open(request,timeout=45) as response:
                raw=response.read(MAX_BYTES+1);mime=response.headers.get_content_type();status=response.status
            if len(raw)>MAX_BYTES:raise ValueError('Imagery response exceeds the bounded file size')
            if json_response:
                value=json.loads(raw)
                if not isinstance(value,dict) or 'error' in value:raise ValueError('Provider export error: '+str(value.get('error')))
                return value,raw,mime
            if mime not in ('image/jpeg','image/png'):raise ValueError('Provider did not deliver an original JPEG or PNG')
            return raw,mime,status
        except Exception as error:
            last=error
            if attempt<4:
                delay=min(20,2**attempt*2)
                retry=getattr(error,'headers',{}).get('Retry-After','0')
                if str(retry).isdigit():delay=max(delay,min(60,int(retry)))
                print('Imagery retry:',type(error).__name__,'in',delay,'seconds',flush=True);time.sleep(delay)
    raise last

def service_metadata(offline=False):
    path=REPO/'content/sources/leg_photos/service.json'
    if path.exists():raw=path.read_bytes();value=json.loads(raw)
    else:
        if offline:raise ValueError('The licensed provider snapshot has not been cached')
        value,raw,_=fetch(SERVICE+'?f=pjson',True);atomic_bytes(path,raw)
    description=value.get('serviceDescription','')
    if 'public domain' not in description.lower() or 'conterminous' not in description.lower():
        raise ValueError('Service no longer provides the checked public-domain CONUS orthoimagery context; review rights before acquisition')
    if value.get('mapName')!='USGSImageryOnly' or float(value.get('maxScale',0))!=MIN_SCALE:
        raise ValueError('The imagery service identity/scale changed; review before acquiring new frames')
    source={'id':'usgs-imagery','title':'USGS / The National Map aerial orthoimagery','url':SERVICE,
            'attribution':value.get('copyrightText','USDA, USGS The National Map: Orthoimagery'),
            'metadata_path':'content/sources/leg_photos/service.json','metadata_sha256':digest(raw),
            'license':'U.S. public domain (CONUS orthoimagery)','license_url':RIGHTS_URL,
            'rights_references':[SERVICE+'?f=pjson',RIGHTS_URL,NAIP_URL],
            'rights_scope':'Provider explicitly describes public-domain CONUS orthoimagery. Alaska/Hawaii licensed exceptions are outside this itinerary. Preserve source credits.',
            'capture_context':'Historical aerial imagery; exact frame capture date is not supplied. Service refresh is not image capture date.',
            'minimum_supported_scale':MIN_SCALE}
    atomic_json(REPO/'content/sources/leg_photos/rights.json',source)
    return source

def distance(a,b):
    latitude=math.radians((a[1]+b[1])/2)
    return math.hypot((a[0]-b[0])*111320*math.cos(latitude),(a[1]-b[1])*111320)

def load_route():
    raw=(REPO/'content/itinerary.json').read_bytes();itinerary=json.loads(raw)
    routes={};cumulative={}
    for stage in itinerary['stages']:
        points=json.loads(member(stage['geometry_path']).read_text(encoding='utf-8'))['geometry']['coordinates']
        totals=[0.0]
        for a,b in zip(points,points[1:]):totals.append(totals[-1]+distance(a,b))
        if not totals[-1]:raise ValueError('A route section has no geographic length')
        routes[stage['id']]=points;cumulative[stage['id']]=totals
    return itinerary,digest(raw),routes,cumulative

def point_at(points,totals,fraction):
    target=totals[-1]*fraction
    for i in range(1,len(totals)):
        if totals[i]>=target:
            f=(target-totals[i-1])/(totals[i]-totals[i-1]) if totals[i]>totals[i-1] else 0
            return [points[i-1][n]+f*(points[i][n]-points[i-1][n]) for n in (0,1)]
    return list(points[-1])

def index_route(stages,routes,cumulative):
    grid=defaultdict(list)
    for stage in stages:
        points=routes[stage['id']];totals=cumulative[stage['id']]
        for i,(a,b) in enumerate(zip(points,points[1:])):
            # Conservative bounds ensure no <=1km candidate is lost to the grid.
            dy=MAX_OFFSET/110000;dx=MAX_OFFSET/(110000*math.cos(math.radians(max(abs(a[1]),abs(b[1])))))
            segment=(stage['day_number'],stage['id'],a,b,totals[i],totals[i+1]-totals[i],totals[-1])
            for x in range(math.floor((min(a[0],b[0])-dx)/CELL),math.floor((max(a[0],b[0])+dx)/CELL)+1):
                for y in range(math.floor((min(a[1],b[1])-dy)/CELL),math.floor((max(a[1],b[1])+dy)/CELL)+1):grid[(x,y)].append(segment)
    return grid

def nearest_global(grid,latitude,longitude):
    best=None;sx=111320*math.cos(math.radians(latitude));sy=111320
    for number,day,a,b,start,length,total in grid.get((math.floor(longitude/CELL),math.floor(latitude/CELL)),[]):
        ax=(a[0]-longitude)*sx;ay=(a[1]-latitude)*sy;bx=(b[0]-longitude)*sx;by=(b[1]-latitude)*sy
        dx=bx-ax;dy=by-ay;den=dx*dx+dy*dy;f=max(0,min(1,-(ax*dx+ay*dy)/den)) if den else 0
        offset=math.hypot(ax+f*dx,ay+f*dy);candidate=(offset,number,day,(start+f*length)/total)
        if best is None or candidate[:2]<best[:2]:best=candidate
    return best

def public_metadata():
    path=REPO/'content/sources/visual_curation/manifest.json'
    if not path.exists():raise ValueError('Run Curate-Visuals.py -- public provider provenance archive is required before ground selection')
    archive=json.loads(path.read_text(encoding='utf-8'));geotags=defaultdict(list);pages={};rejected=Counter()
    for record in archive['records']:
        relative=record['archive_path']
        if not relative.startswith('content/sources/visual_curation/'):raise ValueError('Unexpected ground source root')
        compressed=member(relative).read_bytes()
        if digest(compressed)!=record['archive_sha256']:raise ValueError('Ground source archive checksum mismatch')
        raw=gzip.decompress(compressed)
        if len(raw)>16*1024*1024 or digest(raw)!=record['source_sha256']:raise ValueError('Ground source payload checksum mismatch')
        data=json.loads(raw);provenance={'path':relative,'sha256':record['source_sha256'],'archive_sha256':record['archive_sha256']}
        if record['kind']=='geographic_search':
            for point in data.get('query',{}).get('geosearch',[]):
                if point.get('ns')==6 and isinstance(point.get('pageid'),int) and all(isinstance(point.get(k),(int,float)) and math.isfinite(point[k]) for k in ('lat','lon')):
                    geotags[point['pageid']].append((point,provenance))
        elif record['kind']=='image_metadata':
            for key,page in data.get('query',{}).get('pages',{}).items():
                if isinstance(page,dict) and page.get('imageinfo'):pages[int(key)]=(page,provenance)
    unique={}
    for key,items in geotags.items():
        original=items[0][0]
        if any(distance((original['lon'],original['lat']),(item[0]['lon'],item[0]['lat']))>5 for item in items):rejected['ambiguous_geotags']+=1;continue
        unique[key]=items[0]
    return unique,pages,rejected

def normalized_https(value):
    if not isinstance(value,str):return None
    value=html.unescape(value)
    if value.startswith('http://creativecommons.org/'):value='https://'+value[7:]
    parsed=urllib.parse.urlparse(value)
    return value if parsed.scheme=='https' and not parsed.username and not parsed.password else None

def ground_photos(itinerary,routes,cumulative):
    geo,pages,rejected=public_metadata();grid=index_route(itinerary['stages'],routes,cumulative)
    stages={stage['id']:stage for stage in itinerary['stages']};by_day=defaultdict(list);seen=set()
    excluded=re.compile(r'\b(map|diagram|logo|flag|coat of arms|painting|drawing|portrait|montage|collage|cropped|crop|orthophoto|orthophotography|aerial|satellite|naip|landsat)\b|^File:M_? \d{7}',re.I)
    accepted_license=re.compile(r'^(?:CC BY(?:-SA)? [0-9]+(?:\.[0-9]+)?\b|CC0\b|CC-zero\b|Public domain\b|PD\b)',re.I)
    for pageid,(point,gps_provenance) in sorted(geo.items()):
        saved=pages.get(pageid)
        if not saved:rejected['metadata_unavailable']+=1;continue
        page,image_provenance=saved;info=page['imageinfo'][0]
        title=plain(meta(info,'ObjectName')) or point['title'].removeprefix('File:')
        if info.get('mime') not in ('image/jpeg','image/png','image/webp') or excluded.search(point['title']+' '+title):rejected['not_ground_photo']+=1;continue
        if info.get('width',0)<600 or info.get('height',0)<350:rejected['small_image']+=1;continue
        license_name=plain(meta(info,'LicenseShortName'));license_url=normalized_https(meta(info,'LicenseUrl'))
        if not accepted_license.search(license_name) or not license_url:rejected['unsupported_license']+=1;continue
        source=normalized_https(info.get('descriptionurl'));original=normalized_https(info.get('url'));thumb=normalized_https(info.get('thumburl') or info.get('url'))
        if not source or not original or not thumb or urllib.parse.urlparse(thumb).hostname not in ('upload.wikimedia.org','thumb.wikimedia.org'):rejected['invalid_reference']+=1;continue
        identity=info.get('sha1') or original
        if identity in seen:rejected['same_original_identity']+=1;continue
        nearest=nearest_global(grid,point['lat'],point['lon'])
        if nearest is None or nearest[0]>MAX_OFFSET:rejected['outside_ground_offset']+=1;continue
        offset,_,day,fraction=nearest;stage=stages[day];seen.add(identity)
        photo={'id':'commons-'+str(pageid),'title':title,'source_url':source,'thumbnail_url':thumb,'original_url':original,
               'author':plain(meta(info,'Artist')) or 'See source credit','license':license_name,'license_url':license_url,
               'latitude':point['lat'],'longitude':point['lon'],'distance_to_section_meters':round(offset,3),
               'route_mile':round(stage['mile_start']+fraction*stage['distance_miles'],5),'media_kind':'ground',
               'location_label':f'Provider geotag {offset:.0f} m from its nearest trail section',
               'capture_date':plain(meta(info,'DateTimeOriginal')) or None,
               'location_verification':'Provider geotag screened; camera position and depicted subject are not independently verified',
               'review_status':'Licensed geotag metadata screened; not individually field-verified',
               'assignment':{'day_id':day,'distance_meters':round(offset,3),'method':'globally nearest route section from provider geotag',
                             'route_fraction':fraction,'coordinate_role':'provider_geotag_camera_unverified'},
               'provenance':{'commons_pageid':pageid,'geotag_source_path':gps_provenance['path'],'geotag_source_sha256':gps_provenance['sha256'],
                             'image_metadata_source_path':image_provenance['path'],'image_metadata_source_sha256':image_provenance['sha256']}}
        flickr=re.search(r'https?://(?:www\.)?flickr\.com/[^\s"<>]+',meta(info,'Credit'))
        if flickr:photo['social_original_url']=html.unescape(flickr.group(0)).replace('http://','https://',1)
        by_day[day].append(photo)
    for day in by_day:by_day[day].sort(key=lambda p:(p['distance_to_section_meters'],p['id']))
    # Selection happens only after every accepted source has a global owner.
    selected={stage['id']:by_day[stage['id']][:MINIMUM] for stage in itinerary['stages']}
    report={'geotagged_unique_candidates':len(geo),'cached_image_metadata_pages':len(pages),
            'licensed_nearest_ground_candidates':sum(map(len,by_day.values())),
            'selected_ground_photos':sum(map(len,selected.values())),
            'ground_only_minimum_days':sum(len(value)>=MINIMUM for value in selected.values()),
            'ground_days_with_any':sum(bool(value) for value in selected.values()),'exclusions':dict(rejected),
            'maximum_ground_offset_meters':MAX_OFFSET,'global_assignment_before_per_day_selection':True}
    return selected,report

def validate_jpeg(raw):
    from PIL import Image,ImageStat
    if not raw.startswith(b'\xff\xd8') or not raw.endswith(b'\xff\xd9'):raise ValueError('Image is not a complete JPEG')
    with Image.open(io.BytesIO(raw)) as image:
        if image.format!='JPEG':raise ValueError('Decoded image is not JPEG')
        image.load();size=list(image.size);sample=image.convert('RGB').resize((64,64));variation=ImageStat.Stat(sample).stddev
    if max(variation)<2:raise ValueError('Imagery is blank or has insufficient decoded pixel variation')
    return size,variation

def fetch_ground(url):
    hosts={'upload.wikimedia.org','thumb.wikimedia.org'};parsed=urllib.parse.urlparse(url)
    if parsed.scheme!='https' or parsed.hostname not in hosts:raise ValueError('Ground image host is not an official allowed Commons rendition host')
    throttle=REPO/'data/media-expansion/commons-throttle.json'
    if GROUND_BREAKER.is_set() or (throttle.exists() and json.loads(throttle.read_bytes()).get('retry_after_epoch',0)>time.time()):raise RuntimeError('Commons provider cooldown active; preserve cached ground photos and use distinct aerial coverage')
    opener=urllib.request.build_opener(RestrictedRedirect(hosts));last=None
    for attempt in range(4):
        if GROUND_BREAKER.is_set():raise RuntimeError('Commons provider acquisition stopped after rate limit')
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'image/jpeg,image/png,image/webp'})
            with opener.open(req,timeout=30) as response:
                status=response.status;mime=response.headers.get_content_type();raw=response.read(MAX_BYTES+1)
            if len(raw)>MAX_BYTES or status!=200:raise ValueError('Ground photograph response is oversized or incomplete')
            if mime not in ('image/jpeg','image/png','image/webp'):raise ValueError('Ground photograph MIME is unsupported')
            return raw,mime,status
        except Exception as error:
            last=error
            if getattr(error,'code',None)==429:
                GROUND_BREAKER.set()
                atomic_json(throttle,{'provider':'Wikimedia Commons','http_status':429,'recorded_utc':now(),'retry_after_epoch':time.time()+3600,'reason':'Provider requested less disruptive access. Acquisition stops; existing cached images remain valid.'})
                raise RuntimeError('Commons rate limit: no further ground image requests this run') from error
            if GROUND_BREAKER.is_set():raise RuntimeError('Commons provider acquisition stopped after rate limit') from error
            if attempt<3:
                delay=2**attempt*2;retry=getattr(error,'headers',{}).get('Retry-After','0')
                if str(retry).isdigit():delay=max(delay,min(60,int(retry)))
                print('Ground image retry:',type(error).__name__,'in',delay,'seconds',flush=True);time.sleep(delay)
    raise last


def validate_ground_image(raw,mime):
    from PIL import Image
    expected={'image/jpeg':'JPEG','image/png':'PNG','image/webp':'WEBP'}
    if mime not in expected:raise ValueError('Unsupported ground photograph MIME')
    with Image.open(io.BytesIO(raw)) as image:
        if image.format!=expected[mime] or image.width*image.height>20000000:raise ValueError('Ground raster type/dimensions disagree with MIME or bound')
        image.load();dimensions=list(image.size)
    if min(dimensions)<120:raise ValueError('Ground rendition is too small to view')
    return dimensions

def validate_tile_image(raw,mime):
    from PIL import Image,ImageStat
    dimensions=validate_ground_image(raw,mime)
    with Image.open(io.BytesIO(raw)) as image:variation=ImageStat.Stat(image.convert('RGB').resize((64,64))).stddev
    if max(variation)<2:raise ValueError('Imagery tile is blank or has insufficient decoded pixel variation')
    if dimensions!=[256,256]:raise ValueError('Original imagery tile must decode to256x256')
    return dimensions,variation


def cache_ground_photo(photo,offline=False):
    day=photo['assignment']['day_id'];ident=photo['id'];remote=photo['thumbnail_url']
    metadata_relative=f'content/sources/leg_photos/{ident}.json';metadata_path=member(metadata_relative)
    if metadata_path.exists():
        record=json.loads(metadata_path.read_bytes());relative=record['image_path'];raw=member(relative).read_bytes();mime=record['mime']
        if record.get('provider_type')!='commons-thumbnail' or record.get('request_url')!=remote or record.get('day_id')!=day or record.get('photo_id')!=ident or record.get('provenance')!=photo['provenance']:raise ValueError('Cached ground photo source/assignment changed')
        if any(record.get(key)!=photo.get(key) for key in ('original_url','source_url','latitude','longitude','assignment','license','license_url','author')):raise ValueError('Cached ground photograph public metadata changed')
        extension={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}.get(mime)
        if relative!=f'content/media/{ident}.{extension}':raise ValueError('Cached ground image path is not its exact MIME-specific source path')
        if digest(raw)!=record.get('image_sha256') or len(raw)!=record.get('image_bytes'):raise ValueError('Cached ground photograph checksum changed')
        dimensions=validate_ground_image(raw,mime)
        if dimensions!=record.get('decoded_dimensions') or record.get('provider_response')!={'http_status':200,'mime':mime}:raise ValueError('Cached ground photo decoded dimensions/HTTP facts changed')
    else:
        if offline:raise ValueError('Ground photograph not cached: '+ident)
        raw,mime,status=fetch_ground(remote);dimensions=validate_ground_image(raw,mime)
        extension={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[mime];relative=f'content/media/{ident}.{extension}'
        record={'version':1,'provider_type':'commons-thumbnail','day_id':day,'photo_id':ident,'request_url':remote,'remote_thumbnail_url':remote,
                'original_url':photo['original_url'],'source_url':photo['source_url'],'provider_response':{'http_status':status,'mime':mime},
                'source_date':now(),'image_path':relative,'mime':mime,'image_sha256':digest(raw),'image_bytes':len(raw),'decoded_dimensions':dimensions,
                'provenance':photo['provenance'],'latitude':photo['latitude'],'longitude':photo['longitude'],'assignment':photo['assignment'],
                'author':photo['author'],'license':photo['license'],'license_url':photo['license_url'],'title':photo['title']}
        atomic_bytes(member(relative),raw);atomic_json(metadata_path,record);time.sleep(.25)
    card={**photo,'remote_thumbnail_url':remote,'thumbnail_url':'/'+relative,'pixel_dimensions':dimensions,'image_sha256':digest(raw),'source_metadata_path':metadata_relative,'source_retrieved_utc':record['source_date']}
    entry={'sha256':digest(raw),'bytes':len(raw),'mime':mime,'day_id':day,'photo_id':ident,'media_kind':'ground','source_url':remote,
           'metadata_path':metadata_relative,'metadata_sha256':digest(metadata_path.read_bytes()),'pixel_dimensions':dimensions}
    return card,relative,entry


def cache_ground_photos(ground,offline=False,allow_missing=False):
    selected={day:[] for day in ground};files={};failures=[];completed=0;jobs=[p for cards in ground.values() for p in cards]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(cache_ground_photo,p,offline):p for p in jobs}
        for future in concurrent.futures.as_completed(futures):
            original=futures[future]
            try:
                photo,relative,entry=future.result();selected[photo['assignment']['day_id']].append(photo);files[relative]=entry;completed+=1
            except Exception as error:
                if offline and not allow_missing:raise
                failures.append({'photo_id':original['id'],'day_id':original['assignment']['day_id'],'error_type':type(error).__name__,'message':str(error)})
                print('Ground image unavailable; aerial replacement:',original['id'],type(error).__name__,flush=True)
            if (completed+len(failures))%25==0 or completed+len(failures)==len(jobs):
                progress={'completed':completed,'total':len(jobs),'failures':failures,'updated_utc':now()}
                atomic_json(REPO/'data/media-expansion/ground-progress.json',progress);print(json.dumps({'ground_cached':completed,'ground_total':len(jobs),'failed':len(failures)}),flush=True)
    seen_hashes=set()
    for day in sorted(selected):
        selected[day].sort(key=lambda p:(p['distance_to_section_meters'],p['id']));unique=[]
        for photo in selected[day]:
            if photo['image_sha256'] in seen_hashes:
                failures.append({'photo_id':photo['id'],'day_id':day,'error_type':'duplicate_original_bytes','message':'Identical cached image bytes count once; substitute a distinct aerial view'})
                files.pop(photo['thumbnail_url'].lstrip('/'));continue
            seen_hashes.add(photo['image_sha256']);unique.append(photo)
        selected[day]=unique
    return selected,files,failures


def mercator(point):
    return [MERCATOR_RADIUS*math.radians(point[0]),MERCATOR_RADIUS*math.log(math.tan(math.pi/4+math.radians(point[1])/2))]


def geographic(point):
    return [math.degrees(point[0]/MERCATOR_RADIUS),math.degrees(2*math.atan(math.exp(point[1]/MERCATOR_RADIUS))-math.pi/2)]


def tile_definition(row,column,service):
    info=service['tileInfo'];lod=next(v for v in info['lods'] if v['level']==TILE_LEVEL)
    if info['rows']!=256 or info['cols']!=256 or lod['scale']<MIN_SCALE:raise ValueError('Tile matrix or supported scale changed')
    origin=info['origin'];span=lod['resolution']*256
    west=origin['x']+column*span;east=west+span;north=origin['y']-row*span;south=north-span
    sw=geographic([west,south]);ne=geographic([east,north]);center=geographic([(west+east)/2,(south+north)/2])
    return {'level':TILE_LEVEL,'row':row,'column':column,'origin':origin,'resolution':lod['resolution'],'scale':lod['scale'],
            'native_extent':{'xmin':west,'ymin':south,'xmax':east,'ymax':north,'spatialReference':{'wkid':3857}},
            'geographic_extent':{'xmin':sw[0],'ymin':sw[1],'xmax':ne[0],'ymax':ne[1],'spatialReference':{'wkid':4326}},
            'width':256,'height':256},center


def aerial_candidates(itinerary,routes,cumulative):
    service=json.loads((REPO/'content/sources/leg_photos/service.json').read_bytes());info=service['tileInfo']
    lod=next(v for v in info['lods'] if v['level']==TILE_LEVEL);span=lod['resolution']*256;origin=info['origin'];tiles=set()
    for stage in itinerary['stages']:
        points=routes[stage['id']];totals=cumulative[stage['id']]
        for n,(a,b) in enumerate(zip(points,points[1:])):
            steps=max(1,math.ceil((totals[n+1]-totals[n])/DISCOVERY_STEP_METERS))
            for k in range(steps+1):
                p=mercator([a[j]+k/steps*(b[j]-a[j]) for j in (0,1)])
                tiles.add((math.floor((origin['y']-p[1])/span),math.floor((p[0]-origin['x'])/span)))
    grid=index_route(itinerary['stages'],routes,cumulative);result=defaultdict(list)
    for row,column in sorted(tiles):
        tile,center=tile_definition(row,column,service);nearest=nearest_global(grid,center[1],center[0])
        if nearest is None or nearest[0]>AERIAL_MAX_OFFSET:continue
        offset,_,day,fraction=nearest;witness=point_at(routes[day],cumulative[day],fraction);projected=mercator(witness);extent=tile['native_extent']
        if not (extent['xmin']-1e-6<=projected[0]<=extent['xmax']+1e-6 and extent['ymin']-1e-6<=projected[1]<=extent['ymax']+1e-6):continue
        if not (CONUS[0]<center[0]<CONUS[2] and CONUS[1]<center[1]<CONUS[3]):raise ValueError('Tile center outside checked CONUS rights')
        result[day].append({'tile':tile,'center':center,'distance_meters':offset,'route_fraction':fraction,'route_witness':witness})
    for day in result:result[day].sort(key=lambda item:(item['route_fraction'],item['tile']['row'],item['tile']['column']))
    return result


def choose_tiles(ground,candidates,count=None):
    needed=MINIMUM-len(ground) if count is None else count;occupied=[p['assignment']['route_fraction'] for p in ground];selected=[];choices=list(candidates)
    if len(choices)<needed:raise ValueError('Insufficient uniquely owned aerial tiles for this section')
    while len(selected)<needed:
        if not occupied:choice=min(choices,key=lambda t:abs(t['route_fraction']-.5))
        else:choice=max(choices,key=lambda t:min(abs(t['route_fraction']-f) for f in occupied))
        choices.remove(choice);selected.append(choice);occupied.append(choice['route_fraction'])
    return selected


def verify_frame(record,raw,candidate,source):
    tile=candidate['tile'];url=SERVICE+f'/tile/{tile["level"]}/{tile["row"]}/{tile["column"]}'
    if record.get('provider_type')!='cached-tile' or record.get('tile')!=tile or record.get('request_url')!=url:raise ValueError('Cached native tile identity differs')
    if record.get('service_metadata_sha256')!=source['metadata_sha256'] or digest(raw)!=record.get('image_sha256'):raise ValueError('Cached image/source checksum differs')
    witness={'longitude':candidate['route_witness'][0],'latitude':candidate['route_witness'][1]}
    if record.get('center_longitude')!=candidate['center'][0] or record.get('center_latitude')!=candidate['center'][1] or record.get('route_witness')!=witness:raise ValueError('Cached tile geographic assignment differs')
    mime=record.get('mime',record.get('provider_response',{}).get('mime'))
    if record.get('provider_response')!={'http_status':200,'mime':mime}:raise ValueError('Cached HTTP image facts differ')
    dimensions,variation=validate_tile_image(raw,mime)
    if dimensions!=[256,256] or dimensions!=record.get('decoded_dimensions'):raise ValueError('Native cached JPEG dimensions differ')
    return dimensions,variation,tile['geographic_extent']


def aerial(stage,index,candidate,source,offline=False):
    tile=candidate['tile'];center=candidate['center'];fraction=candidate['route_fraction'];offset=candidate['distance_meters']
    ident=f'aerial-{stage["id"]}-{index:02d}';url=SERVICE+f'/tile/{tile["level"]}/{tile["row"]}/{tile["column"]}'
    image_relative=f'content/media/{ident}.jpg';metadata_relative=f'content/sources/leg_photos/{ident}.json';metadata_path=member(metadata_relative)
    if metadata_path.exists():
        record=json.loads(metadata_path.read_text(encoding='utf-8'));image_relative=record.get('image_path',image_relative);raw=member(image_relative).read_bytes();mime=record.get('mime',record.get('provider_response',{}).get('mime'))
        dimensions,variation,extent=verify_frame(record,raw,candidate,source)
    else:
        if offline:raise ValueError('Required aerial tile is not cached: '+ident)
        raw,mime,status=fetch(url)
        if status!=200 or mime not in ('image/jpeg','image/png'):raise ValueError('Cached source did not return an intact original JPEG/PNG')
        dimensions,variation=validate_tile_image(raw,mime);image_relative=f'content/media/{ident}.'+('jpg' if mime=='image/jpeg' else 'png')
        record={'version':1,'provider_type':'cached-tile','day_id':stage['id'],'photo_id':ident,'route_fraction':fraction,
                'center_longitude':center[0],'center_latitude':center[1],'route_witness':{'longitude':candidate['route_witness'][0],'latitude':candidate['route_witness'][1]},'distance_to_section_meters':offset,
                'request_url':url,'provider_response':{'http_status':status,'mime':mime},'tile':tile,'image_path':image_relative,'mime':mime,
                'source_date':now(),'image_sha256':digest(raw),'image_bytes':len(raw),'decoded_dimensions':dimensions,'pixel_stddev':variation,
                'attribution':source['attribution'],'service_metadata_path':source['metadata_path'],'service_metadata_sha256':source['metadata_sha256'],'rights_references':source['rights_references'],
                'capture_date':None,'minimum_supported_scale':MIN_SCALE}
        dimensions,variation,extent=verify_frame(record,raw,candidate,source)
        atomic_bytes(member(image_relative),raw);atomic_json(metadata_path,record);time.sleep(.25)
    metadata_raw=metadata_path.read_bytes();mile=stage['mile_start']+fraction*stage['distance_miles']
    photo={'id':ident,'title':f'Aerial photograph · {stage["id"]} · trail mile {mile:.2f}',
           'source_url':url,'thumbnail_url':'/'+image_relative,'author':'USDA / USGS The National Map',
           'license':source['license'],'license_url':source['license_url'],'media_kind':'aerial',
           'latitude':center[1],'longitude':center[0],'distance_to_section_meters':round(offset,3),'route_mile':round(mile,5),
           'location_label':f'Aerial tile center {offset:.0f} m from this section near trail mile {mile:.2f}',
           'capture_date':None,'source_retrieved_utc':record['source_date'],
           'location_verification':'Globally nearest-section image center, with a route point inside the original aerial tile; not a ground camera view',
           'review_status':'Original USGS source tile, exact geographic bounds, route ownership, decoded raster and nonblank pixels checked',
           'assignment':{'day_id':stage['id'],'distance_meters':round(offset,3),'method':'nearest-section aerialtile','route_fraction':fraction,'coordinate_role':'imagery_tile_center','route_witness':record['route_witness']},
           'actual_extent':extent,'pixel_dimensions':dimensions,'image_sha256':digest(raw),'source_metadata_path':metadata_relative,
           'source_attribution':source['attribution'],'source_tile':{'level':tile['level'],'row':tile['row'],'column':tile['column']}}
    entry={'sha256':digest(raw),'bytes':len(raw),'mime':mime,'day_id':stage['id'],'photo_id':ident,
           'metadata_path':metadata_relative,'metadata_sha256':digest(metadata_raw),'pixel_dimensions':dimensions,'actual_extent':extent,
           'provider_type':'cached-tile','source_tile':photo['source_tile'],'media_kind':'aerial'}
    return photo,image_relative,entry


def publish(itinerary,itinerary_sha,previous,expected_hash,ground,results,source,report,ground_files):
    old={d['day_id']:d for d in previous['days']};files=dict(ground_files);days=[];manifest_days=[];all_ids=set();centers=set();image_hashes={entry['sha256'] for entry in ground_files.values()}
    for stage in itinerary['stages']:
        day=stage['id'];photos=list(ground[day]);aerial_count=0
        for photo,relative,entry in results.get(day,[]):
            center=(round(photo['latitude'],10),round(photo['longitude'],10))
            if center in centers or entry['sha256'] in image_hashes:raise ValueError('Duplicate aerial center or image bytes cannot count as another photo')
            centers.add(center);image_hashes.add(entry['sha256']);files[relative]=entry;photos.append(photo);aerial_count+=1
        if len(photos)!=MINIMUM:raise ValueError('Minimum photo count not acquired for '+day)
        if any(p['id'] in all_ids for p in photos):raise ValueError('One photo source was assigned to multiple sections')
        all_ids.update(p['id'] for p in photos);photos.sort(key=lambda p:(p['route_mile'],p['id']))
        original=old[day];social=[]
        for photo in photos:
            if photo.get('social_original_url'):social.append({'id':photo['id']+'-flickr','title':photo['title'],'source_url':photo['social_original_url'],'provider':'Flickr','location_label':photo['location_label'],'source_relation':'Original source for a uniquely assigned licensed Commons photograph'})
        coverage={**original.get('coverage',{}),'photo_count':len(photos),'ground_photo_count':len(ground[day]),'aerial_photo_count':aerial_count,
                  'minimum_photos_per_leg':MINIMUM,'minimum_met':True,'photo_gap_reason':None,
                  'ground_photo_gap_reason':None if len(ground[day])>=MINIMUM else f'{len(ground[day])} distinct ground photographs are locally cached, licensed and assigned to this nearest section within 1 km; remaining views are explicitly aerial.'}
        days.append({**original,'photos':photos,'social':social,'coverage':coverage})
        manifest_days.append({'day_id':day,'photo_count':len(photos),'ground_photo_count':len(ground[day]),'aerial_photo_count':aerial_count,'photo_ids':[p['id'] for p in photos],'minimum_met':True,'gap_reason':None})
    summary={**previous.get('summary',{}),'day_count':len(days),'days_with_photos':len(days),'photo_cards':len(all_ids),'unique_photos':len(all_ids),
             'minimum_photos_per_leg':MINIMUM,'days_meeting_photo_minimum':len(days),'ground_photo_cards':sum(map(len,ground.values())),
             'aerial_photo_cards':sum(entry['media_kind']=='aerial' for entry in files.values()),'maximum_selected_photo_offset_meters':MAX_OFFSET,'maximum_photos_per_day':MINIMUM,
             'public_social_cards':sum(len(day['social']) for day in days),'photo_gap_day_ids':[],
             'ground_photo_gap_day_ids':[d['day_id'] for d in days if d['coverage']['ground_photo_count']<MINIMUM]}
    visuals={**previous,'version':1,'curated_utc':now(),'summary':summary,'days':days,
             'source_policy':'Each licensed Commons ground source is assigned once to its globally nearest section within 1 km. Provider geotags are screened, not independently verified camera positions. Missing ground views are filled by distinct original USGS aerial tiles assigned from each image center to its globally nearest section within 500 m, with a known route point inside its bounds. Views are historical overhead imagery. Google availability checks and panorama links are not counted as photographs.'}
    visuals_raw=canonical(visuals)
    manifest={'version':1,'itinerary_sha256':itinerary_sha,'route_release':itinerary['metadata']['route_release'],'minimum_photos_per_leg':MINIMUM,
              'created_utc':now(),'visuals_sha256':digest(visuals_raw),'files':files,'days':manifest_days,'sources':[source],
              'assignment_rules':{'ground_maximum_offset_meters':MAX_OFFSET,'ground_owner':'globally nearest section before selection; equal-distance ties choose earlier day',
                                  'ground_coordinate_role':'provider geotag; camera position unverified','aerial_centers':'Original level16 tile image centers; globally nearest section ownership before selection',
                                  'aerial_maximum_offset_meters':AERIAL_MAX_OFFSET,'aerial_tile_level':TILE_LEVEL,'aerial_minimum_scale':MIN_SCALE,
                                  'counts_exclude':'Maps, panorama links, duplicate source IDs, duplicate aerial centers and byte-identical aerial files'},'ground_discovery_report':report}
    # Publish the allowlist before cards referring to its already verified files.
    if digest((REPO/'content/visuals.json').read_bytes())!=expected_hash:raise ValueError('The visual catalog changed while expansion ran')
    atomic_json(REPO/'content/leg_photo_manifest.json',manifest)
    atomic_bytes(REPO/'content/visuals.json',visuals_raw,expected_hash)
    return manifest

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--plan-only',action='store_true');parser.add_argument('--preview-only',action='store_true');parser.add_argument('--cache-only',action='store_true');parser.add_argument('--ground-cache-only',action='store_true');parser.add_argument('--ground-cached-only',action='store_true');parser.add_argument('--offline',action='store_true');parser.add_argument('--workers',type=int,default=4);args=parser.parse_args()
    if not 1<=args.workers<=4:parser.error('workers must be between 1 and 4')
    itinerary,itinerary_sha,routes,cumulative=load_route();cache=REPO/'data/media-expansion';cache.mkdir(parents=True,exist_ok=True)
    lock=cache/('ground.lock' if args.ground_cache_only else 'expand.lock')
    try:descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:raise RuntimeError('Another expansion owns this cache; inspect an abandoned lock before removing it')
    os.close(descriptor)
    try:
        if args.preview_only:
            source=service_metadata(args.offline);candidates=aerial_candidates(itinerary,routes,cumulative);ground,_=ground_photos(itinerary,routes,cumulative)
            first=itinerary['stages'][0];preview=aerial(first,1,choose_tiles(ground[first['id']],candidates[first['id']],MINIMUM)[0],source,args.offline)
            print(json.dumps({'preview':preview[1],'metadata':preview[2]['metadata_path'],'source':source,'record':preview[0]},indent=2),flush=True);return
        previous_raw=(REPO/'content/visuals.json').read_bytes();previous=json.loads(previous_raw)
        if previous.get('route_release')!=itinerary['metadata']['route_release']:raise ValueError('Existing visuals use a different route release')
        ground,report=ground_photos(itinerary,routes,cumulative)
        if args.ground_cache_only:
            cached,files,failures=cache_ground_photos(ground,args.offline);print(json.dumps({'ground_cached':len(files),'ground_failures':len(failures),'published':False}),flush=True);return
        candidates=aerial_candidates(itinerary,routes,cumulative)
        selected={s['id']:choose_tiles(ground[s['id']],candidates[s['id']],MINIMUM) for s in itinerary['stages']}
        jobs=[(s,i,candidate) for s in itinerary['stages'] for i,candidate in enumerate(selected[s['id']][:MINIMUM-len(ground[s['id']])],1)]
        plan={'version':1,'created_utc':now(),'itinerary_sha256':itinerary_sha,'report':report,'aerial_frames_needed':len(jobs),
              'days':[{'day_id':s['id'],'ground_ids':[p['id'] for p in ground[s['id']]],'available_owned_aerial_tiles':len(candidates[s['id']]),'aerial_tiles':selected[s['id']][:MINIMUM-len(ground[s['id']])]} for s in itinerary['stages']]}
        atomic_json(cache/'plan.json',plan);print(json.dumps({'ground_report':report,'aerial_frames_needed':len(jobs)},indent=2),flush=True)
        if args.plan_only:return
        ground_files={}
        if not args.cache_only:
            ground,ground_files,ground_failures=cache_ground_photos(ground,args.offline or args.ground_cached_only,allow_missing=args.ground_cached_only)
            report['ground_download_failures']=ground_failures;report['cached_ground_photos']=len(ground_files)
            jobs=[(s,i,candidate) for s in itinerary['stages'] for i,candidate in enumerate(selected[s['id']][:MINIMUM-len(ground[s['id']])],1)]
        source=service_metadata(args.offline);results=defaultdict(list);failures=[];completed=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures={pool.submit(aerial,s,i,candidate,source,args.offline):(s['id'],i) for s,i,candidate in jobs}
            for future in concurrent.futures.as_completed(futures):
                day,index=futures[future]
                try:results[day].append(future.result());completed+=1
                except Exception as error:failures.append({'day_id':day,'index':index,'error_type':type(error).__name__,'message':str(error)});print('Frame failed:',day,index,type(error).__name__,flush=True)
                if (completed+len(failures))%25==0 or completed+len(failures)==len(jobs):
                    progress={'completed':completed,'total':len(jobs),'failures':failures,'updated_utc':now()};atomic_json(cache/'progress.json',progress);print(json.dumps({k:v for k,v in progress.items() if k!='failures'}),flush=True)
        if failures:raise RuntimeError(f'{len(failures)} frames were not acquired; original visuals preserved. Review data/media-expansion/progress.json and rerun to resume verified cache.')
        if args.cache_only:print(json.dumps({'cached':completed,'published':False}),flush=True);return
        manifest=publish(itinerary,itinerary_sha,previous,digest(previous_raw),ground,results,source,report,ground_files)
        print(json.dumps({'published':True,'days':len(manifest['days']),'photos':sum(d['photo_count'] for d in manifest['days']),'local_files':len(manifest['files'])},indent=2),flush=True)
    finally:lock.unlink(missing_ok=True)

if __name__=='__main__':main()
