# NEXUS OMEGA · AXIOM Alpha-Node R88 — current 30-day as-of freshness guard (C1)

OBJECT = NEXUS_OMEGA_AXIOM_R88_CURRENT_ASOF_WINDOW_GUARD_RESEARCH_20261017_R0
STATE = ISOLATED_TESTED_IMPROVEMENT_CANDIDATE_NOT_INTEGRATED
PREDECESSOR = NEXUS_OMEGA_AXIOM_R87_EXACT_30DAY_COHORT_WINDOW_GUARD_20261017_R0
PREDECESSOR_ZIP_SHA256 = 851e03baea46236ec469bbd8f9c2424484f0097a2b5790f699328a578684d180
PREDECESSOR_CODE_SHA256 = 1dc1243f9c3d2e6f7401e2994a2d28abee925a3e0c791633eafc1434d388f561
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Negative hypothesis and one candidate

R87 enforces a 30-day duration, but a byte-pinned 2025 cohort still returns 100% when a consumer mistakes a historical result for the *current* 30-day KPI. A future-ending 30-day cohort and a missing trusted clock also pass R87's historical audit. R88 adds an explicit `audit_current_30day(events,reader,cohort)` method; the old historical `audit()` remains unchanged. The new current-KPI method requires the cohort end to lie within [independently supplied reader UTC now minus 3600 seconds, now]. Stale, future or unverifiable clock/window => ratio null and scoped HOLD.

## Pre-frozen independent evaluator and outcomes

Evaluator SHA-256: `2299cfb319550462b084f4f80fb3c88790ada48359c22426de1ded4669378c49`.
Identical current-KPI oracle: R87 0/17, R88 17/17 PASS (the R87 interface has no current-KPI contract).
Five stale/future synthetic 30-day negatives: numeric false-current ratio R87 5/5; R88 0/5.
Six missing/malformed-clock negatives: numeric false-current ratio R87 6/6; R88 0/6.
Fresh valid controls: R88 4/4; deliberately broken R88 mutant: 12/17.
Unchanged historical `audit()` regression on R88: R87 15/15, R86 16/16, R85 24/24, R84 18/18.

FALSIFIER = Any numerical current-KPI ratio for a cohort ending in the future, >3600 seconds before trusted as-of, or with no parseable trusted reader clock; or a fresh exact-30-day cohort rejected solely on as-of freshness.

These tests are isolated synthetic independent-process checks, not external scientific acceptance. The reader-clock source string alone is not independent authentication. A real trusted clock/GitHub/policy/receiver adapter is NOT implemented. Actual eligible 30-day denominator and verified autonomous numerator are UNKNOWN; real 90% achievement is NOT COMPUTABLE.

## Source and governance boundaries

Existing owner research path; no new root, workflow, agent stack, worker, model self-modification, private data, production/Hostinger write, external-actor registration, or claim promotion. R87 historical bytes remain untouched. GitHub branch publication does not imply PR/merge/main, scientific validation, or GitHub->WWW parity.

R10 secondary readback: PR #115 OPEN_NOT_MERGED, owner successor head dab7c59070d67e7e2a244bd6d05db9a4d37460e3; original requested source head 539d4bb33d2ba2c4895713c1bc437ece0743eeea. Detached manifest blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df; declared SHA-256 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc not independently recomputed in this read. PR reviews 0, PR conversation comments 0, Issue #93 comments 35 owner-only. No authenticated independent expert receiver ACK or actually executed new expert research established. Owner SEND != external RECEIVE.

BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET = NON_DESTRUCTIVE; C1_DESCRIPTIVE_ONLY.
