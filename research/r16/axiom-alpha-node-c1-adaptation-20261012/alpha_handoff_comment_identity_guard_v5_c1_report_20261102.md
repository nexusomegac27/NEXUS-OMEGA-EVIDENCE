# NEXUS OMEGA · Alpha-Node V5 canonical GitHub comment-identity guard · 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_COMMENT_IDENTITY_GUARD_V5_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_PREPUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=0c6595660cc51cafe0d0d5a7daeeb7007defe9b1
MAIN_IMMEDIATE_PARENT=0c6e9385ad4fb7fdd9a0ee384427460e568b2809
PREDECESSOR_PR=296
PREDECESSOR_ISSUE93_RECEIPT=6583755114
FROZEN_EVALUATOR_FIRST_COMMIT=0df887db883e5d3074b8d220c628bfcb90493de1
CANDIDATE_SECOND_COMMIT=a2632ee3995b8ea117a9341e8e73b450956d5daf
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

GitHub API main ref and immutable main commit were read before the candidate. Source authority read at pinned main: AGENTS.md, GOVERNANCE.md, docs/AI_CONTEXT.md, docs/agent-protocol.md, docs/architecture/REPOSITORY_STRUCTURE.md, index/v1/latest.json, Operator direct C1 rule, Task Anchor V1, Alpha-Node R0, research/pipeline/POLICY.md and continuity guard, Repository Steward script, external write-slot registry, and Issue #93. Latest predecessor Issue #93 receipt was #6583755114; 278 issue comments were returned, latest all owner-authored. External actor allowlist is empty. No new R10 independent expert receipt was observed.

The four exact V1–V4 Python original texts were retrieved from immutable GitHub main, copied without modification into an isolated local directory, independently SHA-256 rehashed and Git-blob recalculated:

| Original | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| V1 | 3666 | `560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9` | `61bb0e9d989cc32f3ca55c2ee7264381345d0559` |
| V2 | 2842 | `04ad66f90be63f173709627f14f5bd87f7577b2d810323ce6156f8829befc98e` | `d3dedde011d601be2c29d0af6dcdbb30f4b3c94c` |
| V3 | 2256 | `40485983568c9c0722abdf4817fb3ef4061d30de44235b7378358772860c85df` | `1671d2cda04fc050b7bdc34abf71af2b22a88c16` |
| V4 | 2305 | `16e797b4e60d5854c7aa3cd25a22511f0cd6e4e8273eb13dca097a7f62ed8b2a` | `b99a6fea864a660e46d73147200ce3ab674c85e8` |

## NEGATIVE HYPOTHESIS / PINNED BASELINE

V4 checks literal receipt URL equality. GitHub issue-comment IDs identify comments independently of the URL path containing their anchor. Two syntactically accepted strings with the same `#issuecomment-201` anchor but different issue/pull paths bypass V4 cross-event deduplication. Another synthetic case uses the same comment ID in two receipt roles within one event. The real V4 module, with exact V1–V3 originals, returned `COHORT_DECLARED_ONLY, 2/2` for the cross-event alias and `COHORT_DECLARED_ONLY, 1/1` for the within-event alias. This is a structural false acceptance, not a proven real unattended handoff.

## ISOLATED CANDIDATE / FROZEN EVALUATOR

The evaluator was committed **first**, before V5 existed, at `0df887db883e5d3074b8d220c628bfcb90493de1`. File `frozen_alpha_handoff_comment_identity_evaluator_v5_20261102.py`: 5802 bytes, SHA-256 `0207c1701402850e185f4a6278826bad6e0e45c31d67b30bf82feada21bb9d11`, blob `f3674a5ef55c311ffa38152bf9ae2809a1f02296`. It was not edited for the candidate.

V5 was committed **second** at `a2632ee3995b8ea117a9341e8e73b450956d5daf`. File `alpha_handoff_comment_identity_guard_v5_20261102.py`: 2846 bytes, SHA-256 `923bad6e7131690856e7cac03b4d35fa84812b247fdef3530d3f52a972fb1711`, blob `9dcdd1ad8a31b1be8065cad030d2ede841ad7d2a`. V5 pins V4 by SHA-256 and wraps it without changing V1–V4. For eligible, structurally counted events, `#issuecomment-<digits>` is canonicalized by removing leading zeros and classified as one comment identity across receipt roles and handoff events. Non-comment root URLs retain exact-string comparison. No network dereference or actor authentication is performed.

A separate local Python process ran the unchanged frozen evaluator against pinned V4 and V5: **16/16 expected synthetic cases PASS**. Stdout: 2813 bytes, SHA-256 `74a8ac3d9bd093cfef52e0511d846e0e81a0fc4dde09215b0326d3915523cd5f`. V5 alias cross-event and within-event fixtures now return `NOT_COMPUTABLE`; distinct comment identities remain `2/2 COHORT_DECLARED_ONLY`. Other cases cover leading zeros, legitimate shared triggers/evaluators, excluded private events, missing evaluator, incomplete population, unknown eligibility, malformed input, V4's preexisting exact collision and mutated pinned V4 bytes. Reproduce from this directory:

```sh
python frozen_alpha_handoff_comment_identity_evaluator_v5_20261102.py alpha_handoff_cross_event_receipt_guard_v4_20261102.py alpha_handoff_comment_identity_guard_v5_20261102.py
```

## FALSIFIER / SCIENTIFIC BOUNDARY

Distinct comment IDs can still be invented or owner-authored; a syntactically valid anchor may not actually belong to its URL's issue. V5 cannot establish GitHub API-authenticated actor identity, comment existence, independent evaluator execution, or unattended handoff. Legitimate batch receipts covering multiple events may be conservatively refused. Frozen-before-candidate means temporal test separation, **not** an independent external scientific reviewer. Project-wide eligible-event numerator and denominator remain `NOT_COMPUTABLE`; no real new handoff success is counted. For this synthetic two-event fixture, the change is from V4 `2/2` false structural acceptance to V5 `NOT_COMPUTABLE`.

## R10 PASSIVE READBACK / PUBLICATION BOUNDARY

PR #115 remains open at `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; no issue comments, review comments or reviews on that PR. Detached manifest at original `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and current PR head has the same Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, 4588 UTF-8 bytes; expected pinned SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc` (not independently recomputed in this iteration). `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `AUTHENTICATED_EXTERNAL_ACTOR=NONE_REGISTERED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`.

This change is restricted to three additive research files in the existing R16 lane, no historical rewrite, new workflow, agent, runtime, Hostinger/WWW, Cursor dispatch, R10 merge or claim promotion. Publication requires actual PR checks, merge, immutable main readback and append-only Issue #93 receipt. `BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE`.
