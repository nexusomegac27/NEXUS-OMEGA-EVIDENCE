/* NEXUS OMEGA R11 · public-safe C1 reference · no trusted time/runtime claim.
   No credentials, no external requests, no dynamic HTML, no GitHub writes. */
export const R11_VERSION = 'NEXUS_TEMPORAL_ANCHOR_R11_PUBLIC_C1_STATIC_V1';
export const R11_MODE = 'PUBLIC_C1_REFERENCE_ONLY';
const SOURCE = './temporal-anchor-r11.json';
const MAX_CLIENT_CLOCK_SHIFT_MS = 2000;

export function formatBrowserUtc(ms) {
  if (!Number.isFinite(ms)) return 'UNAVAILABLE';
  try { return new Date(ms).toISOString().replace('T', ' ').replace('Z', ' UTC'); }
  catch { return 'UNAVAILABLE'; }
}

// A client comparison is NEVER an independent measurement of UTC accuracy.
export function classifyWitness(data, nowMs) {
  if (!data || typeof data !== 'object' || data.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY')
    return 'UNKNOWN';
  const value = data.last_backend_witness_utc;
  if (value === null || value === undefined || value === '') return 'UNKNOWN';
  if (typeof value !== 'string' || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(value)) return 'UNKNOWN';
  const stamp = Date.parse(value), ttl = data.witness_ttl_seconds;
  if (!Number.isFinite(stamp) || typeof ttl !== 'number' || !Number.isSafeInteger(ttl) || ttl < 1 || ttl > 86400 || !Number.isFinite(nowMs)) return 'UNKNOWN';
  const age = nowMs - stamp;
  if (age < -2000) return 'UNKNOWN'; // future timestamps: never call live
  return age > ttl * 1000 ? 'STALE' : 'LAST_WITNESSED_REPORTED';
}

export function browserClockShift(wallOriginMs, monoOriginMs, wallNowMs, monoNowMs) {
  for (const v of [wallOriginMs,monoOriginMs,wallNowMs,monoNowMs]) if (!Number.isFinite(v)) return 'UNKNOWN';
  if (monoNowMs < monoOriginMs) return 'UNKNOWN';
  return Math.abs((wallNowMs - wallOriginMs)-(monoNowMs - monoOriginMs)) > MAX_CLIENT_CLOCK_SHIFT_MS
    ? 'SHIFT_DETECTED' : 'NOT_DETECTED_UNVERIFIED';
}

function node(tag, cls, content) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (content !== undefined) e.textContent = String(content);
  return e;
}

async function init() {
  if (document.getElementById('nexus-temporal-anchor-r11')) return;
  const host = document.getElementById('meilensteine') || document.querySelector('main');
  if (!host) return;
  const section = node('section','nexus-r11-temporal');
  section.id = 'nexus-temporal-anchor-r11';
  section.setAttribute('aria-labelledby','nexus-temporal-title');
  const title = node('h2','', 'NEXUS · Zeitanker / R11'); title.id = 'nexus-temporal-title';
  const status = node('p','nexus-r11-tag','C1 · öffentliche Zeitreferenz – kein Node-Herzschlag');
  const clockLabel = node('p','nexus-r11-label','UTC-Anzeige nach lokaler Browseruhr (unverifiziert)');
  const clock = node('output','nexus-r11-clock','—'); clock.setAttribute('aria-label','Unverifizierte Browser-UTC-Zeit');
  const quality = node('p','nexus-r11-quality','Zeitquellenqualität: USER_DEVICE_UNVERIFIED');
  const witness = node('p','nexus-r11-witness','Letzter Backend-Witness: UNKNOWN');
  const runtime = node('p','nexus-r11-runtime','R10: AWAITING_OPERATOR_FUNDAMENT · N33: OPEN · G11: HOLD');
  const note = node('p','nexus-r11-note','Ein laufender Browserzähler beweist keine UTC-Synchronisation, Node-Ausführung oder wissenschaftliche Kontinuität.');
  const link = node('a','nexus-r11-evidence','E12 Evidenz · GitHub PR #320');
  link.href = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/320';
  link.rel = 'noopener noreferrer';link.target='_blank';
  section.append(title,status,clockLabel,clock,quality,witness,runtime,note,link);
  host.insertAdjacentElement('afterend',section);
  const wallOrigin = Date.now(), monoOrigin = performance.now();
  function tick() {
    if (document.hidden) return;
    const wall = Date.now(), mono = performance.now();
    clock.textContent = formatBrowserUtc(wall);
    if (browserClockShift(wallOrigin,monoOrigin,wall,mono)==='SHIFT_DETECTED')
      quality.textContent='Zeitquellenqualität: CLOCK_SHIFT_DETECTED · UTC UNVERIFIED';
  }
  tick();
  window.setInterval(tick,1000);
  try {
    const response=await fetch(SOURCE,{cache:'no-store',credentials:'omit'});
    if(!response.ok) throw new Error('HTTP '+response.status);
    const payload=await response.json();
    const state=classifyWitness(payload,Date.now());
    const raw=typeof payload.last_backend_witness_utc==='string' ? payload.last_backend_witness_utc : 'NONE';
    witness.textContent = `Letzter publizierter Backend-Witness: ${state} · ${raw} (nicht durch Browser kryptografisch validiert)`;
    if(payload.node_runtime_state !== 'NOT_ESTABLISHED')
      runtime.textContent = 'R10/Node-Runtime: UNKNOWN – keine automatische Vertrauenshochsetzung';
  } catch {
    witness.textContent='Letzter publizierter Backend-Witness: UNKNOWN · SOURCE_UNAVAILABLE';
  }
}
if (typeof document !== 'undefined') {
  if (document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
}
