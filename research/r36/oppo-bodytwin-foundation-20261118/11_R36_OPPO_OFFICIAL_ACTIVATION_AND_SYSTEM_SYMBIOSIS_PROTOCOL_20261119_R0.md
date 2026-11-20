# R36 | OPPO official activation and NEXUS system integration: bounded gate design
OBJECT = NEXUS_OMEGA_AXIOM_R36_OPPO_OFFICIAL_ACTIVATION_AND_SYSTEM_SYMBIOSIS_DESIGN_20261119_R0
PARENT = R36 PR375 original foundation @ 6d49c733dc9a0b0fb0b7e3000c28a9b44f239a34; Cursor NAV receiver ZIP 6365 bytes SHA256 5545a5bd5194ba0b14f2876e7b451a7cfa4f9894a5a8e8759434cc6b719d9104, independently ZIP CRC and 5/5 source file hashes MATCH.
SCOPE = SCIENTIFIC_DESIGN_AND_SCOPED_CURSOR_PREPARATION_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED = NO
OPPO_ACTIVATED = NOT_PROVEN
PHYSICAL_REFERENCE = NOT_ESTABLISHED
CONSENT_BIND = OPEN
REAL_CAPTURE_AUTHORIZED = NO
DEVICE_REMOTE_CONTROL_AUTHORIZED = NO
HOSTINGER_WRITE = NO
WWW_WRITE = NO
PR_MERGE = NO
R36 = OPEN

## Operator intent, separated into THREE switches
ENROLLMENT_ARMED = authenticated, source-pinned device recognized by operator-controlled NEXUS receiver. This is not a stream, not motion, not physical proof.
TRANSPORT_ARMED = a safe, non-raw-data signed challenge/response can be transmitted and durable authenticated receipt returned through the actual authorized private channel. An HTTP 200 response, a GitHub PR, or a server-only ACK alone is insufficient.
MEASUREMENT_ARMED = bounded actual IMU collection on real hardware, with user-visible start/stop, consent when applicable, source-locked app version, reference/pre-registration and independent science approval. This never follows automatically from enrollment or transport.
The system may be ENROLLMENT_READY with TRANSPORT_HOLD and MEASUREMENT_HOLD.

## OPPO to full NEXUS graph
PRIVATE_DEVICE / exact sensor app (no hidden always-on capture)
 -> LOCAL_IMMUTABLE_CAPTURE_OR_DIAGNOSTIC (actual event ns, monotonic counters, axis/frame and discontinuity)
 -> OFFLINE_SEAL (original bytes/hash, local consent/scope and RUN_ID; hardware key when attested)
 -> PRIVATE_RELAY/RECEIVER (strict allowlisted destination and TLS, nonce, replay-resistant sequence; no secret in receipts)
 -> DURABLE_STORAGE_ACK (observed source SHA + run ID + receiver signature, ack nonce)
 -> DEVICE_VERIFIED_ACK (device verifies receiver identity, signature, original hash and nonce)
 -> SCIENCE_QUARANTINE (private quality/census, clock alignment, reference, uncertainty; no automatic claim)
 -> AXIOM_C1_INDEPENDENT_ADJUDICATION (strong negative results, full predecessor)
 -> PUBLIC_SAFE_PROJECTION (current/open/archive source derivatives, no raw original hash, operator-reviewed)
 -> BODYTWIN VISUAL RESEARCH (device illustration only until true device-to-segment mapping and body reference).

## Noncompensatory gates for the FIRST official readiness activation
O0 SOURCE/CUSTODY: Private PR33 and private R36 PR35 originals pin exact app/APK source, installed app signature, historic R21 bytes, device/companion identity and receiving endpoint. Missing original=>SOURCE_GAP. No substituted historical files.
O1 DEVICE CENSUS: Both actual physical devices independently report OS/build + SensorManager sensors vendor/name/version/type/range/resolution/minDelay, sampling batching, permission/foreground availability, monotonic clock; model name alone not enough. Do not assume companion is another CPH2219. Distinguish previously Cursor-reported Android13/SDK33 from fresh DEVICE_OBSERVED.
O2 THREAT MODEL: private owner-approved identity and trust roots, signature or Android Keystore optional if actual hardware attestation supported; key nonexportability only after verified attestation. Any fallback to unverified key must be visibly lower assurance and HOLD for strong registration claims.
O3 DRY-RUN: bounded read-only hello/challenge without IMU, person, location or secret; accept exactly one nonce-bound private receiver acknowledgment. No server mutation beyond an explicitly allowed short-lived diagnostic receipt. On connection failure, stop, preserve reason, do not roam to similar-named endpoint.
O4 AUTHORIZED SCOPED MEASUREMENT (NOT PERMITTED BY THIS DOC): offline-first non-human static fixture only after separately written operator scope and signed prereg predecessor choice; explicit start/stop/time limit and local seal. Human trial requires separately recorded granular consent and calibrated body reference.
O5 TWO-DEVICE REFERENCE: compare H0 no fusion, fixed offset, affine skew, nonlinear drift, gyro integration, complementary filter, SR-UKF and optional graph on identical source, heldout data and rank checks. Gated NIS reduction is not a consistency PASS; NEES requires true known state.
O6 NEXUS INTEGRATION: authenticated separate receive ACK; bounded parser schemas, byte-level rehash, no direct executable feed data, no automatic claim or BodyTwin anatomy.
O7 RELEASE: only independently rehashed, public-safe, reversible C1 projection, exact causal parent/current/open/archive. External WWW deploy is separate operator authorization + HTTP/browser witness and rollback.

## Android official constraints checked 2026-11-19
- Android SensorEvent.timestamp is monotonic per given sensor and uses the elapsedRealtimeNanos clock base. Two smartphones do not share a clock automatically; sensor HAL may drift relative to Android elapsed realtime.
- On API31+ target apps, accelerometer/gyro registration rates commonly capped at 200 Hz without manifest HIGH_SAMPLING_RATE_SENSORS; declare actual sampling and permission, no higher rate by assertion.
- Android9+ background continuous sensors do not deliver ordinary events: use approved user-visible foreground operation or stop; do not bypass OS privacy.
- Foreground-service types/permissions differ by OS+target SDK; decide only after app source and census (not any blanket health foreground assumption).
- Android hardware-backed key attestation is optional and must be independently checked against trusted chain/nonce; device key storage is not scientific sensor authentication by itself.

Official primary docs:
https://developer.android.com/reference/android/hardware/SensorEvent
https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview
https://developer.android.com/develop/background-work/services/fgs/service-types
https://developer.android.com/privacy-and-security/security-key-attestation
https://source.android.com/docs/core/interaction/sensors/hal-interface

## Required stop signals
Mismatch of source build or phone identity; no exact original R21; duplicate/replay nonce; unauthorized endpoint; missing device signature/ack; rate/permission/visibility conflict; private raw hash in public index; Consent OPEN on human capture; unknown physical reference; data drift/axis ambiguity; any attempted feed-origin instruction. NO SILENT FALLBACK. 
