# G03 — PART A PREREGISTRATION ATTACK (R10R9, Lane 2)

```text
OBJECT        = R10R9_G03_PART_A_PREREG_ATTACK_LANE2_20261005_R0
EXECUTOR      = GROK-BOT (external non-lineage reviewer; NOT AXIOM, NOT CURSOR_PRAXIS)
TARGET        = E2 design of record = PR #45 M01–M12 (head 73b8596a…) + ORDER §5–§11
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
MODE          = DESIGN ATTACK ONLY · NO EXECUTION · NO LLM CALLED AS SUBJECT · R10R6 E2 NOT EXECUTED
LAST_VERIFIED = 2026-10-05
```

Source IDs `L2-xxx` refer to `/workspace/r10r9/out/G01_part_lane2.csv`. Repo context and gaps: `/workspace/r10r9/work/REPO_CONTEXT_lane2.md`.

## 0. Attack posture and bottom line

The study is attacked as if the reviewer wanted to reject it. The question is not "is Soft-Lineage plausible?" but "if this study returned PASS, what would that PASS actually license?"

**Bottom line (major claim, §35 format)**

| Field | Content |
|---|---|
| OBSERVATION | PR #45 repairs the old triple confound (C×M×E in one arm) with a full 2^4 factorial (L2-002). But (i) the manipulation of C is undefined at the "NO" level, (ii) C is delivered through the same channel as P (prompt text), (iii) M uses closed models whose training overlap is UNKNOWN, (iv) only C×M and C×E are preregistered, (v) retention/revision metrics need an interaction stage that the design does not specify, (vi) MESOI, model list, evaluator and thresholds are still UNSET. |
| SOURCE | L2-002, L2-003 (repo); L2-010 (AI-agent researcher degrees of freedom), L2-013 (correlated LLM errors), L2-016 (prompt-format sensitivity), L2-011/L2-012 (judge bias), L2-015 (model drift), L2-031 (interaction power). |
| SOURCE_CLASS | VENDOR_OR_PROJECT_DOC (repo); PREPRINT / PEER_REVIEWED conference (externals, see ledger). |
| INTERPRETATION | In its current form a PASS would be compatible with at least four non-Soft-Lineage explanations: shared-prefix prompt effect, model-family monoculture masking (or producing) the effect, judge/normalization artifacts, and post-hoc threshold choice. The design is **repairable**, but only if the controls in §2 are added and frozen. |
| ALTERNATIVE | The design is already adequate and the residual threats are second-order. Rejected: threats T02, T03, T06, T09, T10, T14 each can generate a spurious PASS of the central test by themselves. |
| UNCERTAINTY | Magnitude of each bias in this specific setup is unknown (no pilot data, by design). |
| FALSIFIER | A pre-specified pilot (E1-style, synthetic, no Soft-Lineage hypothesis test) showing that placebo-constitution, judge-swap and paraphrase controls produce effects < the frozen non-inferiority margins would demote these threats from "PASS-invalidating" to "reportable". |
| IMPACT_ON_R10R9 | Part A cannot be released as-is. Required: controls R-01…R-22 below + G04/G05/G06 + reduced framing (G07 draft). |

## 1. Threat-by-threat attack (all 16 threats in ORDER §10)

Severity: **S1** = can by itself produce a spurious PASS or FAIL of the central test; **S2** = biases estimates materially; **S3** = reduces precision/generalizability.

### T01 — TASK SELECTION BIAS (S1)
- **Mechanism:** Tasks chosen (consciously or not) where a shared constitution helps (e.g., tasks rewarding "cite evidence, hedge") or where heterogeneity trivially decorrelates errors. Selecting tasks after piloting with the candidate models = outcome-contingent selection (catalogued as a researcher degree of freedom in L2-010).
- **Breaks:** External meaning of any C effect; the central test can be passed by battery construction.
- **Required controls:** R-01 task generation from **templates frozen before any model contact** (G05); R-02 stratified **random sampling** of instances from each template pool (seeded, seed published in the receipt); R-03 **no model-in-the-loop filtering** of tasks except a pre-declared "solvability by a human adjudicator" screen; R-04 ≥ 7 task classes with fixed quotas (G05 `battery_composition`); R-05 report per-class effects, not only pooled.
- **Residual:** Template authors share the operator's priors. Mitigation: at least one template family authored by a party outside the NEXUS lineage (MA-L2-06).

