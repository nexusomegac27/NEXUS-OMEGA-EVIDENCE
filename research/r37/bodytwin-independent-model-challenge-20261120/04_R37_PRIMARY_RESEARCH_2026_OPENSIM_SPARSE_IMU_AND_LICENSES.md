# R37 BodyTwin model research — source-first mathematical, physical and code bibliography
OBJECT = NEXUS_OMEGA_AXIOM_R37_BODYTWIN_SOURCE_FIRST_LITERATURE_AND_LICENSES_20261120_R0
RESEARCH_AS_OF = 2026-11-20
SOURCE_CLASS = PRIMARY_PAPER_OR_OFFICIAL_PROJECT_DOC_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SOURCE_IS_NOT_AN_OPPO_REFERENCE = TRUE
REMOTE_CODE_OR_MODEL_DOWNLOAD_AUTHORITY = DENY

## Layer S0 — physical and mathematical observability
S01 Official Android SensorEvent: https://developer.android.com/reference/android/hardware/SensorEvent
Provides device-local monotonic nanosecond timestamps, acceleration including gravity for TYPE_ACCELEROMETER and gyroscope angular velocity. Two different phones do NOT share a synchronized clock by merely using elapsedRealtimeNanos.
S02 Android AOSP sensor type, HAL calibration/time: https://source.android.com/docs/core/interaction/sensors/sensor-types and https://source.android.com/docs/core/interaction/sensors/hal-interface
Differentiates sensor type, body/device frame, calibrated/un-calibrated hardware and implementation. Recording under SensorManager is not direct raw chip ADC provenance.
S03 BIPM/JCGM official GUM catalogue incl JCGM 100:2008/Amd.1:2026 non-linear models: https://www.bipm.org/en/committees/jc/jcgm/publications
Explicit assumptions, sensitivity coefficients, units and appropriate uncertainty propagation are first-order requirements. Not a source of NEXUS reference accuracy.
S04 Invariant Kalman filtering (2018 survey): https://www.annualreviews.org/content/journals/10.1146/annurev-control-060117-105010
Mathematical Lie-group EKF research prior, candidate alternative to SR-UKF; validity of source observation/pose still separate.
S05 2026 error-state Kalman wearable IMU study published Nov 17: https://www.mdpi.com/2076-3417/16/22/11392
Current research on constrained IMU pose estimation; expert must independently reconstruct its model and actual experimental setup before drawing any transfer claim.

## Layer S1 — physically anchored musculoskeletal inverse kinematics
S06 OpenSim official OpenSense overview: https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53084203
OpenSim/OpenSense converts calibrated IMU orientation trajectories into kinematic model outcomes. Calibration, body attachment and model assumptions are prerequisites.
S07 Official OpenSim how IMU inverse kinematics works: https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53086369
The IK solver positions a model to best match measured IMU orientations. 'best matches' means model-dependent estimate, not direct absolute anatomical truth.
S08 OpenSim open-source core code and Apache-2.0 license: https://github.com/opensim-org/opensim-core ; https://github.com/opensim-org/opensim-core/blob/main/LICENSE.txt
A permissive open-source library possible baseline, but exact version and dependencies must be locked and license notices preserved.
S09 OpenSense methodological validation paper (2022): https://pmc.ncbi.nlm.nih.gov/articles/PMC8859896/
Human joint inference depends on wearable sensors, sensor-to-segment alignment and drift. It is not a result about an unmounted OPPO.
S10 2026 review of inertial human motion capture: https://doi.org/10.1016/j.jbiomech.2026.113542
Describes biomechanical segment calibration and limitations; reviewer must check version and actual available text before reproducing detailed claims.
S11 Sensor-to-segment functional calibration 2026: https://pmc.ncbi.nlm.nih.gov/articles/PMC13250779/
Mounting/functional axis quality impacts joint angles. Need actual placement, independent reference and subject context.

