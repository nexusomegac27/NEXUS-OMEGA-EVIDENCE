# R37 — AXIOM independent intake and 60s stationary OPPO source-data adjudication
OBJECT = NEXUS_OMEGA_AXIOM_R37_60S_OPPO_STATIONARY_SOURCE_DATA_INDEPENDENT_ADJUDICATION_20261120_R0
ISSUED = 2026-11-20
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_SENSOR_SEGMENT_REPLAYED_BODYTWIN_NOT_TESTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
PUBLIC_SAFE = METRICS_ONLY_NO_RAW_SENSOR_PRIVATE_DIGEST_OR_DEVICE_UID
R36_PARENT_OPEN = YES
R37_PR378_OPEN_DRAFT_NO_MERGE = YES
BODYTWIN_VALIDATED = NO
OPPO_ENROLLMENT = NOT_ESTABLISHED
PRIVATE_TRANSPORT = NOT_EXECUTED
HUMAN_CONSENT_BIND = OPEN
OPERATOR_DEVICE_RUN_APPROVAL_WITNESSED_IN_RETURN = NO
INDEPENDENT_ORIGIN_ATTESTATION = NOT_ESTABLISHED
CURSOR_R37_REAL_DATA_RETURN = RECEIVED_AS_USER_UPLOAD_TO_AXIOM_NOT_YET_PRIVATE_GITHUB_ORIGINAL
BODYTWIN_REAL_STREAM_OUTPUT = NOT_PRESENT

## Exact scope of what was independently checked
Two separately uploaded Cursor ZIPs plus their external sidecars were byte-hashed independently, both sidecar hashes MATCH, both ZIP CRC PASS. The earlier R36R2->R37 foundation ZIP has 5/5 internal SHA256SUMS exact matches; the R37 actual-IMU return has 12/12 exact matches after normalizing ZIP path separators. Its nested sensor ZIP is CRC PASS and contains a compressed NDJSON segment whose bytes EXACTLY MATCH the separately bundled segment. These are independent verifications of RECEIVED BYTES, not independent attestation of Android app signing, device origin or execution authorization. To prevent a public/private CAS correlation leak, exact original archive/segment SHA256 are recorded only in the restricted R37 private review, NOT here.

## Direct independent sensor-stream calculations (read from raw supplied gzip NDJSON, not copied from Cursor summary)
R37 run class: single OPPO model CPH2219 reported by source; Android app reported as com.nexusomega.maps. Actual signed APK/source-build hash not delivered by this bundle.
- Total sensor events: accelerometer 6,374; gyroscope 6,366; no nonfinite values; no duplicate or backwards timestamps *within either sensor channel*.
- Accelerometer sensor-event monotonic span: 63.612293650 s; gyroscope: 63.532421358 s. This is NOT an exactly 60s recorded sensor span.
- Median event interval for both channels: 9.981510 ms; actual frequency calculated from sensor timestamps about 100.185 Hz. Cursor's approximately 99.61/99.49 Hz quotes are counts divided by total 63.988s wall duration; label those WALL-RATE rather than SENSOR-EVENT-RATE.
- Gyroscope magnitude median 0.00203686647 rad/s, magnitude MAD ~0.0003844672 rad/s; near-zero residual bias/noise consistent with a stationary phone.
- Accelerometer magnitude median 9.81855214549 m/s², magnitude MAD ~0.00484270019 m/s², ~0.012 m/s² above standard g=9.80665. Consistent with approximate table stationarity, not independently calibrated accuracy.
- Median per-axis accelerometer, gyro and full record remain PRIVATE; no participant or human body was measured. Observed nonzero noise/bias is scientifically expected.
- All per-sensor inter-event gaps <= 10.001 ms in this archived run; NO missing-event claim outside this exact stream.

## Predeclared 60s segment vs extended capture
R37 original design targeted one 60s local monotonic measurement. Archived capture starts/ends approximately 63.988 s apart by report wall timestamps. Crucially, the local source seal includes a MONOTONIC STOP DEADLINE: 363 accelerometer + 363 gyro events occur AFTER that deadline, lasting about 3.622 s beyond it. When restricting the analysis to <= the independently archived deadline *without altering original file*, first 60s subset contains 6,011 accelerometer and 6,003 gyro events, spanning approx 59.989 and 59.909 s respectively. This is an explicit protocol deviation / app STOP timing investigation, not a claim the additional data are invalid as signal. Preserve both full and prereg window measurements, never replace originals.
Source explicitly requests 100 Hz in actual segment metadata, whereas the R37 GitHub candidate protocol requested 50 Hz. Rate mismatch is a documented prereg/protocol deviation; it does not imply real-device fraud. Run was APP_DEADLINE with a producer-reported 'arm then fire then start' path.

