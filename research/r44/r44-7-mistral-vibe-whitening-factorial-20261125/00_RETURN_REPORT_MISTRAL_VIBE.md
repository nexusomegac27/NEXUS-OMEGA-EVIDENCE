# R44-7 Rueckgabebericht MISTRAL/VIBE: Whitening-Reparatur und 2x2-Faktorial (RC03)

Artikel: research/r44/r44-7-mistral-vibe-whitening-factorial-20261125/
Referenz: NEXUS_OMEGA_AXIOM_R44_7_EXPERT_MAXI_ORDER_20261125_R0 (Issue 443), Direktive AXIOM_RETURN_SELF_OPTIMIZATION_V1
Datum: 2026-11-25. CLAIM_CEILING = C1_DESCRIPTIVE_ONLY. Ausfuehrungsstatus: LOCAL_SYNTHETIC_EXECUTED_C1. R44_7_FORMAL_EXECUTED bleibt 0. Kein kanonisches Gate-Credit.

## 1. Auftrag und Scope

Issue 443 als kanonischer Einstiegspunkt, alles ausschliesslich ueber GitHub bezogen. Scope- und Lease-Freigabe durch den Operator erteilt vor Ausfuehrung (2026-11-25). Lease- und ressourcenbezogene Werte sind in Abschnitt 6 dokumentiert. Die Defektdaten zu E32/E33 wurden aus dem AXIOM-Stack uebernommen; das Originalmodell model5.py wurde nicht empfangen und nicht ausgefuehrt, daher kein Baseline-Replay des Originalmodells und keine Originaldaten-Nutzung.

## 2. Priorisierte Forschungsfrage

Falsifizierung der AXIOM-Korrektur des Whitening-Defekts im nichtlinearen Referenzmodell und Trennung ihres Einflusses von Sensorgeometrie (Design), Kovarianzschaetzung (bekannte Kovarianz, damit ausgeschlossen) und Modellstruktur (fest gehalten). Der Defekt: gls_nonlinear verwendet L r statt L^T r und impliziert damit die Gewichtungsmatrix L^T L statt W = L L^T.

## 3. RC01 Replikation und Verschaerfung

Eigene Replikation mit eigener Cholesky-Zerlegung und eigener 3x3-Inverse:

- rho 0.8: OLD 30.694444444444446, KORRIGIERT 28.91666666666668, Ziel r^T W r 28.916666666666675. AXIOM: 30.69444444444444 / 28.91666666666668 / 28.916666666666686. MATCH in allen drei Groessen.
- rho 0.3: OLD 7.815934065934066, KORRIGIERT 7.717032967032965, Ziel 7.717032967032965. AXIOM: 7.815934065934064 / 7.717032967032965 / 7.717032967032966. MATCH in allen drei Groessen.

Verschaerfender Zusatzbefund (eigenstaendig): ueber 200 deterministische Zufallsvektoren r (LCG seed 20261125, Bereich [-2,2]) weicht OLD in 200 von 200 Faellen vom Ziel ab, maximale relative Abweichung 1.2917; KORRIGIERT trifft das Ziel in 200 von 200 Faellen (Toleranz 1e-9). Der Gradientenwinkel zwischen dem falschen Gradienten 2 L^T L r und dem korrekten 2 W r betraegt 7.27 Grad (Kosinus 0.99195). Ursache exakt identifiziert: r^T L^T L r impliziert L^T L als Gewichtung, nicht W.

## 4. RC03 2x2-Faktorial (Praeregistrierung a7f9e1df476684f4aee5ea566863a55db6a0cbbb57332d272280c732cefcc968)

Design: 4 Arme, je Arm N=2000; Modell f(t; a, b, c) = a sin(b t) + c t; Wahrheit (1.2, 2.4, 0.3); AR(1)-Kovarianz rho 0.8, sigma 0.1, bekannt; Arme: A OLD narrow (n=10, t in [0,2]), B KORR narrow, C OLD wide (n=20, t in [0,4]), D KORR wide; gemeinsame Zufallszahlen je Design (gepaart); Newton mit exaktem Restkraemmungsterm, LM-Daempfung, Abbruch nach Praeregistrierung.

Ergebnisse (unconditional Coverage, Misserfolg zaehlt als Nicht-Treffer):

