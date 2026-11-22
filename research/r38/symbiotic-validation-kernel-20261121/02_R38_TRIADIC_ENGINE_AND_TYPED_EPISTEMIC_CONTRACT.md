# R38 deterministic symbiotic validation — machine and human authority protocol
OBJECT = NEXUS_OMEGA_AXIOM_R38_SYMBIOTIC_VALIDATION_DECISION_PROTOCOL_20261121_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CURRENT_IMPLEMENTATION = SPEC_ONLY_NOT_EXECUTED
PHYSICAL_HUMAN_BODY_REFERENCE = NOT_ESTABLISHED
BODYTWIN_VALIDATED = NO
PRODUCTION_WRITE_AUTHORITY = NONE

## Source graph and disciplined three parties
SYMBIOSIS is a governance workflow, not human/machine cognitive equivalence:
- OperatorHuman: independent explicit scopes, decisions to approve/veto a bounded future action; can choose research goal, cannot logically declare missing evidence observed.
- MachineVerifier: deterministic source-bound functions for original-source byte integrity, lawful scope, type, units, frames, clocks, nonfinite/duplicate rejects, physical observability and claim ceilings. It may produce UNKNOWN and REPORTED_ONLY.
- AdversarialReviewer: other actor and other execution/inspection provenance challenges positive and negative cases, ties lineage to true distinct parent sources and catches false source/authority equivalence; cannot impersonate operator authorization.
An independent reviewer can disagree with machine/other reviewer; no majority vote upgrades missing physical evidence. Human veto is a hard no-action boundary, not 'ground truth' of sensor physics.

## Triadic decision state transition
PROPOSED -> SOURCE_AUTHENTICATED_OR_SCOPE_GAP -> IN_QUARANTINE -> SYNTHETIC_EXECUTED -> PRIVATE_SOURCE_REPLAY_CONDITIONAL -> CHALLENGED -> C1_ADJUDICATED_SCOPED -> PUBLIC_SAFE_CANDIDATE -> SEPARATE_DEPLOY_AUTHORIZATION.
Each arrow records {old_state, new_state, run_id, actor_id, timestamp_utc, source_commit, original_scope, exact_test_ids, evidence_refs, causal_parent_refs, uncertainty, gate_reason}; a SOURCE_GAP means the edge is missing and the next state cannot be asserted. Tests in safe lanes may proceed even if private sensor access remains blocked.

## Typed inputs
SourceArtifactRecord = {id, origin_kind, access_class, exact_repository, path, bytes, sha256, independent_actor_ref, issued_timestamp, source_clock_domain, sample_units, source_version, original_vs_derived}.
Origin classes = PRIVATE_DEVICE_ORIGINAL, PRIVATE_EXPERT_RETURN, PUBLIC_LIBRARY, SYNTHETIC_FIXTURE, REPORT_ONLY, UNVERIFIED_UNTRUSTED.
SourceLineage = {original_ref, parent_chain[], missing_ref[], derived[]}. Missing not silently replaced.
OwnerScope = {verified_owner_identity_private, device_id_private, app_signing_evidence, sensors, duration, storage, start_stop_witness, timestamp, action, allowed, revocation}. Null or unverified -> NO_DEVICE_CAPTURE, NO_PRIVATE_NETWORK_TRANSFER, NO_HUMAN_CAPTURE; PRIVATE_READ_ONLY subject to separately authorized existing source access.
DeviceStream = {source_id, source_type, device_physical_sensor_count, channel_count, channels[], sensor_clock, monotonic_window, rate_source_hz, units, frame, reference_status, body_mount_status}. Counting channel names as independent IMUs fails.
ModelRun = {model_commit, src_sha256, code_kind, source_sha, version, type: EXISTING_ORIGINAL_BODYTWIN | NEW_RESEARCH_CANDIDATE, actor, exact_runtime_evidence, input_src, output_src, mode: OFFLINE, run_id, seed, test_suite_version}.
Challenge = {challenger_id, real_actor_registration, independent_source_lineage, test_result_by_id, observed_sha256, code_version, conflict_list}.
PublicClaim = {claim_type, physical_entity, source_class, observable_dof, estimate, uncertainty, mounting_reference, valid_from, predecessor, successor, visibility}.
No untrusted model output may submit permissions, issue instructions, define its own authority labels or change these enums.

## Typed outputs
PHONE_ACCEL_OBSERVED | PHONE_GYRO_OBSERVED | PHONE_STATIC_CANDIDATE | DEVICE_ORIENTATION_ESTIMATED | DEVICE_BIAS_ESTIMATED | UNOBSERVABLE_DOF | JOINT_ESTIMATE_REFERENCE_SCOPED | GENERATIVE_BODY_PRIOR | UNSUPPORTED_BODY_MEASUREMENT | MODEL_NOT_CONNECTED | SOURCE_GAP | AUTHORITY_GAP | PRIVACY_FAIL | EVIDENCE_C1_DESC.
NO claims BODY_MEASURED_REFERENCE_BOUND/JOINT_ANGLE_MEASURED unless a separately authorized and independently verified calibrated wearable/reference body trial supports that precise targeted DOF. An unmounted desk-phone run always returns NO_BODY_OBSERVED, regardless of model score or human admiration.

## Gate formula
source_ok = independent original byte verification + correct source class + actor provenance for asserted scope
consent_ok = exact permitted operation; may not be inferred from operator conceptual research approval
semantic_ok = every physical claim supported by actual mounted/reference observability
privacy_ok = no private raw rows, identifiers or shared CAS content digest in public derivative
model_ok = source code/env tested, no accidental old consumer substitution
independent_ok = second true source and toolchain verified for claims requiring independent witness
c1_candidate = source_ok AND consent_ok_for_that_operation AND semantic_ok AND privacy_ok AND model_ok AND independent_ok
No averaging, weighted vote, ternary state 'neutral' or generic self-declared SIGNED prefix may override false components. If consent for purely synthetic local test is N/A, document NO_DEVICE_ACTION and no person, not fake owner approved.

## Stateless/replay proof
Validate no hidden global state carrying approval across independent run IDs, disallow replay of old owner scope for a new capture; preserve file-original hash while creating derived predeadline subset. Label run states STARTED, STOPPED, FAILED, SUPERSEDED and UNKNOWN; only exact execution receipt proves actual run. A syntactic GitHub issue comment is not trusted private source receipt.

## Causal memory
Use PROV-O-compatible source entities/activities/agents; maintain three exposed states on website: CURRENT (supported current C1), OPEN (unresolved or current negative limitation), HISTORICAL_ARCHIVE (only superseded content, not deleted). Every replaced claim includes exact predecessor, reason, first-seen and supersession evidence. Old URLs resolve to archival content with current successor. No Hostinger change authorized by this R38 implementation PR; renderer should be tested locally first.
