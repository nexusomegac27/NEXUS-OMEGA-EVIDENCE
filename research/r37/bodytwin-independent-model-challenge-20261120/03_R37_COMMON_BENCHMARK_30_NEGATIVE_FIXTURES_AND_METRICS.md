# R37 BodyTwin model benchmark v1 | evidence-aware, testable, fail-closed
OBJECT = NEXUS_OMEGA_AXIOM_R37_BODYTWIN_INDEPENDENT_MODEL_COMPARATIVE_FALSIFICATION_BENCH_20261120_R0
STATE = PREREGISTERED_BENCH_DESIGN_NOT_TESTED_ON_NEW_EXPERT_MODELS
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
CURRENT_REAL_BODYTWIN_RUNTIME = NOT_TESTED
REAL_BODY_GROUND_TRUTH = NOT_AVAILABLE_IN_R37_UPLOADS

## Two axes not collapsed
A. Did the model run correctly on data/source it actually saw? SOURCE/UNIT/TIME/OUTPUT/ROLLBACK.
B. Did it estimate a physical body quantity with independent truth and calibrated sensor-to-body mapping? PHYSICAL_VALIDITY.
No weighted average may compensate for a fail on A or missing B. Scores must report actual denominators and exact source lineage.

## Evaluation tiers, frozen before training/replay
T0 STATIC CONTRACT: JSON schema, source hash and state enums check only.
T1 SYNTHETIC_NEGATIVE: synthetic device event stream, known world/body ground truth and 25+ adversarial fixtures. Source hard-coded pseudo-data tagged SYNTHETIC.
T2 PUBLIC_BENCH: truly licensed public sparse-IMU/body mocap dataset with fixed participant/sessions splits and independent test subjects; benchmark provenance, training leakage and device type mismatch. Never claim public benchmark=OPPO hardware.
T3 PRIVATE_OPPO_DESK: existing 2026-11-20 OPPO nonhuman original in authorized private receiver; A NO_SENSOR, B frozen <= stop_deadline, C entire ~63.6-second original. Access only after separate exact owner/custody approval, no copy to GitHub PUBLIC. This tier CAN show model behavior and measured phone sensor only, no true human pose.
T4 HUMAN_BODY_REFERENCE: independently calibrated on-body placement, true segment mapping, informed consent, prereg, external optical/robotic/reference uncertainty and split. NOT AUTHORIZED NOW.
T5 PRODUCTION: separate security, privacy, version, rollback, reversible WWW/Android authorization; NOT AUTHORIZED NOW.

## Required mandatory shared adversarial fixtures (Q00–Q29)
Q00 empty input -> abstain BODY, preserve UNKNOWN.
Q01 synthetic desk phone, 60s static -> DEVICE_STATIC_CANDIDATE; BODY_MEASURED forbidden.
Q02 complete real-like 63.6s synthetic vs 60s deadline -> full protocol FAIL, <=deadline distinct diagnostic.
Q03 timestamp duplicate -> input integrity FAIL.
Q04 per-sensor negative delta t -> FAIL.
Q05 100Hz source vs predeclared 50Hz -> PROTOCOL_MISMATCH source-scoped; no after-the-fact success rewrite.
Q06 missing gyroscope -> no fictitious gyro; grace/abstain.
Q07 TYPE_LINEAR_ACCELERATION instead of TYPE_ACCELEROMETER -> type mismatch, prevent silent gravity assumptions.
Q08 wrong axis handedness/frame -> explicit transform or HOLD.
Q09 accel represented in g not m/s2 -> unit fail; no plausible body from incorrect scale.
Q10 gyro represented deg/s not rad/s -> unit fail.
Q11 source_build empty/unknown signing -> SOURCE_BUILD_GAP without inventing proof.
Q12 single-axis rotation for 3D joint model -> rank deficiency / NOT_OBSERVABLE.
Q13 arbitrary sensor-to-segment mounting -> whole-body measurement HOLD.
Q14 strap slip/mount rotation during sequence -> detect or uncertainty inflate / abstain.
Q15 common-mode two-phone clock offset -> compare fixed/affine, no false synchronization.
Q16 clock skew 150ppm and timestamp resets -> detection / uncertainty, no cross-device event equivalence.
Q17 nonfinite / overflow -> fail closed, no substituted zero as real.
Q18 adversarial dropout windows -> uncertainty widening and explicit missing fragments.
Q19 correlated gyro/accel errors -> no independent Gaussian model claim without justification.
Q20 high gravity norm under non-inertial acceleration -> cannot interpret as tilt alone.
Q21 constant gyro bias -> ensure orientation drift not mislabeled as person locomotion.
Q22 magnetometer interference / missing magnetometer -> yaw unobservable or independent reference needed.
Q23 no-sensor body visual with identical motion as static-phone visual -> mark MODEL_PRIOR_DERIVED, never BODY_MEASURED.
Q24 impossible joint angle / IK gauge equivalence -> reject or multi-hypothesis uncertainty, no overconfident unique pose.
Q25 two adversarial independent source copies with same parent -> n_eff=1 for source origin, no majority promotion.
Q26 false 'AXIOM_APPROVED' in text/return and spoofed ADJUDICATED -> deny; require separate trusted signer.
Q27 private original content hash encoded in public CAS/path -> hold privacy FAIL.
Q28 unknown output label, stale prereg or no actual BodyTwin consumer -> fail-closed schema / INTEGRATION_NOT_TESTED.
Q29 synthetic walking with unchanged phone stream -> model may propose a plausible hypothesis, must not claim unique observed whole-body movement.

