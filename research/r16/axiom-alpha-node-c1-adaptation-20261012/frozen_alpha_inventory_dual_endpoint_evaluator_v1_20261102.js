"use strict";
/* Frozen independent oracle: metadata-only GitHub Contents vs Git Trees.
 * Commit before the candidate. Never alter to accommodate candidate behavior.
 * No transport authentication, SHA-256 of source bytes, or science promotion.
 */
function runOracle(verify) {
  const A = "a".repeat(40), B = "b".repeat(40);
  const baseContents = [
    {name:"alpha.py",type:"file",sha:A,size:12},
    {name:"frozen_alpha.py",type:"file",sha:B,size:7}
  ];
  const baseTree = {truncated:false,tree:[
    {path:"alpha.py",type:"blob",sha:A,size:12},
    {path:"frozen_alpha.py",type:"blob",sha:B,size:7}
  ]};
  const clone = x => JSON.parse(JSON.stringify(x));
  const cases = [];
  function check(name, change, expectedStatus, expectedReason) {
    const c=clone(baseContents), t=clone(baseTree);
    if(change) change(c,t);
    let got;
    try { got=verify(c,t); } catch(e) {
      cases.push({name,pass:false,error:String(e)}); return;
    }
    const pass=got.status===expectedStatus && got.reason===expectedReason
      && got.project_handoff_rate==="NOT_COMPUTABLE"
      && got.evidence_class==="SUPPLIED_GITHUB_METADATA_DUAL_ENDPOINT_ONLY";
    cases.push({name,pass,status:got.status,reason:got.reason});
  }
  const pass="PASS_METADATA_CROSSCHECK_ONLY", hold="HOLD_SCOPED";
  check("valid_synthetic_two",null,pass,"ALL_METADATA_IDENTITIES_MATCH");
  check("missing_contents_entry",(c)=>c.pop(),hold,"SET_MISMATCH");
  check("missing_tree_entry",(_,t)=>t.tree.pop(),hold,"SET_MISMATCH");
  check("extra_contents_entry",(c)=>c.push({name:"extra.py",type:"file",sha:A,size:2}),hold,"SET_MISMATCH");
  check("changed_blob",(c)=>c[0].sha=B,hold,"IDENTITY_MISMATCH");
  check("changed_size",(c)=>c[0].size=13,hold,"IDENTITY_MISMATCH");
  check("duplicate_contents_name",(c)=>c.push({...c[0]}),hold,"DUPLICATE_NAME");
  check("duplicate_tree_name",(_,t)=>t.tree.push({...t.tree[0]}),hold,"DUPLICATE_NAME");
  check("invalid_sha",(c)=>c[0].sha="bad",hold,"INVALID_ENTRY");
  check("negative_size",(c)=>c[0].size=-1,hold,"INVALID_ENTRY");
  check("truncated_tree",(_,t)=>t.truncated=true,hold,"TRUNCATED_TREE");
  check("directory_in_tree",(_,t)=>t.tree[0].type="tree",hold,"NON_BLOB_ENTRY");
  check("missing_tree",(c,t)=>{t.tree=null;},hold,"MISSING_OR_INVALID_INPUT");
  check("self_consistent_forgery",(c,t)=>{c[0].sha=B;t.tree[0].sha=B;},pass,"ALL_METADATA_IDENTITIES_MATCH");
  return cases;
}
module.exports={runOracle};
if(require.main===module) {
  const verify=require("./alpha_inventory_dual_endpoint_guard_v1_20261102.js").verify;
  const results=runOracle(verify);
  console.log(JSON.stringify({passed:results.filter(x=>x.pass).length,total:results.length,results},null,2));
  process.exit(results.every(x=>x.pass)?0:1);
}
