# Verifizierte Quellen und Quellenstand — R46-3 GLM_R1

Stand: 2026-11-27. Verifizierungsgrad je Quelle explizit angegeben.

## In dieser Runde erneut geöffnet (Volltextzugriff bestätigt)
- Android Developers, `SensorEvent` API-Referenz (Felder: `timestamp`, `values`, `accuracy`, `sensor`, `firstEventAfterDiscontinuity`): https://developer.android.com/reference/android/hardware/SensorEvent — in dieser Runde geöffnet, Titel und Feldstruktur bestätigt. Belegt: Zeitbasis je Sensor, Standardzuordnung ACC m/s², GYRO rad/s; keine Aussage über die konkrete App.
- Sensors 2026, 26(15), 4685 — "Precision and Error Propagation in Static MEMS-IMU Inertial Navigation: A Stochastic Time-Series Analysis", 23.07.2026, 36 S.: https://doi.org/10.3390/s26154685 — in dieser Runde geöffnet, Titel/Datum/Umfang bestätigt. Inhaltliche Grenze (laut Order-Quellenfile): ca. 40-minütige statische Studie an Samsung Galaxy S22+; keine Übertragung von Whiteness/Varianz auf OPPO 70 s oder auf Betrags-SD.

## Aus der Order (03_SOURCES.md @ d7e1c95d) übernommen, in dieser Runde nicht erneut volltextverifiziert
- Review of Smartphone Accelerometers for Usage in Research and Engineering, IEEE MIM 2025: https://doi.org/10.1109/MIM.2025.11198885 (indexiert; Sensorrauschen, Bias, Zeitstempel, Drift)
- Smartphone MEMS Accelerometer and Gyroscope Measurement Errors, Sensors 2023: https://doi.org/10.3390/s23177609 (Six-Position, deterministische/stochastische Fehlerkanäle)
- Multi-Position-Kalibrierung 2014: https://doi.org/10.3390/s140814885
- NIST SP 1065, Handbook of Frequency Stability Analysis (2008): https://www.nist.gov/publications/handbook-frequency-stability-analysis (Allan-Statistik; methodische Referenz)
- Piché, Online Tests of Kalman Filter Consistency: https://doi.org/10.1002/acs.2571 (NIS; benötigt tatsächliche Innovationskovarianz)
- Montanari et al., Functional Observability, PNAS: https://doi.org/10.1073/pnas.2113750119 (zielgerichtete Beobachtbarkeit, keine pauschale Poserekonstruktion)
- JCGM GUM: https://doi.org/10.59161/JCGM100-2008E (Unsicherheitsmodell-Pflicht)
- Android Sensors Overview (API31+-Restriktionen, angeforderte ≠ gemessene Rate): https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview

## Interne, nicht verlinkbare Referenzen (ohne öffentliche URL, bewusst ohne Link)
- Issue #470 (kanonischer Auftragseinstieg, Repository nexusomegac27/NEXUS-OMEGA-EVIDENCE, öffentlich abrufbar)
- 02_EVIDENCE.json @ HEAD d7e1c95d276b20254b8c30a4de4b1310d18a1b31 (R21-Aggregate, APK-/WWW-Blöcke)
- Order-Text NEXUSO~1.TXT (13733 B) und versiegeltes Order-ZIP (22619 B, SHA-256 geprüft)

## Public BodyTwin-Route
- https://www.nexus-mobile.de/bodytwin/ — in dieser Runde NICHT abgerufen (noetig gehaltene Grenze der Order: bounded receipts nur bei tatsächlichem Abruf); kein Outage-Claim, Status = NOT_FETCHED_SANDBOX.
