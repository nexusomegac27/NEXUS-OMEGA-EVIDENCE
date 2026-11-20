# R36 external expert handoff — one bounded evidence route per reviewer
OBJECT = NEXUS_OMEGA_AXIOM_R36_EXPERT_NAVIGATION_AND_RETURN_CONTRACT_20261119_R0
STATE = EXTERNAL_RESEARCH_ONLY | NO_IMPLICIT_WRITE_GRANT
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PRIMARY_SCIENCE = OPPO_BODYTWIN
BODYTWIN_VALIDATED = NO
PRIVATE_ORIGINALS = ACCESS_ON_SEPARATE_OPERATOR_AUTHORIZATION_ONLY

## Entry protocol
Read [R36 START](../README.md), [causal graph](01_CAUSAL_SOURCE_GRAPH_AND_PR_INDEX.md), [open disagreements](02_R36_INTAKE_DISAGREEMENTS_AND_SCIENCE_GATES.md) before proposing a fix. Review the [OPPO measurement candidate](../oppo-bodytwin-foundation-20261118/02_R36_OPPO_BODYTWIN_MEASUREMENT_PREREGISTRATION.md) and original [E01–E10 mandate](../oppo-bodytwin-foundation-20261118/03_R36_INDEPENDENT_EXPERT_MAXI_ORDER_E01_E10.md) without treating either as an empirically valid design.

Pick ONE scope in a return; if multiple scopes are investigated, label a distinct falsifier and source set for each:
- E01 SENSOR/ANDROID: determine what exact on-device original/clock API census is needed. Do not guess OPPO hardware from the marketing model.
- E02 CLOCK: compare offset, affine skew, piecewise drift on synthetic+future physical reference; identify rank loss.
- E03 FILTER/NIS: correct invalid gated NIS pass, check nulls and conditional distribution, judge UKF vs SR-UKF and no-filter.
- E04 BIOMECHANICS: determine what phone-to-rigid-segment extrinsics can be measured, what full-body pose cannot.
- E05 METROLOGY: independent dimensional/unit audit of the Stage1 uncertainty budget and risk of pre-data target tuning; instrument class + u_ref.
- E06 LEDGER: signed authority, valid immutable transitions, strict per-query logical-read budget, public-private CAS attacks.
- E07 PUBLICATION: CURRENT/OPEN/HISTORICAL_ARCHIVE source-derived navigation; no lost negative evidence, no live autopromotion.
- E08 ADVERSARIAL CHALLENGER: independently refute strongest claims including ternary = mandatory neutral, 30min/10min prereg merge and X5 original witness.
- E09 SECURITY/CONSENT: real operator identity, actual right to access originals, revocation vs tamper logs, external code and third party rights.
- E10 INDEPENDENT INTEGRATOR: compare Variant A vs Variant B with observable physical outcomes, falsifiers, uncertainty and provenance; report HOLD if unresolved.

## Self-critical validation BEFORE delivery
A. Propose at least TWO independent design alternatives plus a minimum null model; identify causal mechanism and what would falsify each.
B. State original full source URI/DOI, retrieval timestamp, source_published and revision dates, actual accessed content (FULL_TEXT/ABSTRACT/metadata), license and SHA of received original if actually present.
C. Supply one highest-value positive fixture AND one adversarial negative control. Report NOT_RUN unless exact runnable source, command, toolchain, exit, stdout and result bytes are present.
D. Include a source-known attacker view for all privacy/authority studies; assume attacker can read published code and inputs.
E. Include numeric uncertainty units and dimensional checks; a low NIS or a small residual alone is not model validity.
F. Disclose whether investigator already saw R35/R36 proposal; if yes PREEXPOSED. Give any common underlying provider/prompt/toolchain; independent claims need demonstrably distinct provenance.
G. Explicitly identify the claim you REFUSE to make, plus a single STOP/HOLD condition and the minimal missing original bytes.
H. Compare any code against the actual source SHA at original ref, never a reconstructed or guessed file. No PR merge, Hostinger deploy, public uploads of private OPPO bytes, agent registration or on-device capture.

## Return contract (single source-bound handoff per expert)
```text
OBJECT = <researcher_unique_object>
PARENT_PIN = <PR and full commit SHA>
IDENTITY = SELF_DECLARED_UNVERIFIED or independent attestation
EXPOSURE = PREEXPOSED or BLINDED_WITH_WITNESS
MANDATE = E01..E10
SCOPE = EXTERNAL_RESEARCH_ONLY
SOURCE_INVENTORY = per-source URL, revision, content class, exact SHA when available
H0/H1/H2 = rival concept descriptions with null
TEST = exact source, fixture, command, toolchain, result hash or NOT_RUN
SELF_REFUTATION = strongest original negative with outcome
METROLOGY = units/frames/timestamps/reference+uncertainty
CONTRADICTIONS = exact former record -> evidence -> proposed successor
CLAIMS_NOT_MADE = ...
OPEN_GATES = ...
STATUS = DESIGN_ONLY | REPLAYED_SYNTHETIC | SOURCE_GAP | REJECTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORIZATION = NO_EXTERNAL_WRITE_NO_DEVICE_CAPTURE_NO_MERGE
```

## How to hand off safely
External experts return a file through an operator-approved intake path or human-mediated channel; do not create a new GitHub directory/branch or post sensitive material in public issues. AXIOM/Operator performs source custody and independent analysis, then Cursor may receive a distinct scoped execution order. A manually pasted response without original bytes is CONTENT_RECEIVED but not source-exact hash verified. A self-declared signature is not independent identity attestation.

## Time/budget and source-failure safety
A source lookup is bounded: up to three focused primary-source paths and up to two attempts per unavailable source for one specialist pass; then SOURCE_GAP + next best rival hypothesis. Do not recurse from a failed candidate into unlimited web or memory searches. Stop if uncertainty forbids legitimate inference; HOLD is a valid outcome.

## Primary official documentation
Android `SensorEvent` https://developer.android.com/reference/android/hardware/SensorEvent
Android `SensorManager` https://developer.android.com/reference/android/hardware/SensorManager
BIPM JCGM100 https://www.bipm.org/en/doi/10.59161/jcgm100-2008e
IEEE Selection-induced innovation contraction https://ieeexplore.ieee.org/abstract/document/11714296
OSF https://help.osf.io/article/330-welcome-to-registrations
EDPB consent https://www.edpb.europa.eu/sme/be-compliant/process-personal-data-lawfully_en
