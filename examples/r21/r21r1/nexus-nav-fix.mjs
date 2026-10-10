/**
 * NEXUS OMEGA . R21R1 . WP-G2 . nexus-nav-fix/v1 fail-closed validator and classifier.
 * C1_DESCRIPTIVE_ONLY. No runtime, no hardware claim, no promotion from browser geolocation.
 * Physical truth boundary: a GPS_PROVIDER fix is SOURCE_REPORTED_GNSS until a witnessed
 * network-disabled hardware test exists. GNSS-only is only claimable with that witness.
 * Schema: schema/r21/r21r1/nexus-nav-fix-v1.schema.json
 */

export const NAV_FIX_SCHEMA_VERSION = 'nexus-nav-fix/v1';
export const MIN_SATELLITES_USED_FOR_TRUSTED_FIX = 4;
export const MAX_HORIZONTAL_ACCURACY_M = 500;
export const MAX_FIX_AGE_S = 30;
export const MAX_CLOCK_SKEW_S = 2;

const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const ALLOWED_PROVIDERS = new Set(['GPS_PROVIDER']);

function finite(x) { return typeof x === 'number' && Number.isFinite(x); }
function isUtc(s) { return typeof s === 'string' && UTC.test(s) && !Number.isNaN(Date.parse(s)); }

function validateLocation(loc) {
  if (!loc || typeof loc !== 'object' || Array.isArray(loc)) throw new Error('BAD_LOCATION');
  if (!finite(loc.latitude) || loc.latitude < -90 || loc.latitude > 90) throw new Error('BAD_LATITUDE');
  if (!finite(loc.longitude) || loc.longitude < -180 || loc.longitude > 180) throw new Error('BAD_LONGITUDE');
  if (loc.altitude_m !== null && loc.altitude_m !== undefined && !finite(loc.altitude_m)) throw new Error('BAD_ALTITUDE');
  if (!finite(loc.horizontal_accuracy_m) || loc.horizontal_accuracy_m <= 0) throw new Error('BAD_ACCURACY');
  if (loc.horizontal_accuracy_m > MAX_HORIZONTAL_ACCURACY_M) throw new Error('UNBOUNDED_ACCURACY');
  if (!isUtc(loc.utc)) throw new Error('BAD_FIX_UTC');
  if (!Number.isSafeInteger(loc.elapsed_realtime_nanos) || loc.elapsed_realtime_nanos < 0) throw new Error('BAD_MONOTONIC_TIME');
  if (typeof loc.is_mock !== 'boolean') throw new Error('BAD_MOCK_FLAG');
  if (loc.is_mock === true) throw new Error('MOCK_LOCATION_REJECTED');
  return loc;
}

function validateGnssStatus(gnss) {
  if (!gnss || typeof gnss !== 'object' || Array.isArray(gnss)) throw new Error('NO_GNSS_STATUS');
  if (!Number.isSafeInteger(gnss.satellites_visible) || gnss.satellites_visible < 0) throw new Error('INVALID_GNSS_STATUS');
  if (!Number.isSafeInteger(gnss.satellites_used_in_fix) || gnss.satellites_used_in_fix < 0) throw new Error('INVALID_GNSS_STATUS');
  if (gnss.satellites_used_in_fix > gnss.satellites_visible) throw new Error('INVALID_GNSS_STATUS');
  return gnss;
}

