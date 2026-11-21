# R38 official standards and critical science input
OBJECT = NEXUS_OMEGA_AXIOM_R38_OFFICIAL_ANDROID_PROV_GUM_SOURCE_REGISTER_20261121_R0
STATE = SOURCE_REGISTER_NOT_PHYSICAL_VALIDATION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RETRIEVAL_DATE = 2026-11-21

S01 Google Android SensorEvent, exact definition of event timestamp and device-frame values:
https://developer.android.com/reference/android/hardware/SensorEvent
For a given sensor timestamps should be monotonically increasing, using the same clock base as SystemClock.elapsedRealtimeNanos. Multi-device clocks are not automatically equivalent. In R38 use event times for windowing, not wall/arrival times; verify sensor channel and actual sample rate.
S02 Android SystemClock:
https://developer.android.com/reference/android/os/SystemClock
elapsedRealtimeNanos tracks time since boot including deep sleep. No cross-device synchronization inferred.
S03 W3C PROV-O Recommendation:
https://www.w3.org/TR/prov-o/
Provenance entities/activities/agents represented with explicit source/derivation, do not conflate two copies of same original with separate physical observations.
S04 BIPM/JCGM official publications including JCGM 100:2008:
https://www.bipm.org/en/committees/jc/jcgm/publications
Measurement uncertainties require model/reference/units and suitable assumptions; posterior EKF covariance from assumed noise is not metrologically calibrated real-world error by itself.
S05 OpenSim/OpenSense original project:
https://github.com/opensim-org/opensim-core
https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084203
Inverse kinematics requires calibrated wearable segment orientation inputs and actual model, not a desk phone. Verify source license for use.
S06 Current R37 model candidate original operator upload:
NEXUS_OMEGA_R37_Expert_Stage0_Return_20261120_R0.zip, 127368B, sha256 35895a55f1a7fea35dab49de5c9dbd58665b2415a68dd034bd1251d54a1388a1 (source-supplied to AXIOM, not in public GitHub); M01 8/8 and 10/10 independently synthetic replayed; M02 original SHA seal 14/16 mismatch and one-device channel-count error.
S07 R37 public/source original:
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/378
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/380
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/379
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/381
R37 research phase is terminal, but these prior GitHub source objects remain historically addressable after unmerged closure.
S08 R37 OPPO PRIVATE source custody in DIFFERENT repository:
https://github.com/nexusomegac27/NEXUS-OMEGA-PRIVATE-SCIENCE-CUSTODY/pull/36
A private 404 for unauthenticated readers is not proof of source absence. Do not publish private raw or source digest in public R38.

## Data relevance
Official docs support timestamp/frame/uncertainty/provenance model definitions; they do not establish a completed, authorized R38 kernel or any body measurement. No new 2026 software paper can bypass source originals, independent observer truth, sensor-to-segment calibration or owner scope.
