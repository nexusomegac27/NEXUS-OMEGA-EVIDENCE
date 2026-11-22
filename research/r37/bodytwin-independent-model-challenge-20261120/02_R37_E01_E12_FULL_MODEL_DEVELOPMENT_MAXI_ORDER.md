# R37 — MAXI ORDER: independently authored COMPLETE BodyTwin architectures and prototypes
OBJECT = NEXUS_OMEGA_AXIOM_R37_EXTERNAL_BODYTWIN_INDEPENDENT_FULL_MODEL_DEVELOPMENT_MAXI_ORDER_20261120_R0
ISSUED = 2026-11-20
STATE = MODELS_TO_BE_AUTHORED_NOT_YET_IMPLEMENTED_OR_VALIDATED
SCOPE = EXTERNAL_RESEARCH_AND_ISOLATED_SYNTHETIC_PROTOTYPES_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
BODYTWIN_VALIDATED = NO
OPPO_PHYSICAL_REFERENCE = NOT_ESTABLISHED
NO_NEW_SENSOR_CAPTURE = YES
HUMAN_CONSENT = OPEN
R36 = OPEN | R37 = OPEN_DRAFT
ALL_RETURNS = GITHUB_ONLY_REGISTERED_C1_SOURCE_CUSTODY
UNREGISTERED_AGENT_WRITE_RIGHTS = DENY_PENDING_REGISTRATION
NO_MERGE_NO_HOSTINGER_NO_WWW_NO_DEVICE = YES

## Research directive — maximum freedom, highest falsifiability
Each principal specialist must deliver their **OWN COMPLETE model from first principle to executable offline prototype**, not merely an analogy, architecture slide or reworded existing NEXUS filter. They may create genuinely novel state spaces, hybrid Bayesian filters, differentiable optimization, geometry-aware factor graphs, learned conditional generative models, physics-coupled skeletons, mixed methods, or a proof that a null-state model is preferable. State clearly which components are borrowed, original, or newly designed and whose license controls each. 'Complete' means the complete RESEARCH PROCESSING CONTRACT and runnable offline demonstrator on available synthetic/public test data; it does NOT imply validated human measurement, training data access or approved production implementation.

### Independent model tracks (each delivers a different self-contained prototype)
M01 — FOUNDATION ZERO / PHONE-TWIN COUNTERMODEL
Develop the smallest observable, typed, source-exact model of only the actual device. SO(3)/gyro integration + gravity-referenced roll/pitch with unknown yaw/global position, timestamps, bias drift and uncertainty. Abstain on body/segment states. Include exactly-zero-input, 60s stationary, post-deadline, wrong-axis and synthetic motion trials. Present as serious alternative architecture and negative benchmark, not an inferior toy.
M02 — GEOMETRIC BODYTWIN / CALIBRATED 2-SEGMENT HINGE
Design a complete body-adjacent 2-IMU rigid-body relative orientation / constrained joint system. Derive mounting transforms, joint axis identifiability, gauge freedoms and yaw ambiguity, with calibrated reference required. Hinge may run with synthetic two-segment fixtures; if neither phone actually worn on known segments, real R37 joint-angle outputs = NOT_OBSERVABLE. Compare factor graph/batch smoother vs one SR-UKF and robust null.
M03 — LEARNED SPARSE-IMU FULL-BODY HYPOTHESIS
Independently build a training/inference research pipeline using genuinely permitted open public motion/IMU datasets, e.g. DIP-IMU/IMUPoser when license and subject-consent/data terms support the use. Conditional pose distribution, attention over source availability, explicit epistemic/aleatoric uncertainty, strong OOD abstention on desk phone, source-aware output class GENERATIVE_PRIOR_NOT_OBSERVED. A single phone may generate a body-like model prior, NEVER a measured full body. Provide dataset splits by participant/session and calibration domain; NOT_TRAINED if compute or licensed data absent. Reference code/weights provenance and no pretense of independently reproduced SOTA scores.
M04 — HYBRID PHYSICS-INFORMED BODYTWIN
Independently develop full state+inference pipeline joining mechanistic IMU observation models, sensor-to-segment calibrated kinematics, sparse pose prior, contact constraints and a robust optimization/uncertainty/abstention layer. Compare true segment reference vs no-reference and mass/joint length confounders. May choose Lie-group invariant EKF, SO(3) factor graph, SR-UKF, fixed-lag smoother, biomechanics model or its own novel alternative, with explicit complexity/energy and rank analysis.
M05 — ALTERNATIVE ORIGINAL CONCEPT / UNCONSTRAINED CHALLENGER
Design a scientifically reasoned COMPLETELY DIFFERENT end-to-end pipeline, including the possibility that BodyTwin should be a probabilistic multi-resolution 'measurement-and-representation twin', not a generative humanoid. Demonstrate falsifiable advantage (robustness/calibration/latency/coverage) over M01–M04 at fixed data and compute. Only accept if reproducible and source-pinned; it may reject anatomical pose inference altogether.

