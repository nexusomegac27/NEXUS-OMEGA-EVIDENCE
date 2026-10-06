# G23 — R10R9 REVISED MASTER PREREGISTRATION (draft; executable but NOT released)

```text
OBJECT          = R10R9_G23_REVISED_MASTER_PREREGISTRATION_SYNTHESIS_20261005_R0
STATUS          = DRAFT_NOT_FROZEN · NOT_RELEASED · NOTHING EXECUTED · R10R6 E2 NOT EXECUTED
CLAIM_CEILING   = C1_DESCRIPTIVE_ONLY (for this document and for every result it could produce)
AUTHOR          = GROK-BOT external non-lineage reviewer (synthesis of lanes 1–3). Not AXIOM.
INTEGRATES      = G03, G04, G05, G06 (Part A) · G08, G09, G10 (Part B) · G11, G12, G13 (Part C) ·
                  G14, G15, G17, G18 (framework/metaphor) · G07 (gate verdicts) · G20/G21 (obligations)
LAST_VERIFIED   = 2026-10-05 (Europe/Berlin)
```

> **EXECUTION RELEASE CONDITION (ORDER sec. 38).** GROK-BOT does not release execution. No part of this preregistration may be executed until this sequence has completed: **GROK_RETURN → AXIOM source/content adjudication → R10R6 external-non-lineage gate decision → AXIOM explicit Part-A execution release.** Only then may empirical R10R9-A (starting with E1, then A-MIN) begin. **B0 and C each need their own separate AXIOM execution release**, and only after their own gates (G08-B0 and G-C, G07 sec. 3) pass. Freezing this document requires every parameter in sec. 3 marked `UNSET` to be set, and its hash recorded, before the first model call.

## 1. Framing (after reduction)

- **Part A is preregistered as a shared-policy-text configuration test**, label **H_SP** (G07 verdict `REDUCE_TO_STANDARD_POLICY_CONFIGURATION_TEST`). It is **not** a Soft-Lineage validation. If AXIOM adopts a hash-bound definition equating Soft-Lineage with exactly the C manipulation (PO-A1, Alternative A1), the H_SP result may be cited as "the operational Soft-Lineage test under definition <hash>", still at C1.
- **Part B** is split into **B0** (synthetic POC; never biological validation) and **B1** (real-data roadmap; not executed unless data is available). PH is a **demoted optional arm**. Δ is tested **only as a hold/abstention policy**.
- **Part C** is a **profile** (Biscuit-or-COSE capsule + SCITT registration + NEXUS claim-ceiling field). It is not a new token format. Its gate is on HOLD until a trust model exists.
- **Governance invariants** (ORDER sec. 2): no claim above C1; no "validated" language for Soft-Lineage or B0; WCA/WAL is an expired individual draft; hash/signature/SCITT ≠ truth; A2A/MCP ≠ NEXUS governance; metaphor ≠ mechanism; synthetic success ≠ external validity.
- **Terminology** (PO-F2, PO-F6): factor C = "shared policy text P_c (hash)". `AIR_GAP` is not used; it is replaced by `UNRESOLVED` (state) and `NCI_RELATION` (relation). Any remaining metaphor in this document is a registry alias only (NEVER_COMPRESS, answers_lane3 Q24).

## 2. Hypotheses and falsifiers (frozen wording candidates)

