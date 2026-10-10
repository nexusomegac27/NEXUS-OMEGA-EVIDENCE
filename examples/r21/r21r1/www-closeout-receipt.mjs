/**
 * NEXUS OMEGA . R21R1 . WP-G1 . Source-bound 3-proof WWW closeout receipt validator.
 * C1_DESCRIPTIVE_ONLY. Mirrors schema/r21/r21r1/www-closeout-receipt.schema.json.
 * WWW_LIVE_VERIFIED is only valid with all three separated proofs:
 * (A) ACTUAL_PRODUCTION_FILESET_HASH, (B) HOSTINGER_SCOPED_WRITE_RECEIPT,
 * (C) INDEPENDENT_PUBLIC_BROWSER_AND_HTTP_READBACK.
 * This validator checks structural completeness; physical truth requires Cursor receipts.
 */

export const CLOSEOUT_SCHEMA_VERSION = 'nexus-r21r1-www-closeout/v1';

const SHA256 = /^[a-f0-9]{64}$/;
const COMMIT = /^[a-f0-9]{40}$/;
const ROUTE_PATH = /^\/orbis\/astra-nav\/[a-z0-9._-]+$/;
const READBACK_URL = 'https://www.nexus-mobile.de/orbis/astra-nav/';

const ROOT_KEYS = new Set(['schema_version', 'object_id', 'claim_ceiling', 'nexus_link_verified', 'terminal_state', 'production_fileset', 'hostinger_scoped_write', 'independent_public_readback', 'material_caveats', 'source_lineage']);
const FILESET_KEYS = new Set(['state', 'source_commit', 'files', 'scope_class', 'rollback_witness', 'observed_utc']);
const FILE_KEYS = new Set(['route_relative_path', 'expected_sha256', 'bytes']);
const WRITE_KEYS = new Set(['state', 'source_commit', 'writer_role', 'write_receipt_id', 'file_hashes_match', 'observed_utc']);
const READBACK_KEYS = new Set(['state', 'url', 'independent_reviewer', 'observed_utc', 'http_body_sha256', 'browser_map_tiles_visible', 'attribution_visible', 'desktop_mobile_pass', 'r19_regression_pass', 'asset_sha256_receipt']);

function nonEmpty(x) { return typeof x === 'string' && x.trim().length > 0; }
function checkKeys(obj, allowed, label) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) throw new Error('BAD_' + label);
  for (const k of Object.keys(obj)) if (!allowed.has(k)) throw new Error('UNEXPECTED_FIELD');
}
function stateOf(s) { if (!['PASS', 'PENDING', 'FAIL'].includes(s)) throw new Error('BAD_STATE'); return s; }

function validateFileEntry(f) {
  checkKeys(f, FILE_KEYS, 'FILE_ENTRY');
  if (typeof f.route_relative_path !== 'string' || !ROUTE_PATH.test(f.route_relative_path)) throw new Error('ROUTE_PATH_OUT_OF_SCOPE');
  if (typeof f.expected_sha256 !== 'string' || !SHA256.test(f.expected_sha256)) throw new Error('BAD_SHA256');
  if (!Number.isSafeInteger(f.bytes) || f.bytes < 0) throw new Error('BAD_BYTES');
  return f;
}

function validateFileset(s) {
  checkKeys(s, FILESET_KEYS, 'PRODUCTION_FILESET');
  stateOf(s.state);
  if (typeof s.source_commit !== 'string' || !COMMIT.test(s.source_commit)) throw new Error('BAD_SOURCE_COMMIT');
  if (!Array.isArray(s.files)) throw new Error('BAD_FILESET');
  for (const f of s.files) validateFileEntry(f);
  if (s.scope_class !== 'ADDITIVE_ORBIS_ASTRA_NAV_ONLY') throw new Error('SCOPE_CLASS_VIOLATION');
  if (s.rollback_witness !== null && typeof s.rollback_witness !== 'string') throw new Error('BAD_ROLLBACK_WITNESS');
  if (s.observed_utc !== null && s.observed_utc !== undefined && typeof s.observed_utc !== 'string') throw new Error('BAD_OBSERVED_UTC');
  return s;
}

function validateWrite(w) {
  checkKeys(w, WRITE_KEYS, 'HOSTINGER_WRITE');
  stateOf(w.state);
  if (w.source_commit !== null && !(typeof w.source_commit === 'string' && COMMIT.test(w.source_commit))) throw new Error('BAD_SOURCE_COMMIT');
  if (w.writer_role !== null && typeof w.writer_role !== 'string') throw new Error('BAD_WRITER_ROLE');
  if (w.write_receipt_id !== null && typeof w.write_receipt_id !== 'string') throw new Error('BAD_WRITE_RECEIPT_ID');
  if (w.file_hashes_match !== null && typeof w.file_hashes_match !== 'boolean') throw new Error('BAD_FILE_HASH_MATCH');
  if (w.observed_utc !== null && typeof w.observed_utc !== 'string') throw new Error('BAD_OBSERVED_UTC');
  return w;
}

