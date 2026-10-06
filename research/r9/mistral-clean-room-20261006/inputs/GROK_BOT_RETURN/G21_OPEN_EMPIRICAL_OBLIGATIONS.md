# G21 — OPEN EMPIRICAL OBLIGATIONS (R10R9, consolidated from lanes 1–3)

```text
OBJECT        = R10R9_G21_OPEN_EMPIRICAL_OBLIGATIONS_SYNTHESIS_20261005_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SCOPE         = obligations that need data: pilots, experiments, dataset verification, implementation tests.
                Nothing here has been executed. R10R6 E2 NOT executed. No human or LLM subject was used.
OWNER ROLES   = AXIOM (release and adjudication) · operator (inputs, budget, ethics decisions) ·
                executor (as released by AXIOM; GROK-BOT does not self-release, ORDER sec. 38)
PRECONDITION  = Every EO below that involves running models, generating data or recruiting people
                needs an explicit AXIOM execution release for its part (ORDER sec. 38).
LAST_VERIFIED = 2026-10-05 (Europe/Berlin)
```

## A. Part A (H_SP shared-policy-text configuration test)

| ID | Obligation | Origin | Owner | Prerequisites | Blocks | Does NOT block | Success / discharge criterion |
|---|---|---|---|---|---|---|---|
| EO-A1 | **E1 calibration pilot** on a disjoint item set. Estimates DEFF; puts S1 accuracy in the 0.35–0.85 band; sets adherence floors per model family; runs the contamination / prior-knowledge probe (`PARAMETRIC_LEAK` tagging); checks determinism at temperature 0. No H_SP hypothesis is tested. | PR #45 M05 (L2-002); G03 R-08, R-16; G06 sec. 6, 13; GAP-L2-06 | executor; operator supplies the model list | PO-A2, PO-A8; model list | G06-PRECISION gate; prereg freeze; final T | Design | E1 receipt hashed; DEFF upper 80% CI bound recorded |
| EO-A2 | Blind neutrality rating of the A-PLACEBO text, plus a length/structure match check of the C− (node-specific) texts. | G04 sec. 5; answers_lane2 Q02 | executor (raters outside lineage) | Texts drafted | CT6 interpretation; prereg freeze | Battery | ≥ 2 blind raters; agreement threshold met |
| EO-A3 | Human equivalence validation of the P=INDEP paraphrase pool. | G03 R-13 | executor | Pool drafted | P manipulation validity | C manipulation | Pool frozen with equivalence ratings |
| EO-A4 | Author the battery outside the lineage, from G05 templates (7 classes; recommended 400 = 6×43 + 142 MINORITY_CORRECT). Verify claim-level disjointness by script. Run the prior-knowledge probe. | G05; G03 R-01…R-06; MA-L2-06 | operator (commission writers), executor (scripts) | PO-A1 | A-MIN, A-FULL | B0, C | Battery JSON frozen and hashed; disjointness script PASS |
| EO-A5 | **A-MIN (first experiment, E2-stage-1)**: S* only (M=HET with 3 capability-balanced models, E=PART, P=SHARED); arms C+ / C− (NODE_SPECIFIC) / A-PLACEBO; 2-stage; ≈300 tasks (≥281 designed-minority items), R=3 → 16,200 node-calls (R=5 alternative: ≈185 tasks, ≈16,650 calls). Tests CT3 and CT4 at margin 0.10, plus CT6. | answers_lane2 Q25; G06 sec. 6; work/calc/power_calc_2_output.txt | executor | AXIOM Part-A release (sec. 38); EO-A1..A4; PO-A1..A9 | A-FULL; any falsification statement for H_SP | B0, C | Preregistered CT3/CT4 decision (PASS / FAIL / INCONCLUSIVE_PRECISION) with receipt |
| EO-A6 | **A-FULL**: full 2^4 (C, M, E, P), 16 cells, T=400, R=3, n=3, 2 stages (115,200 node-calls), plus auxiliary arms A-PLACEBO, A-NONE (28,800), A-ANCHOR (5%), optional A-RETR. Primary family of 8 (C, M, E, P, C×M, C×E, M×E, C×P), Holm FWER. | G04 sec. 3, 5; G06 sec. 4, 6 | executor | A-MIN PASS (lane 2 Q25; FAIL ⇒ report falsification, INCONCLUSIVE ⇒ new larger study); separate AXIOM release; G06-PRECISION PASS | Generality claims ("constitution erases diversity", C×M/C×E) | A-MIN reporting | Preregistered F1–F4 analyses with receipt |
| EO-A7 | Run-time manipulation checks (G03-B): document-level partition overlap = 0; zero peer tokens in Stage 1; zero canary carry-over; constitution adherence C+ ≥ floor and > placebo. | G03 sec. 3 | executor | During EO-A5/A6 | Outcome unblinding | — | Gate G03-B PASS per cell |
| EO-A8 | Drift control: pinned versions or fingerprints per call; interleaved blocks; anchor set at start, middle and end. | G03 T16 | executor | During EO-A5/A6 | Validity of cross-time comparisons | — | Drift within frozen tolerance or blocks flagged |
| EO-A9 | Optional open-weight-only replication stratum (makes MODEL_INDEPENDENCE BOUNDED for those pairs). | MA-L2-02; G04 sec. 6 | operator (decide), executor | A-MIN | MODEL-dependence statements beyond UNKNOWN | Main analysis | Replication with weight hashes |
| EO-A10 | Optional A-RETR sensitivity (heterogeneous retrievers) to bound the shared-METHOD contribution. Default is no retrieval (in-packet evidence). | G03 T05; answers_lane2 Q05 | executor | Retrieval used at all | Claims about METHOD independence | Main analysis | φ_err difference reported |