| ID | Hypothesis | Primary test | Falsifier | Source |
|---|---|---|---|---|
| H_SP-1 | In S* (M=HET, E=PART), C+ (same policy text) vs C− (node-specific texts) does not increase pairwise error correlation φ_err by ≥ δ_φ. | CT3: one-sided NI, upper 95% CI of Δ_C φ_err < δ_φ | F-SL1(a) | G04 sec. 7 |
| H_SP-2 | C+ does not suppress justified dissent (JDR) or designed minority-correct retention (MCR). | CT4: lower 95% CI of Δ_C JDR > −δ_d and of Δ_C MCR > −δ_mc | F-SL1(b) | G04 sec. 7 |
| H_SP-3 | C+ does not trivially decorrelate by lowering warranted convergence. | CT5: lower 95% CI of Δ_C WC > −δ_wc | CT5 fails | G04 sec. 7 |
| H_SP-4 | C does not erase diversity created by model or evidence heterogeneity. | F3: TOST equivalence of C×M and C×E on φ_err within ±δ_φ (A-FULL only) | F-SL1(c): TOST-confirmed positive C×M or C×E | G06 sec. 4 |
| H_SP-5 (descriptive) | C+ effect differs from a shared length-matched placebo text. | CT6 (reported, not part of PASS) | C+ ≡ A-PLACEBO on M1–M4 ⇒ "effect attributable to shared prefix" | G04 sec. 5, 7 |
| H-B0-1 | Δ as a HOLD policy reduces HIGH_COST_FP at COVERAGE ≥ 0.80 by ≥ 25% relative to the best non-Δ-PH hold policy, with ΔFNR ≤ +5 pp. | Paired movie-level bootstrap on TEST | G08-B0 FAIL conditions | G08 sec. 7 |
| H-B0-2 | P-PH or Δ-PH beats the best non-PH pipeline or hold policy on β, HOTA or AURC(HIGH_COST_FP) in ≥ 1 condition family (Holm). | Same | Otherwise PH stays DEMOTED | G08 sec. 7 |
| H-C-1 | The NAC profile rejects all negative fixtures G-C01..G-C11. | Fixture suite | Any negative accepted | G11 sec. 5 |

**CENTRAL_PASS (Part A) = CT1 ∧ CT2 ∧ CT3 ∧ CT4 ∧ CT5** (intersection-union test). CT1 = manipulation check (textual identity plus blind behavioural adherence above floor and above placebo). CT2 = SOURCE/DATA partition overlap 0 (claim-level ≤ ceiling); MODEL status reported with qualifier. CT1 or CT2 failure ⇒ `NOT_TESTED`, never PASS.

## 3. Parameters (operator / AXIOM inputs; unset ones are explicit, with safe defaults)

`UNSET` = must be set before freeze; the safe default applies only for planning and is the conservative, reversible choice. `DEFAULT_PENDING_OPERATOR` = lane-proposed value to confirm or replace. `SYNTHESIS_SAFE_DEFAULT` = added in this synthesis as the most restrictive reversible option, not taken from a lane.