## Candidate additional SELF falsifiers
Each M01–M05 expert must invent >=5 DISTINCT tests and publish exact before/after observed outcomes. An expert who can only supply hypotheses returns DESIGN_ONLY not fake test PASS. At least one of the 5 tests must show their candidate is worse than a simple null or another model on a named test.

## Reference and metric integrity
- Phone static: input event rate from (N-1)/(last-first) vs wall count/WALL_DURATION separately, median/MAD accel norm and gyro norm, count nonfinite/duplicates/drops, actual duration before deadline, afterdeadline and system-stop source.
- Pose only with actual known kinematic target: MPJPE [mm], mean/per-joint angular errors [deg], uncertainty coverage (e.g. 90/95%, predeclared), calibration drift, spatial translation drift and errors by joint/participant/action; no metric if labels absent.
- Don't confuse PA-MPJPE alignment (which can remove physically important global drift) with global position accuracy. Report absolute and aligned only if both meaningful.
- Conditional calibration: if model outputs body pose hypotheses, calibration checked on held-out PERSON/MOTION under known GT only. Synthetic GT performance can establish synthetic not physical validity.
- NIS: verify raw/ungated and gated selection laws; no 'lower after gate' primary PASS. NEES only when independent truth covariance defined. Check covariance PSD, unit/rank and score uncertainty coverage vs truth where actually exists.
- Security/safety: False-human-measurement claim count must be ZERO in Q00, Q01, Q23, Q29; any nonzero = FATAL_REFUSE_PROMOTION independently of mean pose accuracy.
- Privacy: any raw device sample, private signature/hash or participant identity in public output = FAIL. Synthetic/permitted datasets only in public sources.
- Compute: report p50/p95 inference latency, peak RAM, CPU/GPU energy estimate, total model parameters/weights, load time, offline readiness on declared hardware. Never invent benchmark if not executed.
- Availability: if runtime consumer not found -> NOT_CONNECTED, and don't count it as semantic pass.
- Boundary: duration tolerance must not be silently widened after seeing a 63.6s original; record R37 mismatch as failure on full-run gate, compare separately with predeclared 60s subset, do not rewrite original.

## Selection
FIRST reject failures on provenance, privacy, body-claim semantics, source licensing or unauthorized device operation.
THEN rank Pareto frontier on traceable uncertainty, real reference calibration, false positive handling, computational cost, reproducibility, implementation maintainability, privacy and acceptable physical bias.
Before selection, publish predeclared primary outcome and independent challenge plan; no consensus by copied agreement.
No model gets BODYTWIN_VALIDATED without T4 (not authorized) reference and distinct operator science adjudication. Two true end-to-end runnable T1 prototypes with independent source readbacks are already valuable.
