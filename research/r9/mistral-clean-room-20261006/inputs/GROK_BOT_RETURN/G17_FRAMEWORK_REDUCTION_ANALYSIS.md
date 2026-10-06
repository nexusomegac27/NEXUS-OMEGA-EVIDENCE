# G17 — Framework Reduction Analysis (ORDER sec. 27–28)

```text
OBJECT        = G17_FRAMEWORK_REDUCTION_ANALYSIS
LANE          = 3 · GROK-BOT external non-lineage reviewer
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY · DESIGN/ANALYSIS ONLY
LAST_VERIFIED = 2026-10-05
PRIOR-ART MATRIX = G16_SELF_CONTAINED_ORDER_PRIOR_ART_MATRIX.csv (PA-01…PA-22)
LEDGER        = G01_part_lane3.csv
VERDICT (lane 3) = REDUCE_C1_R10R9_TO_EXISTING_STANDARDS_AND_METHODS — for the "self-contained order" / SCEF construct
```

## 1. The question as posed

> Is a "self-contained NEXUS order" just DESIGN-BY-CONTRACT + PREREGISTRATION + POLICY-AS-CODE + PROVENANCE + STATE MACHINE + ASSURANCE CASE?

**Answer: yes, with one addition the order itself omitted: the military mission order (OPORD/commander's intent).** Mission orders are the closest single prior art for the *intent* layer and for the "act without asking back" rule. Adding them to the list leaves no SCEF component uncovered. What remains distinctly NEXUS is a **convention bundle**, not a method: claim ceiling + source-class typing + reduction-as-success + metaphor hygiene. That convention is useful and cheap, but it is not a new framework.

## 2. Component-by-component reduction

| SCEF component (ORDER sec. 27) | Where it appears in ORDER.txt | Prior art that already covers it (G16 IDs) | Residual NEXUS-specific content |
|---|---|---|---|
| INTENT | sec. 0 "OPERATOR INTENT", sec. 39 one-sentence core | **PA-08 FM 5-0**: commander's intent is "a clear and concise expression of the purpose of the operation and the desired objective and military end state" and "establishes the limits within which a subordinate may exercise initiative" (para 1-69, L3-028); PA-05 preregistration research question (L3-017); PA-06 SPIRIT objectives (L3-019) | none |
| ONTOLOGY | sec. 3 source classes, sec. 18 NAC levels, D_EPISTEMIC/D_CONTROL | PA-02/03/04 typed formal specs; PA-07 RFC terminology sections; PA-10/11 GSN/SACM element types; PA-21 SHACL closed shapes | the specific source-class vocabulary (an enumeration, not a method) |
| STATE | header STATE=, sec. 0 current head/state | PA-08 OPORD para 1 "Situation"; PA-17 SCXML; PA-15 ASL; PA-19 provenance records | binding state to a git commit hash, which is ordinary provenance (PA-19) |
| INVARIANTS | sec. 2 "MUST NOT" list; `SIGNATURE_VALID != AUTHORIZED` etc. | PA-01 DbC class invariants (L3-021); PA-02 TLA+ invariants; PA-18 policy-as-code (OPA/Cedar) | the content of the invariants (epistemic non-equalities), not the mechanism |
| SOURCE_BOUNDARIES | sec. 3–4 | PA-19 PROV/SLSA/SCITT; PA-09/10 assurance-case evidence and context nodes; PA-06 SPIRIT data sources | the **claim-boundary columns per source** (WHAT_IT_SUPPORTS / DOES_NOT_SUPPORT). This resembles assurance-case "context/assumption" nodes but is applied to literature. A weak residual. |
| EXECUTION_RULES | sec. 1, 34, 36 | PA-07 BCP 14 MUST/SHOULD (L3-025); PA-13/14/16 workflow languages; PA-08 OPORD para 3 "Execution" + coordinating instructions; PA-05 prereg analysis plan | "no ping-pong", which is the mission-command principle of disciplined initiative within intent (L3-028 D-14, 1-69) |
| FAILURE_MODES | sec. 10, 20, 30, 1 (BLOCKED_LANE != BLOCKED_SYSTEM) | PA-08 branches = "contingency options built into the base plan" (1-47); PA-07 RFC 3552 mandatory Security Considerations (L3-027); PA-15 Retry/Catch; PA-09 safety cases (hazard analysis); PA-01 contract violation | none |
| OUTPUT_CONTRACT | sec. 34–35 | PA-06 SPIRIT checklist; PA-13 CWL typed outputs; PA-20 A2A artifacts; reporting guidelines generally | the sec. 35 per-claim tuple (OBSERVATION…IMPACT). It is close to assurance-case claim–evidence–context structure (PA-10/11). |
| TERMINAL_STATES | sec. 11, 37 | PA-17 SCXML final states; PA-15 Succeed/Fail; PA-14 BPMN end events; PA-08 end state; PA-20 A2A TaskState | `REDUCE_*` as a *success* terminal state. This is unusual as a formal state, but it is the scientific-method norm of accepting null and reduction results. |

Count from G16: every SCEF component is covered by at least 5 independent prior-art families (intent 5, output_contract 7, source_boundaries 8, terminal_states 9, ontology/invariants/failure_modes 12, execution_rules 13, state 16). The coverage tags are my own judgement and should be independently re-tagged.

## 3. What the ORDER is *less* than the sum of its prior art

The reduction cuts both ways. The ORDER lacks properties that each reduction target has:

1. **No formal semantics.** Unlike TLA+/Z/SCXML/ASL (PA-02, PA-03, PA-15, PA-17), there is no grammar. ALL-CAPS tokens are both prose and identifiers. RFC 8174 exists precisely to separate normative capitals from ordinary words (L3-026), and the ORDER loses that signal by writing everything in capitals.
2. **No machine-checkability.** Nothing in the ORDER is validated by a schema (contrast JSON Schema/SHACL, PA-21).
3. **Not referentially closed.** G18 §4 lists 18 adjudicated unbound references. Among them: the "operator's R10R9 draft" that sec. 31 orders to be audited, the "original R9 text" whose contradiction sec. 12 repairs, three unresolvable `:chatgpt-content-reference{index=n}` pointers, and the undefined central term "Soft-Lineage".
4. **A stale external pin.** A2A is pinned to 1.0.0 (sec. 4.2, 22), but the latest release is v1.0.1, published 2026-05-28 13:34 CEST (L3-038). MCP and SLSA are left as "current" without a version (current values: MCP 2026-07-28, L3-039; SLSA v1.2, L3-052).
5. **Length is not closure.** At 29,285 bytes, the order is long. LLM performance degrades when relevant content sits mid-context (L3-047), so length can reduce the probability that a constraint is actually applied.

## 4. Minimal difference (if any)

After reduction, the smallest residual that is not obviously a renamed existing method is:

```text
SCEF_RESIDUAL =
  CLAIM_CEILING as an output-wide monotone constraint
    (no emitted statement may exceed level Ck; every external claim carries a source class)
+ REDUCTION_IS_SUCCESS as a declared terminal state
+ METAPHOR two-layer rule with leak test (G14)
```

- Each item is a **convention** that can be expressed *inside* existing methods. The claim ceiling is a policy-as-code rule over output statements (PA-18) or an assurance-case confidence constraint (PA-10/11). Reduction-as-success is a terminal state (PA-17). The metaphor rule is a style rule plus a static diff test.
- No item needs the NEXUS branding to operate.
- The *combination*, applied to LLM-agent research orders read by both humans and LLMs, is plausibly not documented as a single profile. I found no such profile, but my search was targeted, not systematic. That makes the composition a candidate **profile**, comparable to how the NEXUS repo already describes its pipeline as "inspired by RO-Crate, W3C PROV, OCFL, BagIt … conformance not claimed" (README, L3-053).

**Recommended naming:** call it "NEXUS order profile (over OPORD structure + prereg + DbC/policy-as-code + provenance + state machine + assurance-case claim boundaries)". Retire "framework" / "SELF_CONTAINED_EXECUTION_FRAME" as a novel construct.

## 5. Reduction gate (ORDER sec. 35 gate format)

| Field | Content |
|---|---|
| INPUT | ORDER.txt (sha256 7cd05a1f…0baf), G16 matrix |
| PREDICATE | ∀ SCEF component c: ∃ prior art p with SOURCE_CLASS ∈ {PRIMARY_STANDARD, PRIMARY_SPECIFICATION, PEER_REVIEWED} covering c; AND the residual contains no mechanism that cannot be expressed in those methods |
| PASS (= REDUCE) | Both hold → `REDUCE_C1_R10R9_TO_EXISTING_STANDARDS_AND_METHODS` for the SCEF construct |
| FAIL (= NEXUS contribution) | A component with no prior art, or a residual mechanism (not a convention) that changes outcomes |
| UNKNOWN | Coverage tags not independently re-tagged; search not systematic → current result = PASS_WITH_CAVEATS |
| RECOVERY | An independent re-tagger outside NEXUS lineage re-codes G16; a systematic search for an "agent research order profile" |
| FALSE_POSITIVE_RISK | Over-generous coverage tags (e.g. counting OPORD "failure modes" = branches as equivalent to falsifiers) |
| FALSE_NEGATIVE_RISK | The composition could have emergent value (fewer relay errors) that per-component reduction cannot see. Only the G18 empirical question can test that. |

**Current result: PASS (reduce) with caveats.** This does *not* reduce Part A's soft-lineage question or Part C's delegation semantics. Those are other lanes. The anti-reduction case for them is attacked in G19.

## 6. Major claims (ORDER sec. 35 format)

**MC-G17-1 — SCEF is fully covered by prior art.**
- OBSERVATION: The G16 matrix shows coverage of all 9 components. A single document type, the US Army mission order, covers intent, state, execution, branches/failure modes and end state (L3-028).
- SOURCE: L3-017, L3-019, L3-021…L3-046. SOURCE_CLASS: PRIMARY_STANDARD / PRIMARY_SPECIFICATION / PEER_REVIEWED.
- INTERPRETATION: "Self-contained order = decodable compressed world-model" restates long-standing order and specification practice.
- ALTERNATIVE: The bounded-task LLM-agent context might demand properties (e.g. robustness to model drift) that none of the prior art addresses.
- UNCERTAINTY: The coverage tags are reviewer judgement. Paywalled standards (ISO 15026-2, UL 4600, Z) were assessed from abstracts only.
- FALSIFIER: An SCEF component for which a competent re-tagger finds no prior-art coverage.
- IMPACT_ON_R10R9: Remove novelty language. Treat SCEF as a profile.

**MC-G17-2 — The ORDER does not meet its own closure standard.**
- OBSERVATION: 18 adjudicated unbound references, 3 unresolvable citation pointers, a stale A2A pin (G18 §4; L3-038).
- SOURCE: ORDER.txt bytes; checker output `work/refclosure_ORDER_lane3.json`; L3-038, L3-039, L3-052. SOURCE_CLASS: PRIMARY_SPECIFICATION (for the version facts).
- INTERPRETATION: Branding the order as "in sich geschlossen" (closing paragraph) is an over-claim.
- ALTERNATIVE: The missing objects exist in the operator's workspace and were omitted only in transport.
- UNCERTAINTY: The adjudication is by a single reviewer.
- FALSIFIER: Supplying the missing objects with hashes, after which a re-check finds 0 material unbound references.
- IMPACT_ON_R10R9: The sec. 31 claim audit cannot be completed as ordered. This is material ambiguity MA-L3-01 (see answers_lane3.md).

**MC-G17-3 — The residual is a convention bundle.**
- OBSERVATION: Claim ceiling, source-class typing, reduction-as-success and the metaphor rule can each be expressed in policy-as-code, assurance-case or state-machine prior art.
- SOURCE: PA-10, PA-11, PA-17, PA-18 (L3-030, L3-031, L3-044, L3-041, L3-042). SOURCE_CLASS: PRIMARY_*/PEER_REVIEWED.
- INTERPRETATION: The minimal NEXUS difference is a profile of conventions. Its value is empirical (does it reduce errors?), not conceptual.
- ALTERNATIVE: Claim-ceiling enforcement across a multi-agent pipeline, if implemented as a checked type over outputs, might be a genuinely new tool artefact.
- UNCERTAINTY: No implementation exists to inspect. Evidence-grading schemes in other fields were not reviewed in this lane (UNVERIFIED).
- FALSIFIER: A working checker that rejects outputs exceeding the ceiling and measurably lowers claim-inflation errors relative to plain review.
- IMPACT_ON_R10R9: If the operator wants a NEXUS contribution, build and test that checker (G18 metrics). Do not rely on prose.
