"use strict";
// Run137 frozen evaluator. Must be committed before cohort candidate; no imports from it.
module.exports = function evaluate(aggregate, classify) {
  const sha = "a".repeat(40), digest = "b".repeat(64);
  const base = {
    EVENT_ID:"RUN137-E001", SOURCE_COMMIT:sha, SOURCE_SHA256:digest,
    SOURCE_BYTES:"123", SOURCE_URI:"https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+sha+"/research/r16/example.json",
    HANDOFF_ROUTINE:"TRUE",HANDOFF_PUBLIC:"TRUE",HANDOFF_AUTHORIZED:"TRUE",
    HANDOFF_ACCESSIBLE:"TRUE",HANDOFF_AUTOMATED:"TRUE",HANDOFF_MANUAL_TRIGGER:"FALSE",
    READBACK_COMMIT:"TRUE",READBACK_SOURCE:"TRUE",READBACK_TEST:"TRUE"
  };
  const event=(id,change={})=>Object.entries({...base,EVENT_ID:id,...change})
    .map(([k,v])=>k+"="+v).join("\n")+"\n";
  const a=event("RUN137-E001"), b=event("RUN137-E002"), c=event("RUN137-E003");
  const manual=event("RUN137-E003",{HANDOFF_MANUAL_TRIGGER:"TRUE"});
  const privateEvent=event("RUN137-E004",{HANDOFF_PUBLIC:"FALSE"});
  const readbackGap=event("RUN137-E005",{READBACK_TEST:"FALSE"});
  const malformed=event("RUN137-E006",{HANDOFF_ACCESSIBLE:"YES"});
  const wrongCommit=event("RUN137-E007",{SOURCE_COMMIT:"c".repeat(40)});
  const cases=[
    ["one",[a],"VALID_COHORT_CLAIMS_ONLY",1,1],
    ["two_distinct",[a,b],"VALID_COHORT_CLAIMS_ONLY",2,2],
    ["mixed_manual",[a,manual],"VALID_COHORT_CLAIMS_ONLY",2,1],
    ["private_excluded",[privateEvent],"VALID_COHORT_CLAIMS_ONLY",0,0],
    ["readback_gap",[readbackGap],"VALID_COHORT_CLAIMS_ONLY",1,0],
    ["same_source_different_events",[a,b],"VALID_COHORT_CLAIMS_ONLY",2,2],
    ["manual_only",[manual],"VALID_COHORT_CLAIMS_ONLY",1,0],
    ["three_mixed",[a,manual,privateEvent],"VALID_COHORT_CLAIMS_ONLY",2,1],
    ["duplicate_identical",[a,a],"FAIL_CLOSED",null,null],
    ["duplicate_conflicting",[a,event("RUN137-E001",{HANDOFF_AUTOMATED:"FALSE"})],"FAIL_CLOSED",null,null],
    ["invalid_scope",[a,malformed],"FAIL_CLOSED",null,null],
    ["invalid_commit_uri",[a,wrongCommit],"FAIL_CLOSED",null,null],
    ["null_record",[a,null],"FAIL_CLOSED",null,null],
    ["empty",[],"FAIL_CLOSED",null,null],
    ["not_array",a,"FAIL_CLOSED",null,null],
    ["too_many",Array.from({length:501},(_,i)=>event("RUN137-"+String(i).padStart(5,"0"))),"FAIL_CLOSED",null,null],
    ["unknown_field",[a+"EXTRA=TRUE\n"],"FAIL_CLOSED",null,null],
    ["non_string",[42],"FAIL_CLOSED",null,null],
    ["bad_event_id",[event("run137-e008")],"FAIL_CLOSED",null,null],
    ["manual_auto_both_true",[event("RUN137-E009",{HANDOFF_MANUAL_TRIGGER:"TRUE"})],"VALID_COHORT_CLAIMS_ONLY",1,0]
  ];
  const failures=[];
  for(const [name,input,status,eligible,auto] of cases){
    let actual;
    try{actual=aggregate(input,classify)}catch(e){failures.push(name+":THREW:"+e.message);continue;}
    if(actual.status!==status||actual.eligible_claim_count!==eligible||
      actual.automated_claim_count!==auto||
      actual.projectwide_denominator!=="NOT_COMPUTABLE"||
      actual.verified_automated_count!=="NOT_ESTABLISHED"||
      actual.claim_ceiling!=="C1_DESCRIPTIVE_ONLY")
      failures.push(name+":"+JSON.stringify(actual));
  }
  return {total:cases.length,pass:cases.length-failures.length,failures,
    negative_fixtures:cases.filter(c=>c[2]==="FAIL_CLOSED").length,
    positive_controls:cases.filter(c=>c[2]!=="FAIL_CLOSED").length,
    immutable_oracle:"RUN137_FROZEN_BEFORE_CANDIDATE"};
};