### 3.1 Part A
| Parameter | Status | Safe default / planning value | Source |
|---|---|---|---|
| SOFT_LINEAGE_DEFINITION | UNSET | Use the H_SP label; no lineage claim (PO-A1) | MA-L3-03; G07 |
| MODEL_LIST (HET-a/b/c; pinned IDs, fingerprints, inference config) | UNSET | Template only (G04 sec. 6). Any closed model ⇒ MODEL_INDEPENDENCE = UNKNOWN; pair status = weaker of two | GAP-L2-05 |
| HOM capability balancing | DEFAULT_PENDING_OPERATOR | HOM model rotated across the 3 HET families, balanced per task | G04 sec. 2 |
| EPISTEMIC_DEPENDENCE_LOW requirement | DEFAULT_PENDING_OPERATOR | Option A: SOURCE/DATA low by construction + MODEL nominal (UNKNOWN), with mandatory qualifier | MA-L2-02 |
| C− definition | DEFAULT_PENDING_OPERATOR | NODE_SPECIFIC, independently authored, length ±5%, same skeleton and procedural checklist; A-NONE and A-PLACEBO as auxiliary arms | MA-L2-01 (B) |
| Constitution texts C+/C−, placebo text, paraphrase pool | UNSET | Must be authored, blind-rated (placebo neutrality; paraphrase equivalence) and hashed | EO-A2, EO-A3 |
| Exposure protocol | DEFAULT_PENDING_OPERATOR | 2-stage (S1 independent; S2 peer answers + justifications, not evidence); K-1-full 2^5 optional; never K-1-half for retention metrics | MA-L2-04; G04 sec. 4 |
| n nodes per team | DEFAULT_PENDING_OPERATOR | 3 | G04 sec. 1 |
| MESOI (smallest interaction of interest) | UNSET | 5 pp planning; sensitivity 3–10 pp | GAP-L2-05; G06 sec. 6 |
| δ_φ (φ_err NI margin) | UNSET | 0.10 (0.05 requires T≈469–629 at R=3) | G04 sec. 7; G06 sec. 6 |
| δ_d (JDR margin) | UNSET | 0.05 | G04 sec. 7 |
| δ_mc (designed MCR margin) | UNSET | 0.10 (0.15 if T is limited) | G04 sec. 7; G06 sec. 6 |
| δ_wc (WC margin) | UNSET | 0.05 | G04 sec. 7 |
| α | DEFAULT_PENDING_OPERATOR | F1: Holm FWER 0.05 over 8 (planning Bonferroni 0.00625); F2: one-sided 0.025 per IUT component; F3: TOST 0.05; F4: BH-FDR q = 0.05 | G06 sec. 4 |
| DEFF | UNSET until E1 | 3 (conservative) if E1 not run | G06 sec. 13 |
| R (runs per task × cell) | DEFAULT_PENDING_OPERATOR | 3 at frozen non-zero temperature, plus R=1 at temperature 0 as determinism probe | G03 sec. 2 |
| Temperature / decoding values | UNSET | Frozen per model; recorded in the receipt | G06 sec. 11 |
| T_AMIN | DEFAULT_PENDING_OPERATOR | ≈300 tasks, ≥281 designed-minority items (MINORITY_CORRECT / PARTIALLY_OBSERVABLE), R=3 (alt. ≈185 at R=5) | answers_lane2 Q25 |
| T_FULL | DEFAULT_PENDING_OPERATOR | 400 adjudicable tasks = 6 classes × 43 + 142 MINORITY_CORRECT | G05; G06 sec. 6 |
| Battery authorship | DEFAULT_PENDING_OPERATOR | ≥ 1 template family authored by a party outside the NEXUS lineage; closed synthetic world; prior-knowledge probe | MA-L2-06; G05 |
| Battery reuse | SYNTHESIS_SAFE_DEFAULT | E1, A-MIN and A-FULL item sets mutually disjoint (supports "replicated on a fresh battery", Q01) | answers_lane2 Q01 |
| Retrieval | DEFAULT_PENDING_OPERATOR | None: evidence in-packet, web/tools disabled. If retrieval is used: per-node index, frozen deterministic retriever, logged IDs, A-RETR sensitivity | G03 T05 |
| Evaluator | UNSET (identity/hash) | Deterministic scorer primary; blind human audit ≥ 10% stratified by cell; ≥ 2 blind raters for justification; LLM judge secondary only, out-of-family, identity-stripped | G03 T10; G06 sec. 1 |
| Adherence floor (CT1) | UNSET until E1 | Per model family from E1 | G03 G03-B |
| Missing-data thresholds | DEFAULT_PENDING_OPERATOR | Cell missingness > 10% ⇒ CELL_FLAG; C-arm missingness difference > 5 pp ⇒ central test UNKNOWN; worst/best-case bounds | G06 sec. 10 |
| Retries | DEFAULT_PENDING_OPERATOR | API error: ≤ 2 identical retries then MISSING; schema-invalid: 1 frozen re-ask then WRONG_NON_ABSTAIN; canary violation: invalidate, 1 fresh re-run | G06 sec. 8 |
| Drift anchors | DEFAULT_PENDING_OPERATOR | 5% of tasks re-run at start, middle and end (cells 01 and 16); interleaved blocks; tolerance UNSET | G03 T16; G04 sec. 5 |
| Run window | UNSET | Whole design within one frozen window | G03 T16 |
| Seeds | UNSET | Published in receipt (task order, cell block, node slot, HOM family, paraphrase, constitution variant, partition, option order) | G06 sec. 12 |

