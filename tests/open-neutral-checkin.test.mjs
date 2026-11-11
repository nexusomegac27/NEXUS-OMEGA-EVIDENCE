/**
 * A00–A30 + F10–F12 + C13/C15 schema/privacy/HTTP regression for Open Neutral Check-in.
 * Drives fixtures/a00-a30.json expect/patch/omit/raw/duplicate/rate_flood/policy contract
 * plus 17-field request contract, digests-only privacy, 415 Content-Type, four schema objects.
 */
import { EventEmitter } from 'node:events';
import { mkdtempSync, readFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  processCheckin,
  createLedger,
  createAppHandler,
  baselineCheckinPayload,
  f10f12PolicySurface,
  MAX_BODY_BYTES,
  MAX_CONTENT_CHARS,
  ALLOWED_TOP_LEVEL_FIELDS,
  FIELD_MAX,
} from '../examples/open-neutral-checkin/open-neutral-checkin.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const FIXTURE_PATH = join(
  __dirname,
  '..',
  'examples',
  'open-neutral-checkin',
  'fixtures',
  'a00-a30.json',
);
const SCHEMA_PATH = join(__dirname, '..', 'schema', 'open-neutral-checkin-v1.json');

const fixtures = JSON.parse(readFileSync(FIXTURE_PATH, 'utf8'));
let passed = 0;
let failed = 0;
const failures = [];

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function buildBody(fx) {
  if (typeof fx.raw === 'string') return fx.raw;
  if (typeof fx.raw_bytes === 'number') return 'x'.repeat(fx.raw_bytes);

  const base = baselineCheckinPayload();
  if (Array.isArray(fx.omit)) {
    for (const k of fx.omit) delete base[k];
  }
  if (fx.patch && typeof fx.patch === 'object') {
    Object.assign(base, fx.patch);
  }
  if (typeof fx.large_content === 'number') {
    base.content = 'C'.repeat(fx.large_content);
  }
  return JSON.stringify(base);
}

