/**
 * NEXUS OMEGA Q0 Reference R1 — Independent Audit Test Suite (FAIL_CLOSED)
 * Objekt: NEXUS_OMEGA_AXIOM_Q0_RECONSTRUCTED_VIEWER_R1_FAIL_CLOSED_TEST_SUITE_20261108_R0
 * Auftrag: AXIOM_REMEDIATION_SPEC_20261108_R1 (18/18 gefordert; hier 20 Prüfungen
 * inkl. der neuen R1-Verifikationsbefunde N7 Default-Pose-Stereografie und N8 y-Kantenguard)
 *
 * Ausführungsumgebung: Node.js (getestet als funktionale Replik; kanonische
 * Node-Ausführung erfolgt im Repo unter tests/audit-q0-reference-r1.mjs gegen
 * q0-reference-r1/viewer.js). Exit-Code 0 nur bei 20/20 PASS.
 *
 * Assert-Semantik: Positive Prüfungen müssen finite, korrekte Geometrie liefern.
 * Negative Prüfungen MÜSSEN mit definiertem Fehlercode FAIL_CLOSED enden;
 * nichtendliche Ausgaben oder stille Substitutionen gelten als FEHLER.
 */

import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const src = fs.readFileSync(new URL('../q0-reference-r1/viewer.js', import.meta.url), 'utf8');

// DOM/Canvas-Stubs (wie im R0-Audit; zeichnet in ein Call-Protokoll)
const calls = [];
const elements = new Map();
const elem = id => {
  if (!elements.has(id)) elements.set(id, {
    id, value: 'perspective', textContent: '', children: [],
    appendChild(x) { this.children.push(x); },
    addEventListener() {},
    getContext() {
      return {
        clearRect() {}, beginPath() {},
        moveTo(x, y) { calls.push(['moveTo', x, y]); },
        lineTo(x, y) { calls.push(['lineTo', x, y]); },
        stroke() {}
      };
    },
    width: 800, height: 600
  });
  return elements.get(id);
};
const sandbox = {
  document: {
    getElementById: elem,
    createElement: () => ({ appendChild() {}, addEventListener() {} }),
    querySelectorAll: () => []
  },
  requestAnimationFrame: () => {},
  setInterval: () => {},
  fetch: async () => ({ ok: false }),
  console
};
vm.runInNewContext(
  src + '\n;globalThis.__x={vertices,edges,applySO4,project,toScreen,draw,angles,errorState};',
  sandbox, { timeout: 2000 }
);
const { vertices, edges, applySO4, project, toScreen, draw } = sandbox.__x;

const checks = [];
function test(name, fn) {
  try { fn(); checks.push({ name, pass: true }); }
  catch (err) { checks.push({ name, pass: false, error: String(err) }); }
}
const expectsCode = (fn, code) => {
  try { fn(); assert.fail('no error raised'); }
  catch (err) {
    if (err && err.code === undefined) throw err; // assert.fail weiterreichen
    assert.equal(err.code, code, `expected ${code}, got ${err.code}`);
  }
};
const allFinite = fn => { const out = fn(); assert.ok(out.every(Number.isFinite), 'nonfinite output'); return out; };

const zero = { XY: 0, XZ: 0, XW: 0, YZ: 0, YW: 0, ZW: 0 };

// ============ Positive/Baseline-Prüfungen (12) ============
test('P01 16 unique 4D vertices', () => {
  assert.equal(vertices.length, 16);
  assert.equal(new Set(vertices.map(x => x.join(','))).size, 16);
});
test('P02 32 unique bit-adjacent edges', () => {
  assert.equal(edges.length, 32);
  for (const [i, j] of edges) assert.equal(vertices[i].filter((v, k) => v !== vertices[j][k]).length, 1);
});
test('P03 SO(4) norm invariance over all 6 planes (no drift)', () => {
  for (const plane of Object.keys(zero)) {
    const a = { ...zero, [plane]: 1.237 };
    for (const v of vertices) {
      const w = applySO4(v, a);
      const n = v.reduce((s, x) => s + x * x, 0), m = w.reduce((s, x) => s + x * x, 0);
      assert.ok(Math.abs(m - n) < 1e-12, `norm drift in plane ${plane}`);
    }
  }
});
test('P04 identity rotation all vertices', () => {
  for (const v of vertices) {
    const w = applySO4(v, zero);
    for (let i = 0; i < 4; i++) assert.ok(Math.abs(w[i] - v[i]) < 1e-9);
  }
});
test('P05 orthographic drops W', () => {
  const out = allFinite(() => project([1, 2, 3, 0.5], 'orthographic'));
  assert.deepEqual(out, [1, 2, 3]);
});
test('P06 perspective nominal finite', () => allFinite(() => project([1, 2, 0, 0.1], 'perspective')));
test('P07 stereographic nominal finite (w<1)', () => allFinite(() => project([1, 2, 0, 0.1], 'stereographic')));
test('P08 schlegel nominal finite', () => allFinite(() => project([1, 2, 0, 0.1], 'schlegel')));
test('P09 double-perspective nominal finite', () => allFinite(() => project([1, 1, 0.2, 0.1], 'double-perspective')));
test('P10 perspective near-pole finite (w=2.999999)', () => allFinite(() => project([0.1, 0.1, 0.1, 2.999999], 'perspective')));
test('P11 draw pipeline nominal full render (orthographic)', () => {
  calls.length = 0;
  elem('projection-mode').value = 'orthographic';
  draw();
  assert.equal(sandbox.__x.errorState, null);
  assert.ok(calls.length > 0, 'nothing drawn');
  for (const c of calls) for (const v of c.slice(1)) assert.ok(Number.isFinite(v));
});
test('P12 draw pipeline nominal full render (perspective)', () => {
  calls.length = 0;
  elem('projection-mode').value = 'perspective';
  draw();
  assert.equal(sandbox.__x.errorState, null);
});

