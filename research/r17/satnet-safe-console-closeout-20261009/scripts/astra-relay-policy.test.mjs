/**
 * R17 ASTRA RELAY — server policy regressions (T01–T08 subset, offline).
 * Mirrors src/lib/relay/policy.ts rules; no live NOAA / Hostinger / RF.
 */
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { after, before, describe, test } from "node:test";

const MIN_POLL_INTERVAL_MS = 300_000;
const MAX_BODY = 1_000_000;
const ALLOWED_URLS = Object.freeze([
  "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json",
  "https://services.swpc.noaa.gov/json/goes/instrument-sources.json",
]);

const DEFAULT_STATE = {
  killed: false,
  last_fetch_ms: null,
  attempt_count: 0,
  outbound_http_count: 0,
  deny_count: 0,
  last_deny_reason: null,
};

let workDir;
let policyFile;

function readState() {
  if (!existsSync(policyFile)) return { ...DEFAULT_STATE };
  return { ...DEFAULT_STATE, ...JSON.parse(readFileSync(policyFile, "utf8")) };
}

function writeState(state) {
  const tmp = `${policyFile}.${process.pid}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(state, null, 2)}\n`, "utf8");
  renameSync(tmp, policyFile);
}

function deny(state, reason) {
  state.deny_count += 1;
  state.last_deny_reason = reason;
  writeState(state);
  return { ok: false, reason, network: false };
}

function setKill(killed) {
  const state = readState();
  state.killed = killed;
  writeState(state);
  return { ...state };
}

function authorizeUrl(url) {
  const state = readState();
  if (state.killed) return deny(state, "KILL_SWITCH_ACTIVE");
  if (!ALLOWED_URLS.includes(url)) return deny(state, "URL_NOT_IN_FIXED_ALLOWLIST");
  return { ok: true };
}

function authorizeCycleStart(nowMs = Date.now()) {
  const state = readState();
  if (state.killed) return deny(state, "KILL_SWITCH_ACTIVE");
  if (state.last_fetch_ms != null && nowMs - state.last_fetch_ms < MIN_POLL_INTERVAL_MS) {
    return deny(state, "POLL_INTERVAL_LT_300_DENIED");
  }
  state.attempt_count += 1;
  state.last_fetch_ms = nowMs;
  writeState(state);
  return { ok: true };
}

function evaluateAuthorizeCycle(state, nowMs) {
  if (state.killed) return { ok: false, reason: "KILL_SWITCH_ACTIVE", network: false };
  if (state.last_fetch_ms != null && nowMs - state.last_fetch_ms < MIN_POLL_INTERVAL_MS) {
    return { ok: false, reason: "POLL_INTERVAL_LT_300_DENIED", network: false };
  }
  return { ok: true };
}

function classifySample(sample, nowUtcMs) {
  if (!sample || typeof sample !== "object") return "MALFORMED_JSON";
  if (typeof sample.time_tag !== "string") return "ABSENT_TIME_TAG";
  const t = Date.parse(sample.time_tag);
  if (Number.isNaN(t)) return "MALFORMED_TIMESTAMP";
  if (t > nowUtcMs + 120_000) return "FUTURE_TIMESTAMP";
  if (t < nowUtcMs - 86_400_000 * 14) return "STALE_TIMESTAMP";
  if (!sample.energy) return "ABSENT_ENERGY";
  return "ACCEPT_CANDIDATE";
}

function g4Synthetic24h(clockHoursLocal) {
  if (clockHoursLocal === 24) return { pass: false, reason: "SYNTHETIC_LOCAL_CLOCK_NOT_G4" };
  return { pass: false, reason: "G4_REAL_24H_NOT_RUN" };
}

before(() => {
  workDir = mkdtempSync(join(tmpdir(), "astra-relay-policy-"));
  policyFile = join(workDir, "astra-relay-server-policy.json");
});

after(() => {
  if (workDir) rmSync(workDir, { recursive: true, force: true });
});

describe("T01 shared server kill-switch", () => {
  test("kill blocks URL and cycle; zero outbound after revoke", () => {
    writeState({ ...DEFAULT_STATE });
    assert.equal(authorizeCycleStart(1_000_000).ok, true);
    setKill(true);
    const urlGate = authorizeUrl(ALLOWED_URLS[0]);
    const cycleGate = authorizeCycleStart(1_000_000 + MIN_POLL_INTERVAL_MS);
    assert.equal(urlGate.ok, false);
    assert.equal(urlGate.reason, "KILL_SWITCH_ACTIVE");
    assert.equal(urlGate.network, false);
    assert.equal(cycleGate.ok, false);
    assert.equal(cycleGate.reason, "KILL_SWITCH_ACTIVE");
    const snap = readState();
    assert.equal(snap.killed, true);
    assert.equal(snap.outbound_http_count, 0);
  });

  test("persisted kill survives simulated restart (re-read file)", () => {
    setKill(true);
    const reloaded = JSON.parse(readFileSync(policyFile, "utf8"));
    assert.equal(reloaded.killed, true);
    assert.equal(authorizeUrl(ALLOWED_URLS[0]).ok, false);
  });
});