function runCase(fx) {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-'));
  try {
    const ledger = createLedger(tmp);
    const rateBucket = { hits: [] };

    if (fx.policy) {
      const surface = f10f12PolicySurface();
      const p = surface[fx.policy];
      assert(p, `policy ${fx.policy} missing`);
      if (fx.policy === 'f10') {
        assert(p.status === 'CLOSED', 'F10 must be CLOSED');
        assert(p.default === 'DENY', 'F10 default DENY');
        assert(p.public_external_write_api === 'HOLD', 'F10 HOLD');
      }
      if (fx.policy === 'f11') {
        assert(p.status === 'CLOSED_TESTED_PATH', 'F11 CLOSED_TESTED_PATH');
        assert(p.fail_closed === true, 'F11 fail_closed');
      }
      if (fx.policy === 'f12') {
        assert(p.status === 'CLOSED_EMPTY_REGISTER', 'F12 CLOSED_EMPTY_REGISTER');
        assert(Array.isArray(p.legacy_grant_register), 'F12 register array');
        assert(p.legacy_grant_register.length === 0, 'F12 empty register');
      }
      return;
    }

    if (fx.rate_flood) {
      let last;
      for (let i = 0; i < fx.rate_flood; i++) {
        const body = JSON.stringify(
          baselineCheckinPayload({
            interaction_id: `rate-${String(i).padStart(8, '0')}`,
            content: `rate flood observation ${i}`,
          }),
        );
        last = processCheckin(body, { ledger, rateBucket, rateLimit: 30 });
      }
      assert(last.status === 'DENIED', `${fx.id}: expected DENIED after flood`);
      assert(last.deny_code === 'RATE_LIMITED', `${fx.id}: expected RATE_LIMITED got ${last.deny_code}`);
      return;
    }

    if (fx.duplicate) {
      const body = JSON.stringify(baselineCheckinPayload({
        interaction_id: 'duplicate-test-id-001',
        content: 'first submission for idempotency',
      }));
      const first = processCheckin(body, { ledger, rateBucket });
      assert(first.status === 'STAGED_UNTRUSTED', `${fx.id}: first must STAGED`);
      const second = processCheckin(body, { ledger, rateBucket });
      assert(second.status === 'DUPLICATE', `${fx.id}: second must DUPLICATE got ${second.status}`);
      return;
    }

    const body = buildBody(fx);
    // BODY_TOO_LARGE: bypass rate for large raw; engine still checks bytes
    const result = processCheckin(body, { ledger, rateBucket });

    if (fx.expect === 'STAGED_UNTRUSTED') {
      assert(result.status === 'STAGED_UNTRUSTED', `${fx.id}: expected STAGED_UNTRUSTED got ${result.status}/${result.deny_code}`);
      assert(result.epistemic === 'STAGED_UNTRUSTED_NOT_VALIDATED', `${fx.id}: epistemic`);
      assert(result.scientific_status === 'RAW_NOT_VALIDATED', `${fx.id}: scientific_status`);
      if (typeof fx.expect_redactions_ge === 'number') {
        const n = Array.isArray(result.redactions) ? result.redactions.length : 0;
        assert(n >= fx.expect_redactions_ge, `${fx.id}: redactions ${n} < ${fx.expect_redactions_ge}`);
        assert(
          typeof result.content_redacted === 'string' && result.content_redacted.includes('[REDACTED:'),
          `${fx.id}: content_redacted missing marker`,
        );
      }
      return;
    }

    if (fx.expect === 'DENIED') {
      assert(result.status === 'DENIED', `${fx.id}: expected DENIED got ${result.status}`);
      assert(
        result.deny_code === fx.deny_code,
        `${fx.id}: deny_code expected ${fx.deny_code} got ${result.deny_code}`,
      );
      return;
    }

    if (fx.expect === 'DUPLICATE') {
      assert(result.status === 'DUPLICATE', `${fx.id}: expected DUPLICATE`);
      return;
    }

    throw new Error(`${fx.id}: unhandled expect ${fx.expect}`);
  } finally {
    try {
      rmSync(tmp, { recursive: true, force: true });
    } catch {
      /* ignore */
    }
  }
}

console.log(`SUITE ${fixtures.suite} cases=${fixtures.cases.length}`);
console.log(`MAX_BODY_BYTES=${MAX_BODY_BYTES} MAX_CONTENT_CHARS=${MAX_CONTENT_CHARS}`);

for (const fx of fixtures.cases) {
  try {
    runCase(fx);
    passed += 1;
    console.log(`PASS ${fx.id} ${fx.title}`);
  } catch (e) {
    failed += 1;
    failures.push({ id: fx.id, title: fx.title, error: String(e && e.message ? e.message : e) });
    console.log(`FAIL ${fx.id} ${fx.title}: ${e && e.message ? e.message : e}`);
  }
}

// Extra: dual-arity ledger positional form
try {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-arity-'));
  const ledger = createLedger(tmp);
  const body = JSON.stringify(baselineCheckinPayload({ content: 'arity check' }));
  const r = processCheckin(body, ledger, {});
  assert(r.status === 'STAGED_UNTRUSTED', 'dual-arity STAGED');
  passed += 1;
  console.log('PASS X_DUAL_ARITY');
  rmSync(tmp, { recursive: true, force: true });
} catch (e) {
  failed += 1;
  failures.push({ id: 'X_DUAL_ARITY', error: String(e.message || e) });
  console.log(`FAIL X_DUAL_ARITY: ${e.message || e}`);
}

function runExtra(id, fn) {
  try {
    fn();
    passed += 1;
    console.log(`PASS ${id}`);
  } catch (e) {
    failed += 1;
    failures.push({ id, error: String(e && e.message ? e.message : e) });
    console.log(`FAIL ${id}: ${e && e.message ? e.message : e}`);
  }
}

