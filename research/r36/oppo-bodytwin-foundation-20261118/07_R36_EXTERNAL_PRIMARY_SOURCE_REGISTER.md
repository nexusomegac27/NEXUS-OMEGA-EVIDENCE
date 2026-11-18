# R36 verified external primary source register
OBJECT = NEXUS_OMEGA_AXIOM_R36_PRIMARY_SOURCES_AND_RESEARCH_FALSIFIERS_20261118_R0
STATE = SOURCE_DESK_RESEARCH_NOT_OPPO_REPLICATION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
OBSERVED_DATE = 2026-11-18

P01 Android official SensorEvent API:
https://developer.android.com/reference/android/hardware/SensorEvent
Observed: time stamp given in nanoseconds, per sensor monotonic, uses elapsedRealtimeNanos time base. Does not certify clock identity across distinct phones or source temporal accuracy under actual OPPO HAL.
P02 AOSP Sensor Types and HAL interface:
https://source.android.com/docs/core/interaction/sensors/sensor-types
https://source.android.com/docs/core/interaction/sensors/hal-interface
Observed: hardware/software sensors, factory compensation, uncali variants, drift/timestamp source concerns. OPPO actual installed sensor needs on-device census, not guessed chip raw.
P03 OPPO official regional specs:
https://www.oppo.com/in/smartphones/series-f/f19/specs/
Official regional listing explicitly identifies CPH2219 as F19 with accelerometer/gyro. Separate prior operator private source calls hardware OPPO A74. Regional product label ambiguity and real installed sensor model require actual on-device proof. Published specs alone are not a calibration.
P04 Galna et al. 2025:
https://pubmed.ncbi.nlm.nih.gov/40086251/
DOI 10.1016/j.jbiomech.2025.112632, unconnected IMU synchronization. Pair-specific reproducible clock drift observed in their experimental hardware; transfer to Android OPPO is a falsifiable hypothesis, not an established rate.
P05 FDA wearables:
https://www.fda.gov/medical-devices/regulatory-science-tools-catalog/open-access-wearables-dataset-evaluate-factors-impacting-accuracy-smartphone-gait-metrics
FDA official states 374 retained; accompanying archived public original source:
https://github.com/dbp-osel/wearables-for-gait-synchronized-smartphone-imu-and-walkway-data
README states 370 retained. Both are original records with differing denominators. Do not import trial count or data until original source versions, content file hashes, trial-ID sets and license/consent are independently reconciled. Neither uses OPPO CPH2219, neither claims full body movement.
P06 Gated-NIS:
https://arxiv.org/abs/2512.18508
Submitted v1 2025-12-20, v2 2026-01-09, v3 2026-05-23. Latest arxiv title 'Selection-Induced Contraction of Innovation Statistics in Gated Kalman Filters'; current IEEE article listing:
https://ieeexplore.ieee.org/abstract/document/11714296
The analytical gate-conditioned innovation moments pertain to a specified model and selection setting; NEXUS math derivation, adaptation and independent replay NOT_DONE.
P07 BIPM JCGM metrology:
https://www.bipm.org/en/committees/jc/jcgm/publications
JCGM 100:2008, 101:2008 and Amendment 1:2026 for nonlinearity. Framework for reference uncertainty and nonlinear measurement models; no OPPO test implied.
P08 Public NEXUS frontend:
https://www.nexus-mobile.de/
Actual connected-browser observer from 2026-11-18 observed 3-zone problem, Research Wire panel showing HTTP_404, science/preprint list, source-generated data older than fetch date. A displayed 404 panel is not independently observed raw server HTTP response; use explicit source states and archive old.
P09 Public primary NEXUS GitHub source custody:
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/373
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/374
These are research design PRs; not deployed WWW, physical sensor measurements or external authenticated proofs.

Verification obligations:
- Distinguish original full text, abstract-only, metadata listing and independently run code.
- For linked PDFs inspect actual PDF pages/figures, not only a search snippet; record version and license.
- Apply finite source candidate search budget and event-source date, feed-listing date, fetch date separately.
- Scientific priority: OPPO/BodyTwin direct measurement sources over general AI preprints and homepage cosmetic features.
