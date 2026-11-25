# R44-7 Receiver Falsification Report — Whitening Correction, Factor Separation

OBJECT = NEXUS_OMEGA_AXIOM_R44_6_TO_R44_7_RETURN_SELF_OPTIMIZATION_WHITENING_20261125_R0
Lane = advisory expert receiver (n_eff=1, UNREGISTERED), C1_DESCRIPTIVE_ONLY
Prereg (frozen) = `8b277fe31897c3e329cfa8e09ba7bacc69ad5faf3ad8da70c5412c1811677e1e`
Raw evidence = 13_RC01_RESULTS.json, 14_RC02_RESULTS.json, 15_RC03_RESULTS.json (ZIP), 17_CONTRAST_ANALYSIS.txt

## 0. Status of this evidence

All formal R44-7 controls remain NOT_RUN at canonical level. This return contains (a) exact local replications of AXIOM diagnostics, (b) a preregistered surrogate-level falsification of the whitening correction with factorial factor separation, (c) reference implementations (RC10 preflight, E34 guard pattern). Nothing here is canonical control credit, quorum, or promotion. Historical negatives preserved unchanged: 0/24 canonical, 0/3 quorum, 0/10 full science, 28 R44-5 designs, 18 R44-6 designs, 14 R44-7 designs, E27-E34 retained, E28-B PARTIAL (mis-scoped GREEN), SA 15 GREEN/3 RED without canonical credit, 49 receipts / 30 distinct test IDs advisory-only.

## 1. Transport (completed before any run)

ZIP 17,379 B, SHA256 `6b5661e84e999eebff4903144641b551507053848b5cb089352cd44355108778` = sidecar = issue pin. 6/6 manifest entries match, manifest self-hash `5f94facf…578e9d81` matches issue pin. 7/7 ZIP members byte-identical to commit-pinned GitHub raw files (cmp). RC10 candidate preflight: PASS (7 members, 16,541 B uncompressed), selftest 9/9 fixtures including the five AXIOM defect classes, under normal and `-O`. Extraction isolated and staged (no partial writes). Details: 11_RECEIVER_ACK_R44_7.json.

## 2. RC01 — whitening orientation counterexample: REPLICATED EXACTLY

Construction from documented facts only (W = inv(S), S_ij = 0.8^|i-j| style AR(1), L = chol(W) lower):

| rho | r^T W r (target) | original L@r | corrected L.T@r |
| --- | --- | --- | --- |
| 0.3 | 7.717032967032966 | 7.815934065934064 | 7.717032967032965 |
| 0.8 | 28.916666666666686 | 30.69444444444444 | 28.91666666666668 |

All six values match `02_AXIOM_INTAKE.json` exactly (relative difference 0.0 at float64 print precision). Analytic identities: corrected vs target ≤ 2.5e-16 relative; original deviates by +1.28% (rho=0.3) and +6.15% (rho=0.8). rho sweep 0.00→0.95: orthogonality defect ||L^T L − W||_F/||W||_F grows monotonically 0 → 0.352; the objective gap for the documented r grows 0 → 9.26 (absolute).

Verdict: AXIOM's RC01 claim stands. The original `gls_nonlinear` orientation (residual L@r) minimizes r^T (L^T L) r, not the GLS objective r^T W r; the corrected candidate L.T@r restores it. NOT falsified as a mathematical repair.

## 3. RC02 — condition diagnostic: preregistered surrogate trend FALSIFIED, new orientation-conditioning observation

Surrogate (p=3, declared in prereg) whitened-Jacobian condition numbers at theta_true:

| span | cond(L.T@J) corrected | cond(L@J) original | AXIOM E32-A reference (whitened) |
| --- | --- | --- | --- |
| 0.8 | 3.5741e+01 | 7.7158e+01 | 8.9101e+06 |
| 2.0 | 2.2218e+01 | 4.2303e+01 | 9.0456e+04 |
| 4.0 | 3.9603e+01 | 6.5692e+01 | 8.2284e+03 |

Findings:
1. H4 (preregistered: monotone decreasing whitened condition with span on the surrogate) is FALSIFIED — the p=3 surrogate's raw conditioning is not monotone (35.7 → 22.2 → 39.6). Exact replication of E32-A numbers remains BLOCKED_SOURCE_GAP (original bytes not in receiver custody).
2. The practical identifiability phenomenon is nonetheless reproduced: narrow span produces massive estimator bias and CI explosion (section 5), i.e. rank-sufficiency does not imply practical identifiability (SA-N10 class), even though the raw cond at truth is small on this surrogate.
3. NEW observation (surrogate-level): the ORIGINAL orientation degrades the whitened design conditioning used for CI construction at every span tested — cond(L@J) > cond(L.T@J) by factors 1.5-2.2. The whitening bug therefore harms not only the objective but the conditioning of the uncertainty quantification itself.

