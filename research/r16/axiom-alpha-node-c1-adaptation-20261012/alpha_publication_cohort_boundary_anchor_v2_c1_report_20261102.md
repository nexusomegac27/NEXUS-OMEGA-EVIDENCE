# NEXUS OMEGA · Alpha-Node · Bounded publication cohort first-boundary anchor V2 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_COHORT_FIRST_BOUNDARY_ANCHOR_V2_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE_PRE_PUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=2736760efd59f285e9af40292292e9df85e3ed95
PREDECESSOR_PR=284
PREDECESSOR_ISSUE93_RECEIPT=6568454883
FROZEN_ORIGINAL_V1_BLOB=3a046d603991e369319cdf7d0305d3b2f3329f8e
FROZEN_ORIGINAL_V1_BYTES=4662
FROZEN_ORIGINAL_V1_SHA256=f4cdd6da100891164a734dd81ef2873f4726c33fc28cfeb77cbfa305733d05e3
FROZEN_V2_ORACLE_FIRST_COMMIT=f1ffd93fbeea44552a4797812310d3d9667bea81
FROZEN_V2_ORACLE_BLOB=44aa7b7a118a4e97633af762614f9baa09b97185
FROZEN_V2_ORACLE_SHA256=32001324a755cccaaadfc6ccf8770a4c593d929ea89b31ab5ef03076c5e93dee
CANDIDATE_SECOND_COMMIT=d824e8f21284c9d201ff23297959d52cd384e0d5
CANDIDATE_BLOB=cebce85f00598c97251e01017f6eb3360f12a22e
CANDIDATE_SHA256=3ec701e63d61fcb09b387bad02f65f8f62aeeb220ffe97c5663f06bdfcc2df48
```

## OBSERVE / original bytes / predecessor

The published 274–283 census at immutable main `2736760efd59f285e9af40292292e9df85e3ed95` contains ten PR records and 36 source-file records. Its original manifest Git blob is `2f4dbfa8b05a073d5fd939b5fc779a2734f65fdd`. The frozen V1 Python evaluator (4,662 bytes, independently SHA-256 and Git-blob checked against GitHub) verifies adjacent parent pointers only when `prev` is already set. It **does not** bind PR #274's `parent_commit` or its first `merge_commit` to a fixed source-exact boundary. That is a structural false-acceptance class, not evidence that the historical GitHub commits were altered.

The real #274 boundary was independently compared through GitHub's commit comparison API: base `964fe47c4bdbad599e0689b132ff73c0822f3518`, head `3cc35487e8cae54aeac95377b6a8c376f412dc4f`, **ahead=1, behind=0**. These exact two IDs are the only new V2 anchors. The final cohort main anchor remains `7961026bf0f630aee160e083122c2900744d2da1`.

## NEGATIVE HYPOTHESIS / candidate

Counterhypothesis: a manifest with a forged first parent, or a forged first merge plus correspondingly changed second parent, can satisfy the old structural oracle despite misrepresenting the bounded cohort's start. The single isolated V2 candidate wraps the unchanged V1 evaluator and then requires the two verified first-boundary IDs. It makes **no** HTTP request, changes no old evaluator, and authenticates no external actor.

## PINNED BASELINE / INDEPENDENT TEST / FALSIFIER

A separate ten-fixture Python evaluator was **committed first**, at `f1ffd93fbeea44552a4797812310d3d9667bea81`, before candidate commit `d824e8f21284c9d201ff23297959d52cd384e0d5`. The frozen oracle was not edited after the candidate was written. The original V1 Python source was reproduced locally with an independently matching 4,662-byte SHA-256 and Git blob.

Local isolated Python execution, with fixed expected outcomes:
- Baseline V1: **10/10 expected outcomes**, including two observed false accepts of the new boundary-negative fixtures.
- Candidate V2: **10/10 expected outcomes**; first-parent and first-merge forgeries **2/2 rejected**, versus **0/2 rejected by V1**.
- Positive and six inherited regression cases retained their expected outcomes. One **explicit falsifier** (jointly forged middle merge and successor parent) remains **accepted by both V1 and V2**; it is a known residual gap, not a PASS for authenticity.
- Baseline stdout SHA-256: `fd7063fbfa14f17b6650ac9f0cb0ac42285ae9059009070897252a57ab1aa4c5`; candidate stdout SHA-256: `765155f3b8ba7239ec9eb4eb7c6be99708504b5c0c790f8b5f7166c16e60fffa`.

A separately implemented JS structural cross-check on the **actual GitHub manifest** returned: actual manifest V1/V2 **PASS/PASS**; forged first parent **PASS/REJECT**; forged first merge **PASS/REJECT**; forged middle link **PASS/PASS**. The frozen Python V2 oracle was **not executed against the full actual manifest**; the JS cross-check is not mislabeled as that execution. Neither synthetic test nor JS structural readback proves GitHub actor identity, HTTP transport authenticity, receipt completeness, or project-wide automation.

Reproduce from a checkout containing the existing V1 evaluator and the two new V2 files:
```bash
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_cohort_boundary_evaluator_v2_20261102.py baseline
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_cohort_boundary_evaluator_v2_20261102.py candidate
```

## DECISION / metrics / boundaries

Before: 0/2 new first-boundary tamper fixtures rejected by V1. After: 2/2 rejected by V2 under the frozen oracle. The denominator is **two synthetic boundary mutations**, not real handoffs. Ten historical PRs and 36 source files are a selected, bounded provenance cohort, not the project-wide eligible-publication population. `AUTOMATION_RATE_PROJECT_WIDE=NOT_COMPUTABLE`; `FULL_READBACK_RATE_PROJECT_WIDE=NOT_COMPUTABLE`.

Publish only these additive C1 research artifacts in the existing R16 directory through the owner-controlled GitHub PR/CI route. Preserve original V1 and historical files. A branch commit or PR is not main publication; merge, actual main, byte/sha/blob readback and Issue #93 receipt require separate post-publication verification. No runtime, Ruleset, external agent slot, Hostinger, WWW, R10 merge, biological experiment, new scheduler or claim promotion.

R10 side-observation: PR #115 remained open during this readback; the 264 inspected Issue #93 comments were owner-authored and the PR discussion contained no independent expert return. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.
