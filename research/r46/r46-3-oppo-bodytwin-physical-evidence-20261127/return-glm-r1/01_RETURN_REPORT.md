# NEXUS Ω OMEGA — R46-3 Return: Physische Evidenz, Informationsgehalt und Identifizierbarkeit

OBJECT=NEXUS_OMEGA_VIBE_R46_3_EXPERT_RETURN_GLM_R1_20261127_R0 · CLAIM_CEILING=C1_DESCRIPTIVE_ONLY · 2026-11-27

## Frage

Was stützt die historische R21-Ruhemessung (OPPO, 9. November 2026, 7.014 ACC- und 7.004 GYRO-Ereignisse, ausschließlich Aggregatdaten) wissenschaftlich tatsächlich — und welche Größen sind daraus prinzipiell nicht identifizierbar? Daraus abgeleitet: Welche Mindestfelder und Vertragsregeln braucht die künftige OPPO → NEXUS_APP → BodyTwin-Evidenzlinie?

## Executive Summary

1. **Arithmetik stabil, Evidenz dünn.** Effektivraten und die Residualidentität reproduzieren sich exakt (rel. Abweichung 0 bzw. 1.3e-14), aber die 14.018 Sensorereignisse werden auf 16 publizierte Skalare verdichtet (Faktor 3504.5, W08). Die Aggregate bestimmen die zeitliche und richtungsmäßige Struktur des Sensorrauschens nicht.
2. **"0 Lücken" beweist nicht Verlustfreiheit.** Ein deterministischer Gegenzeuge zeigt: 81 Einzelausfälle auf 7.095 geplante Ereignisse erzeugen null Lücken über der 5×Median-Schwelle (W09). Die Schwelle ist konstruktiv lückenblind.
3. **Per-Achsen-Rauschen ist modellebunden.** Radiales und isotropes Modell liefern σ_axis ≈ 0.0091719 m/s² (unter 1e-6 relativ gleich), unterscheiden sich aber im implizierten |g+b| um ≈ 8.6e-6 m/s². Allgemein identifiziert die Betrags-SD nur die Projektion e_g'·Σ·e_g der Rauschkovarianz auf die Gravitationsrichtung — niemals die volle Achsen-Kovarianz (W11/W12). Die Prereg-Erwartung eines √3-Faktors wurde dabei durch die Ausführung **widerlegt** und als Falsifikation dokumentiert (F10).
4. **Orientierung ist unheilbar unsichtbar.** Unter dem Gravity-only-Modell ist a_meas gegen Yaw um die Gravitationsachse exakt invariant (Gitterzeuge, 1441 Punkte, max. Abweichung 0); unter SO(3) bleibt nur der Betrag invariant (W16). Keine BodyTwin-Orientierung aus stationären Betragsaggregaten.
5. **Der g-Offset ist signifikant, aber nicht attribuierbar.** mag_mean liegt 0.026088 m/s² über dem konventionellen g0 (z ≈ 238 gegen die statistische Unsicherheit des Mittels); ob Bias, Neigung, Skalierung oder lokales g dafür verantwortlich ist, ist nicht identifizierbar → KORREKTUR-ABSTAIN (W19).
6. **Der Evidenzrahmen hält sechs Vertragsverletzungen zuverlässig ab** (historisch-als-live, Producer-Tick-Refresh, Body-Pose-aus-Tisch, synthetisch-als-physisch, Quell-Hash-als-Wahrheit, stale/unknown-Vermischung) bei bestehenden Positivkontrollen (Non-Vacuity, W20–W25).

## Methodik

