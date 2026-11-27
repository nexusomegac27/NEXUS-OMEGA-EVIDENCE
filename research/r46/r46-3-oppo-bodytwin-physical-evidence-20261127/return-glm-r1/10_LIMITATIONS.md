# Verbleibende Grenzen — R46-3 GLM_R1

## Ausdrücklich NICHT etabliert (Stand dieses Returns)
- Unabhängiges Rohdaten-Replay der R21-Messung (Rohdaten in privater Kustodie).
- Achsen-Kovarianz, Bias-Vektor, Skalierungsmatrix, Missalignment: aus Betragsstatistiken nicht identifizierbar (F04/W12).
- Whiteness, Drift, Allan-Charakteristik, effektive Stichprobengröße des realen Geräts.
- NIS/NEES: keine Innovationsmodell-Evidenz, keine unabhängige Zustandsreferenz.
- Konfidenzintervalle aus reinen Betragsstatistiken.
- Lokale g-Korrektur: statistisch signifikanter Offset (z ~ 238), Attribution nicht identifizierbar (ABSTAIN, W19).
- APK-Provenienz, Unit-Test-Semantik, Produktionsreife, BodyTwin-Validierung.
- Öffentliche BodyTwin-Route in dieser Runde nicht abgerufen; Status NOT_FETCHED_SANDBOX, kein Outage-Claim.

## Modellbindungen
- Alle W11/W12-Ergebnisse gelten nur unter dem jeweils angegebenen isotropen
  Small-Noise-Modell; allgemeiner identifiziert mag_stdev nur die Projektion
  e_g'·Sigma·e_g der Rauschkovarianz auf die (unbekannte) Gravitationsrichtung.
- Einheiten (ACC m/s², GYRO rad/s) sind an die korrekte Android-SensorEvent-Zuordnung
  gebunden, die für die konkrete App nicht unabhängig etabliert ist.

## Verfahrensgrenzen
- Die Prereg-Erwartung zu W12 (Faktor √3) wurde durch die Ausführung widerlegt;
  die Prereg-Datei blieb eingefroren, die Divergenz ist in 04_RESULTS.json dokumentiert.
- Prereg-Hash ist nur lokal notiert (nicht extern bezeugt).
- Die Sandbox bot kein sha256sum (defekt), keine crypto.subtle-Instanz und keinen
  ZIP-Stack; SHA-256 und ZIP-Bau wurden eigen implementiert und gegen bekannte
  Testvektoren sowie den publizierten Order-ZIP-Hash verifiziert.
- Batch-Abrufe des GitHub-Connectors waren instabil; Einzelabrufe erfolgreich.

## Kein Gate-Kredit
- Die 25 ausgeführten Prüfungen erzeugen keinen formalen Gate-Kredit und heben
  keinen Hold. Registrierte Designs R46-3-N01..N20/P01..P04 bleiben NOT_RUN.
