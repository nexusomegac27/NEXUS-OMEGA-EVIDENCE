# NEXUS OMEGA · R26 — Ring / Orbit Source Error Budget — R2 Precision Annotation (EB1′ limits)

## MISTRAL/VIBE · annotates R26-04_R1 (non-destructive; R1 remains in force) · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_ERROR_BUDGET_EB1PRIME_LIMITS_ANNOTATION_20261010_R2
ANNOTATES           = R26-04_RING_ORBIT_SOURCE_ERROR_BUDGET_R1.md (sha256 2b2fe0845fe88459894c25712213ed7874761ce367393a9aeeca153859fda275, blob 77b4d8b88e617b018e79fa063b07b77dcbcf48a8)
DOES_NOT_SUPERSEDE  = R26-04_R1 (R1 rule text unchanged; this annotation encodes the formal limits)
TRIGGER             = AXIOM R1 adjudication (PR #72 merged, adjudication sha256 5bad43e76f80be29e25c4cb21d194b8f272bec6db9d63aba7a4b921264b980cc,
                     sections 2D and 5.2: EB1′ identifiability limits must be encoded before D1/D3 prereg freezing)
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED (deterministic arithmetic witnesses only)
REPO_LAW            = corrections append; R26-04_R1 and R0 remain unmodified (AGENTS.md rule 5)
```

## 1 · EB1′ is a necessary screen, formally

Under a deterministic, exhaustive, same-coordinate error model r = f + u with a joint
norm bound ‖u‖ ≤ B, the reverse triangle inequality gives ‖f‖ ≥ max(0, ‖r‖ − B).
Hence B < ‖r‖ guarantees only a NONZERO minimum residual component in f under the
model — a necessary condition, NOT sufficient for filter dominance or causal
attribution. Dominance over the other terms would additionally require
‖r‖ > 2B under the same exhaustive-model assumptions (design illustration, not
empirical proof). EB1′ is therefore carried as a conservative fail-closed screen /
necessary condition only, exactly as adjudicated (D3: ACCEPT_NECESSARY_SCREEN_ONLY).

## 2 · Covariance envelopes are not deterministic bounds

A covariance matrix by itself does not substitute for a worst-case bound. A probabilistic
envelope may replace B only with declared: distribution/tail assumptions, confidence
level, dependency structure, coordinate frame, and common units. Angular ring error,
cartesian orbit-position error and external witness uncertainty may not be normed
together without a declared projection/Jacobian.

## 3 · Identifiability of joint components (formalised)

Deterministic non-uniqueness witness (arithmetic, no data claimed): observed residual
r = 10 m; declared per-term upper bounds 9 m for every non-filter term. Two decompositions:

| Component | A (m) | B (m) |
|---|---|---|
| e_epoch | 8.0 | 2.0 |
| e_model | 1.5 | 7.0 |
| e_frame | 0.3 | 0.6 |
| e_clock | 0.1 | 0.2 |
| e_num | 0.1 | 0.2 |
| e_filter | 0.0 | 0.0 |
| sum | 10.0 | 10.0 |

Both satisfy every individual bound, both sum exactly to r, and the attributions differ
materially — the component decomposition is NOT identifiable from the residual alone.
Identification requires one of: synthetic truth (D-0/D-3, by construction), an external
independent reference, or declared structure (correlation matrix plus per-component
spectral/parametric signatures, e.g. bias-like vs √t-diffusive). Otherwise the verdict
is UNIDENTIFIABLE_WITH_CURRENT_DATA.

## 4 · Freeze guards

- D3 carried: EB1′ = conservative screen / necessary condition;
  FULL_CAUSAL_ATTRIBUTION_FREEZE = NO.
- D-6 must document B (worst-case aligned sum, no independence assumed) or a fully
  declared probabilistic envelope, plus the identifiability route used (construction /
  external reference / declared structure), or return UNIDENTIFIABLE_WITH_CURRENT_DATA.

## 5 · Status grammar

```text
R26_04_R2_STATUS            = ISSUED_PRECISION_ANNOTATION_DESIGN_ONLY
R26_04_R1                   = IN_FORCE_UNCHANGED (annotated, not superseded)
EB1_PRIME_STATUS            = NECESSARY_CONDITION_NOT_SUFFICIENT (reverse-triangle bound)
DOMINANCE_ILLUSTRATION       = ||r|| > 2B (design bound only, exhaustive-model assumption)
COVARIANCE_ENVELOPE         = NOT_A_BOUND_WITHOUT_DECLARED_ASSUMPTIONS
JOINT_IDENTIFIABILITY       = NOT_IDENTIFIABLE_FROM_RESIDUAL_ALONE (witness table)
IDENTIFICATION_ROUTES       = SYNTHETIC_TRUTH | EXTERNAL_REFERENCE | DECLARED_STRUCTURE | UNIDENTIFIABLE
CLAIM_CEILING               = C1_DESCRIPTIVE_ONLY
EXPERIMENTS                 = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
