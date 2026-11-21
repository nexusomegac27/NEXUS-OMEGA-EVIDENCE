# R38 offline actual-consumer A/B/C differential and independent model adapter
OBJECT = NEXUS_OMEGA_AXIOM_R38_OFFLINE_ACTUAL_BODYTWIN_CONSUMER_AND_MODEL_ABC_REPLAY_20261121_R0
STATE = EXECUTION_DESIGN_NOT_REAL_CONSUMER_TEST
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED = NO
NO_NEW_DEVICE_CAPTURE = YES
NO_OPPO_NETWORK_UPLOAD = YES

## Two distinct executable interfaces
ActualConsumerAdapter: wraps actual shipped NEXUS BodyTwin entrypoint after source/build read-only census. output source = real app/runtime source build with exact git commit. No actual consumer found => NOT_CONNECTED. No shadow/mock agent may produce a green 'real consumer' result.
CandidateAdapter(M01..M05): wraps newly received independent model code in unprivileged offline sandbox, signature model_version+code_hash+rights; output always NEW_RESEARCH_CANDIDATE. M01 source-only baseline independently 8/8+10/10, not equivalent to existing NEXUS consumer. M02 current prototype is boundary-only, source seal mismatch.
Both implement offline interface:
Adapter.load(source_version, immutable_model_blob, restrictions) -> capability_or_NOT_CONNECTED
Adapter.run(data_stream, run_mode, source_clock, fixture_metadata, immutable_evidence_context) -> TypedOutput
Adapter.describe_observed_dof() -> explicit frames/units + known observability
Adapter.abort() -> bounded stop + no further model reads/permissions

## A/B/C exact deterministic sequence
A: NO_SENSOR_INPUT, empty source -> no measured person, candidate prior-generative animation only as model hypothesis.
B: archived existing OPPO source, only event timestamps <= original monotonic deadline. User-provided prior measurements claim 6011 ACC and 6003 GYRO, actual count must be independently recalculated by Cursor from original source. NO write to original, output C1 private derivation, exact source-domain.
C: same original full sensor stream including 363 postdeadline ACC +363 GYRO, 6374 ACC +6366 GYRO; DURATION_PROTOCOL_FAIL as 60s, may be processed for scientifically separate descriptive comparison.
All three have unique run IDs with parent original and model sha, permission scope, explicit timebase. Full archive preserved. 50Hz preplanned versus 100Hz source actual not silently reconciled.

## Hard checks
SOURCE_ONLY_USER_REPORT != PRIVATE_ORIGINAL_RECEIPT. If actual phone original missing in private authorized receiver, no fake B/C: run A plus synthetic B/C, return PRIVATE_REPLAY_NOT_AUTHORIZED_OR_SOURCE_GAP.
No anatomical pose from unmounted phone. If algorithm returns a whole-body pose prior, label GENERATED_PRIOR_NOT_MEASURED with uncertainty/observability and real source trajectory. If a runtime UI/API emits BODY_MEASURED, JOINT_ANGLE_MEASURED, BODYTWIN_VALIDATED, requires nonpresent independent human reference and mounting: FAIL_UNSUPPORTED_ANATOMY.
If outputs identical for A and B or C, no inference that measured phone informed human body; causal countermodel of prior animation. If outputs differ, not proof of physical body truth, only evidence input influenced model.
Calculate per channel rate from sensor-event deltas, wall separately, explicit deadline, stop delay and samples accepted after deadline. Use no hidden clock resynchronization.

## Runner requirements
Deterministic environment pinned seed/runtime; code and input whitelisted; network-disabled; readonly original; run single record per mode; reject nonfinite, duplicated source, wrong units; bounded CPU/memory/time; safe serialized types only, no pickle, no arbitrary dynamic imports from downloaded models.
Return 3 source-proof/output rows per runnable adapter with hashes in authorized private receiver, C1 public summary containing only sanitized counts and statuses. Requires independent reviewer/source readback before marking adjudicated.
No connected app/owner evidence -> STOP, not long source-finding loop. Cursor may implement and test harness with synthetic inputs in parallel while missing private file stays a source gap.
