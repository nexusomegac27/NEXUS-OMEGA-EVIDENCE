# G14 — Metaphor Compression Framework (ORDER sec. 23–26)

```text
OBJECT        = G14_METAPHOR_COMPRESSION_FRAMEWORK
LANE          = 3 of 3 · GROK-BOT external non-lineage reviewer
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = DESIGN_ONLY (no human or LLM experiment was run)
LAST_VERIFIED = 2026-10-05
SOURCES       = ledger G01_part_lane3.csv (L3-xxx); NEXUS usage in work/REPO_CONTEXT_lane3.md
INPUT_ORDER   = /workspace/r10r9/ORDER.txt (29,285 raw bytes, CRLF, sha256 7cd05a1f3e05fbc27b5ce655ea258cff56ef169cb48648bb49f5ef80ce6b0baf)
```

## 0. Reviewer stance (one paragraph)

The research question is "can metaphor carry high information density without lowering scientific precision?". In this form it is not new and it is not NEXUS-specific. It is the classic question of whether analogies and metaphors help or harm comprehension, studied in structure-mapping theory (L3-002, L3-003), conceptual metaphor theory (L3-001), metaphor-framing experiments (L3-004–L3-007), analogy-induced misconception research (L3-008, L3-009, L3-011) and cognitive-load theory (L3-012, L3-013). NEXUS can add one bounded thing: a **testable acceptance rule for metaphors inside governed specifications**. That rule is the two-layer code plus the leak test plus non-inferiority on false inference. The rule is an engineering convention. It is not a scientific discovery, and adopting it does not need the experiment. The experiment is only needed to decide whether metaphors should be **allowed at all** in NEXUS orders.

## 1. Definitions

| Term | Definition (proposed, not canonical) |
|---|---|
| Concept κ | A unit of the formal specification: predicates, state transitions, gates, fixtures and falsifiers that a reader must be able to apply. |
| D_LAYER(κ) | The formal representation: the decoded, independently available specification text or code for κ. |
| M_LAYER(κ) | A short metaphorical expression μ that names a familiar *base* domain B, used to evoke κ in the *target* domain T. |
| DECODE_KEY(μ→κ) | An explicit relational mapping: a list of base relations ↦ target relations (`maps`), **plus** a list of base relations that must **not** be transferred (`does_not_map`), **plus** a sense tag when μ is polysemous. This follows structure-mapping: what an analogy transfers is relations chosen by systematicity, not object attributes (L3-002). |
| Licensed inference | An inference about κ that follows from D_LAYER. |
| False inference | An inference a reader draws from μ (with or without the key) that D_LAYER does not license. The danger case is an inference D_LAYER contradicts. |
| Material false inference | A false inference that would change a PREDICTION, GATE, FIXTURE, FALSIFIER, STATE TRANSITION, authority decision or claim level (the ORDER sec. 26 list, extended by authority and claim level). |

Metaphor is therefore treated as **lossy semantic compression with side information**:

```text
reader_model(κ) = decode(μ, DECODE_KEY, reader_priors)
loss(μ)  = licensed inferences the reader fails to recover            (information lost)
leak(μ)  = unlicensed inferences the reader adds from the base domain  (false inference)
cost(μ)  = tokens + reading time + decode effort
```

Conceptual metaphor theory predicts that a metaphor *highlights* some aspects and *hides* others (L3-001, ch. 3). In this framework, hiding is `loss` and over-transfer is `leak`. The analogy-misconception literature shows that a single analogy tends to shrink a complex concept to the source's core (L3-008), and that learners over-extend conceptual metaphors (L3-009). That is why `does_not_map` is mandatory and not optional.

## 2. Two-layer code — required structure

Every technical metaphor in a NEXUS order MUST be emitted as:

```json
{"term":"AIR_GAP","sense":"STATE|RELATION","M_LAYER":"…","D_LAYER_ref":"<path#anchor or sha256>",
 "DECODE_KEY":{"maps":[["base relation","target relation"]],"does_not_map":["…"]},
 "safe_use":"…","prohibited_use":["…"]}
```

Rules:

