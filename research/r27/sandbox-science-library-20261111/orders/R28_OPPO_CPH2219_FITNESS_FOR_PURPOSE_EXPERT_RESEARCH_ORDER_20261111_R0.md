# NEXUS OMEGA — R28 / OPPO CPH2219: Independent Expert Fitness-for-Purpose Research Order

OBJECT = NEXUS_OMEGA_R28_OPPO_CPH2219_INDEPENDENT_FITNESS_FOR_PURPOSE_EXPERT_RESEARCH_20261111_R0
STATE = OPERATOR_ISSUED_PUBLIC_SAFE_RESEARCH_ORDER_DRAFT_PR_NOT_MERGED
DATE = 2026-11-11
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
SENDER = AXIOM (scientific governance and source audit, not device executor)
RECIPIENT = INDEPENDENT_SELF_IDENTIFIED_EXPERTS
RECEIVER = NEXUS_OPERATOR_AXIOM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SCOPE = EXTERNAL_RESEARCH_ONLY; NO_DEVICE_ACTION
PHYSICAL_CALIBRATION = NOT_ESTABLISHED
RESEARCH_EXECUTION = NOT_CLAIMED
R28_SEAL_REHASH = CURSOR_REPORTED_MATCH_NOT_INDEPENDENTLY_REHASHED_IN_THIS_PUBLIC_ORDER
EXTERNAL_GITHUB_ACTOR = NOT_REGISTERED; WRITE_SLOT = NOT_ALLOCATED
PR33_PRIVATE_CUSTODY = OPERATOR_REPORTED_OPEN_DRAFT_NOT_MERGED; NO_PRIVATE_SOURCE_TRANSFER

## 1. Exact predecessor and order of authority

PREDECESSOR_OBJECT = NEXUS_OMEGA_R27_NEUTRAL_INDEPENDENT_EXPERT_SANDBOX_LIBRARY_MANDATE_20261111_R0
PREDECESSOR_REPO = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PREDECESSOR_COMMIT = a0851058f4bfcf4b376628f7f362b8cfdedab80d
PREDECESSOR_PATH = research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md
PREDECESSOR_BYTES = 4241
PREDECESSOR_SHA256 = 2268fe2c1905951facdf0fad35da6483ef76f148c9893b49b2efdb96a7650d16
PREDECESSOR_GIT_BLOB_SHA1 = ea3413388876c747c5c4a3e182fe8117b8efe06d

Retrieve pinned predecessor before work:
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/a0851058f4bfcf4b376628f7f362b8cfdedab80d/research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md

Read, in order: AGENTS.md; GOVERNANCE.md; docs/AI_CONTEXT.md; docs/agent-protocol.md; docs/architecture/REPOSITORY_STRUCTURE.md; docs/governance/REPOSITORY_ORDER_POLICY.md; docs/governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md; docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json; docs/governance/NEXUS_OMEGA_TASK_ANCHOR_NORM_V1.md; and the R27 neutral mandate. All exist at the immutable predecessor commit. This is an **additive owner-authored research assignment inside the existing R27 Science Sandbox**, not a reclassification of R28 physical testing, a separate sandbox runtime, a new repository, or a permission grant. Predecessor changes must be published as new versions, not a rewrite.

## 2. Causal handoff: what is and is not established

Operator/Cursor chat reports: R28 original transfer ZIP 25,890 bytes / SHA256 d591e7503cb1396b433894952fdb994dc79e91368096400c8bec57ac4b23952d; R28 return-seal ZIP 6,394 bytes / SHA256 9cd651007ad4d8500008d067e1ce93cc371469dc849105c44bf9d24f1ab6e956; reported MATCH; tip ALREADY_BOUND; primary status TURN_ENDED_SUCCESS; next hardware/Windows host receipt pending. These are **reported** physical custody facts here: original transfer bytes and device are not in this public mandate, and neither seal implies metrological validity. No real OPPO sensor-gain/bias/cross-axis calibration has been proven by this document. Previous private PR #33 is **not** merged; avoid quoting private paths, source trees or content.

