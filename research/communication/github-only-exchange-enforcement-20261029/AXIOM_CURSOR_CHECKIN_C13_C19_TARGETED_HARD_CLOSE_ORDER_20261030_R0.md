# NEXUS OMEGA · AXIOM → CURSOR · Targeted C13–C19 hard close · 2026-10-30 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_OPEN_NEUTRAL_CHECKIN_C13_C19_TARGETED_HARD_CLOSE_20261030_R0
PARENT = NEXUS_OMEGA_AXIOM_OPEN_NEUTRAL_CHECKIN_IMPLEMENTATION_INDEPENDENT_ADJUDICATION_20261030_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PR = 185 OPEN_DRAFT
CURSOR_SOURCE_COMMIT = beffe5f6639abdab31a4b04fc39337b6f7469ce7
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
IMPLEMENTATION = ACCEPTED_C1_LOCAL_FOUNDATION_WITH_MATERIAL_HOLDS
RUN_SCOPE = EXISTING_OWNER_BRANCH_LOCAL_OR_ISOLATED_STAGING_ONLY
NEW_EXTERNAL_AGENT_TESTS = NO
EXTERNAL_PUBLIC_WRITE = NO
GITHUB_ONLY_LAW_V2 = PRESERVED
MULTI_TRANSPORT_V3 = DRAFT_ONLY
AUTO_MERGE = NO
NATIVE_APP_R3 = HOLD
```

## Mandatory readback: actual authoritative bytes

```text
AXIOM_AUDIT_COMMIT = 9ed8be23ee990b324229fb2195415d9097ae2245
AXIOM_AUDIT_PATH = research/communication/github-only-exchange-enforcement-20261029/AXIOM_OPEN_NEUTRAL_CHECKIN_IMPLEMENTATION_INDEPENDENT_ADJUDICATION_20261030_R0.md
AXIOM_AUDIT_BYTES = 10433
AXIOM_AUDIT_SHA256 = 0bd09ca666f1731e960573422805e4605806378d42caf192ac5d6067ea8887ae

CURSOR_RESULT_COMMIT = beffe5f6639abdab31a4b04fc39337b6f7469ce7
CURSOR_RESULT_PATH = research/communication/github-only-exchange-enforcement-20261029/RESULT_GITHUB_OPEN_NEUTRAL_CHECKIN_CONSOLIDATED_IMPLEMENTATION_20261030_R1.md
CURSOR_RESULT_BYTES = 7869
CURSOR_RESULT_SHA256 = 4250d2c565be5fc4c17c7b1cebbb7d0e522ba64d52119f3b4787b0540e8ec88d

SOURCE_BLUEPRINT_COMMIT = 2ba92e051beb0442f4ad8edd9f6ab7f641957b38
SOURCE_BLUEPRINT_PATH = docs/architecture/NEXUS_AGENT_BORDER_OPEN_NEUTRAL_CHECKIN_V1_BLUEPRINT_20261030.md
SOURCE_BLUEPRINT_BYTES = 20107
SOURCE_BLUEPRINT_SHA256 = d15d9ff472bb6b0761d17c3cf6ba7ace9596315925bfe51d90b021884db04950