1. **D_LAYER first.** The formal text must exist, be addressable (path plus hash) and be complete without μ (ORDER sec. 26 condition 3).
2. **One sense per token.** A polysemous term (inside NEXUS today: AIR_GAP, SYMBIOSIS and HANDSHAKE each have 2–3 senses, see REPO_CONTEXT) must carry a sense tag or be split into distinct identifiers.
3. **No metaphor as an identifier in executable artefacts** (enum values, gate states, schema keys) unless a mapping table to a neutral identifier is in the same artefact. Observed counter-example: `S.AIR_GAP` in the E0.2 gate code (L3-053).
4. **No metaphor stacking.** One metaphor per concept per paragraph. A metaphor must not be decoded through another metaphor.
5. **Familiarity declared.** Novel metaphors are processed by comparison and need the key. Conventionalised ones are processed by categorisation (L3-003). NEXUS coinages are novel for every external reader, so the key is mandatory for them.

## 3. Scientificity rule (ORDER sec. 26), operationalised

A metaphor μ for concept κ is ACCEPTABLE iff all three hold:

| Condition | Operational predicate | Data |
|---|---|---|
| S1 reduces communication cost | `cost(METAPHOR_PLUS_DECODE_KEY) < cost(FORMAL_ONLY)` at **equal or better** comprehension. Here cost = tokens of the stimulus actually needed (μ + key; D_LAYER stays available but is not read) + reading time. | Token count under a pinned tokenizer; timing |
| S2 does not increase material false inference | Non-inferiority: the upper bound of the 90 % CI of `FIR(M+K) − FIR(FORMAL_ONLY)` is below the margin Δ_FI (TOST/one-sided logic, L3-015). **A non-significant difference is NOT enough.** | False-inference probes (G15) |
| S3 formal spec independently available | D_LAYER_ref resolves and passes the leak test (sec. 4) | Static check |

S1 has a real tension that must be stated openly: the key is not free. If `tokens(μ + DECODE_KEY) ≥ tokens(D_LAYER)`, the metaphor saves nothing on tokens. It can then only be justified by recall or transfer gains. For short formal definitions (e.g. "UNRESOLVED ≠ FALSIFIED; missing input ⇒ UNRESOLVED") that will usually be the case. **Prediction (falsifiable): for most NEXUS concepts, M+K is not shorter than a well-written formal sentence.**

## 4. METAPHOR_LEAK test = FAIL_METHOD (gate in ORDER sec. 35 format)

| Field | Content |
|---|---|
| INPUT | Order/spec O (bytes plus hash); a term registry listing every metaphor token; derived artefacts (predictions, gates, fixtures, falsifiers, state machine, authority rules). |
| PREDICATE | Build O′ = O with every metaphor token replaced by its neutral identifier, and every metaphor-only sentence deleted. Re-derive all artefacts from O′. LEAK := any derived artefact(O′) ≠ derived artefact(O), after canonicalisation (identifier renaming via the registry is allowed). Second check: decode consistency. Every D_LAYER for the same token must yield the same artefact semantics (e.g. one state value, not two). |
| PASS | All artefacts are identical modulo registry renaming, AND decode is consistent. |
| FAIL | Any artefact changes (METAPHOR_LEAK = FAIL_METHOD), OR two decodes of the same token disagree (DECODE_INCONSISTENCY, also FAIL_METHOD). |
| UNKNOWN | Artefacts cannot be re-derived mechanically (prose-only gates), or the registry is incomplete. Mark the result HOLD; it is not a PASS. |
| RECOVERY | Move the content the metaphor was carrying into D_LAYER; split polysemous tokens; re-run. |
| FALSE_POSITIVE_RISK | Harmless re-derivation noise, e.g. an LLM-based re-derivation that varies between runs. Mitigate with deterministic extraction or majority-of-k with a fixed seed and model version. |
| FALSE_NEGATIVE_RISK | The metaphor only influences *human* readers (covert framing, L3-004/L3-005). That leaves the artefacts unchanged but changes people's decisions. **The static leak test cannot detect this. Only the reader experiment (sec. 5) can.** |

Worked application to current NEXUS bytes (C1, observational):

