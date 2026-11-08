# NEXUS OMEGA R17 — OPPO ↔ Bodytwin: Canonical scientific source baseline
OBJECT = NEXUS_OMEGA_AXIOM_R17_OPPO_BODYTWIN_FOUNDATIONAL_RESEARCH_BASELINE_20261108_R0
DATE = 2026-11-08
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHOR = AXIOM / OPERATOR-SCOPED EXTERNAL_RESEARCH_ONLY
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
EXECUTION = NO_SENSOR_CAPTURE_NO_RUNTIME_WRITE_NO_WWW_DEPLOY
TRUTH_AUTHORITY = NONE
CLAIM_PROMOTION = NO

## 0. Aim, negative scope, nonconflation
Investigate how an existing physical OPPO smartphone could contribute *bounded, auditable, user-authorized inertial motion evidence* to the existing NEXUS OMEGA Bodytwin visualization. This is **not** permission to start sensor collection, re-install an APK, create a public IMU stream, activate Pixel9a sync, infer human full-body anatomy, calibrate human joints, alter Hostinger, or change C1 claims. The existing Bodytwin 4D Soft-View is a *symbolic four-dimensional visualization*. A three-axis gyroscope and three-axis accelerometer are not four-dimensional physical position measurements.

## 1. Binding classes: DO NOT treat as one evidence source
### 1.1 Operator / earlier project reports (not current byte rehash)
- OPPO = OPPO A74 / CPH2219. Earlier NEXUS package identifier: `com.nexusomega.maps`.
- Prior Android capture lane references `ScientificImuForegroundService`, local bounded IMU app, Android ADB used for development (not as the intended permanent data transport).
- Earlier OPPO run reported approximately 41,534 accelerometer and 36,307 gyroscope samples across ~6 min 55 sec and two sealed segments. No original current APK, live device hardware manifest, full raw session, exact signed build or independent real-time HTTPS relay receipt supplied in **this R17 intake**. Prior run is therefore HISTORICAL_REPORTED_ONLY.
- Past Pixel 9a + OPPO architectures are NOT current authorization for dual-device fusion, Pixel admission, time alignment, or public disclosure. OPPO-only single-device research first.
- Earlier deployments/telemetry included legacy relay and candidate device-hash mappings; do not reuse any earlier identifier, hardware serial, IP, transport endpoint, credential or assumption as a new identity/trust root. Device IDs must be independently re-established without disclosure of persistent identifiers.

