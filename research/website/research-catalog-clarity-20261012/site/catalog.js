"use strict";
/* NEXUS OMEGA · public-science directory view · SPDX-License-Identifier: Apache-2.0
   Displays existing canonical /research/catalog.json; never writes or promotes sources. */
(() => {
  const PUBLIC_SOURCE = "/research/catalog.json";
  const SNAPSHOT = "./catalog-snapshot.json";
  const MAX_BYTES = 180000;
  const MAX_RECORDS = 500;
  const TYPE_LABELS = Object.freeze({
    SCIENTIFIC_RESULT:"Forschungsresultat",
    ENGINEERING_RESULT:"Technischer Befund",
    NEGATIVE_RESULT:"Negativer Befund",
    OPEN_STATUS:"Offener Status"
  });
  const KNOWN = Object.keys(TYPE_LABELS);
  const $ = id => document.getElementById(id);
  const typeOptions = [...document.querySelectorAll(".types button")];
  const state = {data:[],filtered:[],kind:"",query:"",order:"newest",withheld:0,source:"NONE"};
  function make(tag,cls,text) {
    const el=document.createElement(tag);if(cls)el.className=cls;
    if(text!==undefined)el.textContent=String(text);return el;
  }
  function safeHref(path) {
    if(typeof path!=="string" || !/^\/research\/record\/[a-z0-9-]+\/$/.test(path)) return "/research/";
    return path;
  }
  function safeEntry(raw) {
    if(!raw||typeof raw!=="object"||!KNOWN.includes(raw.PUBLICATION_CLASS)||
        typeof raw.PUBLIC_ID!=="string"||!/^[a-z0-9-]{1,110}$/.test(raw.PUBLIC_ID)||
        typeof raw.TITLE!=="string"||raw.TITLE.length>250||
        typeof raw.href!=="string"||safeHref(raw.href)!==raw.href||
        raw.CLAIM_CEILING!=="C1_DESCRIPTIVE_ONLY") return null;
    return {
      id:raw.PUBLIC_ID,title:raw.TITLE,
      type:raw.PUBLICATION_CLASS,
      evidence:typeof raw.EVIDENCE_STATE==="string"?raw.EVIDENCE_STATE.slice(0,120):"NOT_ESTABLISHED",
      date:typeof raw.DATE==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(raw.DATE)?raw.DATE:"",
      href:raw.href
    };
  }
  function setFreshness(ok,summary,note,dataDate) {
    $("source-dot").className="source-dot "+(ok?"ok":"warn");
    $("data-status").textContent=summary;
    $("source-detail").textContent=note;
    $("source-date").textContent=dataDate;
  }
  async function jsonFrom(url) {
    const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),9000);
    try {
      const response=await fetch(url,{cache:"no-store",credentials:"omit",signal:controller.signal,headers:{Accept:"application/json"}});
      if(!response.ok)throw new Error("HTTP "+response.status);
      const declared=Number(response.headers.get("Content-Length")||0);
      if(declared>MAX_BYTES)throw new Error("Katalog zu groß");
      const text=await response.text();
      if(new TextEncoder().encode(text).byteLength>MAX_BYTES)throw new Error("Katalog zu groß");
      return JSON.parse(text);
    } finally {clearTimeout(timeout)}
  }
  function intake(data) {
    if(!data||data.claim_ceiling!=="C1_DESCRIPTIVE_ONLY"||!Array.isArray(data.records)||
        data.records.length>MAX_RECORDS || data.claim_promotion===true) throw new Error("Katalogvertrag verletzt");
    const seen=new Set();const items=[];
    for(const raw of data.records){
      const entry=safeEntry(raw);
      if(!entry||seen.has(entry.id))throw new Error("Nicht zulässiger oder doppelter Record im Katalog");
      seen.add(entry.id);items.push(entry);
    }
    return {entries:items,withheld:Number.isInteger(data.withheld_count)&&data.withheld_count>=0?data.withheld_count:0,generatedAt:data.generated_at||"unbekannt"};
  }
  function counters() {
    const n=type=>state.data.filter(x=>x.type===type).length;
    $("total").textContent=String(state.data.length).padStart(2,"0");
    $("n-all").textContent=state.data.length;
    $("n-science").textContent=n("SCIENTIFIC_RESULT");
    $("n-engineering").textContent=n("ENGINEERING_RESULT");
    $("n-negative").textContent=n("NEGATIVE_RESULT");
    $("n-open").textContent=n("OPEN_STATUS");
    $("withheld-count").textContent=state.withheld+" separat";
    typeOptions.forEach(btn=>{
      const chosen=btn.dataset.kind===state.kind;
      btn.classList.toggle("chosen",chosen);
      btn.setAttribute("aria-pressed",String(chosen));
    });
    $("type").value=state.kind;
  }
  function row(rec) {
    const article=make("article","record");
    const left=make("div","record-main");
    const title=make("a","record-title",rec.title);
    title.href=rec.href;
    const sub=make("div","record-sub");
    sub.append(make("span","",rec.id));
    if(rec.date)sub.append(make("span","",rec.date));
    left.append(title,sub);
    const middle=make("div","record-class");
    const pill=make("span","pill "+(rec.type==="NEGATIVE_RESULT"?"negative":rec.type==="OPEN_STATUS"?"open":""),TYPE_LABELS[rec.type]);
    const st=make("span","state-name",rec.evidence.replaceAll("_"," ").toLocaleLowerCase("de-DE"));
    middle.append(pill,st);
    const href=make("a","record-link","RECORD ↗");href.href=rec.href;
    article.append(left,middle,href);return article;
  }
  function render() {
    const q=state.query.toLocaleLowerCase("de-DE").trim();
    const current=state.data.filter(x=>(!state.kind||x.type===state.kind)&&
       (!q||[x.title,x.id,x.type,x.evidence].some(t=>t.toLocaleLowerCase("de-DE").includes(q))));
    const date=s=>s.date||"0000-00-00";
    current.sort((a,b)=>state.order==="name"?a.title.localeCompare(b.title,"de"):
      state.order==="oldest"?date(a).localeCompare(date(b))||a.id.localeCompare(b.id):
        date(b).localeCompare(date(a))||a.id.localeCompare(b.id));
    state.filtered=current;
    const list=$("records");list.replaceChildren();
    if(!current.length){
      const e=make("p","empty",state.data.length?"Keine Treffer für diese Filter.":"Keine überprüfbaren Records verfügbar.");
      list.append(e);
    }else for(const rec of current)list.append(row(rec));
    $("shown").textContent=current.length+" von "+state.data.length+" Records · C1_DESCRIPTIVE_ONLY";
    counters();updateUrl();
  }
  function updateUrl(){
    const qs=new URLSearchParams();
    if(state.query)qs.set("q",state.query.slice(0,100));
    if(state.kind)qs.set("type",state.kind);
    if(state.order!=="newest")qs.set("order",state.order);
    const query=qs.toString();
    try{history.replaceState(null,"",location.pathname+(query?"?"+query:"")+location.hash)}catch{}
  }
  function fromUrl(){
    const q=new URLSearchParams(location.search);
    state.query=(q.get("q")||"").slice(0,100);
    state.kind=KNOWN.includes(q.get("type"))?q.get("type"):"";
    state.order=["newest","oldest","name"].includes(q.get("order"))?q.get("order"):"newest";
    $("q").value=state.query;$("order").value=state.order;
  }
  async function initialize(){
    fromUrl();
    let src=null,canonicalError=null;
    try {
      const data=await jsonFrom(PUBLIC_SOURCE);
      src=intake(data);state.source="CANONICAL_WWW";
      setFreshness(true,"KANONISCHER KATALOG","Öffentliche Quelle aktuell abgerufen · keine Validitäts-Promotion","QUELLE · "+String(src.generatedAt).slice(0,19));
    }catch(err){canonicalError=err;
      try{
        const data=await jsonFrom(SNAPSHOT);
        src=intake(data);state.source="ARCHIVE_SNAPSHOT";
        setFreshness(false,"ARCHIV-SNAPSHOT · NICHT LIVE",
          "Live-Katalog nicht verfügbar ("+String(err.message||"Quelle fehlt").slice(0,90)+") · historische Kopie",
          "SNAPSHOT · 2026-09-22");
      }catch{
        setFreshness(false,"KATALOG NICHT VERFÜGBAR","Weder Live-Quelle noch referenzierter Snapshot zugänglich","SOURCE GAP · C1");
        const list=$("records");list.replaceChildren();const p=make("p","empty","Die Quellendaten konnten nicht geladen werden. ");
        const l=make("a","","Originaldaten direkt aufrufen ↗");l.href=PUBLIC_SOURCE;p.append(l);list.append(p);
        return;
      }
    }
    state.data=src.entries;state.withheld=src.withheld;render();
  }
  $("q").addEventListener("input",e=>{state.query=e.target.value.slice(0,100);render()});
  $("type").addEventListener("change",e=>{state.kind=KNOWN.includes(e.target.value)?e.target.value:"";render()});
  $("order").addEventListener("change",e=>{state.order=e.target.value;render()});
  typeOptions.forEach(btn=>btn.addEventListener("click",()=>{state.kind=btn.dataset.kind;render()}));
  $("reset").addEventListener("click",()=>{state.kind="";state.query="";state.order="newest";$("q").value="";$("order").value="newest";render()});
  window.addEventListener("popstate",()=>{fromUrl();render()});
  initialize();
})();