- `AIR_GAP` in `E0_2_FULL_INTEGRATION_TEST_AXIOM_R1.py`: renaming the symbol is behaviour-neutral, so it passes predicate part 1. Part 2 fails. The ORDER sec. 24 D_LAYER ("a declared non-collapse relation between two semantic types") does not describe what the code does ("missing/unknown input ⇒ hold"). The AXIOM receipt also records that integrated GATE5 returns AIR_GAP where standalone GATE5 returns FALSIFIED (L3-053). → **DECODE_INCONSISTENCY = FAIL_METHOD for AIR_GAP as currently used.** This can be repaired by splitting the token into `UNRESOLVED` (state) and `NCI_RELATION` (relation).
- R10R7 order sec. 2 already specifies the neutral-copy removal test (YANG_MILLS, FATHER, CHILD, SPALT, NADELOEHR …). In the public repo I found no executed receipt of that test. → Status UNVERIFIED that it was ever run.

## 5. Three-condition experiment (design only)

### 5.1 Hypotheses (preregistrable)

- **H1 (cost):** tokens and reading time are lower in M+K than in FORMAL_ONLY, at equal or better comprehension. *Prediction from §3: H1 fails on tokens for most short concepts.*
- **H2 (precision, non-inferiority):** FIR(M+K) − FIR(FORMAL_ONLY) < Δ_FI.
- **H3 (metaphor-only harm):** FIR(METAPHOR_ONLY) > FIR(FORMAL_ONLY). This is the expected direction and the positive control for the false-inference probes. If H3 fails, the probes are insensitive and H2 cannot be interpreted.
- **H4 (recall/transfer benefit):** delayed recall and transfer are higher in M+K than in FORMAL_ONLY. This is the only route by which metaphors could earn their place.
- **H5 (expertise moderation):** the M+K advantage, if any, shrinks or reverses with domain expertise (expertise-reversal, L3-013).

### 5.2 Design

- **Conditions:** FORMAL_ONLY / METAPHOR_ONLY / METAPHOR_PLUS_DECODE_KEY. Stimuli are from G15 (10 concepts; ≥ 8–12 items per concept per measure after piloting).
- **Assignment:** within-participant across concepts, using a Latin square. Each participant sees each concept in exactly one condition, and every condition equally often, so a participant never sees the same concept twice. Randomise order. Counterbalance concept × condition across lists.
- **Control for exposure:** include a FORMAL_ONLY condition with a matched-length neutral filler. Steen et al. found that reading the text itself, not the metaphor, moved responses once a non-metaphor control was added (L3-006). Measure pre-existing familiarity with the base domain and with NEXUS.
- **Readers:** (a) human participants stratified by expertise (novice / technical non-NEXUS / NEXUS-internal); (b) optionally LLM readers as a *separate* study. LLM readers are not human proxies: training overlap is unknown (ORDER sec. 8), and long-context use is unreliable (L3-047). Pin LLM readers by model ID, version, temperature and seed. Never pool them with humans.
- **NEXUS-internal readers** are lineage-contaminated. Analyse them separately, never as primary evidence.
- **Blinding:** item scorers are blind to condition. Free-recall rubrics are scored by ≥ 2 raters, with a chance-corrected agreement threshold preregistered.
- **Ethics:** human-subject administration requires the applicable ethics review and informed consent before any data collection. That decision belongs to the operator/AXIOM, outside this order.

### 5.3 Measures (each in the ORDER sec. 35 metric format)

