/* NEXUS OMEGA Gate V2 · browser-only independent GET observations · C1 */
import {
  CONTRACT, sourceUrl, liveUrl, validateReleaseManifest,
  digest, parseGitHubContent, compareFile, classify, isC1Marked, statusIsStale, restOrRawPinned
} from './gate-core.mjs';
const $ = id => document.getElementById(id);
const ORIGIN = location.origin;
const API = 'https://api.github.com/repos/' + CONTRACT.repository;
const DEADLINE_MS = 12000;
let running=false, startedAt=-Infinity, lastCompletedAt=NaN, hiddenSinceCheck=false, pip=null;
let lastStatus={code:'NO_OBSERVATION', label:'NO OBSERVATION', detail:'Keine aktuelle Prüfung'},lastCount='— / 10',lastTime='Nicht geprüft',lastRef='—';
function el(name, css='', value) {const e=document.createElement(name);if(css)e.className=css;if(value!==undefined)e.textContent=String(value);return e;}
function humanDate(date) {return new Intl.DateTimeFormat('de-DE',{dateStyle:'medium',timeStyle:'short',timeZone:'Europe/Berlin'}).format(date);}
function putStatus(s,count='— / 10',ref='—',completed=false) {
  lastStatus=s; lastCount=count; lastRef=ref;
  if(completed){lastCompletedAt=performance.now();hiddenSinceCheck=false;lastTime=humanDate(new Date())+' · Geräteuhr ungeprüft';}
  $('verdict').textContent=s.label; $('verdict-desc').textContent=s.detail;
  $('match-counter').textContent=count; $('timestamp').textContent=lastTime;
  $('head').textContent='RELEASE REF · '+ref;
  $('dot').className='status-indicator '+(s.code==='MATCH_C1'?'ok':s.code==='DIVERGENCE'?'fail':'warn');
  $('dock-status').textContent=s.label; $('dock-info').textContent=s.detail;$('dock-time').textContent='C1 · '+lastTime;
  refreshPip();
}
async function timedGet(url, responseType, sameOrigin=false) {
  const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),DEADLINE_MS);
  try {
    const r=await fetch(url,{method:'GET',signal:ctl.signal,cache:'no-store',credentials:'omit',redirect:'error',referrerPolicy:'no-referrer',headers:sameOrigin?{}:{Accept:'application/vnd.github+json'}});
    if(!r.ok){const e=Error('HTTP '+r.status);e.status=r.status;e.rateRemaining=r.headers.get('x-ratelimit-remaining');e.retryAfter=r.headers.get('retry-after');throw e;}
    const size=Number(r.headers.get('Content-Length')||0);
    if(size>CONTRACT.maxBytes)throw Error('RESPONSE_TOO_LARGE');
    if(responseType==='json') {
      const text=await r.text();if(text.length>750000)throw Error('JSON_TOO_LARGE');
      return JSON.parse(text);
    }
    const bytes=new Uint8Array(await r.arrayBuffer());
    if(bytes.length<1||bytes.length>CONTRACT.maxBytes)throw Error('BYTES_SIZE_INVALID');
    return bytes;
  } finally {clearTimeout(timer);}
}
async function getRelease(){
  const m=await timedGet(ORIGIN+CONTRACT.targetRoot+CONTRACT.manifest,'json',true);
  return validateReleaseManifest(m);
}
async function getSource(file,ref){
  return restOrRawPinned(file,ref,async(f,pin)=>{
    const bytes=parseGitHubContent(await timedGet(sourceUrl(f,pin),'json'));
    return {sha:await digest(bytes),bytes:bytes.length,raw:bytes};
  });
}
async function getWWW(file){
  const bytes=await timedGet(liveUrl(file,ORIGIN),'bytes',true);
  return {sha:await digest(bytes),bytes:bytes.length,raw:bytes};
}
async function getMainHead(){
  try{
    const arr=await timedGet(API+'/commits?sha=main&per_page=1','json');
    return Array.isArray(arr)&&/^[0-9a-f]{40}$/.test(arr[0]?.sha)?arr[0].sha:null;
  }catch{return null;}
}
function renderRows(rows,refs){
  const panel=$('files');panel.replaceChildren();
  for(const x of rows){
    const item=el('article','file-row'),body=el('div');
    const a=el('a','',x.file);a.href='https://github.com/' + CONTRACT.repository + '/blob/' + refs + '/' + CONTRACT.sourceRoot + x.file;
    a.target='_blank';a.rel='noopener noreferrer';body.append(a);
    body.append(el('p','',x.gh?'SOURCE '+(x.gh.transport==='GITHUB_RAW_PINNED'?'[GITHUB RAW FALLBACK]':'[GITHUB REST]')+' · '+x.gh.sha.slice(0,16)+'… · '+x.gh.bytes+' B':'SOURCE · UNAVAILABLE'));
    body.append(el('p','',x.www?'WWW · '+x.www.sha.slice(0,16)+'… · '+x.www.bytes+' B':'WWW · UNAVAILABLE'));
    if(x.error)body.append(el('p','',String(x.error).slice(0,220)));
    item.append(body,el('span','file-state '+x.status.toLowerCase(),x.status));panel.append(item);
  }
}
async function run(force=false){
  const now=performance.now();
  if(running||(!force&&now-startedAt<CONTRACT.clickCooldownMs))return;
  if(!globalThis.crypto?.subtle){putStatus({code:'HOLD_CRYPTO',label:'WEBCRYPTO NICHT VERFÜGBAR',detail:'SHA-256 benötigt einen sicheren Browserkontext'});return;}
  running=true;startedAt=now;$('run').disabled=true;
  $('verdict').textContent='PRÜFUNG LÄUFT';$('verdict-desc').textContent='Gepinnte GitHub-Quellen gegen Website und Release-Manifest…';
  let rows=[],ref='—';
  try{
    const release=await getRelease();ref=release.sourceCommit.slice(0,12);
    const mainHead=await getMainHead();
    for(const file of CONTRACT.files){
      const [a,b]=await Promise.allSettled([getSource(file,release.sourceCommit),getWWW(file)]);
      const gh=a.status==='fulfilled'?a.value:null,www=b.status==='fulfilled'?b.value:null;
      const r=compareFile(file,release.fileRecords[file],gh,www);
      if(a.status==='rejected'||b.status==='rejected')r.error=(a.status==='rejected'?'SOURCE '+(a.reason?.message||a.reason):'WWW '+(b.reason?.message||b.reason));
      rows.push(r);
    }
    renderRows(rows,release.sourceCommit);
    const html=rows.find(x=>x.file==='index.html');
    const c1=!!html?.gh&&!!html?.www&&isC1Marked(new TextDecoder('utf-8',{fatal:true}).decode(html.gh.raw))&&isC1Marked(new TextDecoder('utf-8',{fatal:true}).decode(html.www.raw));
    const s=classify(rows,true,c1,mainHead);
    const count=rows.filter(x=>x.status==='MATCH').length+' / '+CONTRACT.files.length;
    putStatus(s,count,ref,true);
    const m=$('main-ref');if(m)m.textContent=mainHead?mainHead.slice(0,12):'UNKNOWN';
  } catch(e){renderRows(rows,ref);putStatus({code:'HOLD_RELEASE_BIND',label:'RELEASE-NACHWEIS FEHLT',detail:String(e.message||e).slice(0,220)},'— / 10',ref,true)}
  finally{running=false;$('run').disabled=false;}
}
function refreshPip(){if(!pip||pip.closed){pip=null;return;}const d=pip.document;
  for(const [id,val] of [['pip-code',lastStatus.label],['pip-info',lastStatus.detail],['pip-meta',lastCount+' · '+lastTime+' · '+lastRef]]){const x=d.getElementById(id);if(x)x.textContent=val;}}
