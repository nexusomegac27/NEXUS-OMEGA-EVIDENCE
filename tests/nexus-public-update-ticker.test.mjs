// SPDX-License-Identifier: Apache-2.0
import test from "node:test";
import assert from "node:assert/strict";
import {
  TICKER, parsePublicFeed, parseGitHubCommits, readSources
} from "../examples/nexus-public-update-ticker-v1.mjs";

const NOW = Date.parse("2026-10-11T08:00:00Z");
const SHA = "7ea59978c4f3d56eb87993f8d6881399be30e657";
const later = (n) => new Date(NOW + n).toISOString();
function feed() {
  return {
    object: "NEXUS_PUBLIC_EVENT_REGISTRY_DERIVATIVE_V1",
    canonical_authority: false,
    claim_ceiling: "C1_DESCRIPTIVE_ONLY",
    updated_at_utc: later(-5000),
    events: [
      {canonical_sequence: 1, event_type: "HOLD", object: "R27",
       short_description: "Scoped hold", timestamp_utc: later(-9000),
       detail_link: "/research/", claim_ceiling: TICKER.claim},
      {canonical_sequence: 2, event_type: "SYSTEM", object: "R27",
       short_description: "Documented update", timestamp_utc: later(-20000),
       detail_link: "/status/public-event-registry.json", claim_ceiling: TICKER.claim}
    ]
  };
}
function commits() {
  return [{sha: SHA, commit: {message: "R27 research source merged\n\nNot a WWW deploy",
    committer: {date: later(-15000)}}}];
}
function fakeResponse(x, status = 200) {
  return {ok: status >= 200 && status < 300, status,
    headers: {get: () => null}, text: async () => JSON.stringify(x)};
}

