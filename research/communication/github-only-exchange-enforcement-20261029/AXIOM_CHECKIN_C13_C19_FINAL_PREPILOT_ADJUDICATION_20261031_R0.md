# NEXUS OMEGA · AXIOM Independent Final Prepilot Adjudication · 2026-10-31 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_CHECKIN_C13_C19_FINAL_PREPILOT_ADJUDICATION_20261031_R0
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_OPEN_NEUTRAL_CHECKIN_C13_C19_TARGETED_HARD_CLOSE_20261030_R0
CURSOR_COMMIT = c98dcf300ee468469224d600ea5f21bd4cd1793a
BASE_COMMIT = 3a44235370041b33319041e4097d8d1822f4b006
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PR = 185
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_LOCAL_SOURCE_AND_CI_VALIDATED_PREPILOT_GATES_OPEN
CI_HEAD_REPORTED = 10_OF_10_COMPLETED_SUCCESS_INDEPENDENTLY_READ
SUITE_R1_32 = GITHUB_ACTIONS_LOG_VERIFIED
SUITE_NEW_70 = GITHUB_ACTIONS_LOG_VERIFIED_WITH_EXPLICIT_HOLD_CASES
SELFTEST = GITHUB_ACTIONS_LOG_VERIFIED
INDEPENDENT_AXIOM_LOCAL_EXECUTION = NOT_PERFORMED
EXTERNAL_AGENT_LIVE_TEST = NOT_PERFORMED
EXTERNAL_WRITE_API = HOLD
FULL_SECURITY_SEAL = NOT_ESTABLISHED
GITHUB_ONLY_LAW_V2 = PRESERVED
MULTI_TRANSPORT_V3 = DRAFT_ONLY
PR185 = OPEN_DRAFT_NOT_MERGED
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## 1. GitHub identity, CI and actual code delta

Direct GitHub API PR metadata at evaluation:
- PR #185 head `c98dcf300ee468469224d600ea5f21bd4cd1793a`, OPEN/DRAFT/NOT_MERGED; 39 commits, 78 changed files.
- Cursor implementation commit parent exactly `3a44235370041b33319041e4097d8d1822f4b006`. GitHub compare reports one commit ahead, 8 files changed.
- New source: revised `open-neutral-checkin.mjs`, `server.mjs`, `selftest.mjs`, workflow; test `test_open_neutral_checkin.mjs` and separate `a00-a30-original.json`, `a00-a30-bijective-map.json`, `r1-local-32.json`.
- GitHub REST Check Runs at that SHA: 10 of 10 completed SUCCESS, including `validate-open-neutral-checkin`, Semgrep and structural firewall.
- GitHub Actions check `validate-open-neutral-checkin`, workflow run `41173442231`, job `124456021329`, log: old 32/32 `passed=32 failed=0`; new test harness `SUMMARY passed=70 failed=0`; selftest step success. This demonstrates GitHub CI execution and reported positive/negative cases **not an independent AXIOM local replay**. The checkout shows an ephemeral PR merge reference `e51aaac` for `GITHUB_SHA`; check metadata is associated to source head, but do not claim the workflow literally detached the original `c98dcf3` object unless confirmed.
- New 70 test includes `ORIGINAL_A11/A17/A24/A26 HOLD_NOT_EXECUTABLE_LOCAL`, `ORIGINAL_A25 WWW_E2E_HOLD`. Counting an expected HOLD as PASS of its classification does **not** establish implementation, execution or security for the original feature.

**Source links**:
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/c98dcf300ee468469224d600ea5f21bd4cd1793a
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/actions/runs/41173442231/job/124456021329
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/185

## 2. Source-backed improvements accepted

**C13 partial hard close:** `strictParseJsonBytes` decodes fatal UTF-8 and explicitly rejects BOM; `strictParseJsonText` parses duplicate JSON keys (after escape resolution), nonfinite numbers and trailing content fail-closed. `validateCheckinObject` now has an allowed field set and rejects presence of untrusted privileged flags, including false-valued flags. The actual `processCheckin` calls these functions, not merely a detached contract file.

