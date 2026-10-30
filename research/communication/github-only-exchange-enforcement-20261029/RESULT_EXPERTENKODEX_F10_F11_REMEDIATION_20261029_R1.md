# RESULT · Expertenkodex F10/F11 Hard Remediation R1

```text
OBJECT = NEXUS_OMEGA_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_RETURN_20261029_R1
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1
AXIOM_AUDIT = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_V1_INDEPENDENT_ADJUDICATION_20261029_R1
PINNED_PARENT_COMMIT = d1af9bc31317a07e9c4db29afe5c5faf1605b647
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_F10_WITNESSED_F11_FAIL_CLOSED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
DATA_ROUTE = GITHUB_ONLY
AUTO_MERGE = NO
NATIVE_APP_R3 = HOLD
```

## Scope executed

1. Independent GitHub rehash of AXIOM adjudication R1 + Expertenkodex V1 + prior RESULT_ENFORCEMENT R0 (MATCH).
2. F10: dual-identity Task-Anchor discrepancy witness (historical Identity A preserved; live Identity B recorded).
3. F11: DispatchValidator fail-closed when EXPERTENKODEX/CODEX_* headers absent; authenticated legacy grant escape hatch documented.
4. Regression + targeted negative tests (local scoped suite).
5. Read-only Capability Census for authenticated external GitHub receiver (no install / no new identity).
6. Return via PR #185 only (this object + STRUCTURE honesty bump).

## F10 · Task-Anchor dual identity

```text
WITNESS =
 research/communication/github-only-exchange-enforcement-20261029/
 F10_TASK_ANCHOR_DISCREPANCY_WITNESS_20261029_R1.md
IDENTITY_A_HISTORICAL_CRLF = 2720 / aca0ae99…e5b4f8
IDENTITY_B_LIVE_LF = 2661 / 92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b
ERASURE = NO
SOURCE_EXACT_RECONCILE = DOCUMENTED_DUAL_IDENTITY
F10_STATUS = WITNESSED_NOT_SILENTLY_NORMALIZED
```

AXIOM finding confirmed: Cursor-reported Identity A ≠ current GitHub-readable Identity B. Both hashes retained; neither invented.

## F11 · Dispatch Kodex mandatory

```text
IMPLEMENTATION =
 scripts/nexus_github_exchange_chain.py
 · DispatchValidator requires Expertenkodex bind
 · OR authenticated legacy grant (_is_authenticated_legacy_grant)
 · ELSE FAIL_CLOSED MISSING_EXPERTENKODEX_HEADER
TESTS =
 tests/test_nexus_github_exchange_chain.py :: TestF11*
NEGATIVE = order without EXPERTENKODEX/CODEX_* → REJECT
F11_BYPASS_PRIOR = CLOSED_BY_FAIL_CLOSED_DEFAULT
```

Prior AXIOM observation (validator only when Kodex header already present) remediated: absence of headers no longer skips the Kodex branch for substantive dispatch.

## Tests (local, Cursor report)

```text
EK_UNIT = tests/test_nexus_expertenkodex_v1.py · 33_OF_33_PASS
EXCHANGE_UNIT = tests/test_nexus_github_exchange_chain.py · 45_OF_45_PASS
SCOPED_COMBINED = 78_OF_78_PASS · EXIT_0
FULL_DISCOVER_WINDOWS_CAVEAT =
 prior full unittest discover observed non-F11 failures
 (symlink WinError 1314 · validate_anchor ASSET_PATH_ESCAPE on `\`)
 · NOT attributed to F10/F11 remediation
 · NOT claimed as universal PASS
GITHUB_CI = PENDING_POST_PUSH_THIS_COMMIT
```

## Capability Census (read-only)

```text
CENSUS =
 research/communication/github-only-exchange-enforcement-20261029/
 CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261029_R1.md
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
APP_INSTALL = NO
NEW_AGENT_IDENTITY = NO
PERMISSION_GRANT = NO_WITHOUT_SEPARATE_ORDER
```

## STRUCTURE tip (honesty bump)

```text
REPOSITORY_STRUCTURE_VERSION = 1.7.19
LANE = active_research_lanes.github-only-exchange-enforcement-20261029
TIP_OBJECT = NEXUS_OMEGA_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1
PARENT_TIP = NEXUS_OMEGA_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0
PINNED_COMMIT_AT_TIP_WRITE = d1af9bc31317a07e9c4db29afe5c5faf1605b647
STRUCTURE_CONTENT_SHA256 =
 280230727457e238d9901f4af3443626f1a5070c5c8697a389a2dd87893a3a32
STRUCTURE_BYTES = 19058
```

## Artifact hashes (this return package, pre-commit)

```text
RESULT_THIS =
  (exclude self-hash recursion; file bytes/sha256 reported at commit tip)
F10_WITNESS =
 3241 / 6da8c517dbcbe9607d2af0e232fe081c3098f8974f1c3108237be185373c5d5f
CENSUS =
 2888 / 21a225add97edacc276f048bfb57badb58153f4db25c53a36ca1a3f825744cea
STRUCTURE_JSON =
 19058 / 280230727457e238d9901f4af3443626f1a5070c5c8697a389a2dd87893a3a32
AXIOM_AUDIT_R1_PRESERVED =
 7131 / 38339af22120fccd13aa30f9c14df7d71a038147694f40779714f91929502b18
```

## Integrity / walls

```text
HISTORICAL_OBJECTS = PRESERVED
AXIOM_AUDIT_R1 = UNCHANGED_APPEND_ONLY_PREDECESSOR
PARENT_ENFORCEMENT_R0 = PRESERVED
HASH_MATCH ≠ SCIENTIFIC_TRUTH
LOCAL_78_OF_78 ≠ GITHUB_CI_THIS_TIP
F10_WITNESSED ≠ ANCHOR_SINGLE_IDENTITY_CLAIM
F11_FAIL_CLOSED ≠ MAIN_BRANCH_RULESET_ENFORCEMENT
GITHUB_MAIN_ENFORCEMENT = NOT_ESTABLISHED
TERMINAL_PASS = NO
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
```

## Prohibitions observed

- No Hostinger/www write; no invent WRITE_ACK.
- No AUTO_MERGE; no NATIVE_APP_R3 start; no claim promotion.
- No erase of Identity A / AXIOM R1 / prior RESULT_ENFORCEMENT.
- No manual Operator file handoff; GITHUB_ONLY via PR #185.

## NEXT

```text
NEXT = AXIOM_INDEPENDENT_RECEIVER_AND_POLICY_ADJUDICATION
CURSOR_ACTION_AFTER_PUSH_CI = NONE
```
