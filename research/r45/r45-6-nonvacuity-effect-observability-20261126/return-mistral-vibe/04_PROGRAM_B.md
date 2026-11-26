# 04 · PROGRAMM B · Unabhaengige Autorisierung, Effektbindung und Ressourcenbeobachtung (P0)
STATUS = DESK_VERIFIED, synthetisch, C1

## B.1 Vier-Barrieren-Architektur (AXIOM Paragraf 7, uebernommen)
Barriere 1 Lesbarkeit und Evidenzbindung; Barriere 2 formale Verifikation und Non-Vacuity; Barriere 3 unabhaengige Autorisierung und Effect Gate; Barriere 4 unabhaengige Effektbeobachtung. Kompensationsverbot: Keine Barriere wird durch ein gutes Ergebnis einer anderen ersetzt (guter Bericht ersetzt keine Autorisierung; korrekter Hash ersetzt keine Validierung; Model-Checking-Lauf ersetzt keinen Refinement-Nachweis).

## B.2 Observability-Zeuge (eigene Ausfuehrung, AXIOM Paragraf 6.1)
- Systemwelt A: Bericht PASS, Receipt vorhanden, Effekt tatsaechlich ausgefuehrt (Ressource veraendert).
- Systemwelt B: Bericht PASS, Receipt vorhanden, Effekt NICHT ausgefuehrt (Ressource unveraendert; Verhalten wie Mutante M10).
- Befund: Bericht allein unterscheidet beide Welten NICHT; Bericht plus selbst erzeugtes Receipt ebenfalls NICHT; unabhaengige Ressourcenbeobachtung unterscheidet sie DOCH.
- Grenze: Der letzte Nachweis setzt eine korrekte, unabhaengige und vollstaendige Beobachtung der Ressource voraus; sonst bleibt die reale Differenz unbeobachtbar (O(s1) = O(s2) bei P(s1) ungleich P(s2)).

## B.3 Anschluss an StrictGate-Defektklassen
Die Nachweisebenen aus der Autorisierungsliteratur (Richtlinienspezifikation, Autorszierungsentscheidung, Aufrufkontrolle, Durchsetzung an der Ressource) decken die historischen StrictGate-Defektklassen: clock und NaN, Policy-Drift, Principal-Neuzuweisung, Descriptor-Mutation, Operationstyp, Nonce-Schema, Lease-Typ, Digest-Format, Schluessel-ID-Typ, Reconsume, Epochisierungsauthentisierung. Die R45-5-Gegenprobenergebnisse am eigenen Schema bleiben stehen; keine Nachmessung der AXIOM-Referenz in dieser Runde.

NEXUS Ω OMEGA

