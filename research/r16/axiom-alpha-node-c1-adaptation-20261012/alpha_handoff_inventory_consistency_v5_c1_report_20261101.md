# NEXUS OMEGA · AXIOM Alpha-Node · Declared handoff inventory consistency V5 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_DECLARED_INVENTORY_CONSISTENCY_V5_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
BASE_MAIN=71feb351c3e2436344a10b22b53ba19c946d73df
BASE_PARENT=3fef33f230f5cfbec75167811d0a12787f1847db
FROZEN_EVALUATOR_FIRST_COMMIT=fcb8a1cf4330ce34fc18bf3c2d12c9701a41d9d3
CANDIDATE_SECOND_COMMIT=daf5b4b261496819ad81c534407cdda1a31053ed
RUNTIME_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / NEGATIVE_HYPOTHESIS

The predecessor V4 at pinned `main` was retrieved by GitHub content API and independently reconstructed as 1,873 bytes, SHA-256 `92f2fa54dd7cf441f03c179e2732dd1a69983977e93c2144c088cc720f7466a6`, Git blob `f78106128faf0f1af869958897fea315fa349cfc`. Its V3 dependency was reconstructed as 3,920 bytes, SHA-256 `297b26d3d2eb9164459ad3fa31333acd52fb0ed8c1f70e64f1241808b90fcd11`, blob `b79b70e92771700afba4f5c860471da09c2775ed`. Neither original is modified.

Counter-hypothesis: V4's `coverage_complete=true` and nonempty `coverage_source` already prevent a failed but eligible attempt from being silently omitted. The fixed evaluator disproved this: with an originally declared two-attempt inventory, omission of failed attempt B yields a structurally valid **1/1 = 100%** under V4 instead of **1/2 = 50%**. This is a synthetic false-positive counterexample, not evidence of a real omitted NEXUS handoff.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

V5 imports V4 unchanged and requires a separately declared `inventory` with nonempty source reference, source commit equal to the pinned commit, strictly typed count, unique canonical expected attempt IDs, and exact equality of expected versus observed attempt IDs. A discrepancy returns `NOT_COMPUTABLE`; valid cases retain V4's eligibility arithmetic. The evaluator was committed **before** the candidate and not edited by it. All fixtures executed in separate local Python subprocesses.

| Fixed-oracle comparison | V4 baseline | V5 candidate |
|---|---:|---:|
| Expected outcomes | 5/17 | **17/17** |
| Inventory-mismatch negatives rejected | 0/12 | **12/12** |
| Positive and regression controls | 5/5 | **5/5** |
| Omitted failed attempt versus unchanged two-ID inventory | 1/1 = 100% | **NOT_COMPUTABLE** |
| Real authenticated project-wide automation rate | NOT_COMPUTABLE | NOT_COMPUTABLE |

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_inventory_evaluator_v5_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_evidence_ref_canonical_guard_v4_20261101.py
# expected: 5/17, exit 1
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_inventory_evaluator_v5_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_inventory_consistency_guard_v5_20261101.py
# expected: 17/17, exit 0
```

## FALSIFIER / SOURCE GAP / DECISION

Falsifier: V5 accepts a row set differing from the independently declared inventory, or changes the correct numerator/denominator for any of the five controls. **Known residual counterexample:** if both the inventory and attempt list are dishonestly truncated to A, V5 still returns structural 1/1 = 100%. It does not authenticate the inventory, prove complete enumeration, detect coordinated falsification, verify a GitHub event, or provide a productive collector. The independent *test logic* was temporally frozen; it was not authored by an independently authenticated external reviewer. Thus neither a real 90% target achievement nor independent scientific validation is established.

The full authenticated project-wide eligible-handoff denominator and publication-readback denominator remain absent. `AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. No external actor registration, R10 expert-return promotion, ruleset modification, Cursor dispatch, Hostinger/WWW write, runtime integration, model modification, or C1 claim promotion. Actual PR/CI/merge/main readback and append-only Issue #93 receipt are separate publication gates, not asserted by this research report.
