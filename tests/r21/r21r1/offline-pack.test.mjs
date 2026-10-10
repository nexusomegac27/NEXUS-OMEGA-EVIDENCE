import test from 'node:test';
import assert from 'node:assert/strict';
import { validateOfflinePack, routeAvailability, OFFLINE_PACK_SCHEMA_VERSION } from '../../examples/r21/r21r1/offline-pack.mjs';

const EVAL = '2026-10-10T12:00:00Z';
const REQUEST_POINT = [10.0037, 53.5511];
const ATOM_REF = { asset_id: 'osm-germany-extract-2026-10', atom_sha256: 'b'.repeat(64) };

const DOP20_ATOM = {
  asset_id: 'hamburg-dop20-2018-tiles',
  upstream_contributors: ['Freie und Hansestadt Hamburg, LGV'],
  source_url: 'https://geoportal.hamburg.de/',
  license_id: 'DL-DE-BY-2.0',
  native_gsd_m: 0.2,
  acquired_utc: '2018-04-30T11:22:00Z',
  asset_sha256: 'c'.repeat(64),
  rights_status: 'APPROVED_FOR_THIS_USE',
  attribution: { first_class: true, visible_label: '(c) Freie und Hansestadt Hamburg, LGV', expiry_check_required: true },
  nexus_transformation: 'keine (synthetische Test-Fixture, kein Produktivbeschluss)',
  symbiose_links: [],
  is_living_artifact: true
};

function pack(extra = {}) {
  return {
    schema_version: OFFLINE_PACK_SCHEMA_VERSION,
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    pack_id: 'hamburg-routing-graph-pilot',
    pack_kind: 'ROUTING_GRAPH',
    pack_revision: '2026.10.10-r0',
    region: { name: 'Hamburg Pilot', bbox_wsen: [9.6, 53.3, 10.5, 53.9] },
    produced_utc: '2026-10-10T00:00:00Z',
    producer: 'SYNTHETIC_TEST_ONLY_PRODUCER',
    data_license_id: 'ODbL-1.0',
    archives: [
      { role: 'routing_graph', file_name: 'hamburg-graph.brp', sha256: 'a'.repeat(64), bytes: 1234 },
      { role: 'attribution_manifest', file_name: 'attribution.json', sha256: 'e'.repeat(64), bytes: 210 }
    ],
    min_client_version: '0.1.0',
    routing: { engine: 'brouter', engine_version: '1.8.1', profile: 'car-fast' },
    provenance_atom_ref: ATOM_REF,
    update_policy: { rollback_supported: true },
    ...extra
  };
}

const vectorPack = pack({
  pack_id: 'hamburg-vector-pilot',
  pack_kind: 'VECTOR_MAP',
  routing: undefined,
  archives: [
    { role: 'map_tiles', file_name: 'hamburg-vector.pmtiles', sha256: 'f'.repeat(64), bytes: 4567 },
    { role: 'attribution_manifest', file_name: 'attribution.json', sha256: 'e'.repeat(64), bytes: 210 }
  ]
});

const request = (extra = {}) => ({ evaluation_utc: EVAL, point: REQUEST_POINT, ...extra });

test('a complete routing pack with provenance atom reference validates', () => {
  assert.equal(validateOfflinePack(pack()).pack_kind, 'ROUTING_GRAPH');
});

test('no pack means no routing claim (NO_PACK_NO_ROUTE)', () => {
  assert.equal(routeAvailability(null, request()), 'NO_PACK_NO_ROUTE');
  assert.equal(routeAvailability(undefined, request()), 'NO_PACK_NO_ROUTE');
});

test('a request outside the pack bbox is out of coverage', () => {
  assert.equal(routeAvailability(pack(), request({ point: [13.4, 52.5] })), 'OUT_OF_COVERAGE');
});

test('an expired pack is not routeable', () => {
  const expired = pack({ valid_until_utc: '2026-10-09T23:59:59Z' });
  assert.equal(routeAvailability(expired, request()), 'PACK_EXPIRED');
});

test('a non-routing pack never claims routing', () => {
  validateOfflinePack(vectorPack);
  assert.equal(routeAvailability(vectorPack, request()), 'NO_ROUTING_GRAPH_IN_PACK');
});

