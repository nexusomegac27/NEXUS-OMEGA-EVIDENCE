# AXIOM Alpha-Node — declared-cohort handoff denominator guard V2 · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_COHORT_DENOMINATOR_V2_20261029_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 3df2b6bf7849284d96e07b5f50b528aeda5a345d  
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/201  
PREDECESSOR_ISSUE93_RECEIPT = 6507268967  
PRODUCTION_INTEGRATION = NO  
WWW_PARITY = NOT_ESTABLISHED

## Source / authority / baseline

Read exact repository objects on the pinned `main`: `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha-Node adaptation contract, operator direct-publication rule, Task Anchor Norm V1, repository-order policy, research pipeline README, and external write-slot registry. The registered external GitHub actor allowlist is empty. Authenticated GitHub connector login: `nexusomegac27` with owner push permission. The existing V1 source `alpha_handoff_denominator_guard_v1_20261029.py` was retrieved at the pinned commit, reconstructed byte-for-byte locally: **3,343 bytes**, SHA-256 `0f88904c3d7c75a1b334508d7ac6aa9a66ebbacfb3813c28c077bba519616b0b`, Git blob `e146e4efcd7d48bf4b56c7b8e6972f8ea4e6c235` MATCH.

V1 already correctly labels its sample as `DECLARED_INPUT_ONLY_NOT_AUTHENTICATED` and refuses to calculate project-wide rates. But it accepts a list with one reported successful handoff and returns `1/1` even if a second eligible attempted handoff was omitted by the caller. V1 has no declared-population field or manual-nudge flag. This is a **scope-completeness detection gap**, not a demonstrated malicious actor or false project-wide claim.

## Single candidate / negative hypothesis / falsifier

Hypothesis: a bounded, explicit cohort census plus manual-nudge evidence will reject omitted attempts and stop inflated *sample* automation numerators. Falsifier: V2 returns success for declared IDs `[a1,a2]` when only `a1` is supplied; credits an attempt requiring a manual nudge; includes private/inaccessible/unauthorized/nonroutine attempts in the eligible denominator; or promotes any sample to a project-wide rate. All must fail. The independent evaluator also checks duplicate IDs/JSON keys, missing fields, missing readbacks, reported safety violations and zero-denominator handling.

V2 accepts a declared cohort ID, `scope_complete=true`, an exact list of attempt IDs and the corresponding rows. It requires a bijection and strictly typed fields, and preserves V1's 262,144-byte input cap, 1,000-row cap, duplicate-JSON-key rejection and nonfinite-number rejection. Eligible = accessible AND routine AND public AND authorized. Automated success = eligible AND automated AND delivered AND NOT manual_nudge. Published-readback numerator requires all four reported commit/source/test/receipt flags. Safety violations are reported separately. All inputs are **self-declarations**, not verified event inventories.

## Isolated test / measured delta

- Frozen independent evaluator **first commit**: `frozen_alpha_handoff_cohort_oracle_v2_20261029.py`, 5,239 bytes, SHA-256 `0cc3adec7002ee0db544ee78342a1eadaaa2ce899dfa1863bcf6f472fafc676a`, Git blob `49ae026505eabe7bf2d7eed7c8321d3e51e3b682`.
- Isolated V2 **second commit**: `alpha_handoff_denominator_guard_v2_20261029.py`, 4,759 bytes, SHA-256 `3028c3dfa23ad2e267cddf7e56c7a2f18ef55bdc171ec9c45036061d03fb7148`, Git blob `6a725d1f014910c1a23a3d7ec4f227188abd6696`.
- Command: `python frozen_alpha_handoff_cohort_oracle_v2_20261029.py -q` in this R16 research directory. Independent Python subprocess evaluation on Linux: **20/20 PASS**, synthetic cases only. The oracle was committed before the V2 candidate; no evaluator modifications after candidate commit.
- Same omitted-attempt scenario: V1 (its native input schema) returned `1/1` for the one visible row, with no way to declare missing `a2`; V2 (new schema with declared `[a1,a2]`) returned `FAIL_CLOSED` / exit 2. This is a **differential interface-capability result**, not identical-input binary equivalence.
- Positive 10-eligible-row control with one manual nudge: V2 returns **9/10**, not 10/10. Private, inaccessible, unauthorized and nonroutine rows are excluded from the eligible denominator; published rows missing any readback flag do not count as full readbacks.

## Boundary / decision

The `scope_complete` flag is caller-attested; the guard cannot independently discover omitted attempts that are also absent from the declared ID list. The four readback booleans are not byte-level GitHub receipts. Real automation success rate, real full-readback rate and real unauthorized-action population remain **NOT_COMPUTABLE** without a complete independently authenticated event population. No third-party evaluator, full-repository integration, production runtime, Hostinger, WWW, external actor registration, or claim promotion. No existing V1, governance, pipeline or historical evidence file was overwritten. An initial exploratory branch `axiom/alpha-handoff-denominator-guard-c1-20261029` contains an oracle-only draft with an incompatible target filename; it was **not PR-submitted or merged** and is excluded from this candidate's evidence.

## R10 passive readback

The R10 PR #115 was still open with zero comments, zero submitted reviews and zero review threads. The immutable detached manifest was physically fetched at `539d4bb33d2ba2c4895713c1bc437ece0743eeea` (4,588 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`); no new independently authenticated expert return was observed. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.

`BLOCKED_LANE != BLOCKED_SYSTEM`  
`DRIFT_RESET = NON_DESTRUCTIVE`  
`CLAIM_CEILING = C1_DESCRIPTIVE_ONLY`
