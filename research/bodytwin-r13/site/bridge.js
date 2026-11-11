import {RULE,RESEARCH,validatePublicState,freshness} from './bridge-core.mjs';
const byId=id=>document.getElementById(id);
const put=(id,value)=>{const x=byId(id);if(x)x.textContent=String(value);};
let last=null,when=NaN,hidden=false,running=false;
function show(){const state=freshness(last,performance.now()-when,hidden);put('source-state',state);put('source-explainer',state==='PUBLIC_STATUS_OBSERVED_C1'?'Öffentliche Metadaten beobachtet. Keine Sensormessung und kein unabhängiger Zeitzeuge.':state==='STALE_UNVERIFIED'?'Browser-Beobachtung veraltet oder verborgen; eine neue Prüfung ist notwendig.':'Keine verifizierbare aktuelle öffentliche Metadatenantwort.');}
async function refresh(){
 if(running)return;running=true;put('source-state','GET_PENDING');
 const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),10000);
 try{
 const response=await fetch(RULE.source,{method:'GET',cache:'no-store',credentials:'omit',redirect:'error',signal:ctl.signal,headers:{Accept:'application/json'}});
 if(!response.ok)throw Error('HTTP_'+response.status);
 const len=Number(response.headers.get('Content-Length')||0);if(len>RULE.maxBytes)throw Error('SIZE_LIMIT');
 const bytes=await response.arrayBuffer();if(!bytes.byteLength||bytes.byteLength>RULE.maxBytes)throw Error('SIZE_INVALID');
 const raw=new TextDecoder('utf-8',{fatal:true}).decode(bytes);
 last=validatePublicState(JSON.parse(raw));when=performance.now();hidden=false;
 put('body-state',last.state);put('consent-state',last.consent);put('trial-state',last.trial);
 put('observed-device','GET · Geräteuhr ungeprüft · '+new Date().toLocaleString('de-DE'));
 }catch(e){last=null;when=NaN;put('observed-device','SOURCE_GAP · '+String(e?.message||e).slice(0,85));}
 finally{clearTimeout(timer);running=false;show();}
}
put('chain-status',RESEARCH.chain);put('pdf-status',RESEARCH.qwenPdf);put('a72-status',RESEARCH.a72);
byId('refresh').addEventListener('click',refresh);
document.addEventListener('visibilitychange',()=>{if(document.hidden){hidden=true;show();}else{show();refresh();}});
window.addEventListener('pageshow',e=>{if(e.persisted){hidden=true;show();refresh();}});
setInterval(show,10000);
refresh();
