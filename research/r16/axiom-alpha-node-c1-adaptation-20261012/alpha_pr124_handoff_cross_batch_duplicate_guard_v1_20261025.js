"use strict";
// Run139: C1 claim-only cross-batch deduplication; never a project-wide census.
// Rejects duplicate EVENT_IDs even when they arrive in different batches.
// Does not authenticate bytes, actors, independent receiver ACKs or manual-trigger status.
const pinned=require("./alpha_pr124_handoff_classifier_identity_guard_v2_20261025.js");
const fail=()=>({status:"FAIL_CLOSED",eligible_claim_count:null,automated_claim_count:null,
  verified_automated_count:"NOT_ESTABLISHED",projectwide_denominator:"NOT_COMPUTABLE",
  claim_ceiling:"C1_DESCRIPTIVE_ONLY"});
function aggregateBatches(batches){
  if(arguments.length!==1||!Array.isArray(batches)||batches.length<1||batches.length>100)return fail();
  const all=[];
  for(let i=0;i<batches.length;i++){
    if(!Object.prototype.hasOwnProperty.call(batches,i))return fail();
    const batch=batches[i];
    if(!Array.isArray(batch)||batch.length<1||batch.length>500)return fail();
    for(let j=0;j<batch.length;j++){
      if(!Object.prototype.hasOwnProperty.call(batch,j))return fail();
      const raw=batch[j];
      if(typeof raw!=="string"||raw.length>16384||all.length>=500)return fail();
      all.push(raw);
    }
  }
  return pinned(all);
}
module.exports=aggregateBatches;
