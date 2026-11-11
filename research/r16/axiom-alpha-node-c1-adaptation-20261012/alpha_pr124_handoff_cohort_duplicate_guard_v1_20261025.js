"use strict";
// Run137: research-only batch hygiene for reported handoff events.
// This cannot independently authenticate a GitHub actor, original bytes or project coverage.
const failure=()=>({status:"FAIL_CLOSED",eligible_claim_count:null,automated_claim_count:null,
  verified_automated_count:"NOT_ESTABLISHED",projectwide_denominator:"NOT_COMPUTABLE",
  claim_ceiling:"C1_DESCRIPTIVE_ONLY"});
function aggregate(records,classify){
  if(!Array.isArray(records)||records.length<1||records.length>500||typeof classify!=="function")return failure();
  let eligible=0,automated=0;
  const seen=new Set();
  for(const raw of records){
    if(typeof raw!=="string"||raw.length>16384)return failure();
    let claim;
    try{claim=classify(raw);}catch(_){return failure();}
    if(!claim||claim.status!=="VALID_EVENT_CLAIM_ONLY"||
       typeof claim.eligible_claim!=="boolean"||typeof claim.automated_success_claim!=="boolean"||
       claim.verified_automated_success!=="NOT_ESTABLISHED"||
       claim.projectwide_denominator!=="NOT_COMPUTABLE"||
       (claim.automated_success_claim&&!claim.eligible_claim))return failure();
    const matches=raw.match(/^EVENT_ID=([A-Z0-9][A-Z0-9._-]{3,79})$/gm);
    if(!matches||matches.length!==1)return failure();
    const id=matches[0].slice("EVENT_ID=".length);
    if(seen.has(id))return failure();
    seen.add(id);
    if(claim.eligible_claim)eligible++;
    if(claim.automated_success_claim)automated++;
  }
  return {status:"VALID_COHORT_CLAIMS_ONLY",eligible_claim_count:eligible,
    automated_claim_count:automated,verified_automated_count:"NOT_ESTABLISHED",
    projectwide_denominator:"NOT_COMPUTABLE",claim_ceiling:"C1_DESCRIPTIVE_ONLY"};
}
module.exports=aggregate;
