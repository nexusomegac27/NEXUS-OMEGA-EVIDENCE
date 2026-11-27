# Limitationen — R46-4 RETURN (GLM-Lane), 2026-11-27

## 1. Datenlage

- Diese Lane hat **keine OPPO-Rohdaten**: Alle Aussagen beziehen sich auf die R21-Parent-Aggregate (n=7014 acc / n=7004 gyro) und deren statistische Signatur. Einzelbeobachtungen waren nicht zugänglich.
- Keine physische Referenzmessung (0/14 physische Kette): Die lokale Gravitationsmagnitude am Aufstellungsort ist unbekannt; g0 = 9.80665 ist die Standard-Schwerekonstante, kein Messwert.

## 2. Methodische Grenzen

- **Doppelprecision**: Alle Rechnungen in IEEE-754 double. Die Inversion ist an der Lösungsstelle gut konditioniert, aber letzte-Bit-Effekte bleiben (W09: ULP-Granularität ~3.3e-16 absolut). Keine Arbitrary-Precision-Verifikation.
- **MC-Auflösung**: Bei N = 2e6 liegt die SD-Standardabweichung bei ~5e-4 relativ; kleinere Übereinstimmungen sind per MC nicht aufzeigbar. Die Aussagekraft der MC-Kontrollen endet dort.
- **Gauss-Hermite n=32**: Die 1D-Zerlegung ist an der Lösungsstelle exakt; moderate-λ-Zeilen sind kink-limitiert und dienen nur als Diagnostik (D03).
- **Simulation (W20/W21)**: Modellwelt mit Komponenten-Gauß-Rauschen (σ=0.001), LCG + Box-Muller, 1000 Trials. Sie belegt Referenzdominanz im Modell, keine Geräte-eigenschaft.

## 3. Strukturell nicht identifizierbar (T3)

- Kovarianzrichtung aus Betragsmomenten (W05): prinzipiell unmöglich, nicht nur praktisch.
- Absolute Orientierung ohne externe Referenz (W19): Gauge-Freiheitsgrad.
- 1-Posen-Bias entlang g: konfundiert mit Skala/Tilt (W22).

## 4. Nicht berechnet (NOT_COMPUTED)

σ pro Achse, Referenz-Orientierungsunsicherheit, lokale Gravitationsmagnitude, OPPO-Clock-Offset, Temperaturkoeffizienten (siehe 09_RESOURCE_RECEIPT.json). Jede Verwendung dieser Größen in R46-5 erfordert neue Messungen oder explizite Deklaration (Typ-B).

## 5. Verbindlichkeit

- Der Return bestätigt die **interne Konsistenz** der Parent-Aggregate und der AXIOM-Referenzwerte; er bestätigt **nicht** deren physische Korrektheit (dazu wäre die physische Kette nötig).
- Ceiling bleibt C1_DESCRIPTIVE_ONLY. Keine Coverage-Aussagen ohne deklarierte Verteilungsannahmen (JCGM 100/101).
- Prereg-Divergenzen D01–D04 sind vollständig deklariert; das Prereg-File wurde nach der Fixierung nicht verändert.