- **Eingaben:** ausschließlich die autorisierten Aggregatdaten aus 02_EVIDENCE.json am gepinnten HEAD d7e1c95d…, der Order-Text (13.733 B) und das versiegelte Order-ZIP (22.619 B; SHA-256 gegen den publizierten Sidecar-Wert e3a3c946… geprüft). Keine Rohdaten, keine Raw-Digests, kein Gerätezugriff, keine neue Erfassung.
- **Preregistrierung:** 25 Prüfungen (W01–W25) wurden vor der Ausführung in 02_PREREG.md eingefroren (SHA-256 im 04_RESULTS.json vermerkt, nur lokal notiert). Ausführung in einem deterministischen, offline Läufer (03_WITNESSES_RUNNER.js) ohne Zufallsgeneratoren.
- **Unabhängigkeit:** eigene Implementierung und eigene Kennzeichnung (Lineage GLM_R1); Vorläuferstacks dienten als mentale Vorlage, ihre Zahlen wurden nicht reutilisiert.
- **Evidenzdisziplin:** jeder Wert wird einer Klasse zugeordnet (E0 physisch / E1 abgeleitet / E1 modellconditional / E2 synthetisch / Producer-reported / Source-Gap / NOT_COMPUTED); 05_EVIDENCE_FRAME.json klassifiziert jeden R21-Skalar.
- **Grenzen der Methode:** synthetische Zeugen prüfen mathematische Informationsgrenzen, nicht die echte OPPO-Messung; Aggregate gestatten keine Aussage über Intervallverteilungen, Whitening oder Drift.

## Befunde

### A — Aggregat-Audit (E1, direkt abgeleitet)

| Größe | Ergebnis | Prüfung |
|---|---|---|
| ACC-Effektivrate | 100.15353299112422 Hz (rel. Diff. 0) | W01 |
| GYRO-Effektivrate | 100.15354838260195 Hz (rel. Diff. 0) | W02 |
| Median-Kehrwert | 100.1533648475911 Hz, −1.679 ppm gegen effektiv; nur rekordiert | W03 |
| Dauer-Residuum | ACC −0.1176 ms, GYRO −0.1281 ms gegen (N−1)·Median | W04 |
| Rate-Überschuss | +0.15353 % / +0.15355 % gegen angeforderte 100 Hz | W05 |
| Residualidentität | \|9.832738001091458 − 9.80665\| = 0.026088001091459034 stimmt mit dem berichteten Wert auf 1.3e-14 relativ überein | W06 |
| Residual-Lesart | \|mean−g0\| ≠ mean\|x−g0\|: Gegenbeispiel 0 gegen 0.1 konstruiert | W07 |
| Informationsbilanz | 56.072 rohe Zahlenfelder → 16 Skalare (0.0285 %, Faktor 3504.5) | W08 |
| Lückenblindheit | 81 Einzelausfälle, 0 Lücken über 5×Median, max. Lücke = 0.400 der Schwelle | W09 |
| Phasenoffset | nicht ableitbar; Dauerdifferenz 0.099857448 s | W10 |

Die W06-Übereinstimmung belegt, dass der berichtete „gravity_residual_mean_abs" rechnerisch |mean−g0| ist. Ob daneben ein mittlerer absoluter Einzelfehler existiert, bleibt SOURCE_GAP. Wichtig ist die Größenordnung: unter beiden Rauschmodellen wäre E[|M−g0|] ≈ 0.0261, also nahe, aber nicht identisch zur berichteten Zahl — die beiden Größen unterscheiden sich hier nur um ≈ 1.2e-5 (W11). Das zeigt: aus den Aggregaten allein ist die Definition nicht entscheidbar, erst die Rohdaten wären es.

Die Lücken-Aussage wird symmetrisch gelesen: der Wert 0 schließt bis zu ≈ 1.15 % Einzelsampleverlust nicht aus (W09) und beweist keine Verlustfreiheit.

### B — Modellconditionale Größen (nur unter expliziter Modellannahme)

- **M1-RAD** (radial, |ν + σZ|): ν = 9.832738001091458, σ_axis = 0.009171945499229379, λ = ν/σ = 1072.04; P(M < g0) ≈ 0.00223; E[|M−g0|] ≈ 0.0261000 (W11).
- **M3-ISO** (3-D isotrop, nichtzentrales Chi k=3): ν = 9.832729445507752, σ_axis = 0.009171952483041588, δ = 1072.043 (W12). Die Modelle trennen sich im implizierten |g+b| um ≈ 8.56e-6 m/s².
- **Allgemeine Aussage:** für kleines Rauschen ist Var(M) ≈ e_g'·Σ·e_g. Die Betrags-SD identifiziert genau eine Zahl der Rauschkovarianz: die Projektion auf die Gravitationsrichtung. Drei strukturell verschiedene Kovarianzen (isotrop, z-dominant, x-dominant) reproduzieren die beobachtete Betrags-SD unter 1e-6 relativ und implizieren völlig verschiedene Achsen-Kovarianzen (W12). Daraus folgt hart: **keine Achsen-Kovarianz aus Betragsstatistiken.**
- **SD-Definition:** Population- vs. Stichproben-SD unterscheiden sich um 6.54e-7 m/s²; ddof ist undokumentiert (W13).
- **Statistische vs. attributable Unsicherheit:** SE des Mittelwerts ≈ 1.0952e-4 m/s²; der Offset 0.026088 ist also mit z ≈ 238 statistisch deutlich ungleich Null — aber die Attribution (Bias/Neigung/Skalierung/lokales g) ist nicht identifizierbar; jede g-Korrektur bleibt ABSTAIN (W19).

