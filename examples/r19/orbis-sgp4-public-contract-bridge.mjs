/**
 * NEXUS OMEGA · R19/R21R1 · SGP4 → public manifest POSITION adapter.
 * Governs a separately executed satellite.js build; it DOES NOT propagate,
 * admit a slot, fetch a satellite, navigate a handset, or write a website.
 * Original OMM response bytes are REQUIRED: hashing an object serialized back
 * to JSON is not source-exact proof. Pure, deterministic, fail-closed.
 */
import { createHash } from 'node:crypto';

const CAT = /^[0-9]{1,9}$/;
const DIGEST = /^[a-f0-9]{64}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const POSITION_KEYS = Object.freeze([
  'data_class', 'lat_deg', 'lng_deg', 'alt_km', 'element_epoch_utc',
  'target_utc', 'calculated_utc', 'model', 'source_sha256', 'model_version'
]);

function requireC1(ok, id) {
  if (!ok) throw new Error('ORBIS_R19_BRIDGE_HOLD_' + id);
}
function dateMs(value, id) {
  requireC1(typeof value === 'string' && UTC.test(value), id + '_UTC_FORMAT');
  const ms = Date.parse(value);
  requireC1(Number.isFinite(ms) && new Date(ms).toISOString() ===
    new Date(value).toISOString(), id + '_UTC_VALUE');
  return ms;
}
function exactBytes(originalOmmBytes) {
  requireC1(Buffer.isBuffer(originalOmmBytes) ||
    originalOmmBytes instanceof Uint8Array, 'ORIGINAL_SOURCE_BYTES_REQUIRED');
  return Buffer.from(originalOmmBytes);
}

/**
 * Required context:
 * - expectedNoradCatId: independently admitted/identified satellite (string)
 * - originalOmmBytes: exact unmodified, single-satellite upstream JSON body
 * - calculatedUtc: the actual UTC instant at which THIS result was computed,
 *   NOT the propagation target time; supplied by the authorized build actor
 * - modelVersion: an exact resolved satellite.js version, never latest/range
 * - maxEpochOffsetSeconds: release policy (default 172800 s) for model target
 */
export function adaptSgp4ToR19PublicPosition(producerReturn, context) {
  requireC1(context && typeof context === 'object', 'CONTEXT_MISSING');
  const { expectedNoradCatId, originalOmmBytes, calculatedUtc, modelVersion,
    maxEpochOffsetSeconds = 172800 } = context;
  requireC1(typeof expectedNoradCatId === 'string' &&
    CAT.test(expectedNoradCatId), 'CATNR_EXPECTED');
  requireC1(typeof modelVersion === 'string' &&
    /^\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?$/i.test(modelVersion), 'PINNED_SGP4_MODEL_VERSION');
  requireC1(Number.isInteger(maxEpochOffsetSeconds) && maxEpochOffsetSeconds > 0 &&
    maxEpochOffsetSeconds <= 7 * 86400, 'FRESHNESS_POLICY');
  const calculatedMs = dateMs(calculatedUtc, 'CALCULATED');
  const bytes = exactBytes(originalOmmBytes);
  requireC1(bytes.byteLength > 0 && bytes.byteLength < 4_000_000, 'ORIGINAL_SIZE');
  const sha = createHash('sha256').update(bytes).digest('hex');
  requireC1(DIGEST.test(sha), 'HASH');
  let original;
  try { original = JSON.parse(bytes.toString('utf8')); }
  catch { throw new Error('ORBIS_R19_BRIDGE_HOLD_ORIGINAL_JSON_INVALID'); }
  // Never silently select [0] from an ambiguous OMM array.
  if (Array.isArray(original)) {
    requireC1(original.length === 1, 'OMM_ARRAY_AMBIGUOUS');
    original = original[0];
  }
  requireC1(original && typeof original === 'object' &&
    !Array.isArray(original), 'OMM_OBJECT');
  requireC1(typeof original.NORAD_CAT_ID === 'string' ||
    Number.isSafeInteger(original.NORAD_CAT_ID), 'OMM_NORAD');
  const originalNorad = String(original.NORAD_CAT_ID);
  requireC1(CAT.test(originalNorad) && originalNorad === expectedNoradCatId,
    'OMM_NORAD_IDENTITY_MISMATCH');
  const epochMs = dateMs(original.EPOCH, 'ELEMENT');

  requireC1(producerReturn?.ok === true && producerReturn.nexus_link_verified === false &&
    producerReturn.claim_ceiling === 'C1_DESCRIPTIVE_ONLY', 'PRODUCER_STATE');
  requireC1(producerReturn.norad_cat_id === originalNorad,
    'PRODUCER_NORAD_IDENTITY_MISMATCH');
  requireC1(producerReturn.source_sha256 === sha &&
    producerReturn.position?.source_sha256 === sha, 'PRODUCER_SOURCE_DIGEST_MISMATCH');
  requireC1(producerReturn.epoch_utc === original.EPOCH &&
    producerReturn.position.epoch_utc === original.EPOCH,
    'PRODUCER_EPOCH_MISMATCH');
  const p = producerReturn.position;
  requireC1(p.data_class === 'ORBIT_PREDICTED' && p.model === 'SGP4',
    'MODEL_OR_DATA_CLASS');
  requireC1([p.lat_deg, p.lng_deg, p.height_km].every(Number.isFinite) &&
    Math.abs(p.lat_deg) <= 90 && Math.abs(p.lng_deg) <= 180 &&
    p.height_km >= 0, 'INVALID_GEODETIC');
  const targetMs = dateMs(p.target_utc, 'TARGET');
  requireC1(Math.abs(targetMs - epochMs) <= maxEpochOffsetSeconds * 1000,
    'ORBIT_ELEMENTS_STALE_FOR_TARGET');
  // A result calculated before its target time may still be a valid prediction.
  // The meaning of calculated_utc is independent of target_utc.
  requireC1(calculatedMs >= 0, 'CALCULATED_TIME');
  const out = {
    data_class: 'ORBIT_PREDICTED',
    lat_deg: p.lat_deg,
    lng_deg: p.lng_deg,
    alt_km: p.height_km,
    element_epoch_utc: original.EPOCH,
    target_utc: p.target_utc,
    calculated_utc: calculatedUtc,
    model: 'SGP4',
    source_sha256: sha,
    model_version: modelVersion
  };
  requireC1(Object.keys(out).length === POSITION_KEYS.length &&
    POSITION_KEYS.every(key => Object.hasOwn(out, key)), 'PUBLIC_POSITION_FIELD_SET');
  return Object.freeze(out);
}

/** Fail-closed wrapper for a ledger builder that expects null on per-slot hold. */
export function safeAdaptSgp4ToR19PublicPosition(producerReturn, context) {
  try { return { ok: true, position: adaptSgp4ToR19PublicPosition(producerReturn, context), reason: null }; }
  catch (error) { return { ok: false, position: null, reason: String(error.message || error) }; }
}
