import test from 'node:test';
import assert from 'node:assert/strict';
import {selectPhotoLayer, validateAsset, inside, mapMetersPerCssPixel} from '../../examples/r21/orbis-astra-nav-photo-lod.mjs';
const a = (id, gsd, extra={}) => ({
  id,kind:'AERIAL_ORTHOPHOTO',native_gsd_m:gsd,
  bounds_wsen:[9.6,53.3,10.5,53.9],
  source_url:'https://example.org/licensed-test-only',
  source_name:'SYNTHETIC_FIXTURE_DO_NOT_DEPLOY',
  license_id:'SYNTHETIC_TEST_ONLY',
  required_attribution:'SYNTHETIC_FIXTURE',
  acquired_utc:'2026-10-01T00:00:00Z',asset_sha256:'a'.repeat(64),
  rights_status:'APPROVED_FOR_THIS_USE',offline_available:true,...extra
});
const view=(mpp=0.21, extra={})=>({longitude:10,latitude:53.55,requested_mpp:mpp,offline:false,...extra});
test('source-first resolution uses coarsest adequate imagery (not every fine tile)',()=>{
 const r=selectPhotoLayer([a('regional',10),a('orthophoto',0.2),a('veryfine',0.05)],view(0.22));
 assert.equal(r.asset_id,'orthophoto');assert.equal(r.state,'NATIVE_RESOLUTION_SUPPORTED');
});
test('beyond native pixel resolution remains explicitly marked magnified',()=>{
 const r=selectPhotoLayer([a('orthophoto',0.2)],view(0.02));
 assert.equal(r.state,'NATIVE_DETAIL_EXCEEDED');
 assert.ok(r.scale_excess_ratio>1);assert.match(r.label,/Keine zusätzlichen/);
});
test('zoom may not upgrade an unlicensed supposedly sharper image',()=>{
 const r=selectPhotoLayer([a('licensed',1),a('unlicensed',0.02,{rights_status:'PENDING_REVIEW'})],view(0.05));
 assert.equal(r.asset_id,'licensed'); assert.equal(r.state,'NATIVE_DETAIL_EXCEEDED');
});
test('offline requires available local pack, not website or GNSS network fiction',()=>{
 const r=selectPhotoLayer([a('online',0.2,{offline_available:false})],view(0.5,{offline:true}));
 assert.equal(r.state,'COVERAGE_GAP');
});
test('no licensed coverage means gap, never extrapolation',()=>{
 const r=selectPhotoLayer([a('here',0.2)],{...view(1),longitude:50,latitude:1});
 assert.equal(r.state,'COVERAGE_GAP'); assert.equal(r.asset_id,null);
});
test('DOP20 20cm is source limited around zoom 19 in Hamburg',()=>{
 const mpp=mapMetersPerCssPixel(53.55,19);
 assert.ok(mpp>0.17&&mpp<0.19);
 const r=selectPhotoLayer([a('dop20',0.2)],view(mpp));
 assert.equal(r.state,'NATIVE_DETAIL_EXCEEDED');
});
test('north-south bounds fail closed',()=>assert.throws(()=>validateAsset(a('bad',0.2,{bounds_wsen:[10,54,11,53]})),/BAD_BOUNDS/));
test('antimeridian coverage is correct',()=>{
 assert.equal(inside([170,-20,-170,20],175,0),true);
 assert.equal(inside([170,-20,-170,20],-175,0),true);
 assert.equal(inside([170,-20,-170,20],0,0),false);
});
test('duplicate asset IDs rejected',()=>assert.throws(()=>selectPhotoLayer([a('dup',1),a('dup',0.1)],view()),/DUPLICATE/));
test('invalid rights code rejected',()=>assert.throws(()=>validateAsset(a('invalid',1,{rights_status:'AUTO_APPROVED'})),/BAD_RIGHTS/));
test('missing attribution rejected',()=>assert.throws(()=>validateAsset(a('no-credit',1,{required_attribution:''})),/BAD_LICENSE/));
test('bad digest rejected',()=>assert.throws(()=>validateAsset(a('bad-hash',1,{asset_sha256:'0'})),/BAD_ASSET_DIGEST/));
test('bad source URL rejected',()=>assert.throws(()=>validateAsset(a('insecure',1,{source_url:'javascript:alert(1)'})),/BAD_ORIGIN/));
test('missing observation acquisition timestamp rejected',()=>assert.throws(()=>validateAsset(a('no-date',1,{acquired_utc:'UNKNOWN'})),/BAD_CAPTURE_DATE/));
test('bad zoom or bad meters per pixel rejected',()=>{
 assert.throws(()=>mapMetersPerCssPixel(53,99),/BAD_MAP_SCALE/);
 assert.throws(()=>selectPhotoLayer([a('ok',1)],view(0)),/BAD_VIEW/);
});
test('low-res global imagery avoids unnecessarily loading 20cm ortho at wide zoom',()=>{
 const r=selectPhotoLayer([a('global',10),a('ortho',0.2)],view(500));
 assert.equal(r.asset_id,'global');
});
