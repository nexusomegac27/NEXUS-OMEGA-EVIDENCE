/* NEXUS GATE · Browser-only Security+Science transport monitor · SPDX-License-Identifier: Apache-2.0 */
import {CONTRACT,parseGitHubContent,digest,classify,isC1Marked} from "./gate-core.mjs";
const ROOT="https://api.github.com/repos/"+CONTRACT.repository;
const INTERVAL=30*60*1000,CLICK_COOLDOWN=60000,MAX_BYTES=600000;
const $=(id)=>document.getElementById(id);
let lastStart=0,lastStatus={code:"NO_OBSERVATION",label:"NO OBSERVATION",detail:"Noch keine Prüfung durchgeführt"},lastCount="— / 3",lastTime="Nicht geprüft",lastHead="—",running=false,pip=null;
function mk(name,cls,txt){let e=document.createElement(name);if(cls)e.className=cls;if(txt!==undefined)e.textContent=String(txt);return e}
function when(d){return new Intl.DateTimeFormat("de-DE",{dateStyle:"medium",timeStyle:"short",timeZone:"Europe/Berlin"}).format(d)}
function sourceURL(file){return "https://github.com/"+CONTRACT.repository+"/blob/main/"+CONTRACT.sourceRoot+file}
function siteURL(file){return new URL("../"+file,location.href).href}
function emit(status,count,head) {
 lastStatus=status;lastCount=count;lastTime=when(new Date());lastHead=head;
 $("verdict").textContent=status.label;$("verdict-desc").textContent=status.detail;$("match-counter").textContent=count;
 $("timestamp").textContent=lastTime;$("head").textContent="SOURCE HEAD · "+head;
 $("dot").className="status-indicator "+(status.code==="MATCH_C1"?"ok":status.code==="DIVERGENCE"?"fail":"warn");
 $("dock-status").textContent=status.label;$("dock-info").textContent=status.detail;$("dock-time").textContent="C1 · "+lastTime;
 refreshPip();
}
async function fetchSource(file){
 const controller=new AbortController(),abort=setTimeout(()=>controller.abort(),10000);
 try{
  const p=CONTRACT.sourceRoot+file;
  const u=ROOT+"/contents/"+p.split("/").map(encodeURIComponent).join("/")+"?ref=main";
  const r=await fetch(u,{signal:controller.signal,cache:"no-store",credentials:"omit",referrerPolicy:"no-referrer",headers:{Accept:"application/vnd.github+json"}});
  if(!r.ok)throw new Error("GitHub HTTP "+r.status);
  const meta=await r.json();
  const bytes=parseGitHubContent(meta);
  if(bytes.byteLength>MAX_BYTES)throw new Error("GitHub-Datei überschreitet Prüfgrenze");
  return {sha:await digest(bytes),bytes:bytes.byteLength,raw:bytes};
 }finally{clearTimeout(abort)}
}
async function fetchLive(file){
 const controller=new AbortController(),abort=setTimeout(()=>controller.abort(),10000);
 try{
  const r=await fetch(siteURL(file),{signal:controller.signal,cache:"no-store",credentials:"omit",redirect:"error"});
  if(!r.ok)throw new Error("WWW HTTP "+r.status);
  const size=Number(r.headers.get("Content-Length")||0);
  if(size>MAX_BYTES)throw new Error("WWW-Datei überschreitet Prüfgrenze");
  const bytes=new Uint8Array(await r.arrayBuffer());
  if(bytes.length>MAX_BYTES)throw new Error("WWW-Datei überschreitet Prüfgrenze");
  return {sha:await digest(bytes),bytes:bytes.byteLength,raw:bytes};
 }finally{clearTimeout(abort)}
}
function showRows(rows) {
 const list=$("files");list.replaceChildren();
 for (const row of rows){
  const el=mk("article","file-row"),left=mk("div"),name=mk("a","",row.file);
  name.href=sourceURL(row.file);name.rel="noopener noreferrer";name.target="_blank";
  left.append(name);
  left.append(mk("p","",row.github?"GITHUB · "+row.github.sha.slice(0,18)+"… · "+row.github.bytes+" B":"GITHUB · QUELLE NICHT ERREICHBAR"));
  left.append(mk("p","",row.web?"NEXUS · "+row.web.sha.slice(0,18)+"… · "+row.web.bytes+" B":"NEXUS · NICHT BEOBACHTBAR"));
  if(row.error)left.append(mk("p","",row.error));
  el.append(left,mk("span","file-state "+row.status.toLowerCase(),row.status));list.append(el);
 }
}
async function sourceHead(){
 const ctrl=new AbortController(),timer=setTimeout(()=>ctrl.abort(),7000);
 try{
  const r=await fetch(ROOT+"/commits?sha=main&per_page=1",{signal:ctrl.signal,credentials:"omit",cache:"no-store",headers:{Accept:"application/vnd.github+json"}});
  if(!r.ok)return "HEAD UNBEKANNT";
  const z=await r.json();return Array.isArray(z)&&typeof z[0]?.sha==="string"?z[0].sha.slice(0,10):"HEAD UNBEKANNT";
 }catch{return "HEAD UNBEKANNT"}finally{clearTimeout(timer)}
}
async function run(){
 if(running||Date.now()-lastStart<CLICK_COOLDOWN)return;
 if(!globalThis.crypto?.subtle){emit({code:"HOLD_CRYPTO",label:"KRYPTOGRAFIE NICHT VERFÜGBAR",detail:"SHA-256-WebCrypto benötigt einen sicheren HTTPS-Kontext"},"— / 3","—");return}
 running=true;lastStart=Date.now();$("run").disabled=true;$("verdict").textContent="PRÜFUNG LÄUFT";$("verdict-desc").textContent="Zwei unabhängige HTTP-Abfragen je Datei …";
 const rows=[],head=await sourceHead();
 try{
  for(const file of CONTRACT.files){
   const [g,w]=await Promise.allSettled([fetchSource(file),fetchLive(file)]);
   const gh=g.status==="fulfilled"?g.value:null,web=w.status==="fulfilled"?w.value:null;
   const status=!gh?"SOURCE_GAP":!web?"ERROR":gh.sha===web.sha&&gh.bytes===web.bytes?"MATCH":"DIVERGENT";
   rows.push({file,github:gh,web,status,error:g.status==="rejected"?"GitHub: "+String(g.reason.message||g.reason):w.status==="rejected"?"WWW: "+String(w.reason.message||w.reason):null});
  }
  showRows(rows);
  const valid=rows.find(x=>x.file==="index.html"),decoder=new TextDecoder("utf-8");
  const scienceOK=!!valid?.github&&!!valid?.web&&isC1Marked(decoder.decode(valid.github.raw))&&isC1Marked(decoder.decode(valid.web.raw));
  const ok=rows.every(x=>x.github);
  const result=classify(rows,ok,scienceOK);
  const count=rows.filter(x=>x.status==="MATCH").length+" / 3";
  emit(result,count,head);
 }catch(err){emit({code:"HOLD_SCOPE",label:"PRÜFUNG UNVOLLSTÄNDIG",detail:String(err.message||err)},"— / 3",head)}
 finally{running=false;$("run").disabled=false}
}
function refreshPip(){
 if(!pip||pip.closed){pip=null;return}
 const d=pip.document;
 const code=d.getElementById("pip-code"),info=d.getElementById("pip-info"),meta=d.getElementById("pip-meta");
 if(code)code.textContent=lastStatus.label;
 if(info)info.textContent=lastStatus.detail;
 if(meta)meta.textContent=lastCount+" · "+lastTime+" · "+lastHead+" · C1";
}
$("run").addEventListener("click",run);
$("dock-open").addEventListener("click",()=>{const d=$("dock");d.hidden=!d.hidden;if(!d.hidden)refreshPip()});
$("dock-close").addEventListener("click",()=>{$("dock").hidden=true});
$("native-pip").addEventListener("click",async()=>{
 if(!window.documentPictureInPicture?.requestWindow){$("dock").hidden=false;$("dock-info").textContent="Echtes Dokument-PiP wird hier nicht unterstützt. Eingebettetes Schwebefenster aktiv.";return}
 try {
  if(pip&&!pip.closed){pip.focus();return}
  const w=await window.documentPictureInPicture.requestWindow({width:410,height:300});
  pip=w;w.document.title="NEXUS · Gate";
  const style=w.document.createElement("link");style.rel="stylesheet";style.href=new URL("./gate.css",location.href).href;w.document.head.append(style);
  const main=w.document.createElement("main");main.className="dock";
  // PiP CSS override via class names; only text nodes from local status, never remote HTML.
  const heading=mk("h2","","NEXUS · GATE");const code=mk("p","dock-code",lastStatus.label);code.id="pip-code";
  const info=mk("p","",lastStatus.detail);info.id="pip-info";
  const meta=mk("small","",lastTime+" · C1");meta.id="pip-meta";
  main.append(heading,code,info,meta);w.document.body.append(main);
  w.addEventListener("pagehide",()=>{if(pip===w)pip=null});
  refreshPip();
 }catch(e){$("dock").hidden=false;$("dock-info").textContent="Externes PiP-Fenster nicht verfügbar · eingebettete Ansicht aktiv"}
});
const drag=$("dock").querySelector(".dock-head");let start=null;
drag.addEventListener("pointerdown",evt=>{
 if(evt.target.closest("button"))return;
 const rect=$("dock").getBoundingClientRect();start={x:evt.clientX,y:evt.clientY,l:rect.left,t:rect.top};drag.setPointerCapture(evt.pointerId);
});
drag.addEventListener("pointermove",evt=>{
 if(!start)return;
 const panel=$("dock"),x=Math.max(0,Math.min(innerWidth-panel.offsetWidth,start.l+evt.clientX-start.x)),y=Math.max(0,Math.min(innerHeight-panel.offsetHeight,start.t+evt.clientY-start.y));
 panel.style.left=x+"px";panel.style.top=y+"px";panel.style.right="auto";panel.style.bottom="auto";
});
drag.addEventListener("pointerup",()=>{start=null});
drag.addEventListener("pointercancel",()=>{start=null});
run();
setInterval(()=>{if(!document.hidden&&Date.now()-lastStart>=INTERVAL)run()},INTERVAL);
