# R31 – Quellensicheres Wissenschafts- und Frameworkregister
OBJECT = NEXUS_OMEGA_AXIOM_R31_OPEN_INNOVATION_SOURCE_REGISTER_20261117_R0
STATUS = OPEN_RESEARCH_INPUT_NOT_AUTHORITATIVE_TRUTH
DATE = 2026-11-17
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RESEARCH_ONLY = YES

## Zuerst Kausalbindung, dann Fachexpertise

1. Cursor Knowledge Bind R31 (Operator-uploaded): ZIP 6161 B SHA256 64645331902fe6637ed9ae19f744c164f07f28011f7678110c4b6192603ae9f2, Sidecar 174 B SHA256 3ec59f083ab783b0cb21582fd50cf8cfb28dac5db15e09bcdce08e468102e675, 7/7 manifest, ZIP-CRC PASS.
2. Elternbind: 12153 B SHA256 1d425484c41588c2e01bffdb9faa42fad5503e4c4f2943ce2d9616fe45787685. Nur Knowledge-Bind, keine Implementierung.
3. NEXUS R31 öffentliches Primärrecherche-Objekt: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/364#issuecomment-6941793803, 15925 UTF-8 B SHA256 f0c70070b51975f33dfd8905ca34f26317f5b216a25e3a616a479c974234826a.
4. Kausaler privater Statusanker: https://github.com/nexusomegac27/NEXUS-OMEGA-PRIVATE-SCIENCE-CUSTODY/pull/34#issuecomment-6941808009, 1514 B SHA256 832957b2455580b3163a6d6e7789d64eeb553e22c3908c301a06155604c7f4b2. PRIVATE REPO: externe Gutachter haben KEINEN automatisch gewährten Zugang; der Link ist ein Provenienzreferent, kein Aufforderungszugriff.
5. R31 bisheriger unabhängiger A′-Quell-/Teststatus: Historischer Mehrzielkonflikt offline repariert und 18/18 enge Kontrollen unabhängig reproduziert, CF01–CF09 neue materielle explorative Misserfolge, CF10 sicher. Die exakt zugehörigen Original-Python-Dateien sind PRIVAT und werden über diesen Forschungsauftrag nicht verteilt.
6. WWW-Quellkontext: https://www.nexus-mobile.de/bodytwin/science/ ist eine öffentliche C1-Wissenschaftsdarstellung, keine klinische BodyTwin-Validierung, kein produktiver Auto-Publishing-Dienst.

Diese sechs Punkte sind angegebene historische Provenienz, nicht die Behauptung, dass jede zukünftige Expertin die privaten Originale selbst gelesen oder den Code selbst ausgeführt hätte.

## Primärdokumentation und alternative Rahmenwerke – sichtbare Forschungsoptionen

