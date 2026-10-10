import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveTruthView, truthBar } from '../../examples/r21/orbis-gsd-truth-ui.mjs';

const a = (id, gsd, extra = {}) => ({
  id, kind: 'AERIAL_ORTHOPHOTO', native_gsd_m: gsd,
  bounds_wsen: [9.6, 53.3, 10.5, 53.9],
  source_url: 'https://example.org/licensed-test-only',
  source_name: 'SYNTHETIC_FIXTURE_DO_NOT_DEPLOY',
  license_id: 'SYNTHETIC_TEST_ONLY',
  required_attribution: 'SYNTHETIC_FIXTURE',
  acquired_utc: '2026-10-01T00:00:00Z', asset_sha256: 'a'.repeat(64),
  rights_status: 'APPROVED_FOR_THIS_USE', offline_available: true, ...extra
});
const view = (zoom, extra = {}) => ({ longitude: 10, latitude: 53.55, zoom, offline: false, ...extra });

test('coarsest-adequate: wide zoom stays on the 10 m source before DOP20 loads', () => {
  const r = resolveTruthView([a('sentinel-2', 10), a('dop20', 0.2)], view(12));
  assert.equal(r.asset_id, 'sentinel-2');
  assert.equal(r.state, 'NATIVE_RESOLUTION_SUPPORTED');
  assert.match(r.truth_bar, /Quellenaufloesung ausreichend/);
});

test('beyond DOP20 native 0,20 m the truth bar confesses the native limit', () => {
  const r = resolveTruthView([a('dop20', 0.2)], view(21));
  assert.equal(r.state, 'NATIVE_DETAIL_EXCEEDED');
  assert.match(r.truth_bar, /0,20 m nativ ueberschritten - kein neues Foto-Detail/);
});

test('coverage gap yields an honest empty bar, never a fabricated source', () => {
  const r = resolveTruthView([a('elsewhere', 0.2)], { longitude: 50, latitude: 1, zoom: 14 });
  assert.equal(r.state, 'COVERAGE_GAP');
  assert.match(r.truth_bar, /keine lizenzierte Abdeckung/);
});

test('truth bar always names source, native GSD and license together', () => {
  const r = resolveTruthView([a('dop20', 0.2)], view(17));
  assert.match(r.truth_bar, /Herkunft: SYNTHETIC_FIXTURE/);
  assert.match(r.truth_bar, /GSD: 0,20 m nativ/);
  assert.match(r.truth_bar, /Lizenz: SYNTHETIC_TEST_ONLY/);
});

test('bad view parameters fail closed instead of guessing', () => {
  assert.throws(() => resolveTruthView([a('ok', 1)], { longitude: 999, latitude: 0, zoom: 10 }), /BAD_VIEW|BAD_MAP_SCALE/);
});
