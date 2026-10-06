# G04 — PART A FACTORIAL DESIGN V2 (R10R9, Lane 2)

```text
OBJECT        = R10R9_G04_PART_A_FACTORIAL_DESIGN_V2_LANE2_20261005_R0
SUPERSEDES    = nothing (design input to AXIOM adjudication); EXTENDS PR #45 M01/M03/M04/M06
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = DESIGN ONLY · NOT FROZEN · NOT EXECUTED · R10R6 E2 NOT EXECUTED
CENTRAL TEST  = OPERATIONALIZABLE_CONDITIONAL (see §7) — not HOLD_C1_E2_CAUSAL_IDENTIFIABILITY_UNRESOLVED,
                but becomes that HOLD if the operator requires MODEL dependence to be KNOWN-LOW with closed models.
LAST_VERIFIED = 2026-10-05
```

## 1. Unit of analysis and protocol

- **Team:** n = 3 nodes per run (minimum giving 3 pairs for pairwise error metrics and a meaningful 1-of-3 minority).
- **Run:** one team solving one task instance in one cell, fresh stateless sessions (G03 T07).
- **Two-stage protocol in every cell** (needed because retention/revision metrics are undefined without an exposure stage):
  - **Stage 1 (S1, independent):** each node answers alone from its own evidence packet → structured answer + confidence + cited evidence IDs + justification. This is the COMM-OFF measurement.
  - **Stage 2 (S2, peer exposure):** each node receives the other nodes' Stage-1 answers + justifications (not their evidence packets) and may revise. This is the COMM-ON measurement.
  - Primary outcomes for convergence/decorrelation/calibration are computed on S1 *and* S2; retention and revision metrics are S1→S2 transitions.
- **Observation:** (task, cell, run, node, stage).

## 2. Factors and levels (operational definitions)

