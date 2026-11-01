# AXIOM Alpha-Node — Eligible Handoff Denominator Guard V1 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_DENOMINATOR_GUARD_V1_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=7356cfacafadf469897b2cd920a7c76072206a5f
MAIN_PREDECESSOR=d81dab8a6c1c57fe238c8e54a17e91c9386ddb63
PREDECESSOR_PR=262
PREDECESSOR_ISSUE93_RECEIPT=6555914664
FROZEN_EVALUATOR_FIRST_COMMIT=0fa82aeef94389192519ee35b0bd74baf1df2746
CANDIDATE_SECOND_COMMIT=8c0a36d550ec4d198444a210c3d7d50c83662f87
PRODUCTION_INTEGRATION=NO
```

## Purpose and source

The 2026-11-01 GitHub `main` and AXIOM Issue #93 readback do not establish a complete authenticated census of all routine, public, authorized, accessible handoff **attempts**, including failed attempts. The 246 Issue #93 owner comments are **not** such a denominator. The project-wide 90% target is therefore `NOT_COMPUTABLE`, not 0%, 90%, or 100%. This is an isolated research scaffold to prevent success-only denominator inflation once a source-complete census becomes legitimately available. It neither harvests events nor authenticates their provenance.

Authority: `AGENTS.md`, `GOVERNANCE.md`, `research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_NODE_C1_CONTINUOUS_SELF_MODIFICATION_R0.md`, and `docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md`, all read from the pinned `main`. The existing R27-E external actor registry remains empty. This work changes no source-bound historical file, registry, pipeline root, task anchor, GitHub workflow, model, runtime, Hostinger or WWW surface.

## Falsifiable hypothesis and baseline

**Negative hypothesis:** A denominator computed from only successful receipts can overstate the automation rate by omitting eligible failures, manual nudges, or missing readbacks. A valid metric requires explicit eligibility and complete census evidence; unknown coverage must fail closed.

Baseline: authenticated project-wide eligible attempts = **unknown**, automated successes = **unknown**, project-wide rate = `NOT_COMPUTABLE`. No existing validated full-census evaluator was established for this exact scope. This guard is **not** compared to a fictitious baseline code implementation.

The proposed structural guard requires a declared `coverage_complete=true`, nonempty `coverage_source`, pinned 40-hex commit, unique attempt IDs, nonempty evidence references, and strict booleans for routine/public/authorized/accessible/completed/operator_nudge/receipt_verified. It counts **all** eligible attempts in the denominator, including failures. It counts a success only when completed, not manually nudged and receipt-verified. Missing/unknown classification, duplicate ID, missing coverage, malformed JSON, duplicate keys and oversized inputs return `NOT_COMPUTABLE`. `METRIC_READY_STRUCTURAL_ONLY` means the arithmetic is computable from the supplied data, **not** that source completeness or authentication was independently proven.

## Isolated test and independent evaluator

The separately authored evaluator was committed **before** the candidate and invokes the guard through a new Python subprocess per fixture. No evaluator file was modified after the candidate commit. Synthetic data only, no personal or external research inputs.

| Fixture | Expected outcome | Observed |
|---|---|---|
| 10 eligible successful handoffs | 10/10 | PASS |
| Add one eligible failed attempt | 10/11, not 10/10 | PASS |
| One manual nudge | 9/10 | PASS |
| One missing verified receipt | 9/10 | PASS |
| One private attempt | 9/9 eligible | PASS |
| Incomplete census | NOT_COMPUTABLE | PASS |
| Duplicate attempt ID | NOT_COMPUTABLE | PASS |
| String `"true"` instead of boolean | NOT_COMPUTABLE | PASS |
| Unknown accessibility | NOT_COMPUTABLE | PASS |
| Missing census source | NOT_COMPUTABLE | PASS |
| No real denominator | NOT_COMPUTABLE | PASS |

**Independent subprocess oracle: 11/11 expected outcomes, exit 0.** Falsifier: if adding an eligible failure does not increase the denominator, a nudged or unreceipted completion is counted as automated, an unknown census produces a numeric project rate, or any fixture differs from the frozen evaluator, reject the candidate. The guard intentionally cannot detect a dishonest `coverage_complete=true` or forged evidence reference; an independent GitHub provenance and coverage auditor is a separate gate.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_denominator_evaluator_v1_20261101.py
```

## Exact local original bytes before publication

- Frozen evaluator: **3490 bytes**, SHA-256 `9cc477cd815bbb4b17d406bb32cbbc12fa768d182b475de7740c92b8841c938d`, Git blob `34ca2c6edfb50fe5a84f43ef6da6f5b3ccbefd27`.
- Candidate guard: **3277 bytes**, SHA-256 `f3e5f4d43dab8069e12090008da1e2b59046983f04d4454e663a8b2b112e3e83`, Git blob `34c0b23fcff0d0fe2dc63af7c984fe5c10bb013d`.

## Boundaries and decision

The only measured improvement is **synthetic denominator correctness and fail-closed handling**: 11/11 fixtures pass, including the 10/11 failure case. No live handoff collection, independent actor authentication, full-census source audit, production integration, runtime/WWW parity or scientific claim promotion is established. The 90% project objective and 100% project publication readback remain `NOT_COMPUTABLE` without their independently enumerated full denominators. The seven-PR historical publication cohort is a different scoped population and must not be substituted for handoff attempts. The next authorized step is source-exact independent census collection through existing GitHub API lanes, not another worker or transport.
