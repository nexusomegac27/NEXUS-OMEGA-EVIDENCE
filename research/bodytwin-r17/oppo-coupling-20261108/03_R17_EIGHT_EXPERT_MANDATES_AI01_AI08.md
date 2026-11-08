# R17 — External expert consortium: AI-1 through AI-8
OBJECT = NEXUS_OMEGA_AXIOM_R17_EXTERNAL_EIGHT_EXPERT_MANDATES_20261108_R0
STATE = EXPERT_BRIEFS_PREPARED_NOT_PROVIDER_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
OPERATOR_INTENT = CONVENE_FOUNDATIONAL_RESEARCH_FOR_OPPO_TO_BODYTWIN_COUPLING
CURSOR_ROLE = NO_NEW_VISUAL_DESIGN_OR_SENSOR_RUNTIME_ORDER
EXTERNAL_AGENT_WRITE = DENY_PENDING_REGISTRATION

## Source-exact baseline and no-false-expertise rules
Before asserting an implementation capability, expert must distinguish: (A) official OPPO/Android specs, (B) historical NEXUS OPPO app/relay reports, (C) actual user device/manifests if source originally supplied, (D) theoretical candidate architecture, (E) independently observed controlled experiment. Exact model OPPO A74 CPH2219; existing app `com.nexusomega.maps` and native IMU ForegroundService are historical project reports; current app runtime not bound in this public research artifact. Public 4D site live states are separate C1 statuses, not IMU data.
Every expert returns THREE alternatives, one preferred, its strongest counterexample, first-party/peer-reviewed primary source links, license check, dependency/capability limits, quantitative metrics to TEST, uncertainty, privacy and rollback. A review is not implementation, nor is a generated screenshot independent sensor evidence.
External author identity is established only by actual provider-return receipt or authorized operator-delivered original; posting a GitHub issue does NOT dispatch a request to a model provider automatically.

## Expert division, required specific outcomes
### AI-1 / E17-01 — OPPO A74 device source and Android sensor inventory (Android/HAL specialist)
- Build exact target OS/ColorOS/SDK/manifest/permissions/sensor capabilities audit plan using SensorManager.getSensorList and Sensor.getMinDelay, vendor/version, resolution, maxRange, fifo, wake-up. Explain limits of official hardware spec versus installed software.
- Review earlier app, `ScientificImuForegroundService` and historical sample counts as reported but source-gap.
- Three design alternatives for controlled on-device metadata-only census; no serial/IMEI/persistent Android ID; avoid new APK install or ADB write.
- Negative: spoofed Pixel device identifier, hardcoded device fingerprint, unavailable gyro, deleted app sources, ADB-enabled-only false positive.
- Crosscritique AI-2 Android lifecycle; decide if 200Hz target sampling is even appropriate instead of assuming.

### AI-2 / E17-02 — Android native capture lifecycle, foreground services, offline queue (mobile systems specialist)
- Evaluate Android 9–16+ sensor/background restrictions, HIGH_SAMPLING_RATE_SENSORS, target SDK foreground service type selection, 6h dataSync limit for Android15 target, OEM battery restrictions and Android 16+ documentation; no invented service permission.
- Compare user-visible Activity-only, correctly authorized native ForegroundService, and offline-only bounded replay.
- Design start/stop, consent, crash recovery, listener unregister, lifecycle evidence and exactly one authorized capture session.
- Negatives: capture after STOP, collection from BOOT_COMPLETED without user interaction, queue replay after consent expiry, 200Hz request treated as observed rate.
- Crosscritique AI-1 device metadata and AI-4 network delivery.

### AI-3 / E17-03 — Timing, calibration frames and measurement uncertainty (metrology specialist)
- Differentiate device frame, sensor frame, eventual body segment and 4D Soft-View. SensorEvent timestamp monotonic; server/browser UTC not equivalent.
- Develop clock offset/drift uncertainty, sample jitter and synchronization plan, fit biases/temperature and sensor-to-segment calibrations only as approved experiments.
- Null model 6-axis yaw / global position unobservability; no claim inferred human joints.
- Three clock/timestamp plans with worst-case dropout and reboot; independently falsifiable.
- Crosscritique AI-5 fusion and AI-6 rendering.

### AI-4 / E17-04 — Secure transport, authenticated relay, durable ACK (systems/security specialist)
- Independent audit plan of existing reported `/relay/filter/update` path as historical only; current endpoint source and auth unknown. No remote POST probe.
- Compare offline signed import, local authenticated LAN transport, and properly authenticated HTTPS relay + separate private derived viewer; do not default to unauthenticated browser WebSocket/BLE.
- Envelope schema, nonce/seq, batch SHA, ACK/idempotency/backoff, TLS auth and key hygiene, relay source receipt, rate and size caps, WSS origin scrutiny, local erasure.
- Negatives wrong device, old session, duplicated packets, public raw leak, absent server auth, network replay, wrong clock.
- Crosscritique AI-7 privacy and AI-8 independent adversarial.