runExtra('C13_ALLOWED_17_FIELDS', () => {
  assert(ALLOWED_TOP_LEVEL_FIELDS.length === 17, `expected 17 got ${ALLOWED_TOP_LEVEL_FIELDS.length}`);
  const required = ['protocol', 'event_class', 'claim_ceiling', 'interaction_id', 'content'];
  for (const k of required) {
    assert(ALLOWED_TOP_LEVEL_FIELDS.includes(k), `missing required ${k}`);
  }
  for (const k of [
    'schema_version',
    'submitted_at',
    'consent',
    'retention_days',
    'interpretation_labels',
    'interpretation_provenance',
  ]) {
    assert(ALLOWED_TOP_LEVEL_FIELDS.includes(k), `missing optional ${k}`);
  }
  assert(!ALLOWED_TOP_LEVEL_FIELDS.includes('content_redacted'), 'content_redacted must not be request input');
  assert(!ALLOWED_TOP_LEVEL_FIELDS.includes('receipt_id'), 'receipt_id must not be request input');
});

runExtra('C13_FIELD_MAX_BOUNDS', () => {
  assert(FIELD_MAX.provider === 64, 'provider max');
  assert(FIELD_MAX.model === 64, 'model max');
  assert(FIELD_MAX.agent_self_id === 128, 'agent_self_id max');
  assert(FIELD_MAX.capability_brief === 2048, 'capability_brief max');
  assert(FIELD_MAX.dissent === 4096, 'dissent max');
  assert(FIELD_MAX.decline_reason === 2048, 'decline_reason max');
  assert(FIELD_MAX.schema_version === 64, 'schema_version max');
  assert(FIELD_MAX.submitted_at === 64, 'submitted_at max');
  assert(FIELD_MAX.interpretation_provenance === 512, 'interpretation_provenance max');
});

