'use strict';
// Frozen oracle for a C1-only research scaffold. Do not edit after first commit.
const assert = require('node:assert/strict');
const { auditRequiredChecks } = require('./alpha_required_check_collision_guard_v1_20261102.js');
const SHA = 'a3e8b63ecb52f27cef1177ad2bab86057804bbbb';
const APP = 15368;
const ruleset = {enforcement:'active',conditions:{ref_name:{include:['refs/heads/main'],exclude:[]}},rules:[{type:'required_status_checks',parameters:{required_status_checks:[{context:'validate',integration_id:APP}]}}]};
const run = (id,wf,name='validate',app=APP,head=SHA,conclusion='success') => ({id,name,app:{id:app},head_sha:head,status:'completed',conclusion,workflow_id:wf});
const r1=run(125540118916,346195817);
const r2=run(125540117995,340784261);
const r3=run(125540117930,346197649);
const r4=run(125540117014,346228171);
const cases = [
  ['real-four-colliding-workflows',ruleset,[r1,r2,r3,r4],'HOLD_SCOPED','AMBIGUOUS_REQUIRED_CHECK',4],
  ['single-unique-positive',ruleset,[r1],'PASS_STRUCTURAL_ONLY','UNIQUE_CHECK_DECLARED',1],
  ['missing-check',ruleset,[],'HOLD_SCOPED','REQUIRED_CHECK_MISSING',0],
  ['different-app-only',ruleset,[run(1,1,'validate',42)],'HOLD_SCOPED','REQUIRED_CHECK_MISSING',0],
  ['different-head-only',ruleset,[run(1,1,'validate',APP,'0'.repeat(40))],'HOLD_SCOPED','REQUIRED_CHECK_MISSING',0],
  ['failed-check',ruleset,[run(1,1,'validate',APP,SHA,'failure')],'HOLD_SCOPED','REQUIRED_CHECK_NOT_SUCCESSFUL',1],
  ['skipped-check',ruleset,[run(1,1,'validate',APP,SHA,'skipped')],'HOLD_SCOPED','REQUIRED_CHECK_NOT_SUCCESSFUL',1],
  ['same-check-id-duplicated',ruleset,[r1,r1],'HOLD_SCOPED','DUPLICATE_CHECK_ID',2],
  ['two-workflows-collision',ruleset,[r1,r2],'HOLD_SCOPED','AMBIGUOUS_REQUIRED_CHECK',2],
  ['wrong-name-plus-one-valid',ruleset,[run(1,1,'other'),r1],'PASS_STRUCTURAL_ONLY','UNIQUE_CHECK_DECLARED',1],
  ['wrong-app-plus-one-valid',ruleset,[run(1,1,'validate',42),r1],'PASS_STRUCTURAL_ONLY','UNIQUE_CHECK_DECLARED',1],
  ['unconfigured-ruleset',{...ruleset,enforcement:'disabled'},[r1],'HOLD_SCOPED','RULESET_NOT_ACTIVE',0],
  ['missing-required-checks',{...ruleset,rules:[]},[r1],'HOLD_SCOPED','NO_REQUIRED_CHECK_RULE',0],
  ['invalid-input',ruleset,null,'HOLD_SCOPED','MALFORMED_INPUT',0]
];
let pass=0;
for (const [name,r,checks,status,reason,count] of cases){
  const result=auditRequiredChecks({ruleset:r,checkRuns:checks,targetSha:SHA,ref:'refs/heads/main'});
  assert.equal(result.status,status,`${name}: status`);
  assert.equal(result.reason,reason,`${name}: reason`);
  assert.equal(result.matchCount,count,`${name}: count`);
  console.log(`PASS ${name}: ${result.status}/${result.reason}/${result.matchCount}`); pass++;
}
assert.equal(pass,14);
console.log(`FROZEN_EVALUATOR=14/14_PASS; REAL_SOURCE_FIXTURE=4_COLLIDING_CHECKS; PRODUCTION_CI=UNCHANGED`);
