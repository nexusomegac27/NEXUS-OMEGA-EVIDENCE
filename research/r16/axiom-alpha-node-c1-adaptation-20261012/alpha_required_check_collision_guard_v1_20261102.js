'use strict';
// Isolated C1 research guard; consumes declared API records, makes no network or repo changes.
function auditRequiredChecks({ruleset,checkRuns,targetSha,ref}={}){
  const hold=(reason,matchCount=0,ids=[],workflows=[])=>({status:'HOLD_SCOPED',reason,matchCount,checkIds:ids,workflowIds:workflows});
  if (!ruleset || !Array.isArray(checkRuns) || typeof targetSha!=='string' || !/^[0-9a-f]{40}$/.test(targetSha) || typeof ref!=='string') return hold('MALFORMED_INPUT');
  if (ruleset.enforcement!=='active') return hold('RULESET_NOT_ACTIVE');
  const inc=ruleset.conditions?.ref_name?.include;
  const exc=ruleset.conditions?.ref_name?.exclude||[];
  if (!Array.isArray(inc) || !inc.includes(ref) || !Array.isArray(exc) || exc.includes(ref)) return hold('RULESET_REF_MISMATCH');
  const rules=ruleset.rules;
  if (!Array.isArray(rules)) return hold('NO_REQUIRED_CHECK_RULE');
  const req=rules.filter(x=>x?.type==='required_status_checks').flatMap(x=>x?.parameters?.required_status_checks||[]);
  if (req.length===0) return hold('NO_REQUIRED_CHECK_RULE');
  if (req.length!==1 || typeof req[0]?.context!=='string' || !Number.isInteger(req[0]?.integration_id)) return hold('UNSUPPORTED_REQUIRED_CHECK_SET');
  const {context,integration_id}=req[0];
  const matches=checkRuns.filter(x=>x && x.name===context && x.app?.id===integration_id && x.head_sha===targetSha);
  const ids=matches.map(x=>x.id);
  const workflows=[...new Set(matches.map(x=>x.workflow_id))];
  if (ids.some(x=>!Number.isInteger(x))) return hold('MALFORMED_MATCHING_CHECK',matches.length,ids,workflows);
  if (new Set(ids).size!==ids.length) return hold('DUPLICATE_CHECK_ID',matches.length,ids,workflows);
  if (matches.length===0) return hold('REQUIRED_CHECK_MISSING');
  if (matches.length>1) return hold('AMBIGUOUS_REQUIRED_CHECK',matches.length,ids,workflows);
  if (matches[0].status!=='completed'||matches[0].conclusion!=='success') return hold('REQUIRED_CHECK_NOT_SUCCESSFUL',1,ids,workflows);
  return {status:'PASS_STRUCTURAL_ONLY',reason:'UNIQUE_CHECK_DECLARED',matchCount:1,checkIds:ids,workflowIds:workflows};
}
module.exports={auditRequiredChecks};