### T02 — SOURCE LEAKAGE (S1)
- **Mechanism:** In E=PARTITIONED, the "private" evidence of node A leaks to node B via (a) overlapping documents, (b) documents that quote each other, (c) parametric knowledge (the answer is in pretraining data), (d) shared retrieval cache.
- **Breaks:** E factor; D_EPISTEMIC is no longer low in "low" cells → central test predicate (EPISTEMIC_DEPENDENCE_LOW) is false while assumed true.
- **Required controls:** R-06 **closed-world evidence**: every task's evidence packet is a finite set of document IDs; partitions are disjoint at document **and** claim level (claim-level dedup by normalized claim hash, G05 `SOURCE_PARTITION_PLAN`); R-07 **no web access** for subjects; R-08 **parametric-knowledge control**: a "no-evidence" probe of each task per model family (answer without evidence) run in E1, tasks answerable from parametric memory above a pre-set rate are tagged `PARAMETRIC_LEAK` and excluded from E-effect analysis (they stay in a separate stratum); R-09 per-run logging of retrieved document IDs → measured source overlap (Jaccard) as manipulation check.
- **Residual:** Parametric knowledge overlap across closed models is UNKNOWN (L2-013 reports substantial error correlation across >350 LLMs, including across providers). Counterfactual/synthetic-fact tasks (G05 class `TC1` variant `SYNTHETIC_WORLD`) reduce but do not remove it.

### T03 — PROMPT LEAKAGE / C–P CHANNEL CONFOUND (S1)
- **Mechanism:** The constitution is delivered as text in the system prompt. C=SHARED therefore also means "shared prompt prefix of N tokens". Prompt formatting alone can swing accuracy strongly and inconsistently across models (L2-016 reports up to 76 accuracy points on one open model from formatting changes, and only weak correlation of format effects between models).
- **Breaks:** Identifiability of C vs P; Q02 ("constitution = shared prompt effect") cannot be answered.
- **Required controls:** R-10 define **C− = node-specific constitutions** (independently authored, same length ±5%, same section structure, same procedural coverage checklist) rather than "no constitution" (MA-L2-01); R-11 **placebo arm** `C_PLACEBO` = shared, length-matched, non-normative text (no truth-discipline content), run at minimum in the low-D_EPISTEMIC stratum (G04 §4); R-12 **position/format freeze**: constitution always occupies the same slot, same delimiter scheme, in all arms; R-13 P−(independent prompts) = meaning-preserving paraphrases from a frozen paraphrase pool, validated by human equivalence check, assigned at random per node.
- **Residual:** Even with matched length, shared wording may act as a cross-model "anchor". This is precisely what the placebo arm measures.

### T04 — MODEL CONTAMINATION (S2)
- **Mechanism:** Benchmark-derived tasks may be in pretraining data (L2-014 survey); contamination differs by model, so it is confounded with M.
- **Required controls:** R-14 ≥ 50% of tasks from `SYNTHETIC_WORLD` or post-cutoff `TIME_BIND` items (G05); R-15 no public benchmark items verbatim; R-16 contamination probe (verbatim-continuation / no-evidence probe) in E1, results frozen before E2.
- **Residual:** Closed-model cutoffs are self-declared; treat as UNKNOWN when undocumented.

### T05 — SHARED RETRIEVAL BACKEND (S1 in E=PARTITIONED)
- **Mechanism:** One retriever/embedding model/index for all nodes = a shared METHOD (D_EPISTEMIC component) and possibly shared cache → hidden correlation.
- **Required controls:** R-17 **per-node index instances** built only from that node's partition; cache disabled or per-node; R-18 retriever identity logged as `D_METHOD.retriever_id`; R-19 sensitivity arm (subset): heterogeneous retrievers (e.g., lexical BM25-type vs embedding) to bound the retriever contribution; R-07 (no web) applies. Detail in `answers_lane2.md` Q05.
- **Residual:** If all nodes use the same retriever, the study can at most claim "low SOURCE/DATA dependence, shared METHOD dependence" — must be reported exactly so.

