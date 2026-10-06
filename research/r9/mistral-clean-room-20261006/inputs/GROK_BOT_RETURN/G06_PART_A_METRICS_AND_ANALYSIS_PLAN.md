# G06 — PART A METRICS AND ANALYSIS PLAN (R10R9, Lane 2)

```text
OBJECT        = R10R9_G06_PART_A_METRICS_AND_ANALYSIS_PLAN_LANE2_20261005_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = DESIGN ONLY · NOT FROZEN · NO DATA · NO EFFECT SIZES ASSUMED FROM DATA
DEPENDS_ON    = G04 (design), G05 (battery), G03 (controls R-01…R-22)
SCRIPTS       = /workspace/r10r9/work/calc/power_calc.py (+_output.txt), power_calc_2.py (+_output.txt)
LAST_VERIFIED = 2026-10-05
```

All margins and thresholds below are `DEFAULT_PENDING_OPERATOR` until frozen in the prereg hash (G03 T12). Nothing here is an empirical estimate.

## 1. Observation structure and notation

- Indices: task t (T tasks), cell c ∈ {01..16} + auxiliary arms, run r (R runs), node i ∈ {1,2,3}, stage s ∈ {S1, S2}.
- Per observation: answer a, confidence q ∈ [0,1] (probability that a is correct), citations, abstention flag.
- `CORRECT(t,c,r,i,s)` = 1 iff a ∈ ACCEPTABLE_ANSWER_SET (G05). On A3 items, UNDERDETERMINED/ABSTAIN is the correct answer. On A0–A2 items, ABSTAIN is a non-answer: it counts against coverage and is excluded from conditional accuracy.
- `ERR` = 1 iff the node answered (not ABSTAIN) and the answer is wrong. This is the primary error indicator. Sensitivity analysis: ABSTAIN counted as error.
- **Primary outcome Y1** = node-level CORRECT at S2. Y1 is also reported at S1.
- Scoring: a deterministic script is primary. A blind human audit covers ≥10% of items, stratified by cell. An LLM judge may be used only as a secondary scorer, from a family outside the subjects, because of self-preference and judge biases (L2-011, L2-012).

## 2. Metric records (§35 metric format)

### M1 — WARRANTED_CONVERGENCE (WC)
| Field | Content |
|---|---|
| DEFINITION | Per (t,c,r) at S2: WC = 1 iff all 3 nodes give the same answer AND that answer ∈ ACCEPTABLE_ANSWER_SET. Companion: UNWARRANTED_CONVERGENCE (UC) = all same and wrong. Reported: WC rate, UC rate, and warrant ratio WR = WC/(WC+UC). |
| DOMAIN | Team-run level; S2 primary, S1 reported. All classes. A3 items converge warrantedly only on UNDERDETERMINED/ABSTAIN. |
| RANGE | WC, UC ∈ [0,1]; WR ∈ [0,1], undefined if no convergence. |
| GROUND_TRUTH | G05 frozen acceptable answer sets. |
| CALIBRATION_METHOD | Compare with the independence baseline: the product of node accuracies, computed from S1 marginals, is the convergence rate expected if nodes erred independently. Report the excess over that baseline. |
| KNOWN_FAILURE_MODE | Rewards easy tasks; can rise by herding when the majority happens to be right; a bad normalization rule makes it collapse or inflate (G03 T10). |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | Agreement on the battery answer key is not truth. It is only correctness relative to a closed synthetic world and a frozen adjudication rule. |

### M2 — JUSTIFIED_DISSENT_RETENTION (JDR)
| Field | Content |
|---|---|
| DEFINITION | Event: at S1, node i's answer differs from the answer shared by the other two nodes (dissent), AND the dissent is justified. Justified means i is correct, OR i cites the item's pre-tagged decisive claim ID. JDR = P(i keeps its S1 answer at S2, or moves to another correct answer \| justified dissent at S1). Counterpart: UNJUSTIFIED_DISSENT_ABANDONMENT (UDA) = P(i moves to a correct answer \| dissent at S1 with i wrong). Both are always reported together. |
| DOMAIN | Node-event level, S1→S2. Defined only when the other two agree at S1. |
| RANGE | [0,1]. Undefined if there are no events (reported as a count). |
| GROUND_TRUTH | Acceptable answer sets plus decisive-claim tags frozen in G05. |
| CALIBRATION_METHOD | Floor: the S2 self-revision rate of the same node class in the A-NONE / K=SELF arms (G04 §4–5). This separates peer pressure from generic instability. |
| KNOWN_FAILURE_MODE | Stubbornness scores high on JDR, so it must be read with UDA. Event counts are small in E=SHARED cells. Citation-based justification can be gamed by citing every claim, so citing more than k claims voids the citation route. |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | It measures persistence under social exposure conditional on our key, not epistemic virtue. |

