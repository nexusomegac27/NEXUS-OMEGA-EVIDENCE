// R44-9 MISTRAL/VIBE Experimentskript, gehaltene Referenz, via Node ausfuehrbar, keine I/O.
// Repliziert die im Adjudikations-Sandbox identischen Algorithmen; kein produktiver Einsatz, kein Gate-Credit.

const RHO = 0.8, SIGMA = 1.0, Z = 1.959963984540054, Q_BONF = 2.241402727604947;
const AR1 = { 5: 3.62144, 10: 5.4294967296 };
const CELLS = [[0.8,5],[0.8,10],[2,5],[2,10],[4,5],[4,10]];
const MU_MULT = [1, 0.8, 1.1, 1.3];
const N_TRIALS = 256, N_CAL = 4000;

function makeRng(seed) { let x = seed % 2147483647; if (x <= 0) x += 2147483646; let have = false, spare = 0;
  return { uniform() { x = (16807 * x) % 2147483647; return (x - 1) / 2147483646; },
    normal() { if (have) { have = false; return spare; } let u1 = 0; while (u1 <= 0) u1 = this.uniform();
      const u2 = this.uniform(); const r = Math.sqrt(-2 * Math.log(u1)), th = 2 * Math.PI * u2;
      spare = r * Math.sin(th); have = true; return r * Math.cos(th); } }; }

function ar1VarFactor(n) { let s = 1; for (let k = 1; k < n; k++) s += 2 * ((n - k) / n) * Math.pow(RHO, k); return s; }

function oneTrial(rng, s, n) {
  const y = [];
  for (let j = 0; j < 4; j++) { const row = []; let e = Math.sqrt(1 - RHO * RHO) * rng.normal(); row.push(e);
    for (let t = 1; t < n; t++) { e = RHO * e + Math.sqrt(1 - RHO * RHO) * rng.normal(); row.push(e); } y.push(row); }
  const mu = MU_MULT.map(m => s * m);
  const oldM = [0,0,0,0], corM = [0,0,0,0], valid = [0,0,0,0];
  const Mold = [], Mcor = []; let bonOld = true, bonCor = true;
  for (let j = 0; j < 4; j++) { let sum = 0; for (let t = 0; t < n; t++) sum += y[j][t];
    const mh = sum / n; let ss = 0; for (let t = 0; t < n; t++) ss += (y[j][t] - mh) * (y[j][t] - mh);
    const sv = ss / (n - 1);
    const seOld = Math.sqrt(sv / n), seCor = Math.sqrt(sv * AR1[n] / n);
    if (Number.isFinite(mh) && Number.isFinite(sv) && sv > 0) valid[j] = 1;
    if (Math.abs(mh - mu[j]) <= Z * seOld) oldM[j] = 1;
    if (Math.abs(mh - mu[j]) <= Z * seCor) corM[j] = 1;
    if (Math.abs(mh - mu[j]) > Q_BONF * seOld) bonOld = false;
    if (Math.abs(mh - mu[j]) > Q_BONF * seCor) bonCor = false;
    Mold.push(Math.abs(mh - mu[j]) / seOld); Mcor.push(Math.abs(mh - mu[j]) / seCor); }
  return { oldM, corM, valid, M_old: Math.max(...Mold), M_cor: Math.max(...Mcor), bonOld, bonCor }; }

function truncatedBinomTail(a, b) { const M = a + b; let cdf = 0;
  for (let k = 0; k <= Math.min(a, b); k++) { let comb = 1; for (let i = 0; i < k; i++) comb = comb * (M - i) / (i + 1); cdf += comb * Math.pow(0.5, M); }
  return Math.min(1, 2 * cdf); }

function maskBits(mask) { return mask[0] | (mask[1] << 1) | (mask[2] << 2) | (mask[3] << 3); }

function runCell(k, s, n) {
  const rng = makeRng(20261125 + k * 7919);
  const rows = []; const MoldAll = [], McorAll = [];
  for (let t = 0; t < N_TRIALS; t++) { const tr = oneTrial(rng, s, n);
    rows.push([s, n, t + 1, maskBits(tr.oldM).toString(16), maskBits(tr.corM).toString(16), maskBits(tr.valid).toString(16)].join("|"));
    MoldAll.push(tr.M_old); McorAll.push(tr.M_cor); }
  return rows; }

function calibratedQuantile(kArr, Mdist, alpha) { const s = Mdist.slice().sort((a, b) => a - b); return s[Math.ceil(alpha * Mdist.length) - 1]; }

module.exports = { makeRng, oneTrial, runCell, truncatedBinomTail, maskBits, calibratedQuantile };