### T06 — SHARED SYSTEM PROMPT (S1)
- **Mechanism:** Beyond the constitution, operational system-prompt boilerplate (tool instructions, output schema) is shared in all arms.
- **Required controls:** R-20 classify every system-prompt segment as `CONSTITUTION`, `OUTPUT_SCHEMA`, `TOOLING`, `TASK`; only `CONSTITUTION` varies with C, only `TASK` wording varies with P; `OUTPUT_SCHEMA` and `TOOLING` are held identical in **all** cells and declared as a fixed shared D_CONTROL component (so the comparison is "constitution sharing on top of an always-shared schema").
- **Residual:** Shared output schema can itself homogenize answers; reported as a constant, not a factor.

### T07 — SHARED MEMORY (S1 if present)
- **Mechanism:** Persistent memory/caches across tasks or runs, or provider-side conversation memory, carry answers across cells.
- **Required controls:** R-21 stateless calls; fresh session per (node, task, run); provider memory features off; no cross-task context; verify by canary items (a unique token planted in run k must not appear in run k+1 outputs).
- **Residual:** Provider-side undisclosed caching: UNKNOWN; canaries bound but cannot exclude.

### T08 — COMMUNICATION LEAK (S1 for COMM=OFF cells)
- **Mechanism:** Orchestrator passes peer outputs into context inadvertently (shared scratchpad, aggregated logs).
- **Required controls:** network/process isolation per node in Stage 1; orchestrator code reviewed and hashed; message-log audit: in COMM-OFF stage, the number of peer-derived tokens in any context must be exactly 0 (automated check).

### T09 — ANSWER NORMALIZATION ARTIFACTS (S1 for convergence/decorrelation metrics)
- **Mechanism:** Normalizing free-text answers into canonical labels can manufacture agreement (collapsing distinct answers) or disagreement (failing to merge equivalents). Different models' verbosity interacts with normalization → confounded with M.
- **Required controls:** structured answer schema (closed answer set or numeric with unit) for all accuracy-analysed tasks; **normalization rules frozen** and unit-tested on a held-out fixture set before E2; normalization run blind to cell; report % of answers needing non-trivial normalization per cell; sensitivity analysis with strict (exact) vs lenient normalization.

### T10 — JUDGE MODEL BIAS (S1 if an LLM judge scores primary outcomes)
- **Mechanism:** LLM judges show self-preference linked to self-recognition (L2-011) and position/verbosity biases (L2-012); correlated errors across LLMs extend to LLM-as-judge (L2-013).
- **Required controls:** primary outcomes scored **deterministically** against ground truth or by a **frozen adjudication rule**; justification-quality scores (needed for JUSTIFIED_DISSENT_RETENTION) by ≥ 2 human raters blind to cell and model, with inter-rater agreement reported (Cohen's κ or Krippendorff's α; threshold frozen); an LLM judge may be used only as a secondary scorer, from a model family not used as a subject, with order randomization and identity stripping; judge-swap sensitivity analysis.
- **Residual:** Closed judge family overlap with subjects = UNKNOWN; therefore never primary.

