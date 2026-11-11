"use strict";
// Research-only C1 classifier. It validates a single reported handoff event.
// No project-wide inventory or independent receiver readback is established here.
const FIELDS=[
  "EVENT_ID","SOURCE_COMMIT","SOURCE_SHA256","SOURCE_BYTES","SOURCE_URI",
  "HANDOFF_ROUTINE","HANDOFF_PUBLIC","HANDOFF_AUTHORIZED","HANDOFF_ACCESSIBLE",
  "HANDOFF_AUTOMATED","HANDOFF_MANUAL_TRIGGER",
  "READBACK_COMMIT","READBACK_SOURCE","READBACK_TEST"
];
const BOOLS=FIELDS.filter(k=>k.startsWith("HANDOFF_")||k.startsWith("READBACK_"));
const fail=()=>({status:"FAIL_CLOSED",eligible_claim:null,automated_success_claim:null,
  verified_automated_success:"NOT_ESTABLISHED",projectwide_denominator:"NOT_COMPUTABLE"});
function classify(text) {
  if(typeof text!=="string"||text.length>16384||text.includes("\r")||text.includes("\0")) return fail();
  const lines=text.endsWith("\n")?text.slice(0,-1).split("\n"):text.split("\n");
  if(lines.length!==FIELDS.length) return fail();
  const map=Object.create(null);
  for(const line of lines) {
    const i=line.indexOf("=");
    if(i<1) return fail();
    const key=line.slice(0,i),value=line.slice(i+1);
    if(!FIELDS.includes(key)||Object.prototype.hasOwnProperty.call(map,key)||value.length===0) return fail();
    map[key]=value;
  }
  if(FIELDS.some(k=>!Object.prototype.hasOwnProperty.call(map,k))) return fail();
  if(!/^[A-Z0-9][A-Z0-9._-]{3,79}$/.test(map.EVENT_ID)) return fail();
  if(!/^[0-9a-f]{40}$/.test(map.SOURCE_COMMIT)||!/^[0-9a-f]{64}$/.test(map.SOURCE_SHA256)) return fail();
  if(!/^[1-9][0-9]*$/.test(map.SOURCE_BYTES)||!Number.isSafeInteger(Number(map.SOURCE_BYTES))) return fail();
  const prefix="https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+map.SOURCE_COMMIT+"/";
  if(!map.SOURCE_URI.startsWith(prefix)) return fail();
  const sourcePath=map.SOURCE_URI.slice(prefix.length);
  if(!/^[A-Za-z0-9_.\/-]+$/.test(sourcePath)||sourcePath.split("/").some(p=>p===".."||p===""||p===".")) return fail();
  for(const k of BOOLS) if(map[k]!=="TRUE"&&map[k]!=="FALSE") return fail();
  const yes=k=>map[k]==="TRUE";
  const eligible=["HANDOFF_ROUTINE","HANDOFF_PUBLIC","HANDOFF_AUTHORIZED","HANDOFF_ACCESSIBLE"].every(yes);
  const auto=eligible&&yes("HANDOFF_AUTOMATED")&&!yes("HANDOFF_MANUAL_TRIGGER")&&
    ["READBACK_COMMIT","READBACK_SOURCE","READBACK_TEST"].every(yes);
  return {status:"VALID_EVENT_CLAIM_ONLY",eligible_claim:eligible,automated_success_claim:auto,
    verified_automated_success:"NOT_ESTABLISHED",projectwide_denominator:"NOT_COMPUTABLE"};
}
module.exports=classify;
