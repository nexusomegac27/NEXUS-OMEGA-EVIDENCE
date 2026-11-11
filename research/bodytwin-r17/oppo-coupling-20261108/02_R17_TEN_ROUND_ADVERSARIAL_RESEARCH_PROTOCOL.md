# R17 — Ten predeclared independent research rounds and falsification matrix
OBJECT = NEXUS_OMEGA_AXIOM_R17_OPPO_BODYTWIN_TEN_ROUND_EXPERT_FALSIFICATION_PROTOCOL_20261108_R0
STATE = 10_RESEARCH_ROUNDS_DEFINED_NOT_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
EXPERT_LANES = E17_01_TO_E17_08
POLICY = EXTERNAL_DESK_RESEARCH_ONLY / NO_DEVICE_LIVE_CAPTURE / NO_PRODUCTION_WRITES

## Pre-registration logic
Each round requires: source identity and exact version; hypotheses H1/H0; a positive synthetic/control fixture; at least two independent negatives; a falsifiable criterion defined before measurement; observed vs inferred vs reported fields; ambiguity and null results; independent rehash and a reviewer from a distinct lane. Do NOT report PASS because a paper suggests feasibility. No more than an explicit evidence-backed design status until a real run is authorized and independently witnessed.
One round's failure does not authorize skipping that round or compensating with another score. Claim ceiling C1 remains.

| Round | Topic and primary expert | Research decision, null and negative fixtures | Exit evidence and explicit HOLD |
|---|---|---|---|
| F01 | Hardware & build provenance (E17-01) | Is the actually installed OPPO A74 (CPH2219) app/SDK/sensor list what prior NEXUS reports suggest? Negative: substituted device class, hardcoded Pixel hash, unavailable sensor, stale APK metadata. | Original read-only on-device capability receipt when permitted; until then `HOLD_DEVICE_CURRENT_SOURCE` |
| F02 | Sensor acquisition & lifecycle (E17-02) | Native foreground capture vs foreground Activity + offline replay; test no listener activity while stopped, event gaps/duplicates, Android FGS constraints and 200Hz rate cap. Negative: ADB-driven false success, background throttle, service reinit after process kill. | Platform feasibility design with permission matrix and future test; `HOLD_RUNTIME_CONSENT` |
| F03 | Clock, sequence & provenance (E17-03) | Monotonic Android sensor time -> server receipt uncertainty and boot/session reset; negative future/rollback tick, forged UTC, 32-bit rollover assumption, two phones same sample index ≠ sync. | Declared affine clock model and uncertainty/null; `HOLD_INDEPENDENT_CLOCK` |
| F04 | Robust transport and offline ledger (E17-04) | Replay of A/B/C offline, LAN and authenticated relay candidates. Negative non-idempotent ACK, lost batch, TLS wrong host, duplicated seq, WSS origin attacks, reconnect storm, buffer overflow. | Proposed protocol contract and independent security review; `HOLD_RELAY_CURRENT_AUTH` |
| F05 | Bias/calibration & observability (E17-05) | Single 6-axis phone versus relative 3D rigid device pose; compare VQF, SR-UKF and baseline on same **synthetic/open consented** dataset. Null: unobservable yaw & position; negative mislabeled body segment, magnetic disturbance, high linear acceleration. | Filter scope, required calibration, invalidity regions; `HOLD_BODY_SEGMENT_BINDING` |
| F06 | Browser visual meaning and 4D separation (E17-06) | Device orientation ghost/3D overlay vs independent 4D SO(4) viewer; negative showing 6DoF as 4D ground truth, using quaternion as six SO(4) angles, rendering before consent. | Two user-journey mockups and C1 label contract, no production viewer substitution |
| F07 | Security, privacy, access and threats (E17-07) | Consent evidence/expiry, device role authorization, ephemeral pseudonyms; negative public raw-stream leak, fake consent, replayed token, unexpected background sensor capture, source metadata personally identifying. | STRIDE/privacy threat list and precise denied cases; `HOLD_PRIVATE_TO_PUBLIC` |
| F08 | Reliability, mobile power and UI fallback (E17-08) | Labeled lab plan for Android battery/thermal/throttle, network outages, app crash, device reboot, lost graphics context. Negative delayed viewer sample presented as now, hidden tab silently live, media denied, battery drain beyond pre-specified budget. | Pre-registered p50/p95 processing/age/battery metrics, no invented measurements |
| F09 | Integrated negative replay & blind crossreview (E17-01,E17-04,E17-05,E17-07,E17-08) | Five independent counterexamples spanning source mismatch, timestamp corruption, gap, unauthorized pairing, false body reconstruction. Compare reviewers' discrepancies and preserve them, never forced consensus. | Dissent ledger and reproducible failing fixture; no session/receiver authorization |
| F10 | Architecture adjudication and transition plan (AXIOM + external independent assessors) | Independent multicriteria decision A vs B vs C; use evidence hierarchy safety, inspectability, scientific limits, rollback, capability, energy, latency. Null recommendation acceptable. | Source-bound report + next bounded *separately authorized* implementation proposal; `NO_RUNTIME_PROMOTION` |

