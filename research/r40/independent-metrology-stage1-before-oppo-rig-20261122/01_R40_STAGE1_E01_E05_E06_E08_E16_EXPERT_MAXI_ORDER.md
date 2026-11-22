# R40 Stage1 scientific MAXI mandate — independent metrology and physical-test adjudication
OBJECT = NEXUS_OMEGA_AXIOM_R40_INDEPENDENT_METROLOGY_STAGE1_E01_E05_E06_E08_E16_MAXI_ORDER_20261122_R0
STATE = GITHUB_ONLY_RESEARCH_ORDER_NOT_YET_ACKNOWLEDGED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
BODYTWIN_VALIDATED = NO
DEVICE_CAPTURE = NOT_AUTHORIZED
EXTERNAL_WRITE = DENY_PENDING_GITHUB_ACTOR_REGISTRATION
NO_APK_INSTALL | NO_PR_MERGE | NO_HOSTINGER_WRITE | NO_WWW_WRITE
PARENT = R40 public PR391 HEAD 1b72776c699fdaf87b3f70785072cad14fa2b026
R40_CURSOR = RETURN_6262B_SHA256_4efd19dfd52463bac2c50688be0a29205ba48acc0c550010fd5ea7cf058f078e
14_R39_HARD_GATES = ALL_OPEN_OR_HOLD
EXTERNAL_STAGE0 = FIVE_LANES_ONE_UNREGISTERED_PREEXPOSED_ACTOR_NOT_QUORUM

## Scope and scientific claim
A single unmounted OPPO CPH2219 in a rigid cradle can produce device inertial data; without a separately mounted, calibrated anatomical measurement system it cannot establish human joints or full-body motion. The exact next physical trial is not authorized by this order. The research asks whether a 0/45/90/0 roll ladder with independent angle reference offers falsifiable physical information beyond the previously observed stationary phone baseline, and whether source/consent/uncertainty risks require DO_NOT_RUN instead.
Expert research must be genuinely independent, not multiple documents under one account, and may reject the preferred rig entirely.

## E01 — independent angle metrology and fixture
Provide two independent realizable rig-reference options: mechanically calibrated precision inclinometer/angle block and independent optical encoder/camera reference (if viable). Quantify resolution, calibration class, repeatability, backlash, mounting slippage, transverse angular coupling, gravity direction, fixture rigidity, and temperature. Distinguish nominal printed-angle scale from measured reference; no arbitrary 0.5-degree physical acceptance threshold. Provide an error budget with traceable Type A/Type B source for each term, correlations, k factor and likely dominant term. Include falsifier in which reference moves with phone or fixture slips so apparent agreement is circular.

## E06 — Android clock and stop deadline
First-party Android SensorEvent and SystemClock document event timestamp on elapsedRealtimeNanos timebase for sensor events; distinguish event time, delivery time, app wall deadline and independent reference system timing. Propose defensible external clock trigger and mapping with timing uncertainty, not an automatically synchronized clock assumption. Provide an offline, no-sensor virtual-clock negative which catches R37's reported +3.622 s deadline tail and old ~100 Hz vs 50 Hz requested mismatch. No runtime device control or ADB invocation from researcher role.

## E08 — GUM/UKF uncertainty challenge
Derive roll angle phi from accelerometer specific force, explicit sensor frame and sign conventions, reference angle measurement and gyro integrated roll cross-check. Build covariance/Jacobian or deterministic nonlinear Monte Carlo for bias, scale, cross-axis misalignment, mount error, reference time, temperature, sensor noise and common-mode correlation. Demonstrate counterexample where a low internal UKF covariance coexists with a wrong external angle due to common-mode mount offset. No NEES without valid independent physical truth, no gated NIS as primary proof. Current M1 U~0.54 and M2 U~0.48 degree are scenario figures only; report no validated accuracy until a particular reference is characterized.

## E05 — yaw gauge boundary check
For ACC+GYRO only, derive why rotation about gravity is not independently detectable in gravity projection, and why integrated gyro yaw is relative and drift-prone rather than absolute heading. Show exact leg-angle L definitions for +/-L and whether a calibrated external heading/angle reference changes what can be tested. Any magnetometer or Android rotation-vector use is an explicitly different experimental modality and must not be silently mixed. E05 must not force a yaw trial to distract from the primary roll candidate.

## E16 — independent methods veto and trial selection
Not the same author/reviewer lineage as E01/E06/E08. Compare ALT_D DO_NOT_RUN NOW against ALT_A roll ladder 0/45/90/0, ALT_B two-leg yaw and an alternate reference method. Identify falsification information, reference reliability, safety/consent/source risks and possible circular validation for each. If three actor-distinct independently submitted designs have not actually arrived with verifiable GitHub source and rehash, E16 must return INDEPENDENCE_NOT_ESTABLISHED and a scoped recommendation only. E16 cannot set any source hard gate to PASS based on science narrative nor authorize device capture.

## Every deliverable, no substitutions
A: Exact source references (official documentation/DOI/section), with limits of what each proves.
B: At least two practical competing reference protocols, independently estimated metrological uncertainty, hardware/clock requirements and sources.
C: Original mathematical null, observability counterexample and >=5 own hard negative fixtures.
D: Frozen proposed pre-reg before any prospective phone data, with objective units and uncertainty, avoiding invented calibration certificates.
E: Exact signed/registered GitHub actor, source commit and SHA256SUMS, authored independently or explicitly SELF_DECLARED_UNREGISTERED; PREEXPOSED label and independence lineage.
F: 14 frozen R39 hard gate support table including EVIDENCE_MISSING/OPEN status; no positive claim without actual source.
G: One explicit DO_NOT_RUN result and strongest argument against the author's preferred method.
H: Machine-readable return with evidence_type DESIGN_ONLY, measurements NOT_RUN, no automatic GitHub merge, no device/APK/Hostinger/WWW action.
I: Secondary actor independent GitHub source-byte rehash and review, or record SECOND_PARTY_NOT_ESTABLISHED.
J: Private R37 original/OPPO hashes never published into public CAS or borrowed from an older secondary report.

## Timing and boundaries
This is the FINAL TARGETED Stage1 METHODS QUESTION before future physical readiness adjudication; not an authorization to repeat indefinitely. Cursor can separately close source/stop/build/receiver requirements in original R40 Issue392, but any sensor start requires future specific operator one-shot authorization. Scientific Stage1 recommendations cannot override 14 OPEN/HOLD hard gates.
NEXT = REGISTER_INDEPENDENT_ACTORS -> SOURCE_EXACT_STAGE1_RETURNS -> AXIOM_METHODS_CROSSADJUDICATION -> PER_GATE_CURSOR_EVIDENCE -> DECIDE_HOLD_OR_SEPARATE_OPERATOR_SCOPE.
