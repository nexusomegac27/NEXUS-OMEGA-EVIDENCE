"use strict";
// Run140 frozen before candidate: independent black-box oracle, hostile JS arrays.
// Counts are reported C1 claims, never independently verified transfers.
module.exports=function evaluate(target){
const h="a".repeat(40),s="b".repeat(64);
const event=(id,manual=false)=>[
"EVENT_ID="+id,"SOURCE_COMMIT="+h,"SOURCE_SHA256="+s,"SOURCE_BYTES=123",
"SOURCE_URI=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/"+h+"/research/r16/example.json",
"HANDOFF_ROUTINE=TRUE","HANDOFF_PUBLIC=TRUE","HANDOFF_AUTHORIZED=TRUE",
"HANDOFF_ACCESSIBLE=TRUE","HANDOFF_AUTOMATED=TRUE","HANDOFF_MANUAL_TRIGGER="+(manual?"TRUE":"FALSE"),
"READBACK_COMMIT=TRUE","READBACK_SOURCE=TRUE","READBACK_TEST=TRUE"].join("\n")+"\n";
const a=event("RUN140-E0001"),b=event("RUN140-E0002");
const getter=(v,k)=>{const x=v.slice();Object.defineProperty(x,k,{get(){throw Error("getter");}});return x;};
const lengthProxy=v=>new Proxy(v,{get(t,k){if(k==="length")throw Error("length");return Reflect.get(t,k);}});
const revoked=()=>{const x=Proxy.revocable([a],{});x.revoke();return x.proxy;};
const cases=[
["single",()=>target([[a]]),"VALID_COHORT_CLAIMS_ONLY",1,1],
["two",()=>target([[a],[b]]),"VALID_COHORT_CLAIMS_ONLY",2,2],
["manual",()=>target([[event("RUN140-E0003",true)]]),"VALID_COHORT_CLAIMS_ONLY",1,0],
["duplicate",()=>target([[a],[a]]),"FAIL_CLOSED",null,null],
["malformed",()=>target([["EVENT_ID=BAD\n"]]),"FAIL_CLOSED",null,null],
["extra_arg",()=>target([[a]],()=>true),"FAIL_CLOSED",null,null],
["inner_getter",()=>target([getter([a],0)]),"FAIL_CLOSED",null,null],
["outer_getter",()=>target(getter([[a]],0)),"FAIL_CLOSED",null,null],
["inner_length",()=>target([lengthProxy([a])]),"FAIL_CLOSED",null,null],
["outer_length",()=>target(lengthProxy([[a]])),"FAIL_CLOSED",null,null],
["revoked_inner",()=>target([revoked()]),"FAIL_CLOSED",null,null],
["revoked_outer",()=>target(revoked()),"FAIL_CLOSED",null,null]];
const failures=[],thrown=[];
for(const [name,fn,status,eligible,automated] of cases){
let v;try{v=fn();}catch(_){thrown.push(name);failures.push(name+":THREW");continue;}
if(!v||v.status!==status||v.eligible_claim_count!==eligible||v.automated_claim_count!==automated||
v.verified_automated_count!=="NOT_ESTABLISHED"||v.projectwide_denominator!=="NOT_COMPUTABLE"||
v.claim_ceiling!=="C1_DESCRIPTIVE_ONLY")failures.push(name+":MISMATCH");
}
return {total:cases.length,pass:cases.length-failures.length,
negative:cases.filter(x=>x[2]==="FAIL_CLOSED").length,
positive:cases.filter(x=>x[2]!=="FAIL_CLOSED").length,
thrown,failures,oracle:"RUN140_FROZEN_PRE_CANDIDATE_C1_ONLY"};
};
