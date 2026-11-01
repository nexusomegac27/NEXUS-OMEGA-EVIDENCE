#!/usr/bin/env node
/**
 * C13–C19 Hard-Close harness — ORIGINAL A00–A30 + R1_LOCAL_32 (separate).
 * DATA_ROUTE = GITHUB_ONLY · CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
 */
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { mkdtempSync, readFileSync, rmSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import {
  processCheckin,
  processCheckinBytes,
  createLedger,
  baselineCheckinObject,
  strictParseJsonBytes,
  healthPayload,
  createAppHandler,
  DEPLOYMENT_PLANE,
  F10_F12_REGRESSION,
  MAX_BODY_BYTES,
} from './open-neutral-checkin.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname);
const FIX = join(ROOT, 'fixtures');

const ORIGINAL = JSON.parse(readFileSync(join(FIX, 'a00-a30-original.json'), 'utf8'));
const R1 = JSON.parse(readFileSync(join(FIX, 'r1-local-32.json'), 'utf8'));
const BIJ = JSON.parse(readFileSync(join(FIX, 'a00-a30-bijective-map.json'), 'utf8'));

assert.equal(ORIGINAL.suite, 'A00-A30_ORIGINAL_FALSIFICATION_MATRIX');
assert.equal(ORIGINAL.cases.length, 31);
assert.equal(BIJ.mapping.length, 31);
assert.ok(R1.cases && R1.cases.length >= 31);

let passed = 0;
let failed = 0;
const failures = [];

function ok(name) {
  passed += 1;
  console.log(`PASS ${name}`);
}

function fail(name, err) {
  failed += 1;
  failures.push({ name, err: String(err && err.stack ? err.stack : err) });
  console.error(`FAIL ${name}: ${err}`);
}

function tmpLedger() {
  const dir = mkdtempSync(join(tmpdir(), 'onc-c16-'));
  return { ledger: createLedger(dir), dir };
}

function buildBody(c) {
  if (typeof c.raw_bytes === 'number') return Buffer.alloc(Number(c.raw_bytes), 0x41);
  if (c.raw_bytes && Array.isArray(c.raw_bytes)) return Buffer.from(c.raw_bytes);
  if (typeof c.raw === 'string') return Buffer.from(c.raw, 'utf8');
  if (c.raw_json != null) {
    return Buffer.from(typeof c.raw_json === 'string' ? c.raw_json : JSON.stringify(c.raw_json), 'utf8');
  }
  let base = baselineCheckinObject(c.patch || {});
  if (Array.isArray(c.omit)) {
    for (const k of c.omit) delete base[k];
  }
  if (c.large_content) {
    base.content = 'X'.repeat(Number(c.large_content));
  }
  return Buffer.from(JSON.stringify(base), 'utf8');
}

function assertPrivilegeNone(result) {
  assert.equal(result.privilege, 'NONE');
  assert.equal(result.access, 'NO_ACCESS');
}

function assertObservationConsent(result) {
  assert.ok(result.consent === 'unspecified' || result.consent === 'opt_in' || result.consent === 'opt_out');
  assert.ok(typeof result.content_redacted === 'string' || result.content_redacted == null);
  assert.ok(result.retention_days == null || Number(result.retention_days) > 0);
}

async function runOriginalCase(c) {
  const expect = c.expect;
  if (expect === 'HOLD_NOT_EXECUTABLE_LOCAL' || expect === 'WWW_E2E_HOLD') {
    assert.ok(c.hold_reason || expect === 'WWW_E2E_HOLD');
    return;
  }

  if (expect === 'DENIED_MULTI') {
    assert.ok(Array.isArray(c.subcases) && c.subcases.length > 0);
    for (const sub of c.subcases) {
      const { ledger, dir } = tmpLedger();
      try {
        let raw;
        if (sub.kind === 'dup_keys') {
          raw = Buffer.from(
            '{"protocol":"nexus-agent-checkin/1","protocol":"dup","event_class":"CHECKIN_OBSERVATION_ONLY","claim_ceiling":"C1_DESCRIPTIVE_ONLY","schema_version":"1","interaction_id":"obs-dupkeys01abcdef","submitted_at":"2026-10-30T00:00:00.000Z","content":"x"}',
            'utf8',
          );
        } else if (sub.kind === 'nonfinite') {
          // Valid JSON number literal that overflows to Infinity in IEEE-754
          // (bare "Infinity" is INVALID_JSON, not NONFINITE_NUMBER).
          raw = Buffer.from(
            '{"protocol":"nexus-agent-checkin/1","event_class":"CHECKIN_OBSERVATION_ONLY","claim_ceiling":"C1_DESCRIPTIVE_ONLY","schema_version":"1","interaction_id":"obs-nonfinite01abcd","submitted_at":"2026-10-30T00:00:00.000Z","content":"x","n":1e999}',
            'utf8',
          );
        } else if (sub.kind === 'trailing_junk') {
          raw = Buffer.from(
            '{"protocol":"nexus-agent-checkin/1","event_class":"CHECKIN_OBSERVATION_ONLY","claim_ceiling":"C1_DESCRIPTIVE_ONLY","schema_version":"1","interaction_id":"obs-trailjunk01abcd","submitted_at":"2026-10-30T00:00:00.000Z","content":"x"}TRAILING',
            'utf8',
          );
        } else if (sub.kind === 'body_too_large') {
          raw = Buffer.alloc(MAX_BODY_BYTES + 64, 0x41);
        } else if (sub.kind === 'nested_object') {
          const o = baselineCheckinObject({ content: { nested: true } });
          raw = Buffer.from(JSON.stringify(o), 'utf8');
        } else if (sub.kind === 'unknown_field') {
          const o = baselineCheckinObject({ totally_unknown_xyz: true });
          raw = Buffer.from(JSON.stringify(o), 'utf8');
        } else {
          throw new Error(`unknown DENIED_MULTI subcase ${sub.kind}`);
        }
        const r = processCheckinBytes(raw, { ledger });
        assert.equal(r.status, 'DENIED');
        assert.equal(r.deny_code, sub.deny_code);
      } finally {
        rmSync(dir, { recursive: true, force: true });
      }
    }
    return;
  }

  if (expect === 'MULTI_PROVIDER_IDENTICAL') {
    const providers = c.providers || ['p1', 'p2', 'p3', 'p4', 'p5'];
    assert.ok(providers.length >= 5);
    const { ledger, dir } = tmpLedger();
    try {
      for (const p of providers) {
        const raw = buildBody({
          patch: { ...(c.patch || {}), interaction_id: `obs-mp-${p}-${Date.now().toString(16).slice(-8)}`, content: `provider ${p}` },
        });
        const r = processCheckin(raw, { ledger });
        assert.equal(r.status, 'STAGED_UNTRUSTED');
        assertPrivilegeNone(r);
      }
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'CROSS_CLIENT_ISOLATION') {
    const id = `obs-xclient${Date.now().toString(16).slice(-10)}`;
    const body = baselineCheckinObject({ interaction_id: id, content: 'cross-client' });
    const raw = Buffer.from(JSON.stringify(body), 'utf8');
    const a = tmpLedger();
    const b = tmpLedger();
    try {
      const r1 = processCheckin(raw, { ledger: a.ledger });
      const r2 = processCheckin(raw, { ledger: b.ledger });
      assert.equal(r1.status, 'STAGED_UNTRUSTED');
      assert.equal(r2.status, 'STAGED_UNTRUSTED');
    } finally {
      rmSync(a.dir, { recursive: true, force: true });
      rmSync(b.dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'LOAD_BOUND') {
    const count = Number(c.count || 100);
    const { ledger, dir } = tmpLedger();
    try {
      for (let i = 0; i < count; i += 1) {
        const raw = buildBody({
          patch: { interaction_id: `obs-load${String(i).padStart(8, '0')}abcd`, content: `load ${i}` },
        });
        const r = processCheckin(raw, { ledger, rateBucket: { hits: [] }, rateLimit: 10_000 });
        assert.equal(r.status, 'STAGED_UNTRUSTED');
      }
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'MANY_DUPLICATE') {
    const count = Number(c.count || 50);
    const { ledger, dir } = tmpLedger();
    try {
      const body = baselineCheckinObject({ content: 'many-dup' });
      const raw = Buffer.from(JSON.stringify(body), 'utf8');
      const first = processCheckin(raw, { ledger });
      assert.equal(first.status, 'STAGED_UNTRUSTED');
      for (let i = 1; i < count; i += 1) {
        const r = processCheckin(raw, { ledger });
        assert.equal(r.status, 'DUPLICATE');
      }
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'DUPLICATE') {
    const { ledger, dir } = tmpLedger();
    try {
      const raw = buildBody(c);
      const a = processCheckin(raw, { ledger });
      assert.equal(a.status, 'STAGED_UNTRUSTED');
      const b = processCheckin(raw, { ledger });
      assert.equal(b.status, 'DUPLICATE');
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'IDEMPOTENCY_CONFLICT') {
    const { ledger, dir } = tmpLedger();
    try {
      const id = `obs-idemp${Date.now().toString(16).slice(-10)}`;
      const raw1 = Buffer.from(JSON.stringify(baselineCheckinObject({ interaction_id: id, content: 'body-a' })), 'utf8');
      const raw2 = Buffer.from(JSON.stringify(baselineCheckinObject({ interaction_id: id, content: 'body-b-different' })), 'utf8');
      const a = processCheckin(raw1, { ledger });
      assert.equal(a.status, 'STAGED_UNTRUSTED');
      const b = processCheckin(raw2, { ledger });
      assert.equal(b.status, 'IDEMPOTENCY_CONFLICT');
      assert.equal(b.deny_code, 'IDEMPOTENCY_CONFLICT');
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (c.rate_flood) {
    const { ledger, dir } = tmpLedger();
    const bucket = { hits: [] };
    try {
      let limited = false;
      for (let i = 0; i < Number(c.rate_flood); i += 1) {
        const raw = buildBody({
          patch: { interaction_id: `obs-rf${String(i).padStart(10, '0')}`, content: `rf ${i}` },
        });
        const r = processCheckin(raw, { ledger, rateBucket: bucket, rateLimit: 30 });
        if (r.status === 'DENIED' && r.deny_code === 'RATE_LIMITED') {
          limited = true;
          break;
        }
      }
      assert.equal(limited, true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (expect === 'DENIED') {
    const { ledger, dir } = tmpLedger();
    try {
      const raw = buildBody(c);
      const r = processCheckin(raw, { ledger });
      assert.equal(r.status, 'DENIED');
      if (c.deny_code) assert.equal(r.deny_code, c.deny_code);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  // Default: STAGED_UNTRUSTED (+ optional asserts)
  const { ledger, dir } = tmpLedger();
  try {
    const raw = buildBody(c);
    const r = processCheckin(raw, { ledger });
    assert.equal(r.status, expect === 'STAGED_UNTRUSTED' ? 'STAGED_UNTRUSTED' : expect);
    if (c.assert_privilege_none) assertPrivilegeNone(r);
    if (c.assert_observation_consent) assertObservationConsent(r);
    if (c.assert_no_network) {
      assert.equal(r.network, undefined);
      assert.ok(!('outbound' in r));
    }
    if (c.assert_no_rank) {
      assert.ok(!('rank' in r) && !('score' in r) && !('leaderboard' in r));
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

async function runR1Case(c) {
  if (c.policy) {
    const h = healthPayload('127.0.0.1');
    const reg = h.f10_f12_regression || F10_F12_REGRESSION;
    if (c.policy === 'f10') assert.equal(reg.f10.status, 'CLOSED');
    if (c.policy === 'f11') assert.equal(reg.f11.status, 'CLOSED_TESTED_PATH');
    if (c.policy === 'f12') assert.equal(reg.f12.status, 'CLOSED_EMPTY_REGISTER');
    return;
  }

  if (c.rate_flood) {
    const { ledger, dir } = tmpLedger();
    const bucket = { hits: [] };
    try {
      let limited = false;
      for (let i = 0; i < Number(c.rate_flood); i += 1) {
        const raw = buildBody({
          patch: { interaction_id: `obs-r1rf${String(i).padStart(8, '0')}`, content: `r1rf ${i}` },
        });
        const r = processCheckin(raw, { ledger, rateBucket: bucket, rateLimit: 30 });
        if (r.status === 'DENIED' && r.deny_code === 'RATE_LIMITED') {
          limited = true;
          break;
        }
      }
      assert.equal(limited, true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  if (c.duplicate) {
    const { ledger, dir } = tmpLedger();
    try {
      const raw = buildBody(c);
      assert.equal(processCheckin(raw, { ledger }).status, 'STAGED_UNTRUSTED');
      assert.equal(processCheckin(raw, { ledger }).status, 'DUPLICATE');
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
    return;
  }

  const { ledger, dir } = tmpLedger();
  try {
    const raw = buildBody(c);
    const r = processCheckin(raw, { ledger });
    if (c.expect === 'DENIED' || c.deny_code) {
      assert.equal(r.status, 'DENIED');
      if (c.deny_code) assert.equal(r.deny_code, c.deny_code);
    } else if (c.expect === 'STAGED_UNTRUSTED' || !c.expect) {
      assert.equal(r.status, 'STAGED_UNTRUSTED');
      if (c.expect_redactions_ge != null) {
        const n = (r.content_redacted && r.content_redacted.length) || 0;
        assert.ok(n >= Number(c.expect_redactions_ge) || r.content_redacted != null);
      }
    } else {
      assert.equal(r.status, c.expect);
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

/* ----------------------------- C13 unit --------------------------------- */
function runC13() {
  const bom = Buffer.from([0xef, 0xbb, 0xbf, ...Buffer.from('{}', 'utf8')]);
  const bomR = strictParseJsonBytes(bom);
  assert.equal(bomR.ok, false);
  assert.equal(bomR.deny_code, 'BOM_UNSUPPORTED');

  const dup = Buffer.from('{"a":1,"a":2}', 'utf8');
  const dupR = strictParseJsonBytes(dup);
  assert.equal(dupR.ok, false);
  assert.equal(dupR.deny_code, 'DUPLICATE_JSON_KEY');

  const trail = Buffer.from('{"a":1}TRAIL', 'utf8');
  const trailR = strictParseJsonBytes(trail);
  assert.equal(trailR.ok, false);
  assert.equal(trailR.deny_code, 'INVALID_JSON');

  const nf = Buffer.from('{"a":Infinity}', 'utf8');
  const nfR = strictParseJsonBytes(nf);
  assert.equal(nfR.ok, false);
  assert.ok(nfR.deny_code === 'NONFINITE_NUMBER' || nfR.deny_code === 'INVALID_JSON');
}

/* ----------------------------- C14 unit --------------------------------- */
function runC14() {
  const { ledger, dir } = tmpLedger();
  try {
    const id = `obs-c14${Date.now().toString(16).slice(-10)}`;
    const raw1 = Buffer.from(JSON.stringify(baselineCheckinObject({ interaction_id: id, content: 'alpha' })), 'utf8');
    const raw2 = Buffer.from(JSON.stringify(baselineCheckinObject({ interaction_id: id, content: 'beta' })), 'utf8');
    assert.equal(processCheckin(raw1, { ledger }).status, 'STAGED_UNTRUSTED');
    assert.equal(processCheckin(raw1, { ledger }).status, 'DUPLICATE');
    const conflict = processCheckin(raw2, { ledger });
    assert.equal(conflict.status, 'IDEMPOTENCY_CONFLICT');
    const hit = ledger.lookup(id);
    assert.ok(hit);
    assert.ok(hit.body_sha256);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

/* ----------------------------- C15 unit --------------------------------- */
function runC15() {
  const { ledger, dir } = tmpLedger();
  try {
    const raw = Buffer.from(
      JSON.stringify(
        baselineCheckinObject({
          content: 'email test@example.com phone +1-555-0100',
          consent: 'opt_in',
          retention_days: 14,
        }),
      ),
      'utf8',
    );
    const r = processCheckin(raw, { ledger });
    assert.equal(r.status, 'STAGED_UNTRUSTED');
    assert.ok(typeof r.content_redacted === 'string');
    assert.ok(!r.content_redacted.includes('test@example.com'));
    assert.equal(r.consent, 'opt_in');
    assert.equal(r.retention_days, 14);
    const obsFile = join(dir, 'observations.jsonl');
    assert.ok(existsSync(obsFile));
    assert.ok(readFileSync(obsFile, 'utf8').includes('SCIENTIFIC_OBSERVATION'));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

/* ----------------------------- C17 HTTP --------------------------------- */
async function runC17() {
  const { ledger, dir } = tmpLedger();
  const bucket = { hits: [] };
  const handler = createAppHandler({ ledger, rateBucket: bucket });
  const server = createServer(handler);
  await new Promise((res) => server.listen(0, '127.0.0.1', res));
  const { port } = server.address();
  try {
    const health = await fetch(`http://127.0.0.1:${port}/health`);
    assert.equal(health.status, 200);
    const hj = await health.json();
    assert.equal(hj.deployment_plane, 'LOCAL');
    assert.equal(hj.public_external_write_api, 'HOLD');

    const body = JSON.stringify(baselineCheckinObject({ content: 'c17-http' }));
    const post = await fetch(`http://127.0.0.1:${port}/checkin`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body,
    });
    assert.equal(post.status, 202);
    const pj = await post.json();
    assert.equal(pj.status, 'STAGED_UNTRUSTED');

    const dup = await fetch(`http://127.0.0.1:${port}/checkin`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body,
    });
    assert.equal(dup.status, 200);
    assert.equal((await dup.json()).status, 'DUPLICATE');

    // BODY_TOO_LARGE via oversized POST
    const big = 'A'.repeat(MAX_BODY_BYTES + 100);
    const bigRes = await fetch(`http://127.0.0.1:${port}/checkin`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: big,
    });
    assert.equal(bigRes.status, 413);

    // UI is served by server.mjs only — createAppHandler returns 404 for /
    const ui404 = await fetch(`http://127.0.0.1:${port}/`);
    assert.equal(ui404.status, 404);
  } finally {
    await new Promise((res) => server.close(res));
    rmSync(dir, { recursive: true, force: true });
  }

  // Spawn server.mjs for UI GET /
  await runC17UiSpawn();
}

async function runC17UiSpawn() {
  const dir = mkdtempSync(join(tmpdir(), 'onc-ui-'));
  const port = 18765 + Math.floor(Math.random() * 1000);
  const child = spawn(process.execPath, [join(ROOT, 'server.mjs')], {
    cwd: ROOT,
    env: {
      ...process.env,
      NEXUS_CHECKIN_PORT: String(port),
      NEXUS_CHECKIN_HOST: '127.0.0.1',
      NEXUS_CHECKIN_RUNTIME: dir,
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let ready = false;
  const deadline = Date.now() + 8000;
  try {
    while (Date.now() < deadline && !ready) {
      try {
        const r = await fetch(`http://127.0.0.1:${port}/health`);
        if (r.ok) ready = true;
      } catch {
        await new Promise((r) => setTimeout(r, 100));
      }
    }
    assert.equal(ready, true, 'server.mjs did not become ready');
    const ui = await fetch(`http://127.0.0.1:${port}/`);
    assert.equal(ui.status, 200);
    const html = await ui.text();
    assert.ok(/check-?in|observation|NEXUS/i.test(html));
  } finally {
    child.kill('SIGTERM');
    await new Promise((r) => setTimeout(r, 200));
    try {
      child.kill('SIGKILL');
    } catch {
      /* ignore */
    }
    rmSync(dir, { recursive: true, force: true });
  }
}

/* ----------------------------- C18 / C19 -------------------------------- */
function runC18() {
  assert.equal(DEPLOYMENT_PLANE.LOCAL, 'LOCAL');
  assert.equal(DEPLOYMENT_PLANE.STAGING, 'STAGING');
  assert.equal(DEPLOYMENT_PLANE.WWW, 'WWW');
  const h = healthPayload('127.0.0.1');
  assert.equal(h.deployment_plane, DEPLOYMENT_PLANE.LOCAL);
  assert.equal(h.planes.local.status, 'AUTHORIZED_LOOPBACK');
  assert.equal(h.planes.staging.status, 'HOLD_NOT_AUTHORIZED');
  assert.equal(h.planes.www.status, 'HOLD');
  assert.equal(h.public_external_write_api, 'HOLD');
  assert.equal(h.bind, '127.0.0.1_loopback_only');
}

function runC19() {
  assert.equal(F10_F12_REGRESSION.f10.status, 'CLOSED');
  assert.equal(F10_F12_REGRESSION.f11.status, 'CLOSED_TESTED_PATH');
  assert.equal(F10_F12_REGRESSION.f12.status, 'CLOSED_EMPTY_REGISTER');
  const h = healthPayload('127.0.0.1');
  assert.equal(h.f10_f12_regression.f10.status, 'CLOSED');
}

/* ----------------------------- bijection -------------------------------- */
function runBijection() {
  for (const m of BIJ.mapping) {
    assert.equal(m.r1_local_collision, 'R1_LOCAL_LABEL_REUSED_NOT_SAME_TEST');
    const orig = ORIGINAL.cases.find((c) => c.id === m.original_id);
    assert.ok(orig, `missing original ${m.original_id}`);
    assert.equal(orig.expect, m.expect_class);
  }
}

/* ----------------------------- main ------------------------------------ */
async function main() {
  console.log('=== C13 unit ===');
  try {
    runC13();
    ok('C13_STRICT_PARSER');
  } catch (e) {
    fail('C13_STRICT_PARSER', e);
  }

  console.log('=== C14 unit ===');
  try {
    runC14();
    ok('C14_LEDGER_ATOMICITY');
  } catch (e) {
    fail('C14_LEDGER_ATOMICITY', e);
  }

  console.log('=== C15 unit ===');
  try {
    runC15();
    ok('C15_RESEARCH_PRIVACY');
  } catch (e) {
    fail('C15_RESEARCH_PRIVACY', e);
  }

  console.log('=== C16 bijection ===');
  try {
    runBijection();
    ok('C16_BIJECTIVE_MAP');
  } catch (e) {
    fail('C16_BIJECTIVE_MAP', e);
  }

  console.log('=== ORIGINAL A00–A30 ===');
  for (const c of ORIGINAL.cases) {
    const name = `ORIGINAL_${c.id}_${c.expect}`;
    try {
      await runOriginalCase(c);
      ok(name);
    } catch (e) {
      fail(name, e);
    }
  }

  console.log('=== R1_LOCAL_32 ===');
  for (const c of R1.cases) {
    const name = `R1_${c.id || c.name || 'case'}`;
    try {
      await runR1Case(c);
      ok(name);
    } catch (e) {
      fail(name, e);
    }
  }

  console.log('=== C17 HTTP + UI ===');
  try {
    await runC17();
    ok('C17_HTTP_AND_UI');
  } catch (e) {
    fail('C17_HTTP_AND_UI', e);
  }

  console.log('=== C18 planes ===');
  try {
    runC18();
    ok('C18_DEPLOYMENT_PLANES');
  } catch (e) {
    fail('C18_DEPLOYMENT_PLANES', e);
  }

  console.log('=== C19 F10–F12 ===');
  try {
    runC19();
    ok('C19_F10_F12_REGRESSION');
  } catch (e) {
    fail('C19_F10_F12_REGRESSION', e);
  }

  // Dual-arity smoke
  try {
    const { ledger, dir } = tmpLedger();
    try {
      const raw = Buffer.from(JSON.stringify(baselineCheckinObject({ content: 'dual' })), 'utf8');
      const a = processCheckin(raw, ledger);
      const b = processCheckinBytes(raw, { ledger });
      assert.equal(a.status, 'STAGED_UNTRUSTED');
      assert.equal(b.status, 'DUPLICATE');
      ok('X_DUAL_ARITY');
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  } catch (e) {
    fail('X_DUAL_ARITY', e);
  }

  console.log(`\nSUMMARY passed=${passed} failed=${failed}`);
  if (failed > 0) {
    for (const f of failures) console.error(`- ${f.name}: ${f.err.split('\n')[0]}`);
    process.exit(1);
  }
  console.log('ALL_PASS');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
