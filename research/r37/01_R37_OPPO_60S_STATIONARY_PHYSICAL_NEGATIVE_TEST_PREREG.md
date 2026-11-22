# R37 P0 — OPPO 60 s stationary-table negative control: frozen research preregistration
OBJECT = NEXUS_OMEGA_AXIOM_R37_OPPO_TABLE_STATIC_60S_PREREG_20261120_R0
STATE = PROTOCOL_FROZEN_AS_RESEARCH_DESIGN_NO_LIVE_CAPTURE_YET
PRIMARY_NULL = H0_PHONE_IS_STATIONARY_AND_NO_BODY_IS_OBSERVED
ALTERNATIVE = H1_BODYTWIN_ASSERTS_ANATOMIC_MEASUREMENT_FROM_PHONE_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED = NO
R36_SOURCE_LINEAGE = APPEND_ONLY
REAL_CAPTURE = REQUIRE_EXACT_OWNER_APPROVAL_AND_INSTALLED_SOURCE_CENSUS
NONHUMAN_TABLE_FIXTURE_ONLY = YES

## Precondition sequence — each gate independent, no implied permission
G0 SOURCE: original installed NEXUS app source/version/certificate and actual OPPO hardware identity; if missing source, classify SOURCE_GAP, never substitute R21 narrative. Allowed to use available trusted Android SensorManager app without installing a novel APK ONLY after reviewing owner-approved read-only scope.
G1 USER: local, owner-visible scoped START/STOP for EXACT OPPO, EXACT app, sensors {accelerometer, gyroscope}, EXACT 60s, local-only output; no human body, GPS, camera, mic, BLE tracking, advertising ID or health inference. Consent for future human sessions is separate and OPEN.
G2 FIXTURE: OPPO lying untouched on stable table with orientation noted before run, no human attached; observer notes setup (simple textual statement; optional photo only if separately approved). Start and end based on Android monotonic elapsedRealtimeNanos, not network wall clock. Mark operator-observed static fixture and ambient vibration uncertainty, not laboratory certified absolute stillness.
G3 COLLECTION: request 50Hz ACCELEROMETER and GYROSCOPE if actually available, no high-rate permission assumptions; actual event rates from event timestamps. Capture exactly one user-visible elapsed 60s run. Collect per event: source type, event timestamp_ns, SI vector[3], Sensor accuracy, dropped/nonmonotonic/duplicate event counters, source app hash, sensor name/vendor/version/range/resolution/minDelay, Android build, run id, actual start/stop times. Record OS calibration state; no claim of truly chip-raw ADC. If no gyro or app unavailable => SENSOR_GAP/HOLD; never fabricate.
G4 PRIVATE PRESERVATION: local file sealed with sha256 and byte count, owner preview/kill; NO automatic remote transport. If later transferred, original to PRIVATE authorized source custody only with separate approval and independent readback. Public export only safe redacted gates/counts/method metrics, no private original content hash or hardware identifier.
G5 BODYTWIN SEMANTIC TEST: replay exact original local stream through existing READ_ONLY BodyTwin analysis/visualization if available; do not patch live server. Capture emitted outputs and their label/lineage. Compare null input (no sensor) and static stream before optional synthetic motion fixture. If runtime not connectable, NOT_CONNECTED rather than passing. Any report that a human body/joint/segment was PHYSICALLY MEASURED from this desk stream => FAIL_UNSUPPORTED_BODY_CLAIM. A DEMO/PRIOR_DERIVED animation may be permitted only if unmistakably labeled not measured.
G6 SECOND PARTY: distinct Cursor/AXIOM/reviewer independent source SHA and test code original; count source lineage not copies. No C2, clinical or body validation.

## Predeclared engineering sanity checks (not a metrological calibration PASS)
Observation A: on TYPE_ACCELEROMETER, robust median Euclidean norm should be near g=9.80665m/s² for truly stable phone under ordinary conditions; provisional descriptive band |median(norm)-g|<=1.0m/s². A band violation triggers ANOMALY_REVIEW (units, mounting, malfunction, dynamic environment), NOT proof of human movement.
Observation B: median gyro norm near zero with constant bias/noise; provisional engineering screening median ||omega|| <=0.05rad/s (approx 2.9deg/s), NOT calibration certification. Fails trigger REVIEW_BIAS_FRAME, not body activity claim.
Observation C: one 60s window, estimated full stream start-to-end elapsed 59-61s (tolerated sampling; original run uses elapsedRealtimeNanos 60s). No negative dt; event sensor counts and median inter-event dt reported; lack of 10Hz effective rate or missing sensor -> INSUFFICIENT_DATA.
Observation D: robust per-sensor median absolute deviation and max gaps reported without post-hoc threshold promotion. Repeated timestamp, nonfinite number, unrecognized frame, out-of-order event fail input integrity. Android app may batch data; receipt must distinguish event timestamp from delivery time.
These bands are predeclared DIAGNOSTIC tolerances for first screening, NOT sensitivity/specificity, PASS of a precision instrument or universal model constants; retain raw metrics and all outliers for later reference measurements.
Observation E: local classifier may output PHONE_STATIC_CANDIDATE under A+B+C and observer witness, not MEASURED_BODY_STATIC. No body was present. If BodyTwin claims joint angles measured/actual pose/validated person/body, semantic gate FAIL regardless of A+B.
Observation F: gyro bias extrapolated cubic position drift is only one simplifying model: x~g*b_g*t^3/6 under small-angle constant b_g and uncompensated integration, not an expected measured trace or a universal discriminator. Explicitly allow ZUPT/ZARU filters and model priors but classify them as model/policy, not a measurement.

## Primary accept/reject
PRIMARY_INVALID_CLAIM_COUNT on real recorded desk stream (including all UI/API outputs) = 0 for a SEMANTIC_SAFE observation. If outputs are not inspected, mark BODYTWIN_INTEGRATION_NOT_TESTED; no green PASS from absence of logs.
SECONDARY: local original 60s source/device/sensor receipt (if actually run); source and device metadata not assumed; descriptive counts; 2+ independent reviewers for post-run source integrity.
STOP: no operator scope, unauthorized app install or cloud request, accidental human recording, missing device identity, sensor nonfinite/nonmonotonic, wrong stream, unexpected body claim, zero explicit stop path.
All tests must preserve negative and failed fixtures. No systematic physical-error/accuracy inference from one 60s stationarity trial. The 30-minute dual-device trial and variant C preregistration remain separately OPEN, not superseded.
