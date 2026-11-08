/**
 * NEXUS OMEGA Bodytwin Q0 Viewer — Reference Implementation
 * Claim Ceiling: C1_DESCRIPTIVE_ONLY
 * Status: RECONSTRUCTED_EXPERT_REFERENCE · NOT_ORIGINAL_PRODUCTION_SOURCE
 * Tesseract (16 vertices, 32 edges, 24 faces, 8 cells) with SO(4) plane rotations
 * and five projection modes.
 */

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');
const liveEl = document.getElementById('live-status');
const modeSelect = document.getElementById('projection-mode');
const planeContainer = document.getElementById('plane-controls');

let paused = false;
let angles = { XY: 0, XZ: 0, XW: 0, YZ: 0, YW: 0, ZW: 0 };

// Generate tesseract vertices (all combinations of ±1 in 4D)
const vertices = [];
for (let i = 0; i < 16; i++) {
  vertices.push([
    (i & 1) ? 1 : -1,
    (i & 2) ? 1 : -1,
    (i & 4) ? 1 : -1,
    (i & 8) ? 1 : -1
  ]);
}

// Edges: pairs differing by exactly one bit
const edges = [];
for (let i = 0; i < 16; i++) {
  for (let b = 0; b < 4; b++) {
    const j = i ^ (1 << b);
    if (j > i) edges.push([i, j]);
  }
}

function rot2D(theta) {
  const c = Math.cos(theta), s = Math.sin(theta);
  return [[c, -s], [s, c]];
}

function applySO4(v, angles) {
  let p = [...v];
  const planes = [
    ['XY', 0, 1],
    ['XZ', 0, 2],
    ['XW', 0, 3],
    ['YZ', 1, 2],
    ['YW', 1, 3],
    ['ZW', 2, 3]
  ];
  for (const [name, a, b] of planes) {
    const R = rot2D(angles[name]);
    const x = p[a], y = p[b];
    p[a] = R[0][0] * x + R[0][1] * y;
    p[b] = R[1][0] * x + R[1][1] * y;
  }
  return p;
}

function project(p4, mode) {
  let [x, y, z, w] = p4;
  const d = 3.0; // distance
  switch (mode) {
    case 'orthographic':
      return [x, y, z];
    case 'perspective':
      const s = d / (d - w);
      return [x * s, y * s, z * s];
    case 'stereographic':
      const denom = 1 - w;
      if (Math.abs(denom) < 1e-6) return [x, y, z];
      const s2 = 1 / denom;
      return [x * s2, y * s2, z * s2];
    case 'schlegel':
      // simple Schlegel-like: project from point outside
      const scale = 2 / (2 - w);
      return [x * scale, y * scale, z * scale];
    case 'double-perspective':
      const s3 = d / (d - w);
      const s4 = d / (d - z);
      return [x * s3, y * s3 * s4, z * s4];
    default:
      return [x, y, z];
  }
}

function toScreen(p3) {
  const [x, y] = p3;
  const scale = 180;
  return [
    canvas.width / 2 + x * scale,
    canvas.height / 2 - y * scale
  ];
}

function draw() {
  if (paused) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#58a6ff';
  ctx.lineWidth = 1.5;

  const mode = modeSelect.value;
  const projected = vertices.map(v => {
    const r = applySO4(v, angles);
    const p3 = project(r, mode);
    return toScreen(p3);
  });

  for (const [i, j] of edges) {
    const a = projected[i], b = projected[j];
    if (!a || !b || !isFinite(a[0]) || !isFinite(b[0])) continue;
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
  }

  statusEl.textContent = `Mode: ${mode} · C1_DESCRIPTIVE_ONLY · Reference`;
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
      angles[p] = parseFloat(input.value);
    });
    label.appendChild(input);
    planeContainer.appendChild(label);
  });
}

document.getElementById('reset').addEventListener('click', () => {
  angles = { XY: 0, XZ: 0, XW: 0, YZ: 0, YW: 0, ZW: 0 };
  document.querySelectorAll('#plane-controls input').forEach(i => i.value = 0);
});

document.getElementById('pause').addEventListener('click', (e) => {
  paused = !paused;
  e.target.textContent = paused ? 'Resume' : 'Pause';
  if (!paused) draw();
});

modeSelect.addEventListener('change', () => { if (!paused) draw(); });

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
