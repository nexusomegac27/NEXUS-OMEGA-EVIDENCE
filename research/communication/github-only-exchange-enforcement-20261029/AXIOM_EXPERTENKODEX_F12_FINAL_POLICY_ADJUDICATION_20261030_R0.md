# NEXUS OMEGA · AXIOM independent F12 policy and external receiver adjudication · 2026-10-30 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_F12_FINAL_POLICY_ADJUDICATION_20261030_R0
PARENT = NEXUS_OMEGA_CURSOR_EXPERTENKODEX_F12_LEGACY_GRANT_HARD_CLOSE_RETURN_20261030_R0
CURSOR_SOURCE_COMMIT = ee992249164ed9fa7d3e71df4ae8286d31e27d9e
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PR = 185
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_F10_F11_F12_LOCAL_IMPLEMENTATION_CLOSED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
GITHUB_DATA_ROUTE = MANDATORY
MANUAL_OPERATOR_ROUTE = PURE_WORK_ORDER_TEXT_ONLY
NATIVE_APP_R3 = HOLD
TERMINAL_PASS = NO
GITHUB_MAIN_ENFORCEMENT = PARTIAL
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
AUTO_MERGE = NO
HOSTINGER_WRITE = NO
WWW_WRITE = NO
```

## 1. Independent GitHub retrieval and SHA-256

Source commit `ee992249164ed9fa7d3e71df4ae8286d31e27d9e` was directly queried through GitHub. AXIOM independently recomputed all four supplied return SHA-256 values:

| Exact repo-relative path | Bytes | SHA-256 | Verdict |
|---|---:|---|---|
| `research/communication/github-only-exchange-enforcement-20261029/RESULT_EXPERTENKODEX_F12_LEGACY_GRANT_HARD_CLOSE_20261030_R0.md` | 5489 | `0dc1900b56b057b5a8a8be65353c398a253e3c3a7bc141c8b182e46eed90f565` | MATCH |
| `research/communication/github-only-exchange-enforcement-20261029/CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261030_R2.md` | 3233 | `8c7b0834d86d2393134d94412107924841ec72d78aa9f15edc29936afd6f3cb8` | MATCH |
| `docs/governance/EXPERTENKODEX_LEGACY_GRANT_REGISTER_V1.json` | 950 | `3bb2b28ca3c648780242d54c4a9814467d8ca38ffddaf27afee47027309bcdcd` | MATCH |
| `docs/architecture/REPOSITORY_STRUCTURE.json` | 19378 | `e6e54ff3a3dec5a085eb5b3b03222f965f7a0fd3f9495b263d1b478be802e5c4` | MATCH |

The requested legacy register contains `default=DENY` and `grants=[]`. The existing external actor registry `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` has `external_actor_allowlist=[]`; R27-E slot remains `PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED`.

## 2. Independent GitHub CI evidence

GitHub Check Runs endpoint for exact `ee992249164ed9fa7d3e71df4ae8286d31e27d9e`: `total_count=10`; all 10 completed/success, including `semgrep-cloud-platform/scan`, structural firewall, lab and validation checks. Six returned PR-triggered GitHub Actions workflow runs all completed/success. Job log for `Validate repository structure` run `41011899071`, job `123919420993`: `Ran 53 tests ... OK` and `Ran 33 tests ... OK`; combined **86 GitHub CI executed tests PASS**, not just local Cursor report. These tests are relevant scoped suites; no independent AXIOM local rerun and no universal scientific validation is claimed.

GitHub PR #185 metadata: OPEN, DRAFT, NOT MERGED at the source commit, 21 commits/37 changed files. Source-exact CI success at this specific commit, not at future head mutations.

## 3. F10, F11 and F12 scope

- **F10 closed** by prior independent reconstruction: canonical LF JSON is 2661 bytes SHA256 `92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b`; exactly 59 added CR characters yield historical CRLF 2720 bytes SHA256 `aca0ae992a2d27849f7ba626ec6c73defc639968ee90fa417a71a921ede5b4f8`.
- **F11 closed within the tested dispatch path**: a new mandate without Expertenkodex header is rejected by the actual `DispatchValidator`, not merely an isolated validation helper.
- **F12 closed for the current owner-branch configuration**: `LegacyGrantRegistry` checks owner-register entries; the production-candidate register has no grants and default DENY. The raw `authenticated:true` field is not sufficient to bypass the required header. Eight F12-specific negative/fixture tests are present in the GitHub CI-confirmed suite. No active legacy grant is authorized.

**Conditional future risk, not present F12 bypass:** If the register is ever populated with ACTIVE grants, a second explicit trust review is necessary. Current `LegacyGrantRegistry` reads a local register; its owner-attested provenance and the caller's authenticated GitHub principal are not proven by `authenticated:true` alone. No such populated grant is currently valid. Do not enable entries without operator-approved, immutable source and identity binding tests. A fixture-injected synthetic owner register is not proof of live owner authorization.

## 4. Main enforcement and real receiver remain open

GitHub ruleset `21252293` (`main-evidence-protection`) is ACTIVE on `refs/heads/main`, requires only named status check `validate`, permits zero required approving reviews, has `require_code_owner_review=false` and no bypass actors in the observed ruleset. Therefore green 10/10 check runs on PR #185 do not establish that the Expertenkodex-specific check or an independent review is REQUIRED for a future merge. Several checks have generic name `validate`; any enhancement must require the exact uniquely identified check and app source. No ruleset alteration is authorized in this adjudication.

PR #185 public issue comments endpoint returned 0 comments and pull-review endpoint returned 0 reviews at census time; no authenticated distinct expert ACK observed there. This does not establish that no expert could exist elsewhere, only that there is no bound evidence for this lane. The external actor allowlist is still empty, and GitHub reader/writer identity is not automatically conferred by an agent display name.

Technical distinction: a GitHub comment by an authenticated third party may evidence a user-authored claim/receipt, but not independently prove a true file-fetch-and-rehash execution unless the receiver supplies source-exact execution evidence. The verified receiver's principal and source snapshot/bytes/hash must bind to the receipt and independent work evidence. Never self-sign via owner token or treat the producer's synthetic receiver as an external expert.

## 5. Next controlled implementation stage

**Priority P0:** one owner-governed **receiver onboarding/pilot readiness** stage, not another broad fixture round. Cursor may prepare and source-bind a read-only candidate census, per-expert immutable manifests, a receiver self-fetch/rehash script and evidence receipt schema, safe public PR-comment return mode or separately authorized exact create-only return slots, and the required-check ruleset change plan. Do not create a new principal, authorize an external writer, generate/seal secret tokens, install a GitHub App, modify the ruleset, merge PR185, publish to WWW or start Native App R3. Such actions require separate Operator decision.

Pilot acceptance must be empirically observable:
```text
REGISTERED_EXTERNAL_PRINCIPAL = VERIFIED_DIFFERENT_FROM_PRODUCER
RECEIVER_FETCH = REAL_GITHUB_FETCH_AT_IMMUTABLE_COMMIT
RECEIVER_REHASH = OBSERVED_MATCH_WITH_RECEIVER_EVIDENCE
ACK = AUTHENTICATED_GITHUB_ENTRY_BOUND_TO_PRINCIPAL_AND_BYTES
RETURN = OWNER_REHASHED_SOURCE_EXACT
SOURCE_GRAPH = CLOSED_FOR_PILOT
CI_REQUIRED_STATUS = CONFIGURED_AND_ENFORCED_ON_MAIN
EXTERNAL_WRITE_RIGHTS = MINIMUM_APPROVED_ONLY
NATIVE_APP_R3 = HOLD_PENDING_OPERATOR_DECISION
```

GitHub first-party documentation: https://docs.github.com/en/rest/issues/comments (fine-grained Issues/Pull requests write permission for comment creation) and https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets (required status checks and approval parameters). No claim of installed agent adapter from documentation.

```text
TERMINAL =
F10=INDEPENDENT_CLOSED
F11=TESTED_DISPATCH_PATH_CLOSED
F12=EMPTY_REGISTER_FAIL_CLOSED_VERIFIED
CI=10_OF_10_AT_EE992249
TESTS=86_OF_86_GITHUB_CI_EVIDENCED
GITHUB_MAIN_ENFORCEMENT=PARTIAL
REAL_INDEPENDENT_EXPERT_ACK=NOT_ESTABLISHED
TERMINAL_PASS=NO
NEXT=CURSOR_RECEIVER_PILOT_READINESS_AND_RULESET_CHANGE_PLAN
```
