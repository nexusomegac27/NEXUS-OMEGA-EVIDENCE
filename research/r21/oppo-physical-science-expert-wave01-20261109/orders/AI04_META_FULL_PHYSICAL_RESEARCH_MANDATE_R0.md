# AI04_META — Eigenständiger vollständiger R21-Experten-Forschungsauftrag
`OBJECT=NEXUS_OMEGA_R21_AI04_META_PHYSICAL_SCIENCE_FULL_EVOLUTION_20261109_R0`
`STATE=MANDATE_ISSUED_RESEARCH_NOT_EXECUTED`
`ROLE=Scientific time-series signal processing and reproducible analysis`
`CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`
`RECEIVER=NEXUS_OPERATOR_AXIOM`

## Zentrale Forschungsfrage
Which source-preserving processing pipeline can quantify 100 Hz OPPO acceleration/gyro while preventing interpolation, cherry picking and spectral overclaims?

## Zwingende eigenständige Forschungsentwicklung
1. Define original NDJSON/GZIP schema readback, bounded decomp, per-stream timestamp validation, duplicate/missing/quantization detection, and privacy-safe derived summary.
2. Compare robust stationary window algorithms and null models; no blind classification of entire APP_DEADLINE session as strictly stationary.
3. Derive descriptive time-domain, frequency-domain and cross-axis diagnostics with proper units, window PSD normalization, artifact and filtering provenance.
4. Propose independent Python and alternative R/MATLAB calculations with exactly matched inputs and tolerance-driven fixtures; no invented measurements.
5. Design a complete lightweight local lab + immutable original CAS and frozen report generation with provenance and alternate implementation.

## Unabhängige Mindestprimärquellen
1. https://source.android.com/docs/core/interaction/sensors/batching
2. https://pmc.ncbi.nlm.nih.gov/articles/PMC10490716/
Quellen sind Kandidaten, keine Attribution zu bereits gelesenem einzelnen Originaldownload im Agentenreturn. Gegenquellen und negative Erkenntnisse ausdrücklich erfassen.

## Eigenständiger, vollständig finalisierter Return
Alle Felder von `04_AGENTS_RETURN_AND_CROSS_REVIEW.md` 00–10, mindestens 12 Negativkontrollen und 10 Positivkontrollen, alternativer vollständiger technischer Entwicklungspfad, Datenfluss/Mathematik, eindeutige Zeitschranken, Evidenzklassen und eigene Rückbau-Strategie. Originalquellen mit Versionsdatum und DOI, unabhängiger falsifizierbarer Prüfplan, `NOT_EXECUTED` an nicht gemessenen Stellen. Detached `RETURN_MANIFEST.json` mit SHA-256+Bytes ohne Selbsthash. Bis zum separaten Empfänger-ACK sind alle Ergebnisse nur Kandidaten.

## Kanonische Bindung — keine falsche Evidenzpromotion
- `R18_SOFT_VISUAL=PRESERVED`; `R19_FOUNDATION=PRESERVED`; `R20=CLOSED_C1_WITH_MATERIAL_CAVEATS`. R21-Operator-Physical-Capture-Order PR #349, Head `033298ccf6375654f3783d819b0af012f4cc748e`; PR #348 R21 Read-only, Head `1300dcb257e5dc75a7de9f011cda82951e676924`; beide Draft/unmerged beim Intake.
- Cursor-Messreturn: `STATE=PASS_WITH_MATERIAL_CAVEATS_C1_PHYSICAL_OPPO_IMU_CAPTURE_PROVEN`; dies ist *Cursor-berichtete* Provenienz. Der Original-Export (`166349 B / 3eb9e9e9988b66994429d97e566a71aa2c05bbe951f41725465947841a75a9a4`), Segment-NDJSON-GZ (`166831 B / 544f762cbaab3cd562d8cf868cc15fbee1d23b503b72455c015e6698c02c90e2`) und Return-ZIP (`5337 B / e718438aa23b03ce978e1923423ec1e02f42d93887051b64e74be29272273929`) sind in dieser AXIOM-Sitzung NICHT als Originalbytes eingegangen. `AXIOM_INDEPENDENT_R21_CAPTURE_REHASH=NOT_PERFORMED`; `REAL_RAW_VALUES_ANALYZED_BY_AXIOM=0`.
- Gemeldeter Geräteträger: `OPPO_A74_CPH2219`; `com.nexusomega.maps` `1.3.11-alarm-identity-l1-vc15`; Device ID `oppo_a74_095974cd90ed22eb`; Session `r21-oppo-table-rest-20261109`; `SENSOR_START_STOP=EXECUTED_SCOPED_R21`; `STOP_ORIGIN=APP_DEADLINE`.
- Gemeldete Messung: `N=14018`, Dauer `70114 ms`, `ACC=7014`, `GYRO=7004`; arithmetisch `ACC≈100.04 Hz`, `GYRO≈99.89 Hz` auf **Sessiondauer-Basis**, *kein* verifizierter SensorEvent-Zeitstempel-Takt. Magnetometer nicht im Return.
- `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`, `CLAIM_PROMOTION=NO`, `BODYTWIN_VALIDATED=NO`, `PIXEL9A_FEMALE=RESERVED_NO_START`, `HOSTINGER_WRITE=NO`, `PR_MERGE=NO`. Auf GitHub kommen weder Roh-IMU-Werte noch Geheimnisse/Privatpersonen/Standortdaten.
- Wissenschaftlich: Der Android `TYPE_ACCELEROMETER` enthält die Gravitationskomponente; `TYPE_GYROSCOPE` meldet rad/s und ist bereits Android-/Hersteller-kalibriert. `TYPE_GYROSCOPE_UNCALIBRATED` wäre ein eigener Datentyp. Roh-Original im NEXUS-Kontext bedeutet **unveränderte Android-SensorEvents**, NICHT ungefilterte MEMS-Chip-ADC-Rohregister.
- Fehlende Originalbytes sind kein Freibrief zur Erfindung. `RECEIPT_REPORTED != BYTE_VERIFIED != SENSOR_VALIDATED != BODYTWIN_VALIDATED`. Positive und negative Tests sind zunächst PRE_REGISTERED, nicht bestanden.
- Owner-seitige research-only Branch-/PR-Publikation erteilt KEINEN neuen NEXUS-App-Lauf, kein ADB-Pairing, keinen neuen Agent-GitHub-Writer-Slot. Nachgelagerte Cursor-Dateiempfangsprüfung ist read-only; neue Messkampagne separat zu autorisieren.