### Independently disjoint review tracks (not substitutes for their own model prototypes)
M06 — BIPM/GUM UNCERTAINTY + STATE/REFERENCE CERTIFICATION
Independently audit all 5 models: correct units + GUM sensitivity derivatives, joint-frame transform errors, segment mounting slip, gyro bias, wall/event timestamp, non-Gaussian and selective gating, MC coverage. No NIS PASS by post-gate contraction; NEES only with truth; report confidence/coverage conditional on reference. May propose an alternative full model if all fail.
M07 — OBSERVABILITY / MATHEMATICAL FALSIFICATION
Prove or disprove local/global identifiability under 0,1,2,3,6 IMUs and specified mounting and excitation. Construct explicit indistinguishable body motion cases producing identical measured device data, out-of-plane joint rotations and source gaps. Absent reference -> no full-body measurement claim. Challenge any 'unlimited possibility' physics mismatch.
M08 — DATASET/WEIGHT/LICENSING, OOD + SECURITY
Verify original datasets/train-split leakage, licenses of models/weights, subject privacy and training provenance; inject stale data, untrusted expert returns, model/package-prompt injection, malicious serialized weights, masked/private-original hash and wrong device labels. Only run untrusted code in network-disabled sandbox; no automatic external model download/execution.
M09 — MULTI-DEVICE CLOCK, EXTRINSIC AND STATIC/GYRO REFERENCE
Design actual future OPPO+companion calibration needed for relative segment claims (no unauthorized live capture now); discriminate affine/piecewise clock, event arrival jitter, stamped OS time vs sensor time; physically realizable independent reference and consent protocol. Source-backed one-shot future device plan, not execution.
M10 — OPEN-SOURCE BASELINE & PROJECT FIT
Compare official OpenSim/OpenSense (calibrated IMU IK), DIP-IMU/TransPose/PIP, IMUPoser/MobilePoser, newer 2026 sparse-IMU methods, and proposed NEXUS-native code on source license, portability, offline latency, model footprint, dependency policy and actual sensor modality. Do NOT silently copy noncommercial model weights into production. Build a reproducible minimal offline baseline if rights permit; no implied on-device deploy.
M11 — BODYTWIN SEMANTIC PRIVACY + INTERFACE GATE
Build a complete typed data contract separating SENSOR_OBSERVED, DEVICE_ESTIMATED, SEGMENT_ESTIMATED, BODY_PRIOR_GENERATED, BODY_MEASURED_REFERENCE_BOUND, UNKNOWN, REFUTED and NOT_CONNECTED; preserve missing fragments, forbid fake self-asserted AUTHORITY and false public/private CAS link. Test output API/UI/plots against a desk phone and null input, cold restart, replay, source substitution, budget <=3 logical reads per query as prereg.
M12 — ACTOR-INDEPENDENT CROSS-ADJUDICATION
Under distinct approved GitHub identity and toolchain, rehash each model exact source, run adversarial negative controls, inspect claims/metrics/training provenance and independently rank Pareto frontier of physics defensibility, reference traceability, worst-case false human-body claims, compute/latency and maintainability. Prevent shared input/model copies from masquerading as independent review. Any reviewer already exposed to Gemini/NEXUS preferred design must label PREEXPOSED.

