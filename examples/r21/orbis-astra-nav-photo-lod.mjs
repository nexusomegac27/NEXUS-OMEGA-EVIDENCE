/**
 * NEXUS OMEGA · R21 ASTRA-NAV · deterministic, source-first photographic LOD.
 * Standalone REFERENCE, NOT bound to nexus-mobile.de production.
 * This module renders no image, and never invents satellite positioning.
 */
const SHA = /^[a-f0-9]{64}$/;
const TYPES = new Set(['SATELLITE_IMAGERY','AERIAL_ORTHOPHOTO','DEM_RASTER','VECTOR_BASEMAP','PHOTOGRAMMETRY_TEXTURE']);
function finite(x){return typeof x === 'number' && Number.isFinite(x);}
function lon(x){return finite(x) && x>=-180 && x<=180;}
function lat(x){return finite(x) && x>=-90 && x<=90;}
export function validateAsset(a) {
  if(!a || typeof a!=='object' || Array.isArray(a)) throw new Error('BAD_ASSET');
  if(typeof a.id!=='string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(a.id)) throw new Error('BAD_ID');
  if(!TYPES.has(a.kind)) throw new Error('BAD_KIND');
  if(!finite(a.native_gsd_m) || a.native_gsd_m<=0) throw new Error('BAD_GSD');
  if(!Array.isArray(a.bounds_wsen) || a.bounds_wsen.length!==4 ||
     !lon(a.bounds_wsen[0]) || !lat(a.bounds_wsen[1]) ||
     !lon(a.bounds_wsen[2]) || !lat(a.bounds_wsen[3]) ||
     a.bounds_wsen[1]>=a.bounds_wsen[3]) throw new Error('BAD_BOUNDS');
  if(typeof a.source_url!=='string' || !a.source_url.startsWith('https://')) throw new Error('BAD_ORIGIN');
  if(typeof a.source_name!=='string' || !a.source_name.trim()) throw new Error('BAD_ORIGIN');
  if(typeof a.license_id!=='string' || !a.license_id.trim() ||
     typeof a.required_attribution!=='string' || !a.required_attribution.trim()) throw new Error('BAD_LICENSE_OR_CREDIT');
  if(typeof a.acquired_utc!=='string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(a.acquired_utc) ||
     !Number.isFinite(Date.parse(a.acquired_utc))) throw new Error('BAD_CAPTURE_DATE');
  if(typeof a.asset_sha256!=='string' || !SHA.test(a.asset_sha256)) throw new Error('BAD_ASSET_DIGEST');
  if(!['APPROVED_FOR_THIS_USE','PENDING_REVIEW','DENIED'].includes(a.rights_status)) throw new Error('BAD_RIGHTS_STATE');
  if(typeof a.offline_available!=='boolean') throw new Error('BAD_OFFLINE');
  return a;
}
export function inside(bounds, longitude, latitude) {
  const [west,south,east,north]=bounds;
  return latitude>=south && latitude<=north &&
    (west<=east ? longitude>=west && longitude<=east :
      longitude>=west || longitude<=east);
}
/**
 * Choose a valid photographic/raster source whose native resolution meets the
 * requested CSS-pixel scale. If not possible, return honest upscale state.
 * No inference about geographic observation quality from screen zoom.
 */
export function selectPhotoLayer(assets, {
  longitude,latitude,requested_mpp,offline=false
}) {
  if(!lon(longitude) || !lat(latitude) || !finite(requested_mpp) || requested_mpp<=0 ||
     typeof offline!=='boolean') throw new Error('BAD_VIEW');
  if(!Array.isArray(assets)) throw new Error('BAD_CATALOG');
  const eligible = [];
  const ids = new Set();
  for(const a of assets) {
    validateAsset(a);
    if(ids.has(a.id)) throw new Error('DUPLICATE_ASSET_ID');
    ids.add(a.id);
    if(!['SATELLITE_IMAGERY','AERIAL_ORTHOPHOTO'].includes(a.kind) ||
       a.rights_status!=='APPROVED_FOR_THIS_USE' ||
       (offline && !a.offline_available) ||
       !inside(a.bounds_wsen,longitude,latitude)) continue;
    eligible.push(a);
  }
  if(!eligible.length) return {
    state:'COVERAGE_GAP',asset_id:null,requested_mpp,
    source_gsd_m:null,readback_source_url:null,attribution:null
  };
  // Coarsest image resolution that still supports requested ground scale;
  // if all are coarser, use the finest but expose digital magnification.
  const adequate=eligible.filter(a=>a.native_gsd_m<=requested_mpp);
  const selected = adequate.length ?
    adequate.sort((a,b)=>b.native_gsd_m-a.native_gsd_m || a.id.localeCompare(b.id))[0] :
    eligible.sort((a,b)=>a.native_gsd_m-b.native_gsd_m || a.id.localeCompare(b.id))[0];
  const upscale = selected.native_gsd_m>requested_mpp;
  return {
    state: upscale?'NATIVE_DETAIL_EXCEEDED':'NATIVE_RESOLUTION_SUPPORTED',
    asset_id:selected.id,
    requested_mpp,
    source_gsd_m:selected.native_gsd_m,
    scale_excess_ratio: upscale?selected.native_gsd_m/requested_mpp:1,
    source_url:selected.source_url,
    asset_sha256:selected.asset_sha256,
    acquired_utc:selected.acquired_utc,
    license_id:selected.license_id,
    attribution:selected.required_attribution,
    label:upscale?'Keine zusätzlichen Bilddetails verfügbar':'Quellenauflösung ausreichend'
  };
}
/** WebMercator approximate ground scale at latitude: CSS px at 256 tile base */
export function mapMetersPerCssPixel(latitude, zoom) {
  if(!lat(latitude) || !finite(zoom) || zoom<0 || zoom>28) throw new Error('BAD_MAP_SCALE');
  return 156543.03392 * Math.cos(latitude*Math.PI/180) / (2**zoom);
}
