/* Trail progress comes from the local service. Browser storage holds display preferences and uncertain operations for safe retries. */
'use strict';

const element = id => document.getElementById(id);
const ui = Object.fromEntries([
  'status-banner','loading-view','day-view','day-title','day-eyebrow','day-state','day-summary',
  'mile-start','mile-end','leg-distance','day-map','map-error','full-map-link','map-heading','map-subtitle',
  'map-topography','map-topography-detail','map-topography-units','map-topography-source','map-topography-date','map-topographic-toggle','map-satellite-toggle',
  'start-coordinates','end-coordinates','briefing-copy','briefing-points','orientation-copy',
  'orientation-block','dossier-link','completion-panel','completion-heading','completion-description',
  'completion-action','complete-ack','complete-button','pending-action','pending-description',
  'retry-button','completion-message','completion-eligibility','previous-button','next-button','leg-position','source-copy',
  'progress-heading','progress-detail','trail-progress','progress-miles','progress-days','resume-button',
  'refresh-button','day-list','day-search','search-result','empty-search','section-count','trail-sidebar','itinerary-button','current-day-button',
  'overview-button','overview-dialog','close-overview','overview-description',
  'visual-count','visual-status','photo-gallery','trail-photo','photo-error','previous-photo',
  'next-photo','photo-position','photo-title','photo-location','photo-attribution','photo-source',
  'photo-gap','photo-thumbnails','photo-kind','visual-point','visual-point-coordinates','streetview-link','terrain-link','point-gap',
  'panorama-list','panorama-gap','social-list','social-gap','visual-coverage-summary'
].map(id => [id, element(id)]));

const app = {itinerary:null, stages:[], byId:new Map(), trail:null, nonce:null, selected:null, pending:null, saving:false, refreshing:false,
  visuals:new Map(), visualsLoading:true, visualsError:false, visualPhotos:[], visualPoints:[], photoIndex:0,
  topography:null, topographicDays:new Map(), topographyLoading:false,
  satellite:null, satelliteDays:new Map(), satelliteLoading:false, mapStyle:'topographic'};
try {if(localStorage.getItem(`trail.map-style.${location.host}`)==='satellite')app.mapStyle='satellite';}catch{}
const pendingKey = `pct.pending-completion.${location.host}`;
const decimal = number => Number(number).toLocaleString('en-US', {minimumFractionDigits:1, maximumFractionDigits:2});
const dayLabel = number => String(number).padStart(3, '0');
const isCompleted = id => Boolean(app.trail?.completed_day_ids?.includes(id));
const isCurrent = id => Boolean(app.trail && app.trail.current_day_id === id && !app.trail.expedition_complete);
const displayTitle = value => String(value || '').replace(/\bPacific\s+Crest\s+Trail\b/gi,'the trail').replace(/\bPCT\b/gi,'Trail').replace(/^the trail\b/i,'Trail');
const displayCopy = value => String(value || '').replace(/\bPacific\s+Crest\s+Trail\b/gi,'the trail').replace(/\bPCTA route\b/gi,'published route').replace(/\bPCT\b/gi,'trail');

class ServiceError extends Error {
  constructor(message, status=0, data=null) {super(message); this.name='ServiceError'; this.status=status; this.data=data;}
}

async function request(path, options={}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(path, {cache:'no-store', credentials:'same-origin', ...options, signal:controller.signal});
    let data;
    try {data = await response.json();} catch {throw new ServiceError('The local service returned an unreadable response.', response.status);}
    if (!response.ok) throw new ServiceError(data?.error?.message || `The local service could not finish this request (${response.status}).`, response.status, data);
    return data;
  } catch (error) {
    if (error instanceof ServiceError) throw error;
    throw new ServiceError(error.name === 'AbortError' ? 'The local service did not respond in time.' : 'The local service could not be reached.');
  } finally {clearTimeout(timeout);}
}

function showBanner(message, type='') {
  ui['status-banner'].textContent = message;
  ui['status-banner'].className = `status-banner ${type}`.trim();
  ui['status-banner'].hidden = !message;
}

