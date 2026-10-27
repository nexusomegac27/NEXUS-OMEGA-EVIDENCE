"use strict";
// Frozen before the candidate. Independent black-box assertions; no imports from candidate.
module.exports = function evaluate(classify) {
  const commit = "a".repeat(40), hash = "b".repeat(64);
  const base = [
    "EVENT_ID=RUN136-E001",
    "SOURCE_COMMIT=" + commit,
    "SOURCE_SHA256=" + hash,
    "SOURCE_BYTES=123",
    "SOURCE_URI=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/" + commit + "/research/r16/example.json",
    "HANDOFF_ROUTINE=TRUE",
    "HANDOFF_PUBLIC=TRUE",
    "HANDOFF_AUTHORIZED=TRUE",
    "HANDOFF_ACCESSIBLE=TRUE",
    "HANDOFF_AUTOMATED=TRUE",
    "HANDOFF_MANUAL_TRIGGER=FALSE",
    "READBACK_COMMIT=TRUE",
    "READBACK_SOURCE=TRUE",
    "READBACK_TEST=TRUE"
  ];
  const set = (lines,key,val) => lines.map(s=>s.startsWith(key+"=")?key+"="+val:s);
  const drop = (lines,key) => lines.filter(s=>!s.startsWith(key+"="));
  const cases = [
    ["auto_claim",base,"VALID_EVENT_CLAIM_ONLY",true,true],
    ["manual",set(base,"HANDOFF_MANUAL_TRIGGER","TRUE"),"VALID_EVENT_CLAIM_ONLY",true,false],
    ["private",set(base,"HANDOFF_PUBLIC","FALSE"),"VALID_EVENT_CLAIM_ONLY",false,false],
    ["readback_gap",set(base,"READBACK_TEST","FALSE"),"VALID_EVENT_CLAIM_ONLY",true,false],
    ["missing_scope",drop(base,"HANDOFF_ACCESSIBLE"),"FAIL_CLOSED",null,null],
    ["duplicate_scope",[...base,"HANDOFF_PUBLIC=TRUE"],"FAIL_CLOSED",null,null],
    ["bad_bool",set(base,"HANDOFF_AUTOMATED","YES"),"FAIL_CLOSED",null,null],
    ["run_summary",[...drop(base,"HANDOFF_AUTOMATED"),"HANDOFF_AUTOMATED=2_OF_2"],"FAIL_CLOSED",null,null],
    ["bad_hash",set(base,"SOURCE_SHA256","abc"),"FAIL_CLOSED",null,null],
    ["unknown_field",[...base,"CLAIM_PROMOTION=TRUE"],"FAIL_CLOSED",null,null],
    ["missing_event_id",drop(base,"EVENT_ID"),"FAIL_CLOSED",null,null],
    ["invalid_bytes",set(base,"SOURCE_BYTES","0"),"FAIL_CLOSED",null,null],
    ["unbound_uri",set(base,"SOURCE_URI","https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+"c".repeat(40)+"/research/r16/example.json"),"FAIL_CLOSED",null,null],
    ["duplicate_event_id",[...base,"EVENT_ID=RUN136-E001"],"FAIL_CLOSED",null,null]
  ];
  const failures=[];
  for(const [name,lines,status,eligible,auto] of cases) {
    let actual;
    try { actual=classify(lines.join("\n")+"\n"); } catch(e) { failures.push(name+":THREW:"+e.message);continue; }
    if(actual.status!==status || actual.eligible_claim!==eligible ||
       actual.automated_success_claim!==auto ||
       actual.verified_automated_success!=="NOT_ESTABLISHED" ||
       actual.projectwide_denominator!=="NOT_COMPUTABLE")
      failures.push(name+":"+JSON.stringify(actual));
  }
  return {total:cases.length,pass:cases.length-failures.length,failures,
    negative_fixtures:cases.filter(c=>c[2]==="FAIL_CLOSED").length,
    claim_ceiling:"C1_DESCRIPTIVE_ONLY"};
};
