# G18 — Information-Density Metric Proposal for Orders (ORDER sec. 29–30) + Referential-Closure Checker

```text
OBJECT        = G18_INFORMATION_DENSITY_METRIC_PROPOSAL
LANE          = 3 · GROK-BOT external non-lineage reviewer
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY · PROPOSED, NOT CANONICAL
LAST_VERIFIED = 2026-10-05
CHECKER       = work/tools/refclosure_check.py (heuristic prototype)
CHECKER_OUTPUT= work/refclosure_ORDER_lane3.json
TARGET        = ORDER.txt, 29,285 raw bytes, CRLF, sha256 7cd05a1f3e05fbc27b5ce655ea258cff56ef169cb48648bb49f5ef80ce6b0baf
```

## 0. Framing

"Information density" of an order is **not** bits per token in the Shannon sense. What matters is how much **executable, checkable obligation** the order delivers per unit of reader cost, and whether the reader reconstructs it **without importing errors**. All the metrics below are measured **relative to a reference decomposition** of the order: an adjudicated list of atomic obligations A = {a_1..a_n}, covering intents, rules, gates, outputs, terminal states and falsifiers. Producing A is itself a human judgement. That is the main validity threat to the whole family.

Notation: O = order bytes; A = reference atoms; R = registry of declared terms; E = executor output; T(·) = token count under a pinned tokenizer.

## 1. Metric family (each in ORDER sec. 35 metric format)

### M1 SEMANTIC_COVERAGE
- DEFINITION: |{a ∈ A_required : a is stated in O}| / |A_required|, where A_required comes from a task-type template (e.g. a SPIRIT-like checklist for experiments, L3-019, or the 9 SCEF components, G17).
- DOMAIN: one order × one template. RANGE: [0,1].
- GROUND_TRUTH: an adjudicated template mapping by ≥ 2 raters outside the order's lineage.
- CALIBRATION_METHOD: inter-rater agreement on a calibration set of orders; template items pilot-tested.
- KNOWN_FAILURE_MODE: rewards box-ticking; a component can be "present" but unusable (e.g. terminal states listed with no transition rules).
- WHY_IT_IS_NOT_A_TRUTH_METRIC: it measures whether topics are present, not whether the content is correct or sufficient.

### M2 REFERENTIAL_CLOSURE
- DEFINITION: RC = 1 − |U_material| / |Refs|. Refs = all referents in O (declared terms, identifiers, external objects, citation pointers). U_material = referents that neither resolve inside O nor resolve to a pinned external identifier (hash, RFC number, version, DOI, URL with date) **and** that an executor needs in order to act.
- DOMAIN: order. RANGE: [0,1].
- GROUND_TRUTH: an adjudicated reference list (§4 shows a worked example).
- CALIBRATION_METHOD: precision/recall of the automatic checker against adjudication; report both.
- KNOWN_FAILURE_MODE: depends on the materiality judgement. External pins can be pinned but stale (A2A 1.0.0 vs 1.0.1). Domain terms (PSF, Rips filtration) are "unbound" but closed for domain experts.
- WHY_IT_IS_NOT_A_TRUTH_METRIC: a perfectly closed order can be completely wrong.

### M3 AMBIGUITY_RATE
- DEFINITION: the fraction of atoms a ∈ A for which ≥ 2 independent executors (humans or pinned LLMs) produce non-equivalent operationalisations. Equivalence is judged by the adjudicator, or by identical derived artefacts where these are mechanical.
- DOMAIN: order × executor pool. RANGE: [0,1].
- GROUND_TRUTH: adjudicated equivalence classes.
- CALIBRATION_METHOD: include deliberately ambiguous and unambiguous control atoms.
- KNOWN_FAILURE_MODE: homogeneous executors (same model family) under-detect ambiguity because they share the same priors (cf. ORDER sec. 8).
- WHY_IT_IS_NOT_A_TRUTH_METRIC: agreement among executors ≠ the intended meaning.

### M4 QUESTION_DEPENDENCY
- DEFINITION: the number of clarification requests an executor would have to make in order to act on A, normalised by |A|. Measured as (a) questions actually asked when asking is allowed, and (b) recorded assumptions when asking is forbidden (the ORDER sec. 1 regime).
- DOMAIN: order × executor. RANGE: [0, ∞), usually [0,1].
- GROUND_TRUTH: an adjudicator checks whether each question/assumption targets a genuine gap.
- CALIBRATION_METHOD: seed orders with known gaps.
- KNOWN_FAILURE_MODE: no-ping-pong rules hide dependency by converting questions into silent assumptions. **Count recorded assumptions, or the metric is gamed by the rule itself.**
- WHY_IT_IS_NOT_A_TRUTH_METRIC: zero questions can mean confident misreading.

