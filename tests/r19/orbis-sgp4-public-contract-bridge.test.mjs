import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { adaptSgp4ToR19PublicPosition as adapt,
  safeAdaptSgp4ToR19PublicPosition as safe } from '../../examples/r19/orbis-sgp4-public-contract-bridge.mjs';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const omm = (id = 25544) => ({NORAD_CAT_ID:id,EPOCH:'2026-10-10T00:00:00Z',MEAN_MOTION:15.5});
function fixture(original = omm()) {
  const bytes = Buffer.from(JSON.stringify(original));
  const digest = sha(bytes);
  const rec = Array.isArray(original) ? original[0] : original;
  return {
    source:bytes,
    producer:{ok:true,claim_ceiling:'C1_DESCRIPTIVE_ONLY',nexus_link_verified:false,
      norad_cat_id:String(rec.NORAD_CAT_ID),source_sha256:digest,epoch_utc:rec.EPOCH,
      position:{data_class:'ORBIT_PREDICTED',model:'SGP4',lat_deg:12,lng_deg:168,
        height_km:416,epoch_utc:rec.EPOCH,target_utc:'2026-10-10T00:15:00Z',
        source_url:'https://example.org/omm',eci_km:{x:1,y:2,z:3},source_sha256:digest}},
    context:{expectedNoradCatId:'25544',originalOmmBytes:bytes,
      calculatedUtc:'2026-10-10T00:14:00Z',modelVersion:'7.1.0'}
  };
}
test('valid source-exact OMM→SGP4 result projects ONLY schema-required keys',()=>{
  const f=fixture();const out=adapt(f.producer,f.context);
  assert.deepEqual(Object.keys(out).sort(),[
    'data_class','lat_deg','lng_deg','alt_km','element_epoch_utc',
    'target_utc','calculated_utc','model','source_sha256','model_version'].sort());
  assert.equal(out.alt_km,416);assert.equal(out.source_sha256,sha(f.source));
  assert.equal(out.calculated_utc,'2026-10-10T00:14:00Z');
  assert.equal(Object.hasOwn(out,'eci_km'),false);
});
test('source must be original bytes, not parsed object / JSON reconstruction',()=>{
 const f=fixture();f.context.originalOmmBytes=omm();
 assert.match(safe(f.producer,f.context).reason,/ORIGINAL_SOURCE_BYTES_REQUIRED/);
});
test('HTTP 200 multi-object OMM array cannot silently choose first',()=>{
 const f=fixture([omm(25544),omm(39421)]);
 assert.match(safe(f.producer,f.context).reason,/OMM_ARRAY_AMBIGUOUS/);
});
test('single-record OMM array remains source-exact and identity-checked',()=>{
 const f=fixture([omm()]);assert.equal(adapt(f.producer,f.context).source_sha256,sha(f.source));
});
test('independently expected NORAD identity cannot differ from the element record',()=>{
 const f=fixture();f.context.expectedNoradCatId='39421';
 assert.match(safe(f.producer,f.context).reason,/OMM_NORAD_IDENTITY_MISMATCH/);
});
test('producer-selected NORAD must match original OMM record',()=>{
 const f=fixture();f.producer.norad_cat_id='39421';
 assert.match(safe(f.producer,f.context).reason,/PRODUCER_NORAD_IDENTITY_MISMATCH/);
});
test('digest mismatch on response body or computed position fails closed',()=>{
 const f=fixture();f.producer.position.source_sha256='b'.repeat(64);
 assert.match(safe(f.producer,f.context).reason,/PRODUCER_SOURCE_DIGEST_MISMATCH/);
});
test('re-serialized source bytes mismatch producer digest (spaces matter)',()=>{
 const f=fixture();f.context.originalOmmBytes=Buffer.from(JSON.stringify(omm(),null,2));
 assert.match(safe(f.producer,f.context).reason,/PRODUCER_SOURCE_DIGEST_MISMATCH/);
});
test('timezone-naive OMM epoch does not silently become UTC',()=>{
 const f=fixture( {...omm(),EPOCH:'2026-10-10T00:00:00'} );
 assert.match(safe(f.producer,f.context).reason,/ELEMENT_UTC_FORMAT/);
});
test('invalid calculated UTC is rejected; target UTC and calculation time distinct',()=>{
 const f=fixture();f.context.calculatedUtc='2026-10-10T14:00:00+02:00';
 assert.match(safe(f.producer,f.context).reason,/CALCULATED_UTC_FORMAT/);
});
test('no propagation further than default 48-hour model freshness bound',()=>{
 const f=fixture();f.producer.position.target_utc='2026-10-13T00:00:00Z';
 assert.match(safe(f.producer,f.context).reason,/ORBIT_ELEMENTS_STALE_FOR_TARGET/);
});
test('invalid geodetic values are not converted to map markers',()=>{
 const f=fixture();f.producer.position.lat_deg=91;
 assert.match(safe(f.producer,f.context).reason,/INVALID_GEODETIC/);
});
test('missing explicit pinned satellite.js version fails closed',()=>{
 const f=fixture();f.context.modelVersion='^7.1.0';
 assert.match(safe(f.producer,f.context).reason,/PINNED_SGP4_MODEL_VERSION/);
});
test('unknown/inconsistent NEXUS-link or claim class is rejected',()=>{
 const f=fixture();f.producer.nexus_link_verified=true;
 assert.match(safe(f.producer,f.context).reason,/PRODUCER_STATE/);
});
test('source OMM NORAD 6 digits supported, identity represented as string',()=>{
 const f=fixture(omm(123456));f.context.expectedNoradCatId='123456';
 assert.equal(adapt(f.producer,f.context).data_class,'ORBIT_PREDICTED');
});
test('no source body or missing position returns null, not invented lat/lng',()=>{
 const f=fixture();f.context.originalOmmBytes=null;
 assert.equal(safe(f.producer,f.context).position,null);
 const g=fixture();g.producer.position=null;
 assert.equal(safe(g.producer,g.context).ok,false);
});
