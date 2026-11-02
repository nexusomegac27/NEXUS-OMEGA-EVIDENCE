"use strict";
// Frozen independent structural oracle. Input is a declared API projection, NOT authenticated raw bytes.
const TARGETS=["validate-anchor","validate-scientific-ledger","validate-scientific-communication","validate-a83-framework-hardening"];
const OBJECT="NEXUS_OMEGA_ALPHA_REQUIRED_CHECK_LIVE_READINESS_PREFLIGHT_20261103_R0";
const hex=(s,n)=>typeof s==="string"&&new RegExp("^[0-9a-f]{"+n+"}$").test(s);
function assess(x){
 const fail=(reason,counts)=>({decision:"NOT_COMPUTABLE",reason,...(counts?{counts}:{})});
 if(!x||x.object!==OBJECT||!hex(x.parent_main,40))return fail("OBJECT_OR_MAIN_INVALID");
 if(JSON.stringify(x.proposed_targets)!==JSON.stringify(TARGETS))return fail("TARGET_SET_MISMATCH");
 const ss=x.sources;
 if(!ss||JSON.stringify(Object.keys(ss).sort())!==JSON.stringify(["main","pr_head","r10","ruleset"]))return fail("SOURCE_SET_MISMATCH");
 for(const [k,s] of Object.entries(ss)){
  if(!s||typeof s.url!=="string"||!s.url.startsWith("https://")||!Number.isSafeInteger(s.api_response_utf8_bytes)||s.api_response_utf8_bytes<=0||!hex(s.api_response_sha256,64))return fail("SOURCE_METADATA_INVALID:"+k);
 }
 const r=ss.ruleset;
 if(r.ruleset_id!==21252293||r.enforcement!=="active"||JSON.stringify(r.required)!==JSON.stringify([{context:"validate",integration_id:15368}]))return fail("RULESET_DRIFT");
 const counts={};
 for(const label of ["pr_head","main"]){
  const s=ss[label];
  if(!hex(s.commit,40)||(label==="main"&&s.commit!==x.parent_main))return fail("COMMIT_INVALID:"+label);
  if(!Array.isArray(s.checks)||!Number.isSafeInteger(s.total_count)||s.checks.length!==s.total_count||s.total_count<1)return fail("INCOMPLETE_CENSUS:"+label);
  const ids=new Set();
  for(const q of s.checks){
   if(!q||!Number.isSafeInteger(q.id)||q.id<=0||ids.has(q.id)||typeof q.name!=="string"||!q.name||!Number.isSafeInteger(q.app_id)||!["completed","queued","in_progress"].includes(q.status)||!(typeof q.conclusion==="string"||q.conclusion===null))return fail("INVALID_CHECK_RECORD:"+label);
   ids.add(q.id);
  }
  const observed=TARGETS.map(t=>s.checks.filter(q=>q.name===t));
  counts[label]={total_checks:s.total_count,legacy_validate:s.checks.filter(q=>q.name==="validate"&&q.app_id===15368).length,target_present:observed.filter(a=>a.length>0).length,target_success:observed.filter(a=>a.length===1&&a[0].app_id===15368&&a[0].status==="completed"&&a[0].conclusion==="success").length};
  if(observed.some(a=>a.length>1))return {decision:"NOT_READY",reason:"DUPLICATE_TARGET:"+label,counts};
 }
 if(Object.values(counts).some(q=>q.target_success!==4))return {decision:"NOT_READY",reason:"TARGET_CHECKS_NOT_VERIFIED",counts};
 return {decision:"STRUCTURAL_PREFLIGHT_ONLY",reason:"NO_MIGRATION_AUTHORITY",counts};
}
function runTests(){
 const s={object:OBJECT,parent_main:"a".repeat(40),proposed_targets:TARGETS.slice(),sources:{
 ruleset:{url:"https://api.github.com/rules",api_response_utf8_bytes:1,api_response_sha256:"b".repeat(64),ruleset_id:21252293,enforcement:"active",required:[{context:"validate",integration_id:15368}]},
 r10:{url:"https://raw.githubusercontent.com/r10",api_response_utf8_bytes:1,api_response_sha256:"b".repeat(64)}
 }};
 for(const label of ["main","pr_head"])s.sources[label]={url:"https://api.github.com/"+label,api_response_utf8_bytes:1,api_response_sha256:"b".repeat(64),commit:(label==="main"?"a":"c").repeat(40),total_count:4,checks:TARGETS.map((name,i)=>({id:i+1,name,app_id:15368,status:"completed",conclusion:"success"}))};
 if(assess(s).decision!=="STRUCTURAL_PREFLIGHT_ONLY")throw Error("positive failed");
 const mutations=[
 x=>x.object="wrong",x=>x.parent_main="short",x=>x.proposed_targets.pop(),
 x=>delete x.sources.r10,x=>x.sources.r10.api_response_sha256="bad",
 x=>x.sources.ruleset.enforcement="disabled",x=>x.sources.ruleset.required=[],
 x=>x.sources.main.commit="d".repeat(40),x=>x.sources.main.total_count=5,
 x=>x.sources.main.checks[1].id=1,x=>x.sources.main.checks[1].name="validate",
 x=>x.sources.main.checks[1].app_id=9,x=>x.sources.main.checks[1].conclusion="failure",
 x=>x.sources.main.checks[1].status="in_progress",
 x=>{x.sources.main.checks.push({...x.sources.main.checks[0],id:9});x.sources.main.total_count++;}
 ];
 mutations.forEach((m,i)=>{const x=JSON.parse(JSON.stringify(s));m(x);if(assess(x).decision==="STRUCTURAL_PREFLIGHT_ONLY")throw Error("negative accepted "+i);});
 return {passed:mutations.length+1,total:mutations.length+1,negative:mutations.length};
}
if(typeof module!=="undefined")module.exports={assess,runTests,TARGETS};
