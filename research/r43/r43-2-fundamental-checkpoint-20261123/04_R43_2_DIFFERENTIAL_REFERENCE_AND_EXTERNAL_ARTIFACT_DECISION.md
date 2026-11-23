# R43-2 independent differential-reference and BodyTwin method decision

## A. Classical differential two-arm model (AutoClaw X19)
`y_A=+θ+m_A+b_A+r+n_A` and `y_B=-θ+m_B+b_B+r+n_B`.
`θhat_D=(y_A-y_B)/2`, single-arm `θhat_S=y_A`.
In synthetic code m_A/m_B correlation `ρ` varies; common reference `r` cancels by algebra, independent offsets have `var((b_A-b_B)/2)=(σ_b^2/2)` if independent. The covariance term for mounting is `var((m_A-m_B)/2)=(σ_m^2/2)(1-ρ)`. The stated gain is conditional on the model's sign convention, synchronized arms, calibration, shared reference and finite perturbations; the ideal error ratio is not a universal law.

| rho | single sd (degrees) | difference sd (degrees) | observed improvement synthetic |
|---|---:|---:|---:|
| +1.0 | 0.212400184817 | 0.035964552721 | 5.90582027994 |
| +0.5 | 0.210612227881 | 0.106176653861 | 1.98360204643 |
| 0 | 0.212116391145 | 0.146931245386 | 1.44364386613 |
| -1 | 0.211684774637 | 0.202561819439 | 1.04503788139 |

R43-2 E33 **predeclare H0**: when independent reference truth, measurement cost, shared noise and mount/timebase correlation are controlled, differential comparison gives no material uncertainty/coverage improvement over best simpler classical baseline. **H1**: independent repeats with appropriate coverage interval find a stable reproducible advantage, not just a synthetically selected rho=1 arm. Require independent same-timestamp data, at least three countermodels (clock lag, slip anti-correlation, misaligned frames), PSD covariance, meaningful U95 coverage and bootstrap/MC interval, actual angle reference uncertainties. Compare against (1) single-arm (2) averaged independent two-arm *cost matched* (3) differential two-arm (4) permuted/reference-null control. Effects classified C1 only.

## B. BodyTwin science / terminology
C1 descriptive IMU proxy is not an independent physiological human twin. V3 technical PARTIAL, analytical NOT_ESTABLISHED, clinical NOT_ATTEMPTED, usability NOT_ATTEMPTED. NASEM definition and 2025 HDT scoping review noting 18/149 alignment are criteria to audit, not a target statistic or implied medical evidence. Quantum Galileo DOI 10.1126/sciadv.aec8045 is a **method analogy only**: paired controls, phase difference, uncertainty; no quantum/gravity/consciousness extrapolation.

## C. External artifact triage
A01 OpenSense/OpenSim: prioritize original license pin, an independently executable IMU-to-segment tutorial and reference uncertainty. A02 OpenCap: independent optical reference *candidate*, video privacy/clock/occlusion test. A03 PAMAP2: missingness/activity-label null not absolute yaw reference. A04 TotalCapture: independent Vicon candidate subject to source/data license and clock uncertainty. A05 DIP-IMU: IMU pose benchmark, research-only/data use conditions. A06 IMU-Bench: check actual README/source/language and whether independent objective fits dual-phone topology. A07–A13 standards and schemas are review criteria, NOT measured C1 evidence.

## D. Checkpoint call
Reject promotion of illustrative scorecards to empirical rankings. Keep these models as research hypotheses; do not add mandatory OpenSim/OpenCap runtime dependencies, do not start sensor acquisition, and keep all 14 physical gates HOLD. Complete R43-2 research then prepare a scoped Cursor order separately.
