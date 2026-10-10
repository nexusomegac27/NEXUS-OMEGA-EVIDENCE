import {BASE_VECTOR_SOURCE,validatePublicManifest,visibleMarkers,mapReadout} from './ui-model.mjs';

const $=id=>document.getElementById(id);
const error=$('error-note');
function showError(message) {
  error.hidden=false;
  error.textContent=message;
}
function setSlotStatus(s){ $('slot-status').textContent=s; }
function makeSafeLink(label,href) {
  const a=document.createElement('a');a.textContent=label;a.href=href;return a;
}
function renderSlots(manifest) {
  const list=$('slot-list');list.replaceChildren();
  const count=manifest.satellites.length;
  setSlotStatus(count===0
    ? '0 öffentlich zugelassene Satelliten · kein fiktiver Kartenmarker.'
    : count+' Satelliten öffentlich zugelassen; berechnete Positionen werden getrennt geprüft.');
  for(const sat of manifest.satellites) {
    const li=document.createElement('li');
    li.append(makeSafeLink(sat.name+' · NORAD '+sat.norad_cat_id,
      '/orbis/satellites/?id='+encodeURIComponent(sat.id)));
    const suffix=document.createElement('span');
    suffix.textContent=sat.position===null?' · Position nicht belegt':(sat.stale?' · veraltet':' · ORBIT_PREDICTED');
    li.append(suffix);list.append(li);
  }
}
async function start() {
  // Dynamic import is pinned to a specific published MapLibre release, not latest.
  const maplibregl=await import('https://cdn.jsdelivr.net/npm/maplibre-gl@6.13.0/dist/maplibre-gl.mjs');
  if(!maplibregl.supported()) throw Error('WebGL nicht verfügbar; zugängliches Quellenregister bleibt lesbar.');
  const map=new maplibregl.Map({
    container:'map',
    style:BASE_VECTOR_SOURCE.source_origin,
    center:[10.0037,53.5511],zoom:7,
    attributionControl:false,
    maxZoom:22,
    dragRotate:false,
    pitchWithRotate:false
  });
  map.addControl(new maplibregl.NavigationControl({visualizePitch:false}), 'top-right');
  map.addControl(new maplibregl.ScaleControl({maxWidth:120,unit:'metric'}),'bottom-left');
  map.addControl(new maplibregl.AttributionControl({compact:false}),'bottom-right');
  map.keyboard.enable();
  function updateCamera() {
    const view=mapReadout(map.getZoom(),map.getCenter());
    $('camera-info').textContent='Karte (kein GPS-Fix) · Breite '+view.latitude+'° · Länge '+view.longitude+'° · Zoom '+view.zoom_level;
    $('zoom-truth').textContent='VEKTOR-KARTE · keine fotografische GSD · Zoom zeigt nicht automatisch mehr Originaldetails';
  }
  map.on('moveend',updateCamera);
  map.on('load', updateCamera);
  map.on('error', event=>{
    // Do not automatically claim a successful map render after a network failure.
    if(event?.error) showError('Kartenquelle teilweise nicht erreichbar; keine neuen Pixel oder Messungen behauptet.');
  });
  try {
    const response=await fetch('/orbis/satellites/satellites.json',{
      headers:{Accept:'application/json'},cache:'no-store',credentials:'omit'
    });
    if(!response.ok) throw Error('HTTP '+response.status);
    const manifest=validatePublicManifest(await response.json());
    renderSlots(manifest);
    const markers=visibleMarkers(manifest);
    for(const sat of markers) {
      const element=document.createElement('button');
      element.type='button';element.className='orbital-marker';
      element.textContent='◈';element.title='Berechnete Bahnposition: '+sat.label;
      element.setAttribute('aria-label',sat.label+' — ORBIT_PREDICTED');
      element.style.cssText='border-radius:50%;background:#f1da9b;color:#12203a;border:2px solid #192a48;font-size:18px;cursor:pointer;width:34px;height:34px';
      element.addEventListener('click',()=>{window.location.assign(sat.detail_href)});
      new maplibregl.Marker({element}).setLngLat([sat.lng,sat.lat]).addTo(map);
    }
  }catch(e) {
    setSlotStatus('Satelliten-Manifest nicht unabhängig lesbar oder ungültig. Keine Marker veröffentlicht.');
    showError('R19-Datenquelle aktuell nicht verwendbar. Die Vektorkarte bleibt unabhängig von R19 abrufbar.');
  }
}
start().catch(()=>{
 setSlotStatus('Satellitenregister nicht geladen.');
 showError('Kartenengine konnte nicht gestartet werden. Prüfung von CSP, CDN und WebGL erforderlich; keine Online- oder Offline-Funktion behauptet.');
});