function localAsset(path, kind) {
  if (typeof path !== 'string') return null;
  const normalized = '/' + path.replace(/^\.?\//, '');
  const suffix = kind === 'maps' ? 'svg' : 'html';
  return new RegExp(`^/content/${kind}/[A-Za-z0-9_-]+\\.${suffix}$`).test(normalized) ? normalized : null;
}

function parseItinerary(data) {
  if (!data || !Array.isArray(data.stages) || data.stages.length === 0) throw new Error('The itinerary contains no daily sections.');
  const seen = new Set();
  const stages = data.stages.slice().sort((a,b) => a.day_number-b.day_number);
  for (const [index, stage] of stages.entries()) {
    if (!/^day-\d{3,}$/.test(stage.id) || seen.has(stage.id) || stage.day_number !== index+1 ||
        !Number.isFinite(stage.mile_start) || !Number.isFinite(stage.mile_end) || stage.mile_end <= stage.mile_start ||
        !Number.isFinite(stage.distance_miles) || stage.distance_miles <= 0 || !localAsset(stage.map_path,'maps')) {
      throw new Error('A daily section has an invalid identity, distance, or map reference.');
    }
    seen.add(stage.id);
  }
  app.itinerary = data;
  app.stages = stages;
  app.byId = new Map(stages.map(stage => [stage.id, stage]));
}

function applyState(state) {
  if (!state || typeof state.campaign_id !== 'string' || !Number.isInteger(state.revision) ||
      !Array.isArray(state.completed_day_ids) ||
      (state.current_day_id !== null && !app.byId.has(state.current_day_id))) {
    throw new Error('The saved trail record does not match this itinerary.');
  }
  if (app.trail && app.trail.campaign_id !== state.campaign_id) {
    throw new Error('The local campaign changed. Reload the page before saving a section.');
  }
  app.trail = state;
}

function restorePending() {
  try {
    const pending = JSON.parse(localStorage.getItem(pendingKey) || 'null');
    if (pending && pending.campaign_id === app.trail?.campaign_id && app.byId.has(pending.day_id) &&
        /^[A-Za-z0-9_-]{12,100}$/.test(pending.operation_id) && Number.isInteger(pending.expected_revision)) {
      app.pending = pending;
    }
  } catch {/* An unavailable browser cache never changes the authoritative trail record. */}
}

function persistPending(pending) {
  app.pending = pending;
  try {
    if (pending) localStorage.setItem(pendingKey, JSON.stringify(pending));
    else localStorage.removeItem(pendingKey);
  } catch {/* In-memory retries remain safe because the service requires the original day and revision. */}
}

function coordinates(point) {
  if (!point || !Number.isFinite(point.latitude) || !Number.isFinite(point.longitude)) return 'Coordinates unavailable in this route release';
  return `${Math.abs(point.latitude).toFixed(5)}° ${point.latitude >= 0 ? 'N' : 'S'}, ${Math.abs(point.longitude).toFixed(5)}° ${point.longitude >= 0 ? 'E' : 'W'}`;
}

function externalUrl(value) {
  try {const url=new URL(value);return url.protocol==='https:'&&!url.username&&!url.password?url.href:null;}catch{return null;}
}

function safeMapRevision(value) {
  return typeof value==='string'&&/^[A-Za-z0-9._-]{1,128}$/.test(value)?value:null;
}

function renderMapPresentation(stage) {
  const topoRecord=app.topographicDays.get(stage.id),satRecord=app.satelliteDays.get(stage.id);
  const matchesRoute=app.topography?.route_release===app.itinerary?.metadata?.route_release;
  const topographic=Boolean(matchesRoute&&topoRecord?.topographic===true&&safeMapRevision(topoRecord.map_revision||app.topography.map_revision));
  const satelliteReady=Boolean(app.satellite?.route_release===app.itinerary?.metadata?.route_release&&satRecord?.map_path===`content/maps/satellite-${stage.id}.svg`&&safeMapRevision(satRecord.map_revision));
  const satellite=app.mapStyle==='satellite'&&satelliteReady;
  const publication=satellite?app.satellite:app.topography,record=satellite?satRecord:topoRecord;
  const revision=safeMapRevision(record?.map_revision||publication?.map_revision);
  const path=localAsset(satellite?satRecord.map_path:stage.map_path,'maps');
  const map=(satellite||topographic)?`${path}?map_revision=${encodeURIComponent(revision)}`:path;
  ui['map-topographic-toggle'].setAttribute('aria-pressed',String(!satellite));
  ui['map-satellite-toggle'].setAttribute('aria-pressed',String(satellite));
  ui['map-satellite-toggle'].disabled=!satelliteReady;
  ui['map-satellite-toggle'].title=satelliteReady?'Show satellite and aerial imagery for this daily route':'Satellite imagery has not been published for this section';
  if(ui['day-map'].getAttribute('src')!==map) {
    ui['map-error'].hidden=true;
    ui['day-map'].src=map;
  }
  ui['day-map'].alt=`${satellite?'Satellite and aerial trail map':topographic?'Topographic trail map':'Trail route'} for Day ${stage.day_number}, from trail mile ${decimal(stage.mile_start)} to ${decimal(stage.mile_end)}, with section start and finish marked.${satellite?' Historical source imagery shows the area beneath the same daily route.':topographic?' Terrain shading and contours give historical geographic context; contour detail and interval vary.':''} Exact endpoint coordinates follow below.`;
  ui['full-map-link'].href=map;
  ui['map-heading'].textContent=satellite?'Today’s satellite route':topographic?'Today’s topographic route':'Today’s route';
  ui['map-subtitle'].textContent=`${stage.region || 'The trail'} · ${decimal(stage.distance_miles)} mapped miles${satellite?' · Satellite / aerial imagery':topographic?' · Terrain and contour context':''}`;
  ui['map-topography'].hidden=!(satellite||topographic);
  if(!(satellite||topographic))return;
  const terrain=typeof record.terrain_note==='string'&&record.terrain_note.trim()?record.terrain_note:'Terrain shading and contours from the USGS topographic basemap.';
  const contours=typeof record.contour_note==='string'&&record.contour_note.trim()?record.contour_note:'Contour detail and interval vary with location and zoom.';
  ui['map-topography-detail'].textContent=satellite?'Historical satellite / aerial orthoimagery from the USGS National Map. The route, start and finish checkpoints match the topographic view. Imagery is cached locally; capture dates vary and are not established for each tile.':`${terrain} ${contours}`;
  const units=new Map([['m','metres'],['ft','feet'],['meters','metres'],['metres','metres'],['feet','feet']]).get(record.elevation_unit);
  ui['map-topography-units'].textContent=satellite?'This imagery does not show live weather, closures, current water availability or verified stopping places.':units?`Source elevation-label units: ${units}. Terrain is historical map context, not a report of current conditions.`:'Elevation-label units are not supplied for this raster source. Terrain is historical map context, not a report of current conditions.';
  const sourceCopy=ui['map-topography-source'];sourceCopy.replaceChildren();
  const ids=new Set(Array.isArray(record.source_ids)?record.source_ids:[]);
  const sources=(Array.isArray(publication.sources)?publication.sources:[]).filter(source=>ids.has(source.id));
  if(!sources.length)sourceCopy.textContent='Basemap source details are not supplied for this section.';
  for(const [index,source] of sources.entries()) {
    if(index)sourceCopy.append(document.createTextNode(' · '));
    const title=typeof source.title==='string'?source.title:'Basemap source';
    const url=externalUrl(source.url);
    if(url){const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=title;sourceCopy.append(link);}
    else sourceCopy.append(document.createTextNode(title));
    if(typeof source.attribution==='string'&&source.attribution)sourceCopy.append(document.createTextNode(` — ${source.attribution}`));
  }
  const date=typeof record.source_date==='string'?new Date(record.source_date):null;
  const validDate=Boolean(date&&Number.isFinite(date.getTime()));
  ui['map-topography-date'].hidden=!validDate;
  ui['map-topography-date'].textContent=validDate?`Basemap snapshot retrieved: ${date.toLocaleString('en-US',{timeZone:'UTC',year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit',hour12:false})} UTC. This is the retrieval date, not the terrain survey date.`:'';
}

async function loadTopography() {
  if(app.topographyLoading)return;
  app.topographyLoading=true;
  try {
    const data=await request('/api/topography');
    if(data?.version!==1 || typeof data.route_release!=='string' || !Array.isArray(data.days))return;
    app.topography=data;
    app.topographicDays=new Map(data.days.filter(day=>day&&typeof day.day_id==='string'&&/^day-\d{3,}$/.test(day.day_id)).map(day=>[day.day_id,day]));
    const stage=app.byId.get(app.selected);if(stage)renderMapPresentation(stage);
  }catch{/* Optional map metadata does not change the saved trail or require a remote request. */}
  finally{app.topographyLoading=false;}
}

async function loadSatellite() {
  if(app.satelliteLoading)return;app.satelliteLoading=true;
  try {
    const data=await request('/api/satellite');
    if(data?.version!==1||data.route_release!==app.itinerary?.metadata?.route_release||!Array.isArray(data.days))return;
    app.satellite=data;app.satelliteDays=new Map(data.days.filter(day=>app.byId.has(day?.day_id)).map(day=>[day.day_id,day]));
    const stage=app.byId.get(app.selected);if(stage)renderMapPresentation(stage);
  }catch{/* Optional map style leaves the current dossier usable. */}
  finally{app.satelliteLoading=false;}
}

function chooseMapStyle(style) {
  app.mapStyle=style;try{localStorage.setItem(`trail.map-style.${location.host}`,style);}catch{}
  const stage=app.byId.get(app.selected);if(stage)renderMapPresentation(stage);
}

function photoUrl(value) {
  if(typeof value==='string'&&/^\/content\/media\/aerial-day-\d{3}-\d{2}\.(jpg|png)$/.test(value))return value;
  if(typeof value==='string'&&/^\/content\/media\/commons-[A-Za-z0-9_-]+\.(jpg|png|webp)$/.test(value))return value;
  const valueUrl=externalUrl(value);
  if(!valueUrl)return null;
  const url=new URL(valueUrl);
  return ['upload.wikimedia.org','thumb.wikimedia.org'].includes(url.hostname)?url.href:null;
}

function locationLine(record) {
  const parts=[];
  if(record.location_label)parts.push(String(record.location_label));
  if(Number.isFinite(record.route_mile))parts.push(`Near route mile ${decimal(record.route_mile)}`);
  if(Number.isFinite(record.distance_to_section_meters)&&record.distance_to_section_meters>=0) {
    const miles=record.distance_to_section_meters/1609.344;
    parts.push(miles<.1?'Within 0.1 mi of this mapped section':`About ${decimal(miles)} mi from this mapped section`);
  }
  return parts.join(' · ');
}

function renderPhoto({eager=false}={}) {
  const photo=app.visualPhotos[app.photoIndex];
  ui['photo-gallery'].hidden=!photo;
  if(!photo){ui['trail-photo'].removeAttribute('src');return;}
  ui['photo-error'].hidden=true;
  const aerial=photo.media_kind==='aerial';
  ui['photo-kind'].textContent=aerial?'AERIAL PHOTOGRAPH':'GROUND PHOTOGRAPH';
  ui['trail-photo'].loading=eager?'eager':'lazy';
  ui['trail-photo'].alt=`${aerial?'Aerial photograph of an area containing this leg':'Ground photograph near this leg'}: ${photo.title || 'Trail photograph'}${photo.location_label?` — ${photo.location_label}`:''}`;
  ui['trail-photo'].src=photoUrl(photo.thumbnail_url);
  ui['photo-position'].textContent=`Photo ${app.photoIndex+1} of ${app.visualPhotos.length}`;
  ui['previous-photo'].disabled=app.photoIndex===0;
  ui['next-photo'].disabled=app.photoIndex===app.visualPhotos.length-1;
  ui['photo-title'].textContent=photo.title || 'A view near the trail';
  const geo=Number.isFinite(photo.latitude)&&Number.isFinite(photo.longitude)?coordinates(photo):'';
  ui['photo-location'].textContent=[locationLine(photo),geo,photo.capture_date?`Captured: ${photo.capture_date}`:'Capture date unknown',photo.review_status || 'Source metadata screened; exact view unverified'].filter(Boolean).join(' · ');
  ui['photo-attribution'].replaceChildren();
  ui['photo-attribution'].append(document.createTextNode(`Photo: ${photo.author || 'See source credit'} · `));
  const licenseUrl=externalUrl(photo.license_url);
  if(licenseUrl){const link=document.createElement('a');link.href=licenseUrl;link.target='_blank';link.rel='noopener noreferrer';link.textContent=photo.license || 'License details';ui['photo-attribution'].append(link);}
  else ui['photo-attribution'].append(document.createTextNode(photo.license || 'See source licensing'));
  ui['photo-source'].href=externalUrl(photo.source_url);
  for(const [index,button] of Array.from(ui['photo-thumbnails'].children).entries())button.setAttribute('aria-pressed',String(index===app.photoIndex));
}

function renderPhotoThumbnails() {
  ui['photo-thumbnails'].replaceChildren(...app.visualPhotos.map((photo,index)=>{
    const button=document.createElement('button');button.type='button';button.className='photo-thumbnail';
    const kind=photo.media_kind==='aerial'?'Aerial':'Ground';
    button.setAttribute('aria-label',`View photo ${index+1}: ${kind} — ${photo.title || 'Trail photograph'}`);
    button.setAttribute('aria-pressed',String(index===app.photoIndex));
    const img=document.createElement('img');img.src=photoUrl(photo.thumbnail_url);img.alt='';img.loading='lazy';img.referrerPolicy='no-referrer';
    const caption=document.createElement('span');caption.textContent=`${String(index+1).padStart(2,'0')} / ${kind}`;
    button.append(img,caption);button.addEventListener('click',()=>{app.photoIndex=index;renderPhoto({eager:true});});return button;
  }));
}

function renderPoint() {
  const point=app.visualPoints.find(value=>value.id===ui['visual-point'].value);
  ui['visual-point-coordinates'].textContent=point?coordinates(point):'';
  const street=point?externalUrl(point.streetview_url):null;
  const terrain=point?externalUrl(point.terrain_url):null;
  ui['streetview-link'].hidden=!street;ui['terrain-link'].hidden=!terrain;
  if(street)ui['streetview-link'].href=street;
  if(terrain)ui['terrain-link'].href=terrain;
}

function sourceCards(records, container, kind) {
  const cards=[];
  for(const record of records) {
    const source=externalUrl(record.source_url);if(!source)continue;
    const card=document.createElement('a');card.className='visual-source-card';card.href=source;card.target='_blank';card.rel='noopener noreferrer';
    const title=document.createElement('strong');title.textContent=`${record.title || (kind==='panorama'?'360° look-around':'Public trail story')} ↗`;
    const location=document.createElement('span');location.textContent=locationLine(record) || 'See source for location details';
    const credit=document.createElement('small');credit.textContent=kind==='panorama'?`Spherical source page${record.author?` · ${record.author}`:''}${record.capture_date?` · ${record.capture_date}`:''} · Viewer untested`:`${record.provider || 'Public source'} · External page`;
    card.append(title,location,credit);cards.push(card);
  }
  container.replaceChildren(...cards);
  return cards.length;
}

function renderVisuals({resetPhoto=true}={}) {
  if(resetPhoto)app.photoIndex=0;
  const day=app.visuals.get(app.selected);
  app.visualPhotos=(Array.isArray(day?.photos)?day.photos:[]).filter(photo=>photoUrl(photo.thumbnail_url)&&externalUrl(photo.source_url));
  app.visualPoints=(Array.isArray(day?.points)?day.points:[]).filter(point=>typeof point.id==='string'&&Number.isFinite(point.mile));
  app.photoIndex=Math.max(0,Math.min(app.photoIndex,app.visualPhotos.length-1));
  renderPhotoThumbnails();renderPhoto();
  const panoramas=sourceCards(Array.isArray(day?.panoramas)?day.panoramas:[],ui['panorama-list'],'panorama');
  const social=sourceCards(Array.isArray(day?.social)?day.social:[],ui['social-list'],'social');
  const selectedPoint=ui['visual-point'].value;
  ui['visual-point'].replaceChildren(...app.visualPoints.map(point=>{const option=document.createElement('option');option.value=point.id;option.textContent=`Route mile ${decimal(point.mile)}`;return option;}));
  if(app.visualPoints.some(point=>point.id===selectedPoint))ui['visual-point'].value=selectedPoint;
  ui['visual-point'].disabled=!app.visualPoints.length;
  renderPoint();
  ui['visual-count'].textContent=app.visualPhotos.length?`${app.visualPhotos.length} photo${app.visualPhotos.length===1?'':'s'}`:panoramas?`${panoramas} look-around${panoramas===1?'':'s'}`:'Source coverage';
  if(app.visualsLoading) {
    ui['visual-status'].textContent='Loading the photo and look-around collection…';
  } else if(app.visualsError) {
    ui['visual-status'].textContent='The visual collection could not be loaded. Your route map and saved trail progress are still available.';
  } else {
    const ground=app.visualPhotos.filter(photo=>photo.media_kind!=='aerial').length;
    const aerial=app.visualPhotos.length-ground;
    ui['visual-status'].textContent=app.visualPhotos.length?`${app.visualPhotos.length} images for this leg: ${ground} ground photograph${ground===1?'':'s'} and ${aerial} labeled aerial view${aerial===1?'':'s'}. Ground photos are assigned by source location; each aerial area contains a point on this section’s route.`:'Explore this section’s checkpoint links and public sources. Photo coverage varies along the trail.';
  }
  ui['photo-gap'].hidden=app.visualsLoading || app.visualsError || Boolean(app.visualPhotos.length);
  ui['photo-gap'].textContent='No nearby licensed photo is included for this section in the current collection.';
  ui['point-gap'].hidden=app.visualsLoading || app.visualsError || Boolean(app.visualPoints.length);
  ui['point-gap'].textContent='No look-around checkpoint links are included for this section in the current collection.';
  ui['panorama-gap'].hidden=app.visualsLoading || app.visualsError || Boolean(panoramas);
  ui['panorama-gap'].textContent='No independently sourced 360° panorama is included for this section. Use “Check Street View” to check Google Maps availability.';
  ui['social-gap'].hidden=app.visualsLoading || app.visualsError || Boolean(social);
  ui['social-gap'].textContent='No public social post is included for this section in the current collection.';
  const allDays=app.stages.length?app.stages.map(stage=>app.visuals.get(stage.id)):Array.from(app.visuals.values());
  const photoDays=allDays.filter(value=>Array.isArray(value?.photos)&&value.photos.some(photo=>photoUrl(photo.thumbnail_url)&&externalUrl(photo.source_url))).length;
  const panoramaDays=allDays.filter(value=>Array.isArray(value?.panoramas)&&value.panoramas.some(panorama=>externalUrl(panorama.source_url))).length;
  const completePhotoDays=allDays.filter(value=>Array.isArray(value?.photos)&&value.photos.filter(photo=>photoUrl(photo.thumbnail_url)&&externalUrl(photo.source_url)).length>=10).length;
  ui['visual-coverage-summary'].textContent=app.visualsLoading || app.visualsError?'':`Collection coverage: ${completePhotoDays} of ${allDays.length} legs have at least 10 photographs; ${photoDays} include photos; ${panoramaDays} include sourced 360° look-arounds.`;
}

async function loadVisuals() {
  try {
    const data=await request('/api/visuals');
    if(data?.version!==1 || data.route_release!==app.itinerary?.metadata?.route_release || !Array.isArray(data.days))throw new Error('The visual collection does not match this itinerary.');
    app.visuals=new Map(data.days.filter(day=>typeof day.day_id==='string').map(day=>[day.day_id,day]));
    app.visualsError=false;
  }catch {app.visualsError=true;}
  finally {app.visualsLoading=false;if(app.selected)renderVisuals();}
}

function renderProgress() {
  const stages = app.stages;
  const totalMiles = Number(app.itinerary?.metadata?.total_miles) || stages[stages.length-1]?.mile_end || 1;
  const finished = stages.filter(stage => isCompleted(stage.id));
  const completedMiles = finished.reduce((total,stage) => total+stage.distance_miles,0);
  ui['trail-progress'].max = totalMiles;
  ui['trail-progress'].value = Math.min(completedMiles,totalMiles);
  ui['progress-miles'].textContent = `${decimal(completedMiles)} / ${decimal(totalMiles)} mi`;
  ui['progress-days'].textContent = `${finished.length} / ${stages.length} sections`;
  ui['section-count'].textContent = String(stages.length);
  const current = app.byId.get(app.trail?.current_day_id);
  ui['current-day-button'].disabled=!app.trail;
  ui['current-day-button'].textContent=app.trail?.expedition_complete?'Final day':current?`Current day ${current.day_number}`:'Current day';
  if (!app.trail) {
    ui['progress-heading'].textContent = 'Saved place unavailable';
    ui['progress-detail'].textContent = 'You can browse the maps. Reconnect to the local service before saving progress.';
    ui['resume-button'].disabled = true;
  } else if (app.trail.expedition_complete) {
    ui['progress-heading'].textContent = 'Northern terminus reached';
    ui['progress-detail'].textContent = 'Your virtual itinerary is complete. Every daily dossier remains available to revisit.';
    ui['resume-button'].textContent = 'Revisit the final section';
    ui['resume-button'].disabled = false;
  } else if (current) {
    ui['progress-heading'].textContent = `Day ${current.day_number} is ready`;
    ui['progress-detail'].textContent = `Your saved start is trail mile ${decimal(current.mile_start)}. Continue this section whenever you are ready.`;
    ui['resume-button'].textContent = `Return to Day ${current.day_number}`;
    ui['resume-button'].disabled = false;
  }
  const target = Number(app.itinerary?.metadata?.daily_target_miles) || 10;
  ui['overview-description'].textContent = `${stages.length} virtual sections across ${decimal(totalMiles)} mapped miles, targeting about ${decimal(target)} miles per dossier. Boundaries follow the published route geometry.`;
  ui['overview-button'].disabled = !stages.length;
}

function renderDayList() {
  const query = ui['day-search'].value.trim().toLowerCase();
  const exactDay = /^\d+$/.test(query) ? Number(query) : null;
  const matches = app.stages.filter(stage => !query || stage.day_number === exactDay ||
    `day ${stage.day_number} ${dayLabel(stage.day_number)} ${stage.title || ''} ${stage.region || ''} ${decimal(stage.mile_start)} ${decimal(stage.mile_end)}`.toLowerCase().includes(query));
  const fragment = document.createDocumentFragment();
  for (const stage of matches) {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'day-item'; button.dataset.dayId = stage.id;
    if (stage.id === app.selected) button.setAttribute('aria-current','page');
    if (isCurrent(stage.id)) button.classList.add('is-current');
    if (isCompleted(stage.id)) button.classList.add('is-complete');
    const number = document.createElement('span'); number.className='day-number';
    number.append(document.createTextNode('DAY'));
    const strong = document.createElement('strong'); strong.textContent=dayLabel(stage.day_number); number.append(strong);
    const copy = document.createElement('span'); copy.className='day-item-copy';
    const title = document.createElement('strong'); title.textContent=stage.region || displayTitle(stage.title) || 'The trail';
    const detail = document.createElement('small'); detail.textContent=`Mile ${decimal(stage.mile_start)}–${decimal(stage.mile_end)}`;
    copy.append(title,detail); button.append(number,copy);
    const indicator = document.createElement('span'); indicator.className='day-indicator';
    indicator.textContent=isCurrent(stage.id)?'CURRENT':isCompleted(stage.id)?'DONE':'';
    if(indicator.textContent) button.append(indicator);
    button.setAttribute('aria-label', `Day ${stage.day_number}, ${title.textContent}, trail miles ${decimal(stage.mile_start)} to ${decimal(stage.mile_end)}${isCurrent(stage.id)?', current section':isCompleted(stage.id)?', complete':''}`);
    button.addEventListener('click',()=>{selectDay(stage.id);setItineraryOpen(false);element('dossier').focus({preventScroll:true});});
    fragment.append(button);
  }
  ui['day-list'].replaceChildren(fragment);
  ui['empty-search'].hidden=matches.length>0;
  ui['search-result'].textContent=query?`${matches.length} matching section${matches.length===1?'':'s'}`:`${app.stages.length} dossiers · open any section`;
}

function setItineraryOpen(open) {
  ui['trail-sidebar'].hidden=!open;
  ui['itinerary-button'].setAttribute('aria-expanded',String(open));
  document.body.classList.toggle('itinerary-open',open);
  if(open)ui['day-list'].querySelector('[aria-current="page"]')?.scrollIntoView({block:'nearest'});
}

function renderSource() {
  const metadata = app.itinerary?.metadata || {};
  const p = ui['source-copy']; p.replaceChildren();
  const label = metadata.source_name || 'Pacific Crest Trail Association route data';
  p.append(document.createTextNode('Route geography: '));
  let url;
  try {url = new URL(metadata.source_url);} catch {url=null;}
  if (url?.protocol === 'https:') {
    const link = document.createElement('a'); link.href=url.href; link.target='_blank'; link.rel='noopener'; link.textContent=label; p.append(link);
  } else p.append(document.createTextNode(label));
  const license = metadata.license || metadata.source_license;
  if (license) p.append(document.createTextNode(` · ${typeof license === 'string' ? license : license.name || 'See source licensing'}`));
  if (metadata.route_release) p.append(document.createTextNode(` · Route release ${metadata.route_release}`));
  if (metadata.attribution && typeof metadata.attribution === 'string') p.append(document.createTextNode(`. ${metadata.attribution}`));
}

function renderCompletion() {
  const stage = app.byId.get(app.selected);
  if (!stage) return;
  const current = isCurrent(stage.id);
  const completed = isCompleted(stage.id);
  const experience=window.dossierCompletionEligibility;
  const eligible=Boolean(experience?.day_id===stage.id && experience.eligible===true);
  ui['completion-panel'].classList.toggle('not-current',!current);
  ui['completion-action'].hidden=!current || Boolean(app.pending);
  ui['pending-action'].hidden=!app.pending;
  ui['retry-button'].disabled=app.saving;
  ui['complete-button'].disabled=!current || !app.nonce || app.saving || !ui['complete-ack'].checked || Boolean(app.pending) || !eligible;
  ui['completion-eligibility'].hidden=!current;
  ui['completion-eligibility'].textContent=current?(eligible?'Preparation or activity, story, and reflection are saved. This virtual section is ready for deliberate completion.':experience?.day_id===stage.id?(experience.reasons || ['Checking the saved day requirements…']).join(' '):'Checking the saved day requirements…'):'';
  ui['complete-button'].textContent=app.saving?'Saving this section…':'Complete section and continue →';
  if (app.pending) {
    const pendingDay=app.byId.get(app.pending.day_id);
    ui['pending-description'].textContent=`A completion for Day ${pendingDay?.day_number || ''} is awaiting confirmation. Check that save before starting another one.`;
  }
  if (completed) {
    ui['completion-heading'].textContent='This section is complete';
    ui['completion-description'].textContent='Your saved trail record already includes this leg. Revisit its dossier as often as you like.';
  } else if (current) {
    ui['completion-heading'].textContent='Finish this virtual section';
    ui['completion-description'].textContent='When you are ready, save this section as complete to open the next leg of your expedition.';
  } else if (app.trail?.expedition_complete) {
    ui['completion-heading'].textContent='Your itinerary is complete';
    ui['completion-description'].textContent='All daily sections remain available for review.';
  } else if (app.trail) {
    const active=app.byId.get(app.trail.current_day_id);
    ui['completion-heading'].textContent='You’re previewing a future section';
    ui['completion-description'].textContent=`Your saved trail place is still Day ${active?.day_number || app.trail.next_day_number}. Return to the current section when you want to continue.`;
  } else {
    ui['completion-heading'].textContent='Reconnect to save progress';
    ui['completion-description'].textContent='The local service must be available to confirm your current section and save completion.';
  }
}

function selectDay(id, {scroll=false}={}) {
  const stage=app.byId.get(id); if(!stage)return;
  const changedDay=app.selected!==id;
  app.selected=id;
  ui['complete-ack'].checked=false;
  ui['completion-message'].textContent='';
  ui['day-eyebrow'].textContent=`DAILY DOSSIER ${dayLabel(stage.day_number)} · ${stage.region || 'THE TRAIL'}`;
  ui['day-title'].textContent=displayTitle(stage.title) || `Trail miles ${decimal(stage.mile_start)}–${decimal(stage.mile_end)}`;
  ui['day-summary'].textContent=displayCopy(stage.summary) || `Follow the mapped trail from mile ${decimal(stage.mile_start)} to mile ${decimal(stage.mile_end)} in this daily section.`;
  ui['day-state'].textContent=isCurrent(id)?'Your current section':isCompleted(id)?'Completed section':app.trail?'Future section · preview':'Map preview';
  ui['day-state'].className=`state-badge ${isCurrent(id)?'current':isCompleted(id)?'complete':''}`;
  ui['mile-start'].textContent=decimal(stage.mile_start);
  ui['mile-end'].textContent=decimal(stage.mile_end);
  ui['leg-distance'].textContent=`${decimal(stage.distance_miles)} mi`;
  renderMapPresentation(stage);
  ui['start-coordinates'].textContent=coordinates(stage.start);
  ui['end-coordinates'].textContent=coordinates(stage.end);
  ui['briefing-copy'].textContent=displayCopy(stage.summary) || 'Use this daily dossier to learn the route, orient yourself on the map, and give your training a place on the trail.';
  const points=(Array.isArray(stage.briefing)?stage.briefing:[]).filter(value=>typeof value==='string');
  ui['briefing-points'].replaceChildren(...points.map(value=>{const li=document.createElement('li');li.textContent=displayCopy(value);return li;}));
  ui['briefing-points'].hidden=!points.length;
  ui['orientation-block'].hidden=!stage.orientation_prompt;
  ui['orientation-copy'].textContent=displayCopy(stage.orientation_prompt);
  const dossier=localAsset(stage.dossier_path,'dossiers');
  ui['dossier-link'].hidden=!dossier;
  if(dossier)ui['dossier-link'].href=dossier;
  const index=app.stages.indexOf(stage);
  ui['previous-button'].disabled=index===0;
  ui['next-button'].disabled=index===app.stages.length-1;
  ui['leg-position'].textContent=`${stage.day_number} of ${app.stages.length}`;
  ui['loading-view'].hidden=true; ui['day-view'].hidden=false;
  document.title=`Day ${stage.day_number} · Trail Dossier`;
  renderCompletion(); renderDayList(); renderSource(); renderVisuals({resetPhoto:changedDay});
  window.dossierCurrentContext={stage,trail:app.trail,nonce:app.nonce};
  window.dispatchEvent(new CustomEvent('trail:day',{detail:window.dossierCurrentContext}));
  if(scroll)element('dossier').scrollIntoView({block:'start'});
}

function renderAfterState({selectCurrent=false}={}) {
  renderProgress();
  const id=selectCurrent?(app.trail?.current_day_id || app.stages[app.stages.length-1]?.id):app.selected;
  if(id)selectDay(id); else if(app.stages.length)selectDay(app.stages[0].id);
}

async function refreshState({silent=false}={}) {
  if(app.refreshing)return false;
  app.refreshing=true; ui['refresh-button'].disabled=true;
  loadTopography();
  loadSatellite();
  try {
    const data=await request('/api/bootstrap');
    applyState(data); app.nonce=data.nonce;
    renderAfterState();
    if(!silent&&!app.pending)showBanner('Your saved trail place is up to date.','success');
    return true;
  } catch(error) {
    app.nonce=null;
    renderCompletion();
    if(!silent)showBanner(`${error.message} Your last confirmed trail place is shown; saving is unavailable until reconnection.`,'error');
    return false;
  } finally {app.refreshing=false;ui['refresh-button'].disabled=false;}
}

function operationId() {
  if(crypto.randomUUID)return crypto.randomUUID();
  const bytes=new Uint8Array(16);crypto.getRandomValues(bytes);
  return Array.from(bytes,byte=>byte.toString(16).padStart(2,'0')).join('');
}

async function acceptReceipt(receipt) {
  if(!receipt?.ok || receipt.operation_id!==app.pending?.operation_id || receipt.day_id!==app.pending?.day_id) {
    throw new ServiceError('The save response did not identify the requested section.');
  }
  const day=app.byId.get(receipt.day_id);
  // A replay can contain an older committed snapshot, so always ask for current state.
  let currentState;
  try {currentState=await request('/api/state');} catch(error) {
    error.receiptConfirmed=true;
    error.savedDay=day?.day_number;
    throw error;
  }
  applyState(currentState);
  persistPending(null);
  renderAfterState({selectCurrent:true});
  showBanner(app.trail.expedition_complete?`Day ${day.day_number} is saved. You have completed the whole virtual trail.`:`Day ${day.day_number} is saved. Your next dossier is Day ${app.byId.get(app.trail.current_day_id)?.day_number || app.trail.next_day_number}.`,'success');
  ui['completion-message'].textContent=app.trail.expedition_complete?'Your expedition is complete.':'Your next section is ready. Explore it before you decide to continue.';
}

async function submitPending({lookupFirst=false}={}) {
  if(!app.pending||app.saving)return;
  app.saving=true; renderCompletion();
  ui['completion-message'].textContent='Checking the saved trail record…';
  try {
    if(lookupFirst) {
      try {
        const receipt=await request(`/api/operations/${encodeURIComponent(app.pending.operation_id)}`);
        await acceptReceipt(receipt); return;
      } catch(error) {if(error.status!==404)throw error;}
    }
    if(!app.nonce) {
      const data=await request('/api/bootstrap'); applyState(data); app.nonce=data.nonce;
    }
    const pending=app.pending;
    const body={day_id:pending.day_id,expected_revision:pending.expected_revision,operation_id:pending.operation_id};
    const receipt=await request('/api/complete',{method:'POST',headers:{'Content-Type':'application/json','X-PCT-Nonce':app.nonce},body:JSON.stringify(body)});
    await acceptReceipt(receipt);
  } catch(error) {
    if(error.receiptConfirmed) {
      showBanner(`Day ${error.savedDay || ''} was saved, but the current trail place could not be refreshed. Check this save again when the local service is available.`,'error');
      ui['completion-message'].textContent='This section’s completion is confirmed. Its current continuation is awaiting reconnection.';
    } else if(error.status===409) {
      if(error.data?.state)applyState(error.data.state);
      persistPending(null);
      renderAfterState();
      showBanner('The saved trail record changed before this completion. Your current place has been refreshed. Review it before starting another save.','error');
      ui['completion-message'].textContent=error.message;
    } else if(error.status>=400 && error.status<500 && ![401,403,408,429].includes(error.status)) {
      persistPending(null); renderCompletion();
      showBanner(`${error.message} This completion was rejected. Your trail place has not advanced through this request.`,'error');
    } else {
      if([401,403].includes(error.status))app.nonce=null;
      showBanner(`${error.message} The save is awaiting confirmation. Check and retry the same save to avoid advancing twice.`,'error');
      ui['completion-message'].textContent='No new completion will be started until this save is confirmed.';
    }
  } finally {app.saving=false;renderCompletion();}
}

async function beginCompletion() {
  if(!app.trail||!app.nonce||app.saving||app.pending||!ui['complete-ack'].checked||!isCurrent(app.selected)||window.dossierCompletionEligibility?.day_id!==app.selected||window.dossierCompletionEligibility?.eligible!==true)return;
  persistPending({campaign_id:app.trail.campaign_id,day_id:app.selected,expected_revision:app.trail.revision,operation_id:operationId()});
  await submitPending();
}

async function initialize() {
  if(location.protocol!=='http:' || location.hostname!=='127.0.0.1') {
    ui['loading-view'].querySelector('h1').textContent='Open your local trail experience';
    ui['loading-view'].querySelector('p').textContent='Run Start-Hike.cmd, then use the 127.0.0.1 address that it opens. Your saved expedition needs that local service.';
    return;
  }
  const [itineraryResult,stateResult]=await Promise.allSettled([request('/api/itinerary'),request('/api/bootstrap')]);
  if(itineraryResult.status!=='fulfilled') {
    showBanner(`${itineraryResult.reason.message} Relaunch Start-Hike.cmd to restore the local service, then reload this page.`,'error');
    ui['loading-view'].querySelector('h1').textContent='The itinerary is unavailable';
    ui['loading-view'].querySelector('p').textContent='Your saved trail place is unchanged. Reconnect to the local experience and reload.';
    return;
  }
  try {
    parseItinerary(itineraryResult.value);
    if(stateResult.status==='fulfilled') {applyState(stateResult.value);app.nonce=stateResult.value.nonce;restorePending();}
    else showBanner(`${stateResult.reason.message} You can browse the maps; saving is unavailable until reconnection.`,'error');
    renderProgress();
    const initialDay=app.trail?.current_day_id || (app.trail?.expedition_complete?app.stages[app.stages.length-1]?.id:app.stages[0]?.id);
    selectDay(initialDay);
    loadVisuals();loadTopography();loadSatellite();
    if(app.pending)await submitPending({lookupFirst:true});
  } catch(error) {
    showBanner(error.message,'error');
    ui['loading-view'].querySelector('h1').textContent='The trail record needs attention';
    ui['loading-view'].querySelector('p').textContent='No section has been advanced. Check the local application and reload the page.';
  }
}

ui['day-map'].addEventListener('error',()=>{ui['map-error'].hidden=false;});
ui['map-topographic-toggle'].addEventListener('click',()=>chooseMapStyle('topographic'));
ui['map-satellite-toggle'].addEventListener('click',()=>chooseMapStyle('satellite'));
ui['day-map'].addEventListener('load',()=>{ui['map-error'].hidden=true;});
ui['trail-photo'].addEventListener('error',()=>{ui['photo-error'].hidden=false;});
ui['trail-photo'].addEventListener('load',()=>{ui['photo-error'].hidden=true;});
ui['previous-photo'].addEventListener('click',()=>{if(app.photoIndex>0){app.photoIndex--;renderPhoto({eager:true});}});
ui['next-photo'].addEventListener('click',()=>{if(app.photoIndex<app.visualPhotos.length-1){app.photoIndex++;renderPhoto({eager:true});}});
ui['visual-point'].addEventListener('change',renderPoint);
ui['itinerary-button'].addEventListener('click',()=>setItineraryOpen(ui['trail-sidebar'].hidden));
ui['day-search'].addEventListener('input',renderDayList);
ui['current-day-button'].addEventListener('click',()=>selectDay(app.trail?.current_day_id || app.stages[app.stages.length-1]?.id,{scroll:true}));
ui['complete-ack'].addEventListener('change',renderCompletion);
ui['complete-button'].addEventListener('click',beginCompletion);
ui['retry-button'].addEventListener('click',()=>submitPending({lookupFirst:true}));
ui['refresh-button'].addEventListener('click',()=>refreshState());
ui['resume-button'].addEventListener('click',()=>selectDay(app.trail?.current_day_id || app.stages[app.stages.length-1]?.id,{scroll:true}));
ui['previous-button'].addEventListener('click',()=>{const index=app.stages.findIndex(stage=>stage.id===app.selected);if(index>0)selectDay(app.stages[index-1].id,{scroll:true});});
ui['next-button'].addEventListener('click',()=>{const index=app.stages.findIndex(stage=>stage.id===app.selected);if(index>=0&&index<app.stages.length-1)selectDay(app.stages[index+1].id,{scroll:true});});
ui['overview-button'].addEventListener('click',()=>ui['overview-dialog'].showModal());
ui['close-overview'].addEventListener('click',()=>ui['overview-dialog'].close());
ui['overview-dialog'].addEventListener('click',event=>{if(event.target===ui['overview-dialog']){const rect=ui['overview-dialog'].getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)ui['overview-dialog'].close();}});
window.addEventListener('focus',()=>{if(app.itinerary&&!app.saving)refreshState({silent:true});});
window.addEventListener('keydown',event=>{if(event.key==='Escape'&&!ui['trail-sidebar'].hidden&&!ui['overview-dialog'].open){setItineraryOpen(false);ui['itinerary-button'].focus();}});
window.addEventListener('trail:eligibility',event=>{window.dossierCompletionEligibility=event.detail;renderCompletion();});
window.dossierApi={request,refreshState};
initialize();
