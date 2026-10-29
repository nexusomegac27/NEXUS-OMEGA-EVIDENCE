# G6 — CI Governance Inventory

**OBJECT:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_ONLY_EXCHANGE_ENFORCEMENT_20261029_R1`  
**GATE:** `G6`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**STATE:** `PASS_WITH_CAVEATS_C1_CI_WIRED_RIGHTS_NOT_ACTIVATED`

## Integration performed (owner Draft PR only)

| Item | Evidence |
|---|---|
| Unit tests | `tests/test_nexus_github_exchange_chain.py` (22 offline cases) |
| CI workflow step | `.github/workflows/validate-repository-structure.yml` → `python -m unittest tests.test_nexus_github_exchange_chain -v` |
| Policy validator script | `scripts/nexus_github_exchange_chain.py` |
| STRUCTURE lane | `github-only-exchange-enforcement-20261029` @ STRUCTURE `1.7.16` |

## Required checks / branch rules (read-only inventory)

| Surface | Observation |
|---|---|
| Workflow | `validate-repository-structure.yml` runs on `pull_request` + `push` to `main` |
| Draft PR #185 branch | `codex/github-expert-exchange-foundation-20261029` |
| Branch protection API (`rules/branches`) | HTTP 404 — draft branch **not protected** at inventory time |
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
```

## Caveats

- Wiring the unittest into the draft-branch workflow is **local integration**, not proof that main required-checks enforce the V2 law.
- Draft-branch unprotected status is documented, not “fixed” by inventing protection rules.
- No Hostinger/www write; no unregistered agent runtime; no auto-merge.

## Verdict

`G6 = PASS_WITH_CAVEATS_C1_CI_WIRED_RIGHTS_NOT_ACTIVATED`