### 3.2 Part B
| Parameter | Status | Safe default / planning value | Source |
|---|---|---|---|
| Δ definition | UNSET (U09) | A-Δ1..A-Δ3 (segment score; HOLD iff Δ > τ; τ from DEV only); Δ-PH, Δ-COST, Δ-DISAGREE preregistered separately | G08 sec. 2 |
| Coverage operating point | DEFAULT_PENDING_OPERATOR | 0.80 | G08 sec. 7 |
| HIGH_COST_FP reduction margin | DEFAULT_PENDING_OPERATOR | ≥ 25% relative; ΔFNR ≤ +5 pp; held-true share ≤ 2× held-false share | G08 sec. 7–8 |
| Generator parameters G1–G21 | DEFAULT_PENDING_OPERATOR | As G08 sec. 3 (design assumptions, not claims about real vesicles) | G08 sec. 3 |
| n_TEST | DEFAULT_PENDING_OPERATOR | 20 movies per condition; increase if the DEV-pilot CI half-width exceeds 1/2 of the margin | G08 sec. 7 |
| Tuning budget | DEFAULT_PENDING_OPERATOR | Equal for all pipelines (e.g., 100 random-search configs; frozen spaces) | G08 sec. 6 |
| Gate distance ε | DEFAULT_PENDING_OPERATOR | 5 px (ISBI convention) | G08 sec. 5.1 |
| B1 dataset | UNSET | DS-1 MSP-tracker data (L2-131) after verification (EO-B4); otherwise `NOT_EXECUTED_DATA_UNAVAILABLE` | G09 sec. 3 |

### 3.3 Part C
| Parameter | Status | Safe default / planning value | Source |
|---|---|---|---|
| TRUST_ANCHOR set | UNSET | **Empty ⇒ every AUTHORIZED = UNKNOWN ⇒ deny** | G11 G-C11; PO-C1 |
| Signature algorithm | DEFAULT_PENDING_OPERATOR | Ed25519, pinned in protected bytes; reject `none`/unknown | G11 sec. 2 |
| Canonical serialization | UNSET | Exactly one of RFC 8785 JCS or deterministic CBOR/COSE (no dual encodings) | G11 sec. 2; PO-C5 |
| Scope grammar | UNSET | Enumerated scopes only; wildcard/free text ⇒ UNKNOWN ⇒ deny | G11 G-C01 |
| Expiry policy | DEFAULT_PENDING_OPERATOR | Reject child-exp > parent-exp (no silent clamp) | G11 sec. 4 |
| Clock skew bound | UNSET | SYNTHESIS_SAFE_DEFAULT: undefined bound ⇒ time predicate UNKNOWN ⇒ deny | G11 G-C02 |
| MAX_DEPTH | UNSET | SYNTHESIS_SAFE_DEFAULT: 1 (no re-delegation) until the operator sets a value | G11 sec. 4, G-C08 |
| Revocation source | UNSET | Absent/stale ⇒ UNKNOWN ⇒ deny for high-impact scopes | G11 G-C10 |
| CLAIM_CEILING ladder | UNSET (U08) | Only C1 permitted; any higher ceiling ⇒ reject | PO-C4 |
| Protocol pins | DEFAULT_PENDING_OPERATOR | A2A protocol "1.0" (latest release v1.0.1); MCP "2026-07-28"; others ⇒ NAC-0 only | G13 G-I01 |

## 4. PART A protocol

