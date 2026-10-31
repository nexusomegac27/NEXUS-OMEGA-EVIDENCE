# NEXUS OMEGA · AXIOM independent receiver & policy adjudication · 2026-10-30 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_F10_F11_RECEIVER_POLICY_ADJUDICATION_20261030_R0
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
CURSOR_HEAD_VERIFIED = bcdba870c519a2400a37498e4d3d1c3440370b6a
CI_RECEIPT_PREVIOUS = 90ac0337310c61b3bd2991647beab7326f65737a
PR = 185 OPEN_DRAFT_NOT_MERGED
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_F10_CLOSED_F11_DEFAULT_CLOSED_LEGACY_AUTH_BYPASS
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TERMINAL_PASS = NO
EXTERNAL_INDEPENDENT_RECEIVER_ACK = NOT_ESTABLISHED
NATIVE_APP_R3 = HOLD
AUTO_MERGE = NO
WWW_WRITE = NO
HOSTINGER_WRITE = NO
```

## 1. Scope and independent source checks

AXIOM independently read the GitHub commit `bcdba870c519a2400a37498e4d3d1c3440370b6a`, PR 185 metadata, code, tests, F10 discrepancy witness, read-only external receiver capability census, result and original task anchor, plus GitHub Actions and main ruleset. Parent GitHub source was read directly: source ≠ semantic truth.

The two GitHub commit check-runs APIs returned **10 total checks, all completed/success**, separately for `90ac0337310c61b3bd2991647beab7326f65737a` and `bcdba870c519a2400a37498e4d3d1c3440370b6a`. The 10 include `semgrep-cloud-platform/scan`, `r27e-external-structural-firewall`, `nexus-preentry-lab`, `validate-repository-structure` and other validations. Six PR-workflow runs also individually returned success at both commits. **CI_TIP_10_OF_10=INDEPENDENT_GITHUB_CHECK_RUN_CONFIRMED**, not merely producer-reported. This is evidence of executed CI, not C1 promotion, scientific truth or external transfer.

GitHub compare `90ac033...bcdba870`: ahead 1, behind 0, only `docs/architecture/REPOSITORY_STRUCTURE.json` and `research/communication/github-only-exchange-enforcement-20261029/RESULT_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1.md` changed. `STRUCTURE_HONESTY_BUMP_TIP != CI_RECEIPT_TIP` is preserved even though check-run API independently confirms 10/10 success at the newer tip.

## 2. F10 · independent byte-level closure

Source: `research/communication/github-only-exchange-enforcement-20261029/NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0_TASK_ANCHOR.json` at the pinned Cursor head.

AXIOM fetched LF source, counted **59 LF newline characters** and independently SHA-256 hashed the original and reconstructed CRLF variant:

```text
ORIGINAL_GITHUB_LF_BYTES = 2661
ORIGINAL_GITHUB_LF_SHA256 = 92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b
RECONSTRUCTED_CRLF_BYTES = 2720
RECONSTRUCTED_CRLF_SHA256 = aca0ae992a2d27849f7ba626ec6c73defc639968ee90fa417a71a921ede5b4f8
RECONSTRUCTED_CRLF_EQUALS_HISTORICAL_HANDSHAKE = YES_EXACT_MATCH
DELTA = 59_CR_BYTES
F10 = INDEPENDENTLY_RESOLVED_DUAL_BYTE_IDENTITY
```

Preserve both historical classes: `A=CURSOR_WORKTREE_CRLF`, `B=GITHUB_CANONICAL_LF`. No silent rewrite, no claim of tampering, no need to reopen F10 unless new contrary evidence appears.

## 3. F11 · default missing-header block verified; NEW material issue F12

Current `scripts/nexus_github_exchange_chain.py` `DispatchValidator.validate_manifest` now rejects manifests without EXPERTENKODEX fields with `MISSING_EXPERTENKODEX_HEADER`. This default branch and F11 tests are present in source and CI. **F11_DEFAULT_BLOCK = PASS_SOURCE_AND_CI_EVIDENCE**.

However, the same method allows an exception whenever `_is_authenticated_legacy_grant(manifest)` returns true. That function checks **only untrusted, sender-supplied manifest fields**:

```python
grant = manifest.get("expertenkodex_legacy_grant")
if not isinstance(grant, dict): return False
if grant.get("authenticated") is not True: return False
if grant.get("classification") != "LEGACY_PRE_EXPERTENKODEX_V1": return False
if not isinstance(grant.get("grant_id"), str) or not grant["grant_id"].strip(): return False
if not isinstance(grant.get("policy_version"), str) or not grant["policy_version"].strip(): return False
return True
```

There is no validation in this branch of independently verified authority, owner signature/commit, registered grant ID, issuer principal, historic cutoff or source-object legitimacy. The test `test_authenticated_legacy_grant_accepted` explicitly supplies an arbitrary `authenticated: true` fixture and expects a PASS. Hence an untrusted new dispatch envelope can impersonate a legacy exception and skip mandatory codex validation.

```text
F12 = SELF_ASSERTED_LEGACY_GRANT_AUTHENTICATION_BYPASS
STATUS = MATERIAL_SECURITY_AND_GOVERNANCE_GAP
F11_DEFAULT_BLOCK = VERIFIED
F11_UNIVERSAL_MANDATE = NOT_YET_ENFORCED
```

**Required repair:** fail-closed legacy path by default; grant only if an owner-controlled, authenticated, version-pinned allowlist/registry or detached verifiable authorization binds `grant_id`, recipient actor, pre-code-existence source object, issuer and exact commit/path/sha256. Never accept `authenticated: true` in source data as proof. An impossible-to-verify historical object stays `SOURCE_GAP_HOLD`, not auto-promoted. Add negative tests for self-attested legacy, forged grant ID, novel object pretending historic, modified grant and wrong signer; a positive test must use an independently trusted registry fixture. Add tests in the **actual dispatch path**, not just helper unit tests.

## 4. Main ruleset · independent status

Public GitHub REST: ruleset `21252293`, `main-evidence-protection`, active only on `refs/heads/main`.

- required `pull_request`, signatures, linear history, no deletion/non-fast-forward;
- `required_status_checks` contains exactly one context `validate` (integration ID `15368`);
- `required_approving_review_count=0`; `require_code_owner_review=false`;
- the explicit `validate-repository-structure` / Expertenkodex check is **not** independently mandated as its own unique check name;
- no bypass actors listed.

Therefore `PR185_10_OF_10_CI_SUCCESS != EXPERTENKODEX_MAIN_REQUIRED_ENFORCEMENT`. GitHub documentation supports requiring checks and code-owner reviews; modifying the rule requires an authorized repo administrator, not this audit. No rule change, merge, app installation or provider permission change performed.

Reference: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets

## 5. Receiver capability census

`CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261029_R1.md` is read-only. It lists public PR comments, full commits and CI receipts as potential evidence surfaces but **does not identify an independently authenticated external agent principal**, app installation permission or preallocated return slot for this assignment. The established external actor allowlist remains `DEFAULT_DENY`; no actual independent recipient fetch or signed/verified ACK was observed. `PR_COMMENT_POSSIBLE != RECEIVER_ACK_OBSERVED`. The external receiver lane remains scoped `ADAPTER_NOT_CONNECTED`; do not inflate a synthetic receiver to an external expert.

A read-only public source fetch can still proceed independently; any external write, app installation, new GitHub principal or slot activation needs separate operator authorization.

## 6. Minimal next operational decision

Do **not** start Native App R3 or merge PR 185. Focus an owner-controlled Cursor follow-up exclusively on **F12** plus an independent GitHub read-only authenticated recipient capability census / documented authorization plan. Do not redo the independently closed CRLF/LF F10. Keep all artifacts in the current governed repository and return a chat-only pure handshake; no operator-managed ZIPs.

```text
NEXT = CURSOR_F12_LEGACY_GRANT_CLOSURE_AND_REAL_RECEIVER_PREPARATION
F10 = INDEPENDENT_CLOSED_C1
F11 = MISSING_HEADER_DEFAULT_BLOCK_CI_VERIFIED
F12 = OPEN_MATERIAL_BYPASS
RECEIVER_ACK = NOT_ESTABLISHED
PR185 = OPEN_DRAFT
MAIN_ENFORCEMENT = NOT_ESTABLISHED
TERMINAL_PASS = NO
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