function validateReadback(r) {
  checkKeys(r, READBACK_KEYS, 'PUBLIC_READBACK');
  stateOf(r.state);
  if (r.url !== READBACK_URL) throw new Error('READBACK_URL_OUT_OF_SCOPE');
  if (r.independent_reviewer !== null && typeof r.independent_reviewer !== 'string') throw new Error('BAD_REVIEWER');
  if (r.observed_utc !== null && typeof r.observed_utc !== 'string') throw new Error('BAD_OBSERVED_UTC');
  if (r.http_body_sha256 !== null && !(typeof r.http_body_sha256 === 'string' && SHA256.test(r.http_body_sha256))) throw new Error('BAD_SHA256');
  for (const k of ['browser_map_tiles_visible', 'attribution_visible', 'desktop_mobile_pass', 'r19_regression_pass']) {
    if (r[k] !== null && typeof r[k] !== 'boolean') throw new Error('BAD_READBACK_FLAG');
  }
  if (r.asset_sha256_receipt !== null && typeof r.asset_sha256_receipt !== 'string') throw new Error('BAD_ASSET_RECEIPT');
  return r;
}

export function validateCloseoutReceipt(receipt) {
  checkKeys(receipt, ROOT_KEYS, 'RECEIPT');
  if (receipt.schema_version !== CLOSEOUT_SCHEMA_VERSION) throw new Error('BAD_SCHEMA_VERSION');
  if (typeof receipt.object_id !== 'string' || receipt.object_id.length < 10) throw new Error('BAD_OBJECT_ID');
  if (receipt.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY') throw new Error('CLAIM_CEILING_VIOLATION');
  if (receipt.nexus_link_verified !== false) throw new Error('NEXUS_LINK_PROMOTION_REJECTED');
  if (receipt.terminal_state !== 'NOT_LIVE_VERIFIED' && receipt.terminal_state !== 'WWW_LIVE_VERIFIED') throw new Error('BAD_TERMINAL_STATE');
  validateFileset(receipt.production_fileset);
  validateWrite(receipt.hostinger_scoped_write);
  validateReadback(receipt.independent_public_readback);
  if (receipt.material_caveats !== undefined && (!Array.isArray(receipt.material_caveats) || receipt.material_caveats.some(c => typeof c !== 'string'))) throw new Error('BAD_CAVEATS');
  if (receipt.source_lineage !== undefined && (!Array.isArray(receipt.source_lineage) || receipt.source_lineage.some(c => typeof c !== 'string'))) throw new Error('BAD_LINEAGE');
  if (receipt.terminal_state === 'WWW_LIVE_VERIFIED') {
    const fsx = receipt.production_fileset;
    if (fsx.state !== 'PASS' || fsx.files.length < 4 || typeof fsx.rollback_witness !== 'string' || fsx.rollback_witness.length < 8 || typeof fsx.observed_utc !== 'string') throw new Error('LIVE_CLAIM_WITHOUT_COMPLETE_FILESET_PROOF');
    const w = receipt.hostinger_scoped_write;
    if (w.state !== 'PASS' || typeof w.source_commit !== 'string' || !COMMIT.test(w.source_commit) || !nonEmpty(w.writer_role) || typeof w.write_receipt_id !== 'string' || w.write_receipt_id.length < 8 || w.file_hashes_match !== true || typeof w.observed_utc !== 'string') throw new Error('LIVE_CLAIM_WITHOUT_SCOPED_WRITE_RECEIPT');
    const rb = receipt.independent_public_readback;
    if (rb.state !== 'PASS' || !nonEmpty(rb.independent_reviewer) || typeof rb.observed_utc !== 'string' || typeof rb.http_body_sha256 !== 'string' || !SHA256.test(rb.http_body_sha256) || rb.browser_map_tiles_visible !== true || rb.attribution_visible !== true || rb.desktop_mobile_pass !== true || rb.r19_regression_pass !== true || typeof rb.asset_sha256_receipt !== 'string' || rb.asset_sha256_receipt.length < 8) throw new Error('LIVE_CLAIM_WITHOUT_INDEPENDENT_READBACK');
  }
  return receipt;
}

export function isLiveVerifiedEligible(receipt) {
  try { validateCloseoutReceipt(receipt); } catch (e) { return false; }
  return receipt.terminal_state === 'WWW_LIVE_VERIFIED';
}
