# R21 independent primary sources / limits
| ID | Source | Physically relevant fact and claim limit |
| --- | --- | --- |
| A1 | Android SensorEvent timestamp monotonic elapsedRealtimeNanos; per-sensor ordering; sample axis, units — https://developer.android.com/reference/android/hardware/SensorEvent | Android API primary; not device-data proof |
| A2 | TYPE_ACCELEROMETER includes gravity, gyro calibrated versus uncalibrated and bias fields — https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion | Android primary; check exact available hardware types |
| A3 | Sensor batching, FIFO latency and capture callback timing distinction — https://source.android.com/docs/core/interaction/sensors/batching | Android AOSP; assess runtime flags |
| A4 | Monotonic elapsedRealtimeNanos versus wall time; do not conflate — https://developer.android.com/reference/android/os/SystemClock | Android API clock primary |
| S1 | Smartphone MEMS 2023 single-position 4-hour stationary / six-position accelerometer / gyro rate calibration — https://pmc.ncbi.nlm.nih.gov/articles/PMC10490716/ | Independent peer reviewed; hardware not OPPO A74 |
| S2 | TUM inertial calibration: bias, scale, misalignment, noise/temperature reference controls — https://www.fsd.ed.tum.de/research/sensors-data-fusion-and-navigation/research-and-competence-areas/laboratory-testing/ | Research institution, methods only |
| S3 | VQF 6D/9D and algorithm variants vs UKF SR-UKF; reference dataset results — https://vqf.readthedocs.io/en/stable/ | Software/peer-paper reference; not R21 results |
| S4 | VQF Laidig/Seel Information Fusion 2023 DOI 10.1016/j.inffus.2022.10.014 — https://www.sciencedirect.com/science/article/pii/S156625352200183X | Published benchmark; not transferable as OPPO accuracy |
| S5 | Android Sensors HAL raw versus calibrated sensor type and device data chain — https://source.android.com/docs/core/interaction/sensors/sensor-types | Android AOSP; source provenance and bias correction |

## Research decisions derived from the sources
1. A short table-rest acceleration vector should contain approximately Earth's gravitational norm, but `g=9.80665 m/s²` is a conventional reference constant, NOT the measured local gravity or an exact axis reference. Orientation and sensor offset are unknown. Do not use it to assert anatomical calibration.
2. The calibrated Android gyro already applies vendor/factory/online corrections; its static mean is a **residual** candidate, not the intrinsic sensor chip's uncalibrated bias. A future dual-lane acquisition may compare `TYPE_GYROSCOPE` with `TYPE_GYROSCOPE_UNCALIBRATED` if hardware supports it.
3. R21's roughly 70-second session is sufficient to *attempt* static short-term quality, timestamp and residual estimates when source bytes arrive. It is not the multi-hour experimental record used in the cited smartphone Allan-variance paper; long-timescale bias instability/rate random walk/temperature dependencies remain unproved.
4. Timestamp order should be checked per type/sensor; interleaving and transport arrival may not be identical to acquisition times. Ingest URL is not read-only; R21 captures locally as already separately authorized, not via new Hostinger APIs.
5. VQF's published cross-dataset performance is a comparator prior, NOT a predicted OPPO result. NIS consistency needs innovation covariance and model; NEES requires independently known reference truth and correct state covariance.
6. Literature calibration methods should be run on matched hardware under measured environmental/reference conditions. Six static orientations can constrain accelerometer bias and scale; gyro scale testing requires known angular-rate/turn angle reference, not merely six stationary orientations.
`R21_SENSOR_SCIENTIFIC_METRICS=NOT_YET_COMPUTED_FROM_ORIGINALS`.
