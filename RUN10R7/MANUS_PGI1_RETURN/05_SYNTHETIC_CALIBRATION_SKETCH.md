# M-PGI1-05 — Synthetic E1 Calibration Sketch

**Status:** PROPOSED, NOT EXECUTED · **Claim ceiling:** `C1_DESCRIPTIVE_ONLY` · **δ_BW:** `UNSET`

## Objective

Construct a synthetic, fully observable benchmark in which the overlap between BELIEF_STATE and WORLD_STATE is controlled by the generator. The protocol is a design precursor only; it produces no result here and cannot establish a positive operational δ.

## Protocol

1. Generate a finite world proposition universe with known truth values, observation references, validity windows, and partial-observability masks.
2. Generate belief snapshots at overlap levels `0, 0.1, …, 1.0` using controlled mutations: omission, contradiction, value substitution, warrant removal, memory promotion, and referent swap.
3. For each snapshot compute Metric A, Metric B, and optional path diagnostic from canonical JSON only.
4. Randomize fixture order, but bind the generator seed in the receipt; use separate calibration and hold-out sets.
5. Test monotonicity: increasing overlap or removing warrant must move the relevant metric in the prespecified direction. Non-monotonic behavior is a design failure, not a license to tune δ.
6. Test robustness across proposition cardinality, duplicate representations, missing observations, timestamp boundaries, and unknown values.
7. Score classification against generator ground truth with TP, FP, TN, FN, UNKNOWN-preservation rate, and Wilson intervals.
8. Only after independent review may a candidate lower-bound interval be reported as a **proposal**. It must remain `δ_BW=UNSET` for operational use until a separate authorization promotes it.

## Required outputs of a future run

`generator_version`, `seed`, input fixture hashes, metric version, classifier version, per-fixture outputs, monotonicity report, robustness report, confusion matrices, and an explicit statement that no δ has been established.

## Falsifiers

- Metric values do not respond monotonically to controlled overlap.
- Positive and negative fixtures become indistinguishable under a stated representation.
- Missing/unknown evidence is silently classified as preserved.
- Results depend on hidden model activations or an unbound random seed.
- A proposed candidate is reported as an achieved operational guarantee.

No execution, calibration, implementation, or live-system write is performed by this return.
