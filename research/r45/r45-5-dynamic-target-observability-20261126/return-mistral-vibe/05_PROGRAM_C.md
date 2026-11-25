# 05 · PROGRAMM C · StrictGateV4, 13 Gegenproben (E27 bis E29, E34)
STATUS = EIGENES FAIL-CLOSED-REFERENZSCHEMA (Desk). Kein Substitutionscredit: das von AXIOM empfangene Python-Referenzmodell ist nicht auf GitHub; die Pruefung lief an einem eigenen, konzeptionell nachgebildeten Schema mit digest- und nonce-gebundenem Capability-Descriptor, Closure-gebundener Policy-Version sowie Principal-und-Key-Registry.

## C.1 Pruefaufbau-Verlaufsnotiz (Selbstkorrektur, append-only)
- Lauf 1 verworfen: Harness-Fehler, Objekt statt Positionsargumente an die Grant-Funktion, dadurch systematisches E_CAPABILITY_UNKNOWN; zusaetzlich kollabierten die Normalgleichungen numerisch, Wechsel zur Cramer-Resolvente.
- Lauf 2 verworfen: Object.freeze verhindert Feldmutation in dieser Umgebung nicht; der Descriptor-Digest driftete, der Positivfall wurde faelschlich mit E_DIGEST_NOT_BOUND_TO_OPERATION abgewiesen.
- Lauf 3 (final): Descriptor-Felder strikt in Closure, nie exponiert; Policy-Version als wirklich mutierbare Registry gehalten, sodass Drift tatsaechlich abgelehnt wird.

## C.2 Endergebnis finaler Lauf
| Gegenprobe (Klasse, AXIOM Paragraf 2.3) | Beobachtung am eigenen Schema |
| --- | --- |
| Rueckwaertsbewegung der Uhr | E_CLOCK_ROLLBACK_OR_NAN |
| Uhrwert NaN | E_CLOCK_ROLLBACK_OR_NAN |
| Extern geaenderte Policy-Version | E_POLICY_VERSION_DRIFT (Version zum Fail-Zeitpunkt v9.0) |
| Neuzuordnung eines Principals | E_KEY_SCHEMA_OR_UNREGISTERED_OR_UNBOUND |
| Veraenderter Capability-Descriptor | E_DESCRIPTOR_IMMUTABLE_BY_CONSTRUCTION (nie exponiert, nonce-gebundener Content-Hash) |
| Falscher Operationstyp | E_OPERATION_TYPE_MISMATCH |
| Leere Nonce-Zeichenkette | E_NONCE_SCHEMA_OR_EMPTY |
| Doppelte Nonce | EFFECT_EXECUTED (Erstnutzung) then E_NONCE_REPLAY |
| Boolean als Lease-Dauer | E_LEASE_SCHEMA_INVALID |
| Ungueltiges Digest-Format | E_DIGEST_FORMAT_INVALID |
| Verschachtelte Schluessel-ID (TypeError-Klasse) | E_KEY_SCHEMA_OR_UNREGISTERED_OR_UNBOUND (typgeprueft abgelehnt statt TypeError) |
| Ungueltige Request-ID bei Consume (TypeError-Klasse) | EFFECT_EXECUTED (Erstnutzung) then E_NONCE_REPLAY (typgeprueft abgelehnt statt TypeError) |
| Nicht authentifizierter Epochenwechsel | E_EPOCH_CHANGE_NOT_AUTHENTICATED |

Positivfall: EFFECT_EXECUTED. Replay danach: E_NONCE_REPLAY. Effekt-Ledger exakt 3 Eintraege (effect@n8, effect@n12, effect@n20), belegt die atomare Effektgrenze.

## C.3 Zuordnung
Die AXIOM-Tabelle desselben Paragrafen zeigt an der empfangenen Referenz 5x EFFECT_EXECUTED (Uhr, NaN, Policy, Principal, Descriptor), 5x GRANTED, 2x TypeError und 1x ACCEPTED. Das eigene Schema lehnt dieselben 13 Klassen ab. Der AXIOM-Befund, der als unveraenderlich bezeichnete Descriptor sei ein veraenderbares Python-Dictionary, wird hier durch Konstruktion neutralisiert, nicht durch eine Freeze-Funktion. Bewertung bleibt C1, keine Behauptung ueber das reale NEXUS-System.

NEXUS Ω OMEGA

