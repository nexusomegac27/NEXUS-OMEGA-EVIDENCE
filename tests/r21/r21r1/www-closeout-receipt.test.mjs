import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  validateCloseoutReceipt,
  isLiveVerifiedEligible,
  CLOSEOUT_SCHEMA_VERSION
} from '../../../examples/r21/r21r1/www-closeout-receipt.mjs';

const READBACK_URL = 'https://www.nexus-mobile.de/orbis/astra-nav/';
const SOURCE_COMMIT = 'b09dedca1e078c6fc327bf86e32eaf9a98094ea5';

const P0_FILES = [
  { route_relative_path: '/orbis/astra-nav/index.html', expected_sha256: '83a6fec4d6f57072e91623ed58c389da334ccc7523cf89fa0c89bcd77566ee1c', bytes: 3000 },
  { route_relative_path: '/orbis/astra-nav/app.mjs', expected_sha256: '6b631a0a3081c1c50e690764db477f875f1bf81cea6330a8c5905ff098ddd861', bytes: 4184 },
  { route_relative_path: '/orbis/astra-nav/ui-model.mjs', expected_sha256: '985f3d950a335df8163759d3bd7370f3001ddbd0584f65abe48305ffcd443a30', bytes: 4313 },
  { route_relative_path: '/orbis/astra-nav/style.css', expected_sha256: '1330a0e28433f2031ce5f40d384216876634d7e4db1e3bf90abcffb733d9cb0e', bytes: 2796 }
];

function fileset(over = {}) {
  return {
    state: 'PASS',
    source_commit: SOURCE_COMMIT,
    files: P0_FILES.map((f) => ({ ...f })),
    scope_class: 'ADDITIVE_ORBIS_ASTRA_NAV_ONLY',
    rollback_witness: null,
    observed_utc: null,
    ...over
  };
}

function write(over = {}) {
  return {
    state: 'PENDING',
    source_commit: null,
    writer_role: null,
    write_receipt_id: null,
    file_hashes_match: null,
    observed_utc: null,
    ...over
  };
}

function readback(over = {}) {
  return {
    state: 'PENDING',
    url: READBACK_URL,
    independent_reviewer: null,
    observed_utc: null,
    http_body_sha256: null,
    browser_map_tiles_visible: null,
    attribution_visible: null,
    desktop_mobile_pass: null,
    r19_regression_pass: null,
    asset_sha256_receipt: null,
    ...over
  };
}

function receipt(over = {}) {
  return {
    schema_version: CLOSEOUT_SCHEMA_VERSION,
    object_id: 'NEXUS_OMEGA_R21R1_WWW_CLOSEOUT_TEST_FIXTURE',
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    nexus_link_verified: false,
    terminal_state: 'NOT_LIVE_VERIFIED',
    production_fileset: fileset(),
    hostinger_scoped_write: write(),
    independent_public_readback: readback(),
    material_caveats: ['SYNTHETIC TEST FIXTURE - kein Live-Nachweis'],
    source_lineage: ['AXIOM R21R1 MAXI ORDER 2026-10-10'],
    ...over
  };
}

function completeFileset() {
  return fileset({ rollback_witness: 'route-folder-snapshot-20261010', observed_utc: '2026-10-10T13:00:00Z' });
}

function completeWrite() {
  return write({
    state: 'PASS',
    source_commit: SOURCE_COMMIT,
    writer_role: 'CURSOR_OPERATIVE_LANE',
    write_receipt_id: 'hostinger-write-20261010-0001',
    file_hashes_match: true,
    observed_utc: '2026-10-10T13:05:00Z'
  });
}

function completeReadback() {
  return readback({
    state: 'PASS',
    independent_reviewer: 'UNABHAENGIGER_TESTBROWSER',
    observed_utc: '2026-10-10T13:10:00Z',
    http_body_sha256: 'e'.repeat(64),
    browser_map_tiles_visible: true,
    attribution_visible: true,
    desktop_mobile_pass: true,
    r19_regression_pass: true,
    asset_sha256_receipt: 'readback-sha-receipt-20261010'
  });
}

