'use strict';
/** Frozen external black-box oracle: execute V1 and V2 in distinct Node processes. */
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const [baseline,candidate,registryFile] = process.argv.slice(2);
if (!baseline || !candidate || !registryFile) throw Error('USAGE_BASELINE_CANDIDATE_REGISTRY');
const raw = fs.readFileSync(registryFile,'utf8');
const handshake = ['HANDSHAKE_SCHEMA=NEXUS_OMEGA_EXPERT_RETURN_HANDSHAKE_V1',
 'HEAD_FULL_SHA='+'a'.repeat(40), 'RETURN_MANIFEST_SHA256='+'b'.repeat(64),
 'RETURN_MANIFEST_PATH=research/r10/returns/return.json'].join('\n');
const actor = 'fabricated-expert';
const comment = (id,login,body=handshake) => ({id,user:{login},body});
function run(file, input) {
 const p = spawnSync(process.execPath,[path.resolve(file)],{
  input:JSON.stringify(input),encoding:'utf8',timeout:10000});
 assert.equal(p.error,undefined); assert.equal(p.stderr,'');
 assert.ok([0,2].includes(p.status));
 const result=JSON.parse(p.stdout);
 assert.equal(p.status,result.state==='FAIL_CLOSED'?2:0);
 return result;
}
let checks=0,negatives=0;
function expect(input,state,counts={},fail=false) {
 const r=run(candidate,input);
 assert.equal(r.state,state);
 for (const [k,v] of Object.entries(counts)) assert.equal(r.counts[k],v);
 checks++; if(fail) negatives++;
 return r;
}
const v1=run(baseline,{comments:[comment(1,actor)],registeredActors:[actor]});
assert.equal(v1.counts.REGISTERED_ACTOR_RETURN_CANDIDATE_BYTES_UNVERIFIED,1);
checks++;
const standard={registry_utf8:raw,comments:[comment(1,actor)]};
let r=expect(standard,'C1_ACTOR_PROVENANCE_CENSUS',{UNREGISTERED_ACTOR_NO_RECEIVER_ACK:1});
assert.equal(r.denominator,1);assert.equal(r.independent_receiver_acks_established,0);
r=expect({registry_utf8:raw,comments:[comment(2,'nexusomegac27'),comment(3,actor)]},
 'C1_ACTOR_PROVENANCE_CENSUS',{OWNER_AUTHORED_NOT_INDEPENDENT_RECEIVER:1,UNREGISTERED_ACTOR_NO_RECEIVER_ACK:1});
assert.equal(r.denominator,2);
r=expect({registry_utf8:raw,comments:[]},'C1_ACTOR_PROVENANCE_CENSUS');
assert.equal(r.denominator,0);
const forged=raw.replace('"external_actor_allowlist": []','"external_actor_allowlist": ["'+actor+'"]');
assert.notEqual(forged,raw);
for(const input of [
 {registry_utf8:forged,comments:[comment(1,actor)]},
 {registry_utf8:raw.replace('"default": "DENY"','"default": "ALLOW"'),comments:[]},
 {registry_utf8:raw.slice(0,-1),comments:[]},
 {registry_utf8:raw+' ',comments:[]},
 {registry_utf8:raw,comments:[comment(1,actor)],registeredActors:[actor]},
 {registry_utf8:raw,comments:[comment(1,actor),comment(1,actor)]},
 {registry_utf8:raw,comments:[{id:1,user:{},body:handshake}]},
 {registry_utf8:raw,comments:'bad'},
 {registry_utf8:null,comments:[]},
 {comments:[]},
 {registry_utf8:raw,comments:[comment(0,actor)]},
 ]) expect(input,'FAIL_CLOSED',{},true);
console.log(JSON.stringify({state:'PASS',checks,fail_closed_negatives:negatives,
 baseline_forged_registry_candidates:1,after_forged_registry_candidates:0,
 claim_ceiling:'C1_DESCRIPTIVE_ONLY'}));
