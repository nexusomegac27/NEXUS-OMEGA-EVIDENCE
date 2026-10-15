# NEXUS OMEGA · AXIOM Alpha-Node R44 · Publication queue integrity (C1)

```text
OBJECT = NEXUS_OMEGA_AXIOM_R44_BRANCH_ONLY_PUBLICATION_QUEUE_GUARD_20261015_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_R43_DUAL_SOURCE_BRANCH_BYTE_REHASH_PACKAGE_20261015_R0
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
STATE = TESTED_ISOLATED_SCAFFOLD_CANDIDATE_NOT_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Actual source observation · 2026-10-15

GitHub readbacks against immutable main `d355400dabed3c280e1fce5030cab69ea099428b` find three **branch-only** reports: R35 head `48a95b13215a68242c87b589f180c3c8468f3f2b`, R36 head `aae0da1f4002ea06687969a9185b7b87e3aa6ee9`, R39 head `d7c7ce3ab8eb4a2cb030448297eb3364151a0387`. Each is one commit ahead of main; the corresponding report path returns 404 at pinned main. R43 branch is identical to main and its intended report is absent. **This is a four-branch sample, not a complete repository census.**

The passive AXIOM inbox Issue #93 has 19 comments, last ID `6137726458`, and no new receipt observed. PR status for individual sampled branches is **NOT_ESTABLISHED**; branch-only must never be presented as a completed merge.

## Single falsifiable R44 scaffold improvement

The read-only Python classifier emits a consolidated branch-publication queue with explicit `BRANCH_ONLY`, `EMPTY_BRANCH`, `HOLD_SCOPED`, and `MAIN_BLOB_MATCH_ONLY` states. Even a matching Git blob is **not** a complete main publication receipt without independently checked source bytes, tests and immutable commit readback. Synthetic PR OPEN/MERGED and issue-receipt fixtures do not promote branch-only material.

- Physically rehashed R43 predecessor ZIP: 1,158,975 bytes; SHA-256 `163581cd0dd6bf61f38efaab0f0b1bed798192cd5b0763952b1daf8af9641ba2`; manifest **15/15 MATCH**.
- Original frozen R43 evaluator **12/12 PASS**; R42 evaluator **8/8 PASS**.
- R44 separately frozen black-box evaluator SHA-256 `755efa6bce6e620c1dc1f887e760978575c6e8246311b72b2d1fd48e849fcb1d`; final **18/18 PASS**. Initial **17/18** failed and was corrected in the candidate, without editing the evaluator.
- R44 candidate SHA-256 `1d0efd6e0e8dd3fb17039831c10137fc26c60dad3830dc27add17591fe464a27`; deliberately mutated false-main-promotion candidate fails **6/18** tests.
- Derived GitHub observation SHA-256 `2c426e9bcbee9871401a1d038bfa82f1b1edec0cdb57871a0ad4db81797f8ce6`. These are **derived connector observations**, not independently authenticated raw GitHub API responses.
- Local replay package SHA-256 `d873e733e3c1716d4313d034b8c4e2b3a5b1f6f055e3c5b51344e7eeb538d0e0`; **14/14 manifest entries MATCH**. The local ZIP is **not** claimed to be uploaded to GitHub.

**Falsifier:** Any branch-only, empty-branch, PR-only or issue-only record classified as full main publication; or a mismatched main blob accepted as identical. The evaluator is separate code, not independent third-party scientific certification.

## Metrics and governance

In this bounded four-branch sample: **3 BRANCH_ONLY, 1 EMPTY_BRANCH, 0 verified main publications**. The real 30-day eligible handoff denominator and autonomous numerator remain **UNKNOWN**, so the >=90% target is **NOT COMPUTABLE**. No measured reduction in actual GitHub API calls, no productive integration, no WWW parity, no secrets, no new pipeline or external write slots, no Node reset, no runtime or model-weight modification, no claim promotion.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
