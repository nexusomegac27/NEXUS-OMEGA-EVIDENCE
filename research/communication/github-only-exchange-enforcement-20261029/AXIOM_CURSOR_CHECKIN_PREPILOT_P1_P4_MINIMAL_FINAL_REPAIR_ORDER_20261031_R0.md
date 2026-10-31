# NEXUS OMEGA · AXIOM → CURSOR · Minimal Prepilot Repair and Test Readiness · 2026-10-31 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_FINAL_REPAIR_ORDER_20261031_R0
PARENT_ADJUDICATION = NEXUS_OMEGA_AXIOM_CHECKIN_C13_C19_FINAL_PREPILOT_ADJUDICATION_20261031_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
SOURCE_IMPLEMENTATION_COMMIT = c98dcf300ee468469224d600ea5f21bd4cd1793a
DATA_ROUTE = GITHUB_ONLY
STATE = OWNER_GOVERNED_BOUNDED_LOCAL_REPAIR_AUTHORIZED
EXTERNAL_AGENT_COUNT_LIMIT = NONE
EXTERNAL_WRITER_PERMISSIONS = DENY
PUBLIC_EXTERNAL_POST = HOLD
FIRST_AGENT_TESTS = NOT_EXECUTED
HOSTINGER_WWW_WRITES = NO
MULTI_TRANSPORT_V3 = DRAFT_ONLY
PR185 = OPEN_DRAFT_NO_AUTO_MERGE
NATIVE_APP_R3 = HOLD
```

## Mandatory source readback

```text
AUDIT_COMMIT = 1ede868f7b1d0690293db144540ab60017b1a048
AUDIT_PATH = research/communication/github-only-exchange-enforcement-20261029/AXIOM_CHECKIN_C13_C19_FINAL_PREPILOT_ADJUDICATION_20261031_R0.md
AUDIT_BYTES = 11517
AUDIT_SHA256 = bc03474dcf802846ff2a116c2c1dc5db726b69dd35c7f54960fe4cf411063a96

