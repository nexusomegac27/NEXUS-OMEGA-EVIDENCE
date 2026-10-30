/**
 * A00–A30 + F10–F12 regression harness for Open Neutral Check-in.
 * Drives fixtures/a00-a30.json expect/patch/omit/raw/duplicate/rate_flood/policy contract.
 */
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  processCheckin,
  createLedger,
  baselineCheckinPayload,
  f10f12PolicySurface,
  MAX_BODY_BYTES,
  MAX_CONTENT_CHARS,
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

// Compact single-line JSON last — selftest/CI parse via last `{...}` line.
console.log(JSON.stringify({
  suite: fixtures.suite,
  passed,
  failed,
  failures,
  claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
}));

if (failed > 0) process.exit(1);
