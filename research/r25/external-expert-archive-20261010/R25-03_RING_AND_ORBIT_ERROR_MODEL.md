# R25-03 · RING AND ORBIT ERROR MODEL
## Minimal Formalisation + Error Budget (Design-Only)

```text
OBJECT          = R25-03_RING_AND_ORBIT_ERROR_MODEL
CLAIM_CEILING   = C1_DESCRIPTIVE_ONLY
STATUS          = DESIGN_ONLY_NOT_EXECUTED
PARENT          = PR65_OPEN_HOLD_SCOPED + PR66
```

---

## 1. Domain of Validity

A 1-D continuous ring attractor is **appropriate** for a single circular state variable:

- animal heading / compass direction
- orbital true anomaly or argument of latitude (phase on [0, 2π))
- any other pure angular quantity with topology S¹

It is **not automatically appropriate** for:

- full 6-DOF orbital state (r, v)
- mixed Cartesian + angular representations without an explicit projection step
- quantities whose natural topology is R or R³

Any mapping from ring phase θ to a predicted orbital position must declare the projection and its Jacobian; otherwise the error analysis is incomplete.

---

## 2. Minimal Discrete Ring Model (Candidate)

State: N units on a circle, N ∈ {32, 64} (replication points).

```
θ_i = 2π i / N ,  i = 0 … N-1

r_i(t+1) = f( Σ_j W_ij r_j(t) − g_inhib · Σ_k r_k(t) + I_ext(θ,t) + ξ_i(t) )
```

- W_ij : local excitatory kernel (e.g. cosine or Gaussian of angular distance)
- g_inhib : global inhibition strength
- I_ext : external witness / sensory drive (0 when ingress is absent)
- ξ_i : noise process (to be specified; candidate: independent Gaussian or circular)
- f : saturating non-linearity (e.g. ReLU or sigmoid)

**Population-vector readout:**

```
θ̂ = atan2( Σ r_i sin θ_i , Σ r_i cos θ_i )
```

**Circular error against reference phase φ:**

```
d_circ(θ̂, φ) = |atan2( sin(θ̂−φ), cos(θ̂−φ) )|
```

### Explicit non-axioms

- Uniqueness of a single bump is **not** guaranteed by global inhibition alone. Multi-peak and oscillatory regimes exist.
- Persistence of a bump does **not** imply bounded error against an external truth source.
- “Shift without recreation” under external input is a testable hypothesis, not a derived theorem of the minimal model.

All of the above must be established (or refuted) by simulation under the preregistration matrix.

---

## 3. Error Budget Decomposition

Observed circular discrepancy after an open-loop interval T_out is a composite:

```
e_total(T_out) = f(
  e_source_epoch,      // age / quality of last TLE / OMM
  e_orbit_model,       // SGP4 / simplified dynamics residual
  e_clock,             // time synchronisation
  e_frame,             // coordinate / reference-frame mismatch
  e_observation,       // sensor / measurement noise of the external witness
  e_filter,            // internal ring / attractor drift
  e_numeric            // discretisation, integration, floating-point
)
```

These terms are in general **correlated**. An additive independent-error assumption is a modelling choice that must be justified or replaced by a joint covariance structure.

**Critical rule:** When ground truth is absent, only sensitivity analyses and relative model comparisons are admissible. Absolute statements of the form “the filter keeps the orbit within X km” are not scientifically warranted.

---

## 4. Separation of Concerns (mandatory)

| Quantity | Meaning | Allowed treatment |
|----------|---------|-------------------|
| `predicted_state` | Internal attractor / filter output | May evolve open-loop |
| `last_external_witness` | Last signed / timestamped external observation | Never overwritten by the filter |
| Unobserved interval | Pure prediction | Must be labelled as such |
| External correction | Application of a new witness | Must carry its own timestamp, uncertainty and provenance |

This dual-field discipline is the software analogue of the biological distinction between internal bump dynamics and sensory update.

---

## 5. Relation to Existing NA-1 / PR65

PR65 remains on **OPEN_HOLD_SCOPED** for precisely the reasons formalised above:

- Bump uniqueness is not guaranteed by max-inhibition alone.
- Dominance of filter-internal drift over SGP4/TLE error at 120 s has not been demonstrated with an empirical budget.
- Negative fixtures (multi-peak injection, high noise, unit ablation) are still required.

The present document supplies the minimal mathematical frame in which those fixtures can be interpreted. It does **not** lift the HOLD.

---

## 6. Alternative Baselines (must be compared)

Before any stronger claim for a ring implementation:

1. Pure angle-persistence (hold last θ̂)
2. Simple circular Kalman / von-Mises filter
3. Wrapped Gaussian process on the circle

A ring that does not outperform these baselines on the chosen circular metrics under matched noise and seed conditions has no demonstrated engineering advantage.

---

*GROK External Expert · Design-only · C1 · 2026-10-10*
