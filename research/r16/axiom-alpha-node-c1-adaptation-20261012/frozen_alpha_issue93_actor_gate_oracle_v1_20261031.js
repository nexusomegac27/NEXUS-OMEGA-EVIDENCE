'use strict';
/** Frozen black-box adversarial oracle; run against candidate via separate Node process. */
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const path = require('node:path');
const candidate = process.argv[2];
if (!candidate) throw Error('USAGE_CANDIDATE_PATH');
const owner = 'nexusomegac27', registered = 'registered-expert';
const sha40 = 'a'.repeat(40), sha64 = 'b'.repeat(64);
const valid = [
 'HANDSHAKE_SCHEMA=NEXUS_OMEGA_EXPERT_RETURN_HANDSHAKE_V1',
 'HEAD_FULL_SHA='+sha40,
 'RETURN_MANIFEST_SHA256='+sha64,
 'RETURN_MANIFEST_PATH=research/r10/returns/return.json'
].join('\n');
function c(id,actor,body) {return {id,user:{login:actor},body};}
let checks = 0, negatives = 0;
function run(comments,actors=[]) {
 const p=spawnSync(process.execPath,[path.resolve(candidate)],{input:JSON.stringify({comments,registeredActors:actors}),encoding:'utf8',timeout:10000});
 assert.equal(p.error,undefined); assert.equal(p.stderr,'');
 assert.ok([0,2].includes(p.status));
 return {status:p.status,result:JSON.parse(p.stdout)};
}
function expect(comments,actors,expected,fail=false) {
 const {status,result}=run(comments,actors);
 assert.equal(result.state,expected);assert.equal(status,fail?2:0);
 checks++;if (fail) negatives++;
 return result;
}
let r=expect([c(1,owner,valid)],[], 'C1_ACTOR_PROVENANCE_CENSUS');
assert.equal(r.counts.OWNER_AUTHORED_NOT_INDEPENDENT_RECEIVER,1);assert.equal(r.independent_receiver_acks_established,0);
r=expect([c(2,registered,valid)],[], 'C1_ACTOR_PROVENANCE_CENSUS');
assert.equal(r.counts.UNREGISTERED_ACTOR_NO_RECEIVER_ACK,1);
r=expect([c(3,registered,valid)],[registered],'C1_ACTOR_PROVENANCE_CENSUS');
assert.equal(r.counts.REGISTERED_ACTOR_RETURN_CANDIDATE_BYTES_UNVERIFIED,1);assert.equal(r.source_bytes_verified,0);
for(const [id,body] of [
 [4,valid.replace('a'.repeat(40),'z'.repeat(40))],
 [5,valid.replace('b'.repeat(64),'z'.repeat(64))],
 [6,valid.replace('research/r10/returns/return.json','../private.json')],
 [7,valid.replace('return.json','return.zip')],
 [8,valid.replace('HANDSHAKE_SCHEMA','WRONG_SCHEMA')],
 [9,valid+'\nHEAD_FULL_SHA='+sha40],
 [10,'INDEPENDENT_RECEIVER_ACK=MATCH'],
 [11,''],
 ]) {
  r=expect([c(id,registered,body)],[registered],'C1_ACTOR_PROVENANCE_CENSUS');
  assert.equal(r.counts.INCOMPLETE_RETURN_HANDSHAKE_NO_RECEIVER_ACK,1);
}
for(const comments of [
 [c(1,owner,'x'),c(1,owner,'y')],
 [c(0,owner,'x')],
 [{id:1,user:{},body:'x'}],
 [{id:1,user:{login:owner},body:123}],
 [null],
 ]) expect(comments,[],'FAIL_CLOSED',true);
for(const comments of ['bad',null]) expect(comments,[],'FAIL_CLOSED',true);
expect([],null,'FAIL_CLOSED',true);
r=expect([],[],'C1_ACTOR_PROVENANCE_CENSUS');assert.equal(r.denominator,0);
r=expect([c(1,owner,'x'),c(2,registered,valid),c(3,'unknown',valid)],[registered],'C1_ACTOR_PROVENANCE_CENSUS');
assert.equal(r.denominator,3);assert.equal(r.independent_receiver_acks_established,0);
console.log(JSON.stringify({state:'PASS',checks,fail_closed_negatives:negatives,claim_ceiling:'C1_DESCRIPTIVE_ONLY'}));

