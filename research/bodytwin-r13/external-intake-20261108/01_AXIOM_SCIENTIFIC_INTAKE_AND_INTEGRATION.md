# AXIOM · E1–E5 original intake and integration review R0
OBJECT = NEXUS_OMEGA_AXIOM_E1_E5_SOURCE_EXACT_INTAKE_AND_REFERENCE_FALSIFICATION_20261108_R0
STATE = SOURCE_EXACT_EXPERT_REFERENCE_RECOVERED_E2_RECEIPT_BOUND_E2_MAIN_GAP_PRESERVED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY · CLAIM_PROMOTION = NO
EXPERT_PHASE = EXTERNAL_DESIGN_ONLY · CURSOR_VISUAL_IMPLEMENTATION = EXCLUDED

## What was actually supplied
Seven uploaded objects rehashed independently; see 00_MACHINE_INTAKE.json for full byte counts/SHA-256. Both ZIP files passed testzip. The outer GROK archive contains a nested copy of the Q0 reconstructed reference ZIP that is **byte-identical** to the separately uploaded 6358-byte ZIP (SHA-256 6360d3a48fc17cf04f93a731762a7170bf57b61e34ce2994f16f15e096bdae2a).

The reference implements a Canvas2D tesseract, five named projection modes and six plane rotations in code, and is **not** the original production viewer. The corresponding README and JSON explicitly state RECONSTRUCTED_EXPERT_REFERENCE / NOT_ORIGINAL_PRODUCTION_SOURCE. Never use it as a production-source hash witness.

## E2 intake
The full status receipt is available and SHA256 verified (2584 bytes / b68ba8fb2317690fb1a4b99ed3ed3021d1e2f0079c59f06f37271694f76b38b3). The E2 original design document **32883 bytes** / SHA256 3d09270dea994eb21aecf9ec71822a6fa399048441ecdafc961717092b8205f1 was **not supplied**; its detached hash is only reported. This is RECEIPT_ONLY, NOT FULL_E2_REVIEW. No measured FPS or executed experiments. Variant A Canvas2D, B WebGL2, C hybrid are described in the GROK handover as E2 design options, **not** validated source-perfect E2 recommendations.

## GROK preliminary cross-validation erratum (critical)
The supplied GROK report says "five projection modes ... all ... singularity guards". Independent execution of the Q0 reconstructed viewer source with Node.js v22.16.0 shows only 12/18 checks pass. Six precisely identified source-level counterexamples fail:
- Perspective denominator with w=3 returns Infinity / nonfinite coordinates.
- Schlegel-like denominator with w=2 returns Infinity / nonfinite coordinates.
- Double-perspective denominator with z=3 returns Infinity / nonfinite coordinates.
- Stereographic near its pole w=1 silently substitutes an orthographic-like point instead of explicit bounded clipping / invalid-state label.
- NaN in the XY angle produces nonfinite 4D coordinates without explicit refusal.
- toScreen accepts Infinity in its y input and produces a nonfinite screen coordinate.

These are **reconstructed-reference defects, NOT proven production bugs**. The deterministic test script tests/audit-q0-reference.mjs intentionally exits nonzero as a fail-closed witness. Tesseract vertex/edge enumeration and nominal norm-preserving rotations were independently reproduced (positive controls PASS). Aesthetic/rendering recommendations cannot promote a failing numerical oracle to PASS.

## Expert-to-design integration sequence without Cursor
1. E1/#327 challenge projection formula and denominator guards. Give per-mode valid domains and geometrically honest fallback (no silent projection substitution).
2. E2/#328 receive detached receipt with exact original bytes/hash; demand main 32883-byte original or flag source gap. Evaluate A Canvas2D+legible labels and C modular hybrid under Source-Exact, with B WebGL2 behind measured mobile perf/accessibility gate.
3. E3/#329 create source-specific annotated desktop/mobile onboarding and control hierarchy from Q0 reconstructed reference, explicit not production; test screen reader, pause, mobile touch and comprehension of 4D vs body measurement.
4. E4/#330 trace visual claim to C1 source field, retain AUTO-UPDATE-TICK ≠ SCIENCE_DELTA, Consent OPEN, no body validation.
5. E5/#331 reproduce six counterexamples and try at least 14 additional adversarial cases, explicitly retract or amend preliminary blanket claim; full E5 independent final report remains pending.
6. AXIOM compares **independent original E1/E2-main/E3/E4/E5 returns** after receipt and checksum; disagreements stay visible. A concept-selection review is possible after source gaps are classified, but production deployment remains separate.

## Exact release separation
No Hostinger writes. No original live 4D viewer mutations. No PR merges. No physical IMU, sensor activation, health data, A72 closure or body validation. Current status producer can continue independently; repeated ticks must not be marketed as scientific progress.

## Source links
- Central expert intake: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/326
- E1: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/327
- E2: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/328
- E3: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/329
- E4: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/330
- E5: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/331