### C — Identifizierbarkeits-Zeugen (E2, synthetisch)

- **Zeitordnung:** identische Aggregate (n, mean, sd, Rate) bei volatil und geclustert geordneten Serien; Lag-1 unterscheidet sich (W14). Die R21-Aggregate tragen keine Information über die Autokorrelationsstruktur.
- **Richtung:** (0,0,10) und (10,0,0) teilen den Betrag (W15).
- **Yaw-Gauge:** unter a = Rᵀg + b ist a_meas für alle 1441 Yaw-Winkel exakt identisch (max. Abweichung 0); unter SO(3) bleibt nur der Betrag invariant (W16). Heading ist aus stationären Betragsaggregaten prinzipiell nicht rekonstruierbar.
- **Ein-Posen-Kalibrierung:** (scale=1, bias=0) und (scale=0.9, bias=1) liefern am Arbeitspunkt 10 denselben Output, bei −10 verschiedene (W17). Ein Posendatum kalibriert keine affine Kette.
- **Konsistenzregel:** Modell σ=0 mit beobachtetem sd>0 hat eine leere kompatible Menge → INCONSISTENT/ABSTAIN-Demo (W18).

### D — Datenvertrag und Integrität

- Sechs Vertragsverletzungen werden ausführbar REJECT-et, zwei Positivkontrollen bestehen (Non-Vacuity): W20–W25 in 03_WITNESSES_RUNNER.js.
- Ordenskonform: keine neuen physischen Erfassungen, keine APK-Installation, keine WWW-Schreibvorgänge, kein Cursor-Kontakt, keine privaten Rohdaten berührt. Die öffentliche BodyTwin-Route wurde in dieser Runde nicht abgerufen (Status NOT_FETCHED_SANDBOX, kein Outage-Claim).
- Integritätskette: Order-ZIP (22.619 B) SHA-256 = e3a3c946… (MATCH gegen Sidecar); Manifest der Order 8/8 Mitglieder geprüft; eigener Return-Stack mit Manifest 99_SHA256SUMS.txt und ZIP-Sidecar.

### E — Integrationsfundament

