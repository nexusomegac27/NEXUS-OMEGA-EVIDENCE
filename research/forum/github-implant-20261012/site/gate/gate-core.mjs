/* NEXUS OMEGA · Gate V2 source/release evidence core · C1 only · Apache-2.0 */
export const CONTRACT = Object.freeze({
  repository: 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
  sourceRoot: 'research/forum/github-implant-20261012/site/',
  targetRoot: '/forum/github-implant/',
  claimCeiling: 'C1_DESCRIPTIVE_ONLY',
  manifest: 'gate/release-v2.json',
  // Fixed set; no user input / arbitrary path may extend the public acquisition surface.
  files: Object.freeze([
    'index.html', 'assets/github-implant.css', 'assets/github-implant.js',
    'nexus-temporal-anchor-r11.css', 'nexus-temporal-anchor-r11.mjs', 'temporal-anchor-r11.json',
    'gate/index.html', 'gate/gate.css', 'gate/gate.js', 'gate/gate-core.mjs'
  ]),
  maxBytes: 600000,
  freshnessMs: 30 * 60 * 1000,
  clickCooldownMs: 60 * 1000
});
const HEX40 = /^[0-9a-f]{40}$/;
const HEX64 = /^[0-9a-f]{64}$/;
const plainObject = x => x !== null && typeof x === 'object' && !Array.isArray(x);
export function isC1Marked(s) {
  return typeof s === 'string' && s.includes('C1_DESCRIPTIVE_ONLY') &&
    !/\bC2_(?:PROVEN|VALIDATED)\b/.test(s);
}
export function sourcePath(file) {
  if (!CONTRACT.files.includes(file)) throw Error('DENY_PATH_NOT_IN_ALLOWLIST');
  return CONTRACT.sourceRoot + file;
}
export function sourceUrl(file, commit) {
  if (typeof commit !== 'string' || !HEX40.test(commit)) throw Error('INVALID_PINNED_SOURCE_COMMIT');
  return 'https://api.github.com/repos/' + CONTRACT.repository + '/contents/' +
    sourcePath(file).split('/').map(encodeURIComponent).join('/') + '?ref='+commit;
}
export function liveUrl(file, origin) {
  sourcePath(file);
  if (typeof origin !== 'string' || !/^https:\/\/[^/?#]+$/.test(origin)) throw Error('INVALID_SITE_ORIGIN');
  return origin + CONTRACT.targetRoot + file;
}
export function validateReleaseManifest(m) {
  if (!plainObject(m) || Object.keys(m).sort().join(',') !==
      ['claim_ceiling','files','release_ref','schema','target_root'].sort().join(','))
    throw Error('INVALID_RELEASE_MANIFEST_KEYS');
  if (m.schema !== 'nexus-gate-release-v2' || m.claim_ceiling !== CONTRACT.claimCeiling ||
      m.target_root !== CONTRACT.targetRoot || typeof m.release_ref !== 'string' || !HEX40.test(m.release_ref))
    throw Error('INVALID_RELEASE_MANIFEST_METADATA');
  if (!plainObject(m.files) || Object.keys(m.files).length !== CONTRACT.files.length ||
      Object.keys(m.files).some(x => !CONTRACT.files.includes(x))) throw Error('INVALID_RELEASE_FILESET');
  for (const file of CONTRACT.files) {
    const rec = m.files[file];
    if (!plainObject(rec) || Object.keys(rec).sort().join(',') !== 'bytes,sha256' ||
        !Number.isSafeInteger(rec.bytes) || rec.bytes <= 0 || rec.bytes > CONTRACT.maxBytes ||
        typeof rec.sha256 !== 'string' || !HEX64.test(rec.sha256))
      throw Error('INVALID_RELEASE_FILE:' + file);
  }
  return Object.freeze({sourceCommit: m.release_ref, fileRecords: m.files});
}
export function hex(bytes) {
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}
export async function digest(bytes) {
  if (!(bytes instanceof Uint8Array)) throw Error('INVALID_INPUT_BYTES');
  if (!globalThis.crypto?.subtle) throw Error('WEBCRYPTO_NOT_AVAILABLE');
  return hex(new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', bytes)));
}
export function parseGitHubContent(meta) {
  if (!plainObject(meta) || meta.encoding !== 'base64' ||
      typeof meta.content !== 'string' || !HEX40.test(meta.sha || '') ||
      !Number.isSafeInteger(meta.size) || meta.size < 1 || meta.size > CONTRACT.maxBytes)
    throw Error('INVALID_GITHUB_CONTENT_METADATA');
  const encoded = meta.content.replace(/\s/g, '');
  if (!encoded || encoded.length > 900000 || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(encoded))
    throw Error('INVALID_GITHUB_BASE64');
  const raw = atob(encoded);
  if (raw.length !== meta.size) throw Error('GITHUB_SIZE_MISMATCH');
  return Uint8Array.from(raw, ch => ch.charCodeAt(0));
}
export function compareFile(file, pinned, gh, www) {
  const status = !gh ? 'SOURCE_GAP' : !www ? 'WWW_GAP' :
    gh.bytes !== pinned.bytes || gh.sha !== pinned.sha256 ? 'RELEASE_SOURCE_MISMATCH' :
    www.bytes !== pinned.bytes || www.sha !== pinned.sha256 ? 'WWW_RELEASE_MISMATCH' :
    gh.sha === www.sha && gh.bytes === www.bytes ? 'MATCH' : 'DIVERGENCE';
  return {file, status, gh, www};
}
export function classify(rows, manifestOK, c1OK, sourceHead) {
  if (!manifestOK) return {code: 'HOLD_RELEASE_BIND', label: 'RELEASE-BIND FEHLT', detail: 'Die Veröffentlichung besitzt kein vollständig prüfbares Release-Manifest'};
  if (!Array.isArray(rows) || rows.length !== CONTRACT.files.length ||
      new Set(rows.map(x => x.file)).size !== CONTRACT.files.length ||
      rows.some(x => !CONTRACT.files.includes(x.file)))
    return {code:'HOLD_SCOPE',label:'PRÜFUMFANG UNVOLLSTÄNDIG',detail:'Nicht alle zehn Allowlist-Dateien wurden gebunden'};
  if (rows.some(x => x.status === 'SOURCE_GAP')) return {code:'HOLD_SOURCE',label:'QUELLENLÜCKE',detail:'Gepinnte GitHub-Quelle fehlt oder kann nicht gelesen werden'};
  if (rows.some(x => x.status === 'WWW_GAP')) return {code:'HOLD_WWW',label:'WWW-LÜCKE',detail:'Mindestens eine veröffentlichte Datei ist nicht abrufbar'};
  if (rows.some(x => x.status !== 'MATCH')) return {code:'DIVERGENCE',label:'RELEASE-DIVERGENZ',detail:'GitHub, Release-Manifest und WWW-Bytes stimmen nicht vollständig überein'};
  if (!c1OK) return {code:'SCIENCE_WARN',label:'C1-KENNZEICHNUNG FEHLT',detail:'Die referenzierte öffentliche Seite weist ihre C1-Grenze nicht eindeutig aus'};
  // main may move independently of a deployed release. This is not a mismatch.
  return {code:'MATCH_C1',label:'RELEASE-BYTES IDENTISCH',detail: sourceHead ? '10/10 gegen gepinnten Release-Commit · main ist eine getrennte Referenz' : '10/10 gegen gepinnten Release-Commit · main derzeit unbekannt'};
}
export function statusIsStale(lastCheckMonotonicMs, nowMonotonicMs, documentWasHidden, limitMs=CONTRACT.freshnessMs) {
  if (documentWasHidden || !Number.isFinite(lastCheckMonotonicMs) || !Number.isFinite(nowMonotonicMs)) return true;
  if (nowMonotonicMs < lastCheckMonotonicMs) return true;
  return nowMonotonicMs - lastCheckMonotonicMs >= limitMs;
}

/* Fail-closed, same-GitHub raw transport fallback for REST 403/429. */
export function pinnedRawURL(file,commit) {
  if(typeof commit!=='string'||!HEX40.test(commit))throw Error('INVALID_PINNED_COMMIT');
  const path=sourcePath(file).split('/').map(encodeURIComponent).join('/');
  return 'https://raw.githubusercontent.com/'+CONTRACT.repository+'/'+commit+'/'+path;
}
export function restRateFailure(status) {return status===403||status===429;}
export async function fetchRawPinned(file,commit,fetchFn=globalThis.fetch,timeoutMs=12000) {
  const url=pinnedRawURL(file,commit);
  const ctrl=new AbortController(),timer=setTimeout(()=>ctrl.abort(),timeoutMs);
  try{
    const res=await fetchFn(url,{method:'GET',signal:ctrl.signal,cache:'no-store',credentials:'omit',redirect:'error',mode:'cors',referrerPolicy:'no-referrer'});
    if(!res.ok)throw Error('RAW_HTTP_'+res.status);
    const declared=res.headers?.get?.('Content-Length');
    if(declared!==null&&declared!==undefined&&Number(declared)>CONTRACT.maxBytes)throw Error('RAW_CONTENT_TOO_LARGE');
    const bytes=new Uint8Array(await res.arrayBuffer());
    if(!bytes.length||bytes.length>CONTRACT.maxBytes)throw Error('RAW_BYTES_OUT_OF_BOUNDS');
    return {sha:await digest(bytes),bytes:bytes.length,raw:bytes,transport:'GITHUB_RAW_PINNED',sourceIndependence:false};
  }finally{clearTimeout(timer);}
}
export async function restOrRawPinned(file,commit,primary,fetchFn=globalThis.fetch) {
  try{
    const result=await primary(file,commit);
    return {...result,transport:'GITHUB_REST_PINNED',sourceIndependence:false};
  }catch(err){
    if(!restRateFailure(err?.status))throw err;
    // One and only one fallback. No third-party proxy, no retry storm.
    return fetchRawPinned(file,commit,fetchFn);
  }
}

