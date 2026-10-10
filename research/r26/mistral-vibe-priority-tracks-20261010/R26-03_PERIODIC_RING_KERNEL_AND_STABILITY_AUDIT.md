# NEXUS OMEGA · R26 — Periodic Ring Kernel and Stability Audit
## MISTRAL/VIBE deepening of GROK R26 Strategy Priority 1 · WP2 subset · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_20261010_R0
MAXI_MAPPING        = R26-03
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
NA1_SPEC_SHA256     = 6b2bda7e700bf219fc9e7609da7d60b6c4079b0766caf51bb5d82629f31c4c11 (PR65 head 17e0a327, verified byte-exact, 11483 B)
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED — deterministic analytic evaluation and numeric identity checks only; no network simulation, no seeds, no D/NF/NE experiment
```

## 1 · Audited object

NA-1 §3 (source-exact, verified): `W_ij = w0 + w_exc · cos((θ_i − θ_j)/2)^p`,
with `h_i(t+1) = Σ_j W_ij r_j(t) − g_inhib·max_j r_j(t) + I_ext` (MODEL_MAX).
R25-03 §2 (verified, SHA-256 e7eabdf3…): same kernel family with
`− g_inhib·Σ_k r_k(t)` (MODEL_SUM). The kernel audit below is independent of
the inhibition variant; §6 treats the variants.

## 2 · Theorem: admissible exponents of the bare half-cosine kernel

Let Δ = wrap(θ_i − θ_j) ∈ (−π, π] and K_p(Δ) := cos(Δ/2)^p.

**(P1) Real-valuedness.** cos(Δ/2) < 0 on (π, 2π) of the unsigned circle. For
negative base, x^p is real iff p ∈ ℤ or p = a/b (lowest terms) with b odd.
For all other real p the kernel is undefined on half the domain.

**(P2) Circle well-definedness (wrap identity / 0↔2π seam).** A kernel on S¹
must satisfy K(Δ) = K(Δ + 2π). Since cos((Δ+2π)/2) = −cos(Δ/2),
K_p(Δ+2π) = (−1)^p·K_p(Δ) on every real branch. The wrap identity holds for
ALL Δ iff (−1)^p = 1 on both signs of cos(Δ/2), i.e. iff the map x ↦ x^p is
**even**. Hence exactly:
- p = 2k, k ∈ ℕ (even integers): smooth (C^∞), and K = |cos(Δ/2)|^{2k} = cos^{2k}(Δ/2);
- p = a/b, b odd, a even (non-integer): real and 2π-periodic, but identical to
  |cos(Δ/2)|^p with a cusp at Δ = π; C^m differentiable only for p > m;
- p odd integer: **anti-periodic**, K(Δ+2π) = −K(Δ), 4π-periodic, seam
  discontinuity at 0↔2π (deterministic witness: K_1(2π−ε) = −K_1(ε) → −1 vs +1);
- all other p: not real-valued on the circle.

**Corollary (sharpened GROK claim).** The admissible bare-kernel family is
exactly { |cos(Δ/2)|^p : x↦x^p even }; only even integers are smooth.

**(P3) i↔j symmetry.** K_p(−Δ) = K_p(Δ) wherever defined (cos is even), so
W_ij = W_ji holds within each branch; the odd-integer failure is a circle
identification failure, not a local symmetry failure.

**(P4) Translational equivariance.** Holds iff the kernel is well-defined on
S¹ (P2). Otherwise the same physical pair (θ_i, θ_j) yields two different
weights depending on representative choice.

**(P5) Computational witness (fail-closed, numeric semantics).** IEEE-754
`pow(x, p)` with x < 0 and non-integer p returns NaN (C99, JS, Java);
Python 3 returns a complex number on the principal branch. Any implementation
of the bare kernel with non-integer p therefore produces NaN/complex entries
in W for ring separations in (π, 2π) — a deterministic, implementation-level
failure witness, not a theoretical nicety.

**Verdict.** GROK Priority-1 is CONFIRMED and sharpened: freeze must either
restrict p to the admissible class or replace the kernel (§5). Historical
NA-1 results obtained with non-admissible p are invalid as stated; per the
MAXI order a replacement kernel is a NEW CANDIDATE, not a retroactive patch.

## 3 · Distance function fix (binding proposal)

Δ must be computed as the wrapped circular difference
`wrap(x) = atan2(sin x, cos x) ∈ (−π, π]` BEFORE kernel evaluation, and the
0↔2π seam must be a mandatory frozen fixture (ties to NE-5
PHASE_WRAP_AND_ANTIMERIDIAN). For K-B and K-A (§5) the seam is continuous
because they are trigonometric polynomials in cos Δ.

## 4 · Fourier discipline

A smooth 2π-periodic kernel is a cosine polynomial/Fourier series in Δ with
integer modes m. The bare half-cosine corresponds to the half-integer "mode"
m = 1/2 — the exact origin of the failure. Repairs restore integer modes.

## 5 · S¹-valid replacement kernels

### K-B (primary repair candidate; minimal semantic distance to NA-1)

```text
K_B(Δ) = cos^{2k}(Δ/2) = ((1 + cos Δ)/2)^k ,  k ∈ ℕ⁺
```

- Smooth (C^∞), 2π-periodic, symmetric, single peak at Δ=0, zero at Δ=π,
  nonnegative (excitation shape; inhibition enters via w0/subtractive term
  or the global pool — declared explicitly per §6 arm).
- **Finite Fourier spectrum:** K̂_B(m) = C(2k, k+m) / 4^k for |m| ≤ k, else 0
  (verified numerically to 1e-15 for k ∈ {1,2,4}). Modes 0..k only.
- **Width:** cos^{2k}(Δ/2) ≈ exp(−kΔ²/4) near 0, so σ ≈ √(2/k)
  (k=2: 1.00; k=4: 0.71; k=8: 0.50; k=16: 0.35 rad).
- **Mode dominance:** K̂(2)/K̂(1) = (k−1)/(k+2), decreasing in k
  (k=2: 0.25; k=4: 0.50; k=8: 0.70 — sharper kernels separate the
  single-bump mode more cleanly at onset).
- **Total excitation mass:** M_k = ∫_0^{2π} K_B = 2π·C(2k,k)/4^k ~ 2√(π/k)
  (k=1: 3.14; k=2: 2.36; k=4: 1.72; k=8: 1.23; k=16: 0.88 — verified
  numerically). Sharper kernels LOSE mass; bump existence needs
  correspondingly larger w_exc (§7 witness W2).
- Domain declaration: k ∈ ℕ⁺; p ↔ k = p/2 preserves the original
  "sharpness exponent" semantics for admissible even p.

### K-A (independent standard baseline)

```text
K_A(Δ) = e^{κ(cos Δ − 1)} ,  κ > 0   (von Mises / circular normal shape)
```

- Smooth, positive, 2π-periodic, single peak; Fourier coefficients
  I_m(κ)e^{−κ}/I_0(κ)e^{−κ} decay monotonically in m → m=1 selected at onset
  under DC-cancelling inhibition.
- **Identity (verified):** exp(−sin²(Δ/2)/(2σ²)) = exp((cosΔ−1)/(4σ²)) = K_A
  with κ = 1/(4σ²). The chord-Gaussian and the cosine-exponent kernel are the
  SAME family; this closes a tempting false alternative for the D-4 baseline.
- Serves directly as the von-Mises filter baseline required by NA-1 D-4.

### Secondary (optional robustness arm)

Poisson kernel P_r(Δ) = (1−r²)/(1−2r cosΔ + r²), r ∈ (0,1): smooth, positive,
single peak, geometrically decaying Fourier modes. Declared optional; not
required for the freeze decision.

## 6 · MODEL_MAX vs MODEL_SUM (contradiction materialised, not reconciled)

```text
MODEL_MAX (NA-1 §3):  u_i = Σ_j W_ij r_j − g_inhib·max_j r_j + I_ext
MODEL_SUM (R25-03 §2): u_i = Σ_j W_ij r_j − g_inhib·Σ_k r_k + I_ext + ξ_i
```

- SUM-inhibition is **mass-proportional**: every additional peak raises the
  global subtractive term, producing mutual peak suppression — the classical
  local-excitation/broad-inhibition architecture (cf. Noorman et al. 2024:
  local cosine-tuned excitation + broad uniform inhibition).
- MAX-inhibition is **amplitude-proportional**: a second, smaller, distant
  peak adds local excitation but does NOT raise max_j r_j, hence does not
  raise the inhibitory term. **Analytic prediction (DESIGN_ONLY, registered
  for NF-05):** at identical (w0, w_exc, g_inhib, kernel), MODEL_MAX admits
  stable multi-peak states over a strictly larger parameter region than
  MODEL_SUM. Falsifier: NE-6 gain sweep showing earlier two-peak coexistence
  under SUM than MAX.
- Consequence: NF-05 (two-peak injection) outcomes are NOT transferable
  between variants; the freeze must declare both arms or one explicit choice.
  Activity scales and bifurcation boundaries differ as well (SUM couples to
  total activity A; MAX couples to peak amplitude only).

## 7 · Single-bump existence region (Amari-type mean-field, deterministic)

Continuum idealisation, Heaviside activation f = Θ(·−θ), effective profile
W = w_exc·K − g_eff (uniform inhibition at fixed bump mass). A stationary bump
of half-width a solves

```text
θ − h = ∫_0^{2a} (w_exc·K(z) − g_eff) dz        (existence)
stability requires  w_exc·K(2a) < g_eff          (edge in inhibitory zone)
```

Deterministic witnesses (numeric evaluation of these analytic conditions;
NOT simulations, no seeds):

| # | (k, w_exc, g_eff, θ−h) | Existence solutions | Stable edges | Reading |
|---|---|---|---|---|
| W1 | (2, 1.0, 0.3, 0.5) | 2 | 1 | single-bump regime exists |
| W2 | (4, 1.0, 0.3, 0.5) | 0 | 0 | **explicit failure** — mass decay 2√(π/k) kills the bump |
| W3 | (2, 1.0, 0.1, 0.5) | 1 | 0 | bump exists but edge unstable |
| W4 | (2, 1.0, 0.9, 0.5) | 0 | 0 | inhibition too strong |

**Mode selection at onset.** With uniform (DC-cancelling) inhibition the
first unstable mode of the linearised uniform state is m = 1 for K-B and K-A
(their Fourier spectra decay in |m|), selecting a single bump at onset; K-B's
m = 2 suppression ratio (k−1)/(k+2) improves with k. **However**, beyond
onset, multi-bump coexistence cannot be excluded analytically: two-bump
families exist for lateral-inhibition kernels (Laing–Troy, Amari-type
models), and MODEL_MAX enlarges those basins (§6). The empirical guard NF-05
is therefore mathematically mandatory — this is the formal ground of the
PR65 bump-uniqueness HOLD.

## 8 · Negative evidence and falsifiers

1. If any frozen S¹-kernel shows a 0↔2π seam mismatch under deterministic
   evaluation, §2 is falsified for that kernel.
2. If an implementation of the bare kernel with non-integer p produces real
   weights on (π, 2π) in IEEE semantics, P5 is falsified.
3. If the NE-6 gain sweep shows MODEL_SUM admitting two-peak states at
   strictly smaller gains than MODEL_MAX, the §6 prediction is falsified
   (and the arms may collapse — that result would itself be positive
   negative-knowledge).
4. If K_B shows K̂(2)/K̂(1) ≠ (k−1)/(k+2) for any k, the Fourier analysis is
   falsified.
5. If bump existence for (k=4, w_exc=1, g_eff=0.3, θ−h=0.5) is demonstrated
   under the stated idealisation, the Amari witness W2 is falsified.

## 9 · Changes to historical interpretation

- NA-1 with bare cos(Δ/2)^p and non-admissible p: **invalid as stated**
  (undefined/NaN weights), independent of any empirical question.
- NA-1 with p = 2k: mathematically equivalent to K_B; historical intent is
  preserved by adopting K_B with k = p/2 as the new candidate.
- D-4 baseline: K_A recommended (identical to chord-Gaussian; standard).
- No result in this document constitutes an experiment of the D/NF/NE suite.

## 10 · Status grammar

```text
R26_03_KERNEL_AUDIT        = ISSUED_DESIGN_ONLY
BARE_KERNEL_ADMISSIBLE_P   = {2k: k∈ℕ} ∪ {a/b: b odd, a even} = x↦x^p even
BARE_KERNEL_SMOOTH_CLASS   = p ∈ 2ℤ
KERNEL_CANDIDATES          = K_B (primary repair) · K_A (baseline) · P_r (optional)
MODEL_MAX_VS_MODEL_SUM     = MATERIALIZED_BOTH_ARMS_REQUIRED
SINGLE_BUMP_EXISTENCE      = PARAMETER_DEPENDENT (witnesses W1–W4)
MULTI_BUMP_EXCLUSION       = NOT_ESTABLISHED_ANALYTICALLY (NF-05 mandatory)
CLAIM_CEILING              = C1_DESCRIPTIVE_ONLY
EXPERIMENTS                = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
