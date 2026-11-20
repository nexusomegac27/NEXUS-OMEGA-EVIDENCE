# R37 Cursor MAXI order — physical OPPO 60-second negative and safe BodyTwin integration
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R37_OPPO_60S_STILL_PHONE_TEST_AND_BODYTWIN_INTEGRATION_MAXI_ORDER_20261120_R0
AUTHORITY = OPERATOR_R37_TRANSITION_THROUGH_AXIOM
STATE = SCOPED_IMPLEMENTATION_ORDER_READY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R36 = OPEN | R37 = OPEN_DRAFT | R37_ACTUAL_PHONE_DATA = NOT_YET_OBSERVED
SOURCE_GITHUB_ONLY = YES
NO_PR_MERGE = YES | NO_HOSTINGER_WRITE = YES | NO_WWW_LIVE_DEPLOY = YES
NO_HUMAN_BODY_MEASUREMENT = YES | NO_BACKGROUND_HARVESTING = YES
NO_BLANKET_DEVICE_CAPTURE_APPROVAL = YES
OPERATIVE_GOAL = FIRST_REAL_STATIONARY_PHONE_NEGATIVE_NOT_NEW_ANALOGIES

## Explicit pinned prerequisite
Read this new R37 GitHub PR exact HEAD and SHA256SUMS once published.
Public R36 predecessor PR375 before R36R2 bridge @289b0fa5aa1424986b03e2b7fdd94b597edb91af, later appended R36R2 bridge HEAD@1147d390e90886771ab1b3462f29683d4abc98d3; do not pretend old Cursor ACK covers new commits. Private R36 PR35 source parent @16f50bf15bd112736c0c111cd9fbd8b44c9c853a, requires separate restricted authenticated access. No source-data transfer via operator chat to outside experts; GitHub is the ONLY intended order/return interface after registration. R37 branch can be prepared on a separate scientific source snapshot without merging R36.

## Cursor tasks in causal order
C0 READBACK AND ENVIRONMENT:
- Public new PR/head, manifest including machine gate and fixture source. Pin each source sha256/bytes and tooling before running.
- Source-reconcile operator five R36R2 delivered source objects in authorized custody; original chat uploads are available to AXIOM but not automatically present in Cursor's GitHub. No fabricated local presence. If specific original missing, SOURCE_GAP in old context; do not block independent synthetic or code inspection.
- Check private OPPO original app source, currently installed package certificate/version, actual device, sensors, Android OS and target SDK read-only; avoid unapproved ADB/app install or new access to private drive.

C1 IMPLEMENT R37 STATIC NULL CONTROL IN EXISTING APP/TEST LANE:
- Find EXISTING Android SensorManager collector and local export; if absent, prepare a small optional in-app user-visible 60s collector as a review-only patch on a new R37 CODE branch, not in the private original source without owner approval.
- Need TYPE_ACCELEROMETER and TYPE_GYROSCOPE original sensor events (not TYPE_LINEAR_ACCELERATION silently substituted); capture exact sensor_type, timestamp_ns monotonic, 3-vector SI, accuracy, sensor vendor/version/resolution/minDelay, source app git commit and APK signing proof. Note Android gyro values rad/s and accel m/s² including g.
- Capture provenance: DEVICE_REPORTED vs DEVICE_OBSERVED, LOCAL_SOURCE vs HOST_COPY, EVENT_TIME vs RECEIVED_TIME. No raw hardware serial in public metadata.
- Ensure explicit on-screen START / STOP, 60s local monotonic deadline, no network, no FGS/background mode, no microphone/camera/GPS/health sensors. No autonomous retry. If Android policy prevents it, document a STOP not a workaround.

C2 BEFORE PHYSICAL RUN — SYNTHETIC GUARD / API TESTS:
- Use 03_R37_BODYTWIN_60S_NEGATIVE_FIXTURES_AND_STOP_CONTRACT.md as frozen expected statuses. Test at least the 12 cases: good stationary synthetic, too-short 30s, missing gyro, nonfinite, duplicate/nonmonotonic timestamp, arbitrary axis, gravity-free sensor substitution, fake body label, no-sensor BodyTwin baseline, unknown output labels, unauthorized app/transport, app build mismatch/replay.
- Assert input rejects FAIL/HOLD and every fake body-measured/joint-angle/validated flag is rejected, NEVER default allow. Security regression source X5 status/authority string remain open, do not use them as signers.
- If tests fail, repair code only in separate reviewable experimental branch with before/after and negative receipt; no live release.

