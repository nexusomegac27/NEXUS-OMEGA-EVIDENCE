# R37 first principles — official Android sensors and physical inference limits
OBJECT = NEXUS_OMEGA_AXIOM_R37_OPPO_STATIONARY_SENSOR_PRIMARY_SOURCES_20261120_R0
SOURCE_CHECK_DATE = 2026-11-20
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NO_ON_DEVICE_OBSERVATION = TRUE
NO_AUTOMATIC_MODEL_VALIDATION = TRUE

## First-party primary Android references
A01 https://developer.android.com/reference/android/hardware/SensorEvent
Field timestamp (ns) for a given sensor should be monotonic and share base with SystemClock.elapsedRealtimeNanos(). Android documentation says resting gravity sensor is like accelerometer; device-frame sensor units are typed. Two phones' clocks do NOT become synchronized by using local elapsedRealtimeNanos().
A02 https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion
Accelerometer produces acceleration force including gravity, m/s²; gyroscope angular rotation rate rad/s. Linear acceleration is a separate synthesized/processed sensor that EXCLUDES gravity; do not substitute it into a TYPE_ACCELEROMETER fixture without declaration. Rotation/position integration accumulate biases and require a reference.
A03 https://source.android.com/docs/core/interaction/sensors/sensor-types
AOSP describes calibrated vs uncalibrated sensor channels, bias and implementation. "Uncalibrated" may still have factory calibration and temperature compensation; not unprocessed ADC truth.
A04 https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview
SensorManager sampling constraints and default 200Hz cap without HIGH_SAMPLING_RATE_SENSORS in applicable Android versions. R37 requests 50Hz and measures observed rate; no assumption installed OPPO supports 50Hz stable.
A05 https://developer.android.com/reference/android/hardware/SensorManager
Direct implementation official sensor inventory and registerListener. Must inspect exact OS, installed app target and permissions before proposing a code patch.
A06 https://developer.android.com/reference/android/os/SystemClock
elapsedRealtimeNanos monotonic reference for local user-visible 60s timing, NOT independent physical clock.

## Metrology and research references
M01 BIPM JCGM 100:2008, GUM / 2026 amendment primary register: https://www.bipm.org/en/committees/jc/jcgm/publications. The static first screen is descriptive; no calibrated reference u(ref) from a table.
M02 Or, arxiv 2512.18508, conditional innovation consistency when gating: https://arxiv.org/abs/2512.18508. No inference from gated<ungated NIS allowed.
M03 Inertial-based human motion capture review, available full scientific discussion: https://pmc.ncbi.nlm.nih.gov/articles/PMC8024877/. Mounting position, gravity correction and orientation error affect body kinematics; one unmounted phone on table cannot ground a human joint.
M04 Single inertial sensor attitude and zero-velocity/zero-angular-rate updates: https://pmc.ncbi.nlm.nih.gov/articles/PMC8156317/. A stationary moment can be exploited for bias observations, but does not imply global position/yaw observability or full-body pose.
M05 R36R2 external advisory '60s still phone' source: operator-supplied workspace.tar(3).gz 16775 B SHA256 b975970edbf1b47927b267c0acbf9bf08b9877ad8964a4958c16a823e961804f. Class = ADVISORY_INPUT_UNREGISTERED, not GitHub-received expert execution. Methodological x_err ≈ g*b_g*t³/6 is small-angle constant-bias no-compensation illustration only; not a test acceptance identity.

## What the actual hardware test CAN establish
- One device/source app can produce real Android accelerometer+gyro events over one 60s local monotonic stationary fixture with correct units and source chain.
- With time stamps, counts, median/MAD and local observer context, we can report descriptive evidence of stationarity consistency and detect source/capture anomalies.
- If the EXACT connected BodyTwin pipeline falsely outputs measured human anatomy from the unmounted phone, we can falsify that particular semantic claim/runtime branch. Even a pass on that semantic guard means only no such claim observed in the tested conditions.

## What it CANNOT establish
- OPPO is authentically enrolled in NEXUS until installation/trust root and private source receiver ACK observed.
- Another phone shares synchronized timestamps or a valid affine clock mapping.
- Sensor channel is factory-perfectly calibrated, absolute horizontal position or yaw is observable from a free six-axis IMU.
- A human body/joint/segment was physically measured in a trial with NO human present.
- Entire BodyTwin stack is valid, safe, diagnosed or clinically effective, even if the UI is stable.
- A particular numerical drift trace MUST follow t³ or that deviation proves wrongdoing.
- A GitHub PR, hash match or user-visible demo is a host-certified device original.

## Countermodel and honest negative findings
A perfectly smooth animated person can be generated from pure kinematic priors with no sensor input. Compare zero-stream playback; if the same outputs arise, label MODEL_PRIOR_DERIVED. If no current BodyTwin output can be inspected, classify NOT_CONNECTED rather than PASS. A static phone may be bumped or vibrated on a table; gyro/accel anomalies do not imply someone moved.
All sources are candidate external information, separate from the operator's incoming packet and R37 measurements. No code from external pages or self-declared expert notes gets execution or secret authority.
