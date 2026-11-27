# Quellenregister — R46-4 RETURN (GLM-Lane), Stand 2026-11-27

## A. Auftrag und Parent-Evidenz (interner Kanon, NEXUS-OMEGA-EVIDENCE)

- `R46_4_EXTERNAL_OPPO_REFERENCE_METROLOGY_ORDER_R0` — Order-ZIP, Issue #476, Draft-PR #477 (Repo nexusomegac27/NEXUS-OMEGA-EVIDENCE, HEAD f39aeeb2). Eingangsintegrität 12/12 Mitglieder gegen `99_SHA256SUMS.txt` des Order-ZIP verifiziert.
- R21-Parent-Aggregate (aus `08_R21_PARENT_EVIDENCE.json` des Order-ZIP): acc n=7014, Dauer 70.022492373 s, Rate 100.15353299112422 Hz, M=9.832738001091458, S=0.009171945499113295; gyro n=7004, M=0.0019802113232776307, S=0.000664483224551047; g0=9.80665 (Standard-Schwerekonstante, BIPM).
- R46-3-Stack (getragene Konventionen): `R46_3_*_GLM_R1`, Draft-PR #473, Issue #470-Kommentar, von der Nutzerverwaltung „mit Auflagen angenommen“.

## B. Metrologie und Statistik (Öffentlich, prüfbar via DOI)

1. **JCGM 100:2008(E)** — GUM: Guide to the Expression of Uncertainty in Measurement. DOI `10.59161/JCGM100-2008E`. → Typ-A/Typ-B-Trennung, Unsicherheitsbudget-Formalismus (Abschnitt C des Reports).
2. **JCGM 101:2008** — GUM-Supplement 1, Monte-Carlo-Verfahren zur Unsicherheitsfortpflanzung. DOI `10.59161/JCGM101-2008`. → Rechtfertigung der MC-Kontrollläufe (2e6 Trials) und der 3-SE-Toleranzlogik (D02).
3. **NIST J Res 126:038 (2022)** — Kalibrierung dreiaxialer Beschleunigungssensoren. DOI `10.6028/jres.126.038`. → Multi-Posen-Kalibrierung, Scale/Bias/Orthogonalität, Referenzdominanz-Anforderung (W20/W21).
4. **Metrologia/Meas. Sci. Technol. 2026** — Referenzmetrologie für Consumer-IMU. DOI `10.1088/1681-7575/ae5193`. → Referenzketten-Hierarchie, Rückführbarkeit.
5. **Sensors 2023, 23(17), 7609** — Smartphone-/Wearable-Sensor-Kalibrierung ohne spezialisierte Hardware. DOI `10.3390/s23177609`. → Multi-Posen-Designs, Konditionszahlen, Passungs-Gauge (W15–W19).
6. **Measurement 2025, 117929** — SVD-basierte Kalibriermatrix-Extraktion. DOI `10.1016/j.measurement.2025.117929`. → Eigen-/Singulärwertstruktur der Designmatrizen (W15–W18: Ränge, Eigenwerte tetra/six/planar).
7. **Opt. Express / angew. Optik 2024 (PMC11679551)** — Kalibrierte Bildmessung: Design-, Schätz- und Abtastunsicherheit. DOI-basis `PMC11679551`. → Trennung Design-/Estimations-/Messunsicherheit als Vorbild für unsere Klassen T1/T2/T3.
8. **CRLB-Beitrag, Opt. Commun. 2025** — Cramér-Rao-Grenze für Kalibrierparameter. Art.-ID `S0924424725011069`. → Varianzschranken für Scale/Bias bei endlichem Posenbudget.
9. **arXiv 2606.06308 (2026)** — Gauge-Freiheitsgrade in Optimierung mit Rotationsparametern. → Gauge-Analyse W19 (Rotation um [1,1,1] ändert A bei O(Winkel), Beobachtungsresiduum unverändert).
10. **Android Developer Docs: SensorEvent / TYPE_ACCELEROMETER, TYPE_GYROSCOPE** — Datenerzeugung, Latenz, Einheiten, Timestamp-Semantik. → Kanal-Konventionen des Evidence-Contracts (PHYSICAL_ACC/PHYSICAL_GYRO), Zeitreihen-Regeln (AC-N6).

## C. Verwendungsnachweis ( Witness → Quelle )

| Witness | Primärquelle(n) |
|---|---|
| W01/W02 (Inversion, erfcx, GH, MC) | JCGM 101 (MC-Logik), eigene Validierung (D01) |
| W03/W04 (Ratios) | Parent-Aggregate, Order-Referenz `04_REFERENCE.js` |
| W05/W19 (Modell-Äquivalenz, Gauge) | arXiv 2606.06308, Sensors 2023 |
| W06/W07/W08 (Schranken, Folded Normal) | eigene Analysis; JCGM 100 (Verteilungsformalismus) |
| W09 (ULP-Einheiten) | IEEE-754-Arithmetik, Order-Vorgabe |
| W10–W18 (Ränge, Kondition, D/E/A) | Measurement 2025 117929, NIST 2022 |
| W20/W21 (Referenzdominanz) | NIST 2022, Metrologia 2026 |
| W22 (Budget) | JCGM 100, CRLB 2025, Android SensorEvent |
| W23–W34 (Contract) | PMC11679551 (Klassenlogik), interne Konventionen R46-3 |

## D. Abgrenzung

- Alle DOIs/Basen wurden im Zuge von R46-3 bzw. R46-4 recherchiert und inhaltlich auf die hier zitierten Punkte geprüft; Zahlenwerte in `04_RESULTS.json` stammen ausschließlich aus der eigenen deterministischen Rechnung, nicht aus Quellen.
- Keine Quelle liefert OPPO-Gerätespezifika; alle gerätespezifischen Größen sind als `NOT_COMPUTED` ausgewiesen (`09_RESOURCE_RECEIPT.json`).
