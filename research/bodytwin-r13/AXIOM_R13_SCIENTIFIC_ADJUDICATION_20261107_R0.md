# NEXUS OMEGA R13 — AXIOM scientific intake & public Bodytwin boundary
OBJECT = NEXUS_OMEGA_AXIOM_R13_SBT_BODYTWIN_SOURCE_EXACT_SCIENTIFIC_ADJUDICATION_20261107_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_CHAIN_INTEGRITY_PDF_ORIGINAL_RECOVERED_A72_GAP_PRESERVED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
TRUTH_AUTHORITY = NONE
DATE = 2026-11-07
SCOPE = PUBLIC_SAFE_SCIENCE_METADATA_ONLY_NOT_PRIVATE_SOURCE_EXPORT

## Independent byte intake (operator-upload originals)
| Object | Bytes | SHA-256 |
|---|---:|---|
| GROK→QWEN SBT R0 order | 7917 | 594a92275baf3791d4cf74fb9602ce35dcaf89a4e2e80d40ed8a70a1f3bb7fe8 |
| MISTRAL/VIBE SBT B01–B08 return | 40055 | a7b6a9255a50c8328ab4b2b5fc02151a30be18b1471a7836a4dd014169ecc1fe |
| GROK→MISTRAL/VIBE continuation order | 8404 | 7dbd9abc24b879c5563b0ba6ef39d4ceb923b9b53f8859f739c76655739b3cfa |
| MISTRAL/VIBE continuation research | 39624 | 81f3b9787dc51aeb4fa295ae41d287a975b684e2fdc8864718483e524a0c2b97 |
| GROK→MISTRAL/VIBE A72 source-gap order | 6725 | 97c5ff11305d39a28c56dbb6ffc3cbd154f58b93928eedad259a9c5bc0af617c |
| MISTRAL/VIBE A72 source-gap closure return | 18859 | 18fc59a96fe615dbb7250ec741fda251bc8b2517d37b9fb324b7fe57e758aec5 |
| GROK/AXIOM background narrative (TXT) | 10919 | 88b0714b82aa9d1c724bf2e9b55e3e82ec7bf3c10c188dffae93dd4a69a87757 |
| QWEN 'NEXUS-Architektur.pdf', original now accessible | 77038 | a78033b255a8465f183d3a56e6fdde31bffa37280e1500ea9e13b49deec63ea3 |

PDF assessment: 13 pages, file is structurally valid and text was extracted and page 4/7/9 visually inspected. Prior MISTRAL statement 'only 145-byte stub; EXTRACT_BOUND_ONLY' may describe that external session, but is superseded for **this AXIOM intake only**: PDF_ORIGINAL_BYTE_BOUND_YES. Not an endorsement of the PDF's technical accuracy.

## Research lane status
G01 original A72 architecture, Body_Twin_Mesh, and section_XI governance YAML: NOT_FOUND_AS_ORIGINAL_BYTES after search of current Project/Library/known archive names and connected Drive filename searches. The GROK order *claims* originals in another session; such claim is not the byte source. Status remains SOURCE_REPORTED_FROM_ORDER / DESIGN_LEVEL. The order and return MUST NOT be semantically reinterpreted to imply BYTE_BOUND A72. No new A72 primitive IDs.
M01 research registry: nine candidate entries in MISTRAL continuation; independent per-entry license/HEAD recheck not done here. TIC license GAP remains. M02 non-foot static/Nullphase proposals: design only; no sensor thresholds or accuracy measured. M03 binding GATE identities remain pending. M04 YAML checkpoint: present in return; not a running checkpoint.

