"use strict";
// Run138 C1-only hardened cohort adapter. The classifier is pinned by module identity.
// Prevents caller-supplied validators from fabricating claim counts.
// Does NOT authenticate source bytes, actors, receivers or projectwide metrics.
const trusted=require("./alpha_pr124_handoff_scope_claim_classifier_v1_20261025.js");
const previous=require("./alpha_pr124_handoff_cohort_duplicate_guard_v1_20261025.js");
const failure=()=>({status:"FAIL_CLOSED",eligible_claim_count:null,automated_claim_count:null,
  verified_automated_count:"NOT_ESTABLISHED",projectwide_denominator:"NOT_COMPUTABLE",
  claim_ceiling:"C1_DESCRIPTIVE_ONLY"});
function aggregate(records,suppliedClassifier){
  if(arguments.length>1&&suppliedClassifier!==trusted)return failure();
  return previous(records,trusted);
}
module.exports=aggregate;
