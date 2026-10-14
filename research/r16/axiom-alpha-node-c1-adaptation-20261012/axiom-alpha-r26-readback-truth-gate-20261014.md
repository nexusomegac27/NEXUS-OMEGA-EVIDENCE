# AXIOM Alpha-Node R26 — GitHub-main readback truth gate (C1, 2026-10-14)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R26_REMOTE_READBACK_TRUTH_GATE_20261014_R0
STATE = TESTED_SCAFFOLD_CANDIDATE_NOT_INTEGRATED
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR_R25_BRANCH = 4a369fb7975760a0d3874679c1acacc807082992
PREDECESSOR_R25_BLOB = ad7db97fd8f266d41c3175c3259237e7a8aad25e
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Source-exact contradiction and falsifier

The physically available R25 local ZIP SHA-256 is `b0f78ee26bb77e8a5d603ca49b98b7e6ffbe741367828a4d071c593e6b09f983`; its manifest was rehashed **22/22**. R25's pinned source SHA-256 is `9086eb07d0796e4630a66b082339bd22bf16ee6d6b08363cb687aca0b57de646`. The R25 funnel checks local source-receipt hashes but accepts a user-reported `MAIN_READBACK_MATCH`, arbitrary 64-hex readback hash and `issue_receipt=true` without fetching actual GitHub bytes. Its frozen synthetic test 08 counts a placeholder `a*40` commit and `b*64` hash as a completed **1/1** handoff. That is a limitation of **evidence-level classification**, not a mathematical denominator error.

**Negative hypothesis:** an unmerged branch or fictitious Issue #93 comment can be counted as completed. **Falsifier:** R25 reports 1/1 on the synthetic forged receipt; R26 refuses to classify it as independently verified without a real file/main/issue readback. The actual R25 commit `4a369fb7975760a0d3874679c1acacc807082992` was independently compared with main: status `behind` in the branch→main comparison, merge base `d355400dabed3c280e1fce5030cab69ea099428b`; R25 is **not** merged. Issue #93 has 19 comments, latest `6137726458`.

## Isolated candidate and separated tests

A read-only stdlib R26 overlay pins and reuses the unchanged R25 source and independently requests public GitHub REST objects: exact file bytes at immutable commit (SHA-256 + Git blob SHA-1), ancestry of that commit on `main`, and an Issue #93 comment binding path, commit and file SHA-256. Missing or inconsistent evidence is a scoped gap, not success. Synthetic HTTP fixtures are loopback-only and can **never** increment live verified successes. No credentials, writes, runtime activation, or Hostinger calls.

- Candidate SHA-256: `084f3a21b7323a951828653c261c51f05f7290fc3e3a6ccc1d238da38676cb6f`.
- Separate black-box evaluator frozen before implementation: SHA-256 `da4dcbb0eb7fcade90647215f365327e2f9d9a5a386b9dcf4e03042425f7302f`.
- Evaluator: **13/13 PASS**, including wrong bytes, branch-not-main, wrong Issue body/thread, duplicate binding JSON, unknown preflight and blocked nonloopback test endpoint. A supplemental actual R25 source-tamper test returned exit 2, `R25_SOURCE_HASH_MISMATCH`. Frozen test 09 was only a smoke test; it was not modified after freezing.
- Controlled before/after: forged R25 completion **1/1 reported** → R26 **0/1 live-verified**. Valid synthetic remote evidence yields **1 synthetic acceptance / 0 live success**; no real positive remote receipt has been tested.
- Local R15–R24 census: **10 reported attempts**, 0/10 prospective preflight evidenced, 0 eligible and 0 live-verified; target ratio **undefined 0/0**, not 0% or 100%.

## Decision and boundaries

`TESTED_IMPROVEMENT_CANDIDATE` concerns prevention of falsely corroborated GitHub-main handoffs, **not** increased automation throughput. The complete source/test ZIP is available only as a local conversation artifact, SHA-256 `64035290b54f3dd11dbe29aaa108f85c9918d0750881d649326543842c9dec65`, manifest **24/24**; this GitHub note alone does not permit full independent replay. The `preflight=PASS` field remains producer-reported even if live GitHub readback succeeds; issue text is not actor authentication or scientific validation. No historical validator, model, write registry, runtime, website, or path-bound source changed. GitHub-main publication and WWW parity require distinct real receipts.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
