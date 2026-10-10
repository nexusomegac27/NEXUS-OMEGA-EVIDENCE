#!/usr/bin/env node
/**
 * NEXUS OMEGA . R21R1 . WP-G1 . Production fileset manifest verifier.
 * C1_DESCRIPTIVE_ONLY. Fail-closed.
 *
 * Recomputes sha256, byte counts and (optional) git blob sha1 witnesses of the
 * ASTRA-NAV P0 production files from the repository working tree and compares
 * them against validation/r21/r21r1/astra-nav-p0-production-fileset-manifest.json.
 * Any structural defect or mismatch exits with code 1 and a stable error code.
 * A green run of this script is a fileset proof, NOT a deployment proof.
 */
import fs from 'node:fs';
import crypto from 'node:crypto';

const MANIFEST_PATH = 'validation/r21/r21r1/astra-nav-p0-production-fileset-manifest.json';
const ROUTE_PATH_RE = /^\/orbis\/astra-nav\/[a-z0-9._-]+$/;
const SHA256_RE = /^[a-f0-9]{64}$/;
const SHA1_RE = /^[a-f0-9]{40}$/;
const COMMIT_RE = /^[a-f0-9]{40}$/;
const SOURCE_PREFIX = 'examples/r21/astra-nav-p0/';

function fail(code, detail) {
  console.error('FAIL: ' + code + (detail ? ' | ' + detail : ''));
  process.exit(1);
}

let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
} catch (e) {
  fail('MANIFEST_NOT_READABLE', MANIFEST_PATH);
}

if (manifest.schema_version !== 'nexus-r21r1-production-fileset-manifest/v1') fail('INVALID_MANIFEST_CONTRACT');
if (manifest.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY') fail('CLAIM_CEILING_VIOLATION');
if (manifest.scope !== 'ADDITIVE_ORBIS_ASTRA_NAV_ONLY') fail('SCOPE_CLASS_VIOLATION');
if (typeof manifest.source_commit !== 'string' || !COMMIT_RE.test(manifest.source_commit)) fail('BAD_SOURCE_COMMIT');
if (!Array.isArray(manifest.files) || manifest.files.length < 4) fail('BAD_FILESET');

const seen = new Set();
for (const f of manifest.files) {
  if (!f || typeof f !== 'object' || Array.isArray(f)) fail('BAD_FILE_ENTRY');
  if (typeof f.route_relative_path !== 'string' || !ROUTE_PATH_RE.test(f.route_relative_path)) {
    fail('ROUTE_PATH_OUT_OF_SCOPE', String(f.route_relative_path));
  }
  if (typeof f.source_repo_path !== 'string' || !f.source_repo_path.startsWith(SOURCE_PREFIX)) {
    fail('SOURCE_PATH_OUT_OF_SCOPE', String(f.source_repo_path));
  }
  if (typeof f.sha256 !== 'string' || !SHA256_RE.test(f.sha256)) fail('BAD_SHA256', String(f.route_relative_path));
  if (!Number.isSafeInteger(f.bytes) || f.bytes < 1) fail('BAD_BYTES', String(f.route_relative_path));
  if (seen.has(f.route_relative_path)) fail('DUPLICATE_ROUTE_PATH', String(f.route_relative_path));
  seen.add(f.route_relative_path);

  let buf;
  try {
    buf = fs.readFileSync(f.source_repo_path);
  } catch (e) {
    fail('SOURCE_FILE_NOT_READABLE', String(f.source_repo_path));
  }

  const actualSha256 = crypto.createHash('sha256').update(buf).digest('hex');
  if (actualSha256 !== f.sha256) fail('SHA256_MISMATCH', String(f.source_repo_path));
  if (buf.length !== f.bytes) {
    fail('BYTE_COUNT_MISMATCH', String(f.source_repo_path) + ' expected=' + f.bytes + ' actual=' + buf.length);
  }

  const w = f.byte_verification_witness;
  if (w && w.method === 'GIT_BLOB_SHA1_RECONSTRUCTION' && typeof w.git_blob_sha1 === 'string') {
    if (!SHA1_RE.test(w.git_blob_sha1)) fail('BAD_WITNESS_SHA1', String(f.route_relative_path));
    const actualBlobSha1 = crypto.createHash('sha1')
      .update('blob ' + buf.length + '\u0000')
      .update(buf)
      .digest('hex');
    if (actualBlobSha1 !== w.git_blob_sha1) fail('GIT_BLOB_SHA1_MISMATCH', String(f.source_repo_path));
  }
}

console.log('PASS: ASTRA-NAV P0 production fileset manifest verified against repository bytes');
console.log('  files=' + manifest.files.length + ' scope=' + manifest.scope + ' source_commit=' + manifest.source_commit);
console.log('  note: fileset proof only; Hostinger write and public readback remain separate proofs (C1)');
