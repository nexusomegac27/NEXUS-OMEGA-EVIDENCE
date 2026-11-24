# R44-0 experimental prereg and discriminating test plan

**Primary estimand**: improvement in an explicitly defined observable kinematic function of two smartphone signals relative to the best single phone, at matched deployable input/energy/compute/latency budget, independent reference, correct cross covariance and group holdout. If exact two-phone physical original data absent -> `NOT_RUN`, no synthetic substitution of original experimental proof.

## Four pillars
**Pillar A — original/source trust**: real time/source identity, 370/374 trial IDs and license, true data bytes; negative wrong license/corrupt sample/generic HTTP200; 10 original Subject logs from MHEALTH cannot prove dual-phone equivalence. Final 12-file receipt must match current outer ZIP and sidecar without self-referential cycling.

**Pillar B — target-observation identifiability**: independent equal-noise same mount gain `I(AB)=2/(1+rho)` for unit-variance bivariate Gaussian (rho0=2, rho.5=1.333, rho.9≈1.053) without claiming real device gain; identified sum θ1+θ2 vs unidentifiable difference, prior-only nullspace and one shared prior, unit scaling θ→10^6θ flips naive raw eigenvalue thresholds, local rank does not imply global unique θ; static gravity doesn't identify yaw. `ABSTAIN` per target, not whole state if relevant target observable; predeclared threshold/risk curve required.

**Pillar C — fair information nulls**: single phone A, single phone B, naive avg, inverse-covariance fusion, difference, sensor permutation, correlated Gaussian null, mismatch clock/mount reference shift, over-wide interval baseline and no-reference inference. Truth in test model input forbidden unless explicitly marked and scored as `REFERENCE_ORACLE` not deployable.

**Pillar D — independent results**: fresh leave-subject / leave-mount / leave-phone / leave-day holdouts, multiple proper scoring endpoints (WIS/quantile/calibration + width + directional bias + RMSE), coverage stratified and confidence intervals by independent unit (not row), resource actual wall/CPU/tokens/network, authentic external evaluator, no after-the-fact metric switching or privacy leakage.

## Adversarial failures to include
M9 original full 16 according PR425, B02 local alias collision, B03 omitted PDF, B04 fake evaluator identity/partial holdout overlap, B05 embedded preappend receipt mismatch and external seal integrity, source Q1 not a dataset, FDA 370/374 contradiction. A positive-control equivalent original Q4+runtime independently replayed if data permitted, distinct from 0/10 full science gates.

## Boundaries
P01–P10 0/10 full passes, independent authentic actors 0/3, physical14 hold, ALT_D active, E23 privacy hold, no actual dual-phone clinical/kinematic correctness, no production model tuning, no exploit/captcha bypass. This is DESIGN_RESEARCH_ONLY until original receipts.
