# NEXUS OMEGA · R26 — Periodic Ring Kernel and Stability Audit — R1 (versioned correction)

## MISTRAL/VIBE · supersedes R26-03 R0 · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_20261010_R1
SUPERSEDES          = R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT.md (R0)
SUPERSEDED_R0_SHA256    = 8ef2bef21d98880bf56836bc76ffc237d9d9b78de77a0f5660091866884ee889
SUPERSEDED_R0_BLOB_SHA1 = 0bdcb6e8faacc2203c8970e4736ac371e5800421
CORRECTION_TRIGGER  = AXIOM PR #70 scoped adjudication (issuecomment 6102162009), findings 1-3;
                      supported by operator-uploaded R33 computer crossvalidation (AXIOM-reported
                      original sha256 b6354b484354a406500f444db3f247c4f0d3690a736e4890d946b39dbde2f3a1)
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
NA1_SPEC_SHA256     = 6b2bda7e700bf219fc9e7609da7d60b6c4079b0766caf51bb5d82629f31c4c11 (PR65 head 17e0a327)
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED (deterministic analytic/numeric evaluation only; no simulation, no seeds, no D/NF/NE experiment)
REPO_LAW            = corrections append; R0 remains unmodified as historical record (AGENTS.md rule 5)
```

## 1 · Scope of this correction

Retained from R0, unchanged in force: the Amari-type witnesses W1-W4, the wrap-fixture mandate,
the K-A von-Mises baseline (including the chord-Gaussian identity), the Poisson optional arm,
the seam/NaN falsifiers, and the requirement that MODEL_MAX and MODEL_SUM be frozen separately.

Corrected here per the AXIOM adjudication:

| R0 location | Defect (AXIOM finding) | Correction |
|---|---|---|
| §2 vs §3 | wrapped and unwrapped kernel conflated | §2 below: explicit dual definition, corrected admissibility per function |
| §5 "Mode dominance … decreasing in k" | direction wrong: R'(k) = +3/(k+2)^2 > 0 | §4: strictly increasing; inference re-evaluated |
| §7 "m = 2 suppression ratio … improves with k" | same error; associated inference wrong | §4: both margins strictly decrease in k |
| §6 "strictly larger parameter region under MAX" | unproven containment relation | §5: downgraded to registered HYPOTHESIS |

## 2 · Corrected kernel definitions (two distinct functions)

R0 §2 defined Δ = wrap(θ_i − θ_j) ∈ (−π, π] and then argued from cos((Δ+2π)/2)^p on an unwrapped
domain. Those are two DIFFERENT functions. R1 defines both explicitly and scopes every
statement to exactly one of them.

```text
K_bare_p(x) = cos(x/2)^p              literal evaluation on the given representative (R0 §2 target)
K_wrap_p(x) = cos(wrap(x)/2)^p        wrap-before-power (R0 §3 discipline)
            = ((1 + cos x)/2)^(p/2)    closed form (identity verified deterministically)
            = |cos(x/2)|^p             equivalent absolute-value form
