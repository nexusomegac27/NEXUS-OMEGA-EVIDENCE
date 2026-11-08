/**
 * NEXUS OMEGA Bodytwin Q0 Viewer — Reference Implementation R1 (FAIL_CLOSED)
 * Claim Ceiling: C1_DESCRIPTIVE_ONLY
 * Status: RECONSTRUCTED_EXPERT_REFERENCE_R1_REMEDIATION · NOT_ORIGINAL_PRODUCTION_SOURCE
 * Remediation order: AXIOM_REMEDIATION_SPEC_20261108_R1 (Lücken 1–6) + R1-Verifikationsbefunde N7/N8
 *
 * Korrekturdisziplin: Dieses File ist ein NEUER Referenzstand R1. Es überschreibt
 * KEINESFALLS die bytegebundenen Q0-Originaldateien aus PR #332 (Append-only).
 * Silent fallbacks sind eliminiert; jede Singularität und jede nichtendliche
 * Koordinate erzeugt einen definierten Fehlerzustand (FAIL_CLOSED).
 */

const EPS_DENOM = 1e-9;   // Lücken 1–3: ε-Sperre gegen Div/0 an Projektionspolen
const MAX_PIXEL = 100000; // Lücke 6: Bildschirm-Bound (Abs MAX_PIXEL)

class ProjectionInputError extends Error {
  constructor(msg) { super(msg); this.name = 'ProjectionInputError'; this.code = 'INVALID_PROJECTION_INPUT'; }
}
class ProjectionSingularityError extends Error {
  constructor(msg) { super(msg); this.name = 'ProjectionSingularityError'; this.code = 'PROJECTION_SINGULARITY:' + msg; }
}
class SchlegelBoundaryError extends ProjectionSingularityError {
  constructor(msg) { super('SCHLEGEL_BOUNDARY:' + msg); this.name = 'SchlegelBoundaryError'; }
}
class StereographicPoleError extends ProjectionSingularityError {
  // Lücke 4: KEIN stiller orthografischer Fallback mehr
  constructor(msg) { super('STEREOGRAPHIC_POLE:' + msg); this.name = 'StereographicPoleError'; }
}
class InvalidRotationParameterError extends Error {
  constructor(msg) { super(msg); this.name = 'InvalidRotationParameterError'; this.code = 'INVALID_ROTATION_PARAMETER:' + msg; }
}
class ScreenCoordinateError extends Error {
  constructor(msg) { super(msg); this.name = 'ScreenCoordinateError'; this.code = 'SCREEN_COORDINATE:' + msg; }
}

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');
const liveEl = document.getElementById('live-status');
const modeSelect = document.getElementById('projection-mode');
const planeContainer = document.getElementById('plane-controls');

let paused = false;
let errorState = null;
let angles = { XY: 0, XZ: 0, XW: 0, YZ: 0, YW: 0, ZW: 0 };

// Tesserakt: 16 Eckpunkte (alle ±1-Kombinationen), 32 Kanten (differieren in genau einem Bit)
const vertices = [];
for (let i = 0; i < 16; i++) {
  vertices.push([(i & 1) ? 1 : -1, (i & 2) ? 1 : -1, (i & 4) ? 1 : -1, (i & 8) ? 1 : -1]);
}
const edges = [];
for (let i = 0; i < 16; i++) {
  for (let b = 0; b < 4; b++) {
    const j = i ^ (1 << b);
    if (j > i) edges.push([i, j]);
  }
}

// Lücke 5: Striktes Input-Sanitizing für alle Rotationswinkel
function assertFiniteAngle(name, value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new InvalidRotationParameterError(name);
  }
}

function rot2D(theta) {
  const c = Math.cos(theta), s = Math.sin(theta);
  return [[c, -s], [s, c]];
}

function applySO4(v, angleSet) {
  const planes = [['XY', 0, 1], ['XZ', 0, 2], ['XW', 0, 3], ['YZ', 1, 2], ['YW', 1, 3], ['ZW', 2, 3]];
  for (const [name] of planes) assertFiniteAngle(name, angleSet[name]);
  let p = [...v];
  for (const [name, a, b] of planes) {
    const R = rot2D(angleSet[name]);
    const x = p[a], y = p[b];
    p[a] = R[0][0] * x + R[0][1] * y;
    p[b] = R[1][0] * x + R[1][1] * y;
  }
  return p;
}

function assertFinite4D(p4) {
  for (const c of p4) {
    if (!Number.isFinite(c)) throw new ProjectionInputError('nonfinite 4D coordinate');
  }
}