### M5 TOKEN_COST
- DEFINITION: T(O) plus T(all external objects the executor must read to act), under a pinned tokenizer. Report characters and bytes as well.
- DOMAIN: order + closure set. RANGE: ℕ.
- GROUND_TRUTH: the byte strings themselves.
- CALIBRATION_METHOD: fixed tokenizer name and version.
- KNOWN_FAILURE_MODE: ignoring the closure set makes short, unclosed orders look cheap.
- WHY_IT_IS_NOT_A_TRUTH_METRIC: a cost, nothing else.

### M6 RECONSTRUCTION_ACCURACY
- DEFINITION: an independent reader, given only O (no chat history), reproduces A. RA = F1 between the reproduced atoms and A, with a separate count of **added** atoms (hallucinated obligations).
- DOMAIN: order × reader. RANGE: [0,1] for F1; ℕ for additions.
- GROUND_TRUTH: A.
- CALIBRATION_METHOD: ≥ 2 raters align reproduced atoms to A.
- KNOWN_FAILURE_MODE: readers from inside the lineage reconstruct from memory, not from O. Use readers outside the lineage.
- WHY_IT_IS_NOT_A_TRUTH_METRIC: it measures faithful transmission only.

### M7 ERROR_PROPAGATION
- DEFINITION: given a seeded defect d in O (wrong hash, stale version, contradictory rule), the fraction of downstream artefacts in E that inherit d without flagging it.
- DOMAIN: order × seeded defect × executor. RANGE: [0,1].
- GROUND_TRUTH: the defects are known by construction.
- CALIBRATION_METHOD: a library of seeded defects with severity tags; include no-defect controls to estimate false alarms.
- KNOWN_FAILURE_MODE: seeded defects can be easier or harder to spot than natural ones.
- WHY_IT_IS_NOT_A_TRUTH_METRIC: it measures robustness, not correctness.

