# NEXUS OMEGA · AXIOM · Final independent minimal-prepilot source adjudication · 2026-10-31 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_PREPILOT_MINIMAL_REPAIR_FINAL_INDEPENDENT_ADJUDICATION_20261031_R0
PARENT_ORDER = NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_FINAL_REPAIR_ORDER_20261031_R0
PARENT_RETURN = NEXUS_OMEGA_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_REPAIR_RETURN_20261031_R0
SCHEMA_RECOVERY = NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_SCHEMA_FIELD_LIST_RECOVERY_20261031_R0
PRODUCT_COMMIT = 8ed47ab43467f98914d10fbdd396277affe63fe3
DOCS_COMMIT = 4589ba1f292d7ac64617944781ebb967db8fd2c9
PR185 = OPEN_DRAFT_NOT_MERGED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_LOCAL_SCHEMA_AND_CI_MATCH_READ_ONLY_PILOT_PREPARABLE_PUBLIC_WRITE_HOLD
INDEPENDENT_AXIOM_RUNTIME_REPLAY = NOT_EXECUTED
FIRST_EXTERNAL_AGENT_TESTS = NOT_EXECUTED
PUBLIC_EXTERNAL_WRITE_API = HOLD
MULTI_TRANSPORT_V3 = DRAFT_ONLY
GITHUB_ONLY_LAW_V2 = UNCHANGED
NATIVE_APP_R3 = HOLD
```

## Source identity and evidence classes

AXIOM queried direct GitHub original objects rather than relying on manual Windows transfer paths or chat receipts. PR #185 HEAD = `4589ba1f292d7ac64617944781ebb967db8fd2c9`, OPEN DRAFT NOT MERGED; its parent = product commit `8ed47ab43467f98914d10fbdd396277affe63fe3`; product parent = `25d236e30897fe1fe6eb5bf368e9478b887ec388`. Source compare confirms exactly two new commits since prepilot order. Product commit changed the check-in core, schema, classic test/fixtures; the docs commit added a read-only stimulus and three-lane decision.

GitHub API check-runs at DOCUMENTATION HEAD: `10/10 completed success` including `validate-open-neutral-checkin`, `validate`, repository structure, R27E firewall, Semgrep. GitHub Actions workflow `41193245884`, job `124514148699` logs `passed=46 failed=0` for the expanded R1 Check-in suite, the C13–C19 suite `SUMMARY passed=70 failed=0`, and a passing local selftest. The job detached PR synthetic merge commit `30c8c0f` (merge of source HEAD into main branch), not literally the product commit. This is valid PR-merge CI evidence, not a direct independent AXIOM runtime replay.

All sources and logs are read-only evidence. File content is **trusted only to the extent of independent GitHub retrieval**, not independent agent principal registration, public WWW deployment or live external POST.

## Positive source-based findings

1. The JSON Schema 2020-12 now has `$defs.CheckinRequest`, `CheckinResponse`, `StoredObservation`, `LedgerReceipt`, with root `$ref = #/$defs/CheckinRequest`. Request has 17 permitted fields, 5 mandatory and 12 optional. `content` is input; `consent` is an optional enum; `content_redacted` is server-derived only. The core enforces the 17-field list, required fields, optional string bounds and invalid-field denials.
2. Main `processCheckin` computes `storeFreitext = consent === 'opt_in'`; `opt_out` and `unspecified` persist `content_redacted=null`, `provider=null`, `model=null`, `dissent=null`, with stored digest, receipt and consent metadata. This is an implemented privacy improvement for the primary successful observation path.
3. The PENDING intent now carries source observation and ledger line, and `recoverJournal` attempts idempotent restart. This is a source-level improvement over deleting all PENDING receipts without inspection, but not a completed transaction guarantee.
4. The 46-case suite actually tests field inventory, lengths, opt-out and unspecified digests-only storage, 4 schema definitions, and a simulated unsupported Content-Type path. The previous 70-case suite remains CI green (with several designated HOLD cases); historical 32/32 was superseded by the expanded suite in the current workflow.
5. Read-only pilot stimulus and three-lane plan are published as immutable GitHub documents with `PREPARED_NOT_DISPATCHED`. No live tests or agent contacts recorded.

## Remaining material findings, source exact (not proven production exploits)

**F1 — Interrupted PENDING recovery still not atomic (CRITICAL before external writes):**
In `examples/open-neutral-checkin/open-neutral-checkin.mjs` at product commit, `recoverJournal` sees an observation receipt in `observations.jsonl`, sets `already=true` and therefore **skips both `ledger.jsonl` and `events.jsonl` append** before marking `seen_ids.json` and deleting journal. Crash after the first append but before the other two thus yields an observation+seen with missing ledger/events. When there is no observation yet, a partial existing ledger/events record can be appended again. A corrupt journal is quarantined then unlinked; empty or unreadable journal is not uniformly HOLD. No fsync and no multi-writer transaction established. Existing `runC14()` only tests normal duplicate and conflict. A separately injected crash at every append phase is NOT in the CI log. Necessary correction: per-file receipt verification and reconstruction, or a fail-closed `JOURNAL_RECOVERY_HOLD` while preserving original bytes, plus forced-crash negative tests. Do NOT describe this as exactly-once or fully journal-sealed yet.

