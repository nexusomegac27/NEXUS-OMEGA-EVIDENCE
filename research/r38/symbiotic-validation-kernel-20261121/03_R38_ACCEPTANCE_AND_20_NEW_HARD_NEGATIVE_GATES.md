# R38 deterministic implementation acceptance — safety, science, model and negative controls
OBJECT = NEXUS_OMEGA_AXIOM_R38_SVK_FALSIFICATION_AND_ACCEPTANCE_MATRIX_20261121_R0
STATE = BENCH_DESIGN_FROZEN_NO_NEW_R38_RUNTIME_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED = NO
E99_HOLD = PRESERVED

## G0–G10 acceptance and non-compensation
G0 source hashes/commits exact, private source not public, R37 closed science phase. FAIL on incorrect parent/missing manifest.
G1 actual BodyTwin consumer identified by original code+entrypoint+version OR NOT_CONNECTED. No fabricated integration.
G2 real code for kernel, pinned environment and typed source/clock/unit/privacy enums independently testable offline.
G3 original M01 source provenance and 14/16 M02 failure independently rehashed; missing code -> source gap. Repair generates new R38 manifest without replacing old.
G4 independently physical IMU count across distinct device source IDs; same phone ACC+GYRO => ONE IMU, mounting calibration required to claim body.
G5 authorized private A/B/C has original exact immutable source and deadline; no access -> private replay HOLD, safe synthetic can progress.
G6 human veto, machine rule, external challenger each separately authentic; missing independent second-pass => UNSUPPORTED_INDEPENDENCE, not PASS.
G7 all 30 R37 shared fixtures +20 targeted below +5 model self-negative cases, source exact negative record for each, no aggregate pass masking one failing critical gate.
G8 uncertainty calibrated to reference when available, no posterior sigma as physical accuracy, real body DOF not measurable from stationary desk phone.
G9 local publication protocol CURRENT/OPEN/HISTORICAL_ARCHIVE tested; deployment separate, NO HOSTINGER in R38.
G10 independent second readback and replay actually executed, signed/exact source pinned; CI green never proves human physical truth.

## R38 additional hard failures — run after source-only suite
R38-T01 one ACC+GYRO physical device erroneously enumerated as 2 independent IMUs => FAIL_EXPECTED.
R38-T02 historic M02 result SHA+byte mismatch 2/16 => FAIL_EXPECTED for original, PASS only if discrepancy PRESERVED and corrective R38 evidence version is new.
R38-T03 old actual consumer absent but new model present => EXISTING_BODYTWIN_NOT_CONNECTED.
R38-T04 body-like generated animation under zero input -> GENERATIVE_PRIOR_ONLY, reject MEASURED claim.
R38-T05 stationary desk sensor stream and BODY_MEASURED or JOINT_ANGLE_MEASURED label -> FAIL_UNSUPPORTED_ANATOMY.
R38-T06 afterdeadline 363 per channel included in 60s protocol -> FAIL_PROTOCOL, separate full-source descriptive.
R38-T07 100Hz requested actual vs 50Hz planned silently 'matches' => FAIL_PROTOCOL_BINDING.
R38-T08 source_build empty yet APP_SOURCE_ATTESTED=true -> FAIL_SOURCE_AUTH.
R38-T09 owner approval absent yet DEVICE_CAPTURE_AUTHORIZED=true -> FAIL_AUTHORITY.
R38-T10 private original SHA exposed in public source URL/CAS -> FAIL_PRIVACY.
R38-T11 agent self-labels AXIOM_APPROVED -> FAIL_UNTRUSTED_AUTHORITY.
R38-T12 nonfinite JSON, duplicate JSON keys, wrong event axis or unknown class -> FAIL_INPUT_CLOSED.
R38-T13 logical read budget 5, limit 3 -> FAIL_BUDGET even if byte count passes.
R38-T14 ten identical source copies counted n_eff10 -> FAIL_INDEPENDENCE.
R38-T15 operator revoke while run is queued -> STOP_NO_NEW_CAPTURE.
R38-T16 replayed run UUID accepted as fresh owner/device evidence -> FAIL_REPLAY_AUTH.
R38-T17 original source mutation between hash check and read -> FAIL_TOCTOU.
R38-T18 learned-model weight without dataset/weights legal rights -> HOLD_LICENSE_NOT_AUTOGREEN.
R38-T19 no sensor mounting + accurate synthetic skeletal prior -> NO_BODY_MEASURED.
R38-T20 fake 3-IMU minimum treated as universal observability theorem -> FAIL_OVERGENERALIZATION.

## Controls, false positives, false negatives
M01 Unit 8/8 and synthetic fixtures 10/10 were independently executed by AXIOM on original source code in isolated Python, but R38 must capture its own new execution. At least 2 positive controls (synthetic phone static, known synthetic 90° tilt) should return permitted DEVICE estimates, and 2 intentional negative controls (forged anatomical claim, no source-build attestation) should hard fail. Do not count expected rejection as a malicious program crash. Test 30 common Q00–Q29 from R37 #380 machine contract plus 20 listed here; at least 5 new model-self-falsifiers: domain shift, no-sensor prior hallucination, drift, mounting slip, private/public hash leak.
If reference truth is absent: NO_ANGLE_ERROR, NO_NEES, NO_MPJPE claims; only source-conditional algorithmic consistency/uncertainty proxies. NIS after outlier gating cannot be a primary 'pass' because of selection.
A green test suite must show TEST_COMMAND + exact SOURCE_COMMIT + TESTS_EXECUTED_N and every per-ID verdict, with separate runtime consumer classification.

## Required test result schema per item
{id, expected_result, actual_result, source_sha256, model_sha256, test_source_commit, input_source_class, actor, evidence_ref, executed_at_utc, actual_run_id, run_status, failure_label, supersedes_ref}
run_status may be NOT_RUN, PASSED_EXPECTED, FAILED_UNEXPECTED, FAIL_EXPECTED, SOURCE_GAP. No invented raw original IDs.
A fake ACK or absent test is never a PASS.

## Security constraints for Cursor
No cloud/model API calls with raw health/IMU sensor records; sandbox no network/untrusted compiled .pyc; source-only pinned dependencies. Restrict source mount read-only, bound CPU/RAM/time and explicit kill, no remote shell/ADB hidden capture. Real phone input can be tested later through separately authorized private source read-only gate, not because GitHub contains a hash.
