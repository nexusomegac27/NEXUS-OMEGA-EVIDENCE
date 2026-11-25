# 03 EXECUTED SCRIPT VERSIONS (E34 Fehlerarchiv)

Alle Skriptversionen der R44-7-Ausfuehrung MISTRAL/VIBE. Die Endfassung v4 wurde fuer alle 8000 Fits verwendet. Alle frueheren Versionen sind dokumentiert, nicht geloescht, und wurden fuer keine gebundenen Befunde verwendet.

## Versionshistorie

- v1 (VERWORFEN): Gauss-Newton mit Schrittfaktor-2-Fehler (Schritt doppelt so gross wie die aufgeloeste Richtung); divergierte an den Grenzen. Kein Ergebnis gebunden.
- v2 (VERWORFEN): Modellwechsel auf a t / (b + t) + c t; 400/400 Konvergenz, aber flache a-gegen-b Skalierkante auf reinem t-Gitter, Schaetzer an oberer Grenze. Modell verworfen.
- v3 (VERWORFEN): sin-Modell (final), aber Gauss-Newton ohne Restkraemmungsterm im Pilot von Arm A: 2000/2000 MAXITER; das gewichtete nichtlineare Problem hat ein gekruemmtes Tal, GN-Schritte werden dauernd verworfen, die Daempfung pendelt.
- v4 (AKTUELL): exakter Newton-Restkraemmungsterm (fuer f = a sin(b t) + c t geschlossen darstellbar: einzige nichtverschwindende zweite Ableitungen sind ab = t cos(b t) und bb = -a t^2 sin(b t)); LM-Daempfung beibehalten; Abbruch: step < 1e-12 ODER lam >= 1e12 ODER gn < 1e-7 ODER Objektiv-Stall (abs delta o < 1e-13 multipliziert mit max(1,|o|) nach Iteration 5). Kalibrierung: 400/400 CONV, 0 Randtreffer. Vollausfuehrung: 8000/8000 CONV.

## Deterministik

- RNG: Parks-Miller LCG (Multiplikator 16807, Modulo 2147483647, seed 20261125), Box-Muller-Verfahren mit Polarform, gemeinsame Zufallszahlen: ein Generator, Ziehungsreihenfolge je Repetition narrow(10) dann wide(20); jeder Arm liest denselben Stream (armweise Programme replizieren den Stream identisch).
- Kovarianz: AR(1) rho 0.8, sigma 0.1, bekannt; Zuege ueber Cholesky der Kovarianzmatrix; W = Inverse der Kovarianz; Cholesky-Faktor L von W; OLD-Whitening r_w = L r; COR-Whitening r_w = L^T r.
- Schaetzer: Start (1.0, 2.0, 0.2), Grenzen mit Projektion, oben genannter Abbruch. Zielgroessen wie Praeregistrierung.

## Ausfuehrungsprotokoll

- Plattform: MISTRAL/VIBE run_typescript Sandbox. Wandzeit nicht messbar (Uhrdifferenzen gleich null). Ressourcen: Netzwerk 0 B (nur GitHub-Connector-Lesezugriffe auf Issue 443 und PR 444 Dateien), Retries 0, Cache NONE, Tokenbilanz OBSERVABLE_NONE.
- Aufteilung: vier Programme (je Arm) wegen des 60-Sekunden-Budgets; identische Zufallszahlen; Vergleiche innerhalb jedes Designs sind gepaart.

## Referenzkern v4 (armparametrisiert)

    // Whitening-Operatoren und Faktorialkern (TypeScript, Sandboxed)
    const fm = (t, a, b, c) => a * Math.sin(b * t) + c * t;
    // W = inverse(AR(1) Kovarianz); L = chol(W); OLD: rw = L r; COR: rw = L^T r
    // fit: Newton mit exaktem Restkraemmungsterm
    // H = 2 [ Jw^T Jw minus Summe ueber i von rw_i mal (Lm-angehaengte zweite Ableitungen) ]
    // nichtverschwindende Slices: ab = t cos(b t), bb = minus a t^2 sin(b t)
    for (let it = 0; it < 300; it++) {
      // Jacobian J, Whitening Jw = Lm J, Gradient g = 2 Jw^T rw, GN-Hesse A = Jw^T Jw
      // Kraemmung: sAB = Summe rw_i (Lm * t cos(bt))_i ; sBB = Summe rw_i (Lm * minus a t^2 sin(bt))_i
      // A[1] -= sAB; A[3] -= sAB; A[4] -= sBB; dann LM-Daempfung: Ad_ii = A_ii + lam mal max(|A_ii|, 1)
      // Schritt loesen, Projektion auf Grenzen, Zielvergleich oNew < o (sonst Parameter zuruecksetzen)
      // Abbruch nach Praeregistrierung
    }

Der vollstaendige Quelltext entspricht dem Programmcode der vier Armprogramme mit identischem Kern. Der Kern ist durch die Praeregistrierungs- und Evidenz-Hashes gebunden; keine weitere Klartextkopie hier, um Kollisionsrisiken zu vermeiden; die Gesamtlogik ist oben vollstaendig spezifiziert.