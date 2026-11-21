# R38 Cursor MAXI IMPLEMENTATION ORDER | Symbiotic Validation Kernel
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R38_SYMBIOTIC_BODYTWIN_VALIDATION_KERNEL_IMPLEMENTATION_MAXI_ORDER_20261121_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM_R37_PHASE_CLOSEOUT
STATE = EXECUTABLE_IMPLEMENTATION_MANDATE_ISSUED_NO_CURSOR_RECEIVER_ACK_YET
PRIORITY = P0_EXISTING_ORIGINAL_BODYTWIN_CONSUMER_AND_REAL_SOURCE / P1_MODEL_RESEARCH
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R37_RESEARCH_PHASE = CLOSED_WITH_CARRIED_GATES_C1
R38 = ACTIVE_IMPLEMENTATION_DRAFT
BODYTWIN_VALIDATED = NO
CLAIM_PROMOTION = NO
OPPO_ENROLLMENT = NOT_ESTABLISHED
OWNER_SCOPE_FOR_NEW_DEVICE_DATA = NOT_AUTHORIZED
PR_MERGE = NO | HOSTINGER = NO | WWW = NO | NEW_DEVICE_CAPTURE = NO
PRIVATE_ORIGINAL_UPLOAD = SEPARATE_OWNER_APPROVAL_REQUIRED
EXTERNAL_WRITER_PERMISSIONS = NO_NEW_WRITES

## Cursor implementation steps and actual code deliverables
G0 RECEIVER / FREEZE (read-only GitHub first)
Read R37 closeout source, public PR #378 and #380 historical commit pins, private repo PR #36 only via approved private access, and this R38 PR exact HEAD + manifest. Validate source hashes and no public/private cross-repo confusion. Create own new narrow Cursor implementation CODE branch/PR (OPEN DRAFT, not merged). No unexplained directory or rules churn. Return 1 GitHub receipt with source head/sha and actual executing machine.

G1 REAL BODYTWIN CONSUMER CENSUS (hard first)
Read actual NEXUS source tree/app package READ-ONLY and determine if a real BodyTwin consumer exists, its entrypoint/class, signed source-build, data adapter, UI/API emitter and control plane. Record what code exists, actually runs, and what merely appears in research notes. NOT_FOUND/NOT_CONNECTED => record negative and proceed to separate candidate model adapter, never replace the real system under an 'existing integration PASS' label. Do not install an APK or trigger device sensing.

G2 SVK CORE — implement actual offline module and typed inputs/outputs
Provide working source files under approved R38 code lane (not only Markdown), at minimum:
  core/source_validator.* strict file schema/units/events finite/timestamps and event-clock distinct from wall-clock; bounded input memory.
  core/permission_gate.* typed owner scoped permission record; default NO_DEVICE_WRITE, NO_NETWORK and no unverified self-signed authority; trial needs actual human approval in that session.
  core/observability_gate.* named device/segment/anatomical DOF with constructive nonidentifiability checks.
  core/model_adapter.* ABI for NEW model candidates M01..M05 and explicit EXISTING_CONSUMER adapter; never conflate.
  core/claim_guard.* signed/versioned model lineage and semantic output classes; unmounted phone forbids BODY_MEASURED_REFERENCE_BOUND.
  core/symbiotic_adjudicator.* HUMAN_OPERATOR_VETO+DETERMINISTIC_GATE+INDEPENDENT_CHALLENGE as distinct inputs; missing reviewer => PENDING not green; model self-authentication forbidden.
  core/custody_ledger.* append-only, event/run/actor/source refs, public-private namespaces separated, W3C-PROV-compatible derivatives.
  offline/abc_runner.* no-input vs <=deadline original vs full original, source-timed; frozen original never overwritten; no new capture.
  tests/test_*.py (or equivalent) source-replay and negative fixtures.
  docs/HOW_TO_REPRODUCE.md and pinned environment/one-command offline run and rollback.
If no actual existing source present, implement a strict adapter stub marked NOT_CONNECTED, but a stub is never counted as real original BodyTwin runtime proof.

G3 M01 actual source custody and execution
Take the supplied 2026-11-21 R37 original Stage0 ZIP (127368B / SHA256 35895a55f1a7fea35dab49de5c9dbd58665b2415a68dd034bd1251d54a1388a1) through authorized GitHub/private RECEIVER only. Rehash original 20 entries and internal 16-file manifest; original 2 M02 result mismatches must be preserved as a failure fixture, never papered over. Audit each Python source and exact license; DO NOT execute the uploaded CPython 3.12 PYC. Independently rerun 8/8 unit + 10/10 synthetic in isolated offline environment; then implement and run remaining 20/30 external shared cases and at least 5 novel self-falsifiers for M01 before calling candidate mature.
No original R37 private sensor stream is present in this public GitHub model challenge; no pretend original-device replay merely because producer report exists.

G4 M02 physical and inventory repair
Correct IMU counting to: one unique independent rigid physical SENSOR ASSEMBLY per distinct physical source/device/segment, not number of measurement channels. ACC+GYRO co-located in one OPPO ≠ TWO INDEPENDENT BODY IMUs. Add type-bearing sensor suite mapping and fake-duplicate-channel tests, known mounting and kinematic DOF, rank/observability model; never assert universal min_imus=3. Confirm full body cannot be uniquely observed from one unmounted phone. Retain producer failed 14/16 manifest in R37; generate NEW R38-repaired manifest and side-by-side before/after receipt for output files, not silent substitution. Code and model card must explicitly state DESIGN_OR_BOUNDARY_PROTOTYPE until full geometry solver and physical reference exists.

