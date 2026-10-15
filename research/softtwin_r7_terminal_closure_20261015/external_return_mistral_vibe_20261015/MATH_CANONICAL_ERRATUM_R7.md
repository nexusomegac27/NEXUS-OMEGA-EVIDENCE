# MATH_CANONICAL_ERRATUM_R7 — Kanonisches Mathematik-Erratum (R5/R6)

**OBJECT:** NEXUS_OMEGA_R7_MATH_ERRATUM_20261015_R0 · **CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY · **Status:** ERRATUM_READY_BUT_CANONICAL_BIND_PENDING

## Fehlerhafte historische Aussage (bleibt zur Spurenhaftung erhalten, Wiederverwendung als Theorem verboten)

Die Schranke 2*||d||^2/(1-lambda)^2 (vergessene Betragsstriche um lambda) ergibt fuer lambda=-1/2, N=1000 den Wert **888.888889**. Sie ist als allgemeine Energie-Schranke **falsifiziert**: die tatsaechliche Energie der Skalar-Rekursion e_{t+1} = lambda*e_t + d_t mit e_0=0, d_t=(-1)^t betraegt **3993.333333 = 4(N-2+1/3)** und verletzt die Schranke reproduzierbar (E > 888.888889).

## Korrekte Aussagen (numerisch und analytisch verifiziert in dieser Session)

1. **Konservative Schranke:** 2*|e_0|^2/(1-lambda^2) + 2*||d||^2/(1-|lambda|)^2. Fuer e_0=0, ||d||^2=N=1000, lambda=-1/2: **8000** — haelt (E = 3993.333333 <= 8000).
2. **Scharfer induzierter l2-Gain:** 1/(1-|lambda|) = **2** fuer die stabile Faltung mit Null-Anfangsbedingung (sup_{|z|<1} |1/(1-lambda*z)| = 2, numerisch 2.000000). Trennung von der transienten Anfangsantwort bleibt explizit.
3. **Hilbert-Schmidt vs Operatornorm:** Die HS-Kernnorm^2 betraegt 4/3 = 1.333333 und ist NICHT die Operatornorm^2 = 4.000000 — Kernnorm und Operatornorm duerfen nicht vertauscht werden.
4. **l2 strikt in c0:** Zeuge 1/(t+1) liegt in l2 (Partialsumme bis 1e6: 1.644933067, gegen pi^2/6 = 1.644934067); Zeuge 1/sqrt(t+1) liegt in c0 aber nicht in l2 (Partialsumme 1998.540, divergent ~ 2*sqrt(N)).
5. **Abklingen:** d_t -> 0 impliziert e_t -> 0 (Zeuge: max |e_t| fuer t >= 1000 betraegt 0.002000). OHNE d in l2 ist e NICHT in l2 — diese Richtung wird nicht behauptet.
6. **Nichtnormal-Matrix-Gegenbeispiel:** A = [[0.5, 1000], [0, 0.5]] hat Spektralradius rho = 0.5, aber transiente Normen ||A^t|| = 1000.000250 (t=1), 1000.000062 (t=2), 750.000021 (t=3), 500.000008 (t=4) — Peak bei t=1. Matrix-Erweiterungen erfordern explizite Zusatzannahmen; kein Globaltheorem per Analogie.

## Bindungsstatus

Das Erratum ist vollstaendig bewiesen und numerisch verifiziert, aber die **kanonische Bindung** an das Foundation-Dokument (autorisierter append-only Overlay mit autoritativer Quellenreferenz) ist in dieser Session nicht verfuegbar. G5 = HOLD_WITH_PRECISE_REASON: ERRATUM_READY_BUT_CANONICAL_BIND_PENDING. Kein Aufstieg zu C2 (keine autorisierte NEXUS-Claim-Klasse).
