"use strict";
// Run139 frozen, separate black-box evaluator. Commit before the candidate.
// The oracle evaluates claim-only cohort hygiene, not real transfer automation.
module.exports=function evaluate(candidate, prior){
  const sha="a".repeat(40), digest="b".repeat(64);
  const prefix="https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+sha+"/";
  const base={EVENT_ID:"RUN139-E0001",SOURCE_COMMIT:sha,SOURCE_SHA256:digest,
    SOURCE_BYTES:"123",SOURCE_URI:prefix+"research/r16/example.json",
    HANDOFF_ROUTINE:"TRUE",HANDOFF_PUBLIC:"TRUE",HANDOFF_AUTHORIZED:"TRUE",
    HANDOFF_ACCESSIBLE:"TRUE",HANDOFF_AUTOMATED:"TRUE",HANDOFF_MANUAL_TRIGGER:"FALSE",
    READBACK_COMMIT:"TRUE",READBACK_SOURCE:"TRUE",READBACK_TEST:"TRUE"};
  const event=(id,changes={})=>Object.entries({...base,EVENT_ID:id,...changes})
    .map(([k,v])=>k+"="+v).join("\n")+"\n";
  const a=event("RUN139-E0001"), b=event("RUN139-E0002"), c=event("RUN139-E0003");
  const manual=event("RUN139-E0004",{HANDOFF_MANUAL_TRIGGER:"TRUE"});
  const ineligible=event("RUN139-E0005",{HANDOFF_ACCESSIBLE:"FALSE"});
  const sameIdDifferentSource=event("RUN139-E0001",{SOURCE_SHA256:"c".repeat(64)});
  const malformed="EVENT_ID=RUN139-E9999\n";
  const sparseOuter=[ [a], [b] ];delete sparseOuter[1];
  const sparseInner=[a,b];delete sparseInner[1];
  const over=Array.from({length:501},(_,i)=>event("RUN139-M"+String(i).padStart(4,"0")));
  const max=over.slice(0,500);
  const tests=[
    ["unique_cross_batch",()=>candidate([[a],[b]]),"VALID_COHORT_CLAIMS_ONLY",2,2],
    ["duplicate_across_batches",()=>candidate([[a],[a]]),"FAIL_CLOSED",null,null],
    ["same_id_changed_source",()=>candidate([[a],[sameIdDifferentSource]]),"FAIL_CLOSED",null,null],
    ["duplicate_within_batch",()=>candidate([[a,a]]),"FAIL_CLOSED",null,null],
    ["single_batch",()=>candidate([[a]]),"VALID_COHORT_CLAIMS_ONLY",1,1],
    ["mixed_manual",()=>candidate([[a],[manual]]),"VALID_COHORT_CLAIMS_ONLY",2,1],
    ["ineligible",()=>candidate([[a],[ineligible]]),"VALID_COHORT_CLAIMS_ONLY",1,1],
    ["malformed_event",()=>candidate([[a],[malformed]]),"FAIL_CLOSED",null,null],
    ["empty_outer",()=>candidate([]),"FAIL_CLOSED",null,null],
    ["empty_inner",()=>candidate([[a],[]]),"FAIL_CLOSED",null,null],
    ["nonarray_inner",()=>candidate([[a],"bad"]),"FAIL_CLOSED",null,null],
    ["sparse_outer",()=>candidate(sparseOuter),"FAIL_CLOSED",null,null],
    ["sparse_inner",()=>candidate([sparseInner]),"FAIL_CLOSED",null,null],
    ["over_500",()=>candidate([over]),"FAIL_CLOSED",null,null],
    ["exactly_500",()=>candidate([max]),"VALID_COHORT_CLAIMS_ONLY",500,500],
    ["nonstr_event",()=>candidate([[a],[null]]),"FAIL_CLOSED",null,null],
    ["outer_nonarray",()=>candidate("not a cohort"),"FAIL_CLOSED",null,null],
    ["forged_classifier_argument",()=>candidate([[a], [b]],()=>({status:"VALID_COHORT_CLAIMS_ONLY"})),"FAIL_CLOSED",null,null],
    ["three_batches",()=>candidate([[a,b],[c],[manual]]),"VALID_COHORT_CLAIMS_ONLY",4,3],
    ["invalid_event_id",()=>candidate([[a],[event("bad id")]]),"FAIL_CLOSED",null,null]
  ];
  const failures=[];
  for(const [name,fn,status,eligible,automated] of tests){
    let got;
    try{got=fn();}catch(e){failures.push(name+":THREW:"+e.message);continue;}
    if(!got||got.status!==status||got.eligible_claim_count!==eligible||
       got.automated_claim_count!==automated||
       got.verified_automated_count!=="NOT_ESTABLISHED"||
       got.projectwide_denominator!=="NOT_COMPUTABLE"||
       got.claim_ceiling!=="C1_DESCRIPTIVE_ONLY")failures.push(name+":"+JSON.stringify(got));
  }
  const priorFirst=prior([a]),priorSecond=prior([a]);
  const baseline_duplicate_not_rejected=priorFirst.status==="VALID_COHORT_CLAIMS_ONLY"&&
    priorSecond.status==="VALID_COHORT_CLAIMS_ONLY"&&
    priorFirst.automated_claim_count+priorSecond.automated_claim_count===2;
  return {total:tests.length,pass:tests.length-failures.length,
    negative:tests.filter(x=>x[2]==="FAIL_CLOSED").length,
    positive:tests.filter(x=>x[2]!=="FAIL_CLOSED").length,
    baseline_duplicate_not_rejected,failures,
    oracle:"RUN139_FROZEN_BEFORE_CANDIDATE_C1_CLAIM_ONLY"};
};