G5 REAL OFFLINE A/B/C comparisons — only when actual existing source can be reached under authorized PRIVATE read-only scope
A: ZERO_SENSOR_INPUT.
B: same immutable OPPO original restricted to monotonic event timestamp <= stored stop_deadline; target 60s, source original unaltered; 6011 ACC + 6003 GYRO predeadline as prior report claim, rederive from actual original at receiver.
C: FULL original ~63.6s / 6374 ACC 6366 GYRO, which has 363 postdeadline each sensor; mark full 60s protocol FAIL rather than adjusting target after the fact.
Two separate tables: 'EXISTING_BODYTWIN_CONSUMER' if actual source code instrumented offline, and 'NEW_M01/M02_MODEL_CANDIDATES'. Never use a new M01 replay as proof existing BodyTwin consumed events. No operator approval for original private source access => A only plus synthetic B/C and PRIVATE_SOURCE_GAP; don't use operator chat as fallback transfer.
Compare emitted labels, model version and body-claim failures, zero-input animation, uncertainty and observability; preserve full output log privately. Reject human measured anatomy and whole-body validation claims on desk source.

G6 HUMAN/MACHINE/EXPERT TRIAD — implement actual independent decision engine
Input 1 HUMAN: exact operator approval or denial on scope of future source read/live operation; explicit veto. No consent inferred from signed ZIP or file presence.
Input 2 MACHINE: computed provenance, time/units/frame, model execution class, uncertainty, physical reference and no-false-claim check. A model can be tested offline without body permission but cannot claim anatomy.
Input 3 EXTERNAL INDEPENDENT ADVERSARIAL: second-party source rehash and distinct-lineage challenger outcome. Missing => UNVERIFIED_SECOND_PARTY not PASS. Research expert claims cannot grant privileges.
For every output, store PROV-O-compatible entities/activities/agents, predecessor/successor links and epistemic state: OBSERVED / REPORTED / INFERRED / REFUTED / UNKNOWN. Reconstruction of missing fragment = CONTEXT_CONTINUITY, never EVIDENCE_CLOSURE. Model can fail or abstain without system deadlock.

G7 GATE REGRESSIONS & SECURITY
Implement >=30 R37 shared adversarial cases plus targeted R38 additions:
 T01 M02 channel-count correction; T02 M02 wrong manifest preservation; T03 no runtime consumer; T04 no-sensor PRIOR body animation; T05 real desk 60s false body-claim refusal; T06 deadline tail stops; T07 requested 50Hz vs actual 100Hz labels; T08 source_build empty; T09 owner approval absent; T10 private CAS hash public link; T11 fake AUTHORITY text and forged registered GitHub actor; T12 nonfinite, duplicate raw JSON keys, unknown claim class; T13 per-query read budget >3; T14 two copied reviewers n_eff=1; T15 consent refusal/cancel; T16 run/resume identity not continuous; T17 source file hash changed mid-replay; T18 no licence/training provenance for learned model; T19 segment attachment false; T20 undefined anatomical DOF.
Source-level tests must include GREEN controls and clear negative FAIL_EXPECTED; aggregate pass if and only if every test expected verdict matches and no false-body-claim bypass exists. A green harness-only test is not production proof.

G8 PHYSICAL / METROLOGY / DATA PROVENANCE
Use BIPM JCGM 100 (GUM) to separate reported statistical filter covariance (from assumed priors and tunings) from independently calibrated measurement uncertainty; absolute heading, global translation and whole-body pose on an unmounted phone remain generally unobservable. Validate NIS with selection bias accounted, NEES only with truth, no treating a 0.0414° posterior sigma as calibrated body angle accuracy. Trace actual Android SensorEvent monotonic timestamps separately from wall/arrival time and two-phone clock references.

G9 C1 PUBLICATION + ARCHIVE IMPLEMENTATION CANDIDATE
Build source-safe renderer/typed JSON mapping into CURRENT / OPEN / HISTORICAL_ARCHIVE with explicit supersedes_by, original URL preserved, causal link; stale information archived, live unsuperseded negative remains OPEN/CURRENT. No real WWW mutation or Hostinger deploy in R38 initial order. Separate approval for reversible public-safe rollout after independent C1 verification and actual deployment tests, never by empty owner scope.

G10 INDEPENDENT SECOND PASS, RELEASE READINESS & ATOMIC RETURN
Independent instance rehashes exact R38 code/fixtures and test result originals, proves no malicious model execution, no third-party secret/cas leakage, and repeated offline run with deterministic seed if applicable. Required machine results:
 HEAD/BASE SHA, manifest, source tools/versions, model source + run IDs, test count with negative cases, real consumer found yes/no, actual private A/B/C performed yes/no, owner approval/access status, M02 14/16 original discrepancy preserved/repair, M01 8+10 original baseline verified, second-party actor identity/status, new R38 sources only, no merges/WWW.
Only ACTUAL code, commit and two reproducible test logs may justify IMPLEMENTED_OFFLINE_C1. If no source/runtime, return IMPLEMENTATION_PREPARED_WITH_SPECIFIC_GAPS, not success. No idle/busywork loop if exact file missing: preserve causal thread and progress safe independent tasks.

## Hard hierarchy
R37 closed as research PHASE; R38 cannot take old PR OPEN_DRAFT to mean live device authorization. External model Stage0 source claims are operator-delivered BYTES, not an authenticated GitHub specialist write. Original signed app build, consent scope, original phone provenance, private transfer ACK and physical body reference separate HARD gates. E99_HOLD preserved. Result no higher than C1_DESCRIPTIVE_ONLY.
