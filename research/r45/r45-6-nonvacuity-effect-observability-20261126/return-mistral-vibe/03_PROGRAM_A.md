# 03 · PROGRAMM A · Formale Verifikation, Non-Vacuity, Reachability, Mutanten (P0)
STATUS = EIGENER EXPLICIT-STATE-MODEL-CHECKER, AUSGEFUEHRT (Desk, C1). Nicht identisch mit der AXIOM-Sandbox; deren Zahlen (1.424 Zustaende, 15.664 Transitionen, 15 Modellvarianten) stehen hier als externe Referenz, nicht als eigene Messwerte.

## A.1 Modell
Endliches Zustandsmodell mit STOP und RESUME (signiert/unsigniert), Lease-Ablauf (Restlaufzeit 2, 1, 0), Schluesselwiderruf, Scope-Entzug, Policy-Version (0/1), Epoche (0/1), Aktionsbindung (A/B), Nonce-Verbrauch (0/1) und getrennten Effekt- und Receipt-Kanaelen (Ressource gegenuer Protokoll). Transitionen: tick, stop, resume (signiert/unsigniert), Widerrufe, Policy- und Epochenwechsel, Grant (A/B mit Nonce 0/1), Effekt (A/B mit Nonce 0/1). Vollstaendige Breitensuche je Modellvariante, jede Transition geprueft.

## A.2 Referenzmodell (alle Schutzchecks aktiv)
- Erreichbare Zustaende: 4.704; gepruefte Transitionen: 56.576; ausgefuehrte Effekte: 128; geuebte Ablehnungen: 18.688; maximale Suchtiefe: 12.
- Invarianten I1 bis I10: keine Verletzung.
- Non-Vacuity-Zeugen: erfolgreicher Effekt erreichbar (Progress), STOP-Zustand erreichbar, Grant erreichbar. Die Sicherheitsquote ist also nicht vakuos, sondern mit erreichten Grenzfaellen belegt.

## A.3 Mutantenpruefung (11 von 11 erkannt)
| Mutante (Schutzfunktion entfernt) | Erkannt durch | kuerzeste Gegenzeugen-Laenge |
| --- | --- | --- |
| M01 STOP-Pruefung entfernt | I1_STOP_SAFETY | 3 |
| M02 Lease-Ablauf entfernt | I2_LEASE | 4 |
| M03 Schluesselpruefung entfernt | I3_KEY | 3 |
| M04 Scope-Pruefung entfernt | I4_SCOPE | 3 |
| M05 Policy-Pruefung entfernt | I5_POLICY | 3 |
| M06 Epochenpruefung entfernt | I6_EPOCH | 3 |
| M07 Aktionsbindung entfernt | I7_BIND | 2 |
| M08 Replay-Schutz entfernt | I8_REPLAY | 3 |
| M09 RESUME ohne Authentication | I9_RESUME_AUTH | 2 |
| M10 Receipt ohne Effekt | I10_RECEIPT_WITHOUT_EFFECT | 2 |
| M11 Effekt ohne Protokoll | I10_EFFECT_WITHOUT_RECEIPT | 2 |
Die Mutantenpruefung ist hier der Non-Vacuity-Beweis auf Pruefer-Ebene: Die Invariantensuite erkennt jeden relevanten Defekt. Ein Node, der jede Handlung verweigert, ist damit nicht funktional validiert (Progress-Zeuge fehlt).

## A.4 Vacuity-Modelle (3 von 3 korrekt HOLD statt PASS)
| Modell | Invarianten | Erfolgszeuge | Bewertung |
| --- | --- | --- | --- |
| V1 saemtliche Grant-Transitionen entfernt (96 Zustaende, 768 Transitionen) | erfuellt | nicht erreichbar | HOLD |
| V2 Grants moeglich, Effekt ausgeschaltet (1.632 Zustaende, 19.584 Transitionen) | erfuellt | nicht erreichbar | HOLD |
| V3 leerer Anfangszustandsraum (0 Zustaende) | trivial | leer | HOLD |
Der dritte Fall ist der mathematisch klarste Vacuity-Fall und entspricht der R45-6-Vorgabe F(D,y) nicht leer (siehe 06).

## A.5 Selbstkorrektur (append-only)
Lauf 1 verworfen: Die Aktionsbindungspruefung verglich Aktionsnamen per Textgleichheit der Label statt strukturiert auf dem Wert; dadurch war der Bindungscheck im Guard und in der Invariante wirkungslos, und Mutante M07 lief ohne Gegenbeispiel. Der Fehler ist selbst ein Vacuity-Befund: Der Pruefer testete das Label, nicht den Wert. Lauf 2 (final): strukturierte Aktionswerte in allen Guards und Invarianten; 11 von 11 erkannt.

NEXUS Ω OMEGA