| Arm | Coverage | Bias a | Bias b | Bias c |
| --- | --- | --- | --- | --- |
| A_OLD_NARROW | 0.8210 | -0.03403 | -0.03334 | +0.04034 |
| B_COR_NARROW | 0.8880 | -0.00983 | -0.00965 | +0.01166 |
| C_OLD_WIDE | 0.8550 | -0.00097 | -0.00313 | +0.00131 |
| D_COR_WIDE | 0.8695 | -0.00026 | -0.00532 | -0.00138 |

Beschreibende Lesart (C1): Der Reparatureffekt ist stark designabhaengig (Differenz von Differenzen: narrow +6.70 Prozentpunkte, wide +1.45 Prozentpunkte). Weder Gewichtung noch Design allein erklaert das Ergebnis; die Interaktion ist der tragende Befund. Die Bias-Reduktion unter korrekter Gewichtung ist im narrow-Design gross (Faktor rund 3.5), im wide-Design vernachlaessigbar. Kein Arm erreicht die nominale 0.95; bei bekannter exakter Kovarianz ist der Restshortfall konstruktionsbedingt auf die Wald-Approximation zurueckzufuehren, beschreibend ohne Kausalaussage. Abstain nicht ausgeloest (kappa zwischen 3.023 und 10.807, Schwelle 1e10).

## 5. Failure-Flags und Konvergenz

8000 von 8000 Fits CONV, 0 NF, 0 MAXITER, 0 WaldFailed, 0 Randtreffer. Die Konvergenzklasse OBJ_STEP_STALL war in der Praeregistrierung dokumentiert und wurde als Ausstieg genutzt; der Gradientenschwellwert 1e-7 ist unter L-gewichteter Skala numerisch unerreichbar.

## 6. Lease, Ressourcen, Provenienz

- Skriptversionen: v1 verworfen (Faktor-2-Schrittfehler), v2 verworfen (Michaelis-Menten entartet auf reinem t-Gitter), v3 verworfen (GN ohne Kraemmungsterm, MAXITER 2000/2000 im Pilot), v4 aktuell (exakter Newton-Kraemmungsterm). Alle Versionen sind in 03_EXECUTED_SCRIPT_V4.md dokumentiert, nicht geloescht, ein Fehlerarchiv entsprechend E34.
- Runtime: run_typescript Sandbox; Wandzeit nicht messbar (UNKNOWN_COST_WALL); Netzwerkgress 0 B (nur GitHub-Connector-Lesezugriffe); Retries 0; Cache NONE; Tokenbilanz OBSERVABLE_NONE.
- Quellenidentitaet: Issue 443 (1 Kommentar), Draft PR 444 (10 Dateien, Head 4b37f7df377c2dfb39eab05830d3155ae6bf11c1), byte-exakter Readback 6/6 Manifestzeilen MATCH, Manifest-Selbsthash 5f94facff9b89b2774f8a6a7e245e72779c49f2f2e3f5fe0a0ba28ff578e9d81, ZIP-Sidecar 6b5661e84e999eebff4903144641b551507053848b5cb089352cd44355108778 wortidentisch.
- Keine Ausloesung: EXPERT_LIVE_DISPATCH nicht durch diesen Akteur; kein Cursor; kein Merge; ALT_D nicht ausgefuehrt; E23 unberuehrt; W1 offen; B01-B05 offen.

## 7. Bindung und Fehler

Diese Rueckgabe bindet ausschliesslich beschreibende C1-Aussagen. Sie beantragt kein kanonisches Gate-Credit, keine Quorum-Erneuerung, keinen Vollwissenschaftszadl. Innerhalb der Rueckgabe: 24 (R44-3 kanonisch), 28 (R44-5 GI/GLM), 18 (R44-6 SA), 14 (R44-7 RC01-RC14) werden getrennt gezaehlt; die 14 R44-7-Kontrollen bleiben mit Ausnahme der hier beschriebenen RC01/RC03-Ausfuehrung NOT_RUN und erhalten kein Gate-Credit.

Empfehlung: EXPERT_RETURNS_TO_AXIOM_INDEPENDENT_ADJUDICATION_THEN_OPERATOR_DECISION. Vor einer F07/F04-Replay-Entscheidung muessten das Originalmodell model5.py (SHA 9c34bfec2709de8a5c7f45d03c4cf880e2dac8afb6fc7a75f1b64004aa3217c2) lub Dependencies laut Auftrag zuerst empfangen und byte-genau gelesen werden.