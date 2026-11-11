/* NEXUS OMEGA OPPO diagnostic protocol V0 — research-only reference reducer.
   SPDX-License-Identifier: Apache-2.0. NO Android runtime permissions, no network I/O.
   Does NOT enable wireless debugging and does NOT prove physical sensor integrity. */
export const CHANNELS=Object.freeze(["SENSOR","APP_FGS","WIFI","ADB","UPLOAD","SERVER","AUDIT"]);
export const OUTCOMES=Object.freeze(["OK","DEGRADED","DISCONNECTED","HOLD_SOURCE","MISMATCH","RECOVERED","UNKNOWN"]);
export const SOURCES=Object.freeze(["DEVICE_OBSERVED","APP_OBSERVED","SERVER_OBSERVED","CURSOR_REPORTED","SYNTHETIC"]);
const hex=/^[a-f0-9]{64}$/;
const safeId=/^[A-Za-z0-9_.:-]{1,100}$/;
export function checkEvent(e){
  if(!e||typeof e!=="object"||Array.isArray(e))throw Error("EVENT_INVALID");
  if(!safeId.test(e.session_id||"")||!safeId.test(e.event_id||""))throw Error("IDENTITY_INVALID");
  if(!CHANNELS.includes(e.channel)||!OUTCOMES.includes(e.outcome)||!SOURCES.includes(e.source_class))throw Error("ENUM_INVALID");
  if(!Number.isSafeInteger(e.seq)||e.seq<0)throw Error("SEQUENCE_INVALID");
  if(!Number.isSafeInteger(e.mono_ns)||e.mono_ns<0)throw Error("MONOTONIC_CLOCK_INVALID");
  if(typeof e.observed_utc!=="string"||!/^\d{4}-\d{2}-\d{2}T\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(e.observed_utc)||!Number.isFinite(Date.parse(e.observed_utc)))throw Error("UTC_INVALID");
  if(!hex.test(e.payload_sha256||"")||!hex.test(e.previous_sha256||""))throw Error("HASH_FORMAT_INVALID");
  if(typeof e.schema!=="string"||e.schema!=="nexus-mobile-diagnostic-event/v0")throw Error("SCHEMA_INVALID");
  if(Object.keys(e).some(x=>!["schema","session_id","event_id","channel","outcome","source_class","seq","mono_ns","observed_utc","payload_sha256","previous_sha256"].includes(x)))throw Error("UNAPPROVED_FIELD");
  return true;
}
export function appendEvent(state,e) {
  checkEvent(e);
  const s=state??{next_seq:0,last_mono_ns:null,last_payload_sha256:"0".repeat(64),seen:{}};
  if(!Number.isSafeInteger(s.next_seq)||typeof s.last_payload_sha256!=="string")throw Error("STATE_INVALID");
  // Duplicate is acknowledged ONLY if the original payload digest and event ID agree.
  if(e.seq<s.next_seq) {
    const prior=s.seen[String(e.seq)];
    if(prior&&prior.event_id===e.event_id&&prior.payload_sha256===e.payload_sha256)return{...s,verdict:"DUPLICATE_IDENTICAL"};
    throw Error("REPLAY_OR_CONFLICT");
  }
  if(e.seq!==s.next_seq)throw Error("SOURCE_GAP_SEQUENCE");
  if(e.previous_sha256!==s.last_payload_sha256)throw Error("CHAIN_PREDECESSOR_MISMATCH");
  if(s.last_mono_ns!==null&&e.mono_ns<s.last_mono_ns)throw Error("TIMEBASE_REGRESSION");
  return{next_seq:s.next_seq+1,last_mono_ns:e.mono_ns,last_payload_sha256:e.payload_sha256,
    seen:{...s.seen,[String(e.seq)]:{event_id:e.event_id,payload_sha256:e.payload_sha256}},
    verdict:e.source_class==="SYNTHETIC"?"SYNTHETIC_ONLY":"SOURCE_REPORTED_NOT_INDEPENDENTLY_VERIFIED"};
}
// Data plane storage, SHA256 computation, signing, encryption and server ack/readback
// are to be implemented independently with tested Android code. This is a validator
// of *claimed* metadata format only; hashes here are not recomputed or authenticated.