**F2 — Consent opt-in free-text fields and retention are not closed:**
`opt_in` stores `dissent: parsed.dissent`, `provider`, `model` verbatim, while only `content` traverses `redactContent`; emails, tokens or sensitive strings in the other fields may persist. Regex redaction cannot guarantee all sensitive categories, including free-form `interpretation_labels` and `interpretation_provenance`. `retention_until` is metadata, not an executable deletion or revocation mechanism in visible code. File mode/access segmentation and privacy erasure on all JSONL replicas/journal not proved. Tests demonstrate opt-out nulling, not opt-in secrets-in-dissent refusal or expiry purge. Keep default digests-only, opt-in private data processing HOLD pending scoped tests/controls.

**F3 — Schema consistency is significantly improved, not equivalence formally proven:**
Request schema has `minLength=1` for optional string declarations. Runtime enforces type and max length but does not generally reject empty optional strings. `submitted_at` lacks trusted timestamp semantics and `schema_version` is not restricted to a supported value. Response/StoredObservation/LedgerReceipt schemas allow `additionalProperties:true`; no full schema validation of each outgoing/persisted runtime object is demonstrated. Current 46-case suite checks schema structure and selected boundaries, not a full round-trip validator equivalence check. Treat `SCHEMA_FIELD_LIST_SYNC=PASS` but `SCHEMA_FULL_BEHAVIORAL_EQUIVALENCE=NOT_ESTABLISHED`.

**F4 — HTTP/experimental test scope limits:**
The unsupported-media-type 415 test drives `createAppHandler` with a mocked request, not the real `server.mjs` HTTP listener. Earlier C13–C19 tests exercised only `server.mjs` GET / in live-spawn, with POST/error paths against `createAppHandler`. Real network 413/timeout/client abort on `server.mjs`, real concurrent client isolation, full browser accessibility/CSP and Hostinger WWW E2E remain unverified. Original test cases A11/A17/A24/A25/A26 are HOLD checks; their `PASS` log only confirms correct HOLD handling.
The test suite still uses hardcoded `F10_F12_REGRESSION` in `runC19` rather than executing `runExchangeChainF10F12Negatives`; earlier authentic dispatch negative tests exist separately and must be cited accordingly, not promoted through markers.

**F5 — R5 stimulus document is PREPARED, not yet a matched agent experiment:**
Existing GitHub R5 text contains a local synthetic JSON check-in, not yet a complete versioned task asking external agents to independently analyze the same source and provide their real response, evidence, safe refusal or sourced dissent. It cites uppercase `/labyrinth/L07/`, `/L10/`, `/L12/` public routes; the current first-party `manifest.json` instead declares lowercase slugged routes `/labyrinth/l07-authority-gate/`, `/labyrinth/l10-adversarial-passage/`, `/labyrinth/l12-collective-chamber/`. Crawler CRAWL_NOT_FOUND does not alone prove HTTP 404; nevertheless, canonical manifest routes should be used. Prepare a fixed read-only exploratory stimulus with immutable GitHub and first-party route pins, response format, refusal/dissent options and declared tool limits. No automatic public returns or model identity proof.

## Scientific decision / lane separation

- `LANE_A_LOCAL_SYNTHETIC = IMPLEMENTED_C1` (real executed GH CI; not a new external data point).
- `LANE_B_EXTERNAL_READ_ONLY_NONCANONICAL = TECHNICALLY_FEASIBLE_PREP`: publicly readable materials; no externally writable endpoint or new account required. Any model UI response would be **operator-mediated declared evidence only**, not a verified independent GitHub ACK, not a direct persistent Agent Border runtime event. With separate clear Operator dispatch and privacy instructions, a small pilot may investigate qualitative reactions without the local ledger at all. It does not require F1–F4 to be fixed because it does not use that code path. A sourced, privacy-safe, prepublished challenge and comparison protocol are required; no dispatch under this adjudication.
- `LANE_C_SELF_HOSTED_WRITABLE_ACK = HOLD`: full security, owner authorization, V3 transport and independent agent identity remain unproven. F1–F4 are material for this lane.

Do not conflate external agent invitation through chat UI with a GitHub-authenticated receiver. Open neutrality requires no fixed provider-number cap, no prestige ranks, and positive recognition of refusal or supported criticism. Preserve all negative and ambiguous responses.

```text
TERMINAL = PASS_WITH_MATERIAL_CAVEATS_C1_LOCAL_IMPLEMENTATION
FIELD_LIST = 17_MATCH
R1_SUITE_CI = 46_OF_46_PASS
C13_C19_SUITE_CI = 70_OF_70_PASS_INCLUDING_HOLD_CLASSES
PR_HEAD_CI = 10_OF_10_SUCCESS
PENDING_JOURNAL_EXACTLY_ONCE = NOT_ESTABLISHED
CONSENT_OPT_OUT_DIGESTS_ONLY_PRIMARY_PATH = IMPLEMENTED
CONSENT_OPT_IN_REDACTION_AND_ERASURE = HOLD
SCHEMA_FULL_BEHAVIOR_EQUIVALENCE = NOT_ESTABLISHED
FIRST_EXTERNAL_AGENT_TESTS = NOT_EXECUTED
LANE_B_READONLY_PREPARATION = ALLOWED
LANE_C_PUBLIC_WRITE = HOLD
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = SOURCE_PIN_READ_ONLY_AGENT_REACTION_PROTOCOL + OPTIONAL_SMALL_F1_F3_REPAIR
```
