# R21 physical study preregistration and later measurement extension
## Experimental phase A — reprocess first run, no new device use
A01 byte-exact intake, compression/JSON parser inventory, SI units.
A02 per-sensor event count/first+last event span versus app reported session duration.
A03 stationarity evidence: accel norm stability, gyro magnitude, motion outlier segments, no post-hoc deletion; segment definitions preregistered.
A04 descriptive per-axis residuals, covariances, quantization, spectral shape, short tau Allan exploratory with explicit finite-window support and bandwidth.
A05 cross-check synthetic vs actual and fail-closed handoff; withhold 20% temporally *segregated* frames for reproducibility checks (note temporal dependence).
A06 physical interpretation only with an independent reference if/when present. If not, classify `MEASURED_SIGNAL_STATISTICS_WITHOUT_ABSOLUTE_ACCURACY`.

## Experimental phase B — new future physical measures, separate operator authorization needed
B01 repeated table rests after device thermal stabilization, with logged temperature if available; multihour static capture for credible long tau Allan features.
B02 manual six-pose **accelerometer** orientation controls, each pose documented by an independent level/angle reference if feasible; no gyro scale calibration claim.
B03 known angular rotations with physical external reference and timing to assess gyro gain, axis alignment and latency.
B04 deliberate controlled rests between motions; segment rig known and rigid only, otherwise observe *device orientation*, not human joint pose.
B05 optional magnetometer if actual hardware+sensor type available and calibrated, separately tested for disturbances; 6D vs 9D comparison with declared heading observability.
B06 safety/privacy: seated/desk-safe motions, no unsafe movements, no biometric/medical inference, no public streaming.

## Statistical hardening
If 70 s is adequate for a particular short-term quantity, justify by effective sample size, autocorrelation model and window selection; no universal statistical acceptance PASS threshold is assumed. 95% CI must specify bootstrap block length or equivalent model and calibration uncertainty. Every optional sensor/hardware lane must fail closed if unavailable.

Only phase A conceptual research is commissioned by this packet. No physical experiment is automatically launched.
