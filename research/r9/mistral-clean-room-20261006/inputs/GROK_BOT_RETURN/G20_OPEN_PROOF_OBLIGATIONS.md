# G20 — OPEN PROOF OBLIGATIONS (R10R9, consolidated from lanes 1–3)

```text
OBJECT        = R10R9_G20_OPEN_PROOF_OBLIGATIONS_SYNTHESIS_20261005_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SCOPE         = definitional, logical, specification and source-binding obligations that can be discharged
                by writing, deciding or statically checking something. No data collection needed.
                Empirical obligations are in G21.
OWNER ROLES   = AXIOM (adjudication / definition authority) · operator (Nexus Omega; inputs and decisions) ·
                executor (whoever AXIOM releases for the task; GROK-BOT or CURSOR_PRAXIS; no self-release)
LAST_VERIFIED = 2026-10-05 (Europe/Berlin)
```

Status values: `OPEN` · `PARTIALLY_DISCHARGED` (a lane did the work; AXIOM acceptance pending) · `BLOCKED_ON_INPUT`.
"Origin" points to the lane artefact that raised the obligation. Nothing here is discharged by GROK-BOT's say-so: every discharge requires the named owner.

## A. Part A (shared-policy-text configuration test, H_SP)

| ID | Obligation | Origin | Owner | Blocks | Does NOT block | Discharge criterion | Status |
|---|---|---|---|---|---|---|---|
| PO-A1 | Define "Soft-Lineage" formally, or adopt the reduced label H_SP (shared D_CONTROL policy text, independent SOURCE/DATA, no increase in error correlation, no dissent suppression). If a lineage mechanism is intended, define factor L with manipulable levels. | MA-L3-03; U04 (G18); G07 sec. 1; MA-SYN-01 | AXIOM (definition), operator (intent) | Final Part A hypothesis wording; prereg freeze; the choice between REDUCE and HOLD | Design structure (G04), battery spec (G05), metrics (G06), B0, C | Hash-bound definition document cited by G23 | OPEN |
| PO-A2 | Define C=NO. Default: NODE_SPECIFIC, length-matched (±5%), same skeleton. A-NONE and A-PLACEBO run as auxiliary arms. | MA-L2-01; G04 sec. 2, 5 | AXIOM | Freeze of the C manipulation | Battery, metrics, power plan, Part B | AXIOM ruling recorded in the prereg | OPEN (default proposed) |
| PO-A3 | Correct the PR #45 M03 wording "D_EPISTEMIC held constant low" to "balanced across C arms (orthogonal)". | MA-L2-03; REPO_CONTEXT_lane2 obs. 2 | AXIOM | Internal consistency of the PR #45 design of record | Everything else if option A is adopted | Amended M03 text (append-only) | OPEN |
| PO-A4 | Extend the PR #45 preregistered estimable set to C, M, E, P, C×M, C×E, **M×E, C×P**, and rule out fractionation of the core 2^4. | REPO_CONTEXT_lane2 obs. 1, 4; G04 sec. 3 | AXIOM | PASS_C1_PREREG_READY (P2) | A-MIN (which needs no 2FI) | Prereg lists all 8 primary contrasts; alias table attached | PARTIALLY_DISCHARGED (alias computation: work/calc/alias.py, alias_output.txt) |
| PO-A5 | Freeze the central-test logic: CT1–CT5 as an intersection-union test, CT6 reported; F-SL1 written verbatim; absence of interaction claimed only by TOST (F3). | G04 sec. 7; G06 sec. 4; answers_lane2 Q01 | AXIOM (approve), executor (encode as code) | Any central-test verdict | Design work | Analysis code hashed before first E2 call | PARTIALLY_DISCHARGED (specified in G04/G06) |
| PO-A6 | Decide what EPISTEMIC_DEPENDENCE_LOW requires: (A) SOURCE/DATA low by construction + MODEL nominal (UNKNOWN), with qualifier; or (B) MODEL KNOWN-low (open-data models only). | MA-L2-02; G04 sec. 7 | AXIOM | Central-claim wording; model list; whether sec. 9 resolves to HOLD | Design structure, battery, metrics | AXIOM ruling | OPEN (default A) |
| PO-A7 | Define the exposure protocol for retention and revision metrics. Default: 2-stage (S1 independent → S2 peer exposure); K-1-full 2^5 if budget allows; never K-1-half for retention metrics. | MA-L2-04; G04 sec. 4 | AXIOM | Definition of M2, M3, M6 | M1, M4, M5 on Stage 1 | AXIOM ruling | OPEN (default A) |
| PO-A8 | Segment classification of every prompt (CONSTITUTION / TASK / OUTPUT_SCHEMA / TOOLING), with fixed slot and delimiters. Only CONSTITUTION varies with C, only TASK with P. | G03 T03, T06 (R-12, R-20) | executor (draft), AXIOM (approve) | Identifiability of C vs P as contrasts; G03-A gate | Part B, C | Frozen prompt templates hashed | OPEN |
| PO-A9 | Version-freeze manifest and reproducibility receipt schema satisfying RECEIPT_COMPLETENESS_RULE (L2-004). | G03 sec. 2; G06 sec. 11–12 | executor | Any E2 run | Design | Receipt template accepted by AXIOM | PARTIALLY_DISCHARGED (template in G06 sec. 12) |