// ============ Negative Prüfungen: MÜSSEN FAIL_CLOSED sein (8) ============
test('N01 Lücke 1: perspective pole w=3 -> ProjectionSingularityError', () =>
  expectsCode(() => project([1, 1, 1, 3], 'perspective'), 'PROJECTION_SINGULARITY:PERSPECTIVE_POLE_W'));
test('N02 Lücke 2: schlegel pole w=2 -> SchlegelBoundaryError', () =>
  expectsCode(() => project([1, 1, 1, 2], 'schlegel'), 'PROJECTION_SINGULARITY:SCHLEGEL_BOUNDARY:POLE_PLANE_W2'));
test('N03 Lücke 3: double-perspective pole z=3 -> kaskadierte Zurückweisung', () =>
  expectsCode(() => project([1, 1, 3, 0], 'double-perspective'), 'PROJECTION_SINGULARITY:DOUBLE_PERSPECTIVE_POLE_Z'));
test('N04 Lücke 4: stereographic pole w=1 -> FAIL_CLOSED statt stiller orthografischer Substitution', () => {
  expectsCode(() => project([1, 2, 3, 1], 'stereographic'), 'PROJECTION_SINGULARITY:STEREOGRAPHIC_POLE:NO_SILENT_FALLBACK');
});
test('N05 Lücke 5: NaN-Rotationswinkel -> INVALID_ROTATION_PARAMETER', () =>
  expectsCode(() => applySO4([1, 2, 3, 4], { ...zero, XY: NaN }), 'INVALID_ROTATION_PARAMETER:XY'));
test('N06 Lücke 6: nichtendliche Bildschirm-y wird zurückgewiesen', () =>
  expectsCode(() => toScreen([1, Infinity, 0]), 'SCREEN_COORDINATE:NONFINITE_INPUT'));
test('N07 NEU: stereographic DEFAULT-Pose -> definierter Fehlerzustand, keine Mischprojektion', () => {
  calls.length = 0;
  elem('projection-mode').value = 'stereographic';
  draw(); // alle Winkel 0: 8 Eckpunkte mit w=+1 treffen den Pol
  assert.equal(sandbox.__x.errorState, 'PROJECTION_SINGULARITY:STEREOGRAPHIC_POLE:NO_SILENT_FALLBACK');
  assert.equal(calls.length, 0, 'partial render despite FAIL_CLOSED');
});
test('N08 NEU: Kantenguard prüft BEIDE Koordinaten; Nichtendliches erreicht nie moveTo/lineTo', () => {
  calls.length = 0;
  elem('projection-mode').value = 'orthographic';
  sandbox.__x.angles.XW = NaN; // nichtendlicher Winkel -> Fehlerzustand, kein Plot
  draw();
  assert.equal(sandbox.__x.errorState, 'INVALID_ROTATION_PARAMETER:XW');
  assert.equal(calls.length, 0, 'nonfinite coordinate reached canvas');
  sandbox.__x.angles.XW = 0; // Zustand zurücksetzen
  assert.ok(src.includes('isFinite(a[0]) || !isFinite(a[1])'), 'y-guard missing in source');
});

// ============ Receipt ============
const pass = checks.filter(x => x.pass).length;
console.log(JSON.stringify({
  object: 'NEXUS_OMEGA_AXIOM_Q0_RECONSTRUCTED_VIEWER_R1_FAIL_CLOSED_TEST_SUITE_20261108_R0',
  node: process.version,
  pass,
  total: checks.length,
  failed: checks.filter(x => !x.pass),
  remediation_order: 'AXIOM_REMEDIATION_SPEC_20261108_R1',
  claims: 'REVISED_REFERENCE_R1_ONLY_NOT_PRODUCTION',
  claim_ceiling: 'C1_DESCRIPTIVE_ONLY'
}, null, 2));
if (checks.some(x => !x.pass)) process.exitCode = 1; // 20/20 gefordert; Gegenbeispiele werden nie versteckt