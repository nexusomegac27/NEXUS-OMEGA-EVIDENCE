# NEXUS OMEGA · AXIOM — R26 MAX MISTRAL/VIBE independent source and science adjudication
Date: 2026-10-11 · Evidence-only · C1_DESCRIPTIVE_ONLY

```text
OBJECT = NEXUS_OMEGA_AXIOM_R26_MISTRAL_VIBE_MAX_EXPLORATORY_RETURN_ADJUDICATION_20261011_R0
PARENT = NEXUS_OMEGA_AXIOM_TO_PERPLEXITY_R26_MAX_INDEPENDENT_FALSIFICATION_SOURCE_AUDIT_AND_PREREG_PREPARATION_20261011_R0
PARENT_ORDER_MAIN = d2995b789b47037539700d1f6d13e5b007fdbaf2
PARENT_ORDER_SHA256 = 72f088cd2fa22e71eef2e1c020af8409fd3327acdd2aec9b9177b60790811039
SOURCE = NEXUS_OMEGA_MISTRAL_VIBE_R26_MAX_INDEPENDENT_FALSIFICATION_RETURN_20261011_R0.md
SOURCE_ORIGINAL_BYTES = 28368
SOURCE_ORIGINAL_SHA256 = 4e7193c7d7b30524bbffce84603b292a7fe46379adca82d50b8b0465062f73b4
SOURCE_ORIGINAL_GIT_BLOB = a38a3842ae69bd29f3b672884bd350a502d6167d
SOURCE_TRANSPORT = GITHUB_API_EXACT_SOURCE_ONLY
RETURN_ROLE = MISTRAL_VIBE_INDEPENDENT_ADVERSARIAL_SECOND_PASS_NOT_PERPLEXITY
PERPLEXITY_RECEIVER_ACK = PENDING_UNCHANGED
EXPLORATORY_SCIENTIFIC_VERDICT = PASS_WITH_MATERIAL_CAVEATS_C1
ANALYTIC_FIXED_POINT_REPRODUCTION = PASS_SCOPED_N32_K8_L5
TWO_PEAK_TRAJECTORY_INDEPENDENT_REPRODUCTION = NOT_ESTABLISHED_RAW_LOG_AND_INITIALIZATION_GAP
MODEL_MAX_VS_SUM_GENERAL_WINNER = NOT_ESTABLISHED
NF05_NF06 = DESIGN_ONLY_NOT_EXECUTED
D1_KERNEL_FREEZE = NO
D2_INHIBITION_FREEZE = NO
D3_FILTER_CAUSAL_ATTRIBUTION = NOT_ESTABLISHED
R26_FULL_SCIENTIFIC_TERMINAL = NO
PR70 = OPEN_UNMERGED
PR65 = HOLD_SCIENCE_UNMERGED
PR67 = HOLD_PRIVACY_HISTORY_UNMERGED
PR71 = DRAFT_PDF_BINARY_SOURCE_GAP
R26_WWW_HOSTINGER_B2_B3 = NOT_VERIFIED
CURSOR_NEW_WORKER = NO
RUNTIME_RIGHTS = NONE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## 1. Source exactness / privacy separation

The operator supplied two attachments: (a) original 28,368-byte MISTRAL/VIBE scientific report, SHA256 `4e7193c7d7b30524bbffce84603b292a7fe46379adca82d50b8b0465062f73b4` and Git blob `a38a3842ae69bd29f3b672884bd350a502d6167d`; (b) 33,495-byte conversation/working transcript, SHA256 `ae5fd2e05791fdc0f1ebdeb090c1c74c0acb94d2c6a19c48ca4fc13072b2cf39`. The second file repeats the scientific report but prepends and appends conversation-generated work/status text. Its contents were read for context and intermediate error provenance, but the **raw conversation transcript was not placed in the public GitHub repository**, per AGENTS.md privacy policy. This must not be misconstrued as a 2/2 GitHub transfer: only the original scientific report is ingested as original source.

MISTRAL/VIBE self-discloses lack of authorized GitHub write capability. Source-exact operator-to-AXIOM GitHub transport via this separately authorized GitHub connector resolves an **AXIOM intake** capability gap, not a MISTRAL/VIBE sender API event. Therefore `EXTERNAL_EXPERT_SEND_RECEIPT=NOT_ORIGINATED_BY_PRODUCER`. No authenticated Perplexity read or return occurred. Original SHA identity alone is not proof of original calculation provenance.

## 2. Most material new scoped mathematical result — independent numeric replication

Using Python 3.13.5 / NumPy 2.3.5 independently, AXIOM reconstructed exactly the reported idealized recurrence:
- N=32, k=8; `W_ij=((1+cos(2π(i−j)/32))/2)^8`; no W normalization, w0=0, w_exc=1;
- `F_MAX(r)=ReLU(Wr−g·max(r)·1)`; `F_SUM(r)=ReLU(Wr−g·sum(r)·1)`; no bias, stimulus or noise;
- five active units `A={30,31,0,1,2}`; the other 27 output units are inactive;
- `v=(I-W_A)^{-1}·1`; `g_MAX=−1/v_center`; `g_SUM=−1/sum(v)`; rescale `r_A=−g v` so max(r)=1 or sum(r)=1 respectively.

Verified independently:
| Quantity | MAX | SUM |
|---|---:|---:|
| Selected g | 1.9807280461434622 | 0.6050068144805235 |
| Fixed-point residual (L-infinity) | 2.22e-16 | 5.55e-17 |
| Maximum off-arc drive (must be negative) | -0.31795908 | -0.09711955 |
| Radial eigenvalue (restricted active Jacobian) | 1 | 1 |
| Largest non-radial eigenvalue modulus | 1.03778930004910 | 0.9792479 (approx.) |

MAX local shape-perturbation growth at this constructed point is real (eigenvalue modulus exceeds one), while the SUM fixed-point family has contracting non-radial active-set modes in that same *respective* construction. Neither point provides isolated asymptotic stability owing to positive homogeneity. These are checks of **specific local models with their own different g**, not evidence that one inhibition law universally dominates under a matched-normalization intervention. No broad basin of attraction, time-varying noise dynamics or admissible orbital truth claim was inferred.

The source's reported `6.2842−1.9807=4.3033` is **slightly inconsistent arithmetic at its displayed precision**: direct subtraction gives 4.3035 to four decimals. With the exact reconstructed W row sum `6.2841796875` and precise MAX gain, the uniform-state **multiplicative per-step factor** is `4.303451641356538` (not "4.3033 per step" as an exact number). This is a small reporting/rounding correction, not a reversal of the large-gain divergence observation.

The review correctly separates an isolated fixed point from an amplitude-neutral attractor **family** and notes both operators are positively homogeneous only under the stated zero-bias ReLU regime. `SUM` does not intrinsically resolve amplitude neutrality.

**Reproducibility artifact:** `AXIOM_R26_INDEPENDENT_MINIMAL_FIXPOINT_REPRODUCTION_20261011_R0.py` is published with explicit matrices, linear solve, local Jacobian and numeric assertions. This is an independently reproducible spot-check, not a new confirmatory trial or a copy of producer code.

## 3. Findings not yet independently reproduced or overstated in the report

1. **Two-peak trajectory claim**: MISTRAL/VIBE reports asymmetric injection 1.0/0.8, MAX ratio 0.82 with diverging amplitude, and SUM full collapse. But the exact two-peak indices/separation, initial profile, full gain-scaling, iterations, scripted source and raw trajectories are **not supplied as a stand-alone retrievable artifact**. An AXIOM independently reproduced fixed-point/Jacobian check does not verify those trajectories. Result: `REPORTED_EXPLORATORY_NOT_INDEPENDENTLY_REPRODUCED`, not `NF05_PASS` or a universal MAX non-uniqueness theorem. A positive homogeneity theorem already defeats the stronger *isolated asymptotic amplitude-unique fixed point* claim in both unforced ReLU arms, but cannot establish persistent dual bumps from a particular unverified run.
2. **MODEL_MAX vs SUM**: the researcher compares distinct gains (gMAX≈1.9807; gSUM≈0.6050). Even when each creates a nonzero fixed point, this is not a matched-g_eff study. Require at least identical-g and matched-effective-inhibition designs. No `SUM_WINS` or `MAX_WINS`.
3. **S¹ and Fourier**: `c₂/c₁=(k−1)/(k+2)` increasing is algebraically correct for integer positive k and the declared smooth K_B. Aliasing does not materially alter this particular low-mode ratio for the N=32/64, k≤16 window, but this is distinct from arbitrary nonlinear single-bump global stability.
4. **EB1′**: for exhaustive common-coordinate `r=f+u`, valid joint bound `||u||≤B` implies `||f||≥max(0,||r||−B)`. If `B<||r||`, then nonzero f is guaranteed *within the model*; it is sufficient, not generally necessary. No unique physical causal source; SGP4/TLE generic catalog values cannot serve as object-specific ground truth.
5. **Sources**: report grades two sources as fulltext-or-abstract and five as bibliographically checked. Such counts cannot be upgraded to seven fulltext primary-source audits. The report's declaration of `EXPLORATORY_SYNTHETIC_WITH_LOGS` is stronger than what this uploaded package independently exposes: a detailed narrative and summary but no full executable producer logs/code/trajectory tables included. Specific fixes of earlier Gauss-Jordan indexing and quadrature bugs are reported, not independently diff-proven by supplied raw code.
6. **Prereg draft**: only high-level parameters; no calibrated noise model, explicit peak detector, exclusive holdout seeds, tails/multiplicity and object-specific external references. `NF05_NF06=DESIGN_ONLY`.

## 4. Canonical decisions and next differentiating scientific activity

**Accept under C1**: exactly transferred R26 MAX MISTRAL/VIBE second-pass report, fixed-point+Jacobian numerical point independently reproduced, algebraic Fourier/homogeneity bounds, and research negatives. **Reject** as currently unsupported: unconditional NA-1 MAX bump uniqueness, MAX/SUM superiority, completed NF05/NF06, full scientific R26 closure, Perplexity task completion, or real Hostinger deployment.

**Minimal nonredundant next action:**
- The producer provides source code + two-peak initial vector, active unit indices, full time series and branch/gain normalization of MAX/SUM as a separate versioned original via the authorized GitHub API. Validate hard finite-valued array guards and previous solver failures.
- A separate independently prepared *matched-normalization* MAX/SUM negative-fixture with explicit saturating/bias/noise arms is preregistered before any confirmatory trial; the operator must authorize execution. Preserve exploratory versus confirmatory separation.
- Parallel unrelated C1 public-safe textual publication may proceed under Cursor's established domain rule (`nexus-mobile.de` LIVE, `nexus-online.de` coordination), but Hostinger B2 and browser B3 must be actually observed. Cursor continuity reported intake of PR #74 is not a deployment.

No changes or merges to PR #70/#65/#67/#71, no new Cursor worker. No action on unrelated R34. Perplexity remains unacknowledged.

VERDICT = PASS_WITH_MATERIAL_CAVEATS_C1_NEW_EXPLORATORY_COUNTEREVIDENCE_AND_SCOPED_INDEPENDENT_FIXED_POINT_REPRODUCTION

NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.
