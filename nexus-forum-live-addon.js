/* NEXUS OMEGA / GitHub Forum independent issue+comment lanes.
 * Read-only C1 reference candidate. Never a deploy proof.
 * No token. No writes to GitHub. No `innerHTML`. No untrusted code evaluation.
 */
export const VERSION = 'NEXUS_FORUM_LIVE_ADDON_R9_20261104_C1';
export const REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE';
export const API = `https://api.github.com/repos/${REPO}`;
export const REFRESH_MS = 300000;
export const CHANNELS = Object.freeze({
  issues: '/issues?state=all&sort=updated&direction=desc&per_page=20',
  comments: '/issues/comments?sort=created&direction=desc&per_page=15'
});

const LANE_LABELS = {issues:'Forschung / GitHub-Issues', comments:'GitHub-Issue-Kommentare'};
function safeText(v, limit=350) {return typeof v === 'string' ? v.slice(0,limit) : '';}
function safeTime(v) {if(typeof v!=='string')return null; const n=Date.parse(v);return Number.isFinite(n)?new Date(n).toISOString():null;}
function sameOriginLink(value, kind, id) {
  if (typeof value !== 'string' || !Number.isSafeInteger(id) || id<1) return null;
  try {
    const u=new URL(value);
    if(u.protocol !== 'https:' || u.hostname !== 'github.com' || u.username || u.password || u.port || u.search) return null;
    const parent=`/${REPO}/issues/`;
    if(!u.pathname.startsWith(parent))return null;
    if(kind==='issue') {
      if (u.pathname!==parent+id || u.hash) return null;
    } else {
      if (!/^\d+$/.test(u.pathname.slice(parent.length)) || u.hash!==`#issuecomment-${id}`) return null;
    }
    return u.href;
  } catch {return null;}
}
export function normalize(lane, payload) {
  if(!(lane in CHANNELS) || !Array.isArray(payload))throw new TypeError(`Untrusted API shape: ${lane}`);
  const output=[], seen=new Set();
  for(const row of payload){
    if(!row || typeof row!=='object')continue;
    if(lane==='issues'){
      if(row.pull_request || !Number.isSafeInteger(row.number) || row.number<1)continue;
      const link=sameOriginLink(row.html_url,'issue',row.number);
      const time=safeTime(row.updated_at);
      if(!link||!time||seen.has(row.number))continue;
      seen.add(row.number);
      output.push({kind:'ISSUE',id:row.number,link,time,summary:safeText(row.title,180),author:safeText(row.user?.login,60)});
    } else {
      if(!Number.isSafeInteger(row.id) || row.id<1)continue;
      const link=sameOriginLink(row.html_url,'comment',row.id);
      const time=safeTime(row.created_at);
      if(!link||!time||seen.has(row.id))continue;
      seen.add(row.id);
      output.push({kind:'COMMENT',id:row.id,link,time,summary:safeText(row.body,260),author:safeText(row.user?.login,60)});
    }
  }
  return output;
}
function errorCode(err) {return safeText(String(err?.message||err||'UNKNOWN'),100).replace(/\s+/g,' ');}
export async function readChannel(lane,{fetcher=fetch,now=()=>new Date(),previous=null,timeoutMs=9000}={}){
  if(!(lane in CHANNELS))throw new TypeError('Unknown channel');
  const checked_at=now().toISOString();
  const url=API+CHANNELS[lane];
  const ctl=new AbortController();
  const timeout=setTimeout(()=>ctl.abort(),timeoutMs);
  try {
    // Abort even if the fetcher has not added its own timeout; errors become visible states.
    const response=await fetcher(url,{method:'GET',headers:{'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},redirect:'error',signal:ctl.signal,cache:'no-store'});
    if(!response?.ok)throw new Error(`HTTP_${response?.status??'UNKNOWN'}`);
    const rows=normalize(lane,await response.json());
    return {lane,checked_at,status:'FRESH_READ',source:'GITHUB_API',items:rows,last_success_at:checked_at,error:null};
  }catch(err){
    const keep=(previous?.lane===lane && Array.isArray(previous.items) && previous.status !== 'UNAVAILABLE');
    return {lane,checked_at,status:keep?'STALE_SOURCE_ERROR':'UNAVAILABLE',source:'GITHUB_API',items:keep?previous.items:[],last_success_at:keep?(previous.last_success_at||null):null,error:errorCode(err)};
  }finally{clearTimeout(timeout);}
}
export async function readAll(opts={}){
  const channels={};
  await Promise.all(Object.keys(CHANNELS).map(async lane=>{channels[lane]=await readChannel(lane,{...opts,previous:opts.previous?.channels?.[lane]})}));
  return {version:VERSION,claim:'C1_DESCRIPTIVE_ONLY',channels};
}

export function render(root,snapshot,doc=document){
  if(!root || !doc)throw new TypeError('DOM root required');
  root.replaceChildren();
  const heading=doc.createElement('h2');heading.textContent='Neue GitHub-Forschung und Kommentare';root.appendChild(heading);
  const explain=doc.createElement('p');explain.textContent='Getrennt von main-Commits und Pull Requests. Quellenzeiten sind nicht Veröffentlichungszeiten. C1: Kein Wahrheits- oder Live-Claim aus einem Hash.';root.appendChild(explain);
  for(const lane of Object.keys(CHANNELS)){
    const s=snapshot.channels[lane];if(!s)continue;
    const section=doc.createElement('section');section.dataset.nexusChannel=lane;
    section.setAttribute('aria-label',LANE_LABELS[lane]);
    const h=doc.createElement('h3');h.textContent=LANE_LABELS[lane];section.appendChild(h);
    const state=doc.createElement('p');state.dataset.feedState=lane;
    state.textContent=`${s.status} · Letzter Abruf: ${s.checked_at} · Letzter erfolgreicher Abruf: ${s.last_success_at||'KEINER'}${s.error?' · Fehler: '+s.error:''}`;
    section.appendChild(state);
    const ul=doc.createElement('ul');ul.dataset.feedList=lane;
    for(const item of s.items){
      const li=doc.createElement('li');li.dataset.sourceId=String(item.id);
      const a=doc.createElement('a');a.href=item.link;a.rel='noopener noreferrer';a.textContent=`${item.kind} #${item.id} · ${item.summary||'Kein Text'}`;
      const time=doc.createElement('time');time.dateTime=item.time;time.textContent=` · GitHub-Quellenzeit: ${item.time}`;
      li.appendChild(a);li.appendChild(time);ul.appendChild(li);
    }
    if(!s.items.length){const li=doc.createElement('li');li.textContent=s.status==='FRESH_READ'?'Keine Treffer in dieser API-Antwort':'Keine belegbaren aktuellen Daten';ul.appendChild(li);}
    section.appendChild(ul);root.appendChild(section);
  }
}

export function createController({doc=document,fetcher=fetch,scheduler=setInterval,unschedule=clearInterval,now=()=>new Date()}={}){
  let root=doc.getElementById('nexus-forum-live-addon');
  if(!root){root=doc.createElement('section');root.id='nexus-forum-live-addon';root.setAttribute('aria-label','Aktuelle GitHub-Forschungsaktivität');
    // The owner must verify this exact placement against the real deployed DOM before release.
    (doc.querySelector('main')||doc.body).appendChild(root);
  }
  let previous=null,inFlight=false,stopped=false;
  async function refresh(){
    if(stopped || inFlight)return;
    inFlight=true;
    try{const snapshot=await readAll({fetcher,now,previous});if(!stopped){render(root,snapshot,doc);previous=snapshot;}}
    finally{inFlight=false;}
  }
  const interval=scheduler(()=>{void refresh();},REFRESH_MS);
  const ready=refresh();
  return {ready,refresh,stop(){stopped=true;unschedule(interval);},getSnapshot(){return previous;}};
}
// Importing this module from the owner's exact page auto-mounts only in a real browser.
if(typeof window!=='undefined' && typeof document!=='undefined' && window.location?.pathname?.startsWith('/forum/github-implant/')){
  createController();
}