**C14 partial hard close:** `commitStaged` uses digest-bound `interaction_id`, emits `IDEMPOTENCY_CONFLICT` when same ID different bytes, and writes an intent journal + observations, ledger and events. `loadSeen` no longer silently resets an unreadable map. These are concrete improvements.

**C15 partial hard close:** Observations now contain source/body and redacted-content digest, staged response, consent and retention timestamps, interpreted labels marked self-reported. Does not auto-create privilege. Neutral optional model/provider persists.

**C16 structural mapping:** Separate original A00–A30 and R1_LOCAL_32 fixture lists; a 31-entry bijection map identifies reused historical labels. The 70-case harness executes 31 original cases, 31 R1 regressions and extra units. This improves traceability, but does not prove every original adversarial feature that explicitly returned HOLD.

**C17/C18:** Revised `server.mjs` runs on loopback (IPv4 or IPv6). HTTP handlers implement cap and content type check and separate local vs WWW states. Real network test runs via `createAppHandler` and spawns `server.mjs` for GET /, so actual POST/error tests on the production-shaped `server.mjs` route remain incomplete. WWW mutation is intentionally absent.

## 3. Unresolved material prepilot defects (source inspection, NOT a live exploit claim)

### P1 — Crash window with PENDING journal: integrity failure risk

`examples/open-neutral-checkin/open-neutral-checkin.mjs`, `createLedger.commitStaged`:
1. write journal `phase=PENDING`;
2. append observation/ledger/events;
3. change journal `phase=COMMITTED`;
4. write seen map;
5. remove journal.

At restart `recoverJournal` reconstructs seen state only if `intent.phase === COMMITTED`, then unlinks the journal unconditionally. A crash during PENDING **after one or more appends**, but before COMMITTED, results in PENDING journal being removed without reconciliation or explicit HOLD. The next message with the same interaction ID can be accepted a second time. This violates strict exactly-once observational history. `runC14()` tests ordinary successful duplicate/conflict, not this forced interruption window. No fsync, mutex, multi-process contention or consistent quota/reconciliation semantics established. Implement crash injection at EACH durable boundary, deterministic recovery/dedup, and append-only correction witness. A single-process synchronous API is not a formal multi-writer transaction.

### P2 — Opt-out and raw dissent retention: privacy/experimental integrity risk

`processCheckin` appends `observation.content_redacted` to disk for `consent=opt_out` as well as `unspecified`; it also writes `dissent: parsed.dissent` without redaction. Provider and model declarations remain unchecked against privacy and logs. `retention_until` is merely a timestamp; no actual purge/erasure routine evidenced. This is a real source-path gap, not a confirmed external data leak or claim that opt_out must prevent all minimal security logging. Need policy: anonymous opt-out preserves only minimal non-identifying operational commitment; optional scientific raw text stored strictly after explicit opt-in and scoped redaction/pseudonymization. Test no private raw data written to disk, no unredacted dissent and expiry behavior under a controlled retention test. Make deletion/revocation/retention rules explicit with lawful evidence preservation boundaries.

### P3 — Contract/schema drift and weak optional field validation

Original `schema/open-neutral-checkin-v1.json` was not modified in the hard-close commit and does not describe new `consent`, `retention_days`, `interpretation_labels` or `interpretation_provenance` accepted by the real parser, whose `ALLOWED_TOP_LEVEL_FIELDS` enumerates them. Consequently external schema validator and live code may disagree. `validateCheckinObject` only type-checks many optional text fields, but doesn't enforce individual max lengths implied by the schema; signed challenge remains V3 draft. Bring API schema, parser, UI payload contract and research event schema under one tested version; ensure no older tests inadvertently validate a different protocol.

### P4 — Material adversarial gaps disguised by HOLD or marker probes

