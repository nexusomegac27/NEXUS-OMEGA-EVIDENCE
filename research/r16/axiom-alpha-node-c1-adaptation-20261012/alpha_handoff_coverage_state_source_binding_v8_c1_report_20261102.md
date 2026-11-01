# NEXUS OMEGA · AXIOM Alpha-Node · V8 coverage-state source binding · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_COVERAGE_STATE_SOURCE_BINDING_V8_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=9e5110ce84f2bd63bad1882d80a7ee6a219b448d
PREDECESSOR_PR=279
PREDECESSOR_ISSUE93_RECEIPT=6564862176
FROZEN_EVALUATOR_FIRST_COMMIT=b11736e62800f4e60a145f517cc0086c5787c98d
CANDIDATE_SECOND_COMMIT=3f20fa4f2a19cf8bcbc080b67cc80f671334fe9e
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The current `main` was pinned to `9e5110ce84f2bd63bad1882d80a7ee6a219b448d`. V7 and its immutable V3–V6 dependencies were retrieved by GitHub API and independently reconstructed locally. Git blob SHA-1 matches: V3 `b79b70e92771700afba4f5c860471da09c2775ed`, V4 `f78106128faf0f1af869958897fea315fa349cfc`, V5 `fa3f98e48a32a1df618c05ea6bdeeefd0ca7bd44`, V6 `c8a4d93f430062bd0f7708800cf50c7a3f78035a`, V7 `17b78f0c95cb9c469d654e70977c82354bb960ed`. No predecessor was edited. V7's 3,882 original bytes and Git blob were checked separately; it is research-only.

## NEGATIVE HYPOTHESIS / COUNTEREXAMPLE

V7 pins the attempt inventory and outcomes but omits `coverage_complete` from the SHA-256-pinned source snapshot. An input with `coverage_complete=true` can therefore report `METRIC_READY_STRUCTURAL_ONLY` even if the underlying census-completeness assertion was false or absent. The synthetic falsifier uses two declared eligible attempts, one completed and one failed. When the source census is explicitly incomplete but the submitted flag is changed to true, V7 reports **1/2 (50%) as if the denominator were complete**. A manipulated inventory can similarly make an ungrounded 1/1 appear complete; the original source remains unauthenticated in both cases. This is a *false metric-readiness* risk, not an observed production incident.

## PINNED BASELINE / ISOLATED CANDIDATE / FROZEN EVALUATOR

V8 requires a five-key UTF-8 source snapshot: `inventory`, `attempts`, `pinned_commit`, `coverage_source`, and `coverage_complete`. The latter MUST be the exact JSON boolean `true` in the SHA-256-pinned source and in the submitted payload. False, missing, numeric, string, null, array and object variants fail closed as `NOT_COMPUTABLE`. The V7 source schema remains historical and unchanged; this is a prospective V8 contract, not a migration of old records.

The separate 19-case evaluator was committed **before** the V8 candidate at `b11736e62800f4e60a145f517cc0086c5787c98d` and then read back with Git blob `18caea663f8f74fb4e5aea40976f9bf0f4a0650b`. The candidate was committed second at `3f20fa4f2a19cf8bcbc080b67cc80f671334fe9e` and read back with Git blob `30abeb0bf47bf53f96f8446ae6e3dfdc4128dd30`. The evaluator did not change after candidate creation. Each case executed the target validator in an isolated Python subprocess against synthetic fixtures.

| Frozen-oracle measure | V7 original | V8 isolated |
|---|---:|---:|
| Expected outcomes | 8/19 | **19/19** |
| Valid positive/regression cases | 5/5 | **5/5** |
| Negative cases rejected | 3/14 | **14/14** |
| Previously false-accepted negatives | 11 | **0/11 remaining in fixed suite** |
| Authenticated real project-wide handoff rate | NOT_COMPUTABLE | NOT_COMPUTABLE |

Local stdout SHA-256: V7 `1f5c48aafdb3de39ed84bb9341e30e69e1f1f15b010a77138aa5a661aabab43b`; V8 `833071eb4f1e45a8aeb74c931fe228f1e1d3dfafc5d6c75bf5ccfba93c672fd4`. These are locally executed results, not independently GitHub-archived stdout originals.

Reproduce from this existing research directory with Python 3:

```sh
python frozen_alpha_handoff_coverage_state_evaluator_v8_20261102.py alpha_handoff_inventory_outcome_source_binding_guard_v7_20261101.py --mode v7
# expected 8/19; exit 1
python frozen_alpha_handoff_coverage_state_evaluator_v8_20261102.py alpha_handoff_coverage_state_source_binding_guard_v8_20261102.py --mode v8
# expected 19/19; exit 0
```

## FALSIFIER / LIMITATIONS / DECISION

If a producer can alter both the source snapshot and its purported independent expected SHA-256, V8 can still accept a fabricated `coverage_complete=true`. Neither V7 nor V8 authenticates the external producer, source completeness, GitHub actor, event inventory, or any independent source pin. V8 only prevents a *coverage-state mismatch against unchanged pinned bytes*. The 19 tests are synthetic; no real automation numerator or denominator has been established. A future independent test with a genuine authenticated census must falsify or confirm any operational efficacy claim. No runtime, Hostinger, ruleset, new worker, model weights, historical source, or scientific claim promotion was changed.
