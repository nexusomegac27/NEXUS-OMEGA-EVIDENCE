# NEXUS OMEGA — AXIOM Alpha-Node — population-coverage guard V2 — 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_POPULATION_COVERAGE_GUARD_V2_20261102_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_PREPUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=9a99a14d6f50fdc95ae4d8199e29ef1bd8de3001
PREDECESSOR_PR=292
PREDECESSOR_ISSUE93_RECEIPT=6579058793
FROZEN_EVALUATOR_FIRST_COMMIT=f6c1a1706109b4dcf2bd52e9d87ada188e27009a
CANDIDATE_SECOND_COMMIT=9d547ddb618397ca17bca364d3c29210eb742290
SOURCE_V1_GIT_BLOB=61bb0e9d989cc32f3ca55c2ee7264381345d0559
SOURCE_V1_SHA256=560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL BYTES / AUTHORITY

The latest owner repository `main` was read at immutable `9a99a14d6f50fdc95ae4d8199e29ef1bd8de3001`. Bootstrap, governance, operator C1 publication authority, repository order, shared pipeline and read-only Repository Steward were read at that ref. Issue #93 contained 273 owner-authored comments, latest predecessor receipt `6579058793`; PR #292 is merged. The V1 source was independently reconstructed byte-for-byte from GitHub contents: 3,666 bytes, SHA-256 `560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9`, Git blob `61bb0e9d989cc32f3ca55c2ee7264381345d0559`.

## NEGATIVE HYPOTHESIS / BASELINE

V1 trusts `population.enumeration_complete=true` plus a caller-supplied enumeration commit/hash, without comparing event IDs against a declared population ID inventory. If a third eligible event is omitted from two supplied events, V1 reports `COHORT_DECLARED_ONLY, numerator=2, denominator=2` (synthetic apparent 100%), even when `population.enumerated_event_ids=['a','b','c']` is present. This is not a real project-wide numerator or denominator; it is an omission-acceptance defect in a research-only census scaffold.

## ISOLATED CANDIDATE

Additive V2 wrapper `alpha_handoff_population_coverage_guard_v2_20261102.py` (2,842 bytes; SHA-256 `04ad66f90be63f173709627f14f5bd87f7577b2d810323ce6156f8829befc98e`; Git blob `d3dedde011d601be2c29d0af6dcdbb30f4b3c94c`) preserves V1 and checks its SHA-256 before importing. It requires sorted unique bounded ASCII event IDs, explicit count, canonical JSON ID-list SHA-256 and exact equality between enumerated and supplied IDs. Missing/extra event records return `NOT_COMPUTABLE`, not an apparently successful rate. Malformed enumeration returns `INVALID_INPUT`; changed V1 original bytes return `HOLD_SCOPED`.

The ID list, count, digest, and source manifest are **caller-supplied**. V2 does not enumerate GitHub events, authenticate an independent evaluator, verify a source manifest against a provider, or establish a real automation rate. A jointly forged complete population is accepted as `COHORT_DECLARED_ONLY`.

## INDEPENDENT TEST / METRICS

The independent evaluator `frozen_alpha_handoff_population_coverage_evaluator_v2_20261102.py` was committed first at `f6c1a1706109b4dcf2bd52e9d87ada188e27009a`, before the candidate at `9d547ddb618397ca17bca364d3c29210eb742290`; it was not changed afterwards. Evaluator: 5,600 bytes, SHA-256 `883c00efc43aad6d573c0cd566bfcf90f1c58e8c646d658a6e3b020d10c92476`, Git blob `89540dac927a8fad74fe40970b48df37dc26232a`.

Local separate Python process: **18/18 expected outcomes**, stdout JSON 2,511 bytes, SHA-256 `44169e262350a778cf8c53d3877aaf98adb4269f448968b4ce82ca4f4a6b63af`. Frozen tests include a real omitted-event negative fixture, extra-event mismatch, missing digest/list, duplicate/unsorted IDs, malformed count, private exclusion, unknown eligibility, missing evaluator receipt, mutated original V1 bytes, and a deliberately co-forged full-population falsifier. The exact published branch blobs match the locally executed evaluator/candidate files.

**Before:** V1 accepts omitted-event synthetic `2/2` and reports a declared 100%. **After:** V2 returns `NOT_COMPUTABLE` for that same omitted event, while an exact declared `2/2` remains `COHORT_DECLARED_ONLY`. This measures one corrected structural false acceptance, not a measured increase in real handoff automation.

Reproduce from the same directory with:

```sh
python frozen_alpha_handoff_population_coverage_evaluator_v2_20261102.py alpha_handoff_denominator_guard_v1_20261102.py alpha_handoff_population_coverage_guard_v2_20261102.py
```

## R10 PASSIVE HANDSHAKE / SEPARATE LANE

PR #115 remains open; its original detached manifest at immutable `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and latest known head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` have identical Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` and 4,588-byte UTF-8 content. The R10 source is **PR branch-only**, not in `main`; a main-path 404 is not evidence of missing branch bytes. Owner-mediated expert report bytes exist, but PR has zero reviews and no independently authenticated expert ACK. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_INDEPENDENT_GITHUB_ACTOR=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_VERIFIED`. No R10 merge or dispatch.

## DECISION / LIMIT

One candidate only: `TESTED_IMPROVEMENT_C1_ISOLATED`, subject to PR/CI and actual main readback. Project-wide eligible handoff numerator/denominator: `NOT_COMPUTABLE / NOT_COMPUTABLE`. Project-wide publication readback numerator/denominator: `NOT_COMPUTABLE / NOT_COMPUTABLE`. This iteration adds no verified productive handoff. No changes to production CI, runtime, Hostinger, WWW, external actor registry, model weights, or historical files. `BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE`.