## Mandatory end-to-end candidate model anatomy (M01–M05 individually)
A. SCIENTIFIC GOAL: what physical quantity (phone orientation, relative joint hinge, body pose prior) and what explicitly cannot be observed.
B. SENSOR/PROVENANCE ADAPTER: Android type, units, calibration status, frame/epoch/clock and source digest protected privately; exact schema and failure behavior. Synthetic input accepted only with SYNTHETIC tag.
C. TIMING/ALIGNMENT: local monotonic event timestamps, batching, dropout, drift, skew and multi-device coupling. Time stamps vs arrival time clearly different; no unverified synchrony.
D. CALIBRATION: observable bias/scale/axes, gravity, sensor-to-segment transforms and physical mounting; what cannot be calibrated without reference and positive user scope.
E. STATE+EQUATIONS: explicit x_t, f, h, noise, unknown covariance/noise assumptions, SO(3)/SE(3) and biomechanics degrees of freedom, integrator/optimization or NN distribution. Unit and shape sanity tests.
F. UNCERTAINTY: model and observation uncertainty with GUM or justified probabilistic intervals; OOD, nonlinearity, input-missingness, n_eff, nonfinite and PSD checks.
G. COMPUTATION: source-controlled Python/TypeScript or Android-compatible offline prototype; pinned dependencies, no remote mandatory service, headless deterministic frozen fixtures, ≤ reproducible seed; measured benchmark latency/CPU/RAM where executed.
H. OUTPUT/UX: machine and human labels distinguish OBSERVED SENSOR, INFERRED DEVICE, CALIBRATED SEGMENT, MODEL PRIOR / SYNTHETIC PERSON. Single unmounted OPPO => no BODY_MEASURED classification.
I. PRIVACY/GOVERNANCE: no raw data exfiltration or public private-source digest; local-only allowed offline, fail-closed unauthorized actions, kill and replay controls.
J. TEST/DELIVERY: at least 20 shared adversarial fixtures plus 5 original self-falsifiers per model, null baseline, process receipt, source manifest and GitHub-only separate authorized receiver/second-party challenge.

## Compulsory two-context experiment
If real BodyTwin consumer exists, the first test is controlled OFFLINE A NO_SENSOR, B original predeadline window (~60s), C complete original archived phone segment (~63.6s). Existing private source must be accessed ONLY by already authorized protected receiver; do not put it in public model repositories. If no existing consumer, mark REAL_NEXUS_BODYTWIN_NOT_CONNECTED and conduct the same test with NEW candidate code using deliberately sanitized synthetic test fixtures first, then private source only after explicit scoped release. New model != proven old system replay.

## Universal null/alternative evaluation
H0 NullTwin: no human body data; predicts only source availability/phone stationarity without human pose.
H1 physical orientation phone-in-device frame;
H2 geometry + independently calibrated 2-body relative joint (when physical support exists);
H3 conditional learned full body PRIOR not measurement;
H4 original physics+probabilistic hybrid.
Compare all on identical source partition and held-out negatives; do not use a differently sourced test dataset to claim superiority. Require a threshold-free no-sensor/desk-phone false-human-pose-claim counter test before any more flattering metrics.

## Model promotion ceilings
P0_DESIGN_SOURCE => model thought experiment; P1_SYNTHETIC_EXECUTED => run only synthetic/reference permitted sources; P2_PRIVATE_DEVICE_REPLAY => actual phone source processed by candidate, no body attached; P3_REFERENCE_BODY_TRIAL => owner consent and independent mounted reference, not authorized by this order; P4_PRODUCTION_PUBLIC => separately adjudicated and authorized reversible public-safe rollout only. NO progression across absent noncompensatory gates. No clinical, human consciousness, personality or autonomous living-body claims.

## What the external expert actually returns
For EACH model: (1) independently created source tree and GitHub commit with precise source license, (2) technical report equation-level with exact limitations, (3) runnable offline demonstration and frozen test commands, (4) machine-readable manifest and model card, (5) negative and positive result JSON per fixture, (6) explicit sensor/segment/body output schema, (7) dataset/weight provenance & license if trained, (8) second-party independent challenge or CLEARLY PENDING, (9) exact parent commit and returned source hashes, (10) one concise rejected-claim section.
Registration/transport contract in 07. A proposal-only return is valuable and classified DESIGN_ONLY; do not assert runnable implementation where none exists.

## Exit criterion
Not model_count, not impressive animation. R37 achieves a meaningful scientific milestone when at least TWO independently designed full end-to-end candidates can be executed on the SAME controlled offline test suite and an independent checker can say precisely when each candidate must abstain from human-body claims. A future physically validated human BodyTwin remains a separate, currently CLOSED gate.
