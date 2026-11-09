# R21 preregistered physical falsifiers — NO RESULTS AT PUBLICATION
`STATE=PRE_REGISTERED_NOT_EXECUTED`

## Negative controls (28)
N01 — Missing original R21 export, but agent asserts a measured bias. Expected: reject/flag, never silently PASS.
N02 — ZIP SHA mismatch; decompressor still returns a believable stream. Expected: reject/flag, never silently PASS.
N03 — Original GZ hash mismatch or wrong member. Expected: reject/flag, never silently PASS.
N04 — R21 original ZIP bytes from another device/session. Expected: reject/flag, never silently PASS.
N05 — ACC/GYRO counts conflict with 7014/7004. Expected: reject/flag, never silently PASS.
N06 — Per-sensor duplicate or backward nanosecond timestamp. Expected: reject/flag, never silently PASS.
N07 — One stream has Unix epoch milliseconds under timestamp_ns. Expected: reject/flag, never silently PASS.
N08 — Host receive-time used as event acquisition-time. Expected: reject/flag, never silently PASS.
N09 — Global interleaving order incorrectly rejected despite per-sensor monotonicity. Expected: reject/flag, never silently PASS.
N10 — Two-clock anchor uncertainty silently set to zero. Expected: reject/flag, never silently PASS.
N11 — Resampling silently fills physically missing frames. Expected: reject/flag, never silently PASS.
N12 — NAN/INF/out-of-range vector accepted. Expected: reject/flag, never silently PASS.
N13 — deg/s interpreted as rad/s. Expected: reject/flag, never silently PASS.
N14 — Accelerometer gravity removed but labeled TYPE_ACCELEROMETER. Expected: reject/flag, never silently PASS.
N15 — TYPE_LINEAR_ACCELERATION substituted for TYPE_ACCELEROMETER. Expected: reject/flag, never silently PASS.
N16 — Gyro calibrated data labeled uncalibrated raw MEMS register. Expected: reject/flag, never silently PASS.
N17 — Unknown device-to-body mount mapped as full-body kinematics. Expected: reject/flag, never silently PASS.
N18 — Static session assumed perfectly level without reference. Expected: reject/flag, never silently PASS.
N19 — g0 exactly used as physically measured local g. Expected: reject/flag, never silently PASS.
N20 — Gyro mean called true bias without independently verified rest. Expected: reject/flag, never silently PASS.
N21 — 70s Allan minimum labeled full long-term bias instability. Expected: reject/flag, never silently PASS.
N22 — PSD normalization/unit convention inconsistent. Expected: reject/flag, never silently PASS.
N23 — VQF uses offline acausal mode and is compared against real-time UKF as equal latency. Expected: reject/flag, never silently PASS.
N24 — NIS/NEES stated as validated without independent truth/covariance. Expected: reject/flag, never silently PASS.
N25 — APP_DEADLINE falsely attributed to thermal shutdown without evidence. Expected: reject/flag, never silently PASS.
N26 — Raw private sensor logs committed to public GitHub. Expected: reject/flag, never silently PASS.
N27 — Anatomical organ animation inferred from single phone IMU. Expected: reject/flag, never silently PASS.
N28 — Pixel9a female lane activated by combined visualization. Expected: reject/flag, never silently PASS.

## Positive controls (14)
P01 — Original source SHA and byte count independently rehashed and preserved. Expected: documented and independently checkable when source is available.
P02 — Correct session, package, device and boot identity segregated. Expected: documented and independently checkable when source is available.
P03 — 7014 accel and 7004 gyro events recovered from original if available. Expected: documented and independently checkable when source is available.
P04 — Per-sensor strict positive time increments. Expected: documented and independently checkable when source is available.
P05 — Timestamp native nanoseconds independently identified. Expected: documented and independently checkable when source is available.
P06 — ACC units m/s² and GYRO units rad/s source-bound. Expected: documented and independently checkable when source is available.
P07 — Gravitational norm of a stationary positive-control *under declared orientation uncertainty*. Expected: documented and independently checkable when source is available.
P08 — Gyro static mean with confidence caveat and measured covariance. Expected: documented and independently checkable when source is available.
P09 — Independent missing/duplicate packet fixtures visibly fail closed. Expected: documented and independently checkable when source is available.
P10 — Real source and controlled fixture analyses visibly distinguished. Expected: documented and independently checkable when source is available.
P11 — R18/R19/R20 and Pixel lane remain unchanged. Expected: documented and independently checkable when source is available.
P12 — Source-license and no-bodytwins claim flags remain visible. Expected: documented and independently checkable when source is available.
P13 — All metrics include N, units, segment window and source SHA. Expected: documented and independently checkable when source is available.
P14 — Return detached manifest independently rehashed by AXIOM. Expected: documented and independently checkable when source is available.

Interpretation: Tests requiring original R21 data are **NOT_EXECUTED** until byte-valid receipt. Controlled fixture success alone cannot substitute for original physical measurements. These are independent failure-mode designs, not 28 observed failures or 14 observed passes.
