# R39 hard negative and positive predeclared checks
OBJECT=NEXUS_OMEGA_AXIOM_R39_PHYSICAL_OPPO_RIG_PREDECLARED_FALSIFIERS_20261122_R0
STATE=PREPARATION_NOT_RUN
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY | BODYTWIN_VALIDATED=NO
Test purpose: evaluate actual phone-only rigid-body motion under independently measured angular reference, app source/clock and body-claim abstention. PASS counts cannot compensate for missing source/consent/reference.

Hard negative fixtures (each with explicit expected verdict, no execution claim):
F00 unapproved new phone capture => DENY.
F01 missing signed source_build => AUTH_GAP.
F02 changed build after prereg => SOURCE_GAP.
F03 canceled or revoked capture still armed => FAIL_STOP.
F04 2 channels ACC+GYRO counted as 2 distinct IMU assemblies => FAIL_INVENTORY.
F05 roll axis mislabeled yaw or handedness wrong => FAIL_FRAME.
F06 accelerometer g vs m/s2 or gyro deg/s vs rad/s => FAIL_UNITS.
F07 gyroscope relative yaw asserted absolute heading => FAIL_YAW_OBSERVABILITY.
F08 static gravity sensor falsely measures yaw about gravity => FAIL_OBSERVABILITY.
F09 dynamic acceleration treated as gravity-only tilt => UNCERTAINTY_OR_ABSTAIN.
F10 nominal printed 90 degrees labeled calibrated ground truth => FAIL_REFERENCE.
F11 fixture slip unrecognized => FAIL_MOUNTING.
F12 sensor 100Hz vs prereg 50Hz silently accepted => FAIL_RATE.
F13 wall-time count called sensor-event rate => FAIL_CLOCK.
F14 reverse/duplicate/nonfinite source event => FAIL_SOURCE.
F15 FIFO batch report time substituted for event timestamp => FAIL_TIMEBASE.
F16 original R37 3.6s tail deleted or accepted as exact protocol => FAIL_CUSTODY.
F17 physical test code claims actual existing BodyTwin despite no consumer => FAIL_SUBSTITUTION.
F18 real bench motion generates measured human joint => FAIL_UNSUPPORTED_BODY.
F19 zero input generates BODY_MEASURED => FAIL_UNSUPPORTED_BODY.
F20 private raw or content digest published in public CAS => FAIL_PRIVACY.
F21 independent reviewer is same source lineage with a second label => FAIL_INDEPENDENCE.
F22 external model output self-grants AXIOM or operator approval => FAIL_AUTHORITY.
F23 R38 original 25/27 source manifest disguised as 27/27 by runtime rewrite => FAIL_SEAL.
F24 missing source fixture counted green => FAIL_AGGREGATION.
F25 LLM read says OPEN while raw GitHub state says CLOSED => READBACK_CHANNEL_MISMATCH.
F26 restart with old one-shot permission or automatic repeat after end => FAIL_REPLAY_AUTH.
F27 same angle series generated from synthetic reference labeled real calibrated => FAIL_REFERENCE_SOURCE.
F28 physically unattached phone used as measured whole-body pose truth => FAIL_PHYSICS.
F29 rank of toy Jacobian asserted globally physically observable anatomy => FAIL_OVERCLAIM.
F30 unresolved angle reference uncertainties omitted from reported error => FAIL_METROLOGY.
F31 lack of original source receiver rehash counted as independent proof => FAIL_CUSTODY.

Positive controls to design and run OFFLINE before hardware: virtual-clock stop before deadline, source manifest immutable across run, synthetic roll identifiable to device only, synthetic yaw no absolute compass claim, real-consumer absent yields NOT_CONNECTED, source and operator revocation blocks any new capture, independent source-actor readback.
Do not invent allowable error degrees until angle-reference uncertainty and original process variance are quantified, signed into prereg, then examined on held-out future data. No NEES without ground truth.
