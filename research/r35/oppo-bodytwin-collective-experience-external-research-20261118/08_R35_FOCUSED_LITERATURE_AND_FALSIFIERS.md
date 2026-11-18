# R35 OPPO / BODYTWIN | high-value external primary research shortlist
OBJECT = NEXUS_OMEGA_AXIOM_R35_HIGH_VALUE_OPPO_IMU_SCIENCE_SHORTLIST_20261118_R0
STATE = PRIMARY_SOURCE_DESK_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
EVIDENCE_CLASS = PUBLISHED_SOURCE_RESEARCH_NOT_REPLAYED_ON_OPPO
DATE = 2026-11-18
CAUSAL_USE = R35_EXTERNAL_E01_E05_E08
GATE = NO_AUTO_MODEL_OR_CLAIM_PROMOTION

## Directly useful sources with falsifiers
R01 'Synchronisation of multiple unconnected inertial measurement units using software correction' (2025), Journal of Biomechanics, DOI 10.1016/j.jbiomech.2025.112632. 
Primary indexed abstract https://pubmed.ncbi.nlm.nih.gov/40086251/
Source-supported result: IMU pairs showed linear but pair-specific time drift, reproducible within and between sessions in study conditions.
R35 implication: clock offset alone is insufficient; characterize relative clock skew/drift on OPPO vs companion phone under actual motion, device reboots, batching and thermal drift. Falsifier: fixed-offset model generates growing timestamp misalignment while affine model may fit; independent reference pulse required. NOT_RUN_ON_OPPO.

R02 'Open-Access Wearables Dataset to Evaluate Factors Impacting Accuracy of Smartphone Gait Metrics' (FDA regulatory science tool, 2024). 
https://www.fda.gov/medical-devices/regulatory-science-tools-catalog/open-access-wearables-dataset-evaluate-factors-impacting-accuracy-smartphone-gait-metrics
Source-supported: time-synchronized dual-smartphone inertial streams (iPhone X, Samsung S22), independent Xsens IMUs and instrumented walkway, multiple carrying modes; NOT OPPO, not a BodyTwin clinical validation.
R35 implication: candidate public benchmark for test protocol and phone placement confounds, if license/consent/usage terms independently inspected; no direct OPPO transfer. Falsifier: a filter trained with one placement gives poor cross-placement performance. BENCHMARK_CANDIDATE_ONLY.

R03 'CoWear: Towards Collaborative Wearable Inertial Localization with Multiple Smart Devices' (arXiv:2610.20596, 2026).
https://arxiv.org/abs/2610.20596
Source-supported search abstract: collaborative inertial localization across phone/watch/glasses, learned uncertainty weighting and reference framework. It is a PREPRINT and not the same hardware topology as two phones.
R35 implication: compare decentralized estimate+uncertainty fusion vs joint raw inertial state estimation and a no-fusion baseline. Check covariance calibration and correlation; strong counterexample where two correlated devices are treated as independent and become overconfident. SOURCE_REVIEW_CANDIDATE, not replicated.

R04 'Engineering Reliable Wearable Motion Tracking: A Critical Review of Calibration, Error Compensation, and Application-Oriented Method Selection' (Electronics 2026 15(18) 4066; DOI 10.3390/electronics15184066).
https://www.mdpi.com/2079-9292/15/18/4066
Source-supported: calibration taxonomy involving intrinsic sensor error, sensor-to-segment alignment, drift, flexible sensors and external references. REVIEW, not direct OPPO measurement.
R35 implication: BodyTwin MUST make the device-to-body segment alignment assumption explicit; changing phone placement without recalibration can invalidate body claims. Falsifier: controlled placement rotation with fixed body posture changes inferred pose.

R05 'Selection-Induced Contraction of Innovation Statistics in Gated Kalman Filters' (IEEE Xplore document 11714296, 2026; earlier arXiv:2512.18508).
https://ieeexplore.ieee.org/abstract/document/11714296
https://arxiv.org/abs/2512.18508
Source-supported: nearest/selected in-gate Kalman innovations contract, even with matched linear-Gaussian assumptions. Independent verification of actual proof mathematics and NEXUS-specific implementation NOT_RUN.
R35 implication: preregister gated and ungated innovations, sample dimension, chi-square reference and selection conditionality; never promote NIS-only PASS to filter correctness. Falsifier: synthetic matched-model tests produce misleadingly low gated NIS while NEES/trajectory error remain inconsistent.

R06 'Research on IMU data quality assessment and noise reduction algorithm for smartphone' (Navigation Positioning and Timing 2025 12(5):87-98, DOI 10.19306/j.cnki.2095-8110.2025.05.007).
https://dhdwyss.spacejournal.cn/en/article/doi/10.19306/j.cnki.2095-8110.2025.05.007
Source-supported: Allan-variance-based quality assessment and IMU noise-reduction algorithm (abstract). R35 implication: build Allan deviation over predeclared static durations, detect nonstationarity and avoid assuming factory-calibrated Android samples equal raw MEMS output. Dataset/device-specific replication required.

## Expert obligations on each paper
- Source identity and actual version/DOI and public access; never invent PDF/fulltext access.
- Domain transfer assessment to dual smartphones OPPO CPH2219, Android sensor exposure and human body; cite conditions that differ.
- One precommitted negative + positive control and a null model.
- Report original paper findings separately from proposed NEXUS architecture and NOT_RUN_ON_OPPO.
- License/data rights and privacy audit before importing any external dataset.
- Penalize speculative feature additions not improving a measurable OPPO/BodyTwin falsification gate.

## Priority
1. Clock-skew sync R01 + FDA reference dataset R02 for genuine physical design
2. Body segment alignment R04 + robust baseline R06
3. NIS gating bias R05 for filter consistency
4. CoWear R03 for alternative architecture, only if independent direct dataset applicability can be shown
All are candidate literature evidence; none closes OPPO_BODYTWIN validation gates.