## B. Part B (B0 synthetic, B1 real)

| ID | Obligation | Origin | Owner | Blocks | Does NOT block | Discharge criterion | Status |
|---|---|---|---|---|---|---|---|
| PO-B1 | Define Δ formally (U09). Default: assumptions A-Δ1..A-Δ3 (segment-level score; HOLD iff Δ > τ; τ on DEV only; Δ-PH, Δ-COST, Δ-DISAGREE preregistered separately). | G08 sec. 2; G18 U09; GAP-L2-02 | operator (intent), AXIOM (adopt) | B0 freeze; H-B0-1 | Generator spec, pipelines, metrics | Δ definition hash in B0 prereg | OPEN (default proposed) |
| PO-B2 | B0/B1 wording rule: B0 may never be called biological validation; LIGHT_TOXICITY_PROXY is a synthetic degradation model only; no phototoxicity claim without a biological endpoint. | ORDER sec. 12–13, 17; G08 sec. 1; G09 sec. 2 | AXIOM (enforce), executor (comply) | Any B0/B1 publication wording | Running B0 | Wording lint over outputs (no "real vesicles", "phototoxicity", "in cells" in B0 artefacts) | OPEN |
| PO-B3 | Freeze merge/split scoring convention, gate distance ε, fairness rules (equal tuning budget) and the null comparator (random hold at matched coverage). | G08 sec. 4, 6 | executor (draft), AXIOM (approve) | B0 TEST evaluation | Generator implementation | Frozen B0 prereg | OPEN |
| PO-B4 | Remove PH superiority language everywhere. PH stays a demoted optional arm until H-B0-2 passes. | answers_lane2 Q09; G10 | AXIOM | Any PH claim | B0 run | Text audit | OPEN |

## C. Part C (authority capsules)

