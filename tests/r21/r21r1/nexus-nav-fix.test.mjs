import test from 'node:test';
import assert from 'node:assert/strict';
import {
  validateNavFix,
  classifyNavFix,
  isMonotonicPerBoot,
  NAV_FIX_SCHEMA_VERSION,
  MIN_SATELLITES_USED_FOR_TRUSTED_FIX
} from '../../examples/r21/r21r1/nexus-nav-fix.mjs';

const EVAL = '2026-10-10T12:00:05Z';
const nanos = (s) => s * 1e9;

const WITNESS = {
  airplane_mode_on: true,
  wifi_enabled: false,
  cell_data_enabled: false,
  network_connected: false,
  observed_utc: '2026-10-10T11:59:00Z'
};

function fix(extra = {}, loc = {}, gnss = {}, assistance = {}) {
  const base = {
    schema_version: NAV_FIX_SCHEMA_VERSION,
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    provider: 'GPS_PROVIDER',
    permission_state: 'GRANTED',
    device_local_private: true,
    location: {
      latitude: 53.5511,
      longitude: 10.0037,
      altitude_m: 6,
      horizontal_accuracy_m: 12.5,
      utc: '2026-10-10T12:00:00Z',
      elapsed_realtime_nanos: nanos(120),
      is_mock: false,
      ...loc
    },
    gnss_status: { satellites_visible: 9, satellites_used_in_fix: 7, ...gnss },
    assistance: { class: 'ASSISTANCE_UNKNOWN', ...assistance }
  };
  return { ...base, ...extra };
}

test('GPS_PROVIDER fix with unknown assistance validates structurally', () => {
  assert.equal(validateNavFix(fix()).provider, 'GPS_PROVIDER');
});

test('a fused provider can never satisfy the GNSS contract', () => {
  assert.throws(() => validateNavFix(fix({ provider: 'FUSED' })), /PROVIDER_NOT_GNSS/);
});

test('browser geolocation is not GNSS provenance', () => {
  assert.throws(() => validateNavFix(fix({ provider: 'BROWSER_GEOLOCATION' })), /PROVIDER_NOT_GNSS/);
});

test('mock locations are rejected fail-closed', () => {
  assert.throws(() => validateNavFix(fix({}, { is_mock: true })), /MOCK_LOCATION_REJECTED/);
});

test('missing location permission blocks any fix', () => {
  assert.throws(() => validateNavFix(fix({ permission_state: 'DENIED' })), /NO_PERMISSION/);
});

test('unbounded accuracy claims are rejected', () => {
  assert.throws(() => validateNavFix(fix({}, { horizontal_accuracy_m: 5000 })), /UNBOUNDED_ACCURACY/);
});

test('cloud-served privacy model is rejected', () => {
  assert.throws(() => validateNavFix(fix({ device_local_private: false })), /PRIVACY_VIOLATION/);
});

test('missing GNSS satellite status is rejected', () => {
  assert.throws(() => validateNavFix(fix({ gnss_status: null })), /NO_GNSS_STATUS/);
});

test('used satellites beyond visible satellites is invalid status', () => {
  assert.throws(() => validateNavFix(fix({}, {}, { satellites_used_in_fix: 12 })), /INVALID_GNSS_STATUS/);
});

test('classification stays SOURCE_REPORTED_GNSS without offline witness', () => {
  const c = classifyNavFix(fix(), { evaluation_utc: EVAL });
  assert.equal(c.evidence_class, 'SOURCE_REPORTED_GNSS');
  assert.equal(c.assistance_state, 'ASSISTANCE_UNKNOWN');
  assert.equal(c.gnss_only_claim_allowed, false);
  assert.deepEqual(c.reasons, []);
});

