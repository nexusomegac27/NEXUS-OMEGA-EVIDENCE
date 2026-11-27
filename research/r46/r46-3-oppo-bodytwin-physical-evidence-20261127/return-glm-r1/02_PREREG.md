# NEXUS Ω OMEGA — R46-3 Return · Preregistrierung (GLM_R1)

OBJECT=NEXUS_OMEGA_VIBE_R46_3_EXPERT_RETURN_GLM_R1_20261127_PREREG_R0
LINEAGE=VIBE_GLM_R1_FIRST_RUN (unabhängig von AUTOCLAW_R1; Vorläuferstacks nur als mentale Vorlage, keine Zahlenreutilisation)
FREEZE_UTC=2026-11-27T15:40:57Z (lokale Notarzeit, nicht extern bezeugt)
SCOPE=R46-3 Physical Evidence · Target Observability · OPPO NEXUS_APP · BodyTwin (strikt)

Diese Preregistrierung wurde vor Ausführung sämtlicher Prüfungen schriftlich fixiert.
Der SHA-256 dieser Datei wird nach der Ausführung in 04_RESULTS.json unter
`prereg.sha256` festgehalten. Änderungen nach der Ausführung sind verboten.

## Eingabegrundlage (aggregate-only, autorisiert)
- R46-3 Order-Text (NEXUSO~1.TXT, 13733 B) und versiegeltes Order-ZIP 22619 B
  SHA-256 e3a3c946a39ff0b9c0fe084080fbee103ad70f3b28becdddb0759792b47995d0.
- R21-Aggregate aus 02_EVIDENCE.json des gepinnten HEAD d7e1c95d276b20254b8c30a4de4b1310d18a1b31.
- KEINE Rohdaten, KEINE Raw-Digests, KEINE Gerätezugriffe, KEINE neue Erfassung.

## Vorab festgelegte Prüfungen (alle ausführbar in 03_WITNESSES_RUNNER.js)

### A — Aggregat-Arithmetik (E1, direkt aus veröffentlichten Aggregaten ableitbar)
- W01: ACC-Effektivrate f=(N-1)/T muss 100.15353299112422 Hz innerhalb 1e-9 relativ reproduzieren.
- W02: GYRO-Effektivrate f=(N-1)/T muss 100.15354838260195 Hz innerhalb 1e-9 relativ reproduzieren.
- W03: Kehrwert des Median-Intervalls 1/0.009984687 wird nur REKORDIERT (ppm-Klasse, kein MATCH-Claim).
- W04: Differenz Erfassungsdauer vs. (N-1)*Median-Intervall in ms wird nur REKORDIERT.
- W05: Abweichung angeforderte 100 Hz vs. effektive Rate in Prozent wird nur REKORDIERT.
- W06: |mag_mean_ACC - g0| mit g0=9.80665 wird exakt in float64 gegen
  gravity_residual_mean_abs_reported=0.026088001091459367 verglichen (Definiton Zeuge: |mean-g0|).
- W07: Gegenbeispiel konstruiert: |mean-g| kann 0 sein, während mean|x-g| > 0
  (Beleg: die beiden Groessen sind mathematisch verschieden).
- W08: Informationsbilanz: rohe numerische Felder (14018 Events x 4: Zeit + 3 Achsen) = 56072
  Zahlen gegen Anzahl publizierter Skalare; Verdichtungsfaktor wird REKORDIERT.
- W09: GAP-BLINDNESS-Zeuge: synthetische Serie mit 81 Einzelausfällen unter 7014 Samples,
  Median-Intervall identisch: max. Luecke = 2xMedian = 0.600 der 5xMedian-Schwelle,
  also 0 Luecken ueber der Schwelle TROTZ 1.15 % Ereignisverlust.
- W10: ACC/GYRO-Phasenoffset nicht ableitbar; Differenz der Erfassungsdauern wird REKORDIERT.

### B — Modell-conditional (M-COND; Modellannahme explizit, kein physikalischer Gate-Claim)
- W11: M1-RAD (rein radiales 1-D-Rauschmodell |g+b+n|, n~N(0,sigma)): aufloesen nach
  (nu, sigma) aus (mag_mean, mag_stdev); berichte lambda=nu/sigma, P(M<g0), E[|M-g0|].
- W12: M3-ISO (3-D isotropes Rauschen, Betrag nichtzentral-Chi k=3): SD(M) ca. sqrt(3)*sigma_axis;
  Konsequenz dokumentieren: die Zuordnung mag_stdev -> Achsenrauschen ist MODELLEBUNDEN
  (Faktor sqrt(3) zwischen radialem und isotropem Modell).
- W13: SD-Definition unbekannt: Population- vs. Stichproben-SD unterscheiden sich um
  sqrt(N/(N-1)); absolute Differenz wird REKORDIERT.

### C — Identifizierbarkeits-Zeugen (synthetisch, deterministisch)
- W14: identische Aggregate (n, mean, sd, Rate) bei unterschiedlicher Zeitordnung;
  normiertes Lag-1-Produkt unterscheidet sich.
- W15: gleicher Vektorbetrag, unterschiedliche Richtung ((0,0,10) vs (10,0,0)).
- W16: Yaw-Gauge unter Gravity-only-Modell a=R^T g + b: Rotation um die Gravitationsachse
  laesst a_meas exakt invariant (1441-Punkt-Gitter, Abweichung ~1e-15); Zufalls-SO(3):
  nur der Betrag bleibt invariant, die Vektorkomponenten nicht.
- W17: Ein-Posen-Affinambiguitaet: (scale=1,bias=0) vs (scale=0.9,bias=1) liefern bei
  Arbeitspunkt 10 identischen Output, bei -10 verschiedenen.
- W18: Konsistenzdemo: Modell sigma=0 mit beobachtetem sd>0 -> leere kompatible Menge (INCONSISTENT).
- W19: Implizierter Gravitations-Offset: statistische Unsicherheit von mag_mean unter M1-RAD
  = sd/sqrt(N); Attribution (Bias vs. Neigung vs. lokale g-Abweichung vs. Skalierung)
  nicht identifizierbar -> KORREKTUR-ABSTAIN.

### D — Vertrags-Negativfaelle (Evidenzrahmen, je 1 ausfuehrbarer Prueffall)
- W20: historic-labeled-live -> REJECT
- W21: producer-tick-age-refresh -> REJECT
- W22: body-pose-from-table -> REJECT
- W23: synthetic-as-physical -> REJECT
- W24: source-hash-as-truth -> REJECT
- W25: stale-unknown-conflation -> REJECT

## Vorab festgelegte Grenzen
- Kein Claim: Rohdaten-Replay, Achsen-Kovarianz, Bias-Vektor, Allan-Kurve, Whiteness,
  Drift, effektive Stichprobengroesse, NIS/NEES, Konfidenzintervalle aus reinen Betragsstatistiken,
  Kalibrierung, physikalische Validierung, Produktionsreife.
- CLAIM_CEILING = C1_DESCRIPTIVE_ONLY. CLAIM_PROMOTION = NO. FORMALES_GATE_KREDIT = NONE.
- Alle synthetischen Zahlen sind ausdruecklich als E2_SYNTHETIC markiert, nie als OPPO-Messung.