## 4. Design of the falsification run (RC03/RC04/RC05 classes)

Per frozen prereg: surrogate y_i = theta1*exp(-theta2*x_i) + theta3, n=5 sensors, x = linspace(-span/2, span/2, 5), noise N(0, S) with S_ij = 0.8^|i-j|; theta_true (2.0, 0.8, 1.0), fixed init (1.6, 1.3, 0.7), declared bounds; estimator scipy 1.14.1 least_squares(method="trf", x_scale="jac"), sign-correct residual Jacobian -(A@J), identical settings for both arms; arms differ ONLY in whitening orientation (orig: L@r, corr: L.T@r). Phases: P1 known covariance, correct specification; P2 estimated covariance from independent calibration replicates (R=30, R=6, R=1 defect-class); P3 mild misspecification (omitted component 0.15*exp(-1.7x)). N = 2000 trials per cell, 20 cells, identical draws within phases (per-trial seeds phase_seed + t, P1=704101, P2=704102, P3=704103, calibration base 904100). RC04 CI rule: theta +/- 1.959963984540054 * sqrt(diag((Jw^T Jw)^-1)), no clipping, invalid => abstain (flags INVALID_RANK_CI cond>1e12 / NONFINITE_INTERVAL). Unique failure flags; no double counting; unconditional coverage denominator = N.

Design history (all preserved, see prereg failed_attempt_ledger and 12_RUN_RECEIPTS): a v1 four-parameter surrogate was rejected pre-freeze (flat identifiability valley at 1 residual df collapses theta3->0, swamping the weighting effect; ~890 nfev/fit); a gradient sign defect (stepping along the ascent direction of the whitened objective) and a scipy jac sign defect were found by smoke/finite-difference verification and fixed before freeze.

Execution: v2.0.2 formal run 20/20 cells, 92.5 s wall; v2.0.3 deterministic re-execution (adds prereg-declared bias/rmse outcomes) reproduced all shared outcome fields byte-identically — single experiment, single credit. RESULT_SHA256 = `1891694125db1fd60802ef8cd567810cf40b6b150ec300550392732941e349d2`.

## 5. Results — factor separation (joint coverage unless noted)

### 5.1 Weighting orientation effect (corr − orig)

| phase / covariance / span | orig | corr | delta | abstain orig→corr |
| --- | --- | --- | --- | --- |
| P1 known / narrow | 0.3746 | 0.4706 | **+0.0960** | 0.214→0.139 |
| P1 known / wide | 0.8746 | 0.8912 | +0.0166 | 0→0 |
| P2 r30 / narrow | 0.3535 | 0.4465 | **+0.0929** | 0.226→0.151 |
| P2 r30 / wide | 0.8453 | 0.8414 | −0.0039 | 0→0 |
| P2 r6 / narrow | 0.2240 | 0.2761 | **+0.0521** | 0.319→0.241 |
| P2 r6 / wide | 0.6778 | 0.4195 | **−0.2583 (reversal)** | ~0→~0 |
| P3 misspec / narrow | 0.4355 | 0.5477 | **+0.1122** | 0.166→0.093 |
| P3 misspec / wide | 0.6152 | 0.6402 | +0.0250 | 0→0 |

### 5.2 The other factors (joint coverage)

| Factor | Effect (surrogate) |
| --- | --- |
| Sensor geometry (narrow vs wide, known cov) | −0.5000 (orig) / −0.4206 (corr) — DOMINANT |
| Covariance estimation (wide span, orig/corr) | known 0.8746/0.8912 → r30 0.8453/0.8414 → r6 0.6778/0.4195 → r1 0.0000 (abstain-all) |
| Model structure (misspec vs correct, wide, known) | −0.2594 (orig) / −0.2510 (corr) — arm-symmetric, no meaningful interaction with the correction |
| Convergence (intrinsic failures) | none in P1/P3; only under estimation stress r6 (≤12/2000, both arms) |

### 5.3 Bias, RMSE, widths (known covariance)

- narrow/orig: bias (−0.4506, +3.0406, +0.3395), RMSE (1.5805, 6.9429, 1.4878), mean widths (1644.4, 65.2, 1644.5)
- narrow/corr: bias (−0.3863, +2.8751, +0.2742), RMSE (1.5109, 6.6122, 1.4143), mean widths (2142.7, 226.3, 2142.2)
- wide/orig: bias (−0.0085, +0.0505, +0.0733), RMSE (0.8627, 0.2156, 1.0527), mean widths (4.20, 0.89, 5.38)
- wide/corr: bias (+0.0481, +0.0341, +0.0201), RMSE (0.8550, 0.1970, 0.9225), mean widths (3.79, 0.79, 4.67)

