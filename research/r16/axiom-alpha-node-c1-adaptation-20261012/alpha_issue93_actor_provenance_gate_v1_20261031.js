'use strict';
/** Research-only Issue #93 provenance classifier. No external ACK, scientific adjudication or network I/O. */
const OWNER = 'nexusomegac27';
const HEX40 = /^[0-9a-f]{40}$/;
const HEX64 = /^[0-9a-f]{64}$/;
const SCHEMA = 'NEXUS_OMEGA_EXPERT_RETURN_HANDSHAKE_V1';
function extract(body, key) {
  const hits = body.split(/\r?\n/).filter(line => line.startsWith(key + '='));
  return hits.length === 1 ? hits[0].slice(key.length + 1).trim() : null;
}
function classify(comment, registeredActors) {
  if (!comment || typeof comment !== 'object' || Array.isArray(comment) ||
      !comment.user || typeof comment.user.login !== 'string' ||
      !Number.isSafeInteger(comment.id) || comment.id < 1 ||
      typeof comment.body !== 'string' || comment.body.length > 262144 ||
      !Array.isArray(registeredActors) || registeredActors.some(a => typeof a !== 'string')) {
    return {state:'FAIL_CLOSED',reason:'INVALID_API_RECORD'};
  }
  const actor = comment.user.login;
  const body = comment.body;
  if (actor.toLowerCase() === OWNER) {
    return {state:'OWNER_AUTHORED_NOT_INDEPENDENT_RECEIVER',actor,comment_id:comment.id};
  }
  if (!registeredActors.includes(actor)) {
    return {state:'UNREGISTERED_ACTOR_NO_RECEIVER_ACK',actor,comment_id:comment.id};
  }
  const schema = extract(body,'HANDSHAKE_SCHEMA');
  const commit = extract(body,'HEAD_FULL_SHA');
  const digest = extract(body,'RETURN_MANIFEST_SHA256');
  const path = extract(body,'RETURN_MANIFEST_PATH');
  if (schema !== SCHEMA || !HEX40.test(commit || '') || !HEX64.test(digest || '') ||
      !path || !path.startsWith('research/') || path.includes('..') || path.includes('\\') ||
      !path.endsWith('.json')) {
    return {state:'INCOMPLETE_RETURN_HANDSHAKE_NO_RECEIVER_ACK',actor,comment_id:comment.id};
  }
  return {state:'REGISTERED_ACTOR_RETURN_CANDIDATE_BYTES_UNVERIFIED',actor,
          comment_id:comment.id,head_commit:commit,manifest_path:path,
          manifest_sha256_claimed:digest,receiver_ack:'NOT_ESTABLISHED',
          expert_research_executed:'NOT_INDEPENDENTLY_ESTABLISHED'};
}
function census(comments, registeredActors) {
  if (!Array.isArray(comments) || comments.length > 100000 ||
      !Array.isArray(registeredActors) || registeredActors.some(a => typeof a !== 'string')) {
    return {state:'FAIL_CLOSED',reason:'INVALID_CENSUS'};
  }
  const seen = new Set();
  const counts = Object.create(null);
  for (const comment of comments) {
    const result = classify(comment,registeredActors);
    if (result.state === 'FAIL_CLOSED') return result;
    if (seen.has(comment.id)) return {state:'FAIL_CLOSED',reason:'DUPLICATE_COMMENT_ID'};
    seen.add(comment.id);
    counts[result.state] = (counts[result.state] || 0) + 1;
  }
  return {state:'C1_ACTOR_PROVENANCE_CENSUS',denominator:comments.length,
          counts,independent_receiver_acks_established:0,
          source_bytes_verified:0,claim_ceiling:'C1_DESCRIPTIVE_ONLY'};
}
module.exports = {classify,census};
if (require.main === module) {
  try {
    const fs = require('node:fs');
    const data = JSON.parse(fs.readFileSync(0,'utf8'));
    const result = census(data.comments,data.registeredActors);
    process.stdout.write(JSON.stringify(result)+'\n');
    process.exitCode = result.state === 'FAIL_CLOSED' ? 2 : 0;
  } catch (e) {
    process.stdout.write(JSON.stringify({state:'FAIL_CLOSED',reason:'INPUT_PARSE_OR_RUNTIME'})+'\n');
    process.exitCode = 2;
  }
}