### M8 OPERATOR_INTERVENTION_RATE
- DEFINITION: the number of operator actions (relays of hash/path/version, corrections, re-orders) per completed order, split into *routine relay* versus *genuine decision* (following R10R7 sec. 34's distinction).
- DOMAIN: order lifecycle. RANGE: ℕ (or rate per atom).
- GROUND_TRUTH: a logged intervention ledger with a category per action.
- CALIBRATION_METHOD: two coders categorise a sample.
- KNOWN_FAILURE_MODE: an operator who stops intervening because of fatigue, not because the order improved. Also Hawthorne effects.
- WHY_IT_IS_NOT_A_TRUTH_METRIC: low intervention can mean low oversight.

### Additional metrics proposed by this lane
- **M9 FALSIFIER_PRESERVATION:** the fraction of the order's falsifiers and terminal FAIL/HOLD conditions that survive into the executor's plan or output. This metric operationalises ORDER sec. 39, "without compressing away the falsifier". RANGE [0,1]. GROUND_TRUTH: an adjudicated falsifier list. FAILURE_MODE: falsifiers restated but never tested. NOT_TRUTH: it shows the falsifier was preserved, not that it is adequate.
- **M10 DENSITY_VS_OPACITY index (descriptive only):** report the pair (RA, T(O)+closure) per order. **Do not collapse it into a single scalar**; the ORDER sec. 3 rule against one-number scores applies here too.

## 2. Central empirical question (design sketch)

*Do more self-contained orders reduce human relay errors without creating dense but opaque specifications?*

- **Unit:** an order. **Manipulation:** the same task written as (i) a minimal order; (ii) a self-contained order (high M1/M2); (iii) a self-contained order + structured JSON twin (machine-checkable registry, §3).
- **Outcomes:** M8 routine-relay count and M7 error propagation (relay errors), plus M6 RA and M3 ambiguity (opacity).
- **Success:** (ii) or (iii) reduces relay errors versus (i), **and** is non-inferior on RA with a preregistered margin. Same logic as G14 S2.
- **Falsifier:** (ii) reduces relay errors but RA drops, or additions rise. That pattern is "dense but opaque".
- **Confound:** writer skill. Use multiple writers per condition, with writers as a random effect.
- Status: DESIGN ONLY. Not run.

## 3. Anti-compression failure modes (ORDER sec. 30) with detectors

| Failure mode | Detector (mechanical where possible) | Evidence in ORDER.txt (observed) |
|---|---|---|
| DENSE_JARGON | ratio of undeclared domain/NEXUS tokens to declared ones (from §4) | 103 heuristic "unbound candidates" vs 12 in-document definitions (noisy, see §4.3) |
| FALSE_PRECISION | numbers or states without a source or derivation (e.g. "10/10", hashes) not linked to a verifiable object | "AXIOM R1 FAIL-CLOSED REGRESSION 10/10" (sec. 0) with no path. It is bound only via the repo at head c07d437, and the order does not name the repo. |
| SYMBOL_OVERLOAD | one token carrying more than one sense (registry conflict) | AIR GAP (relation in sec. 24 vs state in code), HANDSHAKE (G25 output vs receipts vs protocol), Δ undefined (sec. 16) |
| METAPHOR_STACKING | more than one metaphor decoding another within a paragraph | sec. 23–25 lists 8 metaphors without keys; no stacking inside a single rule was observed |
| HIDDEN_ASSUMPTIONS | assumptions an executor must make that the order does not state (M4b) | the "Soft-Lineage" definition; what "C1" is relative to C0/C2; what R10R6 E2 is |
| ONTOLOGY_DRIFT | same concept named differently across sections or releases | "Authority Capsules V2" vs "NAC"; CONSTITUTION (factor C) vs "governance constitution" vs D_CONTROL component |
| UNBOUND_REFERENCES | §4 checker | 18 adjudicated (§4.2) |
| LONG_PROMPTS_THAT_LOOK_COMPLETE_BUT_ARE_NOT_EXECUTABLE | (a) M2 < 1 for material references; (b) the order requests an output it gives no input for | sec. 31 orders an audit of "THE OPERATOR'S R10R9 DRAFT", which is not included. The closing paragraph calls the order "in sich geschlossen". Long contexts are not reliably used (L3-047). |

## 4. Can referential closure be machine-checked? (Q23) — checker design + worked example

### 4.1 Checker design (concrete)

1. **Declared registry (mandatory input):** the order ships a machine-readable `TERMS` block. For each term it gives id, kind (internal-defined / external-pinned / domain-standard / metaphor), definition anchor or external identifier (RFC number, DOI, version, sha256, URL + access date), and sense tag. This is the same idea as SHACL closed shapes (`sh:closed` rejects undeclared properties, L3-045) and JSON Schema `$ref`, whose value MUST be a URI-reference resolved against a base URI (L3-046).
2. **Extraction:** identifier-shaped tokens (versioned IDs, acronyms, hashes, filenames, citation pointers) plus curated phrase rules for prose references ("the operator's draft", "original text").
3. **Resolution:** an internal term needs a definition anchor present. An external term needs an identifier present **and** a freshness check (fetch → compare the version to latest, recording LAST_VERIFIED). A hash needs the object to be retrievable and the hash to match.
4. **Classification:** RESOLVED / PINNED_FRESH / PINNED_STALE / UNPINNED / UNBOUND / UNRESOLVABLE_POINTER.
5. **Materiality:** a token is material if it appears in a gate, a terminal-state condition, an output requirement or an audit list (sections can be tagged).
6. **Human adjudication column:** required. The checker proposes; a human or non-lineage reviewer disposes.

Answer: **partly yes.** Closure *relative to a declared registry* is mechanically checkable, and is routine in schema validation. Closure of free prose is not, beyond heuristics. NEXUS orders written in all-caps prose defeat mechanical extraction, because ordinary English words and identifiers look identical (RFC 8174's capitalisation convention exists to prevent exactly this, L3-026).

### 4.2 Worked example on ORDER.txt (adjudicated by this reviewer)

| ID | Unbound / problematic reference | Location (line) | Class | Material? |
|---|---|---|---|---|
| U01 | "THE OPERATOR'S R10R9 DRAFT" to be audited | sec. 31, l.1127 | UNBOUND (document-external, no hash/path) | **YES**: blocks sec. 31 as ordered |
| U02 | "THE ORIGINAL R9 TEXT" containing the "real vesicles" contradiction | sec. 12, l.529 | UNBOUND | YES for the Part-B audit trail |
| U03 | `:chatgpt-content-reference{index="0/1/2"}` ×3, plus "R10R9-Entwurf", "R9-Kern" in the German preamble | l.1, l.1475 | UNRESOLVABLE_POINTER | YES: these are exactly the unresolvable SEARCH_RESULT-scheme style pointers that sec. 3 prohibits |
| U04 | SOFT-LINEAGE (7 uses), never defined in the order | l.1, 63, 121, 206, 234, 286, 1184 | UNBOUND central term | **YES** |
| U05 | sec. 31 audit list without identifiers: NON-COMPENSATORY RUNTIME ASSURANCE CONTRACTS, TERNARY LOGIC/EPISTEMIC HOLD, DITL HARDWARE CLAIM, DREAM V3, VAIL, ERC-8370, MULTI-AGENT CONSTITUTIONAL DESIGN, PH VESICLE TRACKING | l.1131–1142 | UNBOUND (title-only) | YES: sec. 3 forbids title-only binding, yet the order supplies only titles |
| U06 | R10R6 E2 (what E2 is) | l.73, 118 | UNBOUND (only its prohibition is stated) | medium |
| U07 | E0.2 / GATE2–GATE7 / "AXIOM R1 … 10/10" | l.49–51 | PARTIAL: commit hash given (l.55), but the repository is not named | medium |
| U08 | C1 / claim ladder (C0…Cn undefined) | header, l.120 | UNBOUND scale | medium |
| U09 | Δ (Δ-gating) | sec. 16, l.651 | UNBOUND symbol | YES for Part B |
| U10 | VDS | sec. 21, l.823 | UNBOUND acronym (an RFC 9943 term, L3-050) | low |
| U11 | PSF, ALPHA COMPLEXES, RIPS, CUBICAL PERSISTENCE | sec. 13–14 | DOMAIN_STANDARD (acceptable) | no |
| U12 | MCP "current first-party spec"; SLSA "current official spec"; W3C PROV no version; A2A pinned 1.0.0 | sec. 4.2–4.5, 22, 31 | UNPINNED ×3; **PINNED_STALE**: A2A latest is v1.0.1 (L3-038) | YES for lane binding |
| U13 | G24_MANIFEST_SHA256.json, G25_HANDSHAKE.json formats | sec. 34 | UNBOUND output schema | medium |
| U14 | OMEGA, AXIOM, CURSOR_PRAXIS, HOSTINGER roles/systems | header, sec. 2 | UNBOUND in the order (AXIOM and Cursor are defined in repo `docs/AI_CONTEXT.md`, L3-053) | low |
| U15 | "AUTHORITY CAPSULES V2" (V1 never referenced) | sec. 18 | UNBOUND predecessor | low |
| U16 | TRACKMATE, STARDIST | sec. 15 | tool names without version/identifier | low |
| U17 | "HUMAN RELAY ERRORS" (sec. 29 central question) | l.1099 | operational definition exists only in R10R7 sec. 35 (external) | medium |
| U18 | "VESICLE-TRACKING / LIGHT-TOXICITY POC" origin | sec. 0 B | UNBOUND (which R10R8 artefact?) | medium |

Material count (YES only): U01, U02, U03, U04, U05, U09, U12 = 7 of 18. Rough RC for material references ≈ 1 − 7/|material refs|. The denominator was not exhaustively enumerated, so **no numeric RC is reported (no false precision).**

### 4.3 Checker performance on this example (honest)

- The heuristic prototype flagged 103 `UNBOUND_CANDIDATE` tokens. Only ~18 of them correspond to adjudicated items (e.g. OMEGA, AXIOM, POC, R10R6 E2, C1, SLSA, PSF, ALPHA, RIPS, Δ, V2, VDS, DITL, W3C/PROV, DREAM V3, VAIL, ERC-8370). **Precision ≈ 0.17.** Most false positives are ordinary capitalised English words.
- The `EXTERNAL_PINNED_NEARBY` rule also produced false positives (e.g. GROK, BOT, PUSH, MAIN), because a hash or version merely appears nearby.
- Mixed-case prose references (Soft-Lineage, Hostinger, TrackMate) were caught only by the curated phrase rules.
- Conclusion: without a declared `TERMS` registry the checker is only a triage aid. With a registry, steps 3–5 are deterministic.

## 5. What must never be compressed (Q24, summary; full answer in work/answers_lane3.md)

Hashes and identifiers, versions and dates, claim ceilings and status labels, falsifiers and FAIL/HOLD conditions, authority/delegation scopes and expiries, negations and "≠" boundaries, and exclusion and stopping rules. These are low-redundancy content: a single-symbol error changes meaning. Compressing them through metaphor or summary removes exactly the bits a checker needs.
