# R35 neutral Stage-0 independent OPPO / BODYTWIN research brief
OBJECT = NEXUS_OMEGA_AXIOM_R35_EXTERNAL_STAGE0_OPPO_BODYTWIN_RESEARCH_BRIEF_20261118_R0
SCOPE = EXTERNAL_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SOURCE_EXPOSURE = PREEXPOSED unless a genuinely isolated reviewer can demonstrate BLINDED
REVIEWER_IDENTITY = SELF_DECLARED_UNVERIFIED unless external authentication proves otherwise

Research question: With two Android phones, one known as OPPO CPH2219, and uncertain IMU clocks, biases, body/frame constraints and no accepted human-body ground truth, which sensor models and falsification protocols could justify a restricted C1 statement about device motion and which cannot justify whole-body movement or clinical inference?

Before reading any preferred NEXUS implementation where possible, independently propose:
1. At least TWO substantively different system architectures and the simplest null model: e.g. direct gyro integration vs local UKF/SR-UKF vs factor graph or batch alignment. Explain scientific discrimination experiments rather than popularity.
2. Explicit sensor observation, latent state, units, frame transformations, clock offset/drift and unknown calibration parameters; observability/identifiability under static, single-axis and coupled excitation, and degenerate motions.
3. Sensor quality taxonomy: calibrated vs uncalibrated Android IMU, clock timestamps, event batching, Android OS/sensor firmware version. Never assert OPPO sensor chipset or exact hardware capability without a direct on-device census.
4. Three strongest ways YOUR proposed architecture could be wrong; at least one adversarial synthetic fixture and one future controlled physical reference fixture, with expectations and fail conditions.
5. Proposed pre-registered metrics: reference orientation/trajectory errors when ground truth exists; innovation consistency (NIS) and state consistency (NEES only with known true state), degrees of freedom, chi-square intervals, gating/selection bias, sensitivity to noise mismatch and temporal correlation, calibration drift, failure rates with uncertainty budgets.
6. Method to separate person motion, phone motion and sensor coordinate frames. Do not infer human-body pose from a single phone trajectory absent independently observed kinematic coupling.
7. Provenance, rights, consent and security constraints, rollback and offline fallback; minimum resource budget to reach an interpretable result.
8. What you CANNOT claim and what absent source/fixture would change your judgment. Include first-party Android sensor docs and metrology sources, versioned primary research with DOI/arxiv ID, uncertainty and limitations.

Deliver one original stage0 artifact with exact full SHA256, observed source URLs/revision/date, alternate hypothesis, own red-team falsification, exposure declaration, status DESIGN_ONLY/REPLAYED/SOURCE_GAP. No physical human trial, private data export, GitHub write by implication, clinical claims, claims of independently executed code without executable log.
