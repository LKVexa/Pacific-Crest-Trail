"""Bounded, resumable public-source discovery. Never copies third-party media bytes."""
import concurrent.futures
import html
import json
import math
import hashlib
import gzip
import os
import uuid
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / 'data' / 'media-discovery'
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'PCTTrainingAdventure/0.1 (personal local educational curation)'

def api(params, cache):
    if cache.exists():
        data = json.loads(cache.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or 'error' in data:
            raise ValueError('Cached provider response is invalid: ' + cache.name)
        return data
    url = API+'?'+urllib.parse.urlencode({'format':'json',**params})
    for attempt in range(9):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':UA})
            with urllib.request.urlopen(req, timeout=50) as stream: data=json.load(stream)
            if not isinstance(data, dict) or 'error' in data: raise ValueError('Provider response is invalid')
            atomic_json(cache, data)
            time.sleep(2.0)
            return data
        except Exception as exc:
            if attempt == 8: raise
            retry = getattr(exc, 'headers', {}).get('Retry-After', '0')
            delay = max(float(retry) if str(retry).isdigit() else 0, min(60, 5 * 2**attempt))
            print('Provider backoff', type(exc).__name__, 'for', delay, 'seconds', flush=True)
            time.sleep(delay)

def cumulative(coords):
    c=[0.0]
    for a,b in zip(coords,coords[1:]):
        lat=(a[1]+b[1])*math.pi/360
        c.append(c[-1]+math.hypot((b[0]-a[0])*111320*math.cos(lat),(b[1]-a[1])*111320))
    return c

def point_at(coords, fraction):
    c=cumulative(coords); target=c[-1]*fraction
    for i in range(1,len(c)):
        if c[i]>=target:
            f=(target-c[i-1])/(c[i]-c[i-1]) if c[i]>c[i-1] else 0
            return [coords[i-1][j]+f*(coords[i][j]-coords[i-1][j]) for j in (0,1)]
    return coords[-1]

def nearest(coords,lat,lon):
    sx=111320*math.cos(math.radians(lat)); sy=111320
    cumulative_m=cumulative(coords)
    best=(float('inf'),0)
    for i,(a,b) in enumerate(zip(coords,coords[1:])):
        ax=(a[0]-lon)*sx; ay=(a[1]-lat)*sy
        bx=(b[0]-lon)*sx; by=(b[1]-lat)*sy
        dx=bx-ax;dy=by-ay;den=dx*dx+dy*dy
        f=max(0,min(1,-(ax*dx+ay*dy)/den)) if den else 0
        distance=math.hypot(ax+f*dx,ay+f*dy)
        if distance<best[0]:best=(distance,(cumulative_m[i]+f*(cumulative_m[i+1]-cumulative_m[i]))/cumulative_m[-1])
    return best

def discover(stage):
    lon,lat=point_at(routes[stage['id']],.5)
    data=api({'action':'query','list':'geosearch','gscoord':f'{lat:.7f}|{lon:.7f}','gsradius':10000,'gsnamespace':6,'gslimit':500},CACHE/(stage['id']+'_geo.json'))
    found=data.get('query',{}).get('geosearch')
    if not isinstance(found,list):
        raise ValueError('Provider geosearch response is incomplete: ' + stage['id'])
    print(stage['id'],len(found),'geotagged candidates',flush=True)
    return stage['id'],found


def plain(value):return re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',html.unescape(str(value)))).strip()
def meta(info,key):return info.get('extmetadata',{}).get(key,{}).get('value','')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def atomic_bytes(path, raw, expected_hash=None):
    """Same-directory verified promotion; file publication is separate from SQLite."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_name(path.name + '.staging-' + uuid.uuid4().hex)
    try:
        with staged.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if sha256(staged.read_bytes()) != sha256(raw):
            raise ValueError('Staged publication checksum mismatch')
        if expected_hash is not None:
            current = sha256(path.read_bytes()) if path.exists() else 'absent'
            if current != expected_hash:
                raise ValueError('Existing visual collection changed; keep it and review this proposal')
        os.replace(staged, path)
    finally:
        if staged.exists():
            staged.unlink()

def atomic_json(path, value, expected_hash=None):
    raw = (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    json.loads(raw)
    atomic_bytes(path,raw,expected_hash)

def merge_manual_panoramas(manifest, previous):
    """Preserve curated source-page links by their existing day, without inventing coverage."""
    if previous:
        if previous.get('route_release') != manifest.get('route_release'):
            raise ValueError('Route release changed; manually review existing panorama associations first')
        old={day['day_id']:day for day in previous['days']}
        for day in manifest['days']:
            retained=old.get(day['day_id'],{}).get('panoramas',[])
            if not isinstance(retained,list) or any(not isinstance(item,dict) or not isinstance(item.get('id'),str) for item in retained):
                raise ValueError('Existing panorama records require review')
            day['panoramas']=retained
            day['coverage']['panorama_count']=len(retained)
    manifest['summary']['sourced_panorama_links']=sum(len(day.get('panoramas',[])) for day in manifest['days'])
    manifest['summary']['days_with_sourced_panoramas']=sum(bool(day.get('panoramas')) for day in manifest['days'])
    manifest['summary']['photo_gap_day_ids']=[day['day_id'] for day in manifest['days'] if not day['photos']]
    manifest['source_policy']+=' Existing manually curated panorama source links are preserved per day. Landmark associations do not establish camera coordinates; interactive viewers remain unverified.'
    return manifest

def validate_visuals(value, stages):
    wanted={stage['id'] for stage in stages}
    found=[day['day_id'] for day in value['days']]
    if len(found)!=len(wanted) or set(found)!=wanted:
        raise ValueError('The visual proposal does not cover exactly this itinerary')
    for day in value['days']:
        if any(not isinstance(day.get(key),list) for key in ['photos','points','social','panoramas']):
            raise ValueError('A visual list is invalid')
        for photo in day['photos']:
            if not photo.get('id') or not photo.get('source_url') or not photo.get('thumbnail_url'):
                raise ValueError('A photo reference is incomplete')

def archive_metadata(cache, repository):
    """Archive public provider JSON bytes, not photographs or personal activity."""
    cache,repository=Path(cache),Path(repository)
    source_files=sorted(set(cache.glob('*_geo.json'))|set(cache.glob('info*.json')))
    if not source_files:
        raise ValueError('No public geographic/image metadata cache files were found')
    # Read and validate all sources before replacing the provenance manifest.
    prepared=[]
    for path in source_files:
        raw=path.read_bytes()
        value=json.loads(raw.decode('utf-8'))
        if not isinstance(value,dict) or 'error' in value:
            raise ValueError('Invalid public source archive: '+path.name)
        prepared.append((path,raw,gzip.compress(raw,mtime=0)))
    destination=repository/'content'/'sources'/'visual_curation'
    records=[]
    for path,raw,compressed in prepared:
        name=path.stem+'.'+sha256(raw)[:16]+'.json.gz'
        target=destination/name
        if target.exists():
            if gzip.decompress(target.read_bytes())!=raw:
                raise ValueError('Archived source identity collision: '+name)
        else:
            atomic_bytes(target,compressed)
        archive_raw=target.read_bytes()
        if sha256(gzip.decompress(archive_raw))!=sha256(raw):
            raise ValueError('Archived source bytes do not match their checksum')
        records.append({'source_filename':path.name,'kind':'geographic_search' if path.name.endswith('_geo.json') else 'image_metadata',
                        'source_endpoint':API,'archive_path':'content/sources/visual_curation/'+name,
                        'source_sha256':sha256(raw),'archive_sha256':sha256(archive_raw),
                        'uncompressed_bytes':len(raw),'compressed_bytes':len(archive_raw),
                        'cache_modified_utc':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
                        'acquisition_time_basis':'Cache filesystem modification time; original HTTP retrieval time and full request URL were not retained.'})
    result={'version':1,'created_utc':datetime.now(timezone.utc).isoformat(),'provider':'Wikimedia Commons public API',
            'scope':'Raw public geographic search and image metadata responses only; no downloaded image/panorama bytes or user workout/journal records.',
            'limits':'Archived provider metadata and permissive-license screening do not establish independent rights, geographic, accessibility or editorial acceptance.',
            'records':records}
    atomic_json(destination/'manifest.json',result)
    return result

def main():
    global itinerary, stages, routes
    if (REPO/'content'/'leg_photo_manifest.json').exists():
        raise RuntimeError('This repository has a sealed minimum-ten-photo edition. Use Expand-Leg-Photos.py to preserve its local images and publication manifest.')
    CACHE.mkdir(parents=True,exist_ok=True)
    ownership=CACHE/'curate.lock'
    try:
        descriptor=os.open(ownership,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError('Another curator owns this cache. Inspect an abandoned lock before removing it.')
    os.close(descriptor)
    try:
        itinerary=json.loads((REPO/'content'/'itinerary.json').read_text(encoding='utf-8'))
        stages=itinerary['stages']
        routes={s['id']:json.loads((REPO/s['geometry_path']).read_text(encoding='utf-8'))['geometry']['coordinates'] for s in stages}
        visual_path=REPO/'content'/'visuals.json'
        previous_raw=visual_path.read_bytes() if visual_path.exists() else None
        previous=json.loads(previous_raw) if previous_raw is not None else None
        previous_hash=sha256(previous_raw) if previous_raw is not None else 'absent'
        run_discovery(stages,previous,previous_hash,visual_path)
    finally:
        ownership.unlink(missing_ok=True)

def run_discovery(stages,previous,previous_hash,visual_path):

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        discovered=dict(pool.map(discover,stages))

    candidate_links={}; ids=set()
    bad=re.compile(r'\b(coat of arms|logo|map|diagram|locomotive|railroad|railway|museum|church|station|school|hospital|plaque|memorial|flag|painting|drawing|portrait|fire engine|truck|train)\b',re.I)
    for s in stages:
        entries=[]
        for p in discovered[s['id']]:
            if bad.search(p['title']):continue
            d,f=nearest(routes[s['id']],p['lat'],p['lon'])
            if d<=5000:entries.append({**p,'distance_to_section_meters':round(d,1),'route_mile':round(s['mile_start']+f*s['distance_miles'],2)})
        entries.sort(key=lambda p:p['distance_to_section_meters'])
        # An upper bound avoids a broad, unbounded Commons crawl.
        candidate_links[s['id']]=entries[:35]
        ids.update(p['pageid'] for p in entries[:35])
    atomic_json(CACHE/'candidate_links.json', candidate_links)
    print('Metadata discovery for',len(ids),'unique candidate photographs',flush=True)
    pages={}
    ordered=sorted(ids)
    for index in range(0,len(ordered),50):
        batch=ordered[index:index+50]
        key='info_'+str(index//50).zfill(3)+'_'+str(batch[0])+'.json'
        result=api({'action':'query','pageids':'|'.join(map(str,batch)),'prop':'imageinfo','iiprop':'url|mime|size|extmetadata','iiurlwidth':900,'iiextmetadatafilter':'Artist|Credit|LicenseShortName|LicenseUrl|UsageTerms|AttributionRequired|Copyrighted|ImageDescription|DateTimeOriginal|ObjectName|Categories'},CACHE/key)
        returned=result.get('query',{}).get('pages')
        if not isinstance(returned,dict):
            raise ValueError('Provider image metadata response is incomplete')
        pages.update(returned)
        print('Metadata',min(index+50,len(ordered)),'/',len(ordered),flush=True)

    good_terms=re.compile(r'\b(trail|mountain|forest|wilderness|lake|river|creek|meadow|ridge|peak|pass|landscape|scenic|valley|canyon|rock|falls|hiking|pct|pacific crest|sierra|cascades|desert|wildflower|summit|volcano|basin|crater|tarn|pond|snow|sunset|waterfall|camp)\b',re.I)
    days=[]; reused={}; license_exclusions=0
    for s in stages:
        eligible=[]
        for link in candidate_links[s['id']]:
            page=pages.get(str(link['pageid']),{}); info=(page.get('imageinfo') or [{}])[0]
            lic=plain(meta(info,'LicenseShortName'))
            lic_url=meta(info,'LicenseUrl')
            if not (lic.lower().startswith(('cc by','cc0','public domain','pd')) or lic.lower() in ('cc-zero','cc-by-sa-4.0','cc-by-4.0')):
                license_exclusions+=1;continue
            if not info.get('mime','').startswith('image/') or info.get('mime') in ('image/svg+xml','image/gif') or info.get('width',0)<600 or info.get('height',0)<350:continue
            description=plain(meta(info,'ImageDescription'))
            cats=plain(meta(info,'Categories'))
            if not good_terms.search(link['title']+' '+description+' '+cats):continue
            title=plain(meta(info,'ObjectName')) or link['title'].removeprefix('File:')
            thumbnail=info.get('thumburl') or info.get('url')
            if not thumbnail:continue
            distance=link['distance_to_section_meters']
            location='Geotag within 250 m of this section' if distance<=250 else f'Nearby geotag, {distance/1000:.1f} km from this section'
            credit=meta(info,'Credit')
            flickr=re.search(r'https?://(?:www\.)?flickr\.com/[^\s"<>]+',credit)
            item={'id':'commons-'+str(link['pageid']),'title':title,'source_url':info.get('descriptionurl'),'thumbnail_url':thumbnail,'author':plain(meta(info,'Artist')) or 'See source credits','license':lic,'license_url':lic_url or 'https://commons.wikimedia.org/wiki/Commons:Licensing','latitude':link['lat'],'longitude':link['lon'],'distance_to_section_meters':distance,'route_mile':link['route_mile'],'location_label':location,'description':description[:650],'capture_date':plain(meta(info,'DateTimeOriginal')) or None,'location_verification':'Provider geotag matched geometrically; subject and camera position may differ','review_status':'Geospatial and license metadata screened; not individually field-verified','social_original_url':html.unescape(flickr.group(0)) if flickr else None}
            score=distance+reused.get(item['id'],0)*400
            if 'pacific crest' in (title+' '+description+' '+cats).lower():score-=700
            eligible.append((score,item))
        eligible.sort(key=lambda x:x[0])
        photos=[]
        # Prefer a mix of locations, then allow nearby shots with explicit proximity labels.
        for score,item in eligible:
            if len(photos)>=6:break
            if any(abs(item['latitude']-p['latitude'])<.0004 and abs(item['longitude']-p['longitude'])<.0004 for p in photos):continue
            photos.append(item);reused[item['id']]=reused.get(item['id'],0)+1
        points=[]
        for i,fraction in enumerate((.15,.5,.85),1):
            lon,lat=point_at(routes[s['id']],fraction)
            viewpoint=f'{lat:.7f},{lon:.7f}'
            points.append({'id':s['id']+'-view-'+str(i),'mile':round(s['mile_start']+fraction*s['distance_miles'],2),'latitude':round(lat,7),'longitude':round(lon,7),'streetview_url':'https://www.google.com/maps/@?'+urllib.parse.urlencode({'api':1,'map_action':'pano','viewpoint':viewpoint,'heading':0,'pitch':0,'fov':90}),'terrain_url':'https://www.google.com/maps/@?'+urllib.parse.urlencode({'api':1,'map_action':'map','center':viewpoint,'zoom':14,'basemap':'terrain'}),'streetview_status':'unverified','sampling_basis':'15%, 50%, 85% of simplified section geographic path; displayed trail mile is approximate','coverage_note':'Google may return a nearby panorama or no imagery. This link does not establish PCT panorama coverage.'})
        social=[]
        for p in photos:
            if p['social_original_url']:
                social.append({'id':p['id']+'-flickr','title':p['title'],'source_url':p['social_original_url'],'provider':'Flickr','location_label':p['location_label'],'source_relation':'Licensed Commons image with original Flickr source recorded by provider'})
        days.append({'day_id':s['id'],'points':points,'photos':photos,'panoramas':[],'social':social,'coverage':{'photo_count':len(photos),'panorama_count':0,'streetview_verified_count':0,'streetview_unverified_count':3,'candidate_count':len(discovered[s['id']]),'photo_gap_reason':None if photos else 'No reusable, relevant geotagged photograph passed this bounded public-source search within 5 km.'}})

    summary={'day_count':len(days),'days_with_photos':sum(bool(d['photos']) for d in days),'photo_cards':sum(len(d['photos']) for d in days),'unique_photos':len(reused),'streetview_checkpoints':len(days)*3,'verified_google_panoramas':0,'public_social_cards':sum(len(d['social']) for d in days),'commons_geo_requests':len(stages),'license_exclusions':license_exclusions,'search_radius_meters':10000,'maximum_selected_photo_offset_meters':5000,'per_day_candidate_cap':35,'maximum_photos_per_day':6}
    manifest={'version':1,'curated_utc':datetime.now(timezone.utc).isoformat(),'route_release':itinerary['metadata']['route_release'],'summary':summary,'source_policy':'Public pages and official provider metadata only. Original media remains on its source host; creator, license and proximity shown. Search results and location links are not treated as verified 360 imagery.','days':days}
    manifest = merge_manual_panoramas(manifest, previous)
    validate_visuals(manifest, stages)
    archive_metadata(CACHE, REPO)
    atomic_json(visual_path, manifest, expected_hash=previous_hash)
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    main()
