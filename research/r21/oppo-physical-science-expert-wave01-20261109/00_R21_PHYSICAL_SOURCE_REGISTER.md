# R21 Source class ledger — first report-level physical observation
`OBJECT=NEXUS_OMEGA_R21_PHYSICAL_ORIGINALS_SOURCE_REGISTER_20261109_R0`

| Objekt | Berichtete Bytes / SHA-256 | Unabhängiger Status hier |
| --- | --- | --- |
| OPPO Roh-Export ZIP | 166349 / `3eb9e9e9988b66994429d97e566a71aa2c05bbe951f41725465947841a75a9a4` | NOT_IN_HAND / NO_REHASH |
| Sensorsegment NDJSON.GZ | 166831 / `544f762cbaab3cd562d8cf868cc15fbee1d23b503b72455c015e6698c02c90e2` | NOT_IN_HAND / NO_REHASH |
| Cursor Rückgabe ZIP | 5337 / `e718438aa23b03ce978e1923423ec1e02f42d93887051b64e74be29272273929` | NOT_IN_HAND / NO_REHASH |
| Original R21 Order ZIP | 13956 / `15fd4a8d9b8db1700c460ddc6806d4641f8485ad18f70b79fcf836e736aae94c` | Voriger AXIOM-Order; durch Cursor MATCH berichtet |

Device: OPPO A74 CPH2219; app `com.nexusomega.maps` version `1.3.11-alarm-identity-l1-vc15`; `device_id=oppo_a74_095974cd90ed22eb` **reported**. `session_id=r21-oppo-table-rest-20261109`; captured local-only; stop APP_DEADLINE.
Duration = 70114 ms; N accel = 7014; N gyro = 7004; total = 14018. **Nominal session-basis rates** = 100.04/s, 99.89/s, 199.93 combined/s. These are NOT raw timestamp rates; no confidence interval and no device readback available.
`SENSOR_START_STOP=EXECUTED_SCOPED_R21` and `PHYSICAL_OPPO_IMU_CAPTURE_PROVEN` are Cursor-reported experiment states. This package does not certify them independently.

## Required immutable byte custody for source escalation
Receive raw ZIP as byte-preserved private object; recompute SHA-256 and bytes BEFORE extraction. Record transport identity, acquisition/app/device hash and host receipt. Then verify inner GZIP SHA and decompress deterministically with size limits, reject path traversal/zip bombs and nonfinite JSON; count each typed event. Preserve raw unchanged; create derivative summary separately. Pin original native `timestamp_ns` per event and source `sensor.type, id, unit, accuracy, values`; record whether values were already corrected by Android HAL. If data absent, `RECEIVER_ACK=INCOMPLETE_SOURCE_GAP`, not PHYSICAL PASS.

## Negative source-edge conditions
Hash mismatch, device ID mismatch, different session ID, contradictory boot clock, duplicate seq, per-sensor nonmonotonic time, sample type mislabeled, compression transform undocumented, key-less redaction, event-count mismatch, missing uncompressed byte hash, stop timestamp not equal event bounds, insufficient privacy, created-file-mtime misused as sensor time.
## Kanonische Bindung — keine falsche Evidenzpromotion
- `R18_SOFT_VISUAL=PRESERVED`; `R19_FOUNDATION=PRESERVED`; `R20=CLOSED_C1_WITH_MATERIAL_CAVEATS`. R21-Operator-Physical-Capture-Order PR #349, Head `033298ccf6375654f3783d819b0af012f4cc748e`; PR #348 R21 Read-only, Head `1300dcb257e5dc75a7de9f011cda82951e676924`; beide Draft/unmerged beim Intake.
- Cursor-Messreturn: `STATE=PASS_WITH_MATERIAL_CAVEATS_C1_PHYSICAL_OPPO_IMU_CAPTURE_PROVEN`; dies ist *Cursor-berichtete* Provenienz. Der Original-Export (`166349 B / 3eb9e9e9988b66994429d97e566a71aa2c05bbe951f41725465947841a75a9a4`), Segment-NDJSON-GZ (`166831 B / 544f762cbaab3cd562d8cf868cc15fbee1d23b503b72455c015e6698c02c90e2`) und Return-ZIP (`5337 B / e718438aa23b03ce978e1923423ec1e02f42d93887051b64e74be29272273929`) sind in dieser AXIOM-Sitzung NICHT als Originalbytes eingegangen. `AXIOM_INDEPENDENT_R21_CAPTURE_REHASH=NOT_PERFORMED`; `REAL_RAW_VALUES_ANALYZED_BY_AXIOM=0`.
- Gemeldeter Geräteträger: `OPPO_A74_CPH2219`; `com.nexusomega.maps` `1.3.11-alarm-identity-l1-vc15`; Device ID `oppo_a74_095974cd90ed22eb`; Session `r21-oppo-table-rest-20261109`; `SENSOR_START_STOP=EXECUTED_SCOPED_R21`; `STOP_ORIGIN=APP_DEADLINE`.
- Gemeldete Messung: `N=14018`, Dauer `70114 ms`, `ACC=7014`, `GYRO=7004`; arithmetisch `ACC≈100.04 Hz`, `GYRO≈99.89 Hz` auf **Sessiondauer-Basis**, *kein* verifizierter SensorEvent-Zeitstempel-Takt. Magnetometer nicht im Return.
- `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`, `CLAIM_PROMOTION=NO`, `BODYTWIN_VALIDATED=NO`, `PIXEL9A_FEMALE=RESERVED_NO_START`, `HOSTINGER_WRITE=NO`, `PR_MERGE=NO`. Auf GitHub kommen weder Roh-IMU-Werte noch Geheimnisse/Privatpersonen/Standortdaten.
- Wissenschaftlich: Der Android `TYPE_ACCELEROMETER` enthält die Gravitationskomponente; `TYPE_GYROSCOPE` meldet rad/s und ist bereits Android-/Hersteller-kalibriert. `TYPE_GYROSCOPE_UNCALIBRATED` wäre ein eigener Datentyp. Roh-Original im NEXUS-Kontext bedeutet **unveränderte Android-SensorEvents**, NICHT ungefilterte MEMS-Chip-ADC-Rohregister.
- Fehlende Originalbytes sind kein Freibrief zur Erfindung. `RECEIPT_REPORTED != BYTE_VERIFIED != SENSOR_VALIDATED != BODYTWIN_VALIDATED`. Positive und negative Tests sind zunächst PRE_REGISTERED, nicht bestanden.
- Owner-seitige research-only Branch-/PR-Publikation erteilt KEINEN neuen NEXUS-App-Lauf, kein ADB-Pairing, keinen neuen Agent-GitHub-Writer-Slot. Nachgelagerte Cursor-Dateiempfangsprüfung ist read-only; neue Messkampagne separat zu autorisieren.
