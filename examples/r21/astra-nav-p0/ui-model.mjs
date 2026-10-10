/**
 * R21 ASTRA-NAV P0 — pure read-only public view model.
 * No GPS_PROVIDER, offline routing, image payload or scientific claim.
 * Satellite origins are R19-derived and never direct NEXUS RF links.
 */
const SLUG=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SHA=/^[a-f0-9]{64}$/;
const UTC=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
export const BASE_VECTOR_SOURCE=Object.freeze({
 id:"openfreemap-liberty-vector",
 kind:"VECTOR_BASEMAP",
 provider:"OpenFreeMap",
 source_origin:"https://tiles.openfreemap.org/styles/liberty",
 dataset_credit:"© OpenMapTiles · © OpenStreetMap contributors",
 provider_credit:"OpenFreeMap",
 license_note:"Provider attribution required; underlying OSM data rights remain distinct",
 native_gsd_m:null, native_resolution_class:"VECTOR_NO_PHOTO_GSD",
 image_photography:false, offline:false
});
export function validatePublicManifest(manifest) {
 if(!manifest||typeof manifest!=="object"||Array.isArray(manifest))throw Error("BAD_MANIFEST");
 if(manifest.schema_version!=="nexus-orbis-satellites/1" ||
    manifest.claim_ceiling!=="C1_DESCRIPTIVE_ONLY" ||
    manifest.nexus_link_verified!==false ||
    !Array.isArray(manifest.satellites)) throw Error("INVALID_R19_CONTRACT");
 const ids=new Set(); const norads=new Set();
 for(const s of manifest.satellites) {
  if(!s||typeof s.id!=="string"||!SLUG.test(s.id) ||
     typeof s.norad_cat_id!=="string"||!/^\d{1,9}$/.test(s.norad_cat_id) ||
     typeof s.name!=="string"||!s.name.trim() ||
     s.admission!=="ADMITTED_C1"||typeof s.identity_source_url!=="string" ||
     !s.identity_source_url.startsWith("https://") ||
     ids.has(s.id)||norads.has(s.norad_cat_id))throw Error("UNVERIFIED_SLOT_IDENTITY");
  ids.add(s.id);norads.add(s.norad_cat_id);
  if(s.position!==null) {
   const p=s.position;
   if(!p||p.data_class!=="ORBIT_PREDICTED" ||
      !s.orbital_elements || s.orbital_elements.data_class!=="ORBIT_ELEMENTS_EXTERNAL" ||
      !Number.isFinite(p.lat_deg)||Math.abs(p.lat_deg)>90||
      !Number.isFinite(p.lng_deg)||Math.abs(p.lng_deg)>180||
      !Number.isFinite(p.alt_km)||p.alt_km<0||
      !UTC.test(p.target_utc)||!SHA.test(p.source_sha256)||
      p.source_sha256!==s.orbital_elements.sha256 ||
      p.element_epoch_utc!==s.orbital_elements.epoch_utc)
    throw Error("INVALID_ORBIT_POSITION");
  }
 }
 return manifest;
}
export function visibleMarkers(manifest) {
 validatePublicManifest(manifest);
 return manifest.satellites.filter(s=>s.position!==null && s.stale!==true)
   .map(s=>({
     id:s.id,label:s.name,norad_cat_id:s.norad_cat_id,
     lng:s.position.lng_deg,lat:s.position.lat_deg,
     detail_href:'/orbis/satellites/?id='+encodeURIComponent(s.id),
     data_class:"ORBIT_PREDICTED", source_epoch_utc:s.position.element_epoch_utc,
     target_utc:s.position.target_utc
   }));
}
export function mapReadout(zoom,center) {
 if(!Number.isFinite(zoom)||!Number.isFinite(center?.lng)||!Number.isFinite(center?.lat))
   throw Error("INVALID_MAP_CAMERA");
 return {
  zoom_level:Number(zoom.toFixed(2)),
  longitude:Number(center.lng.toFixed(5)),
  latitude:Number(center.lat.toFixed(5)),
  photographic_native_gsd_m:null,
  photographic_detail_status:"NO_LICENSED_ORTHOPHOTO_ACTIVE",
  position_source:"MAP_CAMERA_ONLY_GNSS_UNVERIFIED"
 };
}
