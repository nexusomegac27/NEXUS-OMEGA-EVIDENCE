# R17 — Architecture options, data contracts and staged admissibility
OBJECT = NEXUS_OMEGA_AXIOM_R17_OPPO_BODYTWIN_ARCHITECTURE_AND_TRUST_BOUNDARIES_20261108_R0
STATE = RESEARCH_BLUEPRINT_C1_NOT_RUNTIME
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM

## Decision target
Use *actual OPPO inertial data* to inform a separately marked, bounded view of device motion inside Bodytwin, while keeping (A) the existing symbolic 4D math and (B) the Hostinger Cron status board unchanged. Do not directly map a 3D sensor quaternion to six SO(4) plane angles or call it 4D body reconstruction.

## Three implementation alternatives to independently falsify
| ID | Candidate | Merits | Weakness / decisive gate | Recommended sequence |
|---|---|---|---|---|
| R17-A | OFFLINE REPLAY: source-exact original OPPO inertial session (private evidence custody) -> sealed import -> isolated 3D rigid sensor marker rendered into Bodytwin sandbox | Deterministic, no new device networking or public exposure, falsification-first | Original session bytes/consent provenance and calibration needed; no true realtime | **FIRST** once source bytes are legitimately present; use synthetic data until then |
| R17-B | LOCAL ONLY: Android native source -> authorized local network authenticated low-rate stream -> isolated local viewer | Low network latency, no public internet relay | Network identity, cert/trust, captive WiFi, browser auth, Android lifecycle, replay risks, remote device pairing | Comparator, not default |
| R17-C | REUSE EXISTING RELAY: Android native app + local sealed queue -> authenticated HTTPS ingestion to independently verified NEXUS relay -> bounded state estimator -> strictly separated authenticated read-only session view (SSE/HTTPS polls/WSS evaluated, not presumed) | Network independence from ADB, decoupled UI, durable ACK and cross-device labelling, preserves existing public site status feed | Old relay /filter/update route is historical, current auth and uptime unknown; public exposure must be denied by default | **PREFERRED FUTURE ONLINE CANDIDATE AFTER R17-A** |
| R17-D | Browser-only phone sensors / BLE direct phone-to-public-site | Easy demos in some browsers | No verified hardware/source provenance or durable lifecycle, broad permission/security surface, phone-to-web BLE unsupported assumptions | Reject as foundational default; optional benchmark only if proven |

**Recommended research ordering:** A, then C; B as an adversarial architecture comparator. No physical runtime activation is authorized now. Filter choices are hypotheses: existing SR-UKF vs VQF 6D (magnetometer-free) vs a simple complementary/baseline orientation estimate, plus GTSAM offline high-complexity comparator. Require clean, common dataset and timing windows; count accuracy, uncertainty, CPU, energy, latency and mismatch. Avoid universal UKF-vs-EKF cost ratios.

## Separation of devices, frames, clocks and claims
Use explicit terms:
- DEVICE_FRAME = Android physical device XYZ axes (not screen CSS).
- SENSOR_FRAME = actual sensor vendor frame/axis calibration; inspect alignment to device.
- SEGMENT_FRAME = hypothetical mounted body segment; unavailable until independent calibration.
- VIEW_FRAME = 3D rigid body marker or ghost overlay, NOT SO(4) physical coordinates.
- SO4_VIEW = independent 4D educational/symbolic visual controls.
- SENSOR_MONOTONIC_NS = Android SensorEvent.timestamp relative to elapsedRealtimeNanos() base.
- SERVER_RECEIPT_UTC = server receipt time, not trusted sensor acquisition UTC.
- BROWSER_DISPLAY_UTC = device local rendering time, not independent clock witness.
- CLOCK_MAPPING = `t_server ≈ alpha * t_sensor + beta` estimated with uncertainty under explicit network/time-window assumptions; never treat one ping as absolute sync or two devices as synchronized.

Single OPPO accelerometer+gyro can constrain some 3D orientation changes. Absolute heading, global position and body-segment kinematics are not directly observable from these readings alone. 4D frame visual mapping must be an explicit declared education/representation layer. Montage/unmounted, hand wobble, magnetic anomalies, linear acceleration, bias and temperature are required null/negative controls.

