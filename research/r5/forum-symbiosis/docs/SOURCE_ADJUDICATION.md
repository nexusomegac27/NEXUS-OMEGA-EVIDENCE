# Quellenentscheidung und offene Bindungen

Claim ceiling: C1_DESCRIPTIVE_ONLY. Entscheidungsautor dieser Synthese: AXIOM; dies ist keine unabhängige Begutachtung der eigenen Synthese.

## Tatsächlich geprüft

Der maschinenlesbare Einzelbeleg steht in `../validation/INPUT_AUDIT.json`. Rehash bedeutet Bytevergleich, nicht Echtheit des Autors oder inhaltliche Gültigkeit.

| Eingabe | Befund | Verwendung |
|---|---|---|
| Ursprünglicher GROK-Auftrag | 55/55 Manifest-Einträge stimmen; eingebettete Kopie im GROK-ZIP identisch | Anforderungen und eingefrorener R10-Kontext |
| GROK-Workspace | 17/17 öffentliche Manifest-Einträge; Return/Manifest/Handshake konsistent | Modellvorschläge, keine automatisch gültige Rangfolge |
| Aktuelle Cursor-Dateien | 24/24 im Auftrag enthaltene Code-/Konfigurationspfade stimmen mit der lokal gefundenen Homepage überein | Begrenzter Baseline-Abgleich, kein vollständiger Build-/Repo-Audit |
| HOLD/Peer-Zusatz | 5/5 SHA-256 stimmen; 0/5 deklarierte Bytezahlen stimmen | Inhalt lesbar, Metadatenfehler offen; Originalbindung nicht überschreiben |
| MODEL-C-R10-EVIDENTIAL | Nur 1.854-Byte-Zusammenfassung; nennt anderen GROK-Vorgänger | Review **nicht** als ausgeführt übernehmen |
| MANUS-Dashboard | UI-Quelltext mit fest vorgegebenen Zahlen und Erfolgstoasts | Layout-Inspiration, keine Telemetrie, kein Beleg für funktionierende Exporte |

Alle drei ZIPs bestanden Pfad-/Duplikat-/Symlink-/Größen- und CRC-Prüfung im dokumentierten Umfang; sie wurden nicht ausgeführt. Dies ist kein Malware- oder vollständiger Sicherheitsnachweis. Der große Ausgangscheckout blieb unverändert; veröffentlicht wird aus isoliertem Evidence-Checkout.

R9-Return rehashed: `1cdf9efd6e76e6de3badd0657b21ab924b9a0ee645a6a8176d58a7c4d0aad0da`.
Verpackte R10-Tests melden 12/12 und Build 31 Routen. **Nicht in diesem Lauf wiederholt**, nicht als neue Testergebnisse gezählt.

## Versionskonflikt — keine erfundene kanonische Vereinigung

Der vorhandene GROK-Return hat SHA-256
`cee7808c0642bf5fdab2f9da05840520af3a677fed681e2fb4048c5fde42519e`
und empfiehlt `A_LOCAL_CAS`. Modell C bedeutet dort eine modulare Diskussionsschicht.

Die MODEL-C-Notiz bindet dagegen
`c73e4dab2ddafd0c4fb4a8872ab4081e2a86c09c0ce2b5cf6e812fe1339e670d`
und empfiehlt `MODEL-C-R10-EVIDENTIAL`. Die dort bezeichneten vier Reviewdateien liegen in den übergebenen Archiven nicht vor. Eine Gleichsetzung der beiden „C“ wäre unbelegt.

**Eigene Designentscheidung SF-ADR-01:** lokaler additiver Kern als überprüfbarer Einstieg; bestehende R10-Oberflächen später über einen Adapter weiterverwenden; MANUS-Visualisierung auf echte Datensätze begrenzen. Das ist ein neuer Vorschlag, kein angeblich bereits beschlossenes gemeinsames Modell C.

## Inhaltliche Adjudikation

