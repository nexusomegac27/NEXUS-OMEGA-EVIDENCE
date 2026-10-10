# NEXUS OMEGA · R26 — Ring / Orbit Source Error Budget — R1 (versioned correction)

## MISTRAL/VIBE · supersedes R26-04 R0 · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_RING_ORBIT_SOURCE_ERROR_BUDGET_20261010_R1
SUPERSEDES          = R26-04_RING_ORBIT_SOURCE_ERROR_BUDGET.md (R0)
SUPERSEDED_R0_SHA256    = 8a7b3b32e477129f5f224896e266a9d478f223eb1c39fce752b1ccae585ee501
SUPERSEDED_R0_BLOB_SHA1 = ec5214689dfe3d3754a13872a8d8efb40f74ee35
CORRECTION_TRIGGER  = AXIOM PR #70 scoped adjudication (issuecomment 6102162009), findings 4-5
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
R25_03_SHA256       = e7eabdf30eff378ea54766f1220fa7aa9b6f6ec634c72b9b10ccb411e8058b1b
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED (decomposition design + rule correction; no empirical campaign)
REPO_LAW            = corrections append; R0 remains unmodified as historical record (AGENTS.md rule 5)
```

## 1 · Scope of this correction

Retained from R0: the seven-term decomposition e_total = e_epoch + e_model + e_frame +
e_clock + e_obs + e_filter + e_num, the declared correlation notes, the GROWTH-vs-LEVEL
reporting discipline (EB4), EB3 (no absolute accuracy without ground truth), and the
UNIDENTIFIABLE outcome class. Corrected here: EB1 (logically invalid as worded — AXIOM
finding 4) and the evidential status of the SGP4 numeric rows (AXIOM finding 5). EB2
receives an explicit scope caveat.

## 2 · Corrected attribution rule (EB1 replaced)

**Defect of R26-EB1 (R0):** "every other term individually < |r| ⇒ attribute r to
e_filter" is logically invalid — several individually smaller terms can jointly explain
the residual, and correlations/cancellations add further ambiguity.

**Deterministic counterexample (arithmetic, no data claimed):** r = 10 m, e_epoch = 6 m,
e_model = 5 m, others 0. Each non-filter term is individually < 10 (EB1-R0 satisfied
⇒ false attribution), yet the worst-case joint bound is 6 + 5 = 11 m > 10 m: the residual
is fully explicable without the filter. The RSS bound √(36+25) ≈ 7.81 m < 10 m is NOT
admissible without justification, because e_epoch and e_model are declared correlated
(both driven by the same TLE fit) — aligned worst-case is the defensible reading.

```text
RULE R26-EB1' (proposed replacement):
A composite residual r(t0..t0+T_out) against SGP4-propagated states may be attributed
to e_filter ONLY IF a JOINT bound over ALL non-filter terms is documented strictly
below |r| with margin, where the joint bound is EITHER
  (a) worst-case aligned sum  B_wc = Σ_{i≠filter} |e_i|_upper   (no independence assumed), OR
  (b) a declared joint covariance bound (e.g. RSS with explicit cross-covariance terms),
      admissible ONLY with a written independence/correlation justification,
AND the identifiability caveat is stated (residuals consistent with filter-drift
signatures do not prove attribution; cancellation can mask large components).
INDIVIDUAL per-term bounds below |r| are necessary but NOT sufficient.
OTHERWISE: return UNIDENTIFIABLE_WITH_CURRENT_DATA (D-6 outcome class).
```

**EB2 scope caveat (explicit):** D-0/D-3 synthetic-truth runs isolate e_filter + e_num
BY EXPERIMENTAL CONSTRUCTION ONLY — they assume the imposed truth is independent, units
are correct, and numerics are bounded. They are admissible drift evidence for the bound
within that construction and prove nothing about external-state accuracy.

**EB3, EB4: retained unchanged.**

## 3 · Evidential status of the SGP4 numeric rows (downgraded)

The "1–3 km/day LEO growth" and "~1 km at epoch" entries are GENERIC PUBLIC-LITERATURE
accuracy classes, not source-exact, object-specific data. The derived 120-s figures
(1–3 km/day → 1.39–4.17 m; arithmetic verified) are CONDITIONAL linear extrapolations
of those assumed rates, not a measured budget for any actual object. R0's phrasing is
therefore downgraded: no universal km-level dominance and no SGP4 smallness for the
target application follow from this arithmetic. Per-object D-6 must measure or bound
e_epoch/e_model from the actual element source (OMM/TLE epoch age, B* caveat, frame and
time conventions) or return UNIDENTIFIABLE_WITH_CURRENT_DATA. The GROWTH-vs-LEVEL
distinction survives as a REPORTING discipline (EB4): over 120 s the growth term of an
assumed 1–3 km/day rate is metre-class, while any epoch-LEVEL bias is a separate,
independently bounded quantity — neither dominance direction is established without
per-object bounds.

## 4 · Consequences for D-3 / D-6

- D-3 (120-s drift ≤ 1 bin mean, ≤ 3 bins p99): filter-internal criterion on synthetic
  truth; thresholds apply at 120 s ONLY; p99 from 100 seeds remains a wide-CI estimate
  (order statistics + binomial CI, or ≥ 1000 seeds).
- D-6: genuine attribution study under EB1' with joint bounds; STALE-detector lane
  (NE-8) strictly separate from drift measurement.

## 5 · Updated negative evidence and falsifiers

1. If a fresh-epoch LEO TLE shows metre-class absolute truth error vs an independent
   high-precision ephemeris, the generic km-class level reading is falsified for that
   object class.
2. If a documented case exists where all per-term individual bounds hold, yet the joint
   worst-case bound exceeds |r| AND the residual is nevertheless provably filter drift
   (by synthetic truth), EB1' is too strict — positive knowledge.
3. If D-0/D-3 synthetic-truth drift differs materially from an equal-window
   SGP4-composite residual after EB1' decomposition, the isolation claim of D-0/D-3
   is falsified.

## 6 · Status grammar

```text
R26_04_R1_STATUS        = ISSUED_CORRECTED_DESIGN_ONLY
R26_04_R0               = SUPERSEDED_PRESERVED (append-only; historical record)
EB1_R0                  = REJECTED_AS_WORDED (AXIOM) — logically invalid, replaced
EB1_PRIME               = PROPOSED (joint bound: worst-case sum OR justified covariance)
EB2                     = RETAINED_WITH_SCOPE_CAVEAT (isolation by construction only)
EB3_EB4                 = RETAINED_UNCHANGED
SGP4_NUMERIC_ROWS       = GENERIC_LITERATURE_CLASS_CONDITIONAL_ARITHMETIC
UNIDENTIFIABLE_PATH     = DEFINED (primary EB1' failure class)
CLAIM_CEILING           = C1_DESCRIPTIVE_ONLY
EXPERIMENTS             = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