test('routing blocks in non-routing packs are rejected', () => {
  assert.throws(
    () => validateOfflinePack({ ...vectorPack, routing: { engine: 'brouter', engine_version: '1.8.1', profile: 'car-fast' } }),
    /ROUTING_ONLY_FOR_ROUTING_GRAPH/
  );
});

test('a routing pack without an engine block fails closed', () => {
  assert.throws(() => validateOfflinePack(pack({ routing: undefined })), /ROUTING_GRAPH_REQUIRES_ENGINE/);
});

test('unsupported routing engines are rejected', () => {
  assert.throws(
    () => validateOfflinePack(pack({ routing: { engine: 'proprietary-cloud-router', engine_version: '9.9.9', profile: 'car' } })),
    /BAD_ROUTING_ENGINE/
  );
});

test('a matching revision yields ROUTE_AVAILABLE_FROM_PACK', () => {
  assert.equal(routeAvailability(pack(), request({ requested_pack_revision: '2026.10.10-r0' })), 'ROUTE_AVAILABLE_FROM_PACK');
});

test('a mismatching pack revision is rejected', () => {
  assert.equal(routeAvailability(pack(), request({ requested_pack_revision: '2026.10.10-r1' })), 'PACK_REVISION_MISMATCH');
});

test('a mismatching companion pack revision is rejected', () => {
  const companion = pack({
    routing: { engine: 'brouter', engine_version: '1.8.1', profile: 'car-fast', companion_pack_revisions: ['vector-2026.10.10-r0'] }
  });
  assert.equal(
    routeAvailability(companion, request({ required_companion_revision: 'vector-2026.10.10-r1' })),
    'PACK_REVISION_MISMATCH'
  );
  assert.equal(
    routeAvailability(companion, request({ required_companion_revision: 'vector-2026.10.10-r0' })),
    'ROUTE_AVAILABLE_FROM_PACK'
  );
});

test('archives need real sha256 digests', () => {
  assert.throws(() => validateOfflinePack(pack({
    archives: [{ role: 'routing_graph', file_name: 'hamburg-graph.brp', sha256: 'nothex', bytes: 1234 }]
  })), /BAD_DIGEST/);
});

test('packs without archives are rejected', () => {
  assert.throws(() => validateOfflinePack(pack({ archives: [] })), /NO_ARCHIVES/);
});

test('update policies without rollback support are rejected', () => {
  assert.throws(() => validateOfflinePack(pack({ update_policy: { rollback_supported: false } })), /BAD_UPDATE_POLICY/);
});

test('packs without a provenance atom reference are rejected', () => {
  assert.throws(() => validateOfflinePack(pack({ provenance_atom_ref: null })), /PROVENANCE_ATOM_REF_REQUIRED/);
});

function orthoPack(inlineAtom) {
  const p = pack({
    pack_id: 'hamburg-dop20-pilot',
    pack_kind: 'ORTHOPHOTO',
    routing: undefined,
    archives: [{ role: 'orthophoto', file_name: 'hamburg-dop20.pmtiles', sha256: 'd'.repeat(64), bytes: 999 }],
    inline_provenance_atom: inlineAtom
  });
  return p;
}

test('orthophoto packs require an inline provenance atom', () => {
  assert.throws(() => validateOfflinePack(orthoPack(undefined)), /PROVENANCE_ATOM_REQUIRED/);
});

test('research-only orthophoto rights mean no pack (fail-closed)', () => {
  const researchOnly = { ...DOP20_ATOM, rights_status: 'RESEARCH_ONLY_UNTIL_CLEARANCE' };
  assert.throws(() => validateOfflinePack(orthoPack(researchOnly)), /DENIED_RIGHTS_NO_PACK/);
});

test('a cleared DOP20-style orthophoto atom allows a valid pack', () => {
  assert.equal(validateOfflinePack(orthoPack(DOP20_ATOM)).pack_kind, 'ORTHOPHOTO');
});

test('malformed pack ids are rejected', () => {
  assert.throws(() => validateOfflinePack(pack({ pack_id: 'Hamburg Graph!' })), /BAD_PACK_ID/);
});

test('malformed requests fail closed', () => {
  assert.throws(() => routeAvailability(pack(), null), /BAD_REQUEST/);
  assert.throws(() => routeAvailability(pack(), request({ evaluation_utc: 'gestern' })), /BAD_EVALUATION_TIME/);
  assert.throws(() => routeAvailability(pack(), request({ point: [10.0] })), /BAD_POINT/);
});