test('a pending receipt validates and is not LIVE eligible', () => {
  const r = receipt();
  validateCloseoutReceipt(r);
  assert.equal(r.terminal_state, 'NOT_LIVE_VERIFIED');
  assert.equal(isLiveVerifiedEligible(r), false);
});

test('a LIVE claim without a complete fileset proof is rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({ terminal_state: 'WWW_LIVE_VERIFIED' })),
    /LIVE_CLAIM_WITHOUT_COMPLETE_FILESET_PROOF/
  );
});

test('a LIVE claim without a scoped Hostinger write receipt is rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({ terminal_state: 'WWW_LIVE_VERIFIED', production_fileset: completeFileset() })),
    /LIVE_CLAIM_WITHOUT_SCOPED_WRITE_RECEIPT/
  );
});

test('a LIVE claim without an independent readback is rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({
      terminal_state: 'WWW_LIVE_VERIFIED',
      production_fileset: completeFileset(),
      hostinger_scoped_write: completeWrite()
    })),
    /LIVE_CLAIM_WITHOUT_INDEPENDENT_READBACK/
  );
});

test('only all three separated proofs make a receipt LIVE eligible', () => {
  const r = receipt({
    terminal_state: 'WWW_LIVE_VERIFIED',
    production_fileset: completeFileset(),
    hostinger_scoped_write: completeWrite(),
    independent_public_readback: completeReadback()
  });
  validateCloseoutReceipt(r);
  assert.equal(isLiveVerifiedEligible(r), true);
});

test('route paths outside /orbis/astra-nav/ are rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({
      production_fileset: fileset({ files: [{ route_relative_path: '/index.html', expected_sha256: 'a'.repeat(64), bytes: 1 }] })
    })),
    /ROUTE_PATH_OUT_OF_SCOPE/
  );
});

test('malformed source commits are rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({ production_fileset: fileset({ source_commit: 'abc123' }) })),
    /BAD_SOURCE_COMMIT/
  );
});

test('nexus-link promotion inside a receipt is rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({ nexus_link_verified: true })),
    /NEXUS_LINK_PROMOTION_REJECTED/
  );
});

test('unexpected root fields are rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({ promotion: 'shiny' })),
    /UNEXPECTED_FIELD/
  );
});

test('scope violations are rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({
      production_fileset: fileset({ scope_class: 'WHOLE_WEBSITE_OVERWRITE' })
    })),
    /SCOPE_CLASS_VIOLATION/
  );
});

test('unknown terminal states are rejected', () => {
  assert.throws(() => validateCloseoutReceipt(receipt({ terminal_state: 'MAYBE_LIVE' })), /BAD_TERMINAL_STATE/);
});

test('wrong schema versions are rejected', () => {
  assert.throws(() => validateCloseoutReceipt(receipt({ schema_version: 'nexus-r21r1-www-closeout/v2' })), /BAD_SCHEMA_VERSION/);
});

test('readbacks outside the authorised URL are rejected', () => {
  assert.throws(
    () => validateCloseoutReceipt(receipt({
      independent_public_readback: readback({ url: 'https://evil.example/orbis/astra-nav/' })
    })),
    /READBACK_URL_OUT_OF_SCOPE/
  );
});

test('the pending example receipt in validation/ is a valid NOT_LIVE_VERIFIED receipt', () => {
  const raw = readFileSync('validation/r21/r21r1/www-closeout-receipt.pending-example.json', 'utf8');
  const parsed = JSON.parse(raw);
  validateCloseoutReceipt(parsed);
  assert.equal(parsed.terminal_state, 'NOT_LIVE_VERIFIED');
  assert.equal(isLiveVerifiedEligible(parsed), false);
});