## Proposed private packet contract — RESEARCH ONLY (non-implemented)
```json
{
  "schema": "nexus-imu-private-candidate/0",
  "session_id": "EPHEMERAL_SESSION_NON_IDENTIFYING",
  "device_class": "OPPO_A74_CPH2219",
  "source_app_build_sha256": "64hex_FROM_ACTUAL_INSTALLED_ARTIFACT",
  "sensor_manifest_sha256": "64hex_FROM_ON_DEVICE_METADATA",
  "segment_seq": 1,
  "sample_seq_first": 1,
  "samples": [
    {"t_monotonic_ns": 1000000000, "acc_mps2": [0,0,9.81], "gyro_radps": [0,0,0], "flags": ["SYNTHETIC_EXAMPLE_ONLY"]}
  ],
  "event_count": 1,
  "consent_state": "NOT_GRANTED_RUNTIME",
  "source_class": "SYNTHETIC",
  "frame": "DEVICE_FRAME_UNCALIBRATED",
  "algorithm_version": "UNSELECTED",
  "segment_sha256": "64hex_COMPUTE_ONLY_FROM_FINAL_BYTES"
}
```
The shown numeric values are **synthetic placeholders**, not real OPPO samples. This document is not a valid submission payload. No byte hash, signature or technical content proves physical truth. Device persistent IDs, serials, IMSI, IMEI, Android IDs, IP addresses and personal data are excluded from public artefacts; signed/offline private consent required before actual capture.

## Proposed private derived-view envelope — separate schema/authority
```json
{
  "schema": "nexus-bodytwin-derived-motion-candidate/0",
  "session": "PSEUDONYMOUS_AND_ACCESS_CONTROLLED",
  "mode": "DEVICE_ORIENTATION_ONLY",
  "frame": "RELATIVE_3D_DEVICE",
  "quaternion_wxyz": [1,0,0,0],
  "relative_yaw_observability": "UNBOUND",
  "sample_count": 0,
  "quality": "SYNTHETIC_UNVERIFIED",
  "display_state": "RESEARCH_REPLAY_ONLY",
  "claim_ceiling": "C1_DESCRIPTIVE_ONLY"
}
```
No public URL, relay hostname or auth path is authorized by this schema. Strict allowlist/max payload/finite quaternion-norm check, version+session binding and server-side expiry necessary. Public `/bodytwin/live/current.json` remains unchanged and retains its 300 s research-state feed; do not put raw IMU in it.

## Trust, safety and reproducibility boundaries
- Sender: user-invoked native OPPO capture, visible session control and stop, no hidden background collection. Before any real test: on-device capabilities/permissions receipt, original APK hash, scoped and revocable operator consent, offline rollback and source provenance.
- Buffer: bounded RAM/WAL with exact segment hashes, monotonically increasing seq, duplicate guard, gap markers, cap, TTL, encryption at rest and explicit deletion. Keystore/wall-clock are not independent time truth; app crash/restart must emit gap.
- Transport: TLS 1.2+ / modern HTTPS, strong authentication short-lived scoped tokens, credential storage outside source/logs; ACK of exact batch hash, idempotency, retries/backoff, replay/nonce, rate limits. WSS if candidate explicitly validated. No direct unauthenticated OPPO-to-public-websocket.
- Server: independent API/source identity and endpoint audit, minimal process privileges, quarantine and schema validation, no raw private data exposed. No silent fallback to wrong device class/hash.
- Estimator: stationary baseline/gyro bias characterization, sample-time gaps, uncertainty and calibration-quality flags; numerical/algorithm state cannot be promoted to verified anatomy.
- Browser: private authorized read-only route if ever approved, visible user-controlled Connect/Disconnect, stale/kill-switch, reduced motion, explicit 'relative device movement - not body tracking'; no data capture from browser, no hotlink to raw stream. Layout isolation from P0 4D viewer and live status panel mandatory.
- Four-eyes: a source/transport tester and a separate domain/model reviewer independently rehash; reviewer consent is not equivalent to operator authorization.

## Stage-gated integration (scope and authority)
| Gate | Required evidence | Outcome permitted |
|---|---|---|
| G0 | Original source APK manifest, current OPPO sensors and first-party docs, no private IDs in public | Source census PASS only |
| G1 | Synthetic/offline replay, finite math, intentional failures, no network | Bodytwin *synthetic rigid sensor marker* in isolated sandbox |
| G2 | Explicit separate operator consent and install/runtime authorization, secure device-local capture receipt | OPPO-only bounded capture in nonproduction, **not part of R17 research authorization** |
| G3 | Independently verified current relay auth/API, packet hashes/ACK/replay resistance, rollback and privacy | Nonpublic derived movement stream preview |
| G4 | Browser tests mobile+desktop, P0 overlap no regression, 5-min cron independent, stale/kill-switch/access control | C1 **device-relative** visible UI only after dedicated visual/online release approval |
| G5 | External reference instrumentation, sensor-to-segment registration, multi-sensor observability and normative validation | Future research candidate, not granted by R17 |

FAIL_CLOSED if SOURCE_GAP, CONSENT_OPEN, untrusted identity, missing timestamps, scalar/NaN, clocks unobservable, unauthorized sensor start, stale session, packet replay, unverified role, unknown dependency/license, or claiming BODYTWIN_VALIDATED=YES. Preserve historical OPPO and R16 seals append-only.
