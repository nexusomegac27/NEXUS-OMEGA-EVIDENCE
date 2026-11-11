"use strict";
// RUN138 independent frozen evaluator; written before candidate V2.
// Separate from candidate implementation. C1 claim-only, no receiver authentication.
module.exports = function evaluate(aggregate, trusted, legacyEvaluate) {
  const sha="a".repeat(40), digest="b".repeat(64);
  const prefix="https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+sha+"/";
  const fields={
    EVENT_ID:"RUN138-E001",SOURCE_COMMIT:sha,SOURCE_SHA256:digest,
    SOURCE_BYTES:"123",SOURCE_URI:prefix+"research/r16/example.json",
    HANDOFF_ROUTINE:"TRUE",HANDOFF_PUBLIC:"TRUE",HANDOFF_AUTHORIZED:"TRUE",
    HANDOFF_ACCESSIBLE:"TRUE",HANDOFF_AUTOMATED:"TRUE",HANDOFF_MANUAL_TRIGGER:"FALSE",
    READBACK_COMMIT:"TRUE",READBACK_SOURCE:"TRUE",READBACK_TEST:"TRUE"
  };
  const event=(changes={})=>Object.entries({...fields,...changes})
    .map(([k,v])=>k+"="+v).join("\n")+"\n";
  const valid=event(), manual=event({EVENT_ID:"RUN138-E002",HANDOFF_MANUAL_TRIGGER:"TRUE"});
  const malformed="EVENT_ID=RUN138-E003\n";
  const forged=()=>({status:"VALID_EVENT_CLAIM_ONLY",eligible_claim:true,
    automated_success_claim:true,verified_automated_success:"NOT_ESTABLISHED",
    projectwide_denominator:"NOT_COMPUTABLE"});
  const cases=[
    ["implicit_pinned_classifier",()=>aggregate([valid]),"VALID_COHORT_CLAIMS_ONLY",1,1],
    ["explicit_pinned_classifier",()=>aggregate([valid],trusted),"VALID_COHORT_CLAIMS_ONLY",1,1],
    ["forged_valid_event",()=>aggregate([valid],forged),"FAIL_CLOSED",null,null],
    ["forged_malformed_event",()=>aggregate([malformed],forged),"FAIL_CLOSED",null,null],
    ["forged_new_function",()=>aggregate([malformed],()=>forged()),"FAIL_CLOSED",null,null],
    ["malformed_with_trusted",()=>aggregate([malformed],trusted),"FAIL_CLOSED",null,null],
    ["duplicate_with_trusted",()=>aggregate([valid,valid],trusted),"FAIL_CLOSED",null,null],
    ["mixed_with_trusted",()=>aggregate([valid,manual],trusted),"VALID_COHORT_CLAIMS_ONLY",2,1],
    ["explicit_undefined",()=>aggregate([valid],undefined),"FAIL_CLOSED",null,null],
    ["explicit_null",()=>aggregate([valid],null),"FAIL_CLOSED",null,null]
  ];
  const failures=[];
  for(const [name,fn,status,eligible,auto] of cases){
    let result;
    try{result=fn();}catch(e){failures.push(name+":THREW:"+e.message);continue;}
    if(result.status!==status||result.eligible_claim_count!==eligible||
       result.automated_claim_count!==auto||
       result.verified_automated_count!=="NOT_ESTABLISHED"||
       result.projectwide_denominator!=="NOT_COMPUTABLE"||
       result.claim_ceiling!=="C1_DESCRIPTIVE_ONLY")
      failures.push(name+":"+JSON.stringify(result));
  }
  const legacy=legacyEvaluate(aggregate,trusted);
  return {new_total:cases.length,new_pass:cases.length-failures.length,
    negative_fixtures:cases.filter(x=>x[2]==="FAIL_CLOSED").length,
    positive_controls:cases.filter(x=>x[2]!=="FAIL_CLOSED").length,
    legacy_total:legacy.total,legacy_pass:legacy.pass,
    failures:[...failures,...legacy.failures],oracle:"RUN138_FROZEN_BEFORE_CANDIDATE"};
};