## Scientific corrections: do not transfer absolute claims to production
- 6-DoF accelerometer+gyroscope lacks absolute heading/yaw without external reference; relative joint tracking constraints can stabilize *relative* orientation, not magically produce world-heading truth (Lehmann et al., IFAC 2020).
- The <4° value in Lehmann et al. pertains to the paper's specified mechanical test setup; NOT a general human-body accuracy guarantee.
- EKF-low-latency / UKF-reference is a design hypothesis, not a mandated or universally optimal solution. The claimed UKF '3–4× cost' is implementation/hardware/model dependent and was not benchmarked on target hardware; Madgwick/Mahony low-latency path in earlier MISTRAL work differs from later QWEN EKF assignment.
- The 'kinematic limit guarantee' is only a hypothesized model constraint. Individual ROM, sensor-to-segment registration, skin slip and pathology can invalidate naive hard limits; clamp must not silently fabricate valid movements.
- A ZUPT zero-velocity constraint is not valid solely from low local acceleration or gyro variation. Non-foot stationary/periodic contexts require additional evidence.
- A self-contained SHA-256 record chain is reversible by an adversary who can rewrite the whole chain; immutable independent checkpoint origin and trust roots are separate gaps. Hash chain integrity ≠ physical measurements, causal parent proof or trusted UTC.
- RFC3161 signs a time-bound hash token; it cannot prove sensory truth, subject consent or synthetic/biological consciousness.
- Source narrative 'wetware' is an ethics/inspiration input only; no empirical consciousness, learning or human-biological computation claim.
- S1 raw ledger ≠ S2 transformed ledger; a research diagram does not authorize sensor recording, personal data publication or autonomous feedback to the human.

## Existing public Bodytwin surface (separately observed)
https://www.nexus-mobile.de/bodytwin/ is readable as C1 visualization, with 4D projections, symbolic SOFT view and snapshot-style references.
https://www.nexus-mobile.de/research/bodytwin/state.json publicly advertises BODYTWIN=RESEARCH_FOUNDATION_C1, BODYTWIN_VALIDATED=NO, CONSENT_BIND=OPEN, TRIAL_001=DESIGNED_NOT_EXECUTED.
Therefore VISIBLE_PUBLIC_UI != LIVE_CALIBRATED_IMU_SENSOR_NODE. Existing R11/R12 and prior Gate PR321/322 remain unchanged.

## Separate public bridge implementation (not scientific R13 'code execution')
Source under research/bodytwin-r13/site/ consists of standalone HTML/CSS, read-only same-origin JS and fail-closed pure status schema, intended to be staged optionally at /bodytwin/r13/. No private original research document or human raw data is exposed. This is a **different engineering/presentation lane**, not a retroactive rewrite of MISTRAL/GROK research order 'NO CODE'.
Bridge tests: 31/31 V8 pure source/readback checks observed, and separate local Node prototype 32/32 PASS (not byte-exact identity to final GitHub module). GitHub/Windows Node test and actual browser/Hostinger run PENDING.
Scope guard: do not modify existing /bodytwin/ main viewer, do not replace /research/bodytwin/state.json, and do not infer real sensor activity from status GET.

## Primary scientific references
https://www.sciencedirect.com/science/article/pii/S240589632030690X — Lehmann et al. (2020) IFAC, relative tracking only, experimental limits.
https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084203 — OpenSense vendor-/third-party fusion and sync assumptions.
https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084548 — OpenSense measures/outputs and scope limitations.
https://www.mathworks.com/help/fusion/ug/introduction-to-estimation-filters.html — EKF/UKF trade-offs, no universal computational ratio.

## Terminal admissible C1
R13_RESEARCH_C1 = ACCEPT_WITH_CAVEATS
R13_QWEN_PDF_ORIGINAL = BYTE_BOUND_77038
A72_SOURCE_BIND = HOLD_ORIGINAL_BYTES_NOT_PROVIDED
BODYTWIN_PUBLIC_VISUALIZATION = LIVE_PAGE_OBSERVED
LIVE_BODY_SENSOR_TRIAL = NOT_EXECUTED
PUBLIC_BRIDGE_CODE = IMPLEMENTED_CANDIDATE
HOSTINGER_PUBLIC_BRIDGE_DEPLOY = NOT_EXECUTED
OPERATOR_CONSENT_BIND = OPEN
NO_HARDWARE_ACCESS = YES
NO_CLAIM_PROMOTION = YES
