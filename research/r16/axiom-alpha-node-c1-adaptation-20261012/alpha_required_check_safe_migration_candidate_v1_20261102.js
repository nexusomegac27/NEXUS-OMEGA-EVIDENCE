'use strict';
// Research-only patch planner. NO GitHub API calls, ruleset writes, workflow writes, or auto-merge.
const PATHS=[
  '.github/workflows/validate-anchor.yml',
  '.github/workflows/validate-scientific-ledger.yml',
  '.github/workflows/validate-scientific-communication.yml',
  '.github/workflows/validate-a83-framework-hardening.yml'
];
const BLOBS=[
  '3ab2bfecc4949cf23bc9ea1eafeb65c342cf0b0e',
  '787cc06380be6b3981ba2ab0fd20e53cb13881b4',
  '082979fd7531b22873f0a93a8418a5e7d5b6693a',
  'b03b029f7c168ac80ae42f3a40a3ad9481c367a7'
];
const TARGETS=[
  'validate-anchor','validate-scientific-ledger',
  'validate-scientific-communication','validate-a83-framework-hardening'
];
function proposeRequiredCheckMigration({ruleset,workflows,targetContexts}={}) {
  const hold=(reason)=>({status:'HOLD_SCOPED',reason,patches:[],proposedRequiredChecks:[]});
  if(!ruleset||!Array.isArray(workflows)||!Array.isArray(targetContexts)) return hold('MALFORMED_INPUT');
  if(ruleset.enforcement!=='active') return hold('RULESET_NOT_ACTIVE');
  const ref=ruleset.conditions?.ref_name;
  if(!Array.isArray(ref?.include)||!ref.include.includes('refs/heads/main')||!Array.isArray(ref.exclude)||ref.exclude.includes('refs/heads/main')) return hold('REF_SCOPE_MISMATCH');
  const checks=(ruleset.rules||[]).filter(x=>x?.type==='required_status_checks').flatMap(x=>x?.parameters?.required_status_checks||[]);
  if(checks.length!==1||checks[0]?.context!=='validate'||checks[0]?.integration_id!==15368) return hold('REQUIRED_BASELINE_MISMATCH');
  if(workflows.length!==4) return hold('INCOMPLETE_WORKFLOW_POPULATION');
  if(targetContexts.length!==4||targetContexts.some((x,i)=>x!==TARGETS[i])||new Set(targetContexts).size!==4) return hold('UNAPPROVED_TARGET_SET');
  const map=new Map();
  for(const w of workflows) {
    if(!w||typeof w.path!=='string'||map.has(w.path)) return hold('DUPLICATE_OR_INVALID_PATH');
    map.set(w.path,w);
  }
  const patches=[];
  for(let i=0;i<4;i++) {
    const w=map.get(PATHS[i]);
    if(!w||w.sha!==BLOBS[i]||typeof w.content!=='string') return hold('SOURCE_IDENTITY_UNVERIFIED');
    const anchor='jobs:\n  validate:\n';
    if(w.content.split(anchor).length!==2) return hold('AMBIGUOUS_OR_MISSING_JOB_ANCHOR');
    const after=w.content.replace(anchor,'jobs:\n  '+TARGETS[i]+':\n');
    if(after===w.content) return hold('NO_CHANGE');
    patches.push({path:PATHS[i],sourceBlob:BLOBS[i],before:w.content,after:after,requiredContext:TARGETS[i]});
  }
  return {
    status:'PATCH_CANDIDATE_ONLY',
    reason:'FOUR_SOURCE_PINNED_JOB_ID_RENAMES_REQUIRE_SEPARATE_OWNER_RULESET_MIGRATION',
    patches,
    proposedRequiredChecks:TARGETS.map(context=>({context,integration_id:15368})),
    originalRequiredChecks:[{context:'validate',integration_id:15368}],
    liveWorkflowMutation:false,
    liveRulesetMutation:false,
    productionProtectionEstablished:false
  };
}
module.exports={proposeRequiredCheckMigration};
