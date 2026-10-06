# G07 — EXTERNAL NON-LINEAGE GATE VERDICT (R10R9, final synthesis)

```text
OBJECT        = R10R9_G07_EXTERNAL_NON_LINEAGE_GATE_VERDICT_SYNTHESIS_20261005_R0
REVIEWER      = GROK-BOT external non-lineage reviewer (synthesis step over lanes 1-3)
NOT           = AXIOM · CURSOR_PRAXIS · NODE_ACTIVATION_AUTHORITY · CLAIM_PROMOTION_AUTHORITY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
INPUTS        = work/G07_draft_lane2.md; G03, G04, G05, G06 (lane 2); G08, G09, G10 (lane 2);
                G11, G12, G13 (lane 1); G19 (lane 3); work/REPO_CONTEXT_lane{1,2,3}.md
EXECUTION     = none. R10R6 E2 NOT executed. This verdict does NOT release execution (ORDER sec. 38).
LAST_VERIFIED = 2026-10-05 (Europe/Berlin)
```

## 0. Verdicts at a glance

| Gate | Verdict | Fallback / condition | Releases execution? |
|---|---|---|---|
| **PART A — external non-lineage gate (ORDER sec. 11)** | **`REDUCE_TO_STANDARD_POLICY_CONFIGURATION_TEST`** | If the operator keeps the lineage framing without adding a manipulated lineage factor: `HOLD_C1_CAUSAL_IDENTIFIABILITY`. The reduced test itself is prereg-*repairable*, not prereg-*ready*. Once the blocking items in sec. 4 close, it qualifies for `PASS_WITH_CAVEATS_C1_PREREG_REPAIRABLE` **as a policy-configuration test**. | No. AXIOM release is required (sec. 38). |
| PART A — sec. 9 central-test operationalizability | `OPERATIONALIZABLE_CONDITIONAL` (G04 sec. 7) | It becomes `HOLD_C1_E2_CAUSAL_IDENTIFIABILITY_UNRESOLVED` if AXIOM requires MODEL dependence to be KNOWN-low while using closed models (MA-L2-02). | — |
| **PART B0 — synthetic POC gate (G08-B0)** | **`DESIGN_READY_PENDING_FREEZE`**. The outcome is UNKNOWN because nothing was generated or run. | Needs a frozen generator hash, margins, the Δ definition (A-Δ1..3 adopted as assumptions) and DEV/TEST seeds. PH is **DEMOTED** to an optional arm (H-B0-2). | No. A separate AXIOM B0 release is required. |
| PART B1 — real-data gate (G09-B1) | `HOLD_C1_R10R9_PART_B_REAL_DATA_REQUIREMENT` (requirements only; `NOT_EXECUTED`) | Candidate dataset DS-1 (MSP-tracker data, L2-131) is verified to exist, but its annotation protocol, trajectory count and dose metadata are unverified. | No. |
| **PART C — authority capsule gate (G11)** | **`HOLD_C1_R10R9_AUTHORITY_TRUST_MODEL_UNRESOLVED`**, together with the design recommendation `REDUCE_C1_PART_C_TO_PROFILE` (Biscuit-or-COSE capsule + SCITT registration + NEXUS claim-ceiling field) | No trust anchor, revocation source or decidable scope grammar is defined. The repo states `cryptographic_authority = NOT_ESTABLISHED` (L1-053). | No. A separate AXIOM C release is required, after PO-C1..C5 (G20). |

## 1. PART A verdict reasoning (sec. 35 major-claim format)

