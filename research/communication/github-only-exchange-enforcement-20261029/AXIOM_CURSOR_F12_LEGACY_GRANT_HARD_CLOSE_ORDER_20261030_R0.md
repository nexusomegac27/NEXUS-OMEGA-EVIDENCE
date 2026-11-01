# NEXUS OMEGA · AXIOM → CURSOR · F12 Legacy Exception Hard Close

```text
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_F12_EXPERTENKODEX_LEGACY_GRANT_HARD_CLOSE_20261030_R0
PARENT = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_F10_F11_RECEIVER_POLICY_ADJUDICATION_20261030_R0
ISSUER = AXIOM
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = PREPARED_FOR_OPERATOR_WORK_ORDER_FORWARD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PR = 185
DATA_ROUTE = GITHUB_ONLY
MANUAL_OPERATOR_ROUTE = PURE_WORK_ORDER_TEXT_ONLY
NATIVE_APP_R3 = HOLD
AUTO_MERGE = NO
EXTERNAL_RUNTIME_ACTIVATION = NO
```

## Immutable input pins

```text
REPO = nexusomegac27/NEXUS-OMEGA-EVIDENCE
BASE_COMMIT = 264f38ee4edf76bb256211f06351a51d58f0328a
AUDIT_PATH = research/communication/github-only-exchange-enforcement-20261029/AXIOM_F10_F11_RECEIVER_POLICY_ADJUDICATION_20261030_R0.md
AUDIT_BYTES = 8059
AUDIT_SHA256 = ac5c3264de11fc647090ba87f8cdb9f37f3f9362861820b9eb42092ea0ad0810
EXPERTENKODEX_COMMIT = b17d38266777bad61178e608d09e41726b9f4769
EXPERTENKODEX_PATH = docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md
EXPERTENKODEX_BYTES = 15388
EXPERTENKODEX_SHA256 = adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab
```

All sources and necessary ancestors MUST be retrieved independently through GitHub and rehashed. A pure manual Operator work-order reference suffices; do not request payload files.

## Scope: ONE focused remediation, no research-stacking

**G0 Source bind:** Independently fetch exact audit and code at full commit. Bind Task Anchor Norm V1 and Expertenkodex V1, no reconstruction from chat.

**G1 F12 hard close:** The current `DispatchValidator._is_authenticated_legacy_grant` trusts `expertenkodex_legacy_grant.authenticated=true` supplied within an untrusted dispatch manifest. Replace self-attested identity with an **owner-controlled, independently verified** authorization source or disable this exception until such source exists. The grant must bind exact historical object, full commit/path/SHA256, authorized actor/principal, issuer, owner-approved policy version, permitted scope and non-retroactive cutoff. Never infer legitimacy solely from `grant_id` / `policy_version` strings. Independent provider-/repository-verified source identity and authorization must be provable before any legacy bypass.

**G2 Negative and positive tests:** Negative fixtures: self-asserted `authenticated:true`; forged grant identifier; nonhistorical new task disguised as `LEGACY_PRE_EXPERTENKODEX_V1`; forged issuer/actor; expired/revoked permission; wrong repo/commit/path/hash; implicit grandfathering from header absence; nested malformed grant; unregistered external actor. At least one positive *only if* an independently bound trusted grant fixture exists; otherwise clearly `LEGACY_GRANT_DEFAULT_DENY`. Test actual G2 dispatch, not helper-only.

**G3 Regressions:** Preserve previous 40+33 test coverage and run current suites. No blanket full-Windows test claim if unrelated `WinError 1314` or path separators cause unrelated failures; preserve separate diagnostic lane. Inspect GitHub CI at final exact head with check-run API, not just legacy commit statuses.

**G4 Ruleset read-only:** Verify rule 21252293 `main-evidence-protection`. It currently requires `validate` only; required owner review / code-owner review are not established. Report a precise owner-enactable change plan (unique required `validate-repository-structure`, `r27e-external-structural-firewall`, appropriate review count), but do not change rules, merge or grant rights without separately authorized action.

**G5 Receiver plan:** An authenticated external GitHub receiver remains `ADAPTER_NOT_CONNECTED`; do not invent an actor, assign the R27-E slot, publish private data or manufacture an ACK. Continue read-only discovery of actual auth/provider constraints. No pilot without owner grant. Maintain ability to do lawful offline work in parallel.

**G6 Return:** Append-only GitHub return in existing `research/communication/github-only-exchange-enforcement-20261029/`. Return in chat only a brief `OBJECT/COMMIT/PATH/BYTES/SHA256/CI_RUN_ID/CHECKRUNS/BLOCKERS` handshake. No operator ZIP search or manual evidence transfer.

## Terminal requirements

```text
F10 = CLOSED_BYTE_IDENTITY
F11 = DEFAULT_MISSING_CODEX_HEADER_FAIL_CLOSED
F12 = FAIL_CLOSED_UNTRUSTED_LEGACY_GRANT
GITHUB_CI_CHECK_RUNS = EXACT_HEAD_VERIFIED
GITHUB_MAIN_ENFORCEMENT = NOT_CLAIMED_UNTIL_RULES_PROVEN
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED_UNLESS_REAL_INDEPENDENT_EVIDENCE
NATIVE_APP_R3 = HOLD
HOSTINGER = NO
WWW_WRITE = NO
AUTO_MERGE = NO
CLAIM_PROMOTION = NO
NEXT = AXIOM_INDEPENDENT_GITHUB_READBACK
```