wrap(x) = atan2(sin x, cos x) ∈ (−π, π]
```

Deterministic witness table (IEEE-754 double semantics, pow fail-closed):

| x (rad) | wrap(x) | K_wrap(1.5) | K_bare(1.5) | K_wrap(1) | K_bare(1) |
|---|---|---|---|---|---|
| 4 | −2.2832 | 0.268454 | NaN | +0.416147 | −0.416147 |
| 5 | −1.2832 | 0.717077 | NaN | +0.801144 | −0.801144 |
| 6.5 | +0.2168 | 0.991207 | NaN | +0.994130 | −0.994130 |
| 7 | +0.7168 | 0.906216 | NaN | +0.936457 | −0.936457 |

**(T1) K_bare_p (R0 §2 theorem — RETAINED, now correctly scoped).** As a function of the
representative, K_bare_p is 2π-periodic iff the power map x ↦ x^p is even: p ∈ 2ℤ (smooth class)
or p = a/b in lowest terms with a even, b odd (then K_bare = |cos(x/2)|^p on the fundamental
domain, non-smooth at x = π); odd integer p is anti-periodic (deterministic witness:
K_bare_1(2π−ε) = −1 vs K_bare_1(ε) = +1); all other p are not real-valued on half the
circle (IEEE pow(−0.416147, 1.5) = NaN, verified). This theorem is TRUE for K_bare only.

**(T2) K_wrap_p (corrected statement — R0's categorical claim does NOT transfer).** For EVERY
real p > 0, K_wrap_p is real, finite, continuous, symmetric, and 2π-periodic (verified: max
periodicity deviation ≤ 3.3e-16 over a 6π grid for p ∈ {0.5, 1, 1.5, 2, 2.4, 3}; seam deviation
at 0↔2π exactly 0). Smoothness is the actual discriminator:
- K_wrap_p ∈ C^m(S¹) iff m < p (verified: p = 1 derivative jump −½ → +½ at the antipode;
  p = 1.5 is C¹ but not C²; p = 2 is C^∞);
- K_wrap_p ∈ C^∞(S¹) iff p ∈ 2ℤ — exactly the K_B class, K_wrap_2k = K_B = ((1+cos Δ)/2)^k.

**(T3) Fourier discipline corrected (R0 §4, scoped).** The half-integer "mode m = 1/2"
argument applies to K_bare (a 4π-periodic function of the representative). K_wrap_p is a
genuine 2π-periodic function with INTEGER modes for every p > 0 (witness p = 1, |cos(x/2)|:
cosine coefficients a0 ≈ 0.63662 = 2/π, a1 ≈ 0.424413, a2 ≈ −0.084883, a3 ≈ 0.036378 —
computed, no half-integer content).

**(T4) Historical NA-1 verdict, conditionalized.** R0 §9 called NA-1 with non-admissible p
"invalid as stated". Corrected: the NA-1 spec expression cos((θ_i−θ_j)/2)^p does not declare
its evaluation discipline, and the two readings diverge materially:
- bare reading: R0 verdict stands (NaN / anti-periodic / undefined weights);
- wrap reading: the computed kernel is |cos(Δ/2)|^p — well-defined, with smoothness class
  per p (C^m for m < p; C^∞ only for p ∈ 2ℤ).
The defect is the UNDECLARED semantics itself. Historical NA-1 results are therefore not
"valid as stated" under either reading without an implementation audit, which this R1 does
not perform (no historical runtime was inspected).

## 3 · D1 freeze declaration requirements (per AXIOM finding 1)

The kernel freeze must name, explicitly and before any NF-05/NF-06 execution:

1. FUNCTION: K_wrap_p with declared p, or directly K_B (p = 2k). Recommended: K_B, because
   it is the unique C^∞ subclass of the wrapped family and admits the closed Fourier
   spectrum used in the mode analysis.
2. WRAP CONVENTION: wrap(x) = atan2(sin x, cos x) ∈ (−π, π], applied BEFORE the power.
3. ENDPOINT CONVENTIONS: Δ = π admissible; K_wrap_p(π) = 0 for p > 0; 0↔2π seam fixture
   mandatory (NE-5).
4. SMOOTHNESS REQUIREMENT: declare C^∞ (then p ∈ 2ℤ only) or a finite m (then p > m,
   with documented antipode behaviour); undeclared smoothness is not free.
5. NORMALIZATION: K(0) = 1; excitation mass M_k = 2π·C(2k,k)/4^k declared per k and
   carried into w_exc/g_inhib per arm.
6. TESTED SOFTWARE SEMANTICS: IEEE-754 pow, fail-closed (NaN on negative base with
   non-integer p). Mandatory unit fixture: pow(cos(2), 1.5) must equal NaN (deterministic).
7. HISTORICAL MAPPING: p ↔ k = p/2 valid only for even integer p; all other historical
   exponents map to nothing until the implementation discipline is audited.

K_A (von Mises, identical to chord-Gaussian) remains the D-4 baseline candidate unchanged.

## 4 · Corrected mode-ratio analysis (per AXIOM finding 2)

Convention: K_B(Δ) = Σ_m c_m e^{imΔ} with c_m = C(2k, k+m)/4^k for |m| ≤ k, else 0
(cosine-series coefficient a_m = 2·c_m; ratios are convention-free; spectrum verified
numerically to ≤1e-7).

**Formula CONFIRMED:** c_2/c_1 = C(2k,k+2)/C(2k,k+1) = (k−1)/(k+2).

**Direction CORRECTED:** R(k) = (k−1)/(k+2) is strictly INCREASING in k
(R'(k) = 3/(k+2)^2 > 0), with lim R = 1. R0's "decreasing in k" and "improves with k"
are false and withdrawn.

| k | c_1 | c_2 | R = c_2/c_1 | relative margin 1−R = 3/(k+2) | absolute margin c_1−c_2 |
|---|---|---|---|---|---|
| 2 | 0.250000 | 0.062500 | 0.250 | 0.750 | 0.187500 |
| 4 | 0.218750 | 0.109375 | 0.500 | 0.500 | 0.109375 |
| 8 | 0.174561 | 0.122192 | 0.700 | 0.300 | 0.052368 |
| 16 | 0.131718 | 0.109765 | 0.8333 | 0.1667 | 0.021953 |
| 32 | 0.096336 | 0.087836 | 0.9118 | 0.0882 | 0.008500 |

**Corrected inference (replaces both R0 §5 and §7 claims).** Under DC-cancelling uniform
inhibition, mode m destabilises first for the largest c_m. Mode 1 remains the first
unstable mode for every k ≥ 1 (R < 1 always), BUT both separation margins between the
m = 1 and m = 2 onsets — relative (3/(k+2)) and absolute (c_1 − c_2) — strictly DECREASE
in k. Sharper kernels (larger k) therefore make single-bump selection at onset MORE
fragile, not cleaner. R0's contrary stability-mode inference is withdrawn. A rising
second-to-first ratio is evidence AGAINST improved mode separation; it does not
automatically prove anything about bump selection beyond onset, which remains governed by
the non-exclusion of multi-bump coexistence (Laing-Troy-type families; NF-05 mandatory).

**Design consequence for D1:** the k-choice is a genuine trade-off — width σ ≈ √(2/k)
improves with k, while mode-separation margin and excitation mass (~2√(π/k)) degrade
with k. k must be selected with both sides on the table (NE-6 sweep), not from the
withdrawn "sharper is cleaner" inference.

## 5 · MODEL_MAX vs MODEL_SUM: claim downgraded to HYPOTHESIS (per AXIOM finding 3)

The R0 §6 heuristic (a second, smaller, distant peak raises Σ_k r_k but not max_j r_j,
so MAX should suppress additional peaks less) is RETAINED AS MOTIVATION ONLY. The claim
that "MODEL_MAX admits stable multi-peak states over a strictly larger parameter region
at identical gains" is NOT established: it is a statement about the fixed-point set and
its stability of two different nonlinear recurrences, and no proof was given —
normalisation across arms (g_inhib scaling vs. activity coupling), thresholds, total
activity, and the full stability Jacobian are missing. "Identical (w0, w_exc, g_inhib)"
is not an identified equal-inhibition comparison between a max-coupled and a sum-coupled
system. Reclassified: REGISTERED_HYPOTHESIS, to be tested only by a matched parameter
sweep with an explicit normalisation choice (NE-6), arms frozen separately in all cases.

## 6 · Pointers to R26-05/R26-06 (AXIOM finding 6, scoped note)

R26-05's kernel field (K_B with p = 2k) is unaffected by the dual-definition correction
(p = 2k is the unique class where bare and wrapped readings coincide). R26-05/R26-06
remain DRAFT, not frozen, and now additionally depend on the D1 declaration fields of §3
above (wrap convention, smoothness requirement, endpoint conventions, software semantics).
D-3 thresholds apply at 120 s only; the p99-from-100-seeds caveat stands; the STALE
detector lane (NE-8) remains strictly separate from drift measurement. No content change
to R26-05/R26-06 is made by this R1.

## 7 · Updated negative evidence and falsifiers

1. Seam: any frozen S¹-kernel showing a 0↔2π mismatch under deterministic evaluation
   falsifies §2/T2 for that kernel.
2. Semantics: an implementation returning real weights for K_bare with non-integer p on
   negative base falsifies T1's computational clause.
3. Ratio: if c_2/c_1 ≠ (k−1)/(k+2) for any k, or the computed ratio is non-increasing
   in k over k ∈ {2,4,8,16,32}, §4 is falsified.
4. Margin: if 1−R(k) = 3/(k+2) fails to decrease in k, the fragility claim is falsified.
5. Hypothesis: NE-6 showing MODEL_SUM admitting two-peak states at strictly smaller
   matched normalised gains than MODEL_MAX falsifies the §5 hypothesis (that result
   would itself be positive negative-knowledge).
6. Smoothness: if K_wrap_1 exhibits a continuous first derivative at Δ = π, T2 is
   falsified (deterministic witness says it does not: jump −½ → +½).

## 8 · Status grammar

```text
R26_03_R1_STATUS             = ISSUED_CORRECTED_DESIGN_ONLY
R26_03_R0                    = SUPERSEDED_PRESERVED (append-only; historical record)
KERNEL_FUNCTION_DISCIPLINE   = DUAL_DEFINITION_MANDATORY (K_bare vs K_wrap)
K_WRAP_WELL_DEFINED          = ALL_REAL_P_GT_0
K_WRAP_SMOOTH_CLASS          = P_IN_2Z_ONLY (= K_B)
K_BARE_ADMISSIBLE_CLASS      = UNCHANGED (R0 §2 theorem retained, scoped to K_bare)
MODE_RATIO_DIRECTION         = STRICTLY_INCREASING R'(k) = 3/(k+2)^2 > 0
MODE_SEPARATION_MARGIN       = 3/(k+2) DECREASING_IN_k (single-bump onset more fragile with k)
MAX_VS_SUM_REGION_CLAIM      = DOWNGRADED_TO_HYPOTHESIS (NE-6 with matched normalisation)
D1_FREEZE_FIELDS             = FUNCTION/WRAP/ENDPOINTS/SMOOTHNESS/NORMALIZATION/SOFTWARE_SEMANTICS/HISTORY
CLAIM_CEILING                = C1_DESCRIPTIVE_ONLY
EXPERIMENTS                  = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