function markStale(reason='Browser-Pause / Prüfalter überschritten') {
  if(lastStatus.code==='MATCH_C1')putStatus({code:'STALE',label:'NACHWEIS VERALTET',detail:reason},lastCount,lastRef);
}
function evaluateFreshness(){
  if(statusIsStale(lastCompletedAt,performance.now(),hiddenSinceCheck))markStale();
}
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){hiddenSinceCheck=true;markStale('Browserseite nicht sichtbar; frühere Beobachtung nicht aktuell');}
  else {evaluateFreshness();run();}
});
window.addEventListener('pageshow',e=>{if(e.persisted){hiddenSinceCheck=true;markStale('Wiederhergestellte Seite braucht neue Prüfung');run();}});
$('run').addEventListener('click',()=>run());
$('dock-open').addEventListener('click',()=>{$('dock').hidden=!$('dock').hidden;});
$('dock-close').addEventListener('click',()=>{$('dock').hidden=true;});
$('native-pip').addEventListener('click',async()=>{
  if(!window.documentPictureInPicture?.requestWindow){$('dock').hidden=false;$('dock-info').textContent='Picture-in-Picture nicht unterstützt; eingebettetes Panel aktiv';return;}
  try{
    if(pip&&!pip.closed){pip.focus();return;}
    pip=await window.documentPictureInPicture.requestWindow({width:410,height:290});
    const d=pip.document;d.title='NEXUS · Gate';const css=d.createElement('link');css.rel='stylesheet';css.href=new URL('./gate.css',location.href).href;d.head.append(css);
    const main=el('main','dock');const h=el('h2','','NEXUS · GATE');
    const st=el('p','dock-code',lastStatus.label);st.id='pip-code';
    const desc=el('p','',lastStatus.detail);desc.id='pip-info';
    const meta=el('small','',lastTime+' · C1');meta.id='pip-meta';
    main.append(h,st,desc,meta);d.body.append(main);
    pip.addEventListener('pagehide',()=>pip=null);refreshPip();
  }catch{$('dock').hidden=false;$('dock-info').textContent='PiP nicht verfügbar';}
});
const drag=$('dock').querySelector('.dock-head');let start=null;
drag.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;let b=$('dock').getBoundingClientRect();start={x:e.clientX,y:e.clientY,l:b.left,t:b.top};drag.setPointerCapture(e.pointerId);});
drag.addEventListener('pointermove',e=>{if(!start)return;const d=$('dock');d.style.left=Math.max(0,Math.min(innerWidth-d.offsetWidth,start.l+e.clientX-start.x))+'px';d.style.top=Math.max(0,Math.min(innerHeight-d.offsetHeight,start.t+e.clientY-start.y))+'px';d.style.right='auto';d.style.bottom='auto';});
drag.addEventListener('pointerup',()=>start=null);drag.addEventListener('pointercancel',()=>start=null);
run(true);
setInterval(()=>{evaluateFreshness();if(!document.hidden&&(hiddenSinceCheck||!Number.isFinite(lastCompletedAt)||performance.now()-lastCompletedAt>=CONTRACT.freshnessMs))run();},5000);
