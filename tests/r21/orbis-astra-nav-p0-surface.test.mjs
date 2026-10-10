import test from 'node:test';
import assert from 'node:assert/strict';
import {BASE_VECTOR_SOURCE,validatePublicManifest,visibleMarkers,mapReadout} from '../../examples/r21/astra-nav-p0/ui-model.mjs';
const manifest=()=>({schema_version:'nexus-orbis-satellites/1',claim_ceiling:'C1_DESCRIPTIVE_ONLY',nexus_link_verified:false,generated_utc:'2026-10-10T00:00:00Z',slot_ledger_revision:'test-only',satellites:[]});
const sat=(extra={})=>({id:'synthetic-sat',name:'Synthetic satellite — TEST ONLY',norad_cat_id:'123456',admission:'ADMITTED_C1',identity_source_url:'https://example.org/identity',orbital_elements:null,position:null,observations:[],stale:false,...extra});
const e=(a,b)=>assert.throws(()=>validatePublicManifest(a),b);
test('vector source shows OpenFreeMap and OpenStreetMap, not a photo/GNSS claim',()=>{
 assert.equal(BASE_VECTOR_SOURCE.image_photography,false);assert.equal(BASE_VECTOR_SOURCE.offline,false);
 assert.match(BASE_VECTOR_SOURCE.dataset_credit,/OpenStreetMap/);assert.equal(BASE_VECTOR_SOURCE.native_gsd_m,null);
});
test('empty register creates no markers without pretending a satellite is visible',()=>{
 assert.deepEqual(visibleMarkers(manifest()),[]);
});
test('unpositioned admitted satellite is valid but not plottable',()=>{
 const m=manifest();m.satellites=[sat()];assert.equal(validatePublicManifest(m).satellites.length,1);
 assert.equal(visibleMarkers(m).length,0);
});
test('promoted claim or true NEXUS link rejected',()=>{
 const m=manifest();m.nexus_link_verified=1;e(m,/INVALID_R19_CONTRACT/);
 m.nexus_link_verified=false;m.claim_ceiling='C3';e(m,/INVALID_R19_CONTRACT/);
});
test('old numeric zero NEXUS link rejected (R19 schema repair regression)',()=>{
 const m=manifest();m.nexus_link_verified=0;e(m,/INVALID_R19_CONTRACT/);
});
test('wrong schema family or missing array rejected',()=>{
 const m=manifest();m.schema_version='legacy';e(m,/INVALID_R19_CONTRACT/);
 m.schema_version='nexus-orbis-satellites/1';m.satellites=null;e(m,/INVALID_R19_CONTRACT/);
});
test('duplicate NORAD/satellite identities rejected',()=>{
 const m=manifest();m.satellites=[sat(),sat({id:'other'})];e(m,/UNVERIFIED_SLOT_IDENTITY/);
});
test('unsafe route id rejected',()=>{
 const m=manifest();m.satellites=[sat({id:'../escape'})];e(m,/UNVERIFIED_SLOT_IDENTITY/);
});
test('position absent epoch/hash source rejected',()=>{
 const m=manifest();m.satellites=[sat({position:{data_class:'ORBIT_PREDICTED',lat_deg:53,lng_deg:10,alt_km:400,target_utc:'2026-10-10T00:00:00Z',source_sha256:'a'.repeat(64)}})];
 e(m,/INVALID_ORBIT_POSITION/);
});
test('valid synthetic model position gets safe encoded route; stale positions stay hidden',()=>{
 const sha='a'.repeat(64);
 const source={data_class:'ORBIT_ELEMENTS_EXTERNAL',format:'OMM_JSON',source_url:'https://example.org/orbit',epoch_utc:'2026-10-10T00:00:00Z',fetched_utc:'2026-10-10T00:01:00Z',sha256:sha};
 const position={data_class:'ORBIT_PREDICTED',lat_deg:53,lng_deg:10,alt_km:400,
  target_utc:'2026-10-10T00:01:00Z',calculated_utc:'2026-10-10T00:01:02Z',model:'SGP4_SYNTHETIC_FIXTURE_ONLY',element_epoch_utc:source.epoch_utc,source_sha256:sha};
 const m=manifest();m.satellites=[sat({orbital_elements:source,position})];
 const marks=visibleMarkers(m);assert.equal(marks.length,1);
 assert.equal(marks[0].detail_href,'/orbis/satellites/?id=synthetic-sat');
 m.satellites[0].stale=true;assert.equal(visibleMarkers(m).length,0);
});
test('wrong orbital hash rejected for model position',()=>{
 const m=manifest();m.satellites=[sat({orbital_elements:{data_class:'ORBIT_ELEMENTS_EXTERNAL',epoch_utc:'2026-10-10T00:00:00Z',sha256:'a'.repeat(64)},
 position:{data_class:'ORBIT_PREDICTED',lat_deg:53,lng_deg:10,alt_km:400,target_utc:'2026-10-10T00:01:00Z',element_epoch_utc:'2026-10-10T00:00:00Z',source_sha256:'b'.repeat(64)}})];
 e(m,/INVALID_ORBIT_POSITION/);
});
test('pure visual camera never becomes actual GNSS fix or photographic detail',()=>{
 const r=mapReadout(7,{lng:10.0037,lat:53.5511});
 assert.equal(r.position_source,'MAP_CAMERA_ONLY_GNSS_UNVERIFIED');
 assert.equal(r.photographic_native_gsd_m,null);
 assert.throws(()=>mapReadout(NaN,{lng:10,lat:53}),/INVALID_MAP_CAMERA/);
});
test('model position requires calculation time and model identity',()=>{
 const sha='a'.repeat(64);
 const orbit={data_class:'ORBIT_ELEMENTS_EXTERNAL',epoch_utc:'2026-10-10T00:00:00Z',fetched_utc:'2026-10-10T00:00:10Z',sha256:sha};
 const position={data_class:'ORBIT_PREDICTED',lat_deg:53,lng_deg:10,alt_km:400,
 target_utc:'2026-10-10T00:01:00Z',element_epoch_utc:orbit.epoch_utc,source_sha256:sha};
 const m=manifest();m.satellites=[sat({orbital_elements:orbit,position})];
 e(m,/INVALID_ORBIT_POSITION/);
 m.satellites[0].position.model='SGP4_SYNTHETIC_TEST';
 m.satellites[0].position.calculated_utc='2026-10-10T00:01:01Z';
 assert.equal(visibleMarkers(m).length,1);
});
test('cross-satellite measurement identity fails before map even if coordinate exists',()=>{
 const m=manifest();m.satellites=[sat({observations:[{
  data_class:'LIVE_MEASURED_EXTERNAL',source_norad_cat_id:'999999',instrument_id:'TEST',
  value:1,observed_utc:'2026-10-10T00:00:00Z',fetched_utc:'2026-10-10T00:00:01Z'
 }]})];
 e(m,/CROSS_SATELLITE/);
});
test('root contract rejects extra unversioned fields',()=>{
 const m=manifest();m.claim_promotion=false;e(m,/INVALID_R19_CONTRACT/);
});