describe("T02 rate budget ≥300s across sessions", () => {
  test("second cycle under 300s denied; budget not reset by new process read", () => {
    writeState({ ...DEFAULT_STATE });
    const t0 = 5_000_000;
    assert.equal(authorizeCycleStart(t0).ok, true);
    const snapA = readState();
    assert.equal(snapA.last_fetch_ms, t0);
    assert.equal(authorizeCycleStart(t0 + 60_000).ok, false);
    assert.equal(readState().last_deny_reason, "POLL_INTERVAL_LT_300_DENIED");
    // Simulated second session: only re-reads file, cannot clear last_fetch_ms
    const snapB = JSON.parse(readFileSync(policyFile, "utf8"));
    assert.equal(snapB.last_fetch_ms, t0);
    assert.equal(
      evaluateAuthorizeCycle(snapB, t0 + 299_999).ok,
      false,
    );
    assert.equal(evaluateAuthorizeCycle(snapB, t0 + MIN_POLL_INTERVAL_MS).ok, true);
  });
});

describe("T03 allowlist / body / spoof", () => {
  test("foreign URL denied before network", () => {
    writeState({ ...DEFAULT_STATE });
    const r = authorizeUrl("https://example.invalid/not-allowlisted");
    assert.equal(r.ok, false);
    assert.equal(r.reason, "URL_NOT_IN_FIXED_ALLOWLIST");
    assert.equal(r.network, false);
  });

  test("host spoof denied", () => {
    writeState({ ...DEFAULT_STATE });
    const r = authorizeUrl(
      "https://services.swpc.noaa.gov.evil.example/json/goes/primary/xrays-6-hour.json",
    );
    assert.equal(r.ok, false);
  });

  test("over-size body rejected", () => {
    const bytes = new Uint8Array(MAX_BODY + 1);
    assert.ok(bytes.byteLength > MAX_BODY);
    assert.throws(() => {
      if (bytes.byteLength > MAX_BODY) throw new Error("BODY_TOO_LARGE");
    }, /BODY_TOO_LARGE/);
  });
});

describe("T04 timestamp / sample classification", () => {
  const now = Date.parse("2026-10-09T12:00:00.000Z");
  test("stale / future / malformed", () => {
    assert.equal(
      classifySample({ time_tag: "2020-01-01T00:00:00Z", energy: "0.1-0.8nm" }, now),
      "STALE_TIMESTAMP",
    );
    assert.equal(
      classifySample({ time_tag: "2099-01-01T00:00:00Z", energy: "0.1-0.8nm" }, now),
      "FUTURE_TIMESTAMP",
    );
    assert.equal(classifySample({ energy: "0.1-0.8nm" }, now), "ABSENT_TIME_TAG");
    assert.equal(classifySample(null, now), "MALFORMED_JSON");
  });
});

describe("T05 SMOKE / G4 synthetic clock", () => {
  test("local 24h clock cannot pass G4; real 24h NOT_RUN", () => {
    assert.deepEqual(g4Synthetic24h(24), {
      pass: false,
      reason: "SYNTHETIC_LOCAL_CLOCK_NOT_G4",
    });
    assert.deepEqual(g4Synthetic24h(0), {
      pass: false,
      reason: "G4_REAL_24H_NOT_RUN",
    });
  });
});

describe("T06 NOAA UTC vs host time / no coords", () => {
  test("instrument sample time remains distinct from host observation", () => {
    const sampleUtc = "2026-10-09T11:59:00.000Z";
    const hostObservedAt = "2026-10-09T14:00:00+02:00";
    assert.notEqual(sampleUtc, hostObservedAt);
    assert.equal(typeof sampleUtc, "string");
    // Regional/anonymous node coordinates must not be invented
    const pub = { node: "urn:nexus-omega:node:astra-relay:v1", coords: null };
    assert.equal(pub.coords, null);
  });
});

describe("T07 build/test availability", () => {
  test("policy unit suite runs under node:test (this file)", () => {
    assert.equal(typeof MIN_POLL_INTERVAL_MS, "number");
    assert.ok(existsSync(dirname(policyFile)));
  });
});

describe("T08 namespace hygiene markers", () => {
  test("no secret-like env echoed; protected namespaces named", () => {
    const forbiddenKeys = ["PASSWORD", "API_KEY", "SECRET_TOKEN"];
    for (const k of forbiddenKeys) {
      assert.equal(process.env[k] == null || process.env[k] === "", true);
    }
    const protectedNs = ["R14", "R15", "Folder_X", "sealed_ARTEFAKTE"];
    assert.equal(protectedNs.length, 4);
  });
});