function project(p4, mode) {
  assertFinite4D(p4);
  const [x, y, z, w] = p4;
  const d = 3.0; // Kameraabstand
  switch (mode) {
    case 'orthographic':
      return [x, y, z];
    case 'perspective':
      // Lücke 1: ε-Sperre am Pol w = d (Div/0 verhindern), Fehler statt Infinity
      if (Math.abs(d - w) < EPS_DENOM) throw new ProjectionSingularityError('PERSPECTIVE_POLE_W');
      { const s = d / (d - w); return [x * s, y * s, z * s]; }
    case 'stereographic':
      // Lücke 4 + N7: Pol w = 1 liegt AUF dem Tesserakt (Default-Pose!).
      // FAIL_CLOSED mit definiertem Fehlerzustand statt stiller orthografischer Substitution.
      // E1-Designentscheidung offen: Polverschiebung (Projektionspunkt außerhalb der Hülle, z. B. denom = 3 − w)
      // würde die Projektion geometrisch singularitätsfrei machen, ändert aber die Mathematik-Semantik.
      { const denom = 1 - w;
        if (Math.abs(denom) < EPS_DENOM) throw new StereographicPoleError('NO_SILENT_FALLBACK');
        const s2 = 1 / denom; return [x * s2, y * s2, z * s2]; }
    case 'schlegel':
      // Lücke 2: Polebene w = 2 ist geometrisch erreichbar (Eckpunkt-Norm = 2)
      if (Math.abs(2 - w) < EPS_DENOM) throw new SchlegelBoundaryError('POLE_PLANE_W2');
      { const scale = 2 / (2 - w); return [x * scale, y * scale, z * scale]; }
    case 'double-perspective':
      // Lücke 3: kaskadierte ε-Prüfung BEIDE Perspektivachsen
      if (Math.abs(d - w) < EPS_DENOM) throw new ProjectionSingularityError('DOUBLE_PERSPECTIVE_POLE_W');
      if (Math.abs(d - z) < EPS_DENOM) throw new ProjectionSingularityError('DOUBLE_PERSPECTIVE_POLE_Z');
      { const s3 = d / (d - w), s4 = d / (d - z); return [x * s3, y * s3 * s4, z * s4]; }
    default:
      return [x, y, z];
  }
}

// Lücke 6: Boundary-Check VOR Canvas-Plot; Nichtendliches wird zurückgewiesen
function toScreen(p3) {
  const [x, y] = p3;
  if (!Number.isFinite(x) || !Number.isFinite(y)) throw new ScreenCoordinateError('NONFINITE_INPUT');
  const scale = 180;
  const sx = canvas.width / 2 + x * scale;
  const sy = canvas.height / 2 - y * scale;
  if (!Number.isFinite(sx) || !Number.isFinite(sy) || Math.abs(sx) > MAX_PIXEL || Math.abs(sy) > MAX_PIXEL) {
    throw new ScreenCoordinateError('OUT_OF_BOUNDS');
  }
  return [sx, sy];
}

function draw() {
  if (paused) return;
  errorState = null;
  const mode = modeSelect.value;
  const projected = [];
  try {
    // Alles-oder-nichts: keine partielle oder gemischte Projektion (N7)
    for (const v of vertices) {
      projected.push(toScreen(project(applySO4(v, angles), mode)));
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#58a6ff';
    ctx.lineWidth = 1.5;
    for (const [i, j] of edges) {
      const a = projected[i], b = projected[j];
      // N8: Kantenguard über BEIDE Koordinaten (x UND y, nicht nur x)
      if (!isFinite(a[0]) || !isFinite(a[1]) || !isFinite(b[0]) || !isFinite(b[1])) {
        throw new ScreenCoordinateError('EDGE_GUARD_NONFINITE_ENDPOINT');
      }
      ctx.beginPath();
      ctx.moveTo(a[0], a[1]);
      ctx.lineTo(b[0], b[1]);
      ctx.stroke();
    }
    statusEl.textContent = `Mode: ${mode} · C1_DESCRIPTIVE_ONLY · Reference R1 FAIL_CLOSED`;
  } catch (err) {
    // FAIL_CLOSED: definierter Fehlerzustand, Canvas geleert, kein Rendern falscher Geometrie
    errorState = err.code || 'UNKNOWN_ERROR';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    statusEl.textContent = `ERROR_STATE=${errorState} · mode=${mode} · FAIL_CLOSED · Rotation oder Projektion anpassen`;
    return; // Renderloop stoppt; nächster Nutzereingang startet draw() neu
  }
  requestAnimationFrame(draw);
}

function buildControls() {
  const planes = ['XY', 'XZ', 'XW', 'YZ', 'YW', 'ZW'];
  planes.forEach(p => {
    const label = document.createElement('label');
    label.textContent = p;
    const input = document.createElement('input');
    input.type = 'range';
    input.min = -Math.PI;
    input.max = Math.PI;
    input.step = 0.01;
    input.value = 0;
    input.addEventListener('input', () => {
      angles[p] = parseFloat(input.value); // Validierung übernimmt assertFiniteAngle in applySO4
      if (!paused) draw();
    });
    label.appendChild(input);
    planeContainer.appendChild(label);
  });
}

document.getElementById('reset').addEventListener('click', () => {
  angles = { XY: 0, XZ: 0, XW: 0, YZ: 0, YW: 0, ZW: 0 };
  errorState = null;
  document.querySelectorAll('#plane-controls input').forEach(i => i.value = 0);
  if (!paused) draw();
});

document.getElementById('pause').addEventListener('click', (e) => {
  paused = !paused;
  e.target.textContent = paused ? 'Resume' : 'Pause';
  if (!paused) draw();
});

modeSelect.addEventListener('change', () => { if (!paused) draw(); });

// Live-Feed: unverändert, nur-lesend, getrennt von Geometrie-Rendering (E4-Trennung)
async function updateLive() {
  try {
    const r = await fetch('https://www.nexus-mobile.de/bodytwin/live/current.json');
    if (r.ok) {
      const data = await r.json();
      liveEl.textContent = JSON.stringify({
        seq: data.producer?.seq,
        run_utc: data.producer?.run_utc,
        source_changed: data.producer?.source_changed,
        claim_ceiling: data.claim_ceiling
      }, null, 2);
    } else {
      liveEl.textContent = 'Live feed not reachable (read-only)';
    }
  } catch {
    liveEl.textContent = 'Live feed not reachable (read-only)';
  }
}

buildControls();
draw();
updateLive();
setInterval(updateLive, 60000);