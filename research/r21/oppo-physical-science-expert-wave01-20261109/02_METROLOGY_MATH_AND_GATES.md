# R21 scientific measurement plan with explicit physical meaning
## Fundamental quantities
Original `t_{s,i}` is Android SensorEvent acquisition time (ns) monotonic per sensor; `T_session=70.114s` is a separate app-duration metadata field. For each sensor `s` calculate `f_count=N_s/T_session` (only first-pass) and `f_span=(N_s-1)/((t_last-t_first)*1e-9)` from actual events; median `dt_i`, p01/p50/p95/p99 `dt`, gap fraction defined against measured median with sensitivity to factor 1.5, 2.0, 5.0 (no fabricated PASS thresholds), duplicate, nonfinite, quantization and discontinuities. `dt_s>0` per stream. Clock anchors must be treated as uncertain; `elapsedRealtimeNanos` is not UTC.

## Static physical models
Accelerometer Android calibrated output in device axes: `a_m = R_dev^T (-g_world) + b_a + noise + dynamic_motion` up to documented coordinate/sign convention. In the phone-stationary interval, `||a_m||` should be of order terrestrial gravity. **Without known orientation and accurate local g, three-axis static accelerometer bias/scale are not identifiable** from one pose. Gyroscope `omega_m = omega_true + b_g,residual + noise`; steady mean a *candidate* residual gyro bias only if rest independently verified. Estimate sample covariance, median/MAD, cross-axis covariances, conditional autocorrelation and uncertainty.

## Limitations of 70 s
Short-scale overlapping Allan deviation can be explored only at supported tau and with explicit effective sample/window counts; **DO NOT** announce full bias-instability minimum, long-term random walk or temperature coefficient from 70 s. Pre-register physically meaningful extended static sessions (e.g. 30–240 min, if separately authorized) with temperature proxy; six-pose accelerometer with measured alignment; gyro known-rate platform/independent optical reference. No new physical capture is authorized by this research document.

## Gating matrix
G0 R21 Cursor report/session count and device metadata: SOURCE_REPORTED.
G1 Original export ZIP+GZ bytes and exact independent rehash: PENDING.
G2 Event schema, per-stream monotonic timestamps, SI units, total count: PENDING_RAW.
G3 Physical origin: native app/sensor registration, OS/build producer, boot/session binding, local chain of custody: CURSOR_REPORTED_NOT_INDEPENDENTLY_CHECKED.
G4 Measured jitter/gaps/clock drift/duplicated events: PENDING_RAW.
G5 Accelerometer norm, gyro static residual, stationarity segments/uncertainty: PENDING_RAW.
G6 Colored-noise/Allan long-time characterization: INSUFFICIENT_70S; LONG_CAPTURE_NOT_AUTHORIZED.
G7 Device orientation/pose ground truth, six-pose calibration/gyro rate reference: NOT_ESTABLISHED.
G8 UKF/SR-UKF/VQF common-input blind benchmark with independent truth: NOT_STARTED.
G9 Device-to-body segment mount calibration and kinematic observability: NOT_ESTABLISHED.
G10 Scope: R18/R19/R20 intact, Pixel female untouched, no medical/body validation, no WWW: PRESERVE.

## Quantitative analysis preregistration
- Every reported `mean,sd,median,MAD,CI` must include sensor/type, units, numerical method, observation count, segment boundaries and source SHA. 95% confidence intervals need an explicit autocorrelation-aware method, not iid assumption by default; uncertainty traceable to calibration/source.
- Drift/gyro bias / gravity reference from stationary data is conditional on confirmed rest and orientation. Use a device-invariant quaternion distance for filter comparisons, yaw equivalence class for magnetometer-free 6D, no hallucinated GPS or global heading.
- No invented numeric threshold for static jitter/gyro bias, no claim of validated biomechanics, nor output of personal raw events to public repository.
