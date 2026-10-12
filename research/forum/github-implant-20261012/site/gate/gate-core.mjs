/* NEXUS OMEGA · GitHub↔WWW Security + Science Gate · SPDX-License-Identifier: MIT */
export const CONTRACT = Object.freeze({
  repository:"nexusomegac27/NEXUS-OMEGA-EVIDENCE",
  sourceRoot:"research/forum/github-implant-20261012/site/",
  targetRoot:"/forum/github-implant/",
  claimCeiling:"C1_DESCRIPTIVE_ONLY",
  files:Object.freeze(["index.html","assets/github-implant.css","assets/github-implant.js"])
});
export function hex(bytes) {
  return Array.from(bytes, b => b.toString(16).padStart(2,"0")).join("");
}
export async function digest(bytes) {
  if (!globalThis.crypto?.subtle) throw new Error("WebCrypto fehlt / HTTPS erforderlich");
  return hex(new Uint8Array(await globalThis.crypto.subtle.digest("SHA-256",bytes)));
}
export function parseGitHubContent(data) {
  if (!data || data.encoding!=="base64" || typeof data.content!=="string" || !/^[0-9a-f]{40}$/.test(data.sha||"")) throw new Error("Ungültige GitHub-Content-Antwort");
  const encoded=data.content.replace(/\s+/g,"");
  if (encoded.length>900000) throw new Error("Quellobjekt zu groß für das kleine Gate");
  if(!/^[A-Za-z0-9+/]*={0,2}$/.test(encoded))throw new Error("Ungültiges Base64");
  const binary=atob(encoded);
  const bytes=Uint8Array.from(binary,c=>c.charCodeAt(0));
  if (data.size!==bytes.length) throw new Error("GitHub-Bytezahl weicht vom dekodierten Inhalt ab");
  return bytes;
}
export function classify(rows,apiOK,scienceOK) {
  if(!apiOK)return {code:"HOLD_SOURCE",label:"SOURCE GAP",detail:"GitHub-Quelle nicht vollständig beobachtbar"};
  if(!Array.isArray(rows)||rows.length!==CONTRACT.files.length)return {code:"HOLD_SCOPE",label:"PRÜFUMFANG OFFEN",detail:"Nicht alle drei freigegebenen Dateien geprüft"};
  if(rows.some(x=>x.status==="ERROR"))return {code:"HOLD_WWW",label:"WWW GAP",detail:"Mindestens eine Webdatei ist nicht verfügbar"};
  if(rows.some(x=>x.status==="DIVERGENT"))return {code:"DIVERGENCE",label:"BYTE-DIVERGENZ",detail:"GitHub und NEXUS liefern unterschiedliche Dateibytes"};
  if(!scienceOK)return {code:"SCIENCE_WARN",label:"C1-WARNUNG",detail:"C1-Kennzeichnung auf der Website fehlt"};
  if(rows.every(x=>x.status==="MATCH"))return {code:"MATCH_C1",label:"QUELLEN IDENTISCH",detail:"Alle drei beobachteten Dateien stimmen mit GitHub überein · keine Wissenschaftszertifizierung"};
  return {code:"HOLD_SCOPE",label:"UNVOLLSTÄNDIG",detail:"Beobachtung nicht abgeschlossen"};
}
export function isC1Marked(html) {
  return typeof html==="string" && html.includes("C1_DESCRIPTIVE_ONLY") && !/\bC2_(?:PROVEN|VALIDATED)\b/.test(html);
}
export function safeGitHubUrl(url) {
  try {const u=new URL(url);return u.protocol==="https:"&&u.hostname==="github.com"&&u.pathname.startsWith("/nexusomegac27/NEXUS-OMEGA-EVIDENCE/");}
  catch {return false;}
}
