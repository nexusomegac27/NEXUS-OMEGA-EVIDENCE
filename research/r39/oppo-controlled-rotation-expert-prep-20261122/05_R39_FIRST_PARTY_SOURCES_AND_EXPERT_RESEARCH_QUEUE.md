# R39 official primary physics and Android source anchors
OBJECT=NEXUS_OMEGA_AXIOM_R39_PRIMARY_SOURCE_AND_CURRENT_RESEARCH_REGISTER_20261122_R0
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY | SOURCE_NOT_PHYSCIAL_VALIDATION=YES

S01 Android SensorEvent: https://developer.android.com/reference/android/hardware/SensorEvent — per-sensor monotonic event.timestamp in nanoseconds, Android axes, accelerometer including gravity, gyro angular rates. State device and sensor type.
S02 Android SystemClock: https://developer.android.com/reference/android/os/SystemClock — elapsedRealtimeNanos since boot includes deep sleep; does not imply two independent device clocks aligned.
S03 Android Open Source sensor types: https://source.android.com/docs/core/interaction/sensors/sensor-types — type/calibration/frames vs fused orientation; do not mix accelerometer with TYPE_LINEAR_ACCELERATION.
S04 Android Open Source Sensors HAL: https://source.android.com/docs/core/interaction/sensors/hal-interface — event/report timestamps, HAL clock drift and sample scheduling.
S05 Android Open Source Batching: https://source.android.com/docs/core/interaction/sensors/batching — sensor sampling_period vs max_report_latency, late delivery != event acquisition time.
S06 BIPM/JCGM 100:2008: https://www.bipm.org/en/doi/10.59161/jcgm100-2008e — source-specific reference angle uncertainty; model posterior covariance alone is not absolute physical calibration.
S07 BIPM GUM-1:2023: https://www.bipm.org/en/doi/10.59161/jcgmgum-1-2023 — evaluation and expression of uncertainty.
S08 Official OpenSim/OpenSense: https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084203 — IMU-to-body-segment frame and calibration required for anatomical inverse kinematics.
S09 W3C PROV-O: https://www.w3.org/TR/prov-o/ — provenance entity/activity/agent, predecessor/successor and missing source edges.

Research 2024–2026 queue each expert must source verify without invented claims:
- on-device smartphone IMU gyroscope gravity yaw observability, controlled-roll calibration and rig reference alignment.
- Android HAL timestamp fidelity, batching and FIFO source-to-device rehash for CPH2219.
- uncertainty propagation of nominal angular references, mounting slip, manual observer marker jitter and independent clock offset.
- independent body pose falsification from unmounted sensor plus on-body sensor-to-segment calibration.
- OpenSim/IMUPoser/MobilePoser reference model and code/weight/data licensing, if used in candidate tests.
Original 2026-11-22 R38 source return is ONLY source-readback C1; do not promote to original T21–T28 implementation or physical device enrollment.
Publish method evidence table per citation: source URI, last-updated date where shown, exact statement supported, which R39 hypothesis depends on it, what remains not tested on OPPO.
