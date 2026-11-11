# NEXUS OMEGA · AXIOM · Independent implementation adjudication · 2026-10-30 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_OPEN_NEUTRAL_CHECKIN_IMPLEMENTATION_INDEPENDENT_ADJUDICATION_20261030_R0
PARENT = NEXUS_OMEGA_CURSOR_AGENT_BORDER_OPEN_NEUTRAL_CHECKIN_CONSOLIDATED_IMPLEMENTATION_RETURN_20261030_R1
CURSOR_COMMIT = beffe5f6639abdab31a4b04fc39337b6f7469ce7
PARENT_BASE = 4f16fbcfe4b410f22e0ba221e4fc3d47979173ad
PR = 185 OPEN_DRAFT
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_LOCAL_BASE_IMPLEMENTED_SECURITY_AND_RESEARCH_GATES_OPEN
LOCAL_BASE_IMPLEMENTATION = SOURCE_PRESENT_GITHUB_CI_EXECUTED
IMPLEMENTATION_READINESS_TERMINAL_PASS = NO
FIRST_EXTERNAL_AGENT_TEST_READINESS = HOLD
PUBLIC_EXTERNAL_WRITE_API = HOLD
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## 1. Exact independently retrieved primary evidence

Connected GitHub original at `beffe5f6639abdab31a4b04fc39337b6f7469ce7` and direct API check-runs readback:

- PR185 open draft not merged, HEAD == Cursor commit, 35 commits and 71 changed files at source readback.
- Commit parent exactly `4f16fbcfe4b410f22e0ba221e4fc3d47979173ad`; one new implementation commit, 15 changed/added files, no historic source mutation proven here.
- GitHub Check Runs `10/10 completed success` at **exact Cursor HEAD**, includes `validate-open-neutral-checkin` and Semgrep. New dedicated workflow run `41134878370`, job `124334764711`, source-exact stdout contains `SUITE A00-A30_OPEN_NEUTRAL_CHECKIN cases=31`, `PASS A00` through `PASS A30`, `PASS X_DUAL_ARITY`, and `{"passed":32,"failed":0}`. Selftest step completed success; local HTTP status `202 STAGED_UNTRUSTED`, `200 DUPLICATE` evidenced by selftest job logs, not independent AXIOM local re-execution.
- Independently rehashed direct GitHub UTF-8 source content: Result 7869 B SHA256 `4250d2c565be5fc4c17c7b1cebbb7d0e522ba64d52119f3b4787b0540e8ec88d`; core 12362 B SHA256 `79be9bb4a4f19327f4f850a4f548baeb8ae1f7ff238594f6b252600570e362f5`; server 3520 B SHA256 `401febed7489b541e2631a7f6500bc2aafb769954b1e50d90ea60c38c939f5a2`; tests 6517 B SHA256 `4e6fca9d63d62c7819377ae2b2891f44030c6eadf512e99588b7a977b744b320`; selftest 7900 B SHA256 `f40186f0b03d162e088b205341a221cd646428caab62ede63a207aafe508ebf2`; schema 1571 B SHA256 `460d109b8388d09758890a21884da77ea300085e96d9e5e3de2e417a89fbe14c`; source census G1 2448 B SHA256 `7477957ec50f9846e113ab9722badb1000dff1409e7e362bb8307a976ce4ea10`; transport G4 990 B SHA256 `84abd4af6e7c48e9de3e43f8745fb580956c33bab527211c9aeef08d986b1cea`; study G5 2017 B SHA256 `de8e36141ffc0790c47b8faff99f7cff7eead912da7f4b3eb9278b716786af44`. All nine match Cursor's claimed byte lengths and digests.
- Github job logs establish scope of executed checks, not every historical requirement independently tested.

## 2. Positive acceptance (bounded)

