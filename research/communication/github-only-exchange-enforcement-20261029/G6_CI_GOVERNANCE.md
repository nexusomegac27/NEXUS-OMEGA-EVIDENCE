# G6 — CI Governance Inventory (R2)

**OBJECT:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_EXCHANGE_HARD_REMEDIATION_20261029_R2`  
**GATE:** `G6`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**STATE:** `PASS_WITH_CAVEATS_C1_CI_WIRED_RIGHTS_NOT_ACTIVATED`

## Separation (mandatory)

```text
CI_CONFIGURED = YES
CI_EXECUTED = LOCAL_40_OF_40_PASS_THIS_BIND
REQUIRED_CHECK_ENFORCED = NOT_ESTABLISHED
MERGE_AUTHORIZED = NO
```

## Integration performed (owner Draft PR #185 only)

| Item | Evidence |
|---|---|
| Unit tests | `tests/test_nexus_github_exchange_chain.py` (40 offline adversarial cases F01–F09) |
| CI workflow step | `.github/workflows/validate-repository-structure.yml` → `python -m unittest tests.test_nexus_github_exchange_chain -v` |
| Policy / chain script | `scripts/nexus_github_exchange_chain.py` (F01–F04 remediations) |
| STRUCTURE lane | `github-only-exchange-enforcement-20261029` |

## Required checks / branch rules (read-only inventory)

| Surface | Observation |
|---|---|
| Workflow | `validate-repository-structure.yml` on `pull_request` + `push` to `main` |
| Draft PR #185 branch | `codex/github-expert-exchange-foundation-20261029` |
| Branch protection API (`rules/branches`) | HTTP 404 at prior inventory — draft branch **not protected** |
| CODEOWNERS | Root `* @nexusomegac27` |
| GitHub App rights activation | **NOT performed** this bind |
| Auto-merge | **NO** |

## Rights / Codeowners control

```text
NEW_GITHUB_APP_PERMISSIONS = NOT_ACTIVATED
UNAPPROVED_RIGHTS_ESCALATION = NO
CODEOWNERS_MUTATION = NO
BRANCH_RULES_MUTATION = NO
REQUIRED_CHECKS_ENFORCED_ON_MAIN = NOT_ESTABLISHED_THIS_BIND
PR185_MERGE = NO
```

## Caveats

- Local 40/40 PASS and CI step wiring ≠ main required-check enforcement of V2 law.
- Draft-branch unprotected status is documented; protection rules are not invented.
- No Hostinger/www write; no unregistered agent runtime; no auto-merge.

## Verdict

`G6 = PASS_WITH_CAVEATS_C1_CI_WIRED_RIGHTS_NOT_ACTIVATED`
