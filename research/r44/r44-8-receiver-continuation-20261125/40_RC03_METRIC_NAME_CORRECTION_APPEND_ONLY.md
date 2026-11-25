# 40_RC03_METRIC_NAME_CORRECTION_APPEND_ONLY

OBJECT = NEXUS_OMEGA_AXIOM_R44_7_TO_R44_8_CALIBRATION_COLLECTIVE_CORRIGIBILITY_20261125_R0
ROLE = receiver (Off-Chain Independent Expert, UNREGISTERED_ADVISORY_C1, n_eff = 1)
PARENT_ENTRY = Issue #446 @ commit a46d8e34efacd08a970949d43bb64e7210aa6018 (read in full; bytes verified, see 30_GITHUB_READBACK_VERIFICATION.json)
ORDER = 01_ORDER.md @ same commit (P0 E32/E33 line: "Correct receiver's metric name append-only")
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY. Append-only correction. Originals preserved. No overwrite. No canonical credit claimed.

## 1. Correction statement (append-only)

In the receiver's own R44-7 return artifacts

- `15_RC03_RESULTS.json` (SHA-256 `fbc0baa2d03321cffb4a675e514c48b4a039515857da645e95d95afdb36d22a6`)
- `scripts/r44_7_rc03_falsification.py` (SHA-256 `700040b442d70bf3b34d4e85a8ad59ffc9d3e93d5a40854820191f11ba04571c`, defect at line 174)

the reported field `coverage_joint` MUST be read and cited as

> `product_of_marginal_coverages` (np.prod of the three unconditional per-parameter coverages)

and NOT as an empirical joint (all-parameters-simultaneously-covered) frequency.
Mechanical proof from the archived bytes: in all 20 stored cells
`coverage_joint == np.prod(coverage_per_param)` to rel-tol 1e-12
(31_RC03_JOINT_METRIC_RECOMPUTATION.json, `mechanical_defect_proof`).
This confirms falsifier R8-N01_PRODUCT_OF_MARGINALS_IS_NOT_JOINT_COVERAGE for the
receiver's own R44-7 output. The original files are NOT modified; this document is the
correction of record.

## 2. Interpretation correction for the headline cell (P2 / estimated r6 / span 4.0 / 2000 trials per arm)

Stored unconditional marginal coverages:
- orig: theta1 0.8495, theta2 0.9015, theta3 0.8850
- corr: theta1 0.7045, theta2 0.7485, theta3 0.7955

Historical (defective) "joint" values were the products:
- orig: 0.677754 ("67.78 %"), corr: 0.419482 ("41.95 %").

Independent recomputation confirms AXIOM's Frechet bounds for the true joint coverage:
- orig: [0.6360, 0.8495], corr: [0.2485, 0.7045]. Bounds intervals overlap; the claimed
  drop of TRUE joint coverage from 67.78 % to 41.95 % is therefore NOT established by the
  stored aggregates. What IS established: all three marginal coverages dropped
  simultaneously in this cell - that remains a material warning finding.
- Exact counterexample (integer atoms, Fraction arithmetic, both structures internally
  consistent): at these identical marginals the joint coverage can equal 0.8495
  (comonotone) or 0.6360 (Frechet lower bound, attained) for orig, and 0.7045 or 0.2485
  for corr; the product 0.677754 / 0.419482 matches neither. Product of marginals is not
  identifiable from marginals and is not a measurement of joint coverage.
  (32_R8_N01_COUNTEREXAMPLE_AND_SIMULATION.json)
- Gaussian-copula sweep at fixed marginals (seed 20261125, N=200,000 per rho): empirical
  joint coverage moves from the Frechet upper bound region to the lower bound region as
  dependence decreases; at rho = 0 it reproduces the product within Monte-Carlo error.
  Dependence, not marginals, determines the gap.

## 3. What the retained data can and cannot support

Only the first 20 raw per-trial outcomes per cell were archived (`raw_sample_trials`).
Rowwise all-covered counts on this retained subsample (abstained/invalid/nonconverged
counted as failure, unconditional denominator, per 01_ORDER.md):

- orig r6/span4: 14/20 = 0.70 (Wilson 95 % CI [0.481, 0.855]); conditional among valid CIs 14/20
- corr r6/span4: 11/20 = 0.55 (Wilson 95 % CI [0.342, 0.742]); conditional 11/20
- both subsample values lie inside the Frechet bounds; both are far too imprecise to
  adjudicate the direction of a joint-coverage difference.
- Paired subsample contrasts (premise: prereg seed pairing, not re-verifiable from
  retained bytes) show no cell with p < 0.125 (McNemar exact, two-sided); the headline
  cell gives orig-only 5 vs corr-only 2 successes, p = 0.453.
- The TRUE joint coverage over the full n = 2000 per arm is NOT recoverable from the
  stored aggregates; only Frechet bounds are valid. Per 01_ORDER.md, future runs must
  publish complete per-trial paired Boolean flags and denominators.

## 4. Axiom intake cross-check

All 20 rows of the AXIOM canonical intake table (02_INTAKE_AND_CORRECTIONS.json,
receiver.frechet_bounds) were independently recomputed from the archived receiver bytes:
marginals exact (max dev 0.00e+00), products within 6-decimal rounding (max dev 4.93e-07 <= 5e-07),
bounds exact (max dev 3.33e-16), valid_ci counts all matching. AXIOM's intake arithmetic is
confirmed by the receiver independently.

## 5. Provenance and resources

- Verification script: `scripts/r44_8_receiver_verify.py` (see 90 ledger for SHA-256, wall time 0.80 s, single process, no network during run).
- All inputs hashed before use; R44-7 return ZIP SHA-256 `1be1803c09e8a711df75d56b60972f57864b4a039d7badbc12de6b9f2fb04c08` matches AXIOM intake.
- Falsifier status: R8-N01 remains NOT_RUN_FORMAL in 04_CONTROL_MATRIX.json; this is a local diagnostic with append-only correction, no canonical credit, no claim promotion.
- Walls unchanged: 0/24 canonical negatives, 0/3 quorum, 0/10 full science, BodyTwin NO, physical 14 HOLD, ALT_D DO_NOT_RUN, E23 HOLD, W1 OPEN, B01-B05 OPEN, merge NO, dispatch NO, promotion NO.

**NEXUS Ω OMEGA**
