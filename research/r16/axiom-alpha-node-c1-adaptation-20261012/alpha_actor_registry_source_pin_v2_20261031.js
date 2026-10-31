'use strict';
/** Research-only source-bound actor census; does not establish expert identity or ACK. */
const {createHash} = require('node:crypto');
const {census} = require('./alpha_issue93_actor_provenance_gate_v1_20261031.js');
const REGISTRY_BLOB = '1fabcab7f556e83621a3676ddfb3d11cdd964b55';
const REGISTRY_MAIN = '5df8953165087fabf50aba52eb15e3668f50d940';
function checkedRegistry(raw) {
 if (typeof raw !== 'string' || Buffer.byteLength(raw,'utf8') > 262144) {
  throw Error('REGISTRY_BYTES_MISSING_OR_OVERSIZED');
 }
 const bytes = Buffer.from(raw,'utf8');
 const header = Buffer.from('blob '+bytes.length+'\0');
 const oid = createHash('sha1').update(header).update(bytes).digest('hex');
 if (oid !== REGISTRY_BLOB) throw Error('REGISTRY_SOURCE_PIN_MISMATCH');
 const registry = JSON.parse(raw);
 if (!registry || typeof registry !== 'object' || Array.isArray(registry) ||
     registry.object !== 'NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1' ||
     registry.anchor_repo !== 'nexusomegac27/NEXUS-OMEGA-EVIDENCE' ||
     registry.owner_github_login !== 'nexusomegac27' ||
     registry.default !== 'DENY' ||
     registry.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY' ||
     !Array.isArray(registry.external_actor_allowlist) ||
     registry.external_actor_allowlist.length !== 0) throw Error('REGISTRY_POLICY_MISMATCH');
 return registry.external_actor_allowlist;
}
function run(input) {
 if (!input || typeof input !== 'object' || Array.isArray(input) ||
     Object.keys(input).sort().join(',') !== 'comments,registry_utf8') {
  return {state:'FAIL_CLOSED',reason:'INPUT_SCHEMA_OR_CALLER_ACTOR_OVERRIDE'};
 }
 try {
  const actors=checkedRegistry(input.registry_utf8);
  const result=census(input.comments,actors);
  if (result.state==='FAIL_CLOSED') return result;
  return {...result,registry_git_blob:REGISTRY_BLOB,registry_pinned_main:REGISTRY_MAIN,
          actor_registry_binding:'PINNED_SOURCE_BYTES_NOT_IDENTITY_AUTHENTICATION'};
 } catch (_) {return {state:'FAIL_CLOSED',reason:'REGISTRY_SOURCE_OR_POLICY_UNVERIFIED'};}
}
module.exports={run,checkedRegistry};
if(require.main===module) {
 try {
  const fs=require('node:fs');
  const input=JSON.parse(fs.readFileSync(0,'utf8'));
  const result=run(input);
  process.stdout.write(JSON.stringify(result)+'\n');
  process.exitCode=result.state==='FAIL_CLOSED'?2:0;
 } catch (_) {
  process.stdout.write(JSON.stringify({state:'FAIL_CLOSED',reason:'INPUT_PARSE_OR_RUNTIME'})+'\n');
  process.exitCode=2;
 }
}