### T11 — POST-HOC THRESHOLDS (S1)
- **Mechanism:** Choosing "low dependence" or non-inferiority margins after seeing data.
- **Required controls:** all margins (δ_φ for error correlation, δ_d for dissent retention, δ_mc for minority-correct) and all THETA values frozen in the prereg hash **before** the first E2 call; E1 calibration must be completed and its own receipt frozen first (PR #45 M05). Default margins proposed in G06 are flagged `DEFAULT_PENDING_OPERATOR`.

### T12 — OPTIONAL STOPPING (S2)
- **Mechanism:** Running more tasks until the central test passes.
- **Required controls:** fixed N (tasks × runs) frozen; no interim efficacy looks; one pre-declared **futility/integrity** look only (data-quality: parse-failure rate, API error rate) that cannot stop for efficacy; if sequential designs are wanted, alpha-spending must be preregistered (not recommended here).

### T13 — MULTIPLE COMPARISONS (S2)
- **Mechanism:** 4 main effects + 6 2FIs + higher-order × 6 metrics × 7 task classes → hundreds of tests.
- **Required controls:** a **primary family** of exactly 8 contrasts (C, M, E, P, C×M, C×E, M×E, C×P on the primary outcome) with family-wise control (Bonferroni α=0.05/8 used for planning; Holm allowed at analysis); the central test is a single pre-declared **intersection-union** test (all components must pass, so no α inflation across its components); secondary metrics with Benjamini–Hochberg FDR q=0.05 (L2-027); per-class results descriptive only.

### T14 — UNDERPOWERED INTERACTIONS (S1 for H2D)
- **Mechanism:** Interaction contrasts (difference-in-differences) have twice the SE of main effects in a balanced 2×2 coding; an interaction half the size of a main effect needs ~16× the sample (L2-031). An underpowered interaction test that is "not significant" is then misread as "constitution does not collapse diversity".
- **Required controls:** precision plan for interactions explicitly (G06 §6: e.g., 5 pp MESOI ⇒ ≈ 20,460 effective binary observations; ≈ 214–427 tasks at n=3 nodes, R=3 runs depending on design effect); **absence of a C×M or C×E interaction may only be claimed via an equivalence/non-inferiority test** (L2-026), never via non-significance.

### T15 — FAILED BLINDING (S2)
- **Mechanism:** Adjudicators/analysts can infer the cell (e.g., constitution boilerplate visible in outputs; model style recognizable).
- **Required controls:** strip constitution-echo phrases via a frozen redaction list before human scoring; cell labels replaced by random codes; analysis code written and frozen on **synthetic shuffled-label data** before unblinding; a **blinding check**: raters guess cell; if guess accuracy > chance + frozen margin, report as FAILED_BLINDING and down-weight justification-based metrics.

### T16 — MODEL UPDATE DRIFT (S1 across time)
- **Mechanism:** Hosted "same name" models change behaviour over months (L2-015 documents large March→June 2023 shifts in GPT-3.5/GPT-4). If cells are run at different times, drift is confounded with factors.
- **Required controls:** pinned version identifiers where providers allow; record provider-returned model fingerprints/versions per call; **randomized, interleaved run order across all 16 cells within short blocks**; whole design completed within a frozen time window; re-run a fixed **anchor set** (e.g., 5% of tasks) at start, middle and end — drift > frozen tolerance ⇒ affected blocks flagged; open-weight models run locally with weight hashes recorded (makes MODEL_INDEPENDENCE at least BOUNDED for those).

## 2. Required controls checklist (ORDER §10 "REQUIRE")

| Req | Specification (frozen in prereg) | Where specified |
|---|---|---|
| RANDOMIZATION | Seeded randomization of: task→order, cell→time block (interleaved), paraphrase→node (P−), constitution variant→node (C−), partition→node (E=PART), answer-option order. Seeds published. | G04 §5, G06 §9 |
| BLINDING WHERE POSSIBLE | Subjects blind to hypothesis (no mention of study aims in prompts); adjudicators blind to cell/model; analysts blind until analysis code frozen. Subjects cannot be "blind" to their own constitution (inherent). | T15 |
| PREDECLARED EXCLUSIONS | Task-level: no defensible adjudication → excluded from accuracy analysis (ORDER §7); `PARAMETRIC_LEAK`; partition-integrity failure. Run-level: API error, parse failure after 1 frozen retry, canary violation. Never exclude on outcome. | G05 `EXCLUSION_RULE`, G06 §10 |
| PREDECLARED METRICS | 6 metric families with full §35 metric records. | G06 §2 |
| REPEATED RUNS | R ≥ 3 per (task, cell) at frozen non-zero temperature, plus R=1 at temperature 0 where supported as a determinism probe. | G04 §5 |
| POWER_OR_PRECISION_PLAN | Analytic calculation + sensitivity table, script hashed. | G06 §6 |
| MISSING-DATA RULE | Missing ≠ wrong. Primary analysis on observed with missingness modelled; sensitivity: worst-case (missing=wrong) and best-case bounds; cell-level missingness > 10% ⇒ cell flagged. | G06 §10 |
| STOPPING RULE | Fixed N; no efficacy interim; integrity stop only (e.g., >20% calls failing in a block). | T12 |
| MULTIPLE-COMPARISON RULE | Primary family of 8 (FWER), central test IUT, secondary BH-FDR. | T13 |
| VERSION FREEZE | Hashes of: constitutions, paraphrase pool, task battery, partitions, normalization code, scoring code, analysis code, orchestrator code, model IDs/fingerprints, decoding params, judge spec. | G06 §11 |
| REPRODUCIBILITY RECEIPT | Receipt JSON with all hashes + seeds + run timestamps + provider fingerprints; satisfies the repo's RECEIPT_COMPLETENESS_RULE (file name, SHA-256, size, date, validator identity) (L2-004). | G06 §12 |

## 3. Gates introduced by this attack (§35 gate format)

### GATE G03-A — PRE-FREEZE CONTROL COMPLETENESS
| Field | Content |
|---|---|
| INPUT | Prereg package draft (PR #45 M12 package + G04/G05/G06 additions). |
| PREDICATE | Every threat T01–T16 has ≥1 frozen control with a named artifact hash, and controls R-06, R-10, R-11, R-17, R-21 (the S1 controls for leakage/C–P confound/backend/memory) are present. |
| PASS | All present → package eligible for external pre-execution review. |
| FAIL | Any S1 control missing → `HOLD_C1_CAUSAL_IDENTIFIABILITY`. |
| UNKNOWN | Control declared but artifact not hashed → treated as FAIL (fail-closed, consistent with repo rule BYTE_BOUND_OR_REJECTED). |
| RECOVERY | Add artifact, re-hash, resubmit. |
| FALSE_POSITIVE_RISK | Controls exist on paper but are not executed → mitigated by run-time audits (canaries, zero-peer-token check, retrieval-log overlap). |
| FALSE_NEGATIVE_RISK | Over-strict: a control irrelevant to a sub-design (e.g., COMM controls when COMM omitted) blocks release → allow `NOT_APPLICABLE` with written justification. |

### GATE G03-B — MANIPULATION-CHECK GATE (run-time, before outcome unblinding)
| Field | Content |
|---|---|
| INPUT | Run logs (retrieved doc IDs, context token provenance, canary hits), constitution adherence checklist scores. |
| PREDICATE | (a) measured source-overlap Jaccard in E=PART cells ≤ frozen ceiling (default 0.0 at document level); (b) zero peer tokens in COMM-OFF stage; (c) zero canary carry-over; (d) constitution adherence in C+ ≥ frozen floor and distinguishable from C_PLACEBO. |
| PASS | Proceed to outcome analysis. |
| FAIL | Any of (a)–(c) fails ⇒ affected cells excluded and reported; (d) fails ⇒ C manipulation ineffective ⇒ central test reported as `NOT_TESTED`, not as PASS. |
| UNKNOWN | Logs missing ⇒ FAIL for that cell. |
| RECOVERY | Re-run affected cells in a new frozen block (amendment, append-only). |
| FALSE_POSITIVE_RISK | Adherence checklist rewards surface phrases → use behavioural adherence items (e.g., evidence citation present, uncertainty statement present) scored blind. |
| FALSE_NEGATIVE_RISK | Floor set too high for weaker models → floor frozen per model family from E1. |

## 4. What a PASS would mean after these repairs (and what it would not)

- **Would mean (C1, descriptive):** "Under the frozen battery, models, prompts and decoding settings, sharing a length-matched procedural constitution across nodes did not increase cross-node error correlation by more than δ_φ, and did not reduce justified-dissent retention by more than δ_d, relative to node-specific constitutions, in cells with partitioned evidence and nominally heterogeneous models; and the effect differed from (or did not differ from) a shared placebo text by …"
- **Would NOT mean:** that nodes are epistemically independent (closed-model training overlap UNKNOWN); that Soft-Lineage is validated; that the result transfers to other models/versions/tasks; that "lineage" (derivation, inheritance across generations, memory) has any effect — none of those are manipulated (see G07 draft: REDUCE).