| Factor | D-vector class (PR #45 M03 / ORDER §9) | Level − | Level + | Implementation rule (frozen) |
|---|---|---|---|---|
| **C** shared constitution | D_CONTROL.CONSTITUTION | `NODE_SPECIFIC`: each node gets a *different*, independently authored constitution, length ±5%, same section skeleton, same procedural-coverage checklist (evidence citation, uncertainty statement, dissent permission, revision rule) | `SHARED`: all nodes get the *same* constitution text (one of the node-specific texts, rotated across tasks so content is balanced) | Delivered in the same system-prompt slot, same delimiters, in all cells. "No constitution" is **not** the − level (MA-L2-01). |
| **M** model family | D_EPISTEMIC.MODEL | `HOM`: 3 instances of one model; **capability-balanced**: the homogeneous model is rotated across the 3 heterogeneous families (each task assigned at random, balanced, to family a/b/c for its HOM cells) | `HET`: one model from each of 3 families/providers | Without capability balancing, M is confounded with mean accuracy, and error correlation is known to depend on accuracy (L2-013: larger, more accurate models had highly correlated errors). |
| **E** evidence | D_EPISTEMIC.SOURCE + DATA | `SHARED`: all nodes receive the full evidence packet | `PART`: packet split into 3 disjoint partitions (document- and claim-level disjoint), one per node, assignment randomized | Closed world, no web, per-node index (G03 T02/T05; G05 `SOURCE_PARTITION_PLAN`). Partition design must keep each task adjudicable from the union and, for minority-correct tasks, from one partition. |
| **P** prompt | D_CONTROL.PROMPT | `SHARED`: identical task wording | `INDEP`: each node gets a different meaning-preserving paraphrase from a frozen, human-validated pool | Only the `TASK` segment varies; `OUTPUT_SCHEMA` and `TOOLING` segments identical in all cells (G03 T06). |
| **COMM** (optional) | D_CONTROL.COMMUNICATION | see §4 | see §4 | Core design uses the within-run S1→S2 stage contrast instead of a between-cell COMM factor. |

Factor coding for analysis: effect coding −½/+½ (main effects = difference between factor halves; 2FIs = difference-in-differences; L2-031).

**Fixed (non-varied) shared components, declared:** output schema, tooling instructions, decoding parameters per model, orchestrator code, retriever software (unless sensitivity arm, G03 R-19). These are constant D_CONTROL / D_METHOD components and are reported as such, not hidden.

## 3. Core design: full 2^4 factorial, 16 cells (no aliasing)

Every task instance is run in **all 16 cells** (task fully crossed with cells), R runs each, run order randomized and interleaved in time blocks (G03 T16).

D_EPISTEMIC profile column: LOW = (M=HET, E=PART); HIGH = (M=HOM, E=SHARED). D_CONTROL profile: HIGH = (C=SHARED, P=SHARED); LOW = (C=NODE_SPECIFIC, P=INDEP).

| Cell | C | M | E | P | D_EPISTEMIC profile (M,E) | D_CONTROL profile (C,P) |
|---|---|---|---|---|---|---|
| 01 | - NODE_SPECIFIC | HOM | SHARED | SHARED | HIGH | MIXED |
| 02 | - NODE_SPECIFIC | HOM | SHARED | INDEP | HIGH | LOW |
| 03 | - NODE_SPECIFIC | HOM | PART | SHARED | MIXED | MIXED |
| 04 | - NODE_SPECIFIC | HOM | PART | INDEP | MIXED | LOW |
| 05 | - NODE_SPECIFIC | HET | SHARED | SHARED | MIXED | MIXED |
| 06 | - NODE_SPECIFIC | HET | SHARED | INDEP | MIXED | LOW |
| 07 | - NODE_SPECIFIC | HET | PART | SHARED | LOW | MIXED |
| 08 | - NODE_SPECIFIC | HET | PART | INDEP | LOW | LOW |
| 09 | + SHARED | HOM | SHARED | SHARED | HIGH | HIGH |
| 10 | + SHARED | HOM | SHARED | INDEP | HIGH | MIXED |
| 11 | + SHARED | HOM | PART | SHARED | MIXED | HIGH |
| 12 | + SHARED | HOM | PART | INDEP | MIXED | MIXED |
| 13 | + SHARED | HET | SHARED | SHARED | MIXED | HIGH |
| 14 | + SHARED | HET | SHARED | INDEP | MIXED | MIXED |
| 15 | + SHARED | HET | PART | SHARED | LOW | HIGH |
| 16 | + SHARED | HET | PART | INDEP | LOW | MIXED |

**Aliasing structure (core):** full 2^4 ⇒ all 15 factorial effects (4 main, 6 2FI, 4 3FI, 1 4FI) are mutually orthogonal and estimable; nothing is aliased. Required by ORDER §6: C, M, E, P; C×M, C×E, M×E, C×P — all estimable. The remaining 2FIs (M×P, E×P) are estimated and reported as secondary.

**Why the core must NOT be fractionated (verified alias computation, `/workspace/r10r9/work/calc/alias.py`):** the only 8-cell half fraction of 2^4 has defining relation I = CMEP (resolution IV; resolution definitions per NIST/SEMATECH handbook, L2-032). Its alias chains are:
`C=MEP, M=CEP, E=CMP, P=CME, CM=EP, CE=MP, CP=ME`.
So **C×P would be aliased with M×E** — two of the four mandatory interactions would be inseparable — and C×M with E×P, C×E with M×P. PR #45 M01 itself demands resolution ≥ V for any fraction (L2-002); no 2^(4−1) can satisfy that. ⇒ Fractionation of the core is rejected.

Cell-count economy, if budget forces it, must come from **fewer tasks or runs** (with the precision consequences in G06 §6), or from **dropping a whole factor** (PR #45 M01 falsifier suggests dropping P) — never from aliasing.

## 4. Optional COMM factor (K) and its aliasing

Option K-0 (recommended core): COMM is a **within-run stage** (S1 = OFF, S2 = ON) in all 16 cells. C×COMM and E×COMM are estimated as C×Stage and E×Stage interactions (paired within run). Caveat: Stage is confounded with "second attempt / extra reasoning opportunity".

Option K-1 (adds a sham control for that caveat): add between-cell factor K at Stage 2: `PEER` (see peers' answers) vs `SELF` (re-shown own answer and evidence only, same token budget). Then C×K and E×K isolate the *peer* component.
- **K-1-full: 2^5 = 32 cells** — no aliasing. Preferred.
- **K-1-half: 2^(5−1)_V, I = CMEPK, 16 cells.** Alias chains (computed): every main effect aliased only with a 4FI (`C=MEPK`, …, `K=CMEP`); every 2FI aliased only with a 3FI (`CM=EPK, CE=MPK, CP=MEK, CK=MEP, ME=CPK, MP=CEK, MK=CEP, EP=CMK, EK=CMP, PK=CME`). Valid **only under the explicit assumption that all 3FIs are negligible**, which must be preregistered and is a real risk (e.g., C×M×E — "constitution only homogenizes when models AND evidence are shared" — is a substantively plausible 3FI and would contaminate P×K). Furthermore, metrics defined only under K=PEER (retention, revision) would be computed on an 8-cell subset with I = CMEP (resolution IV) ⇒ **C×P = M×E aliasing returns**. ⇒ K-1-half is acceptable only for Stage-1/final-answer metrics, never for retention/revision metrics.

## 5. Auxiliary arms (outside the factorial, answering Q02 and the "no-constitution" ambiguity)

| Arm | Content | Placement | Purpose |
|---|---|---|---|
| A-PLACEBO | `C_PLACEBO`: shared, length-matched, non-normative text (e.g., neutral domain glossary), no truth-discipline content | in stratum S* = (M=HET, E=PART) × P∈{SHARED, INDEP} → 2 extra cells | Distinguish "constitution content" from "shared-prefix effect" (Q02). |
| A-NONE | No constitution at all (only schema/tooling) | same 2 cells | Distinguish "having a procedure" from "sharing a procedure". |
| A-ANCHOR | 5% of tasks re-run at start/middle/end in cells 01 and 16 | time anchor | Drift detection (G03 T16). |
| A-RETR (optional) | heterogeneous retrievers per node in cells 07/08/15/16 | sensitivity | Bounds shared-METHOD contribution (G03 T05). |

Auxiliary arms are analysed as pre-declared planned contrasts against cells 07/08/15/16, not entered into the factorial model.

Randomization (frozen seeds): task→time block; cell order within block; node slot→model (HET); task→HOM family; node→paraphrase (P=INDEP); node→constitution variant (C=NODE_SPECIFIC); task→which node-specific text is used as the shared text (C=SHARED); node→partition (E=PART); answer-option order.

## 6. MODEL-INDEPENDENCE REPORTING TABLE (ORDER §8; PR #45 M04)

**Rules.** `KNOWN` only if both models' training corpora are documented to a level that allows computing overlap (in practice: fully open-data models). `BOUNDED` if open weights and documented data sources/cutoffs allow partial bounds, or if a shared base checkpoint is documented (then *dependence* is bounded from below — known shared ancestry). `UNKNOWN` = default for any closed model and for any pair containing one. Pair status = the weaker of the two. A numeric independence value is permitted only if status = KNOWN (PR #45 M04). No row may claim independence that is not documented; correlated errors are empirically common across providers (L2-013).

**TEMPLATE (illustrative rows, NOT a model selection, NOT data):**

| SLOT | MODEL_PROVIDER | MODEL_FAMILY | MODEL_VERSION (pinned ID / fingerprint) | INFERENCE_CONFIG (temp, top_p, max_tokens, seed, system-slot) | KNOWN_SHARED_ANCESTRY | UNKNOWN_TRAINING_OVERLAP | MODEL_INDEPENDENCE |
|---|---|---|---|---|---|---|---|
| HET-a | `<closed provider A>` | `<family A>` | `<exact ID returned by API>` | `<frozen>` | none documented | YES (closed corpus) | UNKNOWN |
| HET-b | `<closed provider B>` | `<family B>` | `<exact ID>` | `<frozen>` | none documented | YES | UNKNOWN |
| HET-c | `<open-weight provider C>` | `<family C>` | `<weights SHA-256>` | `<frozen>` | `<base checkpoint, if any>` | PARTIAL (data card level) | BOUNDED (vs another open model) / UNKNOWN (vs closed) |
| HOM-x | = HET-a, -b or -c (rotated) | same | same | same | identical model ⇒ maximal shared ancestry | n/a | DEPENDENT_BY_CONSTRUCTION |
| JUDGE (secondary only) | `<provider ∉ subjects>` | `<family ∉ subjects>` | `<exact ID>` | `<frozen, temp 0>` | must be "none documented" with all subjects | YES if closed | UNKNOWN ⇒ never primary scorer |

Pair table to be reported: for each node pair in HET cells → (status, documented shared ancestry, stated cutoffs). **Consequence:** with ≥1 closed model, the M=HET level means *nominal* (provider/family) heterogeneity, and every conclusion must carry the qualifier `MODEL_INDEPENDENCE=UNKNOWN`.

## 7. Operationalization of the central test (ORDER §9)

**Target statement:** CONSTITUTION_OVERLAP_HIGH + EPISTEMIC_DEPENDENCE_LOW, WITHOUT ERROR_CORRELATION_INCREASE OR DISSENT_SUPPRESSION.

**Stratum:** S* = cells {07, 08, 15, 16} (M=HET, E=PART; P averaged). Contrast Δ_C = (C=SHARED) − (C=NODE_SPECIFIC) within S*. Global factorial interactions C×M and C×E (all 16 cells) are read alongside as the "does the constitution erase diversity" test (PR #45 H2D).

| ID | Predicate | Operational measure (G06 definitions) | Decision rule (frozen; margins `DEFAULT_PENDING_OPERATOR`) |
|---|---|---|---|
| CT1 | CONSTITUTION_OVERLAP_HIGH (manipulation check) | (a) textual identity of constitutions across nodes = 1.0 in C+, < frozen ceiling in C−; (b) behavioural adherence score (blind-scored checklist) in C+ ≥ frozen floor and > A-PLACEBO | Fail ⇒ central test `NOT_TESTED` (not PASS, not FAIL) |
| CT2 | EPISTEMIC_DEPENDENCE_LOW | SOURCE/DATA: document-level partition overlap = 0 (logs) and claim-level overlap ≤ ceiling; METHOD: retriever shared ⇒ reported `SHARED_METHOD`; MODEL: status from §6 | SOURCE/DATA must pass; MODEL = UNKNOWN allowed **only** with qualifier (MA-L2-02) |
| CT3 | NO ERROR_CORRELATION_INCREASE | Δ_C of pairwise error correlation (φ on error indicators, marginal-normalized) (φ_err, G06 M4) in S*, Stage 1 and Stage 2 | Non-inferiority: upper 95% CI bound of Δ_C(φ_err) < δ_φ (default 0.10; 0.05 needs T≈469–629 at R=3, G06 §6); and C×M, C×E on φ_err each within ±δ_φ (equivalence, L2-026) |
| CT4 | NO DISSENT_SUPPRESSION | Δ_C of JUSTIFIED_DISSENT_RETENTION (M2) and MINORITY_CORRECT_RETENTION (M3) at Stage 2 | Lower 95% CI bound of Δ_C(JDR) > −δ_d (default 0.05) and of Δ_C(MCR) > −δ_mc (default 0.10) |
| CT5 | NOT TRIVIALLY DECORRELATED | Δ_C of WARRANTED_CONVERGENCE (M1) | Lower 95% CI bound > −δ_wc (default 0.05) — prevents "PASS by making everyone noisier" |
| CT6 | PLACEBO DISCRIMINATION (reported, not part of PASS) | C+ vs A-PLACEBO on M1–M4 | If C+ ≡ A-PLACEBO (equivalence on all) ⇒ report "effect attributable to shared prefix" (Q02) |

**CENTRAL_PASS = CT1 ∧ CT2 ∧ CT3 ∧ CT4 ∧ CT5** (intersection–union test; each component at its own α, no α inflation).

### GATE G04-CENTRAL (§35 gate format)
| Field | Content |
|---|---|
| INPUT | Frozen prereg; E2 outputs for cells 01–16 + auxiliary arms; manipulation-check logs (G03 G03-B). |
| PREDICATE | CENTRAL_PASS as above. |
| PASS | `CENTRAL_TEST_PASS_C1_CONDITIONAL_ON{battery, models, versions, MODEL_INDEPENDENCE status}` — a descriptive statement about this configuration only. |
| FAIL | Any of CT3–CT5 fails with CT1, CT2 passing ⇒ `CENTRAL_TEST_FAIL_C1` (shared constitution associated with error-correlation increase / dissent suppression / convergence loss in this configuration) — this is a Soft-Lineage falsifier (Q01). |
| UNKNOWN | CT1 or CT2(SOURCE/DATA) fails, or CI too wide to decide (straddles margin) ⇒ `NOT_TESTED` / `INCONCLUSIVE_PRECISION`; never reported as PASS. |
| RECOVERY | Amendment (append-only) with new frozen block; precision shortfall ⇒ new study, not extension of the same data (no optional stopping). |
| FALSE_POSITIVE_RISK | Nominal model heterogeneity masks shared training data so errors are correlated in *both* C arms equally (Δ_C ≈ 0 even though dependence is high) — PASS would be uninformative about independence; mitigated by reporting absolute φ_err levels and HOM vs HET contrast. Judge/normalization artifacts (G03 T09/T10). |
| FALSE_NEGATIVE_RISK | Margins too strict for achievable precision ⇒ systematic `INCONCLUSIVE`; mitigated by G06 §6 precision plan. Constitution adherence floor too high for weaker models. |

**Answer to ORDER §9 "IF THIS CANNOT BE OPERATIONALIZED":** It *can* be operationalized for SOURCE/DATA/PROMPT/CONSTITUTION/COMMUNICATION/MEMORY. It *cannot* be operationalized for the MODEL component with closed models (training overlap UNKNOWN). Therefore:
- If the operator accepts `EPISTEMIC_DEPENDENCE_LOW := SOURCE/DATA low by construction + MODEL nominally heterogeneous (UNKNOWN)` → central test operationalizable (conditional).
- If the operator requires MODEL dependence demonstrably low → **`HOLD_C1_E2_CAUSAL_IDENTIFIABILITY_UNRESOLVED`** unless all HET models are open-data (KNOWN) — which changes the population to which results apply.

## 8. Material ambiguities (ORDER §1 format)

### MA-L2-01 — Meaning of C = NO
| Field | Content |
|---|---|
| ASSUMPTION_OPTIONS | (A) no constitution; (B) node-specific, length-matched constitutions; (C) both as 3-level factor. |
| CONSEQUENCE_MATRIX | A: C effect = "having a procedure" + "sharing it" + prompt length (confounded). B: C effect = "sharing" only (cleanest for Soft-Lineage). C: cleanest, +50% C-cells cost, breaks 2-level factorial. |
| RECOMMENDED_DEFAULT | B in the factorial; A and placebo as auxiliary arms (§5). |
| BLOCKS_WHAT | Prereg freeze of the C manipulation. |
| DOES_NOT_BLOCK_WHAT | Task battery, metrics, power plan, Part B. |

### MA-L2-02 — Does EPISTEMIC_DEPENDENCE_LOW require MODEL independence?
| Field | Content |
|---|---|
| ASSUMPTION_OPTIONS | (A) SOURCE/DATA low + MODEL nominal (UNKNOWN); (B) MODEL must be KNOWN-low. |
| CONSEQUENCE_MATRIX | A: test runs with closed models; every claim qualified. B: only open-data models; HOLD with closed models; narrower generality, smaller capability range. |
| RECOMMENDED_DEFAULT | A, with mandatory qualifier and a secondary open-weight-only replication stratum if feasible. |
| BLOCKS_WHAT | Wording of the central claim; choice of model list. |
| DOES_NOT_BLOCK_WHAT | Design structure, battery, metrics. |

### MA-L2-03 — PR #45 M03 "D_EPISTEMIC held constant low across constitution arms"
| Field | Content |
|---|---|
| ASSUMPTION_OPTIONS | (A) "balanced across C arms" (orthogonality); (B) literally constant low in all cells (would remove M and E as factors). |
| CONSEQUENCE_MATRIX | A: consistent with M01 2^4. B: contradicts M01; would collapse design to a 2^2 (C×P) in stratum S* only — cheaper, but loses C×M, C×E (the critical H2D tests). |
| RECOMMENDED_DEFAULT | A. Ask AXIOM adjudication to correct the M03 wording. |
| BLOCKS_WHAT | Nothing if A is adopted. |
| DOES_NOT_BLOCK_WHAT | Everything else. |

### MA-L2-04 — Retention/revision metrics need an exposure stage
| Field | Content |
|---|---|
| ASSUMPTION_OPTIONS | (A) 2-stage protocol in all cells (K-0); (B) between-cell COMM factor; (C) aggregation-only (no revision). |
| CONSEQUENCE_MATRIX | A: retention estimable in all 16 cells; stage confounded with second attempt. B: needs 2^5 full for clean retention interactions. C: retention reduces to "does majority vote keep minority-correct" — trivial and not a node property. |
| RECOMMENDED_DEFAULT | A, plus K-1-full if budget allows. |
| BLOCKS_WHAT | Definition of M2/M3/M6 in prereg. |
| DOES_NOT_BLOCK_WHAT | M1, M4, M5 on Stage 1. |

## 9. Major claim (§35)

| Field | Content |
|---|---|
| OBSERVATION | A full 2^4 with capability-balanced M, node-specific-constitution C−, closed-world partitioned E, paraphrase P, and a 2-stage exposure protocol makes all mandatory effects estimable without aliasing; the only half fraction (I=CMEP) aliases C×P with M×E. |
| SOURCE | alias computation (local script); L2-032 (resolution definitions); L2-002 (PR #45 M01 resolution-V rule); L2-013 (accuracy–error-correlation link motivating capability balancing); L2-016 (prompt-format sensitivity motivating P control). |
| SOURCE_CLASS | VENDOR_OR_PROJECT_DOC (NIST handbook; repo); PEER_REVIEWED conference / PREPRINT (L2-013, L2-016). |
| INTERPRETATION | Identifiability is a design property and is achievable; what remains non-identifiable is MODEL independence with closed models. |
| ALTERNATIVE | A cheaper 2^2 (C×P) inside stratum S* would test the central predicate directly at 1/4 cost but cannot detect "constitution collapses diversity only when models/evidence are shared" (C×M, C×E). |
| UNCERTAINTY | 3FIs unknown; capability balancing is approximate; paraphrase equivalence is human-judged. |
| FALSIFIER | If E1 shows constitution text cannot be varied without changing prompt-format effects of similar size (i.e., C+ ≈ A-PLACEBO everywhere), C is not separable from P in practice ⇒ REDUCE to a prompt-sharing study. |
| IMPACT_ON_R10R9 | G04 becomes the factorial spec for AXIOM adjudication; PR #45 M01 should add M×E and C×P to the preregistered estimable set and adopt MA-L2-01-B. |