### 1.2 First-party published OPPO specifications
Official OPPO A74 CPH2219 specs list: accelerometer, gyroscope, gravity, geomagnetic, proximity, optical sensors and pedometer (availability through app APIs, vendor fidelity, noise and background characteristics NOT verified for user's current handset).
PRIMARY: https://www.oppo.com/sa-en/smartphones/series-a/a74/specs/

### 1.3 Android platform constraints (first-party)
- SensorEvent.timestamp: nanoseconds, monotonic per sensor, uses same time base as SystemClock.elapsedRealtimeNanos. Timestamp is not independently authenticated UTC. Sensor coordinates are tied to default physical screen axes; orientation changes do not simply swap raw sensor axes.
 https://developer.android.com/reference/android/hardware/SensorEvent
- Android SensorManager.getDefaultSensor may return composite/virtual sensor; investigate sensor metadata getVendor/getMinDelay/getResolution/getFifoMaxEventCount and getSensorList, not synthetic sensor promises.
 https://developer.android.com/reference/android/hardware/SensorManager
 https://developer.android.com/reference/android/hardware/Sensor
- Sensors and sensor data can be rate-limited by Android 12+/target; 200 Hz cap through registerListener without HIGH_SAMPLING_RATE_SENSORS permission for higher frequency, and user/system restrictions. SamplingPeriodUs is a request/hint, not proof of actual data rate.
 https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview
- On Android 9+ background continuously reporting sensors are restricted; candidate service lifecycle must be specifically audited on actual OPPO/OS/version. Android 14+ foreground service types have constraints and Android 15+ dataSync FGS can be limited to 6h per 24h for target SDK35+.
 https://developer.android.com/develop/background-work/services/fgs/service-types
 https://developer.android.com/develop/background-work/services/fgs/timeout
- Offline queue and retry/backoff design: Android's first-party offline-first architecture suggests WorkManager for *deferred reliable queued data*, not a hard-realtime 50Hz sample scheduler.
 https://developer.android.com/topic/architecture/data-layer/offline-first

### 1.4 Independent measurement / security sources
- OpenSim/OpenSense expects sensor fusion, syncing and sensor-to-body-segment registration and known calibration pose before applying IMU orientations to joint models. A lone body-unmounted/unknown-mounted smartphone cannot establish multisegment human pose.
 https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084203
- VQF provides an open-source magnetometer-free 6D orientation algorithm with documented bias estimation; treat as **candidate filter**, independently inspect current license, dependencies and target performance. Neither VQF nor SR-UKF guarantees global yaw or physical body accuracy.
 https://vqf.readthedocs.io/en/stable/
- GTSAM documents IMU preintegration, covariance and bias but does not resolve absent absolute reference constraints. Consider a high-complexity offline comparator rather than default mobile runtime dependency.
 https://borglab.github.io/gtsam/imufactor/
- WebSocket security: authentication, origin allowlist, replay/duplicate guards, per-message limits, backpressure and session expiry. Anonymized browser data must be separately authorized from ingest.
 https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html

## 2. Observed WWW baseline (not sensor source)
Public URL https://www.nexus-mobile.de/bodytwin/ was observed externally as a 4D Soft-View with a separate C1 live status panel and a recently repaired P0 panel-overlap. Operator plus Cursor now report multi-viewport P0 PASS with raw hashes; AXIOM has not independently acquired the exact current production DOM geometry in this R17 intake. Existing public status source /bodytwin/live/current.json was publicly read around 2026-11-08T10:05:01Z, producer.seq=161, source_changed=false, BODYTWIN_VALIDATED=NO, CONSENT_BIND=OPEN, PHYSICAL_IMU=NOT_AUTHORIZED. That 300 s Cron feed is for public C1 research states; it is not a 3D pose or IMU streaming endpoint and must NOT be repurposed.

## 3. Real unknowns that R17 experts must close
- Current installed APP/APK provenance, signature, build, package, actual ScientificImuForegroundService state, permissions, Android SDK/ColorOS, dynamic sensors advertised, in-device clock behavior, battery throttle, and storage/source integrity.
- Whether existing OPPO native capture/queue transport still works across an unplugged ADB transition and network interruptions; no direct current HTTP/WSS witness.
- What exact relay API or authenticated, nonpublic derived-display endpoint exists now. Old `/relay/filter/update` mentions are historical reports, not proof of current route or security contract. NO NETWORK_WRITE_PROBE in this round.
- Real unit, axis, timestamp, data-capture/clock offsets, calibrations, sample dropouts, WSS auth, data minimization, and rights to display any resulting pose to the public.
- Production Bodytwin 4D renderer to device quaternion mapping is NOT described by existing symbolic SO(4) 6-plane rotations. A new **3D rigid-sensor marker view** must remain explicitly separate; do not pretend it is an inferred 4D human motion.

## 4. Nonnegotiable R17 constraints
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY; BODYTWIN_VALIDATED=NO; CONSENT_BIND=OPEN; TRIAL_001=DESIGNED_NOT_EXECUTED; A72_ORIGINAL_BINDING=SOURCE_GAP; PHYSICAL_IMU_RUNTIME=NOT_AUTHORIZED; PIXEL_9A=NOT_ADMITTED; DUAL_DEVICE_FUSION=NO; HOSTINGER_WRITE=NO; PUBLIC_RAW_IMU=NO; NO_BIOMETRIC_OR_HEALTH_DATA; NO_SECRET_OR_PERSISTENT_HARDWARE_ID_DISCLOSURE; EXISTING_BODYTWIN_C1_FEED_AND_P0_LAYOUT=PRESERVE; CURSOR_VISUAL_DESIGN_EXCLUDED; R17_EXTERNAL_RESEARCH_ONLY; R11_R12_GATE_V2_R9_HOLDS_SEPARATE.