| ID | Obligation | Origin | Owner | Blocks | Does NOT block | Discharge criterion | Status |
|---|---|---|---|---|---|---|---|
| PO-C1 | Define the TRUST_ANCHOR set and its onboarding/rotation process, plus the KEY_ID→ISSUER binding with validity windows. | G11 sec. 2–3, G-C05, G-C11; Q14, Q15 | operator (who is root), AXIOM (policy) | Every AUTHORIZED claim; any NAC-2→authority step | NAC-0/1/2 *integrity* semantics; Part A; B0 | Signed anchor registry plus policy document | OPEN (blocks Part C gate) |
| PO-C2 | Decidable SCOPE grammar with subset semantics (⊆ decidable; no wildcard/free text without normalization). | G11 G-C01 | executor (design), AXIOM (approve) | Delegation attenuation; G-C01 | Signature format choice | Grammar spec plus decision procedure plus normalization tests | OPEN |
| PO-C3 | Revocation source with fail-closed semantics (UNKNOWN → deny for high-impact scopes). SCITT leaves revocation out of scope. | G11 G-C10; L1-001 | operator, AXIOM | AUTHORIZED predicate | NAC-3 registration | Revocation spec | OPEN |
| PO-C4 | CLAIM_CEILING / ROOT_PROPERTY monotonicity: define the C-ladder (C0…Cn; U08) and the ordering used by `child.CLAIM_CEILING ≤ parent.PROVEN_ROOT_PROPERTY`. | G11 sec. 2, 4; G18 U08; G17 sec. 4 | AXIOM | The only NEXUS-specific Part C semantics | Cryptographic layer | Ladder definition document | OPEN |
| PO-C5 | Choose one canonical serialization (RFC 8785 JCS **or** deterministic CBOR/COSE), domain-separation string, and which NAC-2 fields go into the protected header. Pin the algorithm (Ed25519 default) and reject `none`/unknown algorithms. | G11 sec. 2; Q17; L1-036, L1-038, L1-039 | executor (profile), AXIOM (approve) | Capsule implementation; fixtures | Trust-anchor policy | Profile document | OPEN |
| PO-C6 | Expiry policy: **reject** child-exp > parent-exp (do not intersect windows as UCAN does). Define clock source and skew bound. | G11 sec. 4, G-C02 | AXIOM | G-C02 fixture | Others | Ruling recorded | OPEN (default reject) |
| PO-C7 | Profile instead of a new format: NEXUS statement payload type, SCITT registration policy, Biscuit-or-COSE capsule. No new transparency log, receipt or envelope. | G11 sec. 7; answers_lane1 Q17, Q20 | AXIOM | Any new token-format work | — | AXIOM adopts the REDUCE_C1_PART_C_TO_PROFILE decision | OPEN |
| PO-C8 | Boundary invariants as code: `SIGNATURE_VALID ≠ AUTHORIZED`, `SCITT_RECEIPT ≠ NEXUS_AUTHORIZATION`, `SCITT_RECEIPT ≠ SCIENTIFIC_VALIDITY`, `TOKEN ≠ NEXUS_AUTHORITY` (G-I02), MCP tool output = observation (G-I04). | ORDER sec. 19, 21; G13 sec. 4 | executor | Integration adapters | — | Static check plus fixtures | OPEN |

## F. Framework, metaphor, gates, sources