| Field | Content |
|---|---|
| OBSERVATION | (a) The E2 design of record is PR #45 M01–M12 (head 73b8596a; open, unmerged; L2-002, L1-054). It manipulates C (shared vs non-shared constitution text), M, E and P. **None of these levels manipulates a lineage mechanism**: no inheritance from a parent configuration, no derivation history, no persistent memory, no shared developmental trajectory (G07 draft lane 2 sec. 1). (b) Operationally, "shared constitution" means the same policy text in the system-prompt slot. There is no enforcement channel outside the prompt (G15 MP-08; G19 sec. 2), so C is a *segment of* the prompt and therefore part of D_CONTROL.PROMPT in the broad sense (lane 3, "C ⊂ P"). (c) PR #45 has several design gaps: it preregisters only C×M and C×E (M×E and C×P are missing); it has no placebo arm; C=NO is undefined (MA-L2-01); M03 ("D_EPISTEMIC held constant low") contradicts manipulating M and E (MA-L2-03); and it requires resolution ≥ V for any fraction, which no 2^(4−1) design can meet. The only half fraction (I=CMEP) aliases C×P with M×E (work/calc/alias_output.txt; G04 sec. 3). (d) Operator inputs are unset: model list, MESOI, margins, evaluator lock and E1 calibration (GAP-L2-05/06). (e) The term "Soft-Lineage" is not defined anywhere in the order (U04, MA-L3-03). |
| SOURCE | L2-002, L2-003, L1-054 (repo, PR #45); G03 T01–T16; G04 sec. 3, 7, 8; G06 sec. 6; G15 MP-04, MP-08; G18 sec. 4.2 (U04); G19 sec. 2; work/calc/alias.py. |
| SOURCE_CLASS | VENDOR_OR_PROJECT_DOC / IMPLEMENTATION_REPO (lineage-internal repo); SECONDARY_ANALYSIS (local alias and power computations); PEER_REVIEWED / PREPRINT for threat evidence (L2-013 correlated LLM errors; L2-016 prompt-format sensitivity; L2-011/L2-012 judge bias; L2-015 model drift). |
| INTERPRETATION | Even after repair, a PASS can license only this: *"In this closed-world battery, giving several nominally heterogeneous LLM calls with disjoint evidence the same policy text did not increase error correlation and did not suppress justified dissent beyond margin δ, relative to node-specific texts, and the effect did / did not differ from a shared placebo text."* That is a statement about a **shared policy-text configuration**. It is not a statement about lineage. Calling it a Soft-Lineage validation would mislabel it, which is the sec. 11 FAIL-type risk. **Reducing the label keeps the scientific value and removes the over-claim. Per sec. 11, a reduction result is scientific success.** |
| ALTERNATIVE | (A1) AXIOM defines Soft-Lineage operationally as exactly "shared constitution text, separate epistemics" (the lane 3 reconstruction H_SP, MA-L3-03). The reduced test then **is** the Soft-Lineage test under that definition, and the label becomes `PASS_WITH_CAVEATS_C1_PREREG_REPAIRABLE` once sec. 4 closes. (A2) AXIOM wants a lineage mechanism (inheritance, memory, derivation). A factor L with levels must then be designed, which gives `HOLD_C1_CAUSAL_IDENTIFIABILITY`. (A3) `FAIL_C1_SOFT_LINEAGE_TEST_NOT_MEASURING_SOFT_LINEAGE` is defensible but harsher than needed, because the design does measure a well-defined quantity. |
| UNCERTAINTY | The intended semantics of "Soft-Lineage" in the unavailable E0 D-vector DOCX (GAP-L2-03). MODEL independence is UNKNOWN for any closed model (sec. 8; G04 sec. 6). Effect sizes are unknown (no pilot, by design). |
| FALSIFIER | A hash-bound AXIOM/repo document that defines Soft-Lineage as precisely the C manipulation, with no inheritance or memory component, moves the verdict to A1. A document that defines a manipulable lineage factor with levels moves it to HOLD (A2) until that factor is in the design. |
| IMPACT_ON_R10R9 | G23 adopts the reduced label "H_SP shared-policy-text configuration test". It integrates all lane 2 repairs (full 2^4, placebo and no-constitution arms, C−=NODE_SPECIFIC, 2-stage protocol, capability-balanced M). It keeps A-MIN as the first experiment and leaves every unset operator input as an explicit parameter. |

### 1.1 Reconciliation of the lane 2 vs lane 3 positions on C vs P
- Lane 3 (G19 sec. 2) argues that C ⊂ P, so "C×P is not separable" and Q02's answer is "all of them" unless C uses a non-prompt channel.
- Lane 2 (G03 T03/T06, G04 sec. 2) separates the prompt into frozen segments: `CONSTITUTION` (varied by C), `TASK` wording (varied by P), and `OUTPUT_SCHEMA`/`TOOLING` (fixed). It adds a length-matched shared placebo text (A-PLACEBO).
- **Synthesis:** both are correct at different levels. As *factorial contrasts*, C and P are separately estimable, and C×P is estimable without aliasing in the full 2^4, because they vary different, frozen prompt segments. As a *mechanism*, C is a prompt intervention, so no outcome can show a non-prompt "constitutional" effect. The placebo contrast (CT6) separates "content of the shared policy text" from "sharing any prefix". It cannot separate "constitution" from "prompt". That is exactly why the label is reduced and the design is not abandoned.

## 2. Gate record G07-PART-A (sec. 35 gate format)

| Field | Content |
|---|---|
| INPUT | PR #45 (head 73b8596a) M01–M12; G03 (threats and controls R-01…R-22); G04 (factorial V2); G05 (battery spec); G06 (metrics and analysis); the G23 parameter table. |
| PREDICATE | P1: every manipulated factor maps to a named lineage mechanism. P2: all mandatory effects (C, M, E, P; C×M, C×E, M×E, C×P) are estimable without aliasing. P3: the sec. 9 central test is operationalized (CT1–CT5). P4: every frozen-before-E2 input is present and hashed (model list, MESOI, margins, evaluator lock, E1 receipt, battery, constitution/placebo/paraphrase texts). |
| PASS | P1 ∧ P2 ∧ P3 ∧ P4 → `PASS_C1_PREREG_READY`. |
| FAIL | ¬P1 with P2 and P3 achievable → **`REDUCE_TO_STANDARD_POLICY_CONFIGURATION_TEST` (current state)**. ¬P2 or ¬P3 with the lineage framing kept → `HOLD_C1_CAUSAL_IDENTIFIABILITY`. A design in which C is not manipulated at all, or is confounded with M or E → `FAIL_C1_SOFT_LINEAGE_TEST_NOT_MEASURING_SOFT_LINEAGE`. |
| UNKNOWN | P4 is currently FALSE/UNKNOWN (inputs unset). Under every verdict the state is therefore "not ready to freeze". UNKNOWN is never mapped to PASS. |
| RECOVERY | Rename the test (H_SP). Adopt G04 and G23 (full 2^4; capability-balanced M; C−=NODE_SPECIFIC; A-PLACEBO and A-NONE arms; 2-stage protocol). Add M×E and C×P to the PR #45 preregistered set and correct the M03 wording. Freeze margins (G06). Run E1 on a disjoint pilot. Lock the evaluator. Battery authored outside the lineage (MA-L2-06). Then submit to AXIOM for the sec. 38 decision. |
| FALSE_POSITIVE_RISK | (gate says PASS wrongly) A nominally heterogeneous closed-model panel shares training data, so Δ_C≈0 even though dependence is high. Judge or normalization artifacts (G03 T09/T10). Shared-prefix effects mistaken for constitution content if the placebo arm is dropped. |
| FALSE_NEGATIVE_RISK | (gate withholds PASS wrongly) The operator's concept may truly be "policy sharing only", in which case REDUCE under-claims. That costs little and is reversible via Alternative A1. Margins that are too strict for achievable precision would make the result systematically INCONCLUSIVE (mitigated by G06 sec. 6 and A-MIN sizing). |

## 3. B0 and C gate status records (sec. 35 gate format)

### 3.1 G08-B0 status (design gate; outcome not evaluated)
| Field | Content |
|---|---|
| INPUT | Frozen generator (hash), DEV/TEST seeds, pipeline configs tuned on DEV, Δ definitions (Δ-PH, Δ-COST, Δ-DISAGREE), margins. |
| PREDICATE | H-B0-1: at COVERAGE ≥ 0.80, Δ reduces HIGH_COST_FP by ≥ 25% relative to the best non-Δ-PH hold policy at equal coverage, with ΔFNR ≤ +5 pp, on TEST, in the core grid at SNR ≥ 2. Abstention must not concentrate on true segments (G08 sec. 7–8). |
| PASS | `B0_SYNTHETIC_POC_PASS_C1`: "Δ is a useful hold policy in synthetic movies under generator vX". Never biological validation (sec. 2, sec. 12). |
| FAIL | No FP reduction beyond the best non-PH hold policy, or only at coverage < 0.80. |
| UNKNOWN | **Current state**: not generated, not run. Later: a CI that straddles the margin, or a generator that fails GT validation. |
| RECOVERY | Freeze the generator, Δ and margins; AXIOM B0 release; run B-MIN first (Q25). |
| FALSE_POSITIVE_RISK | Δ exploits generator artifacts (e.g. Gaussian PSF matching LoG/PH kernels). Mitigated by the PSF-misspecified arm and multiple debris shape families. |
| FALSE_NEGATIVE_RISK | The generator is too easy or too hard (ceiling or floor). Mitigated by the SNR sweep. |
| STATUS | `DESIGN_READY_PENDING_FREEZE`. Margins are `DEFAULT_PENDING_OPERATOR`. PH = DEMOTED (promotion only via H-B0-2). |

### 3.2 G-C (Part C authority) status
| Field | Content |
|---|---|
| INPUT | Capsule spec (none exists), pinned TRUST_ANCHOR set (none defined), revocation source (none), scope grammar (none), negative fixtures G-C01..G-C11 (specified in G11, not implemented). |
| PREDICATE | `AUTHORIZED(c, verifier, t)` per G11 sec. 3, the conjunction of signature, key binding to a trust anchor, non-revocation, audience, time, freshness, policy and attenuation. Any UNKNOWN conjunct → deny. |
| PASS | Every negative fixture G-C01..G-C11 is rejected, and the positive fixtures pass, against a profile implementation with pinned anchors. → `NAC_PROFILE_PASS_C1` (authority semantics only; never truth or scientific validity). |
| FAIL | Any negative fixture is accepted, e.g. a self-signed fresh-key capsule (G-C11 + G-C05). |
| UNKNOWN | **Current state**: no anchor set, no revocation, no scope grammar, so AUTHORIZED is undecidable → `HOLD_C1_R10R9_AUTHORITY_TRUST_MODEL_UNRESOLVED`. |
| RECOVERY | PO-C1..PO-C5 (G20). Profile Biscuit or COSE + SCITT. Add the TRUST_ANCHOR_ID, REVOCATION_REF and CLAIM_CEILING fields. Implement the fixtures. Separate AXIOM C release. |
| FALSE_POSITIVE_RISK | Code that treats `SIGNATURE_VALID` as `AUTHORIZED` (the easiest attack, Q15). TOFU anchors. |
| FALSE_NEGATIVE_RISK | Over-strict expiry or skew rules deny legitimate capsules (G-C02). Availability outages deny via UNKNOWN (G-C09/G-C10). |

## 4. Blocking items before any PASS label for Part A (prereg-repair list)
1. Operator: model list with pinned IDs/fingerprints, and the G04 sec. 6 MODEL_INDEPENDENCE table (closed models → UNKNOWN).
2. Operator: MESOI and the margins δ_φ, δ_d, δ_mc, δ_wc (defaults in G23 sec. 3).
3. Evaluator lock: deterministic scorer plus a blind human audit (≥ 10%); any LLM judge is secondary only and from outside the subject families.
4. E1 calibration receipt (DEFF, accuracy band, adherence floors, contamination probe).
5. Battery authored outside the lineage, with a prior-knowledge probe (MA-L2-06).
6. Definition of C=NO → default NODE_SPECIFIC (MA-L2-01 option B).
7. M03 interpretation → "balanced across C arms" (MA-L2-03 option A).
8. Exposure protocol → 2-stage (MA-L2-04 option A).
9. Rename the test to H_SP, or define a lineage factor L (MA-SYN-01).
10. Placebo text authored and rated neutral, blind, before freeze (EO-02).

## 5. What a reduced PASS would and would not mean
- **Would:** a descriptive, configuration-specific C1 result about how sharing a policy text affects error correlation, dissent retention, minority-correct retention, warranted convergence, calibration and revision among nominally heterogeneous LLM calls with partitioned evidence. It is conditional on {battery, models, versions, MODEL_INDEPENDENCE status}.
- **Would not:** validate Soft-Lineage empirically (sec. 2); establish any lineage, inheritance or provenance property; establish MODEL independence; generalize beyond the battery, models or versions; or support any C2+ claim.
