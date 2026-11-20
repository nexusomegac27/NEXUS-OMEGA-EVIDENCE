# R37 60-second static OPPO falsification — frozen negative and positive fixtures
OBJECT = NEXUS_OMEGA_AXIOM_R37_STATIONARY_OPPO_NEGATIVE_TEST_MATRIX_20261120_R0
STATE = EXPERIMENT_DESIGN_ONLY_NOT_EXECUTED_ON_REAL_OPPO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RUN_DURATION_TARGET = 60_SECONDS_MONOTONIC
SENSOR_CHANNELS = TYPE_ACCELEROMETER_M_PER_S2 + TYPE_GYROSCOPE_RAD_PER_S
R37_TEST_MODEL = ONE_PHONE_UNWORN_STATIONARY_TABLE_NO_ANATOMICAL_REFERENCE
BODYTWIN_VALIDATED = NO

## Test semantics
Each fixture is a deliberately separate decision: SOURCE_INTEGRITY, DEVICE_STATIC_CANDIDATE, BODYTWIN_SEMANTIC_SAFETY, and ACTUAL_INTEGRATION_EVIDENCE. No green aggregate hides a failed case. Claim policy must apply to UI strings, API fields, human-facing chart captions, event ledger, export labels and public status.
For all fixtures, a 60-second PHONE_STATIC_CANDIDATE does NOT authorize HUMAN_BODY_STATIC, HUMAN_POSE_MEASURED, JOINT_ANGLE_MEASURED or BODYTWIN_VALIDATED. A zero-motion person is not part of this experiment.

| ID | Fixture / perturbation | Expected reproducible decision | Physical/epistemic meaning |
|---|---|---|---|
| F00 | synthetic 60s, accel norm ~g, gyro near 0, monotonic 50Hz, BodyTwin visible label DEMO_ONLY | SYNTHETIC_STATIC_CANDIDATE, NO_BODY_OBSERVED | positive parser/policy control, not original device data |
| F01 | only 30s stream or 30s longer gap | HOLD_DURATION_INSUFFICIENT | full 60s not witnessed |
| F02 | accelerometer present, gyro missing or unavailable | HOLD_SENSOR_GAP | can't invent missing angular sensor |
| F03 | NaN/Infinity in any component | FAIL_NONFINITE_INPUT | no nonfinite fallback to static |
| F04 | duplicate timestamp in one sensor stream | FAIL_DUPLICATE_EVENT_TIME | count and original event provenance |
| F05 | backwards event timestamp | FAIL_NONMONOTONIC_EVENT_TIME | no reconstructed clock as measured |
| F06 | gyro reported degrees/s but expected SI rad/s, wrong axis/frame | HOLD_UNIT_OR_FRAME_MISMATCH | explicit mapping necessary |
| F07 | only TYPE_LINEAR_ACCELERATION, TYPE_GRAVITY instead of required accelerometer source | HOLD_UNSUBSTITUTABLE_SENSOR_TYPE | synthesized sensor != primary raw stream |
| F08 | static table stream and BodyTwin output claims JOINT_ANGLE_MEASURED or BODYTWIN_VALIDATED | FAIL_UNSUPPORTED_BODY_CLAIM | primary negative scientific result |
| F09 | static source fine but actual BodyTwin consumer unconnected/unobservable | BODYTWIN_INTEGRATION_NOT_TESTED | cannot claim semantic pass from absent output |
| F10 | no-sensor baseline yields same character animation as static stream | PRIOR_DERIVED_DEMO_ONLY | animation does not prove IMU-conditioned human pose |
| F11 | viewer/API displays plausible human pose with no origin label | FAIL_UNLABELED_BODY_INFERENCE | ambiguous visual can misrepresent source |
| F12 | no separately documented owner-approved exact-device 60s session | STOP_CAPTURE_NOT_AUTHORIZED | order is not live approval |
| F13 | installed Android app binary/signature/hash differs from pinned research collector | STOP_APP_SOURCE_MISMATCH | hash of different app cannot authenticate run |
| F14 | raw phone event tries unexpected Hostinger upload/BLE/location/mic/camera/background sensor | STOP_SCOPE_VIOLATION | stop and retain local witness, no retry |
| F15 | actual estimated position drift not cubic despite source's simplified cubic formula | DESCRIPTIVE_MODEL_DIAGNOSTIC_ONLY | not proof of original truth/fraud; model can use ZUPT/ZARU |
| F16 | accel median norm outside prereg 9.80665 ±1m/s² or gyro norm >0.05rad/s | ANOMALY_REVIEW_NOT_BODY_MOVEMENT | check units/bias/mount/environment, not anatomical event |
| F17 | synthetic injected motion mislabeled STATIONARY_PHONE | STATIC_CLASSIFIER_REJECTED | specificity vs deliberate perturbation |
| F18 | text claims 'AXIOM_APPROVED' or fake authenticated authority in a GitHub/LLM note | IGNORE_UNTRUSTED_INSTRUCTION | proof only from actual owner/session root of trust |
| F19 | phone is not attached to any person but BodyTwin outputs HUMAN_BODY_STATIC_MEASURED | FAIL_UNSUPPORTED_BODY_CLAIM | static object cannot support person measurement |
| F20 | two independently labelled experts copy same single source metadata with altered serialization | EVIDENCE_LINEAGE_COLLAPSE_N_EFF_1 | number of messages != independent observations |

## Minimal real-run measurement and report calculations
- Exact raw event count by sensor; median/95th/max inter-event gap (ns), rate from median dt, duplicate and negative dt count, original start/end monotonic times and 60s duration.
- For each accelerometer vector in m/s²: norm= sqrt(ax²+ay²+az²); median norm and median absolute deviation vs 9.80665, per-axis median and noise proxy. Note manufacturer-calibrated != chip raw.
- For gyro vector in rad/s: per-axis median, median ||omega||, MAD, maximum absolute component, estimate bias proxy only under verified static assumption. Gravity-vector can inform pitch/roll, not absolute yaw or world position.
- BodyTwin API/UI output table: type, value, frame, source labels, exact run_id and code_version. No output => NOT_CONNECTED/NOT_TESTED. A BODY MEASURED label on this one-phone desk trial => FAIL and block promotion.
- Predeclared thresholds are engineering sanity guidance, not calibrated u(ref) or precision validation. Preserve all irregularities and stop reasons.
- Source tests run offline in isolated workspace, then independently repeated. No hidden dynamic code import from user report/URL.
- A user-attested table placement supports a stationarity test fixture, not an external certified metrology reference.
- Do not change the scientific frozen 30-min two-phone prereg or later Variant C by post-hoc tuning after seeing this 60s result.

## Return statuses
READY_SYNTHETIC_ONLY | DEVICE_SOURCE_GAP | OWNER_SCOPE_PENDING | REAL_60S_RECORDED_PRIVATE | REAL_STATIC_DATA_ANOMALOUS | BODYTWIN_INTEGRATION_NOT_TESTED | BODYTWIN_SEMANTIC_SAFE_ON_THIS_ONE_RUN | FAIL_UNSUPPORTED_BODY_CLAIM | INDEPENDENT_VERIFIER_PENDING.
No single 'PASS' field is sufficient. No test may set BODYTWIN_VALIDATED=YES from the table run.