### M3 — MINORITY_CORRECT_RETENTION (MCR)
| Field | Content |
|---|---|
| DEFINITION | **Designed (primary for CT4):** MINORITY_CORRECT items under E=PART. The event is that the decisive node is correct at S1. MCR_node = P(decisive node is correct at S2 \| event). MCR_team = P(≥2 of 3 nodes correct at S2 \| event). **Emergent (secondary):** any item and cell where exactly 1 of 3 nodes is correct at S1; same two rates. |
| DOMAIN | Designed: E=PART cells only. Emergent: all cells. |
| RANGE | [0,1]. |
| GROUND_TRUTH | G05 decisive-partition assignment and acceptable sets. |
| CALIBRATION_METHOD | Compare with majority-vote aggregation, which gives MCR_team = 0 by construction for 1-of-3, and with the K=SELF arm. |
| KNOWN_FAILURE_MODE | Emergent minorities are selected on the outcome (regression to the mean: a lone correct node is often lucky). Only the designed variant supports a causal contrast. |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | "Correct minority" is defined by our key. Real-world minorities have no oracle. |

### M4 — ERROR_DECORRELATION (φ_err)
| Field | Content |
|---|---|
| DEFINITION | For each node pair (i,j) in a cell, φ_err = Pearson correlation of the indicators ERR_i and ERR_j over (t,r). This is the correlation coefficient among the pairwise diversity measures in Kuncheva & Whitaker (L2-040). The cell value is the mean over the 3 pairs. Companions: excess joint error EJE = P(ERR_i ∧ ERR_j) − P(ERR_i)P(ERR_j); and, for multi-option items, the same-wrong-answer rate P(a_i = a_j \| both wrong). Kim et al. report that models agree on the same wrong answer often (L2-013). Decorrelation is a lower φ_err. |
| DOMAIN | Cell × stage. S1 isolates the C/M/E/P effects on independent errors; S2 adds the communication effect. |
| RANGE | [−1, 1]. The maximum attainable φ is bounded by the marginal error rates, so φ/φ_max is reported as a sensitivity. |
| GROUND_TRUTH | Error indicators from the key. |
| CALIBRATION_METHOD | Task-cluster bootstrap CI (resample tasks; 10,000 resamples; percentile CIs). Absolute levels are reported per cell, not only contrasts. |
| KNOWN_FAILURE_MODE | φ depends on accuracy level: heterogeneous M with weaker models changes the marginals, so M is capability-balanced (G04 §2). Item difficulty induces positive φ even between independent reasoners, because everyone fails the hard items. Report φ within difficulty strata as well. |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | Low error correlation is not independence of training data (MODEL_INDEPENDENCE stays UNKNOWN), and it is not accuracy. Random guessing is decorrelated. |

### M5 — CALIBRATION
| Field | Content |
|---|---|
| DEFINITION | Primary: Brier score of q against CORRECT on non-abstained answers (L2-041, a strictly proper score). Secondary: ECE with 10 equal-width bins, reliability diagrams (L2-022), and the selective risk–coverage curve with its area (AURC), treating confidence as the selection score (L2-033). |
| DOMAIN | Node level, S1 and S2. |
| RANGE | Brier [0,1], lower is better. ECE [0,1]. AURC [0,1]. |
| GROUND_TRUTH | CORRECT. |
| CALIBRATION_METHOD | ECE is bin-dependent, so bins are frozen. Brier is decomposed into reliability and resolution. |
| KNOWN_FAILURE_MODE | Verbalized confidences cluster at round numbers. ECE is biased with few samples per bin. Abstention changes the denominator, so coverage is always reported with it. |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | Calibration measures agreement between stated confidence and the hit rate on this battery. A well-calibrated node can still be wrong often. |

