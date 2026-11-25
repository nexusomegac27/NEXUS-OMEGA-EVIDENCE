# 03 · PROGRAMM A · Dynamische und datengetriebene funktionale Observabilitaet (E30, E32, E33)
STATUS = DESK_PREVALIDATION_EXECUTED, kein formales Gate-Credit, CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## A.1 Exakte Rangpruefung der GLM-Auswertung (Bruecke zu R45-4)
- Exakte rationale Rangpruefung ueber Bruchrechnung (BigInt-Frac): Projektionsraenge 7 (zwei Messrichtungen), 12 (drei), 15 (vier) exakt gleich der AXIOM-Korrektur; die GLM-Meldung 15/15/15 ist widerlegt.
- Ursache laut AXIOM und hier bestaetigt: certificate_and_witness nutzt unabhaengig von der Messrichtungszahl stets die vollstaendige Beobachtungsmatrix.
- Rowspace-Korrektur: c liegt genau dann im Zeilenraum, wenn A^T w = c loesbar ist oder die Raenge von [A; c^T] uebereinstimmen; ein Vergleich mit einzelnen Basisvektoren ist unzulaessig.

## A.2 Dynamisches Zielmodell (Zeit als zusaetzlicher Informationstraeger)
Zustand x = (a, b, h); a_{t+1} = a_t + lambda b_t; b_{t+1} = b_t + u_t; h_{t+1} = h_t; beobachtet nur y_t = a_t.

| Beobachtung | Rang | Zielgroesse b bestimmbar |
| --- | --- | --- |
| nur aktueller Messwert | 1 | Nein |
| zwei aufeinanderfolgende Messwerte | 2 | Ja |
| vollstaendiger Zustand, drei Komponenten | 2 von 3 | Nein |

Eigene exakte Verifikation: uebereinstimmend mit AXIOM Paragraf 4.1. Geschlossene Form b_t = (y_{t+1} - y_t)/lambda; die b-Schaetzung liegt erst mit der naechsten Beobachtung vor (Schaetzverzoegerung explizit ausgewiesen).

## A.3 Datenbasierte Zielschaetzung, eigene Replikation von AXIOM Paragraf 5
27 informative synthetische Trajektorien, 81 Designzeilen [y_t, y_{t+1}, u_t], Zielvektor z = y_{t+1} - y_t; Loesung der Normalgleichungen als Cramer-Resolvente.
Ergebnis w = (−1.0000000000000013, 0.999999999999999, −5.59e−16), also b_hat_t = 0*u_t − y_t + y_{t+1}, exakt zur 12. Stelle gleich der AXIOM-Angabe. Damit ist das festgelegte System lambda = 1 korrekt wiedergegeben.

## A.4 Modellambiguitaet und Drift
- Ambiguitaetszeuge bestaetigt: lambda = 1 mit b = 2 und lambda = 2 mit b = 1 erzeugen dieselbe Beobachtung (0, 2).
- Driftmodell (a, b, d): Rang 2, augmentiert um b_t + d Rang 3, Ziel nicht identifizierbar; mit unabhaengiger Driftreferenz Rang 3, Ziel identifizierbar. Gleich AXIOM Paragraf 6: y_{t+1} − y_t = b_t + d.

## A.5 Monte-Carlo-Empfindlichkeit (NUMERICAL_SENSITIVITY)
N = 20000, deterministischer LCG (eigener Desk-Lauf, Seed 45506), sigma = 0.01:

| lambda | RMSE gemessen | Theorie Wurzel(2)*sigma/|lambda| | relative Abweichung |
| --- | --- | --- | --- |
| 1 | 0.0141 | 0.014142 | ca. 0.29 Prozent |
| 0.1 | 0.1410 | 0.141421 | ca. 0.29 Prozent |
| 0.01 | 1.4101 | 1.414214 | ca. 0.29 Prozent |
| 0.001 | 14.1015 | 14.142136 | ca. 0.29 Prozent |

Struktur identifizierbar, numerisch um Faktor 1000 empfindlich. Kernbefund gleich AXIOM Paragraf 7; drei getrennte Nachweise erforderlich: strukturell, numerisch, empirisch. Ergaenzend bestaetigt: geringes Messrauschen kann eine historisch rangdefiziente Datenmatrix formal vollrangig erscheinen lassen.

## A.6 Bruecke zur Projektionsvarianz (R45-4 Formel)
Var(x_hat_2) = (1 + cos^2 theta − 2 rho cos theta)/sin^2 theta verifiziert: theta 45 Grad, rho 0 ergibt 3.000; theta 45 Grad, rho 0.9 ergibt 0.4544; theta 1 Grad, rho 0 ergibt 6565.279.

## A.7 Literaturanker, Beschraenkung der Uebertragung
- Zhang et al., arXiv:2512.06614 (7. Dezember 2025), datengetriebene funktionale Zustandschaetzung; Voraussetzungen: Persistency of Excitation, historische Zielmessungen, ausreichende Sequenzlaenge, Rausch- und Stabilitaetsannahmen. Leitsatz: Datengetrieben heisst nicht voraussetzungslos; Parameterfreiheit heisst nicht Annahmefreiheit.
- Zhang, Fernando, Darouach, IEEE TAC 2025, DOI 10.1109/TAC.2024.3462558: funktionale und strukturelle funktionale Observabilitaet, NP-Schwere der minimalen Sensorauswahl mit Approximationsverfahren.
- Van Waarde et al., IEEE TAC 2020, arXiv:1908.00468: Data Informativity.
- Jaiswal, Berger, Tomar, arXiv:2604.00680 (2026): verteilte partielle Zustandschaetzung.
- Wiley IJRNC 2026, DOI 10.1002/rnc.70475: Target Layer State Estimation in Multilayer Complex Dynamical Networks.
Alle Ansaetze sind systematisch einzeln zu pruefen; Uebertragung auf NEXUS-Geraete nur nach ANALOGY_NOT_IDENTITY.

NEXUS Ω OMEGA

