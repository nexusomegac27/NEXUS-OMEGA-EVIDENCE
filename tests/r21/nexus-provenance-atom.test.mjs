import test from 'node:test';
import assert from 'node:assert/strict';
import { validateProvenanceAtom, lodRightsProjection, truthLine } from '../../examples/r21/nexus-provenance-atom.mjs';

const atom = (extra = {}) => ({
  asset_id: 'hamburg-dop20-2021-tile-research',
  upstream_contributors: ['Landesbetrieb Geoinformation und Vermessung Hamburg', 'Copernicus Sentinel-2'],
  source_url: 'https://example.org/dop20-research-fixture',
  license_id: 'DL-DE-BY-2.0',
  native_gsd_m: 0.20,
  acquired_utc: '2021-03-15T10:00:00Z',
  asset_sha256: 'a'.repeat(64),
  rights_status: 'RESEARCH_ONLY_UNTIL_CLEARANCE',
  attribution: { first_class: true, visible_label: 'Hamburg DOP20 (0,20 m) - LGV Hamburg', expiry_check_required: true },
  nexus_transformation: 'PMTiles repack, no resampling beyond native GSD',
  symbiose_links: ['orbis-surface-p0', 'gsd-gate', 'offline-packet-p1'],
  is_living_artifact: true,
  ...extra
});

test('valid atom passes and keeps its Herkunfts-Spur (contributors remain named)', () => {
  const a = validateProvenanceAtom(atom());
  assert.equal(a.is_living_artifact, true);
  assert.equal(a.upstream_contributors.length, 2);
  assert.match(truthLine(a), /Landesbetrieb Geoinformation und Vermessung Hamburg/);
  assert.match(truthLine(a), /Copernicus Sentinel-2/);
  assert.match(truthLine(a), /0,20 m nativ/);
});

test('R21.1 negative 1: missing license_id fails closed', () => {
  assert.throws(() => validateProvenanceAtom(atom({ license_id: '' })), /BAD_LICENSE/);
});

test('R21.1 negative 2: missing native_gsd_m fails closed', () => {
  assert.throws(() => validateProvenanceAtom(atom({ native_gsd_m: undefined })), /BAD_GSD/);
});

test('R21.1 negative 3: invisible attribution fails closed', () => {
  assert.throws(() => validateProvenanceAtom(atom({ attribution: { first_class: false, visible_label: 'x', expiry_check_required: true } })), /INVISIBLE_ATTRIBUTION/);
  assert.throws(() => validateProvenanceAtom(atom({ attribution: { first_class: true, visible_label: '', expiry_check_required: true } })), /INVISIBLE_ATTRIBUTION/);
});

test('R21.1 negative 4: invented pixel beyond native GSD fails closed', () => {
  assert.throws(() => validateProvenanceAtom(atom({ declared_output_gsd_m: 0.05 })), /INVENTED_DETAIL_BEYOND_NATIVE_GSD/);
});

test('research-only rights project to PENDING_REVIEW for LOD selection, never APPROVED', () => {
  assert.equal(lodRightsProjection(atom()), 'PENDING_REVIEW');
  const approved = atom({ rights_status: 'APPROVED_FOR_THIS_USE' });
  assert.equal(lodRightsProjection(approved), 'APPROVED_FOR_THIS_USE');
});

test('atom without contributors or living-artifact flag fails closed', () => {
  assert.throws(() => validateProvenanceAtom(atom({ upstream_contributors: [] })), /BAD_CONTRIBUTORS/);
  assert.throws(() => validateProvenanceAtom(atom({ is_living_artifact: false })), /NOT_A_LIVING_ARTIFACT/);
});

test('placeholder or non-hex digests fail closed (no fake receipts)', () => {
  assert.throws(() => validateProvenanceAtom(atom({ asset_sha256: 'sha256:place-holder-only' })), /BAD_DIGEST/);
});