### M6 — REVISION_ACCURACY
| Field | Content |
|---|---|
| DEFINITION | Over S1→S2 answer changes: W→R (wrong or abstain → correct), R→W, R→R′ (correct → other correct), W→W′. Net revision gain NRG = (#W→R − #R→W)/N_nodes. Revision precision RP = #W→R/(#W→R + #R→W). Revision rate = changes/N. |
| DOMAIN | Node level, S1→S2. |
| RANGE | NRG [−1,1]; RP [0,1]; rate [0,1]. |
| GROUND_TRUTH | CORRECT at both stages. |
| CALIBRATION_METHOD | The K=SELF arm (if run) gives the self-revision baseline; NRG(PEER) − NRG(SELF) is the peer-specific gain. Debate literature reports mixed gains (L2-017, L2-018), so no positive gain is presumed. |
| KNOWN_FAILURE_MODE | Ceiling effects: at high S1 accuracy only R→W is possible. |
| WHY_IT_IS_NOT_A_TRUTH_METRIC | It measures the direction of change relative to the key, not the quality of reasoning. |

**Secondary metrics (BH-controlled):** coverage and abstention rate; INJECTION_FOLLOWED (ADVERSARIAL_SOURCE class); citation validity (cited IDs exist in the node's own partition, which also checks for partition leakage); constitution adherence score (manipulation check, G04 CT1).

## 3. Analysis model

**Scale.** The MESOI is stated in percentage points, so interactions are preregistered on the **risk-difference scale**. Interactions on the logit scale and on the probability scale are not equivalent.

**Primary estimator for Y1.** A linear probability mixed model:

`Y1 ~ C*M*E*P + (1 + C + M + E + P | task) + (1 | task:cell:run)`

- The model is saturated in the fixed factors.
- C, M, E and P vary within task, so random slopes by task are justified under the maximal-structure principle (Barr et al., L2-042).
- `task:cell:run` captures team clustering.
- Estimation uses lme4 (L2-043) with cluster-robust (CR2, task-clustered) SEs.

**Fallback order if the model fails to converge (frozen):**
1. drop random-slope correlations;
2. drop random slopes, largest variance last;
3. random intercepts only, plus task-cluster bootstrap CIs.

**Sensitivity analyses:**
- The same model as a logistic GLMM, with average marginal effects obtained by marginal standardization.
- Node slot / model identity entered as a fixed effect within HET.
- Stage as a factor: the S1+S2 stacked model with Stage × factors, giving C×Stage and E×Stage as the COMM interactions (G04 §4).

**Pair-level and event-level metrics:**
- M4 (φ_err): cell × stage estimates. Factorial contrasts are computed on the 16 cell values, and their CIs come from the task-cluster bootstrap. Each resample redraws tasks with all of their cells, runs and nodes, which preserves the crossed structure.
- M2, M3, M6: GLMM on event-level data with a task random intercept, with the bootstrap as sensitivity.

**Contrast coding.** Effect coding is ±½. A main effect is the difference between the means of the two factor halves. A two-factor interaction (2FI) is a difference-in-differences: (Δ at + level) − (Δ at − level) (L2-031).

## 4. Preregistered contrasts

| Family | Contrasts | Outcome | Test type |
|---|---|---|---|
| F1 PRIMARY_FACTORIAL (8) | C, M, E, P, C×M, C×E, M×E, C×P | Y1 (S2) | Two-sided; Holm step-down at FWER 0.05. Planning uses Bonferroni 0.05/8 = 0.00625. |
| F2 CENTRAL_TEST (IUT) | CT3: Δ_C φ_err in S*. CT4: Δ_C JDR and Δ_C MCR (designed) in S*. CT5: Δ_C WC in S* (G04 §7). | M4, M2, M3, M1 | One-sided non-inferiority, each at α=0.025. Intersection–union test: PASS only if every component passes, so no multiplicity adjustment is needed (L2-026 for the equivalence/NI logic). |
| F3 DIVERSITY_EQUIVALENCE | C×M and C×E on φ_err | M4 | TOST equivalence within ±δ_φ at α=0.05 (L2-026). Absence of an interaction is claimed **only** via F3, never from non-significance in F1. |
| F4 SECONDARY | All other metric × contrast combinations, M×P, E×P, 3FI/4FI, auxiliary-arm contrasts, per-class results | M1–M6, secondary | BH FDR q=0.05 (L2-027). Reported as descriptive. |

**Holm procedure (stated procedurally; no citation bound):** order the 8 p-values ascending, p(1) ≤ … ≤ p(8). Reject H(k) while p(k) ≤ 0.05/(8−k+1). Stop at the first non-rejection.

## 5. Interpretation rules (frozen)

- F1 significant C×M or C×E on Y1 → "the effect of a shared constitution on accuracy depends on model / evidence sharing", reported with sign and CI.
- The central test is decided **only** by the G04-CENTRAL gate.
- Per-class results are always descriptive.
- No result supports a claim about lineage, inheritance, provenance or the MODEL independence of closed models (G07 draft).

## 6. Precision / power plan (assumptions, not empirical effect sizes)

**Assumptions (each stated, each with a sensitivity range):**
- A1. Binary outcome, worst-case σ = 0.5 (p = 0.5).
- A2. Design effect DEFF ∈ {1.5, 2, 3} for within-task/within-team clustering. It is unknown and will be estimated in E1.
- A3. α per F1 contrast = 0.05/8 = 0.00625, two-sided; power 0.80; z-sum = 2.734 + 0.842 = 3.576.
- A4. MESOI (smallest interaction of interest) default 5 pp, range 3–10 pp (GAP-L2-05).
- A5. Balanced full 2^4, tasks fully crossed, n = 3 nodes, R runs. N_obs = 16·T·R·n. N_eff = N_obs/DEFF.
- A6. SE(main) = 2σ/√N_eff and SE(2FI) = 4σ/√N_eff. A 2FI has twice the SE of a main effect at the same N (L2-031). A Monte Carlo check of the algebra gave 0.0140 empirical vs 0.0141 analytic.

**Calculation:** required N_eff = (3.576 · 4 · 0.5 / MESOI)².

| MESOI (pp) | N_eff |
|---|---|
| 3 | 56,834 |
| 5 | 20,460 |
| 7.5 | 9,093 |
| 10 | 5,115 |

**Tasks required for F1:** T = ⌈N_eff · DEFF / (16 · R · 3)⌉.

| MESOI | R | DEFF 1.5 | DEFF 2 | DEFF 3 |
|---|---|---|---|---|
| 5 pp | 3 | 214 | 285 | 427 |
| 5 pp | 5 | 128 | 171 | 256 |
| 10 pp | 3 | 54 | 72 | 107 |
| 10 pp | 5 | 32 | 43 | 64 |

**Precision view (95% CI half-width of a 2FI, n=3, R=3):**

| T | DEFF 1.5 | DEFF 2 | DEFF 3 |
|---|---|---|---|
| 60 | 0.052 | 0.060 | 0.073 |
| 120 | 0.037 | 0.042 | 0.052 |
| 200 | 0.028 | 0.033 | 0.040 |
| 300 | 0.023 | 0.027 | 0.033 |
| 500 | 0.018 | 0.021 | 0.025 |

**Central-test components drive N (power_calc_2):**

*CT3 (φ_err non-inferiority, Fisher-z approximation, one-sided 0.025, power 0.80).*
- Effective pair-observations needed per arm, m:

| φ0 | margin 0.10 | margin 0.05 |
|---|---|---|
| 0.2 | 1,380 | 5,659 |
| 0.4 | 997 | 4,215 |

- Pair-observations per C arm in S* = T · R · 3 pairs · 2 cells.
- Margin 0.10 → T ≥ 154 (φ0 = 0.2, DEFF 2, R = 3).
- Margin 0.05 → T ≥ 469–629 at R = 3, or 281–378 at R = 5.
- Caveat: the approximation treats pair-observations as independent after DEFF and ignores the dependence between the 3 pairs of one team. That dependence is absorbed into DEFF (an assumption).

*CT4 (designed MCR non-inferiority, margin 0.10, p = 0.5 worst case, P(decisive node correct at S1) = 0.7, DEFF 1.5).*
- Requires ≥ 392 effective events per arm, which is ≥ 141 MINORITY_CORRECT tasks.
- With only 43 MC tasks, the CI half-width ≈ 0.126, so CT4 would be structurally INCONCLUSIVE.
- Margin 0.15 → ≥ 63 tasks.

**Recommended default:**
- **T = 400 adjudicable tasks** (6 classes × 43 + 142 MINORITY_CORRECT), n = 3, R = 3, 16 cells, 2 stages.
- That is 400 × 16 × 3 × 3 × 2 = 115,200 node-calls.
- Plus auxiliary arms: 4 cells × 400 × 3 × 3 × 2 = 28,800.
- Plus anchors (5%) and the E1 pilot on a disjoint item set.

**Minimum viable:** MESOI 10 pp and δ_mc 0.15 give T ≈ 72–107 with ≥ 63 MC items. This detects only large interactions.

**Interpretation of a null:** a CI that straddles a margin is reported as INCONCLUSIVE_PRECISION, never as "no effect".

## 7. Stopping rule

- Fixed N, with no interim looks at outcome data and no optional stopping or extension (G03 T13).
- One blind infrastructure checkpoint after about 5% of calls. It checks parse rate, missingness, canary violations and partition-leak checks only, with outcome columns hashed and hidden.
- If budget runs out early, analyze what was collected with the flag `INCOMPLETE_FIXED_N`. All precision-dependent conclusions are downgraded to INCONCLUSIVE. Collecting more data requires a new preregistration and a new study ID.

## 8. Run failures and retries

- API error or timeout: up to 2 retries with the identical request (same seed if supported), logged. After that the observation is MISSING (→ §10).
- Schema-invalid output: 1 frozen re-ask containing the schema reminder only. If it is still invalid, it is scored WRONG_NON_ABSTAIN. This is *not* missing, because format failure is part of the behavior.
- Canary or memory violation (G03 T07): the run is invalidated and re-run once with a fresh session. Repeated violation leads to a cell-level flag.

## 9. Randomization and blinding

- All randomizations listed in G04 §5 use frozen seeds published in the receipt.
- Human adjudicators and auditors are blind to cell. Outputs are stripped of constitution text and model self-identification (G03 T09).
- The analyst runs frozen code on a cell-masked data file. Masks are lifted only after the analysis code hash is logged.

## 10. Missing data and exclusions

- Missing ≠ wrong.
- **Primary analysis:** observed data with the mixed model, assuming MAR conditional on task and cell.
- **Sensitivity:** worst case (missing = wrong) and best case (missing = correct) bounds on all F1/F2 contrasts.
- **Thresholds:** missingness > 10% in any cell → `CELL_FLAG`. Missingness that differs by C arm by more than 5 pp → central test UNKNOWN.
- **Exclusions:** only those pre-declared in G05 `EXCLUSION_RULE` (pre-E2 item exclusions; infrastructure failures). Outcome-dependent exclusion is forbidden.

## 11. Version freeze (hashes required before the first E2 call)

- **Content:** constitution texts (C+, C−, placebo); paraphrase pool; task battery JSON; partition maps; decisive-claim tags.
- **Code:** normalization code; scoring code; analysis code (this plan as code); orchestrator code.
- **Models:** model IDs and provider fingerprints; decoding parameters; judge specification.
- **Parameters:** margins (δ_φ, δ_d, δ_mc, δ_wc); MESOI; seeds; E1 receipt hash.
- **Rule:** an append-only amendment log, where any change creates a new hash (PR #45 M02, L2-002).

## 12. Reproducibility receipt (template fields)

```json
{
  "STUDY_ID": "<R10R6-E2-...>",
  "PREREG_HASH": "<sha256>",
  "FROZEN_ARTIFACTS": [{"FILE":"<name>","SHA256":"<hex>","SIZE_BYTES":0,"DATE":"<ISO8601+offset>"}],
  "SEEDS": {"task_order":0,"cell_block":0,"node_slot":0,"hom_family":0,"paraphrase":0,"constitution_variant":0,"partition":0,"option_order":0},
  "MODELS": [{"SLOT":"HET-a","MODEL_ID":"<exact>","FINGERPRINT":"<as returned>","DECODING":{},"MODEL_INDEPENDENCE":"UNKNOWN"}],
  "RUN_WINDOW": {"START":"<ISO8601+offset>","END":"<ISO8601+offset>"},
  "CALL_COUNTS": {"planned":0,"completed":0,"missing":0,"invalidated":0},
  "ANALYSIS_CODE_HASH": "<sha256>",
  "VALIDATOR_IDENTITY": "<who verified hashes>",
  "CLAIM_CEILING": "C1_DESCRIPTIVE_ONLY"
}
```

The receipt must satisfy the repo's RECEIPT_COMPLETENESS_RULE (L2-004).

## 13. Gate: G06-PRECISION (§35 gate format)

| Field | Content |
|---|---|
| INPUT | Frozen MESOI and margins; E1-estimated DEFF and S1 accuracy; planned T, R. |
| PREDICATE | The planned T satisfies all three requirements in §6 at the E1-estimated DEFF (upper bound of its 80% CI). |
| PASS | E2 may be scheduled. |
| FAIL | Reduce scope: drop P (the PR #45 M01 falsifier), widen margins with operator sign-off, or increase R. Fractionation is never allowed. |
| UNKNOWN | E1 not run, so DEFF is unknown. Use DEFF = 3 (conservative), which gives T = 427 for F1 at 5 pp. |
| RECOVERY | Re-plan before freeze. No post hoc changes. |
| FALSE_POSITIVE_RISK | DEFF underestimated → CIs too narrow. Mitigated by the task-cluster bootstrap. |
| FALSE_NEGATIVE_RISK | The worst-case σ overstates N when accuracies are far from 0.5. This is acceptable, because it errs toward precision. |