## B. Part B

| ID | Obligation | Origin | Owner | Prerequisites | Blocks | Does NOT block | Success / discharge criterion |
|---|---|---|---|---|---|---|---|
| EO-B1 | Implement and validate the B0 generator (G1–G21 parameters; GT objects TRUE_TRACKS, TRUE_DISAPPEARANCE, TRUE_FALSE_DETECTION_REGIONS, TRUE_SIGNAL_LOSS_WINDOWS, DRIFT, DOSE; generator receipt). | G08 sec. 3–4 | executor | AXIOM B0 release; PO-B1, PO-B3 | All B0 runs | Part A, C | GT consistency checks PASS; generator hash frozen |
| EO-B2 | **B-MIN**: VESICLE scenario, SNR {2, 4} × density MID, 20 TEST movies per condition. Δ-PH vs Δ-COST on u-track/LAP at matched coverage 0.80. | answers_lane2 Q25 | executor | EO-B1 | Decision whether PH earns a place | Full B0 | Paired movie-level bootstrap decision |
| EO-B3 | Full B0: 24-condition core grid + stress arms (MS, OCC, DRIFT, BLEACH, TOX proxy, PSF-misspecified) + 2^3 sub-factorial; fair pipeline panel P1–P8, P-PH, P-PH-V; equal tuning budgets; random-hold null comparator. H-B0-1 and H-B0-2. | G08 sec. 3, 6, 7; G10 | executor | EO-B1; DEV-pilot variance for n_TEST | G08-B0 PASS; any B1 attempt | Part A, C | G08-B0 gate decision |
| EO-B4 | Verify B1 candidate datasets before use: DS-1 MSP-tracker data (L2-131) annotation protocol, trajectory count, dose metadata, licence/version. DS-2 ExoDeepFinder is event-level only. DS-3 ISBI download availability is UNVERIFIED. | G09 sec. 3 | executor | — (read-only verification can run any time) | B1 | B0 | Dataset record with DOI, version, hash, annotation level |
| EO-B5 | B1 replication of H-B0-1 on real data, with frozen transfer, split by cell/sample, and annotator-ceiling reporting. | G09 sec. 4–5 | executor | G08-B0 PASS; EO-B4; R1–R5, R7, R9, R10 met; AXIOM release | `B1_REAL_DATA_TRACKING_VALIDATION_C1` | — | G09-B1 gate decision |
| EO-B6 | Phototoxicity: **not in R10R9 scope**. It would require a biological endpoint (division timing, morphology, viability or functional readout) with dark/low-dose controls and dose–response (L2-130). | G09 sec. 2 | operator (scope decision) | Wet-lab data | Any phototoxicity claim | Everything in R10R9 | Not planned |

## C. Part C and integration