### 4.1 Common elements (all stages)
- **Unit:** team of n=3 nodes; fresh stateless sessions per (node, task, run); provider memory off; canary items (G03 T07).
- **Prompt segments (frozen):** CONSTITUTION (varies with C) · TASK (varies with P) · OUTPUT_SCHEMA and TOOLING (identical in all cells; declared as fixed shared D_CONTROL) (G03 T06).
- **Two-stage protocol:** S1 independent answer + confidence + cited evidence IDs + justification; S2 peer answers and justifications shown (not evidence), revision allowed (G04 sec. 1).
- **Evidence:** closed synthetic world; document- and claim-level disjoint partitions under E=PART; no web; citation audit (G05; answers_lane2 Q04).
- **Metrics:** M1 WC/UC/WR; M2 JDR (with UDA); M3 MCR designed (primary) and emergent; M4 φ_err (+ EJE, same-wrong-answer rate); M5 Brier (+ ECE, AURC); M6 NRG/RP/revision rate. Each has a full sec. 35 metric record in G06 sec. 2.
- **Controls R-01…R-22 and gates G03-A (pre-freeze control completeness) and G03-B (run-time manipulation checks)** as in G03.
- **Blinding:** subjects are blind to the hypothesis; adjudicators are blind to cell and model (constitution echoes redacted); the analyst works on masked data until the analysis-code hash is logged; blinding check (G03 T15).
- **Randomization:** seeded and published (G04 sec. 5).
- **Stopping:** fixed N; no efficacy interim; one blind infrastructure checkpoint at ≈5% of calls; budget exhaustion ⇒ `INCOMPLETE_FIXED_N`, with precision-dependent conclusions INCONCLUSIVE; more data requires a new study ID (G06 sec. 7).
- **Missing data:** missing ≠ wrong; MAR primary; worst/best-case bounds; thresholds per sec. 3.1 (G06 sec. 10).
- **Exclusions:** only the pre-declared G05 EXCLUSION_RULE items (no defensible adjudication; PARAMETRIC_LEAK; partition-integrity failure; infrastructure failure). Never outcome-based.
- **Version freeze and receipt:** all hashes per G06 sec. 11. Receipt per G06 sec. 12 satisfying RECEIPT_COMPLETENESS_RULE (L2-004). Append-only amendment log.

### 4.2 Stage E1 — calibration pilot (no hypothesis test)
Disjoint items. Outputs: DEFF (upper 80% CI used for planning), S1 accuracy band 0.35–0.85, adherence floors, contamination probe results, determinism probe. Then **G06-PRECISION gate**: if the planned T is insufficient at the E1 DEFF ⇒ drop P, widen margins with operator sign-off, or raise R. **Never fractionate.**

### 4.3 Stage A-MIN — FIRST EXPERIMENT (E2-stage-1)
| Element | Specification |
|---|---|
| Cells | S* only: M=HET (3 capability-balanced families), E=PART, P=SHARED |
| Arms | **C+** (shared policy text, rotated across tasks) · **C−** (NODE_SPECIFIC) · **A-PLACEBO** (shared, length-matched, non-normative text) |
| Battery | ≈300 tasks, ≥281 designed-minority items; R=3 (alt. ≈185 tasks at R=5) |
| Calls | 300 × 3 arms × 3 runs × 3 nodes × 2 stages = **16,200 node-calls** |
| Tests | CT1, CT2 (manipulation and partition) → CT3 (margin 0.10), CT4 (margin 0.10), CT5; CT6 reported |
| Can show | Falsification of H_SP-1/2/3 for this configuration (F-SL1 a/b); placebo discrimination (H_SP-5) |
| Cannot show | C×M, C×E (no H_SP-4); main effects M, E, P; any generality |
| Decision | PASS ⇒ A-FULL may be requested (separate AXIOM release). FAIL ⇒ H_SP falsified for this configuration; report it. INCONCLUSIVE_PRECISION (e.g., DEFF > 2) ⇒ new, larger study, not an extension (lane 2 Q25, G06 sec. 7). |