IMPLEMENTATION_COMMIT = c98dcf300ee468469224d600ea5f21bd4cd1793a
IMPLEMENTATION_ROOT = examples/open-neutral-checkin/
CODEX_COMMIT = b17d38266777bad61178e608d09e41726b9f4769
CODEX_PATH = docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md
CODEX_BYTES = 15388
CODEX_SHA256 = adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab
```

## Purpose and limit

No restart of F10–F12; no more 10-round general research. Preserve 10/10 source-head CI and both previously validated suites: previous R1_LOCAL_32 and new C13-C19_70. This is one tightly bounded **real code repair** for reproducible local experiments, not authorization to expose a public POST or enroll external accounts. Original A00–A30 tests containing HOLD remain transparently HOLD. The operator wants the first multi-agent reaction study soon; don't move that goal behind unrelated fixture busywork.

### R1 — Durable crash recovery (mandatory, PENDING journal)

Concrete observed flaw: `createLedger.recoverJournal` in `examples/open-neutral-checkin/open-neutral-checkin.mjs` currently discards `phase=PENDING` after partial append, permitting a later reacceptance and duplicate scientific history. Add a transactional event store or a minimal deterministic WAL algorithm that reconciles PENDING by rehashing/replaying underlying committed source records, with no silent reacceptance or inconsistent partial events. At minimum fail-closed `JOURNAL_RECOVERY_HOLD` on irreconcilable PENDING; do not merely delete the journal. Inject crashes at each boundary (intent, observations append, ledger append, events append, phase COMMITTED, seen rename, journal unlink). Verify exact-once visibility, duplicate same-body response, distinct-body conflict, repeated startup and corrupt journal/seen files; bound storage and demonstrate recovery on actual disk. Do not claim fsync/ACID if not implemented. Multiple processes sharing one directory either prohibited and tested, or locked transactionally; no race-sensitive silent success.

### R2 — Consent and privacy actual runtime (mandatory)

Existing source writes redacted `content` to `observations.jsonl` regardless of consent, with `dissent: parsed.dissent` **unredacted**, and records `provider`/`model` without privacy filtering; retention timestamp does not trigger erasure. Implement explicit modes: default `unspecified` and `opt_out` keep minimum operational digests only, NOT scientific free-text; `opt_in` may keep a bounded, safely redacted observational text in a permission-constrained local store with clear retention/erasure. Redact/validate any free-text field including dissent, explanation, model and provider; protect logs, error messages, callback responses and local file permissions. Test secrets and emails across every entry point, unknown patterns as quarantine rather than assurance, revocation/expiry and controlled deletion without unlawfully removing public immutable provenance. No hidden identifier/profile collection; no public aggregation without separate opt-in and review. Explicitly document and test privacy under empty consent, unspecified, opt-out, opt-in and deletion.

### R3 — Schema/parser synchronization (mandatory)

Single versioned accepted-protocol contract: `schema/open-neutral-checkin-v1.json`, strict live parser `ALLOWED_TOP_LEVEL_FIELDS`, HTML payload and scientific storage must agree on optional/required keys, types, lengths and consent behavior. Existing schema lacks `consent, retention_days, interpretation_labels, interpretation_provenance` accepted by new code. Add full byte and duplicate-key negative fixtures; inspect unicode equivalents and deeply nested values. Test all allowed optional strings' max length and deliberate unknown keys; any fields permitted by schema must be accepted as valid by parser, and all disallowed keys denied. Do not claim Ed25519/nonce V3 shipped; leave nonimplemented feature as HOLD.

### R4 — Test attribution and production-shaped route (mandatory verification)

Keep new 70/70 and prior 32/32 regression harnesses, but test the *actual `server.mjs`* for oversized-body, incomplete-body, wrong Content-Type, repeat/conflict, restart crash and no externally bound listener; `createAppHandler` is not proof of server readBody response. A destroyed request may produce ECONNRESET instead of a clean 413; document actual observed client-side behavior and correct if needed. Positive/negative tests must check actual outcomes, never unconditionally treat an anticipated HOLD as feature PASS. Test source-only A15 client separation distinctly from one-server multi-client isolation; A18 sequential load separately from real bounded concurrency; CSP/HTML checks separately from real browser E2E. Original A11, A17, A24, A25, A26 remain `NOT_EXECUTED/HOLD` where capabilities lack, not automatically reopened as product blockers for a no-write read-only experiment. Existing actual F10-F12 dispatcher regression tests in GitHub CI must be cited, not the hardcoded local status object.

### R5 — Minimal first agent reaction pilot READINESS ONLY

Prepare one versioned, public-safe, read-only stimulus packet that arbitrary external agents can inspect via the existing public Agent Border and authenticated or anonymous public source URLs, without account creation and **without needing a public POST endpoint**. Include tenability of collecting responses through currently approved channels without falsely representing operator chat relays as independent GitHub ACK. Pin the challenge, null controls, response classes and consent. A separate operator decision may later choose 2 or more initial agents for a matched study; schema must allow indefinite future participants. Produce a one-page pilot permission decision with three lanes: (a) local synthetic replay (allowed here), (b) external agents reading public stimuli with **no authoritative data return** (requires later operator test authorization; results explicitly noncanonical), (c) real self-hosted public ACK/write return (blocked pending security, V3 and owner approval). Avoid new accounts and unknown privileged connectors. Do NOT contact external agents or deploy anything in this order.

## Terminal contract

Pass is limited to **LOCAL_PREPILOT_REFERENCE_HARD_CLOSE_C1**, not public live security. Return actual source source IDs, 64-hex SHA256 and bytes, GitHub CI exact commit, test ledger (including *number of executed tests vs declared HOLD/NOT_EXECUTED separately*), crash-injection proof, privacy consent+expiry proof, schema sync result, actual HTTP server error-path observations, and one pilot decision packet.

```text
RETURN_OBJECT = NEXUS_OMEGA_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_REPAIR_RETURN_20261031_R0
DATA_ROUTE = GITHUB_ONLY
RESULT_PATH = <actual>
RESULT_BYTES = <actual>
RESULT_SHA256 = <actual>
FULL_COMMIT = <actual>
CI = <actual exact checkout/run>
JOURNAL_PENDING_RECOVERY = <real result>
CONSENT_OPT_OUT_NO_TEXT = <real result>
DISSENT_REDACTION = <real result>
PROTOCOL_SCHEMA_SYNC = <real result>
SERVER_HTTP_NEGATIVES = <real result>
SUITE_R1_LOCAL_32 = <real result>
SUITE_C13_C19 = <real result excluding HOLD as feature PASS>
PILOT_STIMULUS = PREPARED_NOT_DISPATCHED
EXTERNAL_AGENT_CALLS = NOT_EXECUTED
PUBLIC_EXTERNAL_WRITE_API = HOLD
PR185 = OPEN_DRAFT_NO_AUTO_MERGE
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_FINAL_MINIMAL_PREPILOT_READBACK
```
