'use strict';
// Frozen before candidate publication. Research-only migration oracle; no GitHub write or runtime action.
function runTests(plan) {
  const paths = [
    '.github/workflows/validate-anchor.yml',
    '.github/workflows/validate-scientific-ledger.yml',
    '.github/workflows/validate-scientific-communication.yml',
    '.github/workflows/validate-a83-framework-hardening.yml'
  ];
  const blobs = [
    '3ab2bfecc4949cf23bc9ea1eafeb65c342cf0b0e',
    '787cc06380be6b3981ba2ab0fd20e53cb13881b4',
    '082979fd7531b22873f0a93a8418a5e7d5b6693a',
    'b03b029f7c168ac80ae42f3a40a3ad9481c367a7'
  ];
  const targets = [
    'validate-anchor', 'validate-scientific-ledger',
    'validate-scientific-communication', 'validate-a83-framework-hardening'
  ];
  const ruleset = {
    enforcement: 'active',
    conditions: {ref_name: {include: ['refs/heads/main'], exclude: []}},
    rules: [{type: 'required_status_checks', parameters: {
      required_status_checks: [{context: 'validate', integration_id: 15368}]
    }}]
  };
  const workflows = paths.map((path,i)=>({
    path, sha:blobs[i],
    content:'name: '+targets[i]+'\n\non:\n  pull_request:\n\njobs:\n  validate:\n    runs-on: ubuntu-24.04\n'
  }));
  const input = {ruleset, workflows, targetContexts:targets};
  const clone = x=>JSON.parse(JSON.stringify(x));
  const tests = [
    ['positive-four-unique-patches', input, 'PATCH_CANDIDATE_ONLY'],
    ['missing-fourth-workflow', {...input,workflows:workflows.slice(0,3)}, 'HOLD_SCOPED'],
    ['duplicate-path', {...input,workflows:[...workflows.slice(0,3),workflows[0]]}, 'HOLD_SCOPED'],
    ['wrong-blob-id', {...input,workflows:workflows.map((w,i)=>i===2?{...w,sha:'0'.repeat(40)}:w)}, 'HOLD_SCOPED'],
    ['job-id-not-found', {...input,workflows:workflows.map((w,i)=>i===1?{...w,content:w.content.replace('  validate:', '  other:')}:w)}, 'HOLD_SCOPED'],
    ['duplicate-job-anchor', {...input,workflows:workflows.map((w,i)=>i===1?{...w,content:w.content+'jobs:\n  validate:\n'}:w)}, 'HOLD_SCOPED'],
    ['missing-required-rule', {...input,ruleset:{...ruleset,rules:[]}}, 'HOLD_SCOPED'],
    ['wrong-required-app', {...input,ruleset:{...ruleset,rules:[{type:'required_status_checks',parameters:{required_status_checks:[{context:'validate',integration_id:99}]}}]}}, 'HOLD_SCOPED'],
    ['inactive-ruleset', {...input,ruleset:{...ruleset,enforcement:'disabled'}}, 'HOLD_SCOPED'],
    ['wrong-ref', {...input,ruleset:{...ruleset,conditions:{ref_name:{include:['refs/heads/other'],exclude:[]}}}}, 'HOLD_SCOPED'],
    ['extra-required-check', {...input,ruleset:{...ruleset,rules:[{type:'required_status_checks',parameters:{required_status_checks:[{context:'validate',integration_id:15368},{context:'other',integration_id:15368}]}}]}}, 'HOLD_SCOPED'],
    ['target-omitted', {...input,targetContexts:targets.slice(0,3)}, 'HOLD_SCOPED'],
    ['target-duplicate', {...input,targetContexts:[targets[0],targets[0],targets[2],targets[3]]}, 'HOLD_SCOPED'],
    ['target-wrong-name', {...input,targetContexts:[targets[0],targets[1],targets[2],'validate-unapproved']}, 'HOLD_SCOPED'],
    ['malformed-workflows', {...input,workflows:null}, 'HOLD_SCOPED'],
    ['malformed-ruleset', {...input,ruleset:null}, 'HOLD_SCOPED']
  ];
  let pass=0;
  for (const [label,caseInput,expected] of tests) {
    const got=plan(clone(caseInput));
    if (got.status!==expected) throw Error(label+': expected '+expected+', got '+JSON.stringify(got));
    if (expected==='PATCH_CANDIDATE_ONLY') {
      if(got.patches.length!==4 || got.proposedRequiredChecks.length!==4) throw Error(label+': incomplete proposal');
      for(let i=0;i<4;i++){
        const patch=got.patches[i];
        if(patch.path!==paths[i]) throw Error(label+': wrong path');
        if(patch.after!==workflows[i].content.replace('jobs:\n  validate:\n','jobs:\n  '+targets[i]+':\n')) throw Error(label+': unrelated content changed');
        if(patch.before!==workflows[i].content) throw Error(label+': original altered');
      }
    }
    pass++;
  }
  return {passed:pass,total:tests.length,negative:tests.length-1,baselineDuplicateContextCount:4,proposedDistinctContextCount:4};
}
module.exports={runTests};