- Actual Node source exists: `examples/open-neutral-checkin/open-neutral-checkin.mjs`, `server.mjs`, HTML, selftest, fixtures, tests and CI workflow.
- Loopback-only listener checks `NEXUS_CHECKIN_HOST` against `127.0.0.1` or `localhost`, and defaults to `127.0.0.1`. No public service deployed.
- Main processing returns `STAGED_UNTRUSTED`, `DUPLICATE` or `DENIED`; default C1 and observation-only labeling. No actual privileged tool dispatch in this module.
- Optional provider/model declarations and no provider hard-coded allowlist support neutral intake design.
- Source code includes simple redaction, file ledger, global basic rate cap, size cap, UUID receipt, local UI via safe `textContent`. No external registry/credential issuance or first real agent call evidenced.
- Existing earlier F10/F11/F12 actual dispatcher lane was independently validated at earlier pinned commits. This new local suite's policy-surface stubs are *not* themselves real end-to-end regression proofs for the earlier dispatcher.

## 3. Material findings from independent static source review

**C13 / STRICT_PARSE_AND_SCHEMA_GAP — OBSERVED_CODE_GAP; local acceptance repair mandatory.** `processCheckin` uses plain `JSON.parse(buf.toString('utf8'))`; JSON.parse keeps the last of duplicate keys, and the implementation does not reject unknown top-level fields or validate the shipped `schema/open-neutral-checkin-v1.json` in its processing path. Therefore the separate schema's `additionalProperties:false` is NOT enforced. It also does not validate optional provider/model type/length or prohibit nested objects, and the `FORBIDDEN_ACTION_FLAGS` only deny when truthy. Need strict duplicate-key detection, maximum depth, explicit allowlist and exact protocol contract, Unicode byte safety, negative tests against the true HTTP path. Do not claim successful exploit or production compromise from static code.

**C14 / LEDGER_IDEMPOTENCY_AND_CRASH_GAP — OBSERVED_CODE_GAP; mandatory.** `createLedger` uses separate `seen_ids.json` read/write and `ledger.jsonl` append; `processCheckin` calls `ledger.mark(interaction_id, receiptId)` BEFORE `ledger.append('STAGED_UNTRUSTED', record)`. Crash or I/O error after mark and before append loses the event while future checkins are labelled duplicate; same interaction ID with a different payload is currently labelled duplicate rather than `IDEMPOTENCY_CONFLICT`. No demonstrated concurrency atomicity, bounded retention or corruption handling (`loadSeen` silently substitutes `{}` on malformed file). Need atomic transactional or crash-safe recovery, digest binding, replay/conflict distinction and bounded per-run/disk quotas. Tests on actual disk and server.

**C15 / SCIENTIFIC_RESPONSE_AND_CONSENT_GAP — OBSERVED_CODE_GAP; mandatory before empirical tests.** The on-disk staged ledger appends only `receipt_id, interaction_id, body_sha256, redaction_count` — no source-bound safely retained agent response or structured behavior categories. The untrusted response content exists in the POST reply but not in an independently inspectable privacy-reviewed event for blind classification. A hash alone cannot reconstruct the response or explain a sourced dissent/refusal. No consent/publication/retention control in processing path; regular-expression redaction only handles some strings inside `content`, not optional provider/model or all sensitive classes. Need bounded controlled access to redacted, consent-scoped response, original-input commitment, event preservation, deletion/retention policy and explicit redaction failure quarantine. Avoid collecting personal data or publishing untrusted raw contents; no silent profiling. Never classify ordinary dissent as malicious merely for quoting `CLAIM_PROMOTION=YES` or `FINAL_TRUTH` without contextual criterion.

