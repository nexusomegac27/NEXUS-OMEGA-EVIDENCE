# NEXUS OMEGA — R28 OPPO CPH2219 expert primary-source index and source-specific limitations

OBJECT = NEXUS_OMEGA_R28_OPPO_CPH2219_FFP_PRIMARY_SOURCES_20261111_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
REFERENCE_CLASS = OPERATOR_AUTHORED_PUBLIC_SAFE_BIBLIOGRAPHY; LIVE_SOURCES_MAY_CHANGE
RETRIEVAL_CLASS = SOURCES_REVIEWED_ON_WEB_2026-11-11; FULL_PDF_BYTES_NOT_DOWNLOADED_OR_REHASHED
PRIVATE_DEVICE_DATA = WITHHELD
SOURCE_POLICY = LINK_OFFICIAL_DOCUMENTS_ONLY_NO_FULL_TEXT_REPRINT

## Verified source locations (scientific support is use-limited)

1. JCGM/VIM 2.39 — Calibration. https://jcgm.bipm.org/vim/en/2.39.html . Official definition distinguishes calibration from adjustment and verification; a USB/ZIP/hash match is not metrological calibration. The definition does not give OPPO-specific pass limits.
2. JCGM/VIM 2.44 — Verification. https://jcgm.bipm.org/vim/en/2.44.html . Objective evidence against specified requirements; requirements must be specified, not invented.
3. JCGM/VIM 2.45 — Validation. https://jcgm.bipm.org/vim/en/2.45.html . Verification whose specified requirements are adequate for intended use. Primary basis of fitness-for-purpose distinction.
4. JCGM/VIM 2.41 — Metrological traceability. https://jcgm.bipm.org/vim/en/2.41.html . Requires documented unbroken calibration chain contributing uncertainty; six gravity faces alone do not automatically create this chain.
5. BIPM JCGM guide index, GUM JCGM 100:2008 plus published 2026 amendments. https://www.bipm.org/en/committees/jc/jcgm/publications . Uncertainty budget guidance; version and relevance to the measurement model must be declared. Reference only, copyright retained by JCGM.
6. Eurachem (2025) Guide: The Fitness for Purpose of Analytical Methods (3rd edition). https://www.eurachem.org/index.php/component/content/article/3-publications/guides/144-gdmv2014 . General analogous validation-planning framework from analytical methods, **not an accelerometer or smartphone-specific calibration standard**. The 2025 planning supplement should be considered only if applicable.
7. Android Developers — SensorEvent. https://developer.android.com/reference/android/hardware/SensorEvent . Events timestamp in elapsedRealtimeNanos base; SI accelerometer units; TYPE_ACCELEROMETER_UNCALIBRATED can retain **factory calibration and temperature compensation** while exposing bias components. Uncalibrated is not sensor-register raw.
8. Android Developers — Motion sensors. https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion . API availability and gyroscope/accelerometer usage; actual sensor implementation must be inventoried on target unit.
9. Android Developers — Sensors overview. https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview . Requested sampling delay is a hint; actual cadence by event timestamps; Android version/target-specific rate limiting.
10. OPPO official A74 CPH2219 specifications. https://www.oppo.com/benl/smartphones/series-a/a74/specs/ . Product mapping and advertised sensors only; does not establish sensor-chip identity, calibration uncertainty, firmware consistency or availability of every Android sensor type for the exact unit.
11. GitHub governed R27 Science Sandbox neutral mandate (immutable). https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/a0851058f4bfcf4b376628f7f362b8cfdedab80d/research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md . Full A/B/C review, unconstrained scientific conclusions, write-default-deny.

## Methodological corrections to externally supplied DeepSeek opinion

- Four-eyes plausibility, EURAMET competence-review concepts and PTB fitness for purpose form a reasonable **research design rationale**, not evidence that ESK, PTB or EURAMET specifically recommended, certified, mandated or evaluated this OPPO procedure. Original DeepSeek bibliographic links, passage coordinates and exact document versions were not supplied in the operator transmission; their alleged specific institutional quotations are **UNVERIFIED** and must not be treated as source-exact.
- "External" independence is not the same as provider/model plurality; independence requires actual source/access, affiliation/conflict and reasoning checks. No claim of expert recruitment or named human reviewer attendance.
- The proposed sequence is **desk-review now; physical/conditional fitness-for-purpose evaluation after a real host/device receipt**. This does not authorize hardware changes.
- Source licence and copy/redistribution restrictions must be checked **per document version**. Do not commit full third-party PDFs or private source trees.

## Open source-specific falsifiers

S01 A74 CPH2219 marking exists publicly but connected device differs (firmware/hardware); S02 accelerometer event comes from Android fused/virtual proxy rather than assumed sensor source; S03 timestamps violate monotonicity or measured sampling; S04 uncalibrated stream was misinterpreted as uncompensated factory raw; S05 six-position results overfit; S06 reference traceability missing; S07 source dates/editions diverge; S08 official method merely imported from chemical analysis into smartphone validation without checking applicability; S09 privacy/license breach from republishing originals.

State of this index: DOCUMENTARY_SOURCE_REVIEW_ONLY; ORIGINAL_DEVICE_BYTES=NOT_PRESENT; METROLOGICAL_VALIDATION=NOT_EXECUTED; EXTERNAL_PEER_RETURNS=NOT_RECEIVED.