Zehn Befunde (F01–F10) mit Modulzuordnung, Abnahmekriterium, Falsifikator und Grenze sind in 06_INTEGRATION_MATRIX.json gebunden; die Evidenzanforderungsliste für den konsolidierten R46-9-Cursor-Return ist dort enthalten (je-Kanal-Zeitstempel, Frame-/Einheitendeklaration, ddof, Lücken-Histogramm, Allan-Rohdaten, APK/Kotlin/XML, Six-Position-Design, gemeinsame monotonic Zeitbasis).

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt aktualisiert |
|---|---|---|
| [Android SensorEvent API-Referenz](https://developer.android.com/reference/android/hardware/SensorEvent) | 5/5 | 2026 (laufend gepflegt) |
| [Sensors 2026, 26(15), 4685 — Static MEMS-IMU](https://doi.org/10.3390/s26154685) | 4/5 | 2026-07-23 |
| [IEEE MIM 2025 — Review of Smartphone Accelerometers](https://doi.org/10.1109/MIM.2025.11198885) | 4/5 | 2025-10-09 |
| [Sensors 2023 — Smartphone MEMS Measurement Errors](https://doi.org/10.3390/s23177609) | 4/5 | 2023 |
| [Sensors 2014 — Multi-Position-Kalibrierung](https://doi.org/10.3390/s140814885) | 4/5 | 2014-08 |
| [NIST SP 1065 — Handbook of Frequency Stability Analysis](https://www.nist.gov/publications/handbook-frequency-stability-analysis) | 5/5 | 2008 |
| [Piché — Online Tests of Kalman Filter Consistency](https://doi.org/10.1002/acs.2571) | 4/5 | - |
| [Montanari et al. — Functional Observability, PNAS](https://doi.org/10.1073/pnas.2113750119) | 4/5 | 2022 |
| [JCGM 100 (GUM)](https://doi.org/10.59161/JCGM100-2008E) | 5/5 | 2008 |
| [Android Sensors Overview](https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview) | 5/5 | 2026 (laufend gepflegt) |
| Order-Stack (02_EVIDENCE.json, 01_ORDER.md) @ HEAD d7e1c95d, Repo nexusomegac27/NEXUS-OMEGA-EVIDENCE | 3/5 (producer-reported Aggregate) | 2026-11-27 |

Konflikte und Einschränkungen: Die Sensors-2026-Studie stammt von einem anderen Gerät (Samsung Galaxy S22+, ca. 40 min) — kein Gerätevergleich mit OPPO, keine Whiteness-/Varianzübertragung; laut Order nur indexiert/auszugsweise geprüft. Zwei Quellen (Android SensorEvent, Sensors 2026) wurden in dieser Runde erneut geöffnet, die übrigen aus dem geprüften Order-Quellenfile übernommen. Pichés Jahreszahl war aus den verfügbaren Nachweisen nicht gesichert und bleibt offen ("-").

## Offene Fragen

1. Enthält der Original-Return tatsächlich einen mittleren absoluten Fehler (mean|x−g0|) oder nur |mean−g0|? (SOURCE_GAP, entscheidbar nur mit Originalberechnung/Rohdaten.)
2. Welche ddof-Konvention liegt mag_stdev zugrunde? (W13.)
3. Wie hoch ist der tatsächliche Sampleverlust im R21-Lauf? (0 Lücken sind damit unvereinbar nicht belegt, W09.)
4. Existiert eine gemeinsame Zeitbasis beider Kanäle? (Phasenoffset nicht ableitbar, W10.)
5. Ist die öffentliche BodyTwin-Route erreichbar und inhaltlich mit dem lokalen Produzenten-Empfang identisch? (nicht abgerufen.)

## Empfehlungen / Nächste Schritte

1. **R46-4 (Referenzmetrologie):** Six-Position-Design mit unabhängiger Winkellage und dokumentierter Unsicherheit als Design (keine Messfreigabe); Zielgröße e_g'·Σ·e_g durch per-Achsen-Design ersetzen.
2. **R46-5:** NIS erst mit tatsächlicher Innovationskovarianz; Nullmodelle (konstantes g, random walk) gegen UKF/SR-UKF stellen; NEES nur mit unabhängiger Referenz.
3. **R46-6:** gemeinsames monotonic-Zeitfundament; Lücken-Histogramm statt Schwellenzähler im Erfassungsmanifest (F03).
4. **R46-7:** die sechs Vertragstests (W20–W25) in den BodyTwin-Datenvertrag übernehmen; jede Anzeige mit Evidenzklasse + Formelfeld (F02).
5. **R46-9:** Evidenzanforderungsliste aus 06_INTEGRATION_MATRIX.json in den konsolidierten Cursor-Auftrag übernehmen.
6. **Adjudikation:** dieser Return liegt AXIOM zur Bewertung vor (NEXT = R46_3_RETURN_FOR_AXIOM_ADJUDICATION); keine Zwischenübergaben an Cursor.

---

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY · FORMALES_GATE_KREDIT = NONE · PHYSICAL_14_GATES = 0/14 · ALT_D ACTIVE · BODYTWIN_VALIDATED = NO · NEW_PHYSICAL_CAPTURE = NO · APK_INSTALL = NO · WWW_LIVE_WRITE = NO · INTERMEDIATE_CURSOR_HANDOFF = PROHIBITED · NEXT_CURSOR_HANDOFF = R46_9_SERIES_CLOSEOUT

NEXUS Ω OMEGA