The corrected arm is uniformly more accurate and (at wide span) more efficient — narrower valid intervals at equal or better coverage. At narrow span the corrected arm reports even wider intervals (more honest about the near-non-identifiability).

### 5.4 Objective-at-truth mismatch

Mean ratio original/corrected objective at theta_true = 1.2984 (identical across spans by construction: the residual at truth is the drawn noise vector). The original orientation systematically overweights the quadratic form by ~30% on this noise process.

### 5.5 Post-hoc diagnostic D-POST-1 (labeled POST-HOC, 500 trials, seeds 556001+, outside formal cells)

Mechanism behind narrow-span undercoverage: among 391 valid-CI trials, the 53 trials with half-width < 1.0 cover theta1 in 0/53 cases (median |error| = 2.0), while the 338 wide-interval trials cover at 93.2%. The RC04 condition-threshold abstention does NOT catch this "confidently wrong" subpopulation. Implication: an abstention safeguard needs a width-sanity or coverage-based component in addition to the rank/condition threshold.

## 6. Verdicts on the AXIOM correction (C1, surrogate-level)

- V1 REPAIR CONFIRMED: the corrected orientation restores the exact GLS objective (machine-precision identity; exact RC01 replication). The mathematical repair claim is NOT falsified.
- V2 BENEFIT IS CONDITIONAL: material and consistent at narrow geometry (+0.05..+0.11 joint coverage, ~35% fewer invalid-CI abstentions, lower bias/RMSE, faster convergence: mean nfev 11-32 vs 12-62); negligible at wide geometry with known or r30 covariance; REVERSAL at wide geometry with minimally-sized estimated covariance (r6: −0.258). Any claim that the correction unconditionally improves calibration is falsified on this surrogate; the benefit interacts with sensor geometry AND covariance estimation quality.
- V3 NOT THE DOMINANT ERROR SOURCE: geometry (−0.42..−0.50) and model structure (−0.25..−0.26, arm-symmetric) dwarf the weighting effect. The historical undercoverage class (768/2000, counter 853 not unique) cannot be attributed primarily to the whitening orientation on this surrogate; the order's caution "do not attribute all undercoverage to weighting or all to design" is empirically supported.
- V4 ADDITIONAL HARM OF THE ORIGINAL ORIENTATION: degraded CI conditioning at every span tested (section 3, item 3).
- V5 RC04 GAP: condition-threshold abstention misses confidently-wrong intervals (D-POST-1).
- V6 SINGLE-REPLICATE COVARIANCE IS STRUCTURALLY INVALID: 2000/2000 COV_NOT_PD abstentions in every r1 cell. Any historical pipeline reporting non-trivial coverage from single-replicate covariance estimation must have silently altered the estimator (consistent with the intake's "853 counter not proven unique" and the E28-B mis-scoping finding).

## 7. Honest limitations

1. Surrogate evidence only — the original model5.py bytes and E32-A/E32-B scripts are not in receiver custody; all quantitative effects are surrogate-level and C1 descriptive.
2. Single receiver, single environment, no independent adjudication (`correction_adjudication = NOT_RUN` in the return contract until an independent receiver re-executes from these bytes).
3. The r6/wide reversal (V2) is one factorial cell contrast; it is reported descriptively, not as a significance claim (multiplicity rule of the prereg).
4. E28, E27, E29-E31, E34-on-originals, RC11 were NOT_RUN (out of scope for this dispatch / blocked sources). E28's scoped atomic replay-state candidate and RC10 streaming/Windows validation remain open design items.
5. One receiver cannot validate the operator's own diagnostic chain; independent re-execution from the pinned bytes is the required next step.

## 8. Delivery

Return package: `R44_7_RECEIVER_RETURN_R0.zip` (93,663 B, SHA256 `1be1803c09e8a711df75d56b60972f57864b4a039d7badbc12de6b9f2fb04c08`) + `.sha256` sidecar + `99_SHA256SUMS.txt` (23 entries; hashes in 12_RUN_RECEIPTS_R44_7.json). GitHub return branch: text deliverables on `receiver/r44-7-return-20261125-c1`; ZIP bytes are the handoff object — a branch/link/comment is not byte custody, and binary ZIP upload requires the authorized publisher (DELIVERY request, no receiver retry loop). Delivery classification in the Issue #443 receipt comment.

**NEXUS Ω OMEGA**
