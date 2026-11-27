# 04 — Programm A: Abnahmekriterien der gemeinsamen Verarbeitungskette (L0–L3)

Zweck: konkrete, prüfbare Abnahmekriterien je Modul der Zielarchitektur (Order §4, §7.1). Jedes Kriterium
ist mit Gegenprobe und aktuellem Status versehen. Statusklassen wie Gap-Matrix. Diese Datei ist
**Design + Teilausführung** (die mit Fixtures prüfbaren Kriterien wurden in dieser Return ausgeführt:
`results/results_contract.json`, `results/results_js_precision.json`).

| Modul | Abnahmekriterium (messbar) | Gegenprobe | Status |
|---|---|---|---|
| Sensor Capture | Gemessene Nenntaxtrate ±10 %; Lücken >50 ms explizit als `gap`-Ereignis; Duplikate (identische Bytes) als `duplicate`; Einheiten SI-Enum | Gap-/Duplikat-Fixtures; Rate-Zähler gegen `sequence`-Differenz | SOURCE_GAP (Gerät) — Fixtures offline geprüft (8/8) |
| Temporal Anchor | `sensor_monotonic_ns` als DECIMAL_INTEGER_STRING; Monotonie je Stream; Clock-Offset nur als Intervall mit Unsicherheit; kein Precision-Promotion | JS-Präzisionsprobe 10/10 (Kollision bei 2^53+1; Literal-Verlust im Quelltext nachgewiesen) | OFFLINE_TESTED |
| Calibration | `calibration_sha256` bindet Bias/Skalierung/Achsen; manipulierte Kalibrierung muss Chunk-Validierung scheitern lassen | Tamper-Fixture auf Kalibrierhash | DESIGN_ONLY (Gerätequelle fehlt) |
| Observability | Zielgröße explizit; Rang/Konditionierung der Beobachtungsmatrix; leere Feasible-Set ⇒ `UNKNOWN`, nie Inferenz | Degenerate-Bewegungs-Fixture | SOURCE_GAP |
| UKF/SR-UKF | Modell- und Kovarianzparameter versioniert; byteidentischer Output für identische Eingabe | Golden-Replay | SOURCE_GAP (Produktionsquelle) |
| NIS | Dimension korrekt; Innovationskovarianz + Abhängigkeitsstruktur dokumentiert; χ²-Verträglichkeit je Dimension | Falsche-Dimension-Probe muss flaggen | SOURCE_GAP (historische NIS nicht neu bewertet, Order §13) |
| NEES | Nur mit unabhängiger Zustandsreferenz; ohne Referenz Feld absent | Abwesenheits-Assertion | SOURCE_GAP |
| Ω und k* | Versionierte deskriptive Größen; keine Claim-Promotion durch Vertragsvalidierung | Promotion-Versuch muss abgelehnt werden | ARCHITECTURE_READY (Vertragsregel vorhanden) |
| Falsifikation | Nullmodelle, Negativkontrollen, unabhängige Holdouts je neuer Metrik | Register der Negativkontrollen, kein stiller Pass | Teilweise (§2.1-Klassen RED/GREEN 10/10+10/10) |
| Evidence Kernel | Provenienz + Integrität; Receipt-Kette sha-verkettet; Manipulation irgendeines Glieds bricht Kette | Ketten-Verifikationstest | OFFLINE_TESTED (RECEIPTS/ R00–R05 dieser Return) |
| Public Projection | Nur Allowlist; 0 Rohfelder; 304 aktualisiert nie Ereigniszeit | Leak-Scan; Frische-Proben 6/6 | OFFLINE_TESTED |

Explizite Grenze: NIS/NEES-Werte sind **nie** alleiniger Beweis korrekter Zustandsschätzung (Order §7.1);
Coverage, Rauschmodell und beobachtbare Zielgröße sind mit zu führen. `Ω`/`k*` bleiben deskriptiv (C1).
