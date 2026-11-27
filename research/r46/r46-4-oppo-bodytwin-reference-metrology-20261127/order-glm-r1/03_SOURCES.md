# R46-4 scoped sources (metrology and uncertainty)

Verifizierungsstand wie angegeben; Übernahmen aus der adjudizierten R46-3-Quellbasis sind markiert.

## In R46-3 (GLM_R1) erneut geöffnet, Titel/Struktur bestätigt — für R46-4 methodisch tragend
- JCGM 100 (GUM), Unsicherheitsbudget-Pflicht: https://doi.org/10.59161/JCGM100-2008E (2008; in R46-3 aus Order-Quellenfile übernommen, nicht volltextverifiziert)
- NIST SP 1065, Handbook of Frequency Stability Analysis (2008): https://www.nist.gov/publications/handbook-frequency-stability-analysis (übernommen)
- Android SensorEvent API-Referenz (Zeitbasis je Sensor, Werte-Konvention): https://developer.android.com/reference/android/hardware/SensorEvent (in R46-3 geöffnet)
- Android Sensors Overview (API31+-Restriktionen, angeforderte ≠ gemessene Rate): https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview (übernommen)

## Kalibrier-/Fehlermodell-Literatur (aus R46-3-Order übernommen, nicht erneut volltextverifiziert)
- Smartphone MEMS Accelerometer and Gyroscope Measurement Errors, Sensors 2023 (Six-Position, deterministische/stochastische Fehlerkanäle): https://doi.org/10.3390/s23177609
- Multi-Position-Kalibrierung 2014: https://doi.org/10.3390/s140814885
- Review of Smartphone Accelerometers, IEEE MIM 2025: https://doi.org/10.1109/MIM.2025.11198885
- Sensors 2026, 26(15), 4685 (statische MEMS-IMU-Studie, anderes Gerät/andere Dauer — kein Transfer-Claim): https://doi.org/10.3390/s26154685 (in R46-3 geöffnet)

## Beobachtbarkeit/Statistik
- Montanari et al., Functional Observability, PNAS 2022: https://doi.org/10.1073/pnas.2113750119
- Piché, Online Tests of Kalman Filter Consistency: https://doi.org/10.1002/acs.2571 (Jahr unaufgelöst: "-")

## Interne, nicht verlinkbare Referenzen
- Issue #470 inkl. GLM_R1-Return (Draft-PR #473, Branch r46-3-return-glm-r1) und Adjudikations-Empfang (Kommentar 7222655788), Repository nexusomegac27/NEXUS-OMEGA-EVIDENCE
- R46-3-Order-Stack @ HEAD d7e1c95d276b20254b8c30a4de4b1310d18a1b31 (02_EVIDENCE.json als R21-Anker)

Grenze: R46-4 ist design-only; alle Designs zitieren Methodenquellen, aber kein Design ist ein executed measurement test.