| ID | Primärquelle | Tatsächliche Rolle / prüfbare Reichweite | Offene Grenze |
|---|---|---|---|
| S01 | https://www.sqlite.org/lang_conflict.html | ABORT- und Constraint-Verhalten in SQL-Anweisungen | Kein Beweis für anwendungsseitiges ROLLBACK |
| S02 | https://www.sqlite.org/pragma.html | integrity_check und **separate** foreign_key_check, pro Connection FK | Keine komplette Application-Safety-Garantie |
| S03 | https://www.sqlite.org/testing.html | SQLite eigene Crash-/Fault-/Mutation-/Coverage-Methoden | Upstream-Testabdeckung beweist nicht NEXUS-Code |
| S04 | https://hypothesis.readthedocs.io/en/latest/stateful.html | Stateful RuleBasedStateMachine, Sequenzgenerator und minimierte Fehlertraces | Nicht unabhängiges Oracle durch bloßen Einsatz |
| S05 | https://docs.tlapl.us/using%3Atlc%3Astart | TLC finite-state model checking und Gegenbeispiele | Modell ≠ Python-Implementierung; endliche Grenzen |
| S06 | https://github.com/tlaplus/tlaplus/blob/master/USE.md | TLC-Trace-Export/Import JSON; spätere model-based Tests | Keine Ausführung oder Beweis ohne reale Tool-Logs |
| S07 | https://alloytools.org/ | Alloy 6 temporal logic, relational bounded Analyzer | Alternative zu TLC, nicht automatisch gleichwertig |
| S08 | https://quint.sh/docs/what-does-quint-do | Quint Specification, Simulator, Checker, counterexamples | Alternative Spezifikationssprache, Versionspin nötig |
| S09 | https://crosshair.readthedocs.io/en/latest/introduction.html | Symbolische Ausführung vertraglich spezifizierter Python-Funktionen | Nicht unkritisch mit SQLite/IO; Isolation und Scope |
| S10 | https://mutmut.readthedocs.io/en/latest/ | Mutation test survival / weak oracle discovery | Keine Totalverifikation; Laufzeit-/OS-Constraints |
| S11 | https://github.com/jepsen-io/elle | Historienbasierte Transaktions-/Konsistenzanomalien | Beobachtete Vorgänge, keine App-Autorisierung; mögliche False Negatives |
| S12 | https://github.com/shopify/toxiproxy | Synthetische Netzwerkfaults für autorisierte Isolation | Keine Hostinger-Tests ohne Freigabe |
| S13 | https://in-toto.io/docs/getting-started/ | signierte layout/step link metadata und Prozessautorität | Korrekte Signatur ist nicht wissenschaftliche Wahrheit |
| S14 | https://slsa.dev/spec/v1.2/build-provenance | Build Inputs, Builder/Outputs, verifizierbare Herstellung | Build-Herkunft ≠ Operator-Release-Autorisierung |
| S15 | https://theupdateframework.github.io/specification/latest/ | Rollen, Signaturen, Anti-Rollback und Anti-Freeze | Volle TUF-Installation ggf. unverhältnismäßig |
| S16 | https://www.rfc-editor.org/rfc/rfc8785 | JSON Canonicalization Scheme | Kanonische Bytes ≠ authentisierte Origin-Signatur |
| S17 | https://www.rfc-editor.org/rfc/rfc9110 | HTTP Status/Caching/Content-Encoding-Semantik | HTTP 200/304 ≠ wissenschaftlich geprüfter Inhalt |
| S18 | https://playwright.dev/docs/test-assertions | Browser Assertions/DOM Prüfung | Browser Test allein ≠ unabhängiger WWW-Witness |
| S19 | https://w3id.org/ro/crate/1.3 | RO-Crate 1.3 Forschungsdaten, Metadaten und Provenienzobjekte | Beleggraph ≠ automatische empirische Validität |
| S20 | https://www.w3.org/TR/prov-o/ | W3C PROV Entity/Activity/Agent | Ontologie ≠ echte Senderidentität |
| S21 | https://opentelemetry.io/docs/specs/semconv/general/trace/ | Gemeinsame Ereignis-/Trace-Attribute | Telemetrie kann falsch oder selbst attestiert sein |
| S22 | https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries | Webhook-HMAC über empfangene rohe Payload | Authentischer Trigger ≠ wissenschaftliche Freigabe |
| S23 | https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf | NIST SSDF Struktur – mit Versionscheck | Rahmenstandard, kein Codebeweis |
| S24 | https://www.bipm.org/en/committees/jc/jcgm/publications | JCGM/GUM Metrologiereferenz | Sensor-/Forschungsaussage benötigt eigene Messdaten |
| S25 | https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods | AWS TLA+ Erfahrungsforschung | Fallbericht, nicht Beweis für NEXUS |
| S26 | https://apple.github.io/foundationdb/testing.html | Deterministische Simulation als methodisches Vorbild | FoundationDB Simulator kein drop-in für SQLite |

Die Tabelle ist ein *Angebotskorpus* und darf kreativ verworfen, durch bessere Quellen ergänzt und wissenschaftlich kritisiert werden. Wer eine neue Methode vorschlägt, ergänzt die Primärquelle, den Testbereich, die Gegenhypothese, die Lizenz und die praktische Testbarkeit. Der einzelne Prüfer ist NICHT verpflichtet, alle 26 zu lesen. Nur tatsächlich gelesene und konkret ausgewertete Belege dürfen in der Zahl PRIMARY_SOURCES_READ erscheinen.

Bei versionsdynamischen Dokumentationen muss im Return die eingesehene genaue Version/Commit/Access Date angegeben werden. Einige URL-Dokumentationen ändern ihre aktuelle Fassung; die Tabelle selbst behauptet keine dauerhafte Quellenimmutable.

## Quellenanspruch und Bewertungsvorschrift

- SOURCE_EXACT bedeutet tatsächlich geprüfte Rohbytes am Original-Ref und nicht eine Dateinamen-/Hashnennung.
- Ein SHA256-Sidecar prüft unveränderte Bytes nur bei authentisiertem Vergleichswert; es garantiert keine Senderautorität.
- Modelle, Nullhypothesen und Negativkontrollen vor eigener synthetischer Ausführung einfrieren. Nachträglich ergänzte Fälle als POST_HOC.
- Keine Nutzung privater Daten als Voraussetzung. Kein mit unbekanntem Lizenzstatus beigefügter fremder Sourcecode.
- Unterschied: Research-Summary, first-party Documentation, akademisches Paper, Anbieter-Marketing, Community-Forum, unabhängiger Laufzeitbeleg.
- Ein defekter ursprünglicher Prüfer-/Frameworkstandard darf mit reproduzierbarem Gegenbeleg explizit abgelehnt werden.

TERMINAL = PUBLIC_SAFE_C1_SOURCE_REGISTER_NOT_RESEARCH_EXECUTION
