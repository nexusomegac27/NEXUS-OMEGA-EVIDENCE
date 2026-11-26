// Explicitly small synthetic boolean contract; no real IO except stdout.
function run(){
 const keys=["artifact","source_schema","proof_support","transfer_permission","separate_real_grant","identity_action","epoch_fence","stop_clear","reserved_budget","nonce_unused","observer_ready","effect_lease"];
 const gate=(x,skip)=>keys.every(k=>k===skip||x[k]===true);
 let allowed=0,mutants={},unknown={};for(const k of keys)mutants[k]=0;
 for(let m=0;m<2**keys.length;m++){let x=Object.fromEntries(keys.map((k,i)=>[k,!!(m&(1<<i))]));let good=gate(x);if(good)allowed++;for(const k of keys)if(!good&&gate(x,k))mutants[k]++}
 const pos=Object.fromEntries(keys.map(k=>[k,true]));for(const k of keys)unknown[k]=gate({...pos,[k]:null});
 // Model a resource that durably deduplicates request IDs; ACK can be lost independently.
 let resource=new Map(),count=0;
 function commit(req,authorized,loseAck){if(!authorized)return "DENIED";if(!resource.has(req)){resource.set(req,"EFFECT");count++}return loseAck?"UNKNOWN":"RECEIPT"}
 const a=commit("r1",gate(pos),true),before=count;const readback=resource.get("r1");const replay=commit("r1",false,false);const after=count;
 const cases={expired_transfer:gate({...pos,transfer_permission:false}),snapshot_stale_epoch:gate({...pos,epoch_fence:false}),stop_after_grant:gate({...pos,stop_clear:false}),real_grant_absent:gate({...pos,separate_real_grant:false}),fresh_grant:gate(pos),inert_review_no_effect:{terminal:"REVIEW_ELIGIBLE",effects:0},lost_ack:{first:a,before,readback,replay,after},local_snapshot_restore:{local_state:"old",external_effect_still_present:resource.has("r1")}};
 if(allowed!==1||Object.values(mutants).some(v=>v!==1)||Object.values(unknown).some(Boolean)||a!=="UNKNOWN"||before!==after||readback!=="EFFECT")throw Error("contract check");
 return {domain:2**keys.length,allowed,denied:2**keys.length-allowed,mutants,unknown,cases,formal_credit:false,limits:"truth table and toy persistent resource only; no actual authority, signature, concurrency or isolation tested"};
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