### AI-5 / E17-05 — Estimator, sensor fusion and observability (IMU/UKF researcher)
- Compare existing SR-UKF, VQF 6D orientation, simple complementary/null model; optional GTSAM preintegration in offline comparator only. Review mathematical and license accuracy; no unsupported universal performance ratio.
- Document quaternion convention, gravity separation and bias estimates; quantify NIS/NEES where real validation references exist.
- Null: magnetometer-free absolute yaw, global translation and multi-body human posture are unobservable from lone handheld OPPO 6D IMU.
- Report exact benchmark dataset source/license and predeclared metrics; avoid clinical accuracy claims and model training.
- Crosscritique AI-3 clock and AI-6 visual mapping.

### AI-6 / E17-06 — Device-motion visual mapping vs existing SO(4) Bodytwin (UX & scientific visualization specialist)
- Design only; preserve five projection modes, six SO(4) controls and the P0 fixed live C1 panel.
- Alternatives A rigid device 3D orientation ghost, B 3D orientation with uncertainty/latency halo, C timeline synchronized private replay next to symbolic 4D panel.
- Explicitly disallow treating 6-axis IMU as real 4D human geometry. Mockup labels must say relative device orientation, not human full body.
- Negative false live icon, posture hallucination, unreadable mobile panel, reduced-motion or kill-switch failure, stale/duplicate sample.
- Crosscritique E1–E5 Bodytwin visual mandates and AI-5 physically valid limits; Cursor remains excluded from this visual-design lane.

### AI-7 / E17-07 — Privacy, consent, provenance and ethics (independent governance/security expert)
- Build threat model for private motion data, replay/inference threats, device fingerprinting, improper sharing; no raw IMU or persistent identifiers in public GitHub or C1 feed.
- Separate app-level real user consent, research participation, publication and revoke; none granted by this research order. Special caution if motion may infer personal behavior/health.
- Authentication/retention/minimization/legal evaluation, independent hash and signer trust roots, avoid false cryptographic truth claims.
- Negatives fake consent, unauthorized background restart, browser public access, identity substitution, leaked keys.
- Crosscritique AI-4 transport and AI-6 visual semantics.

### AI-8 / E17-08 — Adversarial evaluator and reliability operations (independent red team)
- Challenge all preferred designs and archived assumptions. Write >25 distinct, nonredundant tests (minimum 5 new beyond R17's 25 predefined) spanning sensor, clock, transport, estimator, visual semantics, privacy and Android energy.
- Report positive controls and minimum viable falsifiers. Distinguish simulated/model vs run-on-actual-OPPO.
- Design long-run reliability measurement without inventing uptime, cross-platform/browser regressions, CI/replay/rollback and work-conserving triage.
- Distinguish source SHA, Android install, encrypted relay, HTTP read, visible DOM and genuine scientific validity as different receipt layers.
- Ensure independent external reviewer, not the author of the preferred implementation.

## Cross-review sequencing
- Wave 1 independently: AI-1, AI-2, AI-3, AI-5 -> establish actual plausible sensor/clock/model scope.
- Wave 2 independently: AI-4, AI-6, AI-7 -> transport/privacy/display requirements and 3 options each.
- Wave 3: AI-8 adversarially reviews *source-exact Wave 1+2*, demands one falsification from every author.
- Wave 4: blind pairwise cross-critiques (1↔2, 3↔5, 4↔7, 5↔6, all→8), preservation of dissent. AXIOM adjudicates separately without provider self-certification.
- 10 predeclared research rounds F01–F10 run only when proper returns actually occur. Their absence is NOT_VERIFIED rather than "10 rounds completed".

## Machine return payload
```text
OBJECT=NEXUS_OMEGA_EXTERNAL_R17_AI_<01..08>_ORIGINAL_RETURN_R0
PROVIDER_AND_RUN_ID=REAL_OBSERVED_OR_NOT_ESTABLISHED
SOURCE_COMMIT=PINNED_GITHUB_R17_SHA
SOURCE_CITATIONS=PRIMARY_DOC_URL_VERSION_DATE
READ_ONLY=YES
OBSERVED_VS_REPORTED_VS_SIMULATED=EXPLICIT_PER_RESULT
THREE_ALTERNATIVES=...
HYPOTHESIS_AND_NULL=...
NEGATIVE_FIXTURES=...
DEPENDENCIES_AND_LICENSES=...
OPEN_GAPS=...
PROVENANCE_BYTES_SHA_IF_ATTACHMENT=...
FALSIFIABILITY_AND_CONFIDENCE=...
RECOMMENDATION_DESIGN_ONLY=...
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
NO_SENSOR_OR_PRODUCTION_WRITE=YES
```

## Governance
All external agents have zero inherited write authority and an empty operational allowlist. User supplies or registered authorized handshakes only; GitHub issues are public briefs rather than actual provider dispatch. No raw phone data, phone serial, ADB IP, authentication token, health data, persistent identity or private science archives in experts' public comments. PR merge, Hostinger deployment, A72 closure, Pixel 9a synchronization and real physical capture remain HOLD_NO_START until distinct operator disposition.
