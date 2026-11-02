# NEXUS OMEGA — AXIOM Alpha-Node — receipt-role collision guard V3 — 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_RECEIPT_ROLE_COLLISION_GUARD_V3_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_PREPUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=331cd4619040035ad940795ae93c1559f06e2913
PREDECESSOR_PR=293
PREDECESSOR_ISSUE93_RECEIPT=6580464345
FROZEN_EVALUATOR_FIRST_COMMIT=2a7d1172240e0fc7c245a499645124a36e3c1879
CANDIDATE_SECOND_COMMIT=8f862a928900ce349ae212be8958345e311ead1d
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

GitHub API returned `main=331cd4619040035ad940795ae93c1559f06e2913`. Read AGENTS.md, GOVERNANCE.md, bootstrap context, task anchor, operator direct C1 publication authority, structure/order rules, research pipeline and Repository Steward. Issue #93 returned 275 comments; latest receipt is append-only typo correction #6580464345 to #6580456089. The external actor allowlist is empty. R10 PR #115 remains open with zero PR comments and zero reviews. Its detached R10 manifest is physically retrievable at immutable original commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and later head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; both return Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. No independent R10 actor receipt established.

Pinned V1: `alpha_handoff_denominator_guard_v1_20261102.py`, SHA-256 `560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9`, Git blob `61bb0e9d989cc32f3ca55c2ee7264381345d0559`. Pinned V2: `alpha_handoff_population_coverage_guard_v2_20261102.py`, SHA-256 `04ad66f90be63f173709627f14f5bd87f7577b2d810323ce6156f8829befc98e`, Git blob `d3dedde011d601be2c29d0af6dcdbb30f4b3c94c`. Exact V1/V2 copies were reconstructed from GitHub contents and independently rehashed locally before testing.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

V2 counts a synthetic eligible handoff as `COHORT_DECLARED_ONLY, numerator=1, denominator=1` when `trigger_receipt`, `handoff_receipt` and `independent_evaluator_receipt` all point to the **same** syntactically valid GitHub issue-comment URL. This is a concrete structural false acceptance of three different declared evidence roles from a single pointer. It is not proof that a real handoff was automated.

## ISOLATED CANDIDATE / FROZEN EVALUATOR

The evaluator was created in GitHub **before** the candidate: commit `2a7d1172240e0fc7c245a499645124a36e3c1879`; `frozen_alpha_handoff_receipt_role_evaluator_v3_20261102.py` = 5,437 bytes, SHA-256 `a3faa0a617d391b97649ef926d43c86bd967c0d1127bc77f81a048d60aa99d43`, Git blob `cbb40174e786d774d5d95cc22258c942ee602a7b`. It was not modified after the first commit.

Additive V3 `alpha_handoff_receipt_role_guard_v3_20261102.py` = 2,256 bytes, SHA-256 `40485983568c9c0722abdf4817fb3ef4061d30de44235b7378358772860c85df`, Git blob `1671d2cda04fc050b7bdc34abf71af2b22a88c16`. It rehashes the immutable V2 original before import, preserves V2's population gate and V1's eligibility checks, and rejects collisions among the three receipt-role URLs **only for structurally counted eligible events**. Any such collision returns `NOT_COMPUTABLE`, with null numerator and denominator. This prevents a declared 100% cohort rate from a reused URL.

## INDEPENDENT TEST / METRICS

A separate local Python process executed the frozen evaluator against the GitHub-byte-identical V1, V2, V3 files: **14/14 expected outcomes PASS**. Output JSON: 2,556 bytes, SHA-256 `2da3ea1ae930f817a3582edda34d5740db9585a5b070161e2dbe41a8b1c3c46e`. Cases include all-three identical URLs, all three pairwise collision classes, mixed cohorts, ineligible exclusions, unknown eligibility, missing evaluator, omitted population event, invalid input, pinned V2 mutation and a falsifier.

Before: V2 accepts synthetic same-URL fixture as `1/1 COHORT_DECLARED_ONLY`. After: V3 returns `NOT_COMPUTABLE`. Distinct declared URLs remain `1/1 COHORT_DECLARED_ONLY`. **This is one corrected synthetic false acceptance, not a measured real automation improvement.**

Reproduce from the research directory:

```sh
python frozen_alpha_handoff_receipt_role_evaluator_v3_20261102.py alpha_handoff_population_coverage_guard_v2_20261102.py alpha_handoff_receipt_role_guard_v3_20261102.py
```

## FALSIFIER / SCIENTIFIC LIMIT

Three different URLs may still be three owner-authored comments, invented strings, or unexecuted declarations. V3 accepts that falsifier as `COHORT_DECLARED_ONLY`; URL inequality is not independent actor authentication, scientific evaluation, or actual unattended execution. A single GitHub comment could in principle contain evidence for several roles; V3 conservatively refuses to compute a cohort rate rather than declaring fraud. V3 does not perform GitHub API receipt dereferencing, authenticate authors, or measure project-wide handoff success.

## DECISION / PUBLICATION BOUNDARY

One candidate only. Eligible real handoff numerator/denominator = `NOT_COMPUTABLE / NOT_COMPUTABLE`; project-wide publication readback numerator/denominator = `NOT_COMPUTABLE / NOT_COMPUTABLE`. No new productive handoff counted. Only existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` files added; no historical edits, new roots, runtime, Hostinger, WWW, external actor registration, Cursor dispatch or claim promotion. Publish via owner branch/PR only after actual checks; main merge and Issue #93 readback must be separately verified.

`BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE; CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`.