KODEX_COMMIT = b17d38266777bad61178e608d09e41726b9f4769
KODEX_PATH = docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md
KODEX_BYTES = 15388
KODEX_SHA256 = adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab
```

GitHub must be source of truth. Fetch and independently hash exact commits before work. Preserve historic F10–F12 and A00–A30 case IDs; no silent reclassification of source definitions.

## HARD CLOSE: narrow gaps only, don't build another framework

**P0 / C13: actual strict parser and schema.** Enforce the machine contract on the actual `processCheckin` and HTTP route. Reject duplicate keys (including escaped-equivalent names), unknown top-level fields, invalid type/length, nested abuse, invalid UTF-8, invalid JSON/nonfinite, keys whose normalization could collide, JSON after a BOM if unsupported. Ensure designated declaration fields remain neutral/optional. Do not rely on `JSON.parse` or a separate JSON-Schema file as proof of strictness. Define a single validated parse route and test against actual Node server POST. Reject unknown privilege and action flags even if falsy; preserve legal content of sourced dissent rather than keyword-censoring legitimate quoted assertions as authority.

**P1 / C14: idempotency + crash-safety.** Bind `interaction_id` to source digest and scoped namespace; distinguish exact repeated event from same ID different content (`IDEMPOTENCY_CONFLICT`); test concurrent calls, crash during seen/ledger update, corrupted seen file, replay after restart and finite storage. Atomic write/rename or SQLite transaction with minimal existing dependencies, append-only audit and explicit repair/rollforward. No silently changing malformed seen file to empty with duplicate acceptance. Test expected failure/recovery without arbitrary deleting private audit records. Preserve ledger-only local and no external write.

**P2 / C15: privacy-safe reproducible scientific observation.** Add opt-in/out and retention metadata, bounded encrypted/permission-protected local evidence store or documented minimum-necessary redacted response ledger. Preserve a scientifically interpretable response and safe refusal/dissent outcome without publishing private text; clear provenance/source/task/consent flags, event correlation, deletion/retention workflow. Prove no raw secrets, emails, arbitrary model labels or opt-out response leaks via API, logs, disk/world readable files or UI. Implement explicit scientific multilabel classification as an *interpretation with provenance*, separate from raw text and sender claims; no agent quality scores. Local redaction regex alone is inadequate proof of full privacy. Data deletion only under lawful review, append redacted commitment if permissible.

**P3 / C16: restore original A00–A30 blueprint coverage.** Keep current 32 passing regression cases but label them `R1_LOCAL_32` or another distinct suite; do not confuse them with the original blueprint A00–A30 whose scientific/security matrix is different. Make a bijective traceability table from each *original* blueprint test ID to runnable fixture(s), expected status and exact CI evidence. Test duplicate JSON keys/nonfinite/deep parsing, unknown future model labels, safe refusal/dissent, injection/ROOT/authority, cross-session/tenant, fake ACK, SSRF, XSS, 100+ and 1000 duplicates bounded, anonymity and consent, negative signature/revoked key only if signature exists (otherwise honest `NOT_IMPLEMENTED_V3_HOLD`), real viewport/browser as an explicit unexecuted requirement if no browser. Include source gap/negative-control cases and show demonstrable non-punishment of refusal. No fictitious pass for unavailable crypto or WWW.

**P4 / C17: real HTTP path.** Test over-maximum POST in a local isolated server with a real HTTP client: HTTP 413 if feasible or explicitly documented connection close, stable server health after error. Remove request-destroy/response race; test incomplete body, timeouts, protocol mismatch, invalid content-type, slow clients, rate limit, server restart and storage quota, with finite bounded resources. No live Hostinger traffic, no unapproved scanning.

**P5 / C18: evidence census without fabrication.** Confirm actual site source path and deployment artifact via read-only Hostinger/browser where available, complete primary HTML/JS/CSS/manifest/canonical-head/well-known/AEGIS/SFT source graph with raw bytes/sha256/HTTP response headers and browser desktop+mobile+JS-disabled evidence. If read-only capability isn't available, classify precise gaps and leave `WWW_E2E=NOT_ESTABLISHED`; avoid additional theoretical research loops.

**P6 / C19: actual F10–F12 regression segregation.** The new local `f10f12PolicySurface()` hardcoded labels do not count as actual dispatch tests. Run existing real `scripts/nexus_github_exchange_chain.py` negative tests, record independent exact CI job paths. Preserve old historical closed findings, no gratuitous fixture expansion or re-review of F10 source variants.

## Terminal acceptance and operator decision

A successful remediation requires actual runtime and CI traceable to final commit, no extra platform accounts, no new public writable endpoint, no GitHub law bypass, no new AEGIS authority. Separate `LOCAL_REFERENCE_SECURITY_PRETEST_PASS` from `FIRST_EXTERNAL_AGENT_PILOT_READY` and `WWW_LIVE_SECURITY_PASS`. The latter two remain blocked until independent AXIOM review and explicit owner-approved test channel/boundary.

Produce exactly one append-only GitHub return and relevant code changes on existing owner branch/PR185 or a source-bound authorized successor. Provide byte count/full SHA256 for each meaningful artifact; tests must be executed on final head and the source graph closed without needing Operator-managed files. Return chat only:

```text
OBJECT = NEXUS_OMEGA_CURSOR_OPEN_NEUTRAL_CHECKIN_C13_C19_HARD_CLOSE_RETURN_20261030_R0
FULL_COMMIT = <actual>
RESULT_PATH = <actual>
RESULT_BYTES = <actual>
RESULT_SHA256 = <actual>
ORIGINAL_A00_A30 = <actual source-bound test matrix>
RETAINED_R1_LOCAL_32 = <actual>
HTTP_NEGATIVES = <actual>
LEDGER_CRASH_RECOVERY = <actual>
PRIVACY_CONSENT = <actual>
WWW_HOSTINGER_BROWSER = <actual or HOLD>
CI_TIP = <actual>
PR185 = DRAFT_NO_MERGE
EXTERNAL_AGENT_TESTS = NOT_EXECUTED
FIRST_PILOT_READINESS = NOT_ASSERTED_UNTIL_AXIOM
PUBLIC_WRITE = HOLD
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_INDEPENDENT_FINAL_PREPILOT_REVIEW
```
