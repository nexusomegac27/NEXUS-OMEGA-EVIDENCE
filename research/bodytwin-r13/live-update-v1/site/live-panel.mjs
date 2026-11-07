/* NEXUS OMEGA Bodytwin, public same-origin status only. No sensors. */
import {RULE,validateFeed,classifyFreshness,checkSequence} from './live-core.mjs';
const NS='bt-live-';
const el=(tag,cl='',txt)=>{const x=document.createElement(tag);if(cl)x.className=cl;if(txt!==undefined)x.textContent=String(txt);return x};
const item=(parent,kind,id,label,value)=>{const box=el('div',kind),head=el('small','bt-live-label',label),body=el('strong','bt-live-value',value);body.id=NS+id;box.append(head,body);parent.append(box);return body};
const main=document.querySelector('main')||document.body;
const section=el('section','bt-live-panel');section.id='nexus-bodytwin-live-c1';section.setAttribute('aria-labelledby','bt-live-title');
const header=el('div','bt-live-header'),titles=el('div');
const eye=el('div','bt-live-eyebrow','NEXUS OMEGA · PUBLIC EVIDENCE · C1_DESCRIPTIVE_ONLY');
const title=el('h2','bt-live-title','Bodytwin · live abgeglichener Forschungsstand');title.id='bt-live-title';
const sub=el('p','bt-live-sub','Öffentliche Zustände werden automatisch abgefragt. Abruf ≠ neue Messung ≠ wissenschaftliche Validierung.');
titles.append(eye,title,sub);
const controls=el('div','bt-live-controls');
const refreshButton=el('button','bt-live-refresh','Jetzt prüfen');refreshButton.type='button';
const liveState=el('span','bt-live-status','NO_OBSERVATION');liveState.id=NS+'status';liveState.setAttribute('aria-live','polite');
controls.append(liveState,refreshButton);header.append(titles,controls);section.append(header);
const grid=el('div','bt-live-grid');
item(grid,'bt-live-card','bodytwin','Bodytwin wissenschaftlich validiert','UNKNOWN');
item(grid,'bt-live-card','consent','Consent-Bindung','UNKNOWN');
item(grid,'bt-live-card','trial','Trial 001','UNKNOWN');
item(grid,'bt-live-card','node','R14-R2R1 · Windows Node','—');
item(grid,'bt-live-card','mutation','Mutationstests','—');
item(grid,'bt-live-card','schema','JSON-Schema-Negativtests','—');
section.append(grid);
const footer=el('div','bt-live-footer');
item(footer,'bt-live-foot','producer','Letzte Hostinger-Feed-Erzeugung','NOT_OBSERVED');
item(footer,'bt-live-foot','changes','Letzte echte Datenquellenänderung','NOT_OBSERVED');
item(footer,'bt-live-foot','poll','Letzter Abruf (lokale Geräteuhr)','NOT_OBSERVED');
item(footer,'bt-live-foot','seq','Reducer-Sequenz','—');
item(footer,'bt-live-foot','gateway','Governance','HOLD');
section.append(footer);
const notice=el('p','bt-live-notice','Keine physische Sensoraufnahme. C1-Recherche, kein klinischer Befund. Zeitangaben der Geräteuhr sind nicht unabhängig attestiert.');
const sourceLink=el('a','','Quellenstatus öffnen');sourceLink.href='/research/bodytwin/state.json';sourceLink.rel='noopener noreferrer';
const researchLink=el('a','','R13-Forschungsbrücke');researchLink.href='/bodytwin/r13/';researchLink.rel='noopener noreferrer';
notice.append(' ',sourceLink,' · ',researchLink);section.append(notice);
main.insertBefore(section,main.firstChild);
const put=(id,value)=>{const x=document.getElementById(NS+id);if(x)x.textContent=String(value)};
let running=false,last=null,lastSeq=null,hidden=document.hidden,ever=false;
function setStatus(code){put('status',code);section.dataset.status=code.startsWith('PUBLIC')?'ok':'hold';}
function render(f){
 put('bodytwin',f.bodytwin.validated+' · '+f.bodytwin.state);
 put('consent',f.bodytwin.consent);
 put('trial',f.bodytwin.trial);
 put('node',f.research.node_pass+'/'+f.research.node_total+' · Cursor-Receipt');
 put('mutation',f.research.mutation_pass+'/'+f.research.mutation_total);
 put('schema',f.research.schema_pass+'/'+f.research.schema_total);
 put('producer',f.producer.run_utc+' (Hostzeit, unbeglaubigt)');
 put('changes',f.producer.last_change_utc+(f.producer.source_changed?' · QUELLBYTES GEÄNDERT':' · QUELLBYTES UNVERÄNDERT'));
 put('seq',String(f.producer.seq));
 put('gateway',f.gates.a72+' · '+f.gates.r13_stage_ii+' · '+f.gates.gate_v2);
}
function staleGuard(){if(!last){setStatus('HOLD_NO_FEED');return;}const status=classifyFreshness(last,Date.now(),document.hidden);
 if(status!=='PUBLIC_REFRESH_OBSERVED_C1')setStatus(status);
}
async function refresh(){
 if(running||document.hidden)return;
 running=true;refreshButton.disabled=true;setStatus('GET_PENDING');
 const abort=new AbortController();const timer=setTimeout(()=>abort.abort(),RULE.requestTimeoutMilliseconds);
 try{
  const r=await fetch(RULE.endpoint,{method:'GET',mode:'same-origin',cache:'no-store',credentials:'omit',redirect:'error',referrerPolicy:'no-referrer',headers:{Accept:'application/json'},signal:abort.signal});
  if(!r.ok)throw Error('HTTP_'+r.status);
  const contentType=r.headers.get('Content-Type')||'';if(!/\bapplication\/json\b/i.test(contentType))throw Error('INVALID_JSON_MIME');
  const n=Number(r.headers.get('Content-Length')||0);if(n>RULE.maxResponseBytes)throw Error('RESPONSE_TOO_LARGE');
  const bytes=await r.arrayBuffer();if(!bytes.byteLength||bytes.byteLength>RULE.maxResponseBytes)throw Error('BAD_RESPONSE_BYTES');
  const content=new TextDecoder('utf-8',{fatal:true}).decode(bytes);
  const candidate=validateFeed(JSON.parse(content));
  const freshness=classifyFreshness(candidate,Date.now(),document.hidden);
  if(freshness!=='PUBLIC_REFRESH_OBSERVED_C1')throw Error(freshness);
  const seq=checkSequence(lastSeq,candidate.producer.seq);
  if(seq==='HOLD_SEQUENCE_ROLLBACK'||seq==='HOLD_INVALID_SEQUENCE')throw Error(seq);
  last=candidate;lastSeq=candidate.producer.seq;ever=true;render(last);
  put('poll',new Date().toLocaleString('de-DE')+' · nur Geräteuhr');
  setStatus('PUBLIC_REFRESH_OBSERVED_C1 · '+seq);
 }catch(error){
  setStatus('HOLD_'+String(error?.message||error).slice(0,78));
  if(!ever)put('poll','SOURCE_NOT_OBSERVED');
 }finally{clearTimeout(timer);running=false;refreshButton.disabled=false;}
}
refreshButton.addEventListener('click',refresh);
document.addEventListener('visibilitychange',()=>{hidden=document.hidden;if(hidden){setStatus('HOLD_TAB_HIDDEN');return;}staleGuard();refresh();});
window.addEventListener('pageshow',event=>{if(event.persisted){setStatus('HOLD_RESTORED_PAGE');refresh();}});
setInterval(()=>{staleGuard();if(!document.hidden)refresh();},RULE.refreshMilliseconds);
refresh();
