# NEXUS OMEGA — R21 physikalisch-wissenschaftliche Expertenrunde WAVE01
`OBJECT=NEXUS_OMEGA_AXIOM_R21_OPPO_PHYSICAL_SCIENCE_EXPERT_WAVE01_20261109_R0`
`STATE=OWNER_ISSUED_EIGHT_INDEPENDENT_PHYSICAL_RESEARCH_MANDATES_NOT_EXECUTED`
`BASE_COMMIT=dbbb7411271b5653bccab2aba9176ee2b34b3c91`
`CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`

Dies ist das abgeschlossene **Auftragspaket**, nicht ein abgeschlossener Agenten-Return. Ziel ist die unabhängige wissenschaftliche Analyse der erstmals von Cursor berichteten physikalischen OPPO-Sensoraufnahme, einschließlich überprüfbarer Metrologie und deterministisch falsifizierbarer Fehlerhypothesen. Jeder Agent liefert eine eigene vollständig dokumentierte Weiterentwicklungsfassung (00–10), keine bloße Rezension. Der originale 70-s-R21-Rohdatenstream ist noch nicht unabhängig bei AXIOM empfangen.

## Kanonische Bindung — keine falsche Evidenzpromotion
- `R18_SOFT_VISUAL=PRESERVED`; `R19_FOUNDATION=PRESERVED`; `R20=CLOSED_C1_WITH_MATERIAL_CAVEATS`. R21-Operator-Physical-Capture-Order PR #349, Head `033298ccf6375654f3783d819b0af012f4cc748e`; PR #348 R21 Read-only, Head `1300dcb257e5dc75a7de9f011cda82951e676924`; beide Draft/unmerged beim Intake.
- Cursor-Messreturn: `STATE=PASS_WITH_MATERIAL_CAVEATS_C1_PHYSICAL_OPPO_IMU_CAPTURE_PROVEN`; dies ist *Cursor-berichtete* Provenienz. Der Original-Export (`166349 B / 3eb9e9e9988b66994429d97e566a71aa2c05bbe951f41725465947841a75a9a4`), Segment-NDJSON-GZ (`166831 B / 544f762cbaab3cd562d8cf868cc15fbee1d23b503b72455c015e6698c02c90e2`) und Return-ZIP (`5337 B / e718438aa23b03ce978e1923423ec1e02f42d93887051b64e74be29272273929`) sind in dieser AXIOM-Sitzung NICHT als Originalbytes eingegangen. `AXIOM_INDEPENDENT_R21_CAPTURE_REHASH=NOT_PERFORMED`; `REAL_RAW_VALUES_ANALYZED_BY_AXIOM=0`.
- Gemeldeter Geräteträger: `OPPO_A74_CPH2219`; `com.nexusomega.maps` `1.3.11-alarm-identity-l1-vc15`; Device ID `oppo_a74_095974cd90ed22eb`; Session `r21-oppo-table-rest-20261109`; `SENSOR_START_STOP=EXECUTED_SCOPED_R21`; `STOP_ORIGIN=APP_DEADLINE`.
- Gemeldete Messung: `N=14018`, Dauer `70114 ms`, `ACC=7014`, `GYRO=7004`; arithmetisch `ACC≈100.04 Hz`, `GYRO≈99.89 Hz` auf **Sessiondauer-Basis**, *kein* verifizierter SensorEvent-Zeitstempel-Takt. Magnetometer nicht im Return.
- `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`, `CLAIM_PROMOTION=NO`, `BODYTWIN_VALIDATED=NO`, `PIXEL9A_FEMALE=RESERVED_NO_START`, `HOSTINGER_WRITE=NO`, `PR_MERGE=NO`. Auf GitHub kommen weder Roh-IMU-Werte noch Geheimnisse/Privatpersonen/Standortdaten.
- Wissenschaftlich: Der Android `TYPE_ACCELEROMETER` enthält die Gravitationskomponente; `TYPE_GYROSCOPE` meldet rad/s und ist bereits Android-/Hersteller-kalibriert. `TYPE_GYROSCOPE_UNCALIBRATED` wäre ein eigener Datentyp. Roh-Original im NEXUS-Kontext bedeutet **unveränderte Android-SensorEvents**, NICHT ungefilterte MEMS-Chip-ADC-Rohregister.
- Fehlende Originalbytes sind kein Freibrief zur Erfindung. `RECEIPT_REPORTED != BYTE_VERIFIED != SENSOR_VALIDATED != BODYTWIN_VALIDATED`. Positive und negative Tests sind zunächst PRE_REGISTERED, nicht bestanden.
- Owner-seitige research-only Branch-/PR-Publikation erteilt KEINEN neuen NEXUS-App-Lauf, kein ADB-Pairing, keinen neuen Agent-GitHub-Writer-Slot. Nachgelagerte Cursor-Dateiempfangsprüfung ist read-only; neue Messkampagne separat zu autorisieren.


## Paketinhalt
`00_R21_PHYSICAL_SOURCE_REGISTER.md`; `01_PRIMARY_PHYSICS_SOURCES.md`; `02_METROLOGY_MATH_AND_GATES.md`; `03_PRE_REGISTERED_CONTROLS.md`; `04_AGENTS_RETURN_AND_CROSS_REVIEW.md`; `05_CONFIRMATORY_DESIGN.md`; acht `orders/AI01..AI08`; `orders/CURSOR_RECEIVER_READ_ONLY.md`; `TASK_ORDER_ANCHOR.json`. `MANIFEST_SHA256.json` enthält detached SHA-256/Bytezahlen aller dokumentierten Kinddateien außer sich selbst.

## Kritische nächste Aktion
**Zuerst** den echten lokalen Export und das separate Cursor-Return im privaten Operator-Kanal bytegetreu an AXIOM liefern; unabhängig hashen, SensorEvent-Typen/Schemapfad rekonstruieren, Ereigniszeitstempel pro Sensor prüfen. Solange dies aussteht, können Experten die physikalische Methodik erforschen, aber keine gemessenen Bias-/Allan-/Driftwerte oder erfolgreichen Datenreplikationen behaupten. Alle künftigen realen Messversuche benötigen einen konkreten Auftrag; keine neue Aufnahme durch Publikation dieses Briefs.