## Minimum measurement model (future experiments only; no empirical numbers yet)
- Actual rate: distributions of `dt_sensor_ns`, sensor event count per window, duplicates, gaps and out-of-order events; report requested vs observed, not target as fact.
- Filter: error to an **independent** reference, drift/bias estimate, residual uncertainty and limits; use NIS/NEES only when statistically justified ground truth and model exist. A filter's self-reported confidence is not a proof.
- Network: FIFO occupancy, transmit error and duplicate guards, ACK and retries, end-to-end age decomposition `sensor -> app -> relay -> adapter -> frame`, not only HTTP RTT; explicitly estimate server/browser clock offset.
- Quality: invalid quaternions/nonfinite coordinates, unexpectedly missing gravity, yaw drift, misregistration; kill/hide false visuals and source markers.
- Experience: lag, freeze, reconnect, 4D Soft-View regression, 60s C1 GET and 300s Cron unchanged; accessibility and pause/stop.
- Power: named OS/build, battery level before/after with screen/CPU conditions, not vendor-advertised battery endurance or unverified FPS.
- Integrity: content SHA256, authenticated session evidence and independent rehash, no raw IMU or persistent hardware ID on public GitHub. No SHA claim that proves physical truth.

## Minimal adversarial vector matrix (not executed)
N01 wrong device class / Pixel identity substitution
N02 missing gyro while app reports present
N03 SensorEvent clock monotonic rollback / reboot
N04 event sample drop and duplicate
N05 NaN, Infinity, magnitude overflow
N06 gyro bias leads unbounded yaw in magnetometer-free mode
N07 phone unmounted vs assumed body pose
N08 false consent token / expired consent
N09 private raw IMU in public web JSON
N10 same C1 producer tick mistaken for new IMU sample
N11 stale 3D display with live spinner
N12 falsified precision / inflated confidence
N13 relay ACK on wrong batch SHA
N14 network reconnect with old session key
N15 WSS Origin wildcard/CORS confusion
N16 browser session token in URL/log
N17 Android background sensor listener stops silently
N18 FGS time-limit exhaust on Android target 35+
N19 4D plane angles inferred directly from a 3D quaternion
N20 unauthorized Pixel/OPPO dual sync
N21 source app replaced mid-session
N22 server clock offset falsely treated as independent UTC witness
N23 filter mismatch, gravity not removed correctly
N24 null/magnetic interference incorrectly normalized
N25 repeated or replayed producer seq

Positive controls: synth known rotation about one device axis, stationary zero motion and bias seed, deterministic disconnected replay, exact same segment idempotent ACK, fake/real data separation labels, browser pause does not pause public feed, public C1 status unchanged.

## Independent return contract (each round)
```text
OBJECT=NEXUS_OMEGA_EXTERNAL_R17_FXX_<EXPERT>_RETURN_R0
STATE=SOURCE_BOUND|DESIGN_ONLY|REJECTED|HOLD_SOURCE_GAP
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
SOURCE_URLS_AND_VERSIONS=...
HYPOTHESES_H1_H0=...
TESTS_OBSERVED_VS_PROPOSED=...
COUNTEREXAMPLES=...
SAMPLE_DATA_CLASS=SYNTHETIC|PUBLIC_LICENSED|PRIVATE_NOT_SHARED
LICENSE_REPRODUCIBILITY=...
DISAGREEMENTS=...
UNKNOWN_AND_BLOCKERS=...
IMPACT_ON_C1=...
HASHES_IF_FILES_SUPPLIED=...
NO_DEVICE_OR_WWW_WRITE=YES
```

## Substantive stop-gates
These are not bureaucratic no-op holds: SOURCE_HOLD blocks the *specific* unproven claim or runtime lane, not unrelated desk research. Experts continue falsification and literature work. The R17 source documents are research instructions, not empirical rounds already completed.
