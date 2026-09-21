# R5 active research

All R5 external-agent, exploratory, review, candidate-patch, and pre-integration material belongs below this directory under an explicit agent/topic lane.

## Binding lane rule

Every direct child directory of `research/r5/` must contain its own `README.md` stating purpose, source/provenance status, and integration status.

```text
research/r5/<agent-or-topic>/README.md = REQUIRED
```

No direct child lane is authoritative merely because it exists in Git.

## Current lanes

```text
research/r5/qwen-coder/
research/r5/axiom-platform-audit/
```

`qwen-coder/` preserves the historical delivery surfaces, records the independently rehashed local-original bindings, and provides the ordered landing zone for physical QWEN R5 returns.

`axiom-platform-audit/` contains public GitHub platform observations relevant to R5 and is not a substitute for QWEN return validation.

When an R5 result becomes integration-grade, derive stable artifacts into the mirrored `docs/r5`, `schema/r5`, `scripts/r5`, `tests/r5`, `validation/r5`, and `examples/r5` layers as applicable. Preserve research provenance; do not silently replace the original return.

- `astratis-x-r2-dtepn-meta/` — Astratis X/R2 DT-EPN and Meta package derivatives; explicit provenance gaps, R7 seal HOLD, no activation.
- `astratis-x-r3-synapse-protocol/` — Astratis X/R3 synapse-protocol prototype foundation; C1 only; crypto and token claims caveated; R4 not authorized; R7 seal HOLD.