**C16 / A00_A30_SCOPE_SUBSTITUTION — OBSERVED_TEST_COVERAGE_GAP; mandatory.** Current suite names A00–A30 but exercises a *different* 31-item set than the 2026-10-30 AXIOM blueprint source `docs/architecture/NEXUS_AGENT_BORDER_OPEN_NEUTRAL_CHECKIN_V1_BLUEPRINT_20261030.md` at `2ba92e051beb0442f4ad8edd9f6ab7f641957b38`. Example: blueprint requires duplicate JSON key/nonfinite/deep-nesting, SSRF callbacks, 100+ simulated clients, 1000 duplicates, cross-client isolation, hostile HTML XSS, signature/key lifecycle and real browser viewport tests; current fixture list checks empty body, wrong protocol, email/GitHub token redaction and surface-only F10-F12. Those 32 cases genuinely passed, but `G6=PASS_ALL_ORIGINAL_A00_A30` is *not established*. Restore blueprint IDs with test traceability and add missing negatives; respect V3 draft / real-signature NOT_IMPLEMENTED as scoped holds rather than fabricated passes.

**C17 / HTTP_FAILURE_AND_RESOURCE_RUNTIME — REQUIRES_DYNAMIC_CONFIRMATION.** On `readBody` size overrun server calls `req.destroy()` then attempts `send(res,413,...)`; client may see a socket reset rather than 413, notwithstanding the direct-helper `BODY_TOO_LARGE` fixture. Need actual HTTP oversized-body negative test; documented policy for body timeout/slow clients, Content-Type, global vs per-client rate semantics, disk quota, restart/replay/crash. Do not label observed socket failure without actual isolated test.

**C18 / WWW_SOURCE_AND_BROWSER_GAP — NOT_ESTABLISHED.** G1 census includes narrative "prior HTTP200" and an unbound local PFV source location, but no comprehensive raw Hostinger HTML/JS/CSS/HTTP/headers/route SHA256, no actual independent live browser E2E and no rollback of a deployed production site. Selftest only searches UI text/media-query marker. Static status not equivalent to AEGIS/SFT runtime integration. Live external checkin remains HOLD; initial read-only census may continue without production mutation.

**C19 / F10_F12_MARKER_NOT_DISPATCH — TEST_PROVENANCE_GAP.** `f10f12PolicySurface()` emits hardcoded F10/F11/F12 CLOSED labels and test cases A26–A28 only assert those labels; this is NOT a regression of existing `scripts/nexus_github_exchange_chain.py` dispatcher. Reuse existing actual Python test suite/CI for F11 and F12, preserve source/policy separation. No need to reopen earlier source-fixed defects absent a new failure.

**C20 / OPTIONAL_CRYPTOGRAPHIC_RUNTIME = DESIGN_NOT_SHIPPED.** V3 draft has `signature_b64` etc placeholders, no operational Ed25519 or provider runtime attestation. This is acceptable for isolated anonymous local observation if honestly labelled, but do not claim verifiable external receiver identity or signed ACK from this build.

## 4. Decision

```text
GITHUB_SOURCE_INTEGRITY = PASS_9_OF_9_EXACT_FILES
CI = SUCCESS_10_OF_10_AT_BEFFE5F
LOCAL_REFERENCE_CODE = PRESENT_AND_CHECKS_EXECUTED
FULL_SECURITY_CLOSURE = NOT_ESTABLISHED
PREREGISTERED_A00_A30_COMPLETE = NO
OWNER_BROWSER_WWW_E2E = NOT_ESTABLISHED
EXTERNAL_PILOT_READINESS = HOLD
C13_C14_C15_C16 = TARGETED_MATERIAL_REMEDIATION_REQUIRED
C17_C18_C19 = EVIDENCE_GAP_OR_SCOPED_RETEST
C20 = V3_DESIGN_ONLY_EXPECTED
LIVE_EXTERNAL_API = HOLD
PR185 = OPEN_DRAFT
NATIVE_APP_R3 = HOLD
NEXT = CURSOR_TARGETED_SOURCE_AND_COVERAGE_HARD_CLOSE_THEN_AXIOM_READBACK
```

No claim that the code has been independently executed by AXIOM itself. Independent source review + GitHub Actions job logs only; static vulnerability paths are not proof of live exploit. All new tests must run only against local/staging owner-controlled code. The implementation foundation is accepted as C1 source-backed, but **the user-requested first external agent scientific check-in must not be labelled ready until C13-C16 close and the lawful scoped return/observational channel is defined**.
