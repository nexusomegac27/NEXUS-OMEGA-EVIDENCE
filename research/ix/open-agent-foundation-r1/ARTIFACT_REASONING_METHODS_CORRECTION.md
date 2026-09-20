# Artifact reasoning methods — scientific correction

The R1 source bundle proposes Feynman-style explanation, mind mapping and Zettelkasten organization
as a combined artifact-systematics layer. The organizational intent is useful, but its scientific
status must be narrowed.

## Self-explanation / “Feynman” heuristic

Explaining a mechanism in simple language can expose missing assumptions, unclear dependencies and
unexplained code paths. Research on self-explanation and explanatory questioning supports learning
benefits in some settings.

NEXUS classification:

```text
SELF_EXPLANATION = REVIEW_HEURISTIC
SELF_EXPLANATION != VALIDATION
SIMPLE_EXPLANATION != CORRECT_EXPLANATION
```

A Feynman-style pass may generate `FEYNMAN_GAP` objects. Those gaps become test/falsification
targets; they do not become evidence by being articulated clearly.

## Mind/graph mapping

Graphical or textual concept maps can help expose structure and dependencies. Effects reported in
education literature are domain/task dependent.

The R0 source's “both hemispheres” rationale is rejected. Modern neuroscience does not support the
popular dichotomy that broad cognitive/creative tasks can be assigned to a dominant left/right
hemisphere in that simplified way.

NEXUS classification:

```text
GRAPH_MAPPING = STRUCTURING_HEURISTIC
VISUAL_STRUCTURE != SCIENTIFIC_VALIDITY
LEFT_RIGHT_BRAIN_ACTIVATION_CLAIM = REJECTED
```

## Zettelkasten-style linked atomic notes

The useful element for NEXUS is information architecture:

- one bounded idea/object;
- stable identifier;
- explicit parent/related/contradicts/supersedes edges;
- immutable/correctable history;
- discoverable negative knowledge.

NEXUS classification:

```text
ATOMIC_LINKED_NOTES = INFORMATION_ARCHITECTURE_PATTERN
ZETTELKASTEN != SCIENTIFIC_VALIDATION_METHOD
```

## Combined R1 operational pattern

Allowed:

```text
STRUCTURE
→ EXPLAIN
→ IDENTIFY_GAPS
→ LINK_TO_EVIDENCE
→ TEST/FALSIFY
→ HASH/BIND
```

Not allowed:

```text
EXPLAIN_WELL
→ CLAIM_TRUE
```

## “Humility score”

The source refers to a Humility-Score. No scientific metric is established by the supplied R1
materials. Until an operational definition, measurement model, calibration and falsification
protocol exist:

```text
HUMILITY_SCORE = NOT_ESTABLISHED_AS_SCIENTIFIC_METRIC
```

Uncertainty/caveat counts may instead be reported directly without collapsing them into a scalar.