## Layer S2 — sparse-IMU learned human priors, physically DISTINCT from body evidence
S12 Deep Inertial Poser (2018) paper + author project: https://doi.org/10.1145/3272127.3275108 ; https://dip.is.tuebingen.mpg.de/index.html
Research reconstructs from SIX BODY-WORN IMUs. Benchmark results do not establish 1 phone or 2 phones can uniquely measure full human pose.
S13 TransPose (2021): https://arxiv.org/abs/2105.04605
DNN research for full body pose and global translation using six IMUs; source arXiv is not new NEXUS device ground truth.
S14 Physical Inertial Poser (PIP), CVPR 2022 peer reviewed: https://openaccess.thecvf.com/content/CVPR2022/html/Yi_Physical_Inertial_Poser_PIP_Physics-Aware_Real-Time_Human_Motion_Tracking_From_CVPR_2022_paper.html
Combines learned inertial pose prior with physical constraints; it reports use of six worn IMUs. Critical countercheck: physics constraints and contact priors can be correct by assumption while output wrong on unseen body.
S15 IMUPoser 2023 research/project and source: https://spice-lab.org/projects/IMUPoser/ ; https://github.com/FIGLAB/IMUPoser
Explores commercial phones, watches and earbuds at different placement/availability; public dataset/code not automatic consent to train/relicense. Inspect dataset license, subject consent and splitting.
S16 MobilePoser, ACM UIST 2024 original/project and code: https://doi.org/10.1145/3654777.3676461 ; https://spice-lab.org/projects/MobilePoser/ ; https://github.com/SPICExLAB/MobilePoser
Open-source CODE project notes Creative Commons Attribution-NonCommercial-ShareAlike 4.0. This is not equivalent to Apache-2.0; noncommercial weights/code must not be silently incorporated into an unrestricted deployed application. Verify exact current LICENSE file and weight/data rights separately.
S17 Three-Sensor Inertial Poser (3SIP), May 2026: https://www.sciencedirect.com/science/article/pii/S0097849326000567
Three worn IMUs (head/wrists) generate full-body motion via priors; not direct proof that one unmounted phone measures all joints.
S18 Human-centered lightweight wearable IMU pose (Feb 2026): https://www.nature.com/articles/s41598-026-41004-5
Scientific source reports teacher/student distillation and performance on specific public datasets; no NEXUS hardware cross-validation without independent reproduction.
S19 2026 on-body IMU + vision joint measurement review: https://pmc.ncbi.nlm.nih.gov/articles/PMC13517796/
States accuracy depends on attachment, calibration, joint/plane and protocol; requires independent optical/kinematic reference to claim measured anatomy.

## Tiered source admissibility
PRIMARY_PAPER_READ = actual paper abstract/full-text (record which).
OFFICIAL_DOC_READ = official developer/library site (version record).
CODE_ORIGINAL_VERIFIED = exact upstream repository commit/license and source bytes read.
RESEARCH_REPRODUCED = exact source environment and data rights validated + independent execution.
BODYTWIN_RUNTIME_VALIDATED = requires private actual NEXUS consumer connected to original and source witness; not established.
BODY_REFERENCE_VALIDATED = requires future on-body calibrated reference+consent and independent adjudication; not authorized.
A source title, abstract, video analogy or README cannot fill latter gates. The 2026 publications inform hypotheses and negative controls, not present OPPO anatomy.

## Explicit prohibitions and cost control
Code and public model weights are UNTRUSTED until file/actor/rights reviewed, scanned and sandboxed with network off. NO auto-download, NO executing notebooks from untrusted GitHub repos, NO credential echo or private original CAS linkage. Licenses need SPDX per dependency, models/weights/training data separately; if inaccessible, SOURCE_GAP not substitute. Use bounded 8 first-party research source reads for the first shortlist, then 3 deeper mathematically relevant papers; avoid recursive zeitgeist speculation.
Historical mathematics, SO(3)/SE(3), UKF and biomechanical IK can be combined creatively; no claim about "theoretically unlimited AI" grants bypass of observability, instrument reference, privacy or owner authorization.
