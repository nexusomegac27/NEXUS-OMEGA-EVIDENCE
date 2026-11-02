"use strict";
/* Frozen BEFORE V4 candidate. C1 bounded cohort 274-283; no network, no runtime.
   This is a separate JS structural oracle, not third-party scientific validation.
   The expected source was GitHub Contents on immutable main 558dd66d...
   blob 2f4dbfa8b05a073d5fd939b5fc779a2734f65fdd (19301 bytes).
*/
const MERGES = [
"3cc35487e8cae54aeac95377b6a8c376f412dc4f",
"3fef33f230f5cfbec75167811d0a12787f1847db",
"71feb351c3e2436344a10b22b53ba19c946d73df",
"b23cf96871608a18d21350f9c3df0fb075d9cec1",
"265d760ce6a1e0e0bf4e526e48881d9ef55e3144",
"9e5110ce84f2bd63bad1882d80a7ee6a219b448d",
"c1aee5da5015e1108ceab049c7031180978c109d",
"4e22d346006b67de332bfeb1f0ea68db8412fd70",
"b7f966a886c88e015ac49f32efdf4bf7e31f1fea",
"7961026bf0f630aee160e083122c2900744d2da1"];
const FIRST_PARENT="964fe47c4bdbad599e0689b132ff73c0822f3518";
const COUNTS=[5,5,5,3,3,3,3,3,3,3];
const ROOT="research/r16/axiom-alpha-node-c1-adaptation-20261012/";
const hex=(s,n)=>typeof s==="string"&&new RegExp("^[0-9a-f]{"+n+"}$").test(s);
const clone=x=>JSON.parse(JSON.stringify(x));
function baseline(d){
 if(!d||typeof d!=="object"||Array.isArray(d)||d.claim_ceiling!=="C1_DESCRIPTIVE_ONLY"||
 d.pinned_main!==MERGES[9]||d.cohort?.start_pr!==274||d.cohort?.end_pr!==283||
 d.cohort?.selection!=="EXPLICIT_BOUNDED_NOT_PROJECT_WIDE"||!Array.isArray(d.limitations)||
 !d.limitations.includes("NOT_PROJECT_WIDE")||!d.limitations.includes("NO_ACTOR_AUTHENTICATION")||
 !Array.isArray(d.prs)||d.prs.length!==10)return false;
 const paths=new Set(),receipts=new Set();
 for(let i=0;i<10;i++){
  const p=d.prs[i];
  if(!p||p.number!==274+i||p.merged!==true||p.merge_commit!==MERGES[i]||
  p.parent_commit!==(i?MERGES[i-1]:FIRST_PARENT)||!Number.isInteger(p.receipt_id)||
  receipts.has(p.receipt_id)||!Array.isArray(p.files)||p.files.length!==COUNTS[i])return false;
  receipts.add(p.receipt_id);
  for(const f of p.files){
   if(!f||typeof f.path!=="string"||!f.path.startsWith(ROOT)||paths.has(f.path)||
   !Number.isInteger(f.bytes)||f.bytes<=0||!hex(f.sha256,64)||!hex(f.git_blob_sha1,40)||
   f.github_blob_sha1!==f.git_blob_sha1||f.independent_byte_check!==true)return false;
   paths.add(f.path);
  }
 }
 return true;
}
function cases(source){
 const out=[{name:"actual_manifest_positive",d:clone(source),old:true,next:true}];
 for(let i=0;i<10;i++)for(let j=0;j<source.prs[i].files.length;j++){
  const a=clone(source),f=a.prs[i].files[j];
  f.sha256="f".repeat(64);f.git_blob_sha1="e".repeat(40);f.github_blob_sha1="e".repeat(40);
  out.push({name:"coforged_hashes_"+i+"_"+j,d:a,old:true,next:false});
  const b=clone(source);b.prs[i].files[j].bytes+=1;
  out.push({name:"altered_byte_count_"+i+"_"+j,d:b,old:true,next:false});
 }
 const c=clone(source);c.claim_ceiling="C2";out.push({name:"claim_promotion",d:c,old:false,next:false});
 const m=clone(source);m.prs[3].parent_commit="0".repeat(40);out.push({name:"broken_middle_edge",d:m,old:false,next:false});
 const o=clone(source);o.prs[0].files.pop();out.push({name:"missing_file",d:o,old:false,next:false});
 return out;
}
function run(source,candidate){
 const cs=cases(source);let baseline_pass=0,candidate_pass=0,baseline_detect=0,candidate_detect=0,failures=[];
 for(const c of cs){
  const b=baseline(c.d),n=candidate(c.d);
  if(b===c.old)baseline_pass++;else failures.push("baseline:"+c.name);
  if(n===c.next)candidate_pass++;else failures.push("candidate:"+c.name);
  if(c.old===true&&c.next===false){baseline_detect+=!b?1:0;candidate_detect+=!n?1:0;}
 }
 return {cases:cs.length,baseline_expected:baseline_pass,candidate_expected:candidate_pass,
  new_negative_cases:72,baseline_new_rejected:baseline_detect,candidate_new_rejected:candidate_detect,
  failures,source_scope:"PINNED_COHORT_274_283_ONLY",scientific_independence:"NOT_ESTABLISHED"};
}
module.exports={baseline,cases,run};
