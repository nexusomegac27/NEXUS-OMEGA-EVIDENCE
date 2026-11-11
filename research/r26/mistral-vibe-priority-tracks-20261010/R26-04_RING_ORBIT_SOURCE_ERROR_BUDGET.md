# NEXUS OMEGA · R26 — Ring / Orbit Source Error Budget
## MISTRAL/VIBE deepening of GROK R26 Strategy Priority 2 · WP2 orbit boundary subset · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_RING_ORBIT_SOURCE_ERROR_BUDGET_20261010_R0
MAXI_MAPPING        = R26-04
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
R25_03_SHA256       = e7eabdf30eff378ea54766f1220fa7aa9b6f6ec634c72b9b10ccb411e8058b1b (verified byte-exact, 4811 B, PR67 head 1fcda32d)
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED (decomposition design + source review; no empirical campaign)
```

## 1 · Purpose

Formalise the decomposition `e_total` so that a composite residual — in
particular the 120-second residuals of the NA-1 D-protocol — cannot silently
be read as "filter drift". R25-03 §3 supplied the term list as design; this
document supplies the dependence structure, growth laws, and a binding
attribution rule proposal.

## 2 · Decomposition and dependence structure

```text
e_ext(t)  =  e_epoch(t) + e_model(t) + e_frame(t) + e_clock(t)
          +  e_obs(t)  + e_filter(t) + e_num(t)

e_ext² ≈ Σ_i e_i²  only under a declared independence assumption;
otherwise use the joint covariance structure. Declared correlations:
  (e_epoch, e_model): both driven by the TLE fit → strongly correlated
  (e_filter, e_num): correlated at the discretization floor (2π/N)
```

## 3 · Term-by-term budget with growth laws

| Term | Source | Growth law | Over a 120-s window | Measurability |
|---|---|---|---|---|
| e_epoch | TLE/OMM source-epoch age | ~1 km at epoch; +1–3 km/day for LEO (public SGP4-accuracy literature) | +1.4–4.2 m growth on top of a ~km-LEVEL, near-constant bias | needs fresher elements or independent truth |
| e_model | SGP4 force-model bias: zonals J2..J5 only, single B* drag coefficient, no lunisolar for short LEO arcs, WGS-72 constants, TEME pseudo-inertial output | secular, correlated with e_epoch | bias-like, slow | only vs independent higher-fidelity propagation |
| e_frame | TEME→ECEF convention (UT1–UTC, polar motion, frame naming) | near-constant over 10² s | constant offset | declared convention, documented transform |
| e_clock | filter time base vs element epoch | linear in window | small but declared | timestamp provenance |
| e_obs | external-witness sensor noise | white-ish | zero BY CONSTRUCTION in synthetic-truth tests | witness spec |
| e_filter | ring/attractor-internal drift — the D-0/D-3 target | diffusive component ∝√t (noise-induced; theory lower-bounds drift by the readout estimation accuracy), plus systematic drift field from connectivity/heterogeneity noise | THE quantity the D-grid measures | isolated only by synthetic truth (D-0/D-3) or isolated witness |
| e_num | discretization 2π/N (N=32: 11.25°; N=64: 5.625°), float64, integrator order | bounded, quasi-static | bin floor | declared numerics |

Independent source anchors for the SGP4/TLE rows: standard references put
LEO propagation error near ~1 km at epoch degrading ~1–3 km/day; errors are
minimum near the fitted epoch and grow away from it due to the truncated
analytic model; km-class accuracy is typical for week-scale predictions
compared to high-precision ephemerides (Vallado-class analyses,
differentiable-programming SGP4-gap studies 2024, operator Q&A archives).
This CONFIRMS the prior chain finding that TLE/SGP4 error grows over days,
not over 120 s — for the GROWTH component.

## 4 · Binding attribution rule (proposed for the freeze)

```text
RULE R26-EB1: A composite residual r(t0..t0+T_out) against SGP4-propagated
states may be attributed to e_filter ONLY IF every other term is bounded
above, with documented margins, strictly below |r| over the same window.
OTHERWISE: return UNIDENTIFIABLE_WITH_CURRENT_DATA (D-6 outcome class).
RULE R26-EB2: D-0/D-3 (I_ext = 0, synthetic truth) isolate e_filter + e_num
by construction (e_epoch = e_model = e_frame = e_clock = e_obs = 0);
they are the only admissible drift evidence for the bound.
RULE R26-EB3: No absolute-accuracy statement ("keeps the orbit within X km")
is admissible without external ground truth (R25-03 §3, carried forward).
RULE R26-EB4: GROWTH vs LEVEL distinction is mandatory in every D-6 report:
over 120 s the epoch-age GROWTH is metres, but the epoch LEVEL (~km class)
still dominates any absolute comparison; "SGP4 error is negligible at 120 s"
is true only for the growth term, never for the level.
```

## 5 · Consequences for NA-1 D-3 / D-6

- D-3 (120-s drift ≤ 1 bin mean, ≤ 3 bins p99) is a FILTER-INTERNAL criterion
  on synthetic truth; it neither implies nor is implied by any external-state
  accuracy.
- D-6 becomes a genuine attribution study: it must document e_epoch..e_num
  bounds from the element source (OMM/TLE epoch age, B* caveat, frame and
  time conventions), or declare UNIDENTIFIABLE_WITH_CURRENT_DATA. The
  original NA-1 assumption that the SGP4 share is "small" at 120 s is
  CONFIRMED only for the growth component and remains UNPROVEN for the
  composite level without an independent reference.

## 6 · Negative evidence and falsifiers

1. If a fresh-epoch LEO TLE shows metre-class absolute truth error (vs
   independent high-precision ephemeris), the ~km level claim is falsified.
2. If D-0/D-3 synthetic-truth drift differs materially from an
   equal-window SGP4-composite residual after R26-EB1 decomposition, the
   isolation claim of D-0/D-3 is falsified.
3. If e_clock/e_frame terms are shown negligible to <1e-3 of |r| for the
   chosen element source, their mandatory documentation can be lightened —
   that would be positive simplification knowledge.

## 7 · Status grammar

```text
R26_04_ERROR_BUDGET       = ISSUED_DESIGN_ONLY
EPOCH_LEVEL_DOMINANCE     = DOCUMENTED (km-class bias at 120 s)
EPOCH_GROWTH_120S         = ~1.4–4.2 m (1–3 km/day sources)
ATTRIBUTION_RULES          = R26-EB1..EB4 PROPOSED_FOR_FREEZE
UNIDENTIFIABLE_PATH        = DEFINED
ABSOLUTE_ACCURACY_CLAIMS   = NOT_WARRANTED_WITHOUT_GROUND_TRUTH
CLAIM_CEILING              = C1_DESCRIPTIVE_ONLY
EXPERIMENTS                 = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