| Metric | DEFINITION | DOMAIN | RANGE | GROUND_TRUTH | CALIBRATION_METHOD | KNOWN_FAILURE_MODE | WHY_IT_IS_NOT_A_TRUTH_METRIC |
|---|---|---|---|---|---|---|---|
| COMPREHENSION | proportion correct on forced-choice items keyed to D_LAYER | item × reader | [0,1] | answer key derived from D_LAYER, independently adjudicated | pilot item difficulty; drop items at ceiling or floor | items that test vocabulary instead of rules | measures agreement with the spec, not whether the spec is true |
| RECALL | rubric score of delayed (e.g. 24 h) free reproduction of the formal rule | reader × concept | [0,1] | rubric of rule atoms from D_LAYER | two raters with an agreement threshold | rubric too lenient on paraphrase | memory of the spec, not its validity |
| TRANSFER | proportion correct on novel-case application items | item × reader | [0,1] | D_LAYER applied to the new case by the adjudicator | pilot; adjudicator disagreement ⇒ exclude the item | items solvable by surface heuristics | consistency with the spec only |
| ERROR_RATE | 1 − proportion correct across all non-probe items | reader × condition | [0,1] | as above | as above | conflates guessing with misreading | as above |
| FALSE_INFERENCE_RATE (FIR) | proportion endorsing a probe that the base domain suggests and D_LAYER contradicts (G15 `false_inference_probe`) | probe × reader | [0,1] | the probe's contradiction with D_LAYER | METAPHOR_ONLY must exceed FORMAL_ONLY (positive control, H3) | probes too obvious, i.e. demand characteristics | measures over-transfer from the metaphor, not the truth of the spec |
| MATERIAL_FIR | FIR restricted to probes that would change a gate, prediction or authority decision | as FIR | [0,1] | probe tagged by an adjudicator before data collection | as FIR | tagging bias | as FIR |
| TOKEN_COUNT | stimulus tokens actually presented (μ + key, or D_LAYER) under a pinned tokenizer (name + version) | stimulus | ℕ | the byte strings | fixed tokenizer; also report characters and words | tokenizer dependence | a cost measure only |
| READ_TIME | seconds from stimulus onset to first response | reader × stimulus | ℝ⁺ | timestamps | trim with a preregistered rule | attention lapses | a cost measure only |

Primary outcome = MATERIAL_FIR (H2). Secondary = COMPREHENSION, TRANSFER, TOKEN_COUNT. Everything else is exploratory.

### 5.4 Analysis plan

- **Model:** a mixed-effects logistic regression for each binary outcome, `outcome ~ condition × expertise + (1 + condition | participant) + (1 + condition | concept) + (1 | item)`. The random-effects structure is the maximal one the design justifies, with a preregistered simplification order if the model fails to converge (L3-016).
- **H2:** a non-inferiority/equivalence test on the risk difference (M+K − FORMAL_ONLY), with margin Δ_FI fixed before data collection (L3-015). Proposed default Δ_FI = 0.05 absolute on MATERIAL_FIR. This is a judgement call, not a sourced value. **A metaphor fails S2 if non-inferiority is not shown.** It is not "accepted because there was no significant difference".
- **Multiplicity:** H2 is the single primary test. For secondary outcomes, use Holm correction across the H1/H3/H4/H5 families.
- **Per-concept decisions:** run the acceptance rule per metaphor. Each metaphor needs its own precision. Shrinkage via concept random effects is allowed for estimation, but a per-concept accept/reject decision requires that concept's own CI bound.
- **Stopping:** fixed n, no interim efficacy looks. **Missing data:** participants who complete fewer than 80 % of items are excluded, with the rule preregistered. Report the count.
- **Version freeze:** freeze stimuli bytes, tokenizer, LLM versions and the analysis script, and hash them before launch.

### 5.5 Precision plan (planning for accuracy, L3-014) — illustrative arithmetic, assumptions flagged

The numbers below are my own normal-approximation arithmetic. They are not sourced values.

- Estimating a single FIR near p = 0.15 to ±0.05 (95 % CI) needs ≈ 196 independent responses per condition. ±0.04 needs ≈ 306.
- A two-group non-inferiority test at p = 0.15, margin 0.05, one-sided α = 0.05 and power 0.80 needs ≈ 631 independent responses per condition.
- Responses cluster within participants. With m = 10 probe responses per participant per condition and ICC = 0.10 (an assumption), the design effect is 1.9. That means ≈ 631 × 1.9 / 10 ≈ 120 participants contributing to each condition overall. With the Latin-square within-participant design, ~120–150 participants per expertise stratum is the order of magnitude for **pooled** H2. **Per-concept** non-inferiority at this margin needs roughly 10× more and is unrealistic. Per-concept decisions therefore need a wider margin (e.g. 0.10) or a sequence of smaller, concept-targeted studies.
- Replace these figures with a simulation-based plan using pilot ICC and base rates before preregistration.