test("T0 feed accepts exact public derivative and preserves C1", () => {
  const p = parsePublicFeed(feed(), NOW);
  assert.equal(p.freshness, "RECENT_SOURCE");
  assert.equal(p.events.length, 2);
  assert.equal(p.events[0].id, "event:2");
  assert.equal(p.events[0].level, "PUBLIC_DERIVATIVE_C1");
});
test("T1 canonical ordering uses sequence, not timestamp", () => {
  assert.deepEqual(parsePublicFeed(feed(), NOW).events.map(x => x.sequence), [2, 1]);
});
test("T2 stale source remains visible but explicitly stale", () => {
  const x = feed(); x.updated_at_utc = later(-48 * 3600000);
  assert.equal(parsePublicFeed(x, NOW).freshness, "STALE_SOURCE");
});
test("T3 authoritative or promoted public feed fails closed", () => {
  const a = feed(); a.canonical_authority = true;
  assert.throws(() => parsePublicFeed(a, NOW), /INVALID_PUBLIC_EVENT_REGISTRY/);
  const b = feed(); b.claim_ceiling = "C2";
  assert.throws(() => parsePublicFeed(b, NOW), /INVALID_PUBLIC_EVENT_REGISTRY/);
});
test("T4 repeated event sequence rejected", () => {
  const x = feed(); x.events[1].canonical_sequence = 1;
  assert.throws(() => parsePublicFeed(x, NOW), /INVALID_OR_DUPLICATE_EVENT/);
});
test("T5 future publication timestamp rejected", () => {
  const x = feed(); x.updated_at_utc = later(86400000);
  assert.throws(() => parsePublicFeed(x, NOW), /FUTURE_PUBLIC_EVENT_REGISTRY/);
});
test("T6 unsafe external link is removed, not executed", () => {
  const x = feed(); x.events[0].detail_link = "//evil.invalid/payload";
  assert.equal(parsePublicFeed(x, NOW).events[1].href, null);
  const z = feed(); z.events[0].detail_link = "/../../secrets";
  assert.equal(parsePublicFeed(z, NOW).events[1].href, null);
});
test("T7 invalid event type, future event, or claims fail closed", () => {
  for (const change of [
    ["event_type", "NEXUS_INTERNAL_APPROVAL"],
    ["claim_ceiling", "PROMOTED"],
    ["timestamp_utc", later(86400000)]
  ]) {
    const x = feed(); x.events[0][change[0]] = change[1];
    assert.throws(() => parsePublicFeed(x, NOW), /INVALID_OR_DUPLICATE_EVENT/);
  }
});
test("T8 GitHub commits display only first-line SHA-linked evidence", () => {
  const p = parseGitHubCommits(commits(), NOW);
  assert.equal(p.events[0].href,
    "https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/" + SHA);
  assert.equal(p.events[0].description, "R27 research source merged");
  assert.equal(p.events[0].level, "TRANSPORT_ONLY_NOT_RUNTIME_AUTHORITY");
});
test("T9 invalid commit SHAs reject, never fabricate clickable references", () => {
  const bad = commits(); bad[0].sha = "not-a-real-sha";
  assert.throws(() => parseGitHubCommits(bad, NOW), /INVALID_GITHUB_COMMIT/);
});
test("T10 duplicate commit has one row only", () => {
  const a = commits()[0]; const p = parseGitHubCommits([a, a], NOW);
  assert.equal(p.events.length, 1);
});
test("T11 stale GitHub source is marked stale not LIVE", () => {
  const x = commits(); x[0].commit.committer.date = later(-3 * 86400000);
  assert.equal(parseGitHubCommits(x, NOW).freshness, "STALE_SOURCE");
});
test("T12 handles GitHub offline, public registry still usable", async () => {
  const p = await readSources(async url => {
    if (url.startsWith("https:")) throw new Error("simulated offline");
    return fakeResponse(feed());
  }, NOW);
  assert.equal(p.public.events.length, 2);
  assert.equal(p.github, null);
  assert.deepEqual(p.errors, [false, true]);
});
test("T13 handles public registry offline, GitHub still usable", async () => {
  const p = await readSources(async url => {
    if (url.startsWith("/")) return fakeResponse({}, 503);
    return fakeResponse(commits());
  }, NOW);
  assert.equal(p.public, null);
  assert.equal(p.github.events[0].sha, SHA);
  assert.deepEqual(p.errors, [true, false]);
});
test("T14 neither source available => unknown, not invented LIVE", async () => {
  const p = await readSources(async () => { throw new Error("unavailable"); }, NOW);
  assert.equal(p.public, null);
  assert.equal(p.github, null);
  assert.deepEqual(p.errors, [true, true]);
});
test("T15 bounded payload rejects huge public response", async () => {
  const p = await readSources(async () => ({
    ok: true, status: 200,
    headers: {get: () => "200000"},
    text: async () => JSON.stringify(feed())
  }), NOW);
  assert.deepEqual(p.errors, [true, true]);
});
test("T16 protocol remains read-only: public GET+GitHub GET, never POST", async () => {
  const seen = [];
  await readSources(async (url, opts) => {
    seen.push({url, opts});
    return fakeResponse(url.startsWith("/") ? feed() : commits());
  }, NOW);
  assert.equal(seen.length, 2);
  assert.ok(seen.every(x => x.opts.method === "GET" &&
    x.opts.credentials === "omit"));
  assert.ok(seen.every(x => !/token|secret|auth/i.test(JSON.stringify(x.opts))));
});
test("T18 actual response byte SHA-256 has fingerprint semantics, not authenticity", async () => {
  const p = await readSources(async url =>
    fakeResponse(url.startsWith("/") ? feed() : commits()), NOW);
  if (globalThis.crypto?.subtle) {
    assert.match(p.public.sha256, /^[a-f0-9]{64}$/);
    assert.match(p.github.sha256, /^[a-f0-9]{64}$/);
    assert.notEqual(p.public.sha256, p.github.sha256);
  } else {
    assert.equal(p.public.sha256, null);
  }
  assert.equal(p.github.events[0].level, "TRANSPORT_ONLY_NOT_RUNTIME_AUTHORITY");
});
test("T17 no paid LLM, tracking or internal callbacks in source endpoints", () => {
  assert.equal(TICKER.pollMs, 900000);
  assert.equal(TICKER.publicFeed, "/status/public-event-registry.json");
  assert.ok(TICKER.githubAPI.startsWith("https://api.github.com/"));
});
