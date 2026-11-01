# AXIOM Alpha-Node — CI Ruleset Coverage Witness V1 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_RULESET_COVERAGE_WITNESS_20261101_R0
DECISION=CONTRADICTION_APPEND_PLUS_TESTED_ISOLATED_SCAFFOLD
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=a85f2cda12af2229f434696100f3410ca99c7fcf
MAIN_PARENT=40125c80636b8d4b8cb62bb8671766d96784a846
PREDECESSOR_PR=269
PREDECESSOR_ISSUE93_RECEIPT=6558408946
FROZEN_ORACLE_FIRST_COMMIT=cf5447e52d0e4f9dbf1c4e15673d94f7f2b33495
CANDIDATE_SECOND_COMMIT=64db5537fd753b85392b12405808d496e922dd52
EVALUATOR_STDOUT_THIRD_COMMIT=4059593c3a416cf78c7e93955ab8e1028408bcd6
RUNTIME_OR_RULESET_MUTATION=NO
```

## Source-exact observation and falsified inference

Read-only GitHub API source, checked 2026-11-01:
- Active ruleset ID **21252293**, `main-evidence-protection`: https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293 . It targets `refs/heads/main`, requires signatures, linear history, PR, and **one** required status-check context: `validate` with integration ID **15368**. The ruleset specifies **zero** required approving reviews and no code-owner review.
- Historical PR #269 immutable head **d95c31615c793c12e6ebdcf2fbf8ae356bde7f01**: https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/d95c31615c793c12e6ebdcf2fbf8ae356bde7f01/check-runs . Eight check runs were `completed/success`, all with the same head. They have **five distinct (name, app ID) contexts**. Four `validate` runs share the same name and GitHub Actions app ID 15368.
- **Four distinct observed contexts are not listed as required by the ruleset**: `nexus-preentry-lab`, `r27e-external-structural-firewall`, `semgrep-cloud-platform/scan`, and `validate-repository-structure`. This is **1/5 observed distinct contexts required**, not a claim that all eight runs are individually hard gates.

**Negative hypothesis:** the prior reports' `8/8 SUCCESS` proves that all eight CI runs were mandatory merge gates. **Falsified as a ruleset-enforcement inference.** Actual successful CI execution and branch-rule enforcement are different observations. This is a configuration/assurance gap, not evidence of a failed check being merged or of unauthorized writes. Whether all five contexts *should* become mandatory is a separate Operator governance decision; this candidate does not change the ruleset.

The exact GitHub REST bodies are **not** archived here. The independent evaluator embeds a **normalized subset of connector-returned fields**, including eight observed run IDs. Rulesets are mutable; this observation is time-scoped, not an immutable ruleset attestation. GitHub's branch-protection endpoint separately returned 403 `Resource not accessible by integration`; the ruleset API was accessible. No hidden branch-protection state is inferred.

## One bounded candidate and independent falsifier

A read-only Python scaffold checks active `main` ruleset coverage against a supplied normalized check-run snapshot. It rejects duplicate run IDs, invalid app IDs, wrong heads, unsuccessful/incomplete checks, inactive rulesets, malformed input, and duplicate JSON keys. It reports missing required contexts and duplicate name/app combinations. It **does not** authenticate the supplied JSON, determine the correct governance policy, update GitHub settings, or prove a complete CI inventory.

The separate evaluator was committed before the candidate and kept unchanged. Its 11 subprocess fixtures include: the observed one-required/four-missing/four-duplicate configuration, a synthetic all-contexts-required control, a positive unique-name control, wrong app, inactive/wrong-branch rules, failed check, wrong head, duplicate run ID, empty requirements and bool app ID.

| Measure | Before | After |
|---|---|---|
| Dedicated deterministic ruleset/check-run coverage witness | Not present | Present, isolated |
| Frozen independent expected outcomes | Not run | **11/11 PASS**, exit 0 |
| Observed distinct required contexts | 1/5 | **1/5 unchanged** |
| Duplicate `validate` check runs | 4 | **4 unchanged** |
| Productive enforcement/integration | None | **None** |

**Falsifier:** any fixture with an incorrect status, missing-context list or duplicate count invalidates the candidate. A later authenticated ruleset requiring the four missing contexts and distinct check-run names would refute this time-scoped gap. The local evaluator is separate and frozen before the candidate, but not a second human or external expert.

## Exact original file bindings and reproduction

All are additive under the pre-existing R16 research path:
- Frozen evaluator: **4450 bytes**, SHA-256 `43599728b6098c4a04c9d49c1d7c9645aefcce39b60ccf7b40c8bd1291d49e9a`, Git blob `4cf2488a29d9a5e82d5a41c62260821aa1c6ef71`.
- Candidate: **3727 bytes**, SHA-256 `0ec91a70ed9e4091e6261cab9bc2c91a8457722669d51ccc81a4733609fdf26a`, Git blob `8562bdbb51d7b09f3850050a718c0cfc67f89756`.
- Original evaluator stdout: **2027 bytes**, SHA-256 `899af42b1b966b6622471d72e9dec5911d8f50ef339edf436bb7d0e112d342b8`, Git blob `a426eccc0b6a5b43e2bd41790ce3671466946cbd`.

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_ruleset_coverage_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_coverage_guard_v1_20261101.py
# expected exit 0; 11/11
```

## Boundary and decision

`CONTRADICTION_APPEND` for the inference that eight successful checks mean eight enforced gates; `TESTED_IMPROVEMENT` applies only to the isolated detection scaffold. Project-wide handoff automation and complete publication readback denominators remain `NOT_COMPUTABLE`. R10 PR #115 remained open, with zero independent PR/issue/review responses in this readback; no independent expert research or receiver ACK established.

No ruleset/branch-protection changes, external actor registration, CI evaluator alteration, worker, new pipeline root, Hostinger/WWW change, productive integration, claim promotion, or biological work. Publication requires PR/CI and exact main readback; a branch alone is not publication.
