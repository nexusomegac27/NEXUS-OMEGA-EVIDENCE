import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  validatePublicManifest, detailHref, selectPlottableSatellites, selectDetail,
  fetchPublicManifest, MANIFEST_PATH
} from '../../examples/r19/orbis-satellite-directory.mjs';

const base = {
  schema_version: 'nexus-orbis-satellites/1',
  generated_utc: '2026-10-10T00:00:00Z',
  slot_ledger_revision: 'SYNTHETIC_TEST_ONLY',
  claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
  nexus_link_verified: false,
  satellites: []
};
const source = 'a'.repeat(64);
const sample = () => ({
  id: 'synthetic-sat', name: '<b>TEST ONLY</b>',
  norad_cat_id: '123456', admission: 'ADMITTED_C1',
  identity_source_url: 'https://example.org/test-source',
  orbital_elements: null, position: null, observations: [],
  stale: false
});
const clone = x => structuredClone(x);
const withSat = () => ({ ...clone(base), satellites: [sample()] });
function fails(x, phrase) {
  assert.throws(() => validatePublicManifest(x), new RegExp(phrase));
}
test('JSON Schema parses and matches namespace', () => {
  const schema = JSON.parse(readFileSync(new URL('../../schema/r19/orbis-satellites-manifest.schema.json', import.meta.url), 'utf8'));
  assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
  assert.deepEqual(schema.properties.schema_version.const, base.schema_version);
  assert.ok(schema.properties.satellites.items.required.includes('identity_source_url'));
});
test('empty official-looking public snapshot is valid, but yields no invented markers', () => {
  assert.equal(validatePublicManifest(clone(base)).satellites.length, 0);
  assert.equal(selectPlottableSatellites(clone(base)).length, 0);
});
test('unpositioned satellite stays indexable and produces no map marker', () => {
  const x = withSat();
  assert.equal(validatePublicManifest(x).satellites.length, 1);
  assert.deepEqual(selectPlottableSatellites(x), []);
  assert.equal(selectDetail(x, '?id=synthetic-sat')?.norad_cat_id, '123456');
});
test('detail path is only controlled internal query, no external open redirects', () => {
  assert.equal(detailHref('synthetic-sat'), '/orbis/satellites/?id=synthetic-sat');
  assert.throws(() => detailHref('https://evil.test/#abc'));
  assert.throws(() => detailHref('../orbis'));
  assert.equal(selectDetail(withSat(), '?id=absent'), null);
});
test('duplicate slug fails closed', () => {
  const x = withSat(); const y = sample(); y.norad_cat_id = '987654'; x.satellites.push(y);
  fails(x, 'duplicate_slot');
});
test('duplicate NORAD ID fails closed independently of slug', () => {
  const x = withSat(); const y = sample(); y.id = 'other-slug'; x.satellites.push(y);
  fails(x, 'duplicate_slot');
});
test('9 digit NORAD IDs supported and non-string IDs rejected', () => {
  const x = withSat(); x.satellites[0].norad_cat_id = '123456789';
  assert.equal(validatePublicManifest(x).satellites[0].norad_cat_id.length, 9);
  x.satellites[0].norad_cat_id = 123456789;
  fails(x, 'norad_string');
});
test('malicious satellite slug rejected', () => {
  const x = withSat(); x.satellites[0].id = 'test?next=https://evil.test';
  fails(x, 'satellite_slug');
});
test('source identity URL required before listing', () => {
  const x = withSat(); x.satellites[0].identity_source_url = 'javascript:alert(1)';
  fails(x, 'identity_source');
});
test('public manifest cannot advertise verified NEXUS link or promoted claims', () => {
  const x = withSat(); x.nexus_link_verified = true; fails(x, 'no_nexus_link_claim');
  x.nexus_link_verified = false; x.claim_ceiling = 'C3_PROVEN'; fails(x, 'ceiling');
});
test('synthetic position without actual element digest rejected', () => {
  const x = withSat(); x.satellites[0].position = {
    data_class: 'ORBIT_PREDICTED', lat_deg: 52.5, lng_deg: 13.4, alt_km: 500,
    element_epoch_utc: '2026-10-10T00:00:00Z',
    target_utc: '2026-10-10T00:00:00Z', calculated_utc: '2026-10-10T00:00:00Z',
    model: 'TEST SGP4', source_sha256: source
  };
  fails(x, 'predicted_position');
});
test('source-bound predicted position selected, stale position withheld', () => {
  const x = withSat();
  x.satellites[0].orbital_elements = {
    data_class: 'ORBIT_ELEMENTS_EXTERNAL', format: 'OMM_JSON',
    source_url: 'https://example.org/omm', epoch_utc: '2026-10-10T00:00:00Z',
    fetched_utc: '2026-10-10T00:01:00Z', sha256: source
  };
  x.satellites[0].position = {
    data_class: 'ORBIT_PREDICTED', lat_deg: 52.5, lng_deg: 13.4, alt_km: 500,
    element_epoch_utc: '2026-10-10T00:00:00Z',
    target_utc: '2026-10-10T00:03:00Z', calculated_utc: '2026-10-10T00:03:01Z',
    model: 'SYNTHETIC_TEST_ONLY', source_sha256: source
  };
  assert.equal(selectPlottableSatellites(x).length, 1);
  x.satellites[0].stale = true;
  assert.equal(selectPlottableSatellites(x).length, 0);
  x.satellites[0].stale = false;
  x.satellites[0].position.source_sha256 = 'b'.repeat(64);
  fails(x, 'predicted_position');
});
test('cross-satellite instrument observation must fail', () => {
  const x = withSat();
  x.satellites[0].observations.push({
    data_class: 'LIVE_MEASURED_EXTERNAL', source_provider: 'SYNTHETIC',
    source_url: 'https://example.org/instrument', source_norad_cat_id: '888888',
    instrument_id: 'TEST', metric: 'flux', value: 1,
    unit: 'TEST_UNIT', quality_flag: 'SOURCE_QUALITY_CODE',
    observed_utc: '2026-10-10T00:00:00Z', fetched_utc: '2026-10-10T00:02:00Z'
  });
  fails(x, 'instrument_source_mismatch');
  x.satellites[0].observations[0].source_norad_cat_id = '123456';
  assert.equal(validatePublicManifest(x).satellites[0].observations.length, 1);
});
test('browser may only fetch the same-origin manifest, never CelesTrak per visitor', async () => {
  const fakeFetch = async (path, options) => {
    assert.equal(path, MANIFEST_PATH);
    assert.equal(options.cache, 'no-store');
    return { ok: true, json: async () => withSat() };
  };
  assert.equal((await fetchPublicManifest(fakeFetch)).satellites.length, 1);
  await assert.rejects(fetchPublicManifest(fakeFetch, 'https://celestrak.org/evil'), /same_origin_only/);
  await assert.rejects(fetchPublicManifest(async () => ({ ok: false })), /http_fetch_failed/);
});
