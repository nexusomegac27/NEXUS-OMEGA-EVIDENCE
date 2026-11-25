# 04 · PROGRAMM B · Robuste Beobachtungsauswahl unter unbekannten Parametern (E30 bis E33)
STATUS = DESIGN_ONLY, NOT_RUN_FORMAL. Das AXIOM-Register sieht 20 Negativ- und 4 Positivkontrollen vor.

## B.1 Designanker
- Minimale Sensorauswahl ist NP-schwer (Zhang, Fernando, Darouach, IEEE TAC 2025, DOI 10.1109/TAC.2024.3462558); jedes skalierbare Verfahren braucht eine Approximationsgarantie, keine reine Rangheuristik.
- Informativ statt schlicht: nach Van Waarde et al. (arXiv:1908.00468) ist eine Beobachtungsmenge informativ, wenn die gesuchte Eigenschaft aller mit den Daten vereinbarten Systeme festliegt. Das ist das Auswahlkriterium unter Modellambiguitaet.

## B.2 Eigene Desk-Schranken fuer das Design
- Numerische Empfindlichkeit sigma_b_hat = Wurzel(2) * sigma / |lambda|; Verifikation im Monte-Carlo-Lauf (siehe 03). Das Design muss die Konditionierung der Designmatrix mitpruefen, nicht nur den Rang.
- Drift als Stoergroesse: ohne unabhaengige, beschraenkte Driftreferenz bleibt die Zielgroesse nicht identifizierbar (Rang 2, Zielraum 3). Robuste Auswahl muss mindestens eine Koordinate enthalten, die die Driftkomponente unabhaengig begrenzt.
- Rauschen kann historisch rangdefizite Matrizen formal vollrangig erscheinen lassen (AXIOM Paragraf 7); daraus folgt fuer B: formale Ranggleichheit in Trainingsdaten ist kein Identifizierbarkeitsnachweis.

## B.3 Grenzen
Kein Optimierer ausgefuehrt, keine Hardware-Hypothese, keine FIT-, Energie- oder Hardwarewerte auf NEXUS-Geraete (OPPO, Pixel, Windows, Hostinger) uebertragen. Physische Tests nicht durchgefuehrt.

NEXUS Ω OMEGA

