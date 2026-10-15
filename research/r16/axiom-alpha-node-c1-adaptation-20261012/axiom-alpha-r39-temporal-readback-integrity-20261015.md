# NEXUS OMEGA · AXIOM Alpha-Node R39 · Temporal readback integrity (C1)

```text
OBJECT = NEXUS_OMEGA_AXIOM_R39_TEMPORAL_READBACK_INTEGRITY_20261015_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_R38_TRANSPORT_AND_MAIN_READBACK_RECEIPT_20261015_R0
PREDECESSOR_RECEIPT_SHA256 = 7209d59d5cc1df8f72369b37018bbb4280331b2d2a345ecb23577df479ce45ab
PREDECESSOR_ZIP_SHA256 = 66a0721029ba2904259860a48a11137a04020e86ee1cd59ffa9f448a45410b8e
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
DECISION = TESTED_IMPROVEMENT_CANDIDATE_NOT_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## OBSERVE / ORIGINAL_BYTES
Direct GitHub connector read: main commit `d355400dabed3c280e1fce5030cab69ea099428b`; AGENTS.md Git blob `f24f7cf557927016860279b65d0725275e6270a9`, GOVERNANCE.md `b630b62eb9800e2f57b6c86318c72faadb29c23b`, Alpha-Node R0 `f8adcf6df22bba526c17dbff72b7ad494b42c63e`, operator publication rule `a99e6fc7c71cbf82bdfdd9cf414b44a362073ce8`, Task Anchor Norm `51c97b624f14fe9c3f1dfe1bf13394a773f87935`, Repository Steward V1 `c8f79915e9085d83335c33b2a0dd5407970e4a31`. Git SHA-1 is not an independently computed SHA-256 byte witness. Issue #93 had 19 comments, last ID `6137726458`. The external write-slot actor allowlist was empty.

Physically mounted R38 package: **17,499 bytes**, SHA-256 `66a0721029ba2904259860a48a11137a04020e86ee1cd59ffa9f448a45410b8e`; **12/12** manifest entries rehashed. Physically mounted R38 receipt: **2,988 bytes**, SHA-256 `7209d59d5cc1df8f72369b37018bbb4280331b2d2a345ecb23577df479ce45ab`.

## NEGATIVE_HYPOTHESIS / FALSIFIER
R38 permits a metadata readback timestamp later than the real audit clock and a future-ended measurement period. On a synthetic readback timestamped `2099-01-01T00:00:00Z`, R38 reports `receipt_shaped_without_nudge=1/1`; R39 reports **0/1**, `main_future_dated_readback=1` and `main_missing_complete_readback=1`. On a synthetic period ending in 2099, R38 returns success, while R39 returns `HOLD_SCOPED/FUTURE_PERIOD_END_NOT_OBSERVED`.

A legitimate delayed readback can occur after the measurement period. R39 therefore permits `verified_at_utc > period_end_utc` if it precedes the observed audit clock. The local system clock is **not an authenticated external time source**.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST
A separate black-box evaluator was frozen *before* candidate modification; SHA-256 `f5f52a15e9edd50e1e55c6cd153dc576e644d6c82849dedb9f0755de471a2e03`. It launches subprocesses, never imports candidate logic, and uses synthetic positive and negative fixtures. R38 baseline: **9/16 PASS** (six assertion failures, one error). R39: **16/16 PASS** on the unchanged evaluator; **20/20 PASS** on the unchanged historical R38 evaluator. Candidate SHA-256: `e7048569f05a5f91a041a3060532a9122d2356f7016428bc46b551a91265bdc4`.

Falsify by demonstrating an accepted future-dated readback, accepted future-ended period, or rejection of a legitimate delayed historical readback. This is isolated local verification, **not** external third-party acceptance, GitHub authentication, or productive integration.

## DECISION / METRICS
`TESTED_IMPROVEMENT_CANDIDATE` applies only to the read-only metadata classifier. Historical handoff receipts reported: **10**; independently confirmed eligible preflights: **0**, not a denominator of zero. Actual eligible 30-day denominator and verified autonomous numerator: **UNKNOWN**; >=90% target **NOT_COMPUTABLE**. This local test published **0** main changes; 0/0 main readback fraction is undefined. No new pipeline, runtime mutation, Hostinger deployment, external write-slot change, evaluator promotion, model-weight change, or node reset. GitHub->WWW parity **NOT_ESTABLISHED**.

Local replay materials include original R38 bytes, frozen evaluators, R39 candidate, physical negative fixtures, and test logs; the local package is a separate artifact and is **not** implied to be on GitHub. Branch-only publication, if any, is not a main merge. Preserve all historical negatives and C1 caveats.