### 4.4 Stage A-FULL — repaired full design (only after A-MIN PASS and a separate AXIOM release)
- **Core:** full 2^4 over C (NODE_SPECIFIC / SHARED), M (HOM capability-balanced / HET), E (SHARED / PART), P (SHARED / INDEP) = 16 cells. Every task in all 16 cells. **No aliasing**: all 4 main effects and all 6 two-factor interactions are estimable (G04 sec. 3). The half fraction is prohibited because it aliases C×P with M×E, C×M with E×P, and C×E with M×P.
- **Auxiliary arms:** A-PLACEBO and A-NONE in S* × P∈{SHARED, INDEP} (4 extra cells); A-ANCHOR (5%); optional A-RETR. They are analysed as planned contrasts, not entered into the factorial model.
- **Battery / calls:** T=400, R=3, n=3, 2 stages ⇒ 115,200 node-calls + 28,800 auxiliary + anchors.
- **Primary family F1 (8 contrasts on Y1 at S2): C, M, E, P, C×M, C×E, M×E, C×P.** Holm at FWER 0.05.
- **F2 central test (IUT):** CT3, CT4, CT5 in S* = cells {07, 08, 15, 16}.
- **F3 diversity equivalence:** TOST on C×M and C×E for φ_err within ±δ_φ (H_SP-4). Absence of an interaction is claimed only here.
- **F4 secondary:** all other metric × contrast combinations, M×P, E×P, 3FI/4FI, per-class results; BH-FDR q=0.05; descriptive.
- **Estimator:** linear probability mixed model `Y1 ~ C*M*E*P + (1 + C + M + E + P | task) + (1 | task:cell:run)`, CR2 task-clustered SEs, frozen fallback order. Logistic GLMM sensitivity. φ_err contrasts via task-cluster bootstrap (10,000 resamples) (G06 sec. 3).
- **Model-dominance analysis (H3, secondary):** |M|/|C| ratio with CIs plus variance decomposition (answers_lane2 Q03).
- **Precision basis:** MESOI 5 pp ⇒ N_eff 20,460 ⇒ T ≥ 214/285/427 at DEFF 1.5/2/3 (R=3). CT3 margin 0.10 ⇒ T ≥ 154 (φ0=0.2, DEFF 2). CT4 margin 0.10 ⇒ ≥ 141 MC tasks (G06 sec. 6). T=400 satisfies F1 at DEFF ≤ 2.8 (computed from the G06 formula T = N_eff·DEFF/(16·R·3)).

### 4.5 Interpretation rules (frozen)
Central test decided only by gate G04-CENTRAL. No result supports claims about lineage, inheritance, provenance or closed-model MODEL independence. Every claim carries `CONDITIONAL_ON{battery, models, versions, MODEL_INDEPENDENCE}`.

## 5. PART B0 protocol (requires a separate AXIOM B0 release)
- **Generator:** 2D+t, parameters G1–G21 (G08 sec. 3), including VESICLE_COUNT, trajectory HMM (Brownian/directed/confined), merge/split (MS arm), occlusion, Gaussian PSF (Airy misspecification arm), background, Poisson shot noise, Gaussian read noise, drift, bleaching, blinking signal decay, and **LIGHT_TOXICITY_PROXY (synthetic degradation only; not biological)**.
- **Ground truth:** TRUE_TRACKS, TRUE_DISAPPEARANCE, TRUE_FALSE_DETECTION_REGIONS, TRUE_SIGNAL_LOSS_WINDOWS, DRIFT_VECTOR, DOSE, GENERATOR_RECEIPT.
- **Grid:** {VESICLE, MIXED} × SNR {1, 2, 4, 7} × density {LOW, MID, HIGH} = 24 core conditions; one-factor-at-a-time stress arms; 2^3 sub-factorial (bleaching × decay × toxicity proxy).
- **Pipelines (fair panel):** P1 LoG+LAP, P2 LoG+Kalman, P3 Spotiflow+LAP, P4 u-track, P5 PDA, P6 particle filter, P7 deep tracker, P8 optical-flow-assisted LAP, P-PH, P-PH-V. Equal DEV tuning budgets; StarDist/Cellpose excluded as vesicle baselines (segmenters; strawman risk) (G10).
- **Metrics:** ISBI α/β/JSC/JSCθ/RMSE, MOTA, IDF1, HOTA (point adaptation flagged as ours), fragmentation, IDSW, plus the sec. 16 Δ-gating set (coverage, ACC|non-abstention, FPR, FNR, HIGH_COST_FP, calibration, abstention rate, risk–coverage/AURC, hold accuracy in loss windows).
- **Order:** **B-MIN first** (VESICLE, SNR {2, 4}, density MID, 20 TEST movies per condition; Δ-PH vs Δ-COST on u-track/LAP at coverage 0.80), then the full B0. TEST is used once; a re-test needs new seeds.
- **Allowed wording:** "In synthetic movies generated under model G (version, hash), Δ …". **Forbidden:** "real vesicles", "biological", "phototoxicity", "in cells".