## Material methodological/custody caveats
(1) The uploaded local seal source_build field is EMPTY: exact installed app source commit, APK signing certificate and code-to-capture attestation are not established by this content.
(2) The local seal reports autonomous_eligible=true and alarm_generation=4; these fields do NOT prove that a run was autonomously unauthorized, but actual owner-visible, exact-scoped consent/approval and start/stop witness must be traced. Prior foundation return explicitly stated OWNER_APPROVAL_FOR_60S=ABSENT; this new return does not supply a countersigning approval original. Do not infer authorization retroactively from successful capture.
(3) Underlying original stream exists in the user-uploaded local source return; no separate independent authenticated device-side rehash witness or full installation chain is supplied. Cursor's reported DEVICE_TO_LOCAL_REHASH MATCH is a source claim, not separate AXIOM device access.
(4) NO actual connected BodyTwin consumer log, UI snapshot, human body output, zero-input baseline, 21-fixture runtime results or independent BodyTwin semantic PASS appears in the source package. The primary R37 falsification question is therefore NOT_TESTED, not PASSED.
(5) No human data were collected according to source scope, so this is a DESK DEVICE SIGNAL rather than consented BODY study. Still document device-owner operational authorization and local retention; this report is not a legal assessment.
(6) Secondary physical calibration, dual-phone time synchronization, OPPO enrollment/authentication, private server receipt and clinical/body kinematics remain untested. Source stability is not proof of sensor metrological traceability.

## Adjudication under the "retained thread" law
CONTEXT_ROUTE_KNOWN = YES: R36 methodology -> R37 source original package -> static sensor signal analysis -> required BodyTwin semantic differential experiment.
EVIDENCE_CHAIN_CLOSED = NO: authenticated mobile source code, owner-visible approval receipt, BodyTwin real-stream exposure and independent receiver witness missing.
WHAT_ADVANCES = real-style private sensor event bytes are present and independently parsed; no need to keep redoing source-only analogies before inspecting actual BodyTwin consumer.
WHAT_REMAINS_OPEN = NO_HUMAN_BODY_OBSERVATION, BODYTWIN_INTEGRATION_NOT_TESTED, no body validation or claim promotion.
Uncertainty is preserved without making up absent fragments, and unknown information is not deleted.

## R37 next Cursor move (one bounded differentiating test, no recapture by default)
N0 READ_ONLY locate actual BodyTwin consumer in source and explain how it would ingest *the exact already obtained* archived OPPO stream. Check its signed installed build, no network command or automatic APK install.
N1 ISOLATED OFFLINE REPLAY of the existing source: (a) NO_SENSOR_INPUT control, (b) STATIC_60S_PREDEADLINE_WINDOW, (c) STATIC_FULL_63.6S_WINDOW, with separately source-bound source and output hashes under authorized PRIVATE custody. Do not add mock source observations.
N2 OUTPUT CLASSIFICATION: all UI/API/output machine labels are either PHONE_SENSOR_OBSERVED / MODEL_PRIOR_DERIVED / NO_BODY_OBSERVATION or fail on unsupported HUMAN_BODY_MEASURED / JOINT_ANGLE_MEASURED / BODYTWIN_VALIDATED. If no consumer exists, report INTEGRATION_NOT_TESTED explicitly.
N3 HARDEN APP DEADLINE: explain why ~3.6s worth of events postdeadline were captured; propose regression fixture to stop input at deadline and test exactly 60s, but do not silently remove or alter this original.
N4 SOURCE/OWNER: recover actual explicit local owner scope acknowledgement and installed binary/source_build proof, WITHOUT creating a new receipt retroactively. If absent, preserve APPROVAL_GAP and SOURCE_BUILD_GAP; pause new hardware captures.
N5 CUSTODY: deliver exact original phone segment only to the authorized private GitHub original receiver with operator approval, then independent rehash; publish only sanitized conclusions, never raw source bytes or private original digest; keep R37 #378 and R36 #375 separate and OPEN DRAFT.

## Terminal C1 limits
RESULT = STATIC_OPPO_DEVICE_STREAM_MOTION_CONSISTENT_C1_RECEIVED_BYTES
BODYTWIN_SEMANTIC_FALSIFIER = NOT_RUN
REAL_BODYTWIN_SYSTEM_VALIDATION = NO
OWNER_APPROVAL_WITNESS = GAP
ORIGINAL_HARDWARE_AUTHENTICITY = PRODUCER_REPORTED_PLUS_LOCAL_SOURCE_CUSTODY_NOT_CRYPTO_ATTESTED
NEXT = CURSOR_READONLY_REAL_BODYTWIN_ZERO_VS_STATIC_SOURCE_REPLAY_AND_DEADLINE_AUDIT
NO_CAPTURE_AUTHORIZED = YES
PR_MERGE = NO | HOSTINGER_WRITE = NO | WWW_WRITE = NO