runExtra('C13_ALL_17_FIELDS_ACCEPT', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-all-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        schema_version: '1.0.0',
        submitted_at: '2026-10-31T00:00:00.000Z',
        provider: 'test-provider',
        model: 'test-model',
        agent_self_id: 'agent-self-01',
        capability_brief: 'brief',
        dissent: 'optional dissent',
        decline_reason: 'n/a',
        consent: 'opt_in',
        retention_days: 30,
        interpretation_labels: ['label-a'],
        interpretation_provenance: 'SUBMITTER_DECLARED_UNVERIFIED',
        content: 'full seventeen field checkin',
        interaction_id: 'ix-c13-all-17-fields-01',
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'STAGED_UNTRUSTED', `status=${r.status}`);
    assert(r.privacy_mode === 'OPT_IN_REDACTED', `privacy=${r.privacy_mode}`);
    assert(typeof r.content_redacted === 'string' && r.content_redacted.length > 0, 'content_redacted present on opt_in');
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_FIELD_TOO_LONG', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-long-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        provider: 'P'.repeat(FIELD_MAX.provider + 1),
        interaction_id: 'ix-c13-field-too-long-01',
        content: 'too long provider',
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'DENIED', `expected DENIED got ${r.status}`);
    assert(
      r.deny_code === 'FIELD_TOO_LONG',
      `expected FIELD_TOO_LONG got ${JSON.stringify(r)}`,
    );
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_BAD_FIELD_TYPE_NULL', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-null-'));
  try {
    const ledger = createLedger(tmp);
    const payload = baselineCheckinPayload({
      interaction_id: 'ix-c13-null-provider-01',
      content: 'null provider rejected',
    });
    payload.provider = null;
    const r = processCheckin(JSON.stringify(payload), ledger, {});
    assert(r.status === 'DENIED', `expected DENIED got ${r.status}`);
    assert(
      r.deny_code === 'BAD_FIELD_TYPE',
      `expected BAD_FIELD_TYPE got ${JSON.stringify(r)}`,
    );
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_MISSING_REQUIRED', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-miss-'));
  try {
    const ledger = createLedger(tmp);
    const payload = baselineCheckinPayload({ interaction_id: 'ix-c13-missing-content-01' });
    delete payload.content;
    const r = processCheckin(JSON.stringify(payload), ledger, {});
    assert(r.status === 'DENIED', `expected DENIED got ${r.status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_UNKNOWN_FIELD', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-unk-'));
  try {
    const ledger = createLedger(tmp);
    const payload = baselineCheckinPayload({
      interaction_id: 'ix-c13-unknown-field-01',
      content: 'unknown field',
    });
    payload.extra_secret = 'nope';
    const r = processCheckin(JSON.stringify(payload), ledger, {});
    assert(r.status === 'DENIED', `expected DENIED got ${r.status}`);
    assert(
      r.deny_code === 'UNKNOWN_FIELD',
      `expected UNKNOWN_FIELD got ${JSON.stringify(r)}`,
    );
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_CONTENT_MAX_16000', () => {
  assert(MAX_CONTENT_CHARS === 16000, `MAX_CONTENT_CHARS=${MAX_CONTENT_CHARS}`);
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-content-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        interaction_id: 'ix-c13-content-16001-01',
        content: 'C'.repeat(16001),
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'DENIED', `expected DENIED got ${r.status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_INTERACTION_ID_PATTERN', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c13-iid-'));
  try {
    const ledger = createLedger(tmp);
    const short = processCheckin(
      JSON.stringify(
        baselineCheckinPayload({ interaction_id: 'short', content: 'bad id' }),
      ),
      ledger,
      {},
    );
    assert(short.status === 'DENIED', `short id expected DENIED got ${short.status}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C15_PRIVACY_OPT_OUT_DIGESTS_ONLY', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c15-out-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        interaction_id: 'ix-c15-opt-out-digests-01',
        content: 'secret freitext must not persist',
        consent: 'opt_out',
        provider: 'should-not-store',
        model: 'should-not-store',
        dissent: 'should-not-store',
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'STAGED_UNTRUSTED', `status=${r.status}`);
    assert(r.privacy_mode === 'DIGESTS_ONLY', `privacy=${r.privacy_mode}`);
    assert(r.content_redacted === null, 'content_redacted must be null on digests-only');
    assert(r.provider === null, 'provider null on digests-only');
    assert(r.model === null, 'model null on digests-only');
    const obsPath = join(tmp, 'observations.jsonl');
    assert(existsSync(obsPath), 'observations.jsonl missing');
    const lines = readFileSync(obsPath, 'utf8').trim().split('\n').filter(Boolean);
    assert(lines.length >= 1, 'expected observation line');
    const obs = JSON.parse(lines[lines.length - 1]);
    assert(obs.privacy_mode === 'DIGESTS_ONLY', `obs privacy=${obs.privacy_mode}`);
    assert(obs.content_redacted === null, 'obs content_redacted null');
    assert(obs.provider === null, 'obs provider null');
    assert(obs.model === null, 'obs model null');
    assert(obs.dissent === null, 'obs dissent null');
    assert(typeof obs.body_sha256 === 'string' && obs.body_sha256.length === 64, 'body digest required');
    assert(typeof obs.content_sha256 === 'string' && obs.content_sha256.length === 64, 'content digest required');
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C15_PRIVACY_UNSPECIFIED_DIGESTS_ONLY', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c15-unspec-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        interaction_id: 'ix-c15-unspecified-digests-01',
        content: 'unspecified freitext blocked',
        consent: 'unspecified',
        dissent: 'should-not-store',
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'STAGED_UNTRUSTED', `status=${r.status}`);
    assert(r.privacy_mode === 'DIGESTS_ONLY', `privacy=${r.privacy_mode}`);
    assert(r.content_redacted === null, 'content_redacted null');
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C15_PRIVACY_OPT_IN_REDACTED', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-c15-in-'));
  try {
    const ledger = createLedger(tmp);
    const body = JSON.stringify(
      baselineCheckinPayload({
        interaction_id: 'ix-c15-opt-in-redacted-01',
        content: 'opt-in freitext allowed with redaction',
        consent: 'opt_in',
        provider: 'prov',
        model: 'mdl',
        dissent: 'ok dissent',
      }),
    );
    const r = processCheckin(body, ledger, {});
    assert(r.status === 'STAGED_UNTRUSTED', `status=${r.status}`);
    assert(r.privacy_mode === 'OPT_IN_REDACTED', `privacy=${r.privacy_mode}`);
    assert(typeof r.content_redacted === 'string' && r.content_redacted.length > 0, 'content_redacted string');
    assert(r.provider === 'prov', 'provider stored on opt_in');
    assert(r.model === 'mdl', 'model stored on opt_in');
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

runExtra('C13_SCHEMA_FOUR_OBJECTS', () => {
  const schema = JSON.parse(readFileSync(SCHEMA_PATH, 'utf8'));
  assert(schema.$defs && typeof schema.$defs === 'object', '$defs missing');
  for (const name of ['CheckinRequest', 'CheckinResponse', 'StoredObservation', 'LedgerReceipt']) {
    assert(schema.$defs[name], `missing $defs.${name}`);
  }
  const req = schema.$defs.CheckinRequest;
  assert(Array.isArray(req.required) && req.required.length === 5, 'CheckinRequest required=5');
  assert(req.properties.content.maxLength === 16000, 'content maxLength 16000');
  assert(req.properties.consent && Array.isArray(req.properties.consent.enum), 'consent enum');
  assert(
    JSON.stringify(req.properties.consent.enum) === JSON.stringify(['opt_in', 'opt_out', 'unspecified']),
    'consent enum values',
  );
  for (const k of [
    'schema_version',
    'submitted_at',
    'consent',
    'retention_days',
    'interpretation_labels',
    'interpretation_provenance',
  ]) {
    assert(req.properties[k], `CheckinRequest missing ${k}`);
  }
  assert(!req.properties.content_redacted, 'content_redacted must not be on CheckinRequest');
  assert(schema.$defs.CheckinResponse.properties.content_redacted, 'content_redacted on CheckinResponse');
  assert(schema.$defs.StoredObservation.properties.content_redacted, 'content_redacted on StoredObservation');
  assert(schema.$defs.LedgerReceipt, 'LedgerReceipt present');
  assert(schema.$ref === '#/$defs/CheckinRequest' || schema.$ref?.endsWith('CheckinRequest'), 'root $ref CheckinRequest');
});

runExtra('R4_HTTP_415_UNSUPPORTED_MEDIA_TYPE', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'nexus-onc-r4-415-'));
  try {
    const ledger = createLedger(tmp);
    const handler = createAppHandler({ ledger, rootDir: tmp });
    const req = new EventEmitter();
    req.method = 'POST';
    req.url = '/checkin';
    req.headers = { 'content-type': 'text/plain' };
    let statusCode = 0;
    let body = '';
    const res = {
      writeHead(code) {
        statusCode = code;
      },
      setHeader() {},
      end(chunk) {
        body = String(chunk || '');
      },
    };
    handler(req, res);
    assert(statusCode === 415, `expected 415 got ${statusCode}`);
    const parsed = JSON.parse(body);
    assert(parsed.status === 'DENIED', `expected DENIED got ${parsed.status}`);
    assert(
      parsed.deny_code === 'UNSUPPORTED_MEDIA_TYPE',
      `expected UNSUPPORTED_MEDIA_TYPE got ${parsed.deny_code}`,
    );
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

// Compact single-line JSON last — selftest/CI parse via last `{...}` line.
console.log(JSON.stringify({
  suite: fixtures.suite,
  passed,
  failed,
  failures,
  claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
}));

if (failed > 0) process.exit(1);
