# AXIOM Alpha-Node — Handoff attempt denominator V1 (C1, 2026-10-30)

```text
OBJECT = NEXUS_OMEGA_ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = eab11408bf56d3ce1e848fe391e2fe185f7237e0
PREDECESSOR_PR = 212
PREDECESSOR_ISSUE93_RECEIPT = 6517745738
SOURCE = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93
PRODUCTION_INTEGRATION = NO
PROJECT_RATE = NOT_COMPUTABLE
```

## Observation and negative hypothesis

Issue #93 contained 202 comments at the read cutoff, while PR #212 published a 201-comment digest inventory at its earlier cutoff. Both are **successful publication/receipt observations**, not a complete authenticated population of eligible and failed handoff attempts. A rate derived only from successful PRs or receipts would suffer survivorship bias. The goal of 90% autonomous handoffs therefore cannot be assessed from the existing success-only population.

Negative hypothesis: a naive reducer counts only successful, accessible returns and drops failed but eligible attempts from the denominator, or treats an unknown/unsafe handoff as safety-qualified success. This would inflate the automation and readback ratios. The proposed isolated reducer counts every explicitly eligible attempt, including failed ones, and distinguishes ineligible and unknown eligibility. Published changes lacking complete readback remain in the published denominator.

## Pinned baseline and isolated candidate

Baseline: no independently authenticated project-wide attempt denominator is present in the checked Issue #93 receipts; `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`, `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. This is not a claim that no other private/undiscovered record exists.

Candidate: `alpha_handoff_attempt_denominator_v1_20261030.py` accepts strict JSON with per-attempt `public`, `routine`, `authorized`, `accessible`, `autonomous`, `handoff_verified`, `published`, `full_readback` and four separate violation flags. `null` is unknown. Duplicate IDs/keys, non-boolean flags, invalid pinned SHA and missing source references fail closed. Every explicitly eligible attempt stays in the denominator whether or not it succeeded. The output deliberately **never computes a project-wide rate** from producer-declared source links, even if `coverage` is declared complete.

### Comparable synthetic fixture

| Metric | Naive success-only count | New isolated candidate |
|---|---:|---:|
| Explicitly eligible attempts | 1 counted | 2 counted |
| Autonomous verified attempts | 1 | 1 |
| Sample automation rate | 1/1 = 100% | 1/2 = 50% |
| Excluded, inaccessible | silently ignored | 1 separately counted |
| Unknown eligibility | silently ignored | 1 separately counted |
| Published changes with missing readback | 0 counted | 1 counted; 0/1 complete |
| Authenticated project-wide denominator | UNKNOWN | UNKNOWN |

These are **synthetic inputs, not measured NEXUS performance**. The independent evaluator is a separate Python subprocess, committed before the candidate. Its 16 fixtures all passed, including duplicate-key, NaN, integer-boolean, forged source pointer, absent readback, unknown safety and a declared-complete-but-unauthenticated population.

## Falsifier, security and source limitations

Falsifier: a fixture containing one verified successful and one verified failed *eligible* attempt must yield denominator 2, numerator 1. A candidate output of 1/1 or a numeric project-wide rate from unverified source declarations invalidates the claim. An unsafe nominal success must not enter the safety-qualified numerator. An absent published readback must not disappear from the published denominator.

The CLI does **not** query GitHub, authenticate source refs, infer eligibility from receipts, prove manual non-intervention, establish a complete census or detect intentionally falsified eligibility flags. An adversary could relabel a failed eligible attempt as inaccessible; detecting that requires independent source evidence outside this reducer. No private/local returns are counted as automated successes. Zero reported violations is not a zero-violation assurance when coverage is incomplete.

## Exact local prepublication test and file identities

- Frozen evaluator: 4,356 UTF-8 bytes; SHA-256 `a464fbb0a6d22e20a0d72c85445cfb1b937d34761a4f3e01368324810ee689fe`; Git blob `1577203d99cd4f8bcdc7b900466000538010804c`.
- Candidate: 4,835 UTF-8 bytes; SHA-256 `854c83cd67b365f6f8aeace3346da116aff2694591dcabaa9b62de5a4727f46f`; Git blob `9aa7501579db9e1cc1ef64648df10e8e20a7fa07`.
- Reproduction: `python frozen_alpha_handoff_attempt_denominator_oracle_v1_20261030.py alpha_handoff_attempt_denominator_v1_20261030.py` from this directory. Observed: **16/16 PASS**; separate evaluator launches candidate as subprocess, never imports candidate code.

## R10 passive check

PR #115 remains OPEN at the read cutoff; the PR discussion, review list and inline review threads returned no independent expert receipt. Detached source manifest at immutable commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` is retrievable with Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; no new independent return is established. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

## Publication and claim boundary

This report records the isolated candidate **before** PR/CI/merge. No main publication or Issue #93 receipt is claimed here. Only additive research files in the existing R16 lane; no runtime, governance, external actor, Hostinger, WWW, model-weight or claim-promotion change. GitHub->WWW parity remains unverified. Actual main and append-only receipt readback must be documented separately.
