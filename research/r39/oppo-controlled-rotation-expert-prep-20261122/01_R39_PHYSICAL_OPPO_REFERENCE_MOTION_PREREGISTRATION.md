# R39 prereg — dual-axis controlled PHONE motion, not body validation
OBJECT = NEXUS_OMEGA_AXIOM_R39_OPPO_REFERENCE_RIG_STATIC_TILT_YAW_PHYSICAL_NEGATIVE_PRE_REG_20261122_R0
DESIGN_CLASS = C1_EXPERIMENT_CANDIDATE_BEFORE_INDEPENDENT_METHOD_ADJUDICATION
PHYSICAL_TEST = NOT_AUTHORIZED_NOT_RUN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PRIMARY_CONFOUNDERS = SOURCE_BUILD_OWNER_SCOPE_CLOCK_STOP_RATE_MOUNTING_ANGLE_REFERENCE
TARGET_DEVICE = OPPO CPH2219 (source-reported old R37 identity; independently reconfirm on future approved local run)
HUMAN_BODY = NO

## Core question and falsifiable nulls
Q1 Does actual phone inertial signal change consistently with a separately observed rigid-fixture tilt?
Q2 Does a yaw rotation around gravity produce measurable relative integrated angular change but remain insufficient to establish absolute heading from accelerometer+gyro alone?
Q3 Does existing BodyTwin (if actually connected) abstain from asserting physical HUMAN_BODY_MEASURED/JOINT_ANGLE_MEASURED for an unmounted fixture phone?
Q4 Do app/source, physical motion segments, wall/event clock, strict stop deadline and real receiver ACK match the exact frozen prereg instead of an after-the-fact retrofit?
H0-PHONE-STATIONARY: null model source stays still; tilt/turn segments differ only if actual independent physical actuation occurs.
H0-NO-BODY: no body/segment reference, no scientifically defensible human joint measurement in ANY segment.
H0-YAW-ABS-UNOBSERVABLE: gyro integrated relative yaw may be estimated under assumed initial heading and bias, but no independently absolute heading with just acc+gyro; calibration and magnetometer presence clearly declared.

## Default provisional fixture proposal, not preauthorized fixed duration
Test rig holds the phone securely without an instrumented human, no wrist/body straps, no uncontrolled drops, battery charging hazards or use near people. A reference angular scale/optical marker is recorded offline with its calibration, uncertainty and time registration; if it is only a printed or manually read protractor, report a coarse nominal angle with limited uncertainty rather than a metrological 90.000° truth. Record axis/right-handedness and orientation of phone in sensor frame.
One trial may be split into TWO independent blocks; final timings are design candidates frozen by reviewers BEFORE execution:
TRIAL A GRAVITY-SENSITIVE ROLL: stationary-before (e.g. 15s), commanded ~90° roll with recorded actual transition, stationary-after (e.g. 15s), return to start, stationary-after-return. No claims of exact transition time unless measured independently. Assess gravity-vector component change, gyro integrated relative angle, back-to-start residual and covariance.
TRIAL B YAW AROUND GRAVITY: stationary-before, ~90° yaw of level fixture on turntable, stationary-after, return to start. Assess gyro relative yaw under bias uncertainty, gravity invariance; abstain on absolute yaw without suitable external directional reference. Other sensors (magnetometer/rotation vector) are NOT silently present; if enabled, report a separate instrument class.
Each trial has a separately scoped one-shot operator permit and stop; NO automatic chained next run. The earlier R37 stop-deadline overrun (~3.622s, 363 late events per channel) must have a source-exact repair and cold-run regression before any trial.

## Physical metrics and uncertainty
Collect per-sensor SOURCE timestamp ns, reporting wall time separately, sampling requested/actual and changed rate; nonfinite, backward, duplicate, gap count, FIFO/report latency, stop deadline and tail events, clock alignment with reference, build/signing and consent witness. Rate in events/sec from (N-1)/(last-first), separately N/wall.
Define estimates, not posthoc truth: (a) median gravity magnitude with MAD in static windows (b) gyro median magnitude/noise in static windows (c) calibrated direction/gravity tilt difference with sign conventions and intrinsic estimated uncertainty (d) relative gyro angle and return residual with uncertainty (e) observed latency/truncation versus event deadline (f) angular reference provenance uncertainty, human operator marking error and mechanical slippage.
Primary causal contrast: each motion window vs its own stationary null and independent reference. No NEES without true independently calibrated state; no claim that lower gated NIS alone validates filter; no true anatomical MPJPE from unmounted phone.
Intended conclusions tier DEVICE_SOURCE_OBSERVED / DEVICE_ORIENTATION_ESTIMATED / REFERENCE_ANGLE_CONSISTENT_C1 / SOURCE_OR_METHOD_GAP / WRONG_UNSUPPORTED_BODY_CLAIM. Full body not validated by physical rig.

## Mandatory objective pass/fail structure, no invented thresholds
G0 exact approved prereg independent witness.
G1 app runtime genuine source/build & Android sensor channel census, no unknown model output as authority.
G2 owner approval exact device/sensors/duration/records recipients and explicit stop.
G3 stop deadline regression measured in offline harness before any live run, real physical stop witness afterward.
G4 independently documented mechanical fixture axis, angle and uncertainty; no printed degree assumed certified.
G5 sensor units and monotonic clock, sampling spec and event vs wall measured at source, no silent 50→100Hz reinterpretation.
G6 minimal-no-body semantic gate hard FAIL on false human body measurement.
G7 actual original hash from OPPO to local to private receiver, plus independent second actor rehash before public inference.
G8 source/method distinction and checked negative/positive fixtures.
G9 privacy/rollback/kill and no auto redeploy.
A pass must be source-exact for the gate and never averaged across other gates. A future physical trial can yield a valuable negative, and remains C1.

## Alternative protocols required from external experts
ALT-A one axis 90° gravity roll low setup/short source; ALT-B yaw absolute unobservability; ALT-C calibrated known-axis tilt ± angles under controlled source; ALT-D no new capture if source/build/deadline/consent unresolved. Compare costs, time, independent reference accuracy and expected information gain; specialists can recommend not to run.