### 5.6 Threats and how the design answers them

| Threat | Mitigation |
|---|---|
| Metaphor effect is really exposure or text-length effect (L3-006) | matched-length FORMAL_ONLY filler; pre-measures |
| Covert framing that readers don't report (L3-004, L3-005) | behavioural probes, no self-report |
| Experts find the keys redundant (L3-013) | expertise stratification (H5) |
| Item authors are NEXUS-lineage, which biases the keys | independent item adjudicator outside NEXUS; publish the keys before data collection |
| Domain-specific results (political-framing meta-analysis, L3-007) do not transfer to technical specs | treat prior effect sizes as uninformative; pilot |
| LLM readers contaminated or unstable | separate study, version pinning, repeated runs |

## 6. Major claims (ORDER sec. 35 format)

**MC-G14-1 — The metaphor question reduces to existing research programmes.**
- OBSERVATION: Structure-mapping (L3-002, L3-003), conceptual metaphor (L3-001), framing experiments (L3-004–L3-007), analogy-misconception work (L3-008, L3-009) and cognitive load (L3-012, L3-013) already cover cost, loss, over-transfer and moderation by expertise.
- SOURCE: L3-001…L3-013. SOURCE_CLASS: PEER_REVIEWED (one book, one edited chapter).
- INTERPRETATION: The scientific question is not novel. The NEXUS contribution is at most an acceptance convention for governed specs.
- ALTERNATIVE: Technical governance specs read by mixed human/LLM audiences could behave differently enough to be a new domain.
- UNCERTAINTY: No study found specifically on metaphors in machine-checkable governance orders. My search was targeted, not systematic.
- FALSIFIER: A primary source showing a prior acceptance rule of the form "metaphor + decode key + leak test + non-inferiority" would remove even the convention's novelty. Finding effect sizes for technical specs would make the pilot unnecessary.
- IMPACT_ON_R10R9: Do not frame G14 as a research contribution. Frame it as a hygiene convention plus one optional study.

**MC-G14-2 — Current NEXUS use of AIR_GAP fails the leak test (decode inconsistency).**
- OBSERVATION: Code maps missing and unknown inputs to `AIR_GAP`. The receipt documents a GATE5 AIR_GAP-vs-FALSIFIED divergence. The ORDER's D_LAYER describes a relation, not a state.
- SOURCE: L3-053 (repo at c07d437), ORDER sec. 24. SOURCE_CLASS: IMPLEMENTATION_REPO (lineage-internal).
- INTERPRETATION: One token carries two semantics, and readers and implementers decoded it differently.
- ALTERNATIVE: AXIOM may consider "relation" and "state" the same concept at different levels (the state reports that the relation is undecided). If a written mapping exists, the inconsistency reduces to a missing sense tag.
- UNCERTAINTY: Non-public NEXUS documents may define AIR_GAP fully (UNVERIFIED).
- FALSIFIER: A canonical NEXUS definition document, hash-bound, that both code paths cite and that resolves GATE5 to one value.
- IMPACT_ON_R10R9: Rename or split before any R10R9 gate uses it. Add a decode-consistency check to the gate suite.

**MC-G14-3 — The M+K condition is unlikely to save tokens for short concepts.**
- OBSERVATION: The G15 decode keys (maps + does_not_map) are typically as long as or longer than the formal one-line rule.
- SOURCE: G15 fixtures (this lane). SOURCE_CLASS: N/A (own artefact).
- INTERPRETATION: H1 (cost) will probably fail on tokens. Any benefit must show up in recall or transfer (H4).
- ALTERNATIVE: Once readers learn a key (amortised across documents), later uses of μ cost ~1–3 tokens. That is the real compression channel, but it depends on prior key exposure, i.e. on lineage.
- UNCERTAINTY: Token counts depend on the tokenizer. No measurement has been made.
- FALSIFIER: Measured TOKEN_COUNT(M+K) < TOKEN_COUNT(FORMAL_ONLY) with no comprehension loss for most concepts.
- IMPACT_ON_R10R9: If amortisation is the mechanism, the right experiment is a repeated-exposure design. A single-shot comparison would miss it.