An operator-transmitted DeepSeek assessment recommends independent fitness-for-purpose peer criticism. This is an unsealed secondary research opinion, **not** a PTB/EURAMET certification or a mandate that professional bodies have inspected this device. Verify independently whether each cited institutional standard applies. External experts may reject the rationale, design, outcome and even the need for hardware modification.

## 3. Research question / allowed independence

Can the planned, user-consented, non-destructive OPPO A74 / CPH2219 IMU observation and calibration procedure produce measurements **fit for the explicitly stated NEXUS operational purposes**, with defensible uncertainty and falsifiers, without conflating signed bytes, synthetic tests, Android virtual sensors, six-position self-checks and traceable physical calibration?

Every expert considers A/B/C **fully** from the R27 neutral mandate, then applies them to R28/D. Competence dimensions (not mandatory role assignments): (1) metrology/uncertainty, (2) MEMS/IMU system identification, (3) Android Sensor HAL and power/timing, (4) experimental design/statistics, (5) trustworthy offline-first custody, (6) independent adversarial methods. No provider is reserved a preferred conclusion. Experts declare provider/model/version/developer if actually known, interface, source access, tools actually used and conflict-of-interest. Independence of model family, provenance and instrumentation must be assessed, not presumed.

## 4. Required research lanes and falsification agenda

### A — Ledger and CAS
Assess event sequence, immutable source hashes, end-to-end device→private server receipt, monotonic append, deletion/truncation, replay, chain-fork and external checkpoint survival. Counterexample: valid per-chunk SHA256 with silently omitted final chunk; show detector and its failure case. A stored manifest is not a sensor reading.

### B — State and measurement guards
Define explicit statuses OBSERVED, SOURCE_GAP, UNSUITABLE, REQUIRES_REAL_REFERENCE, CONDITIONAL_FFP, and REJECTED. Reject NaN/Inf, duplicate keys, unknown fields, clock regressions, sensor-type confusion, unit mismatch, orientation mislabel, not-observed fallback, data leakage and post-hoc decision thresholds. Assess safety of state transitions, corrections and rollback; formal/spec-level checks only.

### C — Transport, consent and custody
Compare offline-first local capture/queue plus private CAS receiver, user-visible recording, stable readback, TLS/authentication and no mandatory ADB/USB in production. Model bounded failures: network outage, retry after acknowledgement loss, duplicate delivery, consent revoked during upload, key rotation, clock skew, interrupted battery/thermal run, reinstall and storage exhaustion. No private device paths, keys, raw readings, serial numbers or live endpoint tests in public research.

