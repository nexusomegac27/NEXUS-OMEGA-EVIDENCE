# R35 primary sources register | source-bound preliminary validation
OBJECT = NEXUS_OMEGA_AXIOM_R35_PRIMARY_SOURCE_REGISTER_20261118_R0
SOURCE_CLASS = EXTERNAL_PRIMARY_DOCUMENTATION_OR_DIRECT_STANDARD
STATE = PRIMARY_REFERENCE_VALIDATION_NOT_NEXUS_EXPERIMENT
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

P01 Android Developers Sensors overview
https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview
Direct verified text 2026-11-18: Android accelerometer m/s^2 includes gravity; gyroscope rad/s, hardware and virtual sensors distinguished; sensor inventory and rates vary by device. Does NOT identify OPPO CPH2219 actual installed gyro/calibration.

P02 AOSP Android sensor types
https://source.android.com/docs/core/interaction/sensors/sensor-types
Direct verified text 2026-11-18: Android sensor axes are device relative; base sensors can be bias/temperature-corrected, so not the chip raw output. Experimental calibration must classify preprocessing and exposure.

P03 Android Developers Motion sensors
https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion
Direct verified text 2026-11-18: uncalibrated accelerometer/gyro interfaces and device versus world reference distinction; presence varies by device. C1 BodyTwin body movement not inferred from two device signals without independent mapping.

P04 Android SensorEvent API
https://developer.android.com/reference/android/hardware/SensorEvent
Direct retrieved 2026-11-18 as first-party docs; exact per-device timestamp clock and synchronization must be validated in experiment. Documentation existence does not prove recorded OPPO timestamps satisfy cross-device ground truth.

P05 BIPM JCGM official publications
https://www.bipm.org/en/committees/jc/jcgm/publications
Direct verified 2026-11-18: JCGM 100:2008, JCGM 100/Amd1:2026 nonlinear models, JCGM 101:2008 Monte Carlo uncertainty propagation, JCGM GUM-6:2020 measurement models. No physical reference = uncertainty budget DESIGN_ONLY.

P06 RFC 8785 JSON Canonicalization Scheme
https://www.rfc-editor.org/info/rfc8785
Direct verified 2026-11-18: I-JSON, ECMAScript primitive serialization and deterministic key sorting. Not the same as generic Python json.dumps(sort_keys=True). Authentic vendor import and independent canonical bytes remain unverified from R33.

P07 RFC 9162 Certificate Transparency v2
https://www.rfc-editor.org/info/rfc9162
Direct verified 2026-11-18: public append-only auditable log pattern. Analogy for experience ledger is DESIGN_INFERENCE, not a certified implementation or signature of external agents.

P08 NIST uncertainty guide
https://www.nist.gov/publications/guide-expression-uncertainty-measurement
Direct verified first-party publication catalogue; supports framing of uncertainty and measurement traceability, not any NEXUS sensor metric.

P09 NEXUS scientific parent PRs
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/370
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/372
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/369
Pin full heads recorded in 00. PR sources are owner research records, not external replication.

P10 NEXUS public homepage
https://www.nexus-mobile.de/
Browser-observed 2026-11-18: Research Wire HTTP_404, Science & Open Source panel contains preprint listings with independent source verification NOT_ESTABLISHED. The homepage is not a validated automatic scientific patch feed.

## Research standards
Independent experts must search freely for the most compelling alternate architecture and newer papers rather than only following this list. Include primary DOI/URL, exact publication version and date, conflicts, reproduction methods, device/ground-truth match, licensing. Do not manufacture newer article dates or assert inaccessible text was verified. A prior screenshot, browser page, PDF or abstract is not experimental sensor accuracy.