| ID | Obligation | Origin | Owner | Blocks | Does NOT block | Discharge criterion | Status |
|---|---|---|---|---|---|---|---|
| PO-F1 | **Fix the fail-open default** in the R10R8 seven-gate integration test (missing GATE2/GATE3 default to VERIFIED), and prove UNKNOWN → HOLD/deny with a regression fixture. | L1-053 (AXIOM caveat in repo); G02 sec. 2.1 | executor (fix, under AXIOM release; no git write by GROK-BOT), AXIOM (verify) | Any claim that NEXUS gates are non-compensatory; reuse of E0.2 gates in R10R9 | Part A/B design | Negative fixture (missing input → non-PASS) passes on both integrated and standalone gates | OPEN |
| PO-F2 | **Split AIR_GAP** into `UNRESOLVED` (state) and `NCI_RELATION` (relation). Resolve GATE5 to one value for a missing capsule (integrated AIR_GAP vs standalone FALSIFIED). Keep aliases in a registry. | MA-L3-04; G14 MC-G14-2; REPO_CONTEXT_lane3 RC-05 | AXIOM (canonical decode), executor (rename) | Any R10R9 gate using AIR_GAP | Design work | Decode-consistency check passes (G14 sec. 4) | OPEN (active defect) |
| PO-F3 | TERMS registry (machine-readable JSON twin) for the R10R9 prereg and future orders. Gate on RC_material = 1 and no PINNED_STALE. Re-pin A2A to "protocol 1.0 (latest release v1.0.1)", MCP to 2026-07-28, SLSA to v1.2, PROV-DM to REC 2013-04-30. | G18 sec. 4; MA-L3-02; answers_lane3 Q23 | operator (author), executor (checker) | Prereg freeze (closure) | Research design | Checker run with 0 material unbound references | OPEN |
| PO-F4 | Adopt NEVER_COMPRESS as an invariant of the order profile (identifiers, dates with zone, claim levels, negations, falsifiers, authority fields, thresholds, observation/interpretation boundary, known-unknowns). | answers_lane3 Q24 | AXIOM | Metaphor use inside gates, enums, predictions or falsifiers | — | Profile text adopted | OPEN |
| PO-F5 | Static METAPHOR_LEAK test (O vs O′ re-derivation plus decode consistency) over the R10R9 prereg and gate code. FAIL_METHOD on any artefact change. | G14 sec. 4 | executor | Prereg freeze if metaphors remain in normative text | — | Leak test PASS or metaphors removed | OPEN |
| PO-F6 | Rename factor C to "shared policy text P_c (hash)" and Soft-Lineage to H_SP in the Part A prereg. Keep old names only as registry aliases. | answers_lane3 Q22; G19 sec. 2 | AXIOM | Prereg wording | — | Renamed prereg | OPEN |
| PO-F7 | Retire the novelty framing of "SELF_CONTAINED_EXECUTION_FRAME". Name it "NEXUS order profile" over OPORD + prereg + DbC/policy-as-code + provenance + state machine + assurance case. | G17 sec. 4 | AXIOM | Any novelty claim | — | Wording change | OPEN |
| PO-S1 | **Wording-level sec. 31 audit**: re-bind every G02 verdict to the exact citations of the operator's R10R9 draft once it is supplied (hash or URL). | MA-L1-01 = MA-L3-01; U01, U05 | operator (supply draft), executor (re-audit) | Any statement "R10R9 says X and X is wrong"; final acceptance of R10R9 citations | Referent-level verdicts (G02); Parts A/B/C design | G02 re-issued with a draft hash | BLOCKED_ON_INPUT |
| PO-S2 | Original R9 vesicle/PH text (sec. 12) for the Part B audit trail. | U02; GAP-L2-02 | operator | Verbatim R9 claim audit | B0/B1 design (built from ORDER sec. 12–17) | Text supplied with hash | BLOCKED_ON_INPUT |
| PO-S3 | Re-bind the R10R7 report (R7_00) citations, which use search-result pseudo-URL-scheme links and one-number credibility scores (both prohibited by sec. 3), before any R10R9 reliance. | REPO_CONTEXT_lane1 sec. 4; L1-055; RC-07 | executor (under release) | R10R9 reliance on R7 citations | R10R9 lanes (none rely on them) | Re-bound ledger | OPEN |
| PO-S4 | Unverified identifiers: DREAM v3 canonical DOI (L1-023), VAIL referent (MA-L1-02), ternary-logic referent (MA-L1-03), DITL referent (MA-L1-07), MAC-design referent (MA-L1-05), DreamerV3 alternative (MA-L1-04). | G02 sec. 4 | operator (draft citations), executor | Load-bearing use of those items (already disallowed) | Everything else | Identifiers bound or items dropped | OPEN (non-blocking by default) |
| PO-S5 | Hash-bind the missing E0 D-vector DOCX and the E0.1 formalization DOCX (private README hashes 19474611…, 52366eef…), or declare them non-authoritative. | GAP-L2-03; REPO_CONTEXT_lane1 sec. 2 | operator | Byte-bound verification of the D-vector source | Use of the D split as written in ORDER sec. 9 | Files present with matching hashes | BLOCKED_ON_INPUT |
| PO-S6 | Private R10R7 package declared-vs-present gap (files 01, 03, 04, 06, 07, manus_order/tests and receipts absent). | GAP-L2-04; REPO_CONTEXT_lane1 sec. 2 | operator | Claims depending on those files | R10R9 (does not rely on them) | Files present or README corrected | OPEN |

## Summary
- **Hard blockers of the Part A prereg freeze:** PO-A1, PO-A2, PO-A4, PO-A5, PO-A6, PO-A7, PO-A8, PO-F3 (closure), PO-F6.
- **Hard blockers of the Part C gate:** PO-C1, PO-C2, PO-C3, PO-C4.
- **Active defects:** PO-F1 (fail-open gate default) and PO-F2 (AIR_GAP decode inconsistency).
- **Blocked on operator input:** PO-S1, PO-S2, PO-S5. These block the wording-level audit only, not the system (`BLOCKED_LANE != BLOCKED_SYSTEM`, ORDER sec. 1).