function validateAssistance(a) {
  if (!a || typeof a !== 'object' || Array.isArray(a)) throw new Error('BAD_ASSISTANCE');
  if (a.class !== 'ASSISTANCE_UNKNOWN' && a.class !== 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED') throw new Error('BAD_ASSISTANCE');
  if (a.class === 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED') {
    const w = a.witness;
    if (!w || typeof w !== 'object' || Array.isArray(w)) throw new Error('BAD_OFFLINE_WITNESS');
    if (w.airplane_mode_on !== true) throw new Error('BAD_OFFLINE_WITNESS');
    if (w.wifi_enabled !== false) throw new Error('BAD_OFFLINE_WITNESS');
    if (w.cell_data_enabled !== false) throw new Error('BAD_OFFLINE_WITNESS');
    if (w.network_connected !== false) throw new Error('BAD_OFFLINE_WITNESS');
    if (!isUtc(w.observed_utc)) throw new Error('BAD_OFFLINE_WITNESS');
  }
  return a;
}

export function validateNavFix(fix) {
  if (!fix || typeof fix !== 'object' || Array.isArray(fix)) throw new Error('BAD_NAV_FIX');
  if (fix.schema_version !== NAV_FIX_SCHEMA_VERSION) throw new Error('INVALID_NAV_FIX_CONTRACT');
  if (fix.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY') throw new Error('INVALID_NAV_FIX_CONTRACT');
  if (fix.nexus_link_verified !== undefined && fix.nexus_link_verified !== false) throw new Error('INVALID_NAV_FIX_CONTRACT');
  if (typeof fix.provider !== 'string' || !ALLOWED_PROVIDERS.has(fix.provider)) throw new Error('PROVIDER_NOT_GNSS');
  if (fix.permission_state !== 'GRANTED') throw new Error('NO_PERMISSION');
  if (fix.device_local_private !== true) throw new Error('PRIVACY_VIOLATION_DEVICE_LOCAL_REQUIRED');
  validateLocation(fix.location);
  validateGnssStatus(fix.gnss_status);
  validateAssistance(fix.assistance);
  return fix;
}

/**
 * Classify a structurally valid fix. Never promotes beyond evidence:
 * a fix without an offline witness stays ASSISTANCE_UNKNOWN and can never
 * support a GNSS-only claim, regardless of the provider string.
 */
export function classifyNavFix(fix, { evaluation_utc } = {}) {
  validateNavFix(fix);
  if (!isUtc(evaluation_utc)) throw new Error('BAD_EVALUATION_TIME');
  const reasons = [];
  const fixMs = Date.parse(fix.location.utc);
  const evalMs = Date.parse(evaluation_utc);
  if (fixMs > evalMs + MAX_CLOCK_SKEW_S * 1000) reasons.push('CLOCK_DISCREPANCY');
  const ageS = (evalMs - fixMs) / 1000;
  if (ageS > MAX_FIX_AGE_S) reasons.push('STALE_FIX');
  const used = fix.gnss_status.satellites_used_in_fix;
  if (used === 0) reasons.push('NO_SATELLITES_USED_IN_FIX');
  if (used > 0 && used < MIN_SATELLITES_USED_FOR_TRUSTED_FIX) reasons.push('TOO_FEW_SATELLITES_FOR_TRUSTED_FIX');
  if (reasons.length > 0) {
    return { evidence_class: 'HOLD_NO_FIX', assistance_state: fix.assistance.class, gnss_only_claim_allowed: false, reasons };
  }
  const offlineVerified = fix.assistance.class === 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED';
  return {
    evidence_class: 'SOURCE_REPORTED_GNSS',
    assistance_state: offlineVerified ? 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED' : 'ASSISTANCE_UNKNOWN',
    gnss_only_claim_allowed: offlineVerified,
    reasons
  };
}

/**
 * Monotonic per-boot sequence check: a decreasing elapsedRealtimeNanos between
 * consecutive fixes witnesses a reboot and breaks boot-bound time continuity.
 */
export function isMonotonicPerBoot(fixes) {
  if (!Array.isArray(fixes) || fixes.length === 0) throw new Error('BAD_SEQUENCE');
  for (const f of fixes) validateNavFix(f);
  for (let i = 1; i < fixes.length; i++) {
    if (fixes[i].location.elapsed_realtime_nanos < fixes[i - 1].location.elapsed_realtime_nanos) return false;
  }
  return true;
}
