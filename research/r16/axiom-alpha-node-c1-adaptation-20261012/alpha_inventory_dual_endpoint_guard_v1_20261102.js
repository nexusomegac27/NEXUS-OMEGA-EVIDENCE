"use strict";
/* Isolated C1 research candidate. Compare two supplied GitHub metadata views
 * of one pinned directory: Contents API and Git Trees API. The caller MUST
 * authenticate both fetches and bind them to the same immutable commit/tree.
 * This tool does not fetch GitHub, hash file bytes, or prove handoff execution.
 */
function verify(contents, tree) {
  const base={status:"HOLD_SCOPED",reason:"UNKNOWN",
    evidence_class:"SUPPLIED_GITHUB_METADATA_DUAL_ENDPOINT_ONLY",
    project_handoff_rate:"NOT_COMPUTABLE",file_count:null};
  const fail=reason=>({...base,reason});
  if(!Array.isArray(contents)||!tree||!Array.isArray(tree.tree)
     ||typeof tree.truncated!=="boolean") return fail("MISSING_OR_INVALID_INPUT");
  if(tree.truncated) return fail("TRUNCATED_TREE");
  if(contents.length>1000||tree.tree.length>1000) return fail("INPUT_BUDGET_EXCEEDED");
  const cm=new Map(),tm=new Map(),hex=/^[0-9a-f]{40}$/;
  function validName(x) {
    return typeof x==="string"&&x.length>0&&x!=="."&&x!==".."
      &&!x.includes("/")&&!x.includes("\\")&&!x.includes("\0");
  }
  for(const x of contents) {
    if(!x||x.type!=="file") return fail("NON_BLOB_ENTRY");
    if(!validName(x.name)||!hex.test(x.sha||"")
       ||!Number.isSafeInteger(x.size)||x.size<0) return fail("INVALID_ENTRY");
    if(cm.has(x.name)) return fail("DUPLICATE_NAME");
    cm.set(x.name,{sha:x.sha,size:x.size});
  }
  for(const x of tree.tree) {
    if(!x||x.type!=="blob") return fail("NON_BLOB_ENTRY");
    if(!validName(x.path)||!hex.test(x.sha||"")
       ||!Number.isSafeInteger(x.size)||x.size<0) return fail("INVALID_ENTRY");
    if(tm.has(x.path)) return fail("DUPLICATE_NAME");
    tm.set(x.path,{sha:x.sha,size:x.size});
  }
  if(cm.size!==tm.size||[...cm.keys()].some(n=>!tm.has(n)))
    return fail("SET_MISMATCH");
  for(const [name,entry] of cm) {
    const other=tm.get(name);
    if(entry.sha!==other.sha||entry.size!==other.size)
      return fail("IDENTITY_MISMATCH");
  }
  const names=[...cm.keys()];
  return {...base,status:"PASS_METADATA_CROSSCHECK_ONLY",
    reason:"ALL_METADATA_IDENTITIES_MATCH",file_count:names.length,
    python_files:names.filter(n=>n.endsWith(".py")).length,
    frozen_evaluators:names.filter(n=>n.startsWith("frozen_")&&n.endsWith(".py")).length,
    handoff_python:names.filter(n=>n.startsWith("alpha_handoff")&&n.endsWith(".py")).length,
    dated_20261102:names.filter(n=>n.includes("20261102")).length,
    total_declared_blob_bytes:[...cm.values()].reduce((s,x)=>s+x.size,0)};
}
module.exports={verify};
