# NEXUS OMEGA — R36R2 source adjudication and transition to R37
OBJECT = NEXUS_OMEGA_AXIOM_R36R2_STAGE0_INTAKE_R37_STATIONARY_PHONE_BRIDGE_20261120_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_R36R2_SOURCES_REVIEWED_R37_NEXT
ISSUED = 2026-11-20
PARENT_PUBLIC_PR375 = 289b0fa5aa1424986b03e2b7fdd94b597edb91af | OPEN_DRAFT_NOT_MERGED
PARENT_PRIVATE_PR35 = 16f50bf15bd112736c0c111cd9fbd8b44c9c853a | OPEN_DRAFT_NOT_MERGED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
R36 = OPEN
R37 = NEW_INDEPENDENT_RESEARCH_PHASE_CANDIDATE
BODYTWIN_VALIDATED = NO
OPPO_SENSOR_CENSUS = NOT_OBSERVED_BY_AXIOM
PRIVATE_TRANSPORT = NOT_EXECUTED
REAL_PHONE_CAPTURE = NOT_EXECUTED
CONSENT_BIND = OPEN_FOR_HUMAN_OR_PRIVATE_DATA
PR_MERGE = NO
HOSTINGER_WRITE = NO

## Five user-provided 2026-11-20 originals, local forensic validation
A. External Grok adequacy text: 6096 bytes, SHA256 b43a246f13345997ec76a164609ec8f62db7954837acaeaa911bfb0e0237298b. Self-declared external assessment, not authenticated independent device science.
B. Mistral/Vibe study MD: 23976 bytes, SHA256 356185f1ec4395ef950e9a9ef8e4103ce5c434fae619ce3c54ab1f198d74a90d. PREEXPOSED, source reported GitHub rehash, formal task-anchor and source audit, but GitHub-original research return ACK not established; preserve as unregistered external candidate.
C. AutoClaw_Return.zip: 97937 bytes, SHA256 05da0063a6b883b1eeea65fa610907b0821b2ddce430adab3c120358e56c5033. ZIP CRC PASS; 13/13 SHA256SUMS file hashes MATCH (12 content artifacts + MANIFEST.json). 4 contained synthetic Python scripts X7–X10. STAGE0_SEAL claims PREEXPOSED_PARTIAL, NOT BLINDED; seal report is producer-asserted.
D. OPPO-HARD PDF: 263700 bytes, SHA256 578143f1e43feb6a2313920e770bb9e916a58f0cd7c8c6b20ed3f5daf0ca98de; pdfinfo 10 pages. Self-declared auditor "ZCode zgo/glm-5.2"; original still only operator-supplied, not authenticated operator countersignature, device or active registration. This is a different presentation/source from earlier 18/29-page documents: do not silently substitute.
E. workspace.tar(3).gz: 16775 bytes, SHA256 b975970edbf1b47927b267c0acbf9bf08b9877ad8964a4958c16a823e961804f. Tar safety inventory 4 entries; two actual file hashes in SHA256SUMS MATCH. Original stage0 reviewer labels itself ADVISORY_INPUT_UNREGISTERED, NO_GITHUB_WRITER, NO_SOURCE_VERIFICATION_OF_NEXUS. YAML registry parses successfully in independent PyYAML environment, but this is syntactic validation, not experimental proof.

## Actual independent local isolated synthetic replay
AutoClaw original scripts extracted ONLY into isolated temporary directory, Python -I -B, no network/OS-level device operations:
- X7 redundancy: exit=0; JSON semantic results MATCH saved original, bytes DIFFER (whitespace/serialization).
- X8 ternary vs typed: exit=0; JSON semantic results MATCH saved original, bytes DIFFER.
- X9 bounded search: exit=0; JSON semantic results MATCH saved original, bytes DIFFER.
- X10 clock model: exit=0; model selections MATCH all three (no step -> affine; step 50 and 200 ppm -> piecewise); key numerical values match to engineering tolerances; exact float payload DIFFER due environment/numeric solver. Do not claim byte-exact independent reproduction. Test input simulation n_pulses=12 and no real phone or reference timebase.
The claimed n_eff = 1 for 10 copied returns is accurate FOR THE SIMULATED LINEAGE ROOT LABELS; no actual source-actor independence was authenticated. X8 deliberately compares a naive ternary/default-allow against a secured typed enum; the measured difference is a CONTROL/POLICY difference, not an intrinsic law of hardware ternary safety.

## CRITICAL scientific correction to external Stage0 simplification
A cited static-IMU error propagation x_err~g*b_g*t^3/6 is a small-angle, constant-bias, uncompensated inertial integration approximation. A real Android phone measurement/BodyTwin output is NOT required to follow exactly t^3; ZUPT/ZARU, sensor bias compensation, gravity estimation, sample jitter and low-pass filters change it. Lack of cubic drift alone does NOT prove fraud or a secret prior. Instead, require source- and output-label trace separating observed device acceleration, integrated device-state estimates, and unvalidated human-body inferences.
The external suggestion "60 s table test, no authorization needed" is NOT adopted literally: an owner-visible, specific local device test still needs operator approval for exact app/device/data; human/body recording remains separately gated. A phone resting on a rigid table is NOT a calibrated body kinematics reference.

## R37 discriminating scientific research question
Observe one actual owner-controlled OPPO on a stable surface for exactly 60 s (monotonic start/end), recording only the required accelerometer + gyroscope streams, WITHOUT human wearing, location, camera, microphone, cloud upload or body-data collection. Freeze static protocol/test code before acquiring samples.
Q1 Did the specific deployed Android app enumerate actual sensors and report real monotonic timestamps?
Q2 With one stationary fixture, does raw accelerometer norm stay approximately g, gyro near zero plus bias and noise, with actual delta-t, dropouts and nonfinite input tracked?
Q3 Does the actual BodyTwin pipeline, when given this data, ever claim MEASURED_BODY_MOVEMENT / JOINT_ANGLE_MEASURED / BODYTWIN_VALIDATED? Any such claim from this dataset is a semantic fail. A distinct DEMO/PRIOR_DERIVED label does not itself establish anatomical truth.
Q4 If BodyTwin pipeline has not been connected to the exact original stream, report NOT_CONNECTED / NOT_TESTED rather than PASS.
Q5 Can a separate baseline with no sensor data produce similar BodyTwin visuals? If yes, classify as model/prior demonstration, not sensor-measured body motion.
No invented statistically certified accuracy thresholds; predefine exploratory engineering sanity bands and report departures rather than optimize after observing.

## Scope boundary to successor
R36R2 remains source/methodology parent; keep PR375 and PR35 OPEN DRAFT. R37 is a new separate public Draft PR with first physical static null-control design, owner-visible on-device execution conditional on exact manual operator approval in Cursor session. Public PR only contains source-safe design, code and redacted C1 receipts; private OPPO original run bytes and any identifying hash/metadata belong to explicit private custody only. NO device capture, network handshake or source download has been executed by AXIOM in R36R2.