| ID | Obligation | Origin | Owner | Prerequisites | Blocks | Does NOT block | Success / discharge criterion |
|---|---|---|---|---|---|---|---|
| EO-C1 | Implement the negative fixture suite G-C01…G-C11 (scope/expiry escalation, audience/parent/key swap, replay, reordering, cycle, orphan, revoked key, unknown trust root) plus positive fixtures against a Biscuit-or-COSE + SCITT profile. | G11 sec. 5 | executor | PO-C1..C5; AXIOM C release | NAC profile PASS | Part A, B | All negatives rejected; positives accepted |
| EO-C2 | Integration fixtures G-I01..G-I04: protocol version pin; token ≠ authority; AgentCard signature scope; tool output untrusted. | G13 sec. 4 | executor | EO-C1 | Any A2A/MCP adapter claim | — | Fixtures pass |
| EO-C3 | **Falsification test of the NEXUS epistemic layer**: a preregistered comparison in which NEXUS claim-ceiling/epistemic gates are tested for whether they detect claim inflation that a SCITT + Biscuit + PROV profile without them misses, at a measured false-positive rate. | answers_lane1 Q20 | executor; AXIOM | EO-C1; claim-ceiling checker (EO-F3) | Any "distinctly NEXUS" contribution claim | Profile adoption | Preregistered detection/FP comparison |

## F. Framework, metaphor, information density

| ID | Obligation | Origin | Owner | Prerequisites | Blocks | Does NOT block | Success / discharge criterion |
|---|---|---|---|---|---|---|---|
| EO-F1 | Metaphor three-condition study (FORMAL_ONLY / METAPHOR_ONLY / METAPHOR_PLUS_DECODE_KEY; G15 fixtures MP-01..MP-10). Primary outcome MATERIAL_FIR non-inferiority (default Δ_FI 0.05, a judgement call). H3 positive control. Optional repeated-exposure variant to test amortisation. | G14 sec. 5; answers_lane3 Q21 | operator (ethics review and consent), executor | Ethics review; independent adjudication of G15 keys | Any rule *allowing* metaphors in normative text | The safe default "formal text first; no metaphor in gates" | Preregistered H2 decision per pooled/concept level |
| EO-F2 | Order-profile relay-error study: minimal vs self-contained vs self-contained + JSON twin. Outcomes M8, M7 (relay errors) and M6, M3 (opacity). | G18 sec. 2 | executor; operator | Multiple writers per condition | Any claim that self-contained orders reduce relay errors | Profile adoption as hygiene | Relay errors reduced with non-inferior RA |
| EO-F3 | Build and evaluate a claim-ceiling checker (rejects over-ceiling statements; measures claim-inflation reduction vs plain review). | G17 MC-G17-3; G19 sec. 9.3 | executor | PO-C4 (C-ladder) | Any NEXUS tool-contribution claim | — | Measured reduction at reported FP rate |
| EO-F4 | Independent re-tagging of the G16 coverage matrix by a reviewer outside the lineage, plus a systematic (not only targeted) prior-art search for "agent research order profiles". | G17 sec. 5 | executor (non-lineage) | — | Upgrading the G17 REDUCE result from PASS_WITH_CAVEATS | Current REDUCE verdict | Agreement statistic reported |
| EO-F5 | Evaluate the registry-backed referential-closure checker: precision/recall against independent human adjudication (prototype precision ≈ 0.17 without a registry). | G18 sec. 4.3; answers_lane3 Q23 | executor | PO-F3 registry | Using RC as a release gate | — | Checker misses 0 material refs on test orders |
| EO-F6 | Seeded-defect experiment for NEVER_COMPRESS (does compressing a listed item raise error propagation?). | answers_lane3 Q24; G18 M7 | executor | EO-F2 infrastructure | Empirical support for the list | Adopting the list as a conservative default | Preregistered M7 comparison |

## Execution order (recommended, each step gated)
1. Read-only and no-subject tasks first: EO-B4, EO-F4. They may run under ordinary AXIOM tasking.
2. Part A: EO-A2, EO-A3, EO-A4 → EO-A1 (E1) → **EO-A5 A-MIN** → (only on A-MIN PASS) EO-A6 A-FULL.
3. Part B: EO-B1 → **EO-B2 B-MIN** → EO-B3 → (only with data) EO-B4 → EO-B5.
4. Part C: after PO-C1..C5 → EO-C1 → EO-C2 → EO-C3.
5. Framework/metaphor: EO-F1 (ethics first), EO-F2, EO-F3, EO-F5, EO-F6 are independent of Parts A–C.