### D — Metrological fitness for intended use (R28-specific)
D0: Define **measurand** and target quality separately for (i) stationary gravity/accelerometer bias and scale, (ii) gyro zero-rate drift where gyro exists, (iii) sampling/timebase quality and (iv) downstream SR-UKF/NIS/NEES analytics. Target uncertainty/error bounds MUST be derived from the actual downstream task and available reference, not made up to force a pass.
D1: Distinguish VIM calibration, adjustment, verification, validation, metrological traceability and measured-versus-reported app performance. Manufacturer sensor listing does not prove the exact unit's HAL/API availability or calibration accuracy.
D2: Build a physical/reference inventory: exact CPH2219 unit, hardware/firmware/Android build, sensor vendor/name/version/type, nominal range/resolution, reported accuracy, vendor compensation, timestamp behavior, coordinate frame, host/cable/USB mode, battery/temp, original capture schema. Device identifiers and raw logs remain private.
D3: Evaluate a **proposal** for stationary-rest baseline plus six **known** approximately orthogonal gravity orientations, repeated on separate sessions, with holdout orientations and thermal strata. Six faces may support limited bias/scale inference given justified assumptions; do NOT claim they identify a full arbitrary 3×3 cross-axis/non-orthogonality matrix, temperature behavior or dynamic gyro response.
D4: Specify observation model such as y_a = M_a R^T g + b_a(T,t) + epsilon with independent reference/orientation uncertainty, gravity value and covariance assumptions documented. Assess identifiability/rank, repeatability, hysteresis, stability, noise/Allan deviation, drift, sensor fusion, clipping, outliers and raw/uncalibrated API semantics; compare against competing nulls (bias-only, scale-only, no correction, reordered history). No estimation of physical parameters without real measurements.
D5: Pre-register split by session/day/orientation/temperature rather than random correlated events. Budget measurement uncertainty with Type A and Type B components per JCGM/GUM and dependence-adjusted confidence. If no independent truth/traceable reference, report RELATIVE_OR_INTERNAL_CHECK_ONLY; do not report traceability or absolute accuracy.
D6: Preflight host & device **without operating it here**: design checks for authorized Windows host receipt, Type-C data cable capability, device consent, app identity/signature/rollback, user-controlled time bounds, read-only export and no silent sensor capture or destructive platform calibration.
D7: Downstream UKF: NIS without NEES reference is not independent ground truth. Cross-check noise and coverage on held-out real sessions against nulls, preserve observed misfit, and forbid C2 or medical/neural/Bodytwin promotion.
D8: Require a decisive falsification condition for every optimistic claim: divergent timestamps/units, HAL virtual/physical ambiguity, apparent improvement only on training faces, temperature shift, cross-axis residuals, session-order dependence, corrected stream copying the same virtual sensor, no actual physical reference, or reproducibility failure.

## 5. Negative test matrix / mandatory counter-evidence

For each lane A/B/C/D list input, attack, observable detector, expected result, actual evidence tier, and scope of claim. At minimum research 16 distinct adversarial cases:
N01 manifest MATCH but wrong sensor type; N02 units m/s² vs g; N03 switched ±face label; N04 unknown orientation; N05 non-monotonic timestamps; N06 duplicate timestamp; N07 Android requested rate unequal observed rate; N08 corrected vs uncalibrated stream confused; N09 device warm-up drift; N10 temp covariate absent; N11 held-out orientation residual increase; N12 six-face fit falsely asserted as full matrix identification; N13 device reboot/app update; N14 no real reference but false traceability claim; N15 chunk-loss/replay/duplicate server ACK; N16 consent revoked mid-transfer. Add privacy, independence and NIS/NEES failure fixtures as appropriate. A single unmitigated critical measurement/provenance failure prevents a positive fitness-for-purpose recommendation for the affected use.

## 6. Research outputs and classification

A self-identifying expert produces:
E1 source-exact bibliography (official/primary vs secondary, retrieval UTC, legal terms, source URI and pinned version where attainable; SHA256/bytes only if actually recomputed; do not invent);
E2 claim / counterclaim / adversarial test table for A/B/C/D;
E3 uncertainty and traceability gap inventory, clear target-use-specific tolerance rationale;
E4 proposed preregistered physical protocol and non-destructive host acceptance gates, **not executed**;
E5 graded outcome PER_USE_CASE: SUITABLE_CONDITIONALLY, INSUFFICIENT_EVIDENCE, UNSUITABLE_FOR_PURPOSE, or CONTRADICTED, with scope and explicit dissent. Approval for execution is **never** inferred;
E6 detached child hash manifest with real byte lengths/digests and declared producer GitHub actor or NOT_ESTABLISHED.

Evidence tiers: T0_VERIFIED_ORIGINAL, T1_AUTHENTIC_OFFICIAL_SOURCE, T2_SECONDARY, T3_HYPOTHESIS. Mark every claim STATIC_REVIEW, ACTUALLY_RUN or NOT_EXECUTED. Do not convert proposed test into tested test.

## 7. Repository order law, concrete permitted/prohibited paths

