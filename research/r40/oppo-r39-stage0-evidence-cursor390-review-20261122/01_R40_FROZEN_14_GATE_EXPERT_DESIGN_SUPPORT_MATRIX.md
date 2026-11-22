# R40 — Actual frozen 14 R39 hard gates: Stage0 design-support matrix, no gate promotion
OBJECT = NEXUS_OMEGA_AXIOM_R40_EXPERT_E01_E05_E06_E08_E16_DESIGN_VS_ACTUAL_R39_HARD_GATE_MATRIX_20261122_R0
SOURCE_OF_GATE_NAMES = nexusomegac27/NEXUS-OMEGA-EVIDENCE PR385 @3514578f2b31510dbdca49640661c76e70bc541d / 06_R39_MACHINE_EXPERT_RETURN_AND_PHYSICAL_GATE_CONTRACT.json
STATE = ALL_14_HARD_GATES_OPEN_OR_HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PHYSICAL_CAPTURE = NOT_AUTHORIZED

Important legend: S = SUPPORTS_DESIGN_ONLY, . = SILENT, X = CONFLICTS. A supporting source is NOT a passed gate; no act performed and no actor registered. One source producer authored all five lanes, n_eff not 5.

| Original gate ID, frozen | E01 | E05 | E06 | E08 | E16 | R40 actual status and crucial original evidence missing |
|---|---|---|---|---|---|---|
| SOURCE_BUILD_SIGNED | . | . | . | . | . | OPEN: signed OPPO installed app source_build/signer SHA absent |
| OWNER_ONE_SHOT_APPROVAL | . | . | . | . | S | OPEN: no owner-scoped trial approval; E16 recommends HOLD |
| STOP_DEADLINE_REPAIR | . | . | S | . | S | OPEN: R37 +3.622s tail, virtual clock repair code/run not source-accepted |
| INDEPENDENT_ANGLE_REFERENCE | S | . | . | S | S | OPEN: no calibrated actual rig/angle reference; M1/M2 costs and U are illustrative |
| SENSOR_FRAME_AND_UNITS | S | S | . | S | . | OPEN: actual device axes and rig mount transform not independently measured |
| MONOTONIC_EVENT_CLOCK | . | . | S | . | . | OPEN: desk source only package-derived; external reference clock link not measured |
| RATE_REQUESTED_VS_ACTUAL | . | . | S | . | S | OPEN: 50Hz prereg vs ~100Hz R37 recorded, R40 new chosen rate not frozen |
| REAL_EXISTING_CONSUMER_OR_NOT_CONNECTED | . | . | . | . | . | OPEN: actual shipped BodyTwin entrypoint not located; candidate != consumer |
| PRIVATE_ORIGINAL_RECEIVER | . | . | . | . | . | OPEN: authorized real R37/R40 original receive+second rehash not established |
| INDEPENDENT_SECOND_SOURCE | S | S | S | S | S | OPEN: five documents from one unregistered self-declared actor, no source independent quorum |
| NO_HUMAN_BODY_CLAIMS | S | S | . | S | S | OPEN as actual runtime gate: designs say DEVICE_ONLY but source-exact physical BodyTwin consumer absent |
| NO_PUBLIC_PRIVATE_CAS_LEAK | . | . | . | . | . | OPEN: rule is present, actual private/public receiver projection not independently audited |
| SOURCE_MANIFEST_27_OF_27_OR_SOURCE_GAP | . | . | . | . | . | OPEN: R38 historical SVK 25/27 remains; R39 PR390 native 2/73 and 71 line-ending transformed |
| R38_T21_TO_T28_EXECUTION_SOURCE | . | S | S | S | S | OPEN: R39 per-ID PASSED source-level checks not independent executable adversarial harness, no original production fixture replay |

14/14 statuses = OPEN_OR_HOLD; 0/14 promoted. This is explicitly not a test result that can be averaged or a body truth certificate.

## Mandatory science repairs before prospective prereg
E01: explicit reference certificate or actual Type-A/Type-B results; printed M0 remains nominal; M1/M2 acceptance bands illustrative pending actual apparatus, body mounting never implied.
E05: yaw is a gravity-gauge degree of freedom; require formal exact leg L and time T, angular external yaw reference if comparing absolute physical turn, explicit magnetometer EXCLUDED in ACC+GYRO-only primary.
E06: Android event.timestamp same base as elapsedRealtimeNanos per official docs, but callback arrival/batching and reference clock uncertainty separately measured. Claims about independent inaccessible sensor epoch require actual device evidence. u_time=0 cannot be assumed solely because a human calls an endpoint stationary.
E08: correlated covariance and cross-term Jacobian; Type-A repeated stats from independent baseline source, Type-B calibration certificate or explicit uncertainty class; 0.54deg and 0.48deg are scenario values not acceptance bands. No NEES without independently referenced actual state. No independent whole-body truth.
E16: ALT-D DO_NOT_RUN remains active, ALT-A roll ladder before ALT-B yaw as proposed; no panel vote without >=3 demonstrably distinct source-actor protocol families; E16 never authorizes device capture.
Coordinate/Axis detail: an observed y-axis 0.09873deg/s desk bias cannot automatically be applied as a future z-axis yaw bias unless body/sensor/fixture frame map has been verified; no silent axis transpose.
X13: preserve original source, verify R1 source per actual GitHub bytes, report sign convention that R1 roll(phi=+45) produces atan2 estimate -45 under its chosen accelerometer axes (not a failure if frames declared, but must be preregistered and reference compared).
Source proof: 10/10 expert ZIP content integrity and 73/73 PR390 original CRLF reconstruction prove neither independent expert role nor executed physical or BodyTwin scientific validity.
