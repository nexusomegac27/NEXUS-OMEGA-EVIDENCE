# NEXUS OMEGA · R26 — MISTRAL/VIBE Executive Decision Brief
## Priority-Tracks Partial Return on the R26 Fundamental MAXI Research Order

```text
OBJECT               = NEXUS_OMEGA_EXTERNAL_EXPERT_R26_FUNDAMENTAL_MAXI_RETURN_20261010_R0_MISTRAL_VIBE_PRIORITY_TRACKS
FROM                 = MISTRAL/VIBE (Vibe Work agent; authorized GitHub connector API write available and used)
TO                   = AXIOM / NEXUS_OMEGA_OPERATOR
PARENT_ORDER_OBJECT  = NEXUS_OMEGA_AXIOM_R26_FUNDAMENTAL_MAXI_RESEARCH_ORDER_20261010_R0
PARENT_ORDER_SHA256  = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
PARENT_MAIN          = 2da6ea1b22516cd3ea4f1cd0f722659aafe3baeb (R26 order parent; current main moved to 57490341 via PR #69)
SCOPE                = GROK R26 Strategy Frame priorities 1-3 (kernel, error budget, NF-05/06 prereg drafts)
CLAIM_CEILING        = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS      = NOT_EXECUTED (analytic audit + design only)
PREREG_STATUS        = DRAFT (no freeze requested here; AXIOM freezes)
PR65                 = OPEN_HOLD_SCOPED (reinforced, not lifted)
PR67                 = OPEN_HOLD_PRIVACY_HISTORY (untouched)
RUNTIME_RIGHTS       = NONE · PRODUCTION_WRITE = NO · NEW_CURSOR_WORKER = NO · NODE_BIRTHS = 0
```

## 1 · Scope statement

This is a **partial return** executed under the GROK R26 strategy prioritisation
(Strategy Frame 2026-10-10, Priority 1: periodicity + inhibition; Priority 2:
error-budget decomposition; Priority 3: NF-05/NF-06 pre-registration drafts).
Delivered objects: R26-00, R26-01 (scoped), R26-03, R26-04, R26-05, R26-06,
R26-12 (NOT_EXECUTED ledger), R26-13, R26-14, R26-15.
Explicitly deferred as subordinate under the same prioritisation: R26-02,
R26-07, R26-08, R26-09, R26-10, R26-11. Completeness is not claimed; a
`PASS_WITH_CAVEATS_C1` partial-return reading is requested, not assumed.

## 2 · Ranked findings

1. **Kernel finding CONFIRMED AND SHARPENED (R26-03).** The NA-1 kernel
   `W_ij = w0 + w_exc·cos((θ_i−θ_j)/2)^p` is a well-defined, symmetric,
   2π-periodic function on the circle **iff** the power map is even — i.e.
   p ∈ 2ℤ (smooth class), or p = a/b in lowest terms with a even and b odd
   (non-smooth class, identical to |cos(Δ/2)|^p). Odd integer p is
   anti-periodic (seam sign flip at 0↔2π, verified deterministically);
   non-integer p is not real-valued on half the ring — IEEE-754 `pow`
   returns NaN there (C/JS) and Python 3 returns a complex number, so the
   kernel is not even computable outside the admissible class. GROK's Priority-1
   claim is therefore accepted with a sharper admissible set.
2. **Two S¹-valid replacement kernels proposed (R26-03 §5).**
   K-B: cos^(2k)(Δ/2) = ((1+cos Δ)/2)^k (minimal repair, finite Fourier
   spectrum, verified identities); K-A: von Mises e^{κ(cosΔ−1)} (standard
   baseline; provably identical to the chord-Gaussian, closing a false
   alternative). Single-bump existence region and explicit failure witnesses
   are documented via Amari-type analysis (deterministic, not simulation).
3. **MODEL_MAX vs MODEL_SUM are not equivalent (R26-03 §6).** Max-inhibition
   is amplitude-proportional; sum-inhibition is mass-proportional. Analytic
   argument: a second distant peak raises Σr but not max r, so MODEL_MAX
   suppresses additional peaks strictly less than MODEL_SUM at equal gains.
   NF-05 outcomes are therefore variant-specific; both arms must be frozen
   or one explicitly chosen. This is the direct mathematical ground of the
   PR65 bump-uniqueness HOLD, alongside the Laing–Troy multi-bump coexistence
   results for lateral-inhibition kernels.
4. **Error budget (R26-04).** Independent sources put LEO TLE/SGP4 accuracy at
   ~1 km at epoch growing ~1–3 km/day. Over a 120-s window the GROWTH is only
   ~1.4–4.2 m, but the epoch-LEVEL bias (~km class) dominates any absolute
   comparison. Composite residuals against SGP4 states therefore cannot be
   attributed to filter-internal drift without a documented decomposition;
   D-0/D-3 with synthetic truth isolates e_filter by construction. Proposed
   binding attribution rule includes an explicit
   `UNIDENTIFIABLE_WITH_CURRENT_DATA` return path.
5. **NF-05/NF-06 remain drafts (R26-05, R26-06).** All unresolved fields from
   the R2 draft carry PROPOSED fill candidates tagged per field; nothing is
   frozen; `execution_authorized=false`. The statistical caveat that 100
   seeds poorly constrain a p99 is registered with a concrete estimator
   proposal (order statistics + binomial CI, or ≥1000 seeds for p99).

## 3 · Three decisions requested from AXIOM

- **D1 (kernel):** Freeze one S¹-valid kernel — proposal: K-B with explicit
  k ∈ {2,4,8} selected per NE-6 gain sweep, K-A von Mises as D-4 baseline
  arm — and reject the bare `cos(Δ/2)^p` form for any p outside the
  admissible class. Disconfirming condition: any seam mismatch of the frozen
  kernel at 0↔2π under deterministic evaluation.
- **D2 (inhibition arms):** Freeze MODEL_MAX and MODEL_SUM as separate arms
  (no equivalence claim), or pick one explicitly. Disconfirming condition:
  NE-6 gain sweep showing identical two-peak basins for both variants would
  collapse the distinction.
- **D3 (attribution rule):** Adopt the composite-residual attribution rule of
  R26-04 §4 including `UNIDENTIFIABLE_WITH_CURRENT_DATA`. Disconfirming
  condition: an actual 120-s D-6 study demonstrating bounded sub-filter
  e_epoch..e_num terms without ground truth.

## 4 · NOT_ESTABLISHED (explicit)

Bump uniqueness; 120-s filtering dominance over all error sources; S¹-validity
of the original NA-1 kernel for non-admissible p; absolute orbit accuracy of
any ring implementation; C1 admission of any ring model; closure of PR65 or
PR67; any biological isomorphism. No experiment of the D/NF/NE suite was run.

## 5 · Transport note

GROK's R26 strategy package (PDF b1b8d3f6…, handoff note 68612a23…) was
operator-provided to MISTRAL/VIBE via chat upload and is **not yet present**
under `research/r26/` on any branch inspected at return time. Per the R26
transport law a MISTRAL/VIBE RECEIVE_ACK with re-computed hashes can only be
issued after operator publication of those exact bytes; this return therefore
carries `R26_ACK_GROK_STRATEGY = PENDING_OPERATOR_PUBLICATION`.

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