THE ONLY PUBLIC SCIENCE ROOT = nexusomegac27/NEXUS-OMEGA-EVIDENCE. Research lives at research/<phase>/<agent-or-topic>/; existing owner order home is research/r27/sandbox-science-library-20261111/orders/. Content-addressed evidence: objects/ plus index/. Communication provenance: communication/. Owner-controlled stable documentation: docs/. Schemas: schema/. Tools: scripts/. Tests: tests/. Validation fixtures: validation/. Examples: examples/. No root dumps or unsolicited archive imports. This order's owner-authored file and linked source index remain within pre-existing orders/; owner-controlled receipt within pre-existing receipts/. No new top-level directory, standalone expert repository, history move or structural policy edit. A new structure requires an operator-only coordinated README + docs/architecture/REPOSITORY_STRUCTURE.json (+ affected docs) change and validator execution.

**External researchers: GITHUB_CREATE=DENY, GITHUB_EDIT=DENY, DIRECTORY_CREATE=DENY, MERGE=DENY** because docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json currently lists external_actor_allowlist=[] and no R28 assignment. They may submit research out-of-band through OPERATOR_TO_AXIOM_BRIDGE, or use an independently operator-preallocated exact future slot after verified GitHub login and enforced branch controls. The historical R27-E seven-file slot is unrelated and forbidden for this assignment. Issue #93 is a *passive* return index, not an executing agent, signed identity or authorization. Do not assume a model name is a GitHub login.

EXECUTION=READ_ONLY_DESK_RESEARCH. Do not fetch private source via guessed credentials, run untrusted fragments, touch OPPO/Pixel, reset devices, alter app or Hostinger, write WWW, start calibration, generate production keys, bypass consent, release private data, auto-merge, auto-deploy, forge a physical receipt or self-issue AXIOM ACK. Preserve original history, negative evidence, checkpoints and device state. Drift reset = read exact source and append difference witness; NEVER node reset or memory erasure.

## 8. Receiver and return handshake

RETURN_RECEIVER = NEXUS_OPERATOR_AXIOM
PASSIVE_INBOX = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93
RETURN_TRANSPORT = OPERATOR_TO_AXIOM_BRIDGE_UNTIL_ACTOR_REGISTERED
RETURN_MANIFEST = schema/expert-hash-handshake-v1.schema.json
ORDER_OBJECT = NEXUS_OMEGA_R28_OPPO_CPH2219_INDEPENDENT_FITNESS_FOR_PURPOSE_EXPERT_RESEARCH_20261111_R0
ORDER_SHA256 = CALCULATE_FROM_THIS_EXACT_FILE_AFTER_GITHUB_WRITE; DO_NOT_INVENT
PARENT_COMMIT = a0851058f4bfcf4b376628f7f362b8cfdedab80d
PARENT_SHA256 = 2268fe2c1905951facdf0fad35da6483ef76f148c9893b49b2efdb96a7650d16
RECEIVER_ACK = PENDING_AXIOM_INDEPENDENT_REHASH
CLAIM_PROMOTION = FALSE
CANONICAL_INTEGRATION = NONE
PHYSICAL_CALIBRATION_AUTHORIZATION = NONE_BY_THIS_ORDER

Authoring agent supplies source/readback links; Operator/AXIOM independently verifies bytes, claims, privacy, method and constraints. No producer-issued receiver ACK. Reasoned dissent and an evidence-limited rejection are valid successful research outcomes.

## 9. Decision routing

Desk research can start now using public references and **no device effect**. A final FFP decision may be formulated only for use cases with actual representative observations, independently checked references and uncertainty/risk thresholds. Any calibration execution requires later separate operator-controlled, source-exact, non-destructive physical receipt and authorization. PR33 remains private, DRAFT and unmerged. Independent research NEVER performs PR33 merge or physical calibration.

~~~text
CANONICAL_NEXT = EXPERT_DESK_RESEARCH_A_B_C_D
HARD_DEVICE_GATE = WAIT_TYPE_C_REAL_OPPO_OR_WINDOWS_HOST_RECEIPT
R28_PHYSICAL_EXECUTION = NOT_STARTED_OR_NOT_ESTABLISHED
EXPERT_WRITE_AUTH = DENY
RECEIVER_ACK = PENDING
C1 = DESCRIPTIVE_ONLY
~~~
