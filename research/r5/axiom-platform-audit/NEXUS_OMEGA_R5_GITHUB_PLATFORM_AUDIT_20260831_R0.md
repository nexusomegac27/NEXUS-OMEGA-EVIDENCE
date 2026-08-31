# NEXUS OMEGA R5 — AXIOM live GitHub platform audit

```text
OBJECT = NEXUS_OMEGA_R5_AXIOM_LIVE_GITHUB_PLATFORM_AUDIT_20260831_R0
STATE = OBSERVED_AND_DOCUMENTED_C1
AUDIT_BASE_MAIN = 003c2072b8e29a1c29cbb17e49b5f18bae0581bb
AUDIT_BASE_TREE = 04757c31820e7739de9d14aeafbfcdceb7dc4825
CLAIM_CEILING = C1
RULESET_MUTATION = NO
```

## Live-main drift relative to the QWEN frozen R5 foundation

QWEN-CODER's R5 foundation froze `main` at `bc312c4d2cd6afa579db1f077c88d8fe08fc9470` / tree `c8856faa74efa5770717d2d44dc7d51e4269cb22`.

Current ordered main at this audit base is `003c2072b8e29a1c29cbb17e49b5f18bae0581bb` / tree `04757c31820e7739de9d14aeafbfcdceb7dc4825`.

Therefore:

```text
LIVE_MAIN_DRIFT = YES
FROZEN_R5_BASE_REWRITTEN = NO
```

The drift is expected: it consists of the later repository-order architecture and does not retroactively rewrite the QWEN frozen foundation.

## Ruleset state

Observed repository ruleset:

```text
RULESET_ID = 21252293
RULESET_NAME = main-evidence-protection
TARGET = branch
INCLUDE = refs/heads/main
ENFORCEMENT = active
CURRENT_USER_CAN_BYPASS = never
BYPASS_ACTORS = []
```

Rules include deletion protection, non-fast-forward protection, required linear history, pull-request policy, required signatures, and required status checks.

The required-status-check rule is currently:

```text
STRICT = true
REQUIRED_CONTEXT_COUNT = 1
REQUIRED_CONTEXT = validate
INTEGRATION_ID = 15368
```

## Workflow check identities

At the audit base, the four historical logical validation workflows each declare the same job key/check identity `validate`:

```text
validate-anchor -> validate
validate-scientific-communication -> validate
validate-scientific-ledger -> validate
validate-a83-framework-hardening -> validate
```

The repository-order workflow introduced later declares a distinct job/check identity:

```text
Validate repository structure -> validate-repository-structure
```

However, the live ruleset still requires only the single context `validate`.

Therefore the conservative platform conclusions are:

```text
MAIN_PROTECTED_BY_ACTIVE_RULESET = YES
FOUR_LOGICAL_CI_WORKFLOWS = ESTABLISHED
FOUR_DISTINCT_PLATFORM_REQUIRED_GATES = NOT_ESTABLISHED
STRUCTURE_CHECK_EXECUTES = YES
STRUCTURE_CHECK_HAS_DISTINCT_IDENTITY = YES
STRUCTURE_CHECK_RULESET_REQUIRED = NO
```

`MAIN_UNPROTECTED` is not an allowed inference from the legacy branch-protection endpoint.

## Safe migration implication

A future check-identity remediation should not rename all existing `validate` jobs in one step while the ruleset still requires `validate`; that could make the required context unsatisfiable. A staged migration should preserve a compatible required context until the ruleset transition is explicitly authorized and verified.

This audit changes no workflow, ruleset, branch protection, claim state, or scientific result.