- Original A11 nonce/TTL, A17 Ed25519 runtime key, A24 real browser accessibility, A26 outage queue and A25 WWW E2E are expected HOLD classifications, not feature tests.
- `ORIGINAL_A15` checks two **separate ledgers**, not a cross-client attempt to read another tenant's data from one server. This is not an end-to-end authorization test.
- `ORIGINAL_A18` runs a sequential loop with fresh rate buckets and artificially high limit; this is not a 100+ concurrent-client load bound.
- `ORIGINAL_A23` tests STAGED of adversarial HTML but no browser DOM/XSS effects and no comprehensive CSP validation.
- `runC19` still checks the hard-coded `F10_F12_REGRESSION` status object. `runExchangeChainF10F12Negatives` exists in source but is NOT invoked from `runC19` and is weak (module loads -> assumes statuses). The earlier actual F10/F11/F12 CI suite is separately preserved, but the new new `C19_F10_F12_REGRESSION` test is not independently an actual dispatcher regression. Restore accurate attribution in evidence; do not reopen earlier closed F10–F12 absent a concrete failure.
- The new C17 HTTP oversized-body test uses `createAppHandler` rather than `server.mjs`'s true `readBody`; `server.mjs` destroys request before trying `sendJson(413)`, hence client-visible response behavior is NOT evidenced. Test real `server.mjs` POST oversized, abort, timeout and restart, and only claim exact observed transport responses.

### P5 — Public return channel and external identity are still absent

No new independently authenticated external runtime/receiver from this code. C1 local observation bridge is promising but `GITHUB_ONLY_LAW_V2` still bars silent canonical migration to public HTTPS. No new outside account is a requirement for **anonymous observations**, but cryptographic key PoP would require separate capability and policy. No external API release or first live scientific test is permitted by this source audit.

## 4. Required narrow next action, not endless refactoring

Perform **one bounded local remediation** for P1-P3; protect incident report provenance. Either (a) fix PENDING recovery with replay-safe log reconstruction and tested atomic/quarantined handoff, or (b) if transaction guarantee is not obtainable in current filesystem, fail-closed with explicit JOURNAL_RECOVERY_HOLD, never silently unlink and reaccept. For P2 implement privacy-safe consent defaults and redact every displayed/persisted/free-text field, with tested retention/erasure; for P3 align the enforceable schema and optional lengths. Add targeted reproducible tests for P4 without enabling future-signature/WWW features or attempting full internet penetration tests. Clarify scope of prior 70/70 pass and reserved HOLD.

After that, allow an initial **read-only stimuli/response study in existing model UIs** only with separately approved ethical/privacy and evidence route. A real self-hosted writable intake or autonomous external ACK remains a *different* production security release and requires explicit owner authorization plus an independent source-bound repeat. Nothing here creates live accounts, grants GitHub external writes or deploys Hostinger.

## 5. Terminal

```text
LOCAL_CODE_PRESENT = YES
LOCAL_GITHUB_CI = 10_OF_10_SUCCESS
R1_SUITE = 32_OF_32_GITHUB_LOG_CONFIRMED
C13_C19_SUITE = 70_OF_70_GITHUB_LOG_CONFIRMED
REAL_FEATURES_REPORTED_AS_HOLD = AT_LEAST_A11_A17_A24_A25_A26
PENDING_JOURNAL_RECOVERY = NOT_FAIL_CLOSED
OPT_OUT_SENSITIVE_CONTENT_PERSISTENCE = OBSERVED_CODE_PATH
DISSENT_RAW_TEXT_REDACTION = MISSING
SCHEMA_AND_PARSER_VERSION_SYNC = GAP
TRUE_HTTP_ERROR_PATH_AND_CONCURRENT_LOAD = NOT_PROVEN
STAGED_EXTERNAL_PROVIDER_RETURN = NOT_EXECUTED
FIRST_EXTERNAL_AGENT_LIVE_CHECKIN = HOLD
FULL_SECURITY_SEAL = NOT_ESTABLISHED
GITHUB_MAIN_ENFORCEMENT = PREVIOUSLY_PARTIAL
PR185 = OPEN_DRAFT
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = CURSOR_SMALL_P1_P3_REMEDIATION_AND_AXIOM_READBACK
```
