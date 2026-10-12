"use strict";
/* NEXUS GitHub Implant · read-only public API · C1_DESCRIPTIVE_ONLY
 * SPDX-License-Identifier: MIT
 * No tokens, credentials, trackers, third-party scripts, or HTML injection.
 */
(() => {
  const ORIGIN = "https://api.github.com";
  const OWNER = "nexusomegac27";
  const REPO = "NEXUS-OMEGA-EVIDENCE";
  const ENDPOINT = "/repos/" + OWNER + "/" + REPO;
  const REFRESH_MS = 300000;
  const MIN_REQUEST_INTERVAL_MS = 60000;
  const MAX_PREVIEW_BYTES = 150000;
  const cache = new Map();
  const state = {active:"commits",directory:"",files:[],lastUpdate:0,lastSuccess:0,commitsLoaded:false};
  const byId = (id) => document.getElementById(id);
  const repoPage = "https://github.com/" + OWNER + "/" + REPO;
  const safePage = (url) => {
    try {
      const p = new URL(url);
      return p.origin === "https://github.com" && p.pathname.startsWith("/" + OWNER + "/" + REPO + "/") ? p.href : repoPage;
    } catch (_) { return repoPage; }
  };
  const node = (tag, className, value) => {
    const n = document.createElement(tag);
    if (className) n.className = className;
    if (value !== undefined) n.textContent = String(value);
    return n;
  };
  const link = (label, url, className) => {
    const el = node("a", className, label);
    el.href = safePage(url);
    el.target = "_blank"; el.rel = "noopener noreferrer";
    return el;
  };
  const shortSha = (sha) => typeof sha === "string" ? sha.slice(0, 10) : "—";
  const dateText = (v) => {
    if (!v || Number.isNaN(new Date(v).getTime())) return "Zeit unbekannt";
    return new Intl.DateTimeFormat("de-DE", {dateStyle:"medium", timeStyle:"short", timeZone:"Europe/Berlin"}).format(new Date(v)) + " MEZ/MESZ";
  };
  const message = (target, text, type = "empty") => {
    const e = byId(target); e.replaceChildren(node("p", type, text));
  };
  function status(ok, text) {
    byId("live-dot").className = "status-dot " + (ok ? "ok" : "warn");
    byId("live-label").textContent = ok ? "GITHUB ERREICHBAR" : "LIVE-STATUS UNBEKANNT";
    byId("live-message").textContent = text;
    if (ok) state.lastSuccess = Date.now();
    byId("last-sync").textContent = state.lastSuccess ?
      "Letzter erfolgreicher Abruf: " + dateText(new Date(state.lastSuccess).toISOString()) :
      "Noch kein erfolgreicher API-Abruf";
  }
  async function getJson(path, refresh = false) {
    if (!path.startsWith(ENDPOINT)) throw new Error("Unzulässiger API-Pfad");
    const now = Date.now();
    const previous = cache.get(path);
    if (previous && now - previous.time < (refresh ? MIN_REQUEST_INTERVAL_MS : REFRESH_MS)) return previous.data;
    const ctrl = new AbortController();
    const timeout = setTimeout(() => ctrl.abort(), 11000);
    try {
      const headers = {Accept:"application/vnd.github+json"}; // Avoid CORS preflight on version header
      if (previous && previous.etag) headers["If-None-Match"] = previous.etag;
      const r = await fetch(ORIGIN + path, {headers, signal:ctrl.signal, credentials:"omit", referrerPolicy:"no-referrer", cache:"no-store"});
      if (r.status === 304 && previous) {
        cache.set(path, {...previous, time:Date.now()});
        status(true, "Unverändert · ETag bestätigt");
        return previous.data;
      }
      if (!r.ok) {
        const code = r.status;
        if (code === 403 || code === 429) throw new Error("GitHub API-Limit / Zugriff (" + code + "). Bitte später erneut versuchen.");
        throw new Error("GitHub API antwortet mit HTTP " + code);
      }
      const data = await r.json();
      cache.set(path, {time:Date.now(), data, etag:r.headers.get("ETag")});
      const remaining = r.headers.get("X-RateLimit-Remaining");
      status(true, remaining !== null ? "API antwortet · verbleibendes Limit: " + remaining : "Live-Antwort von GitHub");
      return data;
    } catch (e) {
      status(false, e.name === "AbortError" ? "API-Zeitlimit erreicht" : (e.message || "Netzfehler"));
      if (previous) return previous.data; // previous cached response is NOT a new live observation
      throw e;
    } finally { clearTimeout(timeout); }
  }
  async function loadCommits(force = false) {
    const e = byId("commit-feed");
    if (!state.commitsLoaded) message("commit-feed", "GitHub-Chronik wird geladen …", "loading");
    try {
      const list = await getJson(ENDPOINT + "/commits?sha=main&per_page=15", force);
      if (!Array.isArray(list)) throw new Error("Unerwartetes GitHub-Format");
      e.replaceChildren();
      byId("commit-count").textContent = String(list.length).padStart(2, "0");
      if (list.length) {
        byId("head-short").textContent = shortSha(list[0].sha);
        byId("head-date").textContent = dateText(list[0].commit?.committer?.date);
      }
      list.forEach((item, index) => {
        const row = node("article","feed-item");
        const left = node("div","feed-main");
        const subject = String(item.commit?.message || "Unbenannter Commit").split("\n")[0].slice(0, 240);
        left.append(link(subject, item.html_url, "feed-title"));
        left.append(node("p","feed-sub", (item.commit?.author?.name || "Unbekannte Herkunft") + " · " + dateText(item.commit?.committer?.date)));
        const right = node("div","feed-meta");
        if (index === 0) right.append(node("span","hash-tag","HEAD"));
        right.append(link(shortSha(item.sha) + " ↗",item.html_url,"hash-tag"));
        row.append(left,right);e.append(row);
      });
      if (!list.length) message("commit-feed","Keine Main-Commits gefunden.");
      state.commitsLoaded = true;
    } catch (err) { message("commit-feed", err.message, "error"); }
  }
  async function loadPRs(force = false) {
    message("pr-feed","Pull Requests werden geladen …","loading");
    try {
      const list = await getJson(ENDPOINT + "/pulls?state=all&sort=updated&direction=desc&per_page=20", force);
      if (!Array.isArray(list)) throw new Error("Unerwartetes GitHub-Format");
      const e = byId("pr-feed");e.replaceChildren();
      list.forEach(item => {
        const row=node("article","feed-item"), left=node("div","feed-main");
        left.append(link("#" + item.number + " · " + String(item.title || "Ohne Titel").slice(0,220),item.html_url,"feed-title"));
        left.append(node("p","feed-sub","Aktualisiert " + dateText(item.updated_at)));
        const stateText=item.merged_at?"MERGED":item.state==="open"?"OPEN":"CLOSED";
        row.append(left,node("span","pr-state "+stateText.toLowerCase(),stateText));
        e.append(row);
      });
      if (!list.length) message("pr-feed","Keine Pull Requests vorhanden.");
    } catch(err) {message("pr-feed",err.message,"error");}
  }
  function breadcrumbs() {
    const nav=byId("breadcrumbs");nav.replaceChildren();
    const pieces=state.directory ? state.directory.split("/") : [];
    const all=["ROOT",...pieces];
    all.forEach((name,index)=>{
      if(index) nav.append(node("span","crumb-divider","/"));
      const btn=node("button","crumb-button",name);btn.type="button";
      const path=pieces.slice(0,index).join("/");
      btn.addEventListener("click",()=>loadDirectory(path));
      nav.append(btn);
    });
    byId("up-folder").disabled=pieces.length===0;
    byId("file-search").value="";
  }
  function showFiles() {
    const e=byId("file-list");e.replaceChildren();
    const query=byId("file-search").value.trim().toLocaleLowerCase("de-DE");
    const items=state.files.filter(item => String(item.name).toLocaleLowerCase("de-DE").includes(query));
    items.forEach(item=>{
      const row=node("div","file-item"),btn=node("button","file-button");
      btn.type="button";
      btn.append(node("span","file-type",item.type==="dir"?"▤":"◇"));
      btn.append(node("span","",item.name));
      btn.addEventListener("click",()=>item.type==="dir"?loadDirectory(item.path):previewFile(item));
      row.append(btn,node("span","file-size",item.type==="dir"?"VERZEICHNIS":typeof item.size==="number"?(Math.max(1,Math.ceil(item.size/1024))+" KiB"):"DATEI"));
      e.append(row);
    });
    if(!items.length) message("file-list",query?"Keine Treffer in diesem Ordner.":"Dieser Ordner ist leer.");
  }
  async function loadDirectory(path) {
    const normalized=String(path||"");
    if (normalized.split("/").some(s=>s==="."||s==="..")||normalized.startsWith("/")) return;
    state.directory=normalized;
    byId("file-preview").hidden=true;
    breadcrumbs();message("file-list","GitHub-Verzeichnis wird geladen …","loading");
    try {
      const url=ENDPOINT + "/contents/" + normalized.split("/").map(encodeURIComponent).join("/") + "?ref=main";
      const list=await getJson(url);
      if(!Array.isArray(list)) throw new Error("Ordnerinhalt nicht verfügbar");
      state.files=list.sort((a,b)=>(a.type==="dir"?0:1)-(b.type==="dir"?0:1)||a.name.localeCompare(b.name));
      showFiles();
    } catch(err) {message("file-list",err.message,"error");}
  }
  async function previewFile(item) {
    const preview=byId("file-preview"), body=byId("preview-content");
    preview.hidden=false;byId("preview-name").textContent=item.path;
    byId("preview-original").href=safePage(item.html_url);
    body.textContent="Quelle wird abgefragt …";
    if(item.size > MAX_PREVIEW_BYTES) {body.textContent="Diese Datei ist größer als 150 KB. Das unveränderte Original ist auf GitHub verfügbar.";return;}
    if(!/\.(md|txt|json|jsonl|py|js|mjs|css|html|yml|yaml|xml|toml|csv|sh|svg|sql|ini|log|ts|tsx|jsx)$/i.test(item.name)){
      body.textContent="Diese Datei wird aus Sicherheitsgründen nicht als Text interpretiert. Bitte Original öffnen.";return;
    }
    try {
      const url=ENDPOINT+"/contents/"+item.path.split("/").map(encodeURIComponent).join("/")+"?ref=main";
      const content=await getJson(url);
      if(content.encoding!=="base64"||typeof content.content!=="string")throw new Error("Datei nicht als API-Text verfügbar");
      const bytes=Uint8Array.from(atob(content.content.replace(/\s/g,"")),c=>c.charCodeAt(0));
      body.textContent=new TextDecoder("utf-8",{fatal:false}).decode(bytes);
    } catch(err){body.textContent="Vorschau nicht verfügbar: "+err.message;}
  }
  function chooseTab(key,force=false) {
    state.active=key;
    const tabs=[...document.querySelectorAll('[role="tab"]')];
    tabs.forEach(t=>{
      const selected=t.dataset.tab===key;
      t.setAttribute("aria-selected",selected?"true":"false");
      t.tabIndex=selected?0:-1;
      const p=byId("panel-"+t.dataset.tab);p.hidden=!selected;
    });
    if(key==="commits")loadCommits(force);
    else if(key==="files") {if(!state.files.length||force)loadDirectory(state.directory);else showFiles();}
    else if(key==="prs")loadPRs(force);
  }
  const tabs=[...document.querySelectorAll('[role="tab"]')];
  tabs.forEach((t,index)=>{
    t.addEventListener("click",()=>chooseTab(t.dataset.tab));
    t.addEventListener("keydown",(evt)=>{
      if(!["ArrowLeft","ArrowRight","Home","End"].includes(evt.key))return;
      evt.preventDefault();
      const next=evt.key==="Home"?0:evt.key==="End"?tabs.length-1:(index+(evt.key==="ArrowRight"?1:-1)+tabs.length)%tabs.length;
      tabs[next].focus();chooseTab(tabs[next].dataset.tab);
    });
  });
  byId("file-search").addEventListener("input",showFiles);
  byId("up-folder").addEventListener("click",()=>{
    const parts=state.directory.split("/").filter(Boolean);parts.pop();loadDirectory(parts.join("/"));
  });
  byId("refresh").addEventListener("click",()=>{const key=state.active;chooseTab(key,true);if(key!=="commits")loadCommits(true);});
  loadCommits();
  setInterval(()=>{if(!document.hidden){loadCommits();if(state.active==="prs")loadPRs();}},REFRESH_MS);
})();
