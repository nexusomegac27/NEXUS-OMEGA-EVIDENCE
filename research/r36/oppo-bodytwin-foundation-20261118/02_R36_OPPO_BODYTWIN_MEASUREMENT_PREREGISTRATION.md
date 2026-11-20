# R36 OPPO CPH2219 / BODYTWIN measurement preregistration candidate
OBJECT = NEXUS_OMEGA_AXIOM_R36_OPPO_BODYTWIN_PREREGISTRATION_AND_IDENTIFIABILITY_20261118_R0
STATUS = PREREGISTRATION_CANDIDATE_NOT_EXECUTED
CLAIM = C1_DESCRIPTIVE_ONLY
REAL_DEVICE_CAPTURE = NOT_AUTHORIZED_BY_THIS_DOCUMENT
PHYSICAL_REFERENCE = NOT_ESTABLISHED
CONSENT_BIND = OPEN

## Main question and nulls
Do two specifically censused Android phones including OPPO CPH2219 permit a restricted, reproducible claim about sensor/event timing and calibrated DEVICE relative orientation, beyond null models, under explicit clock offset/skew, sensor bias and axes? Do they establish body kinematics? No unless a separately validated rigid sensor-to-segment mapping and independent body reference are obtained.

H00 minimal: reported sensor values + event times only, no orientation/trajectory reconstruction.
H01 direct gyro integration with precharacterized bias; orientation errors accumulate over intervals.
H02 complementary/gravity constrained orientation under valid acceleration assumptions; yaw/unobservable degrees remain explicit.
H03 UKF/SR-UKF orientation+gyro bias, identical raw inputs and predeclared Q/R process model.
H04 batch factor graph / joint clock+extrinsic model; penalize complexity unless heldout test improves over H01-H03.
Clock C0 fixed offset, C1 affine t2=alpha*t1+beta, C2 bounded piecewise/nonlinear drift. Complexity chosen on withheld data and independently observed timing reference, not fitted residual alone.

## Evidence/data gates in order
G0 PRIVATE CUSTODY: Reconcile preexisting R1-R27 private OPPO anchor and the reported R21 original; verify exact raw ZIP locally inside private storage, no substitution with older 0033/0034/0103 or synthetic sessions. If absent label SOURCE_GAP; never upload to public research PR. Distinguish historic Cursor-reported device census from actual new on-device metadata.
G1 DEVICE/APP CENSUS: Read-only, user-visible approved status inventory: sensor type/vendor/version/resolution/range/minDelay, calibrated/uncalibrated variant, Android build/SDK, app source/build/signing fingerprint, event timestamp clock, sampling/batching/drop/dedup, local timebase; independent source receipts. No continuous capture or ADB dependency.
G2 TIMING: On a physically constrained stationary/repeated-motion rig (if separately approved), use independent reference pulses over full recording window including after reboot/network/batching changes. Separate clock offset, skew, sensor-processing latency and packet-delivery latency. Require identifiability rank/singular-value and heldout residual vs C0/C1/C2.
G3 INTRINSIC CALIBRATION: Static multi-orientation checks with independent orientation/gravimetric reference; estimate bias, gravity inclusion, axis permutations, scale and temperature dependence; Allan deviation only at stable sampling and durations sufficient for each term. Report when a noise component is unidentifiable.
G4 EXTRINSIC/RIGID: Two phones securely mounted with known and varied relative rotation; exercise noncollinear axes, noncommutative rotations, distinct frequencies; detect rank deficiency, symmetry ambiguity and pseudo-perfect residuals from degenerate motion. Use independent calibrated angle/time reference.
G5 ESTIMATORS: Apply null, gyro, complementary, SR-UKF and graph if warranted to identical sealed source bytes. Freeze train/test by session and physical placement BEFORE fitting. Report geodesic SO(3) orientation error with 95th percentile CI, time error in ms, error covariance, gaps/batching and calibration stability. Numeric thresholds based on scientific use case and independent reference uncertainty must be registered pre-data, never tuned after results.
G6 DIAGNOSTICS: Compute ungated and gated NIS with df, accept/reject proportions and conditional reference distributions, plus NEES only when actual state reference is known. Gating can artificially contract NIS under matched model; never use NIS_mean~=1 as sole validity. Include non-Gaussian/correlated noise, bias drift, covariance under/overconfidence, sensor saturation adversaries.
G7 DEVICE-TO-BODY: Source is phone frame, not joint frame. Test placement rotation, strap slip, rigid/nonrigid attachment, segment offsets and observability, using separate calibrated body reference and approved consent. Until these pass: BODYTWIN is synthetically illustrative and only device-level claims allowed.
G8 REPLICATION: At least two independent source-aware reviewers run authentic source/binary/toolchain/fixtures and check SHA-256, uncertainty model, heldout thresholds, failed negative controls, original received ACK. Synthetic results do not count as independent real device evidence.
G9 PUBLICATION: Public-safe C1 release only of separately adjudicated descriptive summaries with changed-source manifest, causal predecessor and explicit LIMITATIONS; private sensor streams/identifiers remain segregated. WWW rollouts separately authorized; new PASS never deletes historic FAIL.

## Expected physical falsifiers
F1 periodic single-axis motion yields ambiguous extrinsic/time parameters; return NOT_IDENTIFIABLE.
F2 deliberate clock skew with fixed-offset model creates growing heldout timing error.
F3 Android HAL batching causes receipt delay without guaranteed timestamp drift; separate event time from delivery time.
F4 cross-placement orientation estimate degrades due to sensor-to-segment mismatch.
F5 accelerometer dominated by non-gravitational acceleration invalidates naive gravity tilt update.
F6 post-gate NIS can fall even if Q/R mismatched; crosscheck independent trajectory/error reference.
F7 no independent reference -> no accuracy/NEES claim.
F8 absent consent -> no human-body trial, regardless of prospective gain.
F9 original session hash missing -> no ORIGINAL_SOURCE_PASS.
F10 positive fixture alone -> cannot promote physical validity.

## Metrological documentation
Use Android official SensorEvent and AOSP sensor HAL/type semantics, JCGM 100:2008 + 2026 nonlinearity amendment, JCGM 101 Monte Carlo propagation when appropriate. Keep units, raw/preprocessed semantics, time and spatial frames, reference instrument calibration, type-A/B uncertainty, reference traceability, model/selection assumptions, sampling plan and precommitted stop rules.