## 6. PART B1 roadmap (not executed unless data is actually available)
Requirements R1–R11 (G09 sec. 1). Three non-identical phenomena: IMAGE_DEGRADATION ≠ PHOTOBLEACHING ≠ PHOTOTOXICITY. No phototoxicity claim without a biological endpoint (L2-130). Candidate DS-1 (MSP-tracker data) only after verification of its annotation protocol, trajectory count and dose metadata (EO-B4). Frozen transfer from B0; split by cell/sample; domain-shift envelope; annotator-ceiling reporting. Gate G09-B1; the best case is `B1_REAL_DATA_TRACKING_VALIDATION_C1` (a tracking claim, not biology).

## 7. PART C profile (requires a separate AXIOM C release; gate currently HOLD)
- **Levels:** NAC-0 UNBOUND · NAC-1 HASH_LINKED (byte integrity relative to a trusted head only) · NAC-2 SIGNED (key possession over canonical bytes) · NAC-3 TRANSPARENCY_ATTESTED (SCITT Transparent Statement = Signed Statement + COSE Receipt, RFC 9943/9942). **Not a total order of trust. No level implies authorization or scientific validity.** WAL (draft-bondar-wca-00, expired individual I-D) is a crosswalk only (G12).
- **Capsule fields:** ALG, KEY_ID, ISSUER, AUDIENCE, SCOPE, ISSUED_AT, NOT_BEFORE, EXPIRES_AT, NONCE_OR_REPLAY_BIND, PARENT_CAPSULE_HASH (over the parent's full signed bytes), CANONICAL_SERIALIZATION, DOMAIN_SEPARATION, **plus TRUST_ANCHOR_ID, REVOCATION_REF and CLAIM_CEILING/ROOT_PROPERTY** (G11 sec. 2).
- **Decision predicate:** `AUTHORIZED` per G11 sec. 3 (signature ∧ key bound to anchor ∧ ¬revoked ∧ audience ∧ time ∧ fresh ∧ policy ∧ attenuation). UNKNOWN ⇒ deny.
- **Attenuation:** child scope ⊆ parent scope; child exp ≤ parent exp (reject, not clamp); child nbf ≥ parent nbf; issuer = parent audience; claim ceiling ≤ proven root property; depth ≤ MAX_DEPTH.
- **Realisation:** Biscuit or COSE capsule; registration via a SCITT Transparency Service with a NEXUS registration policy; NEXUS acts as the policy decision point called by A2A/MCP authorization hooks. NEXUS does not replace A2A/MCP and builds no new log, receipt or envelope (G13).
- **Tests:** negative fixtures G-C01..G-C11 and integration fixtures G-I01..G-I04 (EO-C1, EO-C2).

## 8. Framework and metaphor rules applied to this preregistration
- Formal text first. No metaphor in gates, enums, predictions, falsifiers or authority fields (G14 sec. 2). The static METAPHOR_LEAK test (G14 sec. 4) must PASS on this document before freeze (PO-F5).
- TERMS registry (JSON twin) with RC_material = 1 and no PINNED_STALE entries before freeze (PO-F3).
- NEVER_COMPRESS list applies (answers_lane3 Q24).

## 9. Pre-freeze checklist (all must be TRUE, else the status stays DRAFT_NOT_FROZEN)
1. Every `UNSET` parameter in sec. 3 is set, and the parameter table is hashed.
2. PO-A1..A9, PO-F2, PO-F3, PO-F5, PO-F6 are discharged (G20).
3. EO-A1..A4 are complete with receipts (G21).
4. Gate G03-A PASS (every T01–T16 threat has a frozen, hashed control).
5. G06-PRECISION PASS at the E1 DEFF.
6. AXIOM source/content adjudication of this GROK return is complete.
7. R10R6 external-non-lineage gate decision is recorded.
8. **AXIOM explicit Part-A execution release is recorded (sec. 38).** Without it, nothing runs.
