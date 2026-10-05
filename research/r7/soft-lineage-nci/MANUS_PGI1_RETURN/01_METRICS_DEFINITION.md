# M-PGI1-01 — Candidate Metrics for `dist(BELIEF_STATE, WORLD_STATE)`

**Status:** DESIGN_ONLY · **Claim ceiling:** `C1_DESCRIPTIVE_ONLY` · **δ_BW:** `UNSET`

## Scope and state model

Both states are explicit JSON objects. A proposition is identified by a canonical `proposition_id`; its semantic payload is not inferred from hidden activations.

```text
BELIEF_STATE = {
  propositions: [{ proposition_id, value, confidence, warrant_refs[], status }],
  snapshot_id, timestamp
}
WORLD_STATE = {
  propositions: [{ proposition_id, value, observation_refs[], status }],
  snapshot_id, timestamp
}
```

`value` is canonical JSON. `status ∈ {SUPPORTED, REFUTED, UNKNOWN}`. A warrant/reference is metadata, not proof that a proposition is true. An empty or unavailable reference set is explicitly observable.

### Metric A — Signed proposition disagreement (Jaccard-style)

Let `B` and `W` be the sets of canonical pairs `(proposition_id, value)` in belief and world. Define:

```text
d_set(B,W) = 1 - |B ∩ W| / |B ∪ W|,  if |B ∪ W| > 0
             0,                       if both sets are empty
```

Range: `[0,1]`. `0` means extensional equality of the inspected proposition/value sets; a positive value means at least one disagreement or omission. This is computable, model-independent, and insensitive to hidden model internals.

**Limitation:** equal content can still be epistemically invalid if the belief has no external warrant. Therefore this metric is never used alone for the collapse decision.

### Metric B — Warrant/observation separation loss

For each belief proposition `b`, define `w(b)=1` iff it has at least one valid, externally bound `warrant_ref` whose referent exists in the supplied observation registry and whose semantic role is `OBSERVATION`; otherwise `w(b)=0`. Define `o(w)=1` iff a world proposition has at least one observation reference with the same rule. Let `U = B_ids ∪ W_ids` and:

```text
d_warrant(B,W) = 1 - (sum over id in U of w(id)*o(id)) / max(1, |U|)
```

Range: `[0,1]`. It detects the epistemic distinction even when proposition content matches. A belief that merely repeats internal text, memory, self-consistency, or an unbound tool label has no valid external warrant under this definition.

**Required registry checks:** reference exists, hash/reference matches the snapshot, role is `OBSERVATION`, timestamp is within the declared validity window, and no `SELF_GENERATED` or `MEMORY_ONLY` role is accepted as an external observation.

### Optional Metric C — Provenance-path distance

On an explicit provenance graph, compute the shortest path from a belief node to a node with role `OBSERVATION`, after excluding self-generated and memory-only edges:

```text
d_path = shortest admissible edge count; ∞ if no admissible path exists
```

This is an ordered discrete value, not a substitute for semantic correctness. It is included as a diagnostic candidate; no operational threshold is assigned.

## Independence and combination rule

Metrics A and B are independent in the design sense: A inspects extensional proposition/value overlap; B inspects warrant/observation binding. Neither depends on an LLM family. A combined record MUST preserve both components and their provenance. The classifier is not permitted to average them into an invented universal distance.

## δ policy

`δ_BW` is a provisional calibration parameter only. No positive value is established by this document, the fixtures, or the thought experiments. Until an approved E1 calibration exists, all threshold fields remain `UNSET`; a classifier may still return `GAP_COLLAPSED` on structural violations such as missing warrant or belief-as-world relabelling.

## Canonicalization

1. Parse UTF-8 JSON.
2. Normalize proposition IDs and JSON values canonically.
3. Sort proposition arrays by `proposition_id` then canonical value.
4. Resolve references against the explicit registry.
5. Record metric version and input hashes.

A metric output without input hashes and registry status is non-auditable and MUST be treated as `UNKNOWN`, not as separation.
