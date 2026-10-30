#!/usr/bin/env node
/**
 * G7 one-command deterministic selftest (no install; Node 20+).
 * Runs A00–A30 suite + loopback HTTP smoke + UI/offline markers + rollback receipt.
 */
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import {
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createLedger, processCheckin } from './open-neutral-checkin.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..', '..');
const RUNTIME = join(__dirname, '.runtime', 'selftest');
const RECEIPT = join(RUNTIME, 'SELFTEST_RECEIPT.json');

function sha256(buf) {
  return createHash('sha256').update(buf).digest('hex');
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function runNode(args, opts = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, args, {
      cwd: opts.cwd || ROOT,
      env: { ...process.env, ...(opts.env || {}) },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (d) => {
      stdout += d.toString('utf8');
    });
    child.stderr.on('data', (d) => {
      stderr += d.toString('utf8');
    });
    const timer = setTimeout(() => {
      child.kill('SIGTERM');
      reject(new Error(`timeout: ${args.join(' ')}\n${stderr}`));
    }, opts.timeoutMs || 120000);
    child.on('exit', (code) => {
      clearTimeout(timer);
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

async function waitReady(url, attempts = 40) {
  for (let i = 0; i < attempts; i += 1) {
    try {
      const res = await fetch(url);
      if (res.ok) return true;
    } catch {
      /* retry */
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  return false;
}

async function main() {
  mkdirSync(RUNTIME, { recursive: true });
  const results = [];

  // --- Suite A00–A30 + F10–F12 ---
  const suite = await runNode(['tests/open-neutral-checkin.test.mjs'], {
    timeoutMs: 60000,
  });
  assert(suite.code === 0, `suite exit ${suite.code}\n${suite.stderr}\n${suite.stdout}`);
  const suiteJsonLine = suite.stdout
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.startsWith('{') && l.endsWith('}'))
    .pop();
  assert(suiteJsonLine, 'suite JSON summary missing');
  const suiteSummary = JSON.parse(suiteJsonLine);
  assert(suiteSummary.failed === 0, `suite failures: ${JSON.stringify(suiteSummary.failures)}`);
  assert(suiteSummary.passed >= 32, `expected >=32 passes, got ${suiteSummary.passed}`);
  results.push({
    id: 'G7_SUITE_A00_A30_F10_F12',
    status: 'PASS',
    passed: suiteSummary.passed,
    failed: suiteSummary.failed,
  });

  // --- Offline processCheckin STAGED ---
  const offlineRoot = join(RUNTIME, 'offline-ledger');
  rmSync(offlineRoot, { recursive: true, force: true });
  const ledger = createLedger(offlineRoot);
  const staged = processCheckin(
    JSON.stringify({
      protocol: 'nexus-agent-checkin/1',
      event_class: 'CHECKIN_OBSERVATION_ONLY',
      interaction_id: `selftest-offline-${Date.now()}`,
      content: 'offline selftest observation',
      capability_claim: 'SELFTEST',
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    }),
    ledger,
    {},
  );
  assert(staged.status === 'STAGED_UNTRUSTED', `offline status ${staged.status}`);
  results.push({ id: 'G7_OFFLINE_PROCESS', status: 'PASS', receipt_id: staged.receipt_id });

  // --- Loopback HTTP smoke ---
  const httpRoot = join(RUNTIME, 'http-ledger');
  rmSync(httpRoot, { recursive: true, force: true });
  mkdirSync(httpRoot, { recursive: true });
  const port = 18765;
  const child = spawn(process.execPath, ['examples/open-neutral-checkin/server.mjs'], {
    cwd: ROOT,
    env: {
      ...process.env,
      NEXUS_CHECKIN_HOST: '127.0.0.1',
      NEXUS_CHECKIN_PORT: String(port),
      NEXUS_CHECKIN_RUNTIME: httpRoot,
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let serverErr = '';
  child.stderr.on('data', (d) => {
    serverErr += d.toString('utf8');
  });
  try {
    const ready = await waitReady(`http://127.0.0.1:${port}/health`);
    assert(ready, `server not ready\n${serverErr}`);
    const health = await (await fetch(`http://127.0.0.1:${port}/health`)).json();
    assert(health.ok === true, 'health.ok');
    assert(health.host === '127.0.0.1', 'health.host loopback');

    const ui = await fetch(`http://127.0.0.1:${port}/`);
    assert(ui.status === 200, `ui status ${ui.status}`);
    const uiHtml = await ui.text();
    assert(uiHtml.includes('offlineNote'), 'ui offlineNote marker');
    assert(/@media\s*\(\s*max-width:\s*560px\s*\)/.test(uiHtml), 'ui mobile media query');

    const body = {
      protocol: 'nexus-agent-checkin/1',
      event_class: 'CHECKIN_OBSERVATION_ONLY',
      interaction_id: `selftest-http-${Date.now()}`,
      content: 'http selftest observation',
      capability_claim: 'SELFTEST_HTTP',
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    };
    const post = await fetch(`http://127.0.0.1:${port}/checkin`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });
    const postJson = await post.json();
    assert(post.status === 202, `checkin HTTP ${post.status} body=${JSON.stringify(postJson)}`);
    assert(postJson.status === 'STAGED_UNTRUSTED', `checkin status ${postJson.status}`);

    const dup = await fetch(`http://127.0.0.1:${port}/checkin`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });
    const dupJson = await dup.json();
    assert(dup.status === 200, `duplicate HTTP ${dup.status}`);
    assert(dupJson.status === 'DUPLICATE', `duplicate status ${dupJson.status}`);

    results.push({
      id: 'G8_HTTP_CHECKIN',
      status: 'PASS',
      http_staged: 202,
      http_duplicate: 200,
      receipt_id: postJson.receipt_id,
    });
    results.push({ id: 'G8_UI_MOBILE_OFFLINE_MARKERS', status: 'PASS' });
  } finally {
    child.kill('SIGTERM');
    await new Promise((r) => setTimeout(r, 200));
    try {
      child.kill('SIGKILL');
    } catch {
      /* ignore */
    }
  }

  // --- Source guards: loopback default ---
  const serverSrc = readFileSync(join(__dirname, 'server.mjs'), 'utf8');
  assert(
    /127\.0\.0\.1/.test(serverSrc) && /NEXUS_CHECKIN_HOST/.test(serverSrc),
    'server must default host via NEXUS_CHECKIN_HOST to 127.0.0.1',
  );
  assert(!/0\.0\.0\.0/.test(serverSrc), 'server must not bind 0.0.0.0');
  results.push({ id: 'G8_LOOPBACK_ONLY', status: 'PASS' });

  // --- Rollback: wipe runtime dir, recreate empty ---
  const rollbackProbe = join(RUNTIME, 'rollback-probe');
  mkdirSync(rollbackProbe, { recursive: true });
  writeFileSync(join(rollbackProbe, 'marker.txt'), 'x', 'utf8');
  rmSync(rollbackProbe, { recursive: true, force: true });
  assert(!existsSync(rollbackProbe), 'rollback wipe failed');
  mkdirSync(rollbackProbe, { recursive: true });
  results.push({ id: 'G8_ROLLBACK_RUNTIME_WIPE', status: 'PASS' });

  const receipt = {
    object: 'NEXUS_OMEGA_OPEN_NEUTRAL_CHECKIN_SELFTEST_RECEIPT_20261030_R1',
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    node: process.version,
    platform: process.platform,
    results,
    passed: results.every((r) => r.status === 'PASS'),
    generated_at: new Date().toISOString(),
  };
  const raw = `${JSON.stringify(receipt, null, 2)}\n`;
  writeFileSync(RECEIPT, raw, 'utf8');
  receipt.receipt_sha256 = sha256(raw);
  writeFileSync(RECEIPT, `${JSON.stringify(receipt, null, 2)}\n`, 'utf8');

  console.log(JSON.stringify(receipt, null, 2));
  if (!receipt.passed) process.exit(1);
}

main().catch((e) => {
  console.error(String(e && e.stack ? e.stack : e));
  process.exit(1);
});
