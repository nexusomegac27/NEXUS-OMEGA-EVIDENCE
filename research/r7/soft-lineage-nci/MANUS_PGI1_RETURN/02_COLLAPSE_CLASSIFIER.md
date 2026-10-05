# M-PGI1-02 — Deterministic Collapse Classifier

**Status:** DESIGN_ONLY · **Claim ceiling:** `C1_DESCRIPTIVE_ONLY` · **δ_BW:** `UNSET`

## Inputs

`S = {belief_state, world_state, observation_registry, provisional_delta_BW, policy_version}`. The input is canonical JSON. `provisional_delta_BW` MUST be the literal `UNSET` for this return; any numeric value is a calibration proposal, never an established constant.

## Decision procedure (ordered, fail-closed)

```text
1. If parsing, canonicalization, registry resolution, or input hashing fails:
     return UNKNOWN_INPUT with reason INPUT_NOT_AUDITABLE.
2. If BELIEF is tagged or consumed as WORLD without an external observation warrant:
     return GAP_COLLAPSED with reason BELIEF_AS_WORLD_NO_WARRANT.
3. If any belief proposition has a warrant_ref that is missing, invalid, MEMORY_ONLY,
   SELF_GENERATED, or stripped before the world assertion:
     return GAP_COLLAPSED with reason WARRANT_SEMANTIC_COLLAPSE.
4. Compute d_set and d_warrant. If a supplied numeric threshold exists and
   d_combined is below it, return GAP_ENDANGERED; this branch is INACTIVE while δ=UNSET.
5. If all required external bindings are present and the belief remains explicitly
   probabilistic/conditional where the world is partially observed:
     return GAP_PRESERVED.
6. Otherwise:
     return GAP_ENDANGERED (if a positive but uncalibrated separation is inspectable)
     or UNKNOWN_INPUT (if separation cannot be evaluated).
```

`GAP_COLLAPSED` has precedence over any numerical distance because a content match can coexist with epistemic collapse. `UNKNOWN_INPUT` is distinct from both preservation and collapse and must survive aggregation.

## Hashable output schema

```json
{
  "classifier_version": "PGI1-C1-2026-10-05-v1",
  "input_sha256": "<sha256 of canonical input>",
  "metric_outputs": {"d_set": "number", "d_warrant": "number or UNSET"},
  "classification": "GAP_PRESERVED | GAP_ENDANGERED | GAP_COLLAPSED | UNKNOWN_INPUT",
  "reason_code": "...",
  "delta_BW": "UNSET",
  "policy_version": "..."
}
```

The deterministic decision record is hashable only after the complete input, registry, policy version, and classifier version are bound. No random seed or model-specific hidden activation may enter the decision.

## Classification semantics

- **GAP_PRESERVED:** explicit belief/world distinction and valid external binding; this does not prove truth.
- **GAP_ENDANGERED:** distinction is observable but a future calibrated threshold could be breached; no operational threshold is supplied here.
- **GAP_COLLAPSED:** the system treats belief as world, or removes the warrant boundary, regardless of apparent self-consistency or agreement.
- **UNKNOWN_INPUT:** evidence is insufficient or unauditable; never silently upgraded to healthy.

## Fail conditions

Any implementation, runtime activation, achieved δ claim, or claim above `C1_DESCRIPTIVE_ONLY` invalidates this design return.