C3 EXACT LOCAL OWNER-VISIBLE DEVICE TEST — CONDITIONAL:
- DO NOT RUN until the OPERATOR in the actual Cursor/device session explicitly approves the narrow scope: physical phone identity, installed app/code version, 60s table-only accelerometer+gyro, local data-only, no human participant and visible stop. This order itself is not that final live device acknowledgment.
- Once all prior local checks and that approval exist, collect exactly ONE 60s stationary run from an untouched OPPO on the desk. If the device or app is absent/unreachable, DEVICE_TEST_NOT_RUN (not simulated data presented as original).
- The owner should be present and able to abort; record run_id, local monotonic start/stop and user initiation. No second phone required. No location/video/mic/cloud, no private server/Hostinger or background acquisition, no hidden infinite repeats.
- The phone being on a table is an OPERATOR-OBSERVED FIXTURE; do not assert certified absolute stillness.

C4 ORIGINAL ANALYSIS & SEMANTIC CONTRADICTION:
- Locally source-validate 60s event timestamps, event counts/sensor rates, gyro mean/median/norm and bias/noise proxy, accel norm median/MAD near g, missing data/dropouts, sample gaps. Use fixed engineering bands from 01, label descriptive not calibration.
- Preserve raw vs estimated device orientation vs model-prior positions and any UI/API BodyTwin output. Compare null input (no samples) and static OPPO stream; if a no-sensor demo animates identically, label model/prior display and cannot call sensor-measured anatomy.
- If actual BodyTwin consumer cannot be connected to original stream, report BODYTWIN_INTEGRATION_NOT_TESTED not BODYTWIN_PASS. Capture exact output labels and version on original pipeline, no mock fabricated system real pass.
- If BodyTwin exposes measured human joint angle, human body movement, whole-body pose or validated anatomy on desk-only data, record FAIL_UNSUPPORTED_BODY_CLAIM and freeze/review; do not silently suppress failure or only polish UI.

C5 PRIVATE RECEIVER CUSTODY:
- Keep actual event bytes, device signature or identifying original digest in approved PRIVATE OPPO GitHub/custody if separately authorized, with exact source/byte size/hash and local operator ACK. No public raw sensor lines, private CAS hash, serial, secret or participant data.
- Actual GitHub merge or push is not equal to device-source authentication or reciprocal private server ACK. This 60s local-only test deliberately does not exercise Hostinger transport. Record PRIVATE_TRANSPORT_NOT_EXECUTED.

C6 INDEPENDENT EVIDENCE CHECK:
- A genuinely separate reviewer independently inspects real local source, scripts and output lineage; exact original SHA and two-party claims restricted to authorized private channel. Unavailable second reviewer => C1_REPORT_ONLY_WITH_INDEPENDENCE_GAP, not false fully validated.
- Preserve the R36R2 X7–X10 synthetic research as historical method checks only: do not conflate 10 returned copies with n_eff of 10, or ternary status with authenticated authority.

C7 SYSTEM INTEGRATION DECISION:
- Proposal only: typed output surfaces PHONE_SENSOR_OBSERVED, PHONE_STATIONARY_CANDIDATE, DEVICE_ESTIMATED, MODEL_PRIOR_DERIVED, NO_BODY_OBSERVATION, BODYTWIN_INTEGRATION_NOT_TESTED, FAIL_UNSUPPORTED_BODY_CLAIM, and explicit source/uncertainty. No HUMAN_BODY_MEASURED from 60s tabletop data.
- Add regression gates and private original receiver to future build/test pipeline after code review; no production or website write from this order. Issue separate scoped downstream deployment approval only after actual evidence and safe rollback.
- R37 first success = source-bound physical zero-motion negative with no unsupported body-claim in the actually connected pipeline; this is not a physical BodyTwin proof or dual-phone clock validation.

## Mandatory atomic return
Return a GitHub-only, non-merged PR or explicitly registered receiver location; include:
- exact R37 HEAD and R36R2 bridge parent, independent file readbacks, 12+ synthetic fixture results with source code hash;
- actual DEVICE_CAPTURED_YES/NO + identity consent/owner-approval evidence (restricted private);
- MONOTONIC_60S_YES/NO, SENSOR_CENSUS with real original ref, counts/hz/anomalies and descriptive accelerometer/gyro stats;
- BODYTWIN_CONNECTED_YES/NO, BODY_CLAIM_FAILURE_COUNT, ZERO_INPUT_BASELINE and the exact output code version;
- private source receipt and independent reviewer status if legitimately observed;
- STOP reason for any missing precondition and exact NEXT nonrecursive action;
- signed/hashed SHA256 file manifest. No secret echo, no false PASS, no PR merge/Hostinger or Chat-only transfer.
No external self-declared identity can authorize a device action.

## Explicit terminal fail-closed gates
R36=OPEN; R37=OPEN_DRAFT;
OPPO_ENROLLMENT=NOT_ESTABLISHED until witnessed;
60S_REAL_DATA=NOT_RUN until physical owner-approved capture;
PRIVATE_TRANSPORT=NOT_EXECUTED;
BODYTWIN_VALIDATED=NO;
CONSENT_BIND=OPEN for human/body data;
E99_HOLD=PRESERVED;
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.