test('GNSS-only claim requires the network-disabled hardware witness', () => {
  const c = classifyNavFix(
    fix({}, {}, {}, { class: 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED', witness: WITNESS }),
    { evaluation_utc: EVAL }
  );
  assert.equal(c.evidence_class, 'SOURCE_REPORTED_GNSS');
  assert.equal(c.assistance_state, 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED');
  assert.equal(c.gnss_only_claim_allowed, true);
});

test('an incomplete offline witness is rejected', () => {
  assert.throws(
    () => validateNavFix(fix({}, {}, {}, {
      class: 'OFFLINE_NETWORK_DISABLED_TEST_VERIFIED',
      witness: { ...WITNESS, wifi_enabled: true }
    })),
    /BAD_OFFLINE_WITNESS/
  );
});

test('stale fixes go to HOLD_NO_FIX', () => {
  const c = classifyNavFix(fix({}, { utc: '2026-10-10T11:00:00Z' }), { evaluation_utc: EVAL });
  assert.equal(c.evidence_class, 'HOLD_NO_FIX');
  assert.ok(c.reasons.includes('STALE_FIX'));
  assert.equal(c.gnss_only_claim_allowed, false);
});

test('future-dated fixes witness a clock discrepancy', () => {
  const c = classifyNavFix(fix({}, { utc: '2026-10-10T12:00:10Z' }), { evaluation_utc: EVAL });
  assert.equal(c.evidence_class, 'HOLD_NO_FIX');
  assert.ok(c.reasons.includes('CLOCK_DISCREPANCY'));
  assert.equal(c.gnss_only_claim_allowed, false);
});

test('zero satellites used in fix is not a trusted fix', () => {
  const c = classifyNavFix(fix({}, {}, { satellites_used_in_fix: 0 }), { evaluation_utc: EVAL });
  assert.equal(c.evidence_class, 'HOLD_NO_FIX');
  assert.ok(c.reasons.includes('NO_SATELLITES_USED_IN_FIX'));
});

test('fewer than four used satellites is not a trusted fix', () => {
  const c = classifyNavFix(
    fix({}, {}, { satellites_used_in_fix: MIN_SATELLITES_USED_FOR_TRUSTED_FIX - 1 }),
    { evaluation_utc: EVAL }
  );
  assert.equal(c.evidence_class, 'HOLD_NO_FIX');
  assert.ok(c.reasons.includes('TOO_FEW_SATELLITES_FOR_TRUSTED_FIX'));
});

test('a non-UTC evaluation time is rejected', () => {
  assert.throws(() => classifyNavFix(fix(), { evaluation_utc: '10.10.2026 12:00' }), /BAD_EVALUATION_TIME/);
});

test('monotonic per-boot sequence is recognised', () => {
  const seq = [
    fix({}, { elapsed_realtime_nanos: nanos(10) }),
    fix({}, { elapsed_realtime_nanos: nanos(20) }),
    fix({}, { elapsed_realtime_nanos: nanos(21) })
  ];
  assert.equal(isMonotonicPerBoot(seq), true);
});

test('a decreasing monotonic clock witnesses a reboot and breaks continuity', () => {
  const seq = [
    fix({}, { elapsed_realtime_nanos: nanos(30) }),
    fix({}, { elapsed_realtime_nanos: nanos(20) })
  ];
  assert.equal(isMonotonicPerBoot(seq), false);
});

test('empty sequences are rejected', () => {
  assert.throws(() => isMonotonicPerBoot([]), /BAD_SEQUENCE/);
});

test('negative elapsedRealtime is rejected', () => {
  assert.throws(() => validateNavFix(fix({}, { elapsed_realtime_nanos: -1 })), /BAD_MONOTONIC_TIME/);
});

test('claim-ceiling promotion inside a fix is rejected', () => {
  assert.throws(() => validateNavFix(fix({ claim_ceiling: 'C2_RUNTIME_VERIFIED' })), /INVALID_NAV_FIX_CONTRACT/);
  assert.throws(() => validateNavFix(fix({ nexus_link_verified: true })), /INVALID_NAV_FIX_CONTRACT/);
});