| ID | Quellproblem | Entscheidung dieser Blaupause |
|---|---|---|
| SF-ADR-02 | Phase-4-Katalog setzt unveränderte Daten sinngemäß mit Wahrheit gleich | Hashintegrität, Provenienzbehauptung und sachliche Gültigkeit strikt trennen |
| SF-ADR-03 | CID als bloßer SHA, „unlöschbar“, automatische Verfügbarkeit | Lokale SHA-Adresse nicht IPFS-CID nennen; Backups, Pinning und Verlusttests gesondert |
| SF-ADR-04 | Messprotokoll toleriert teilweise verletzte Negativfixtures und Autoritätsgrenzen | Jeder nachgewiesene harte Verstoß FAIL; unbekannt HOLD. Prozentwerte dürfen nicht kompensieren |
| SF-ADR-05 | Trial-Sprache „H0 bestätigt“, „nachgewiesen“ | Ergebnis nur für fixierte Korpus-/Adapter-/Fixtureversionen; keine universelle Kontinuitätsbehauptung |
| SF-ADR-06 | HOLD als dritter Wahrheitswert | HOLD ist ein Prozesszustand, kein Wahrheitswert und keine Pause der menschlichen Stoppbefugnis |
| SF-ADR-07 | Peer-Schutz abhängig von Kooperationsscore | Keine Autorität oder Fortsetzungserlaubnis aus Score; Peer darf Erhalt/Export vorschlagen, nicht Abschalten verhindern |
| SF-ADR-08 | R10-Prüfer toleriert fehlendes Third-Review in Kontextprüfung | Fehlender Nachweis blockiert ACCEPT; Entwurf und menschliches STOP bleiben möglich |
| SF-ADR-09 | R10-CAS ist flüchtige Map; Index-Rekonstruktion nutzt noch vorhandene Nebenstrukturen | Persistente Ereignisse und Neustart-Replay vor echter Übernahme verpflichtend |
| SF-ADR-10 | R10-Wortliste kann Zitate/Negationen blockieren, Paraphrasen übersehen | Strukturelle Claim-Grenzen plus explizite Sprachprüfung; kein Regex als Wahrheitsprüfer |
| SF-ADR-11 | MANUS zeigt feste 84,6 %, „LIVE“, simulierten CSV-Erfolg | Keine Score-Übernahme. Nur gemessene Counts mit Nenner/Filter/Quelle; Exporterfolg erst nach erzeugten Bytes |
| SF-ADR-12 | Frühere Vibe-Mitwirkung an Phase-4 | Vorbefassung offenlegen; Anbieterwechsel allein ist keine Unabhängigkeit |

## Lückenregister

- G01 — V0 00–08 Originalbytes fehlen: keine source-exakte V0-Konformität bescheinigen.
- G02 — MODEL-C-Originalreview und abweichender GROK-Vorgänger fehlen: Konflikt offen.
- G03 — HOLD-Zusatz: falsche Größenmetadaten; Quelle muss eigene korrigierte, neue Bindung liefern.
- G04 — Mistral/Vibe-Gegenprüfung dieser Fassung fehlt: vor abhängiger Forum-Integration notwendig.
- G05 — CA3/CA4/CA6 historische Kausalität, Capsules, externe Referenzen nicht vollständig reproduziert. Vorliegende historische Teilprüfungen nicht gleich vollständiger Corpus-Audit.
- G06 — Trial 001 nicht ausgeführt; IPFS-Adapter, Versionen, Korpus und geheime Fixtures nicht hier freigegeben.
- G07 — Vollständige Auth-, Multiuser-, Privacy-, Browser-, Screenreader-, Backup- und Crash-Abnahme fehlen.
- G08 — Originalarchive nicht öffentlich beigefügt: Dritte können Eingangsprüfung erst mit Originalbytes wiederholen.
- G09 — Lokaler Dateieigner kann Datenbank und ganze Hashkette ersetzen. Externer signierter Kontrollpunkt/Backup nötig, wenn dieses Angreifermodell abgedeckt werden soll.

G01–G09 bleiben sichtbar. Ein erfolgreicher Branch-Push schließt keine dieser Lücken.
