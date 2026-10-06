# Phase 2 — Korrekturen und verpflichtende Streitpunkte

Erst nach dem unveränderten, gehashten N00 lesen. Die folgenden Feststellungen sind Review-Eingaben, keine zu übernehmenden Urteile. Vorexposition im N00 offenlegen.

## D01 — Originaleingabe

GROK-BOT meldete den ursprünglichen Entwurf als NOT_FOUND und prüfte Abschnitt 31 referentenbasiert. Jetzt liegt `inputs/ORIGINAL_R10R9_DRAFT.txt` mit exakt 15456 Bytes und dem vereinbarten Hash vor. Das behebt die Eingabelücke dieses Reviews, nicht rückwirkend den damaligen Prüfablauf. Der historische BOT-Auftrag (29285 Bytes) liegt separat bei und ist nicht mit dem Originalentwurf identisch. Alle wortlautabhängigen Schlussfolgerungen neu prüfen.

## D02 — A2A: Wortlaut, Version und Status

Der offizielle Projektpost vom 12. März 2026 bezeichnet v1.0 als erste „stable, production-ready version“. Die BOT-Aussage, diese Formulierung sei offiziell nicht auffindbar, ist damit zu korrigieren. Die Release-Seite führt v1.0.1 als späteres Release (veröffentlicht am 28. Mai; der Changelog-Header nennt 26. Mai). Protokollversion, Git-Tag, Changelog-Datum, Publikationsdatum, Projekt-Selbstbeschreibung und formalen Standardstatus getrennt prüfen. Die Korrektur der Wortlautbehauptung beweist weder NEXUS-Governance noch unabhängige Produktionsvalidität. Auch die aktuelle Projekt-Governance muss am Review-Datum neu geprüft werden.

- [Offizielle v1.0-Ankündigung](https://a2a-protocol.org/dev/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/)
- [Offizielle Releases](https://github.com/a2aproject/A2A/releases)
- [Release v1.0.1](https://github.com/a2aproject/A2A/releases/tag/v1.0.1)

Diese zwei Hauptseiten wurden bei der Paketerstellung am 2026-10-06 erneut gelesen. Mistral verifiziert selbst und protokolliert seine Abrufe. Die übrigen BOT-Angaben zu RFC 9943, MCP, WCA/WAL und SLSA sind damit nicht pauschal bestätigt.

## D03 — C als Prompt-Teil

Der Originalentwurf spezifiziert die gemeinsame Verfassung als GATE4–GATE7 + Δ, jedoch keinen Transportkanal. Seine Literaturpassage §1.6 erwähnt zudem ein externes Verfassungsartefakt. Daraus folgt weder `C ⊂ P` noch, dass ARCH_A2 in NEXUS implementiert ist. G00/G07/G23 müssen mit dieser offenen Mechanismusfrage neu gelesen werden. Der Operator berichtet, GROK-BOT habe den Einwand später eingeräumt; diese Gesprächsaussage ersetzt keine revidierte, physisch gebundene G-Datei. Hier wird ausschließlich der ursprüngliche Return erhalten.

## D04–D10 — übrige Pflichtvergleiche

| ID | Streitpunkt | Konkret erforderliche Entscheidung |
|---|---|---|
| D04 | ursprünglicher R10R8-Defekt vs. AXIOM R1 | Originalcode, Originalresultat, R1-Code, R1-Resultat und Receipt versionengenau vergleichen; keine Produktionsfolgerung |
| D05 | AIR_GAP als Zustand/Relation | explizite Trennung, Decode-Key und Migrationsplan ohne historische Umschreibung |
| D06 | GATE5 fehlend/unbekannt/ungültig/out-of-scope | epistemische Zustände von Ausführungs-DENY trennen; Standalone/Integration/R1 vergleichen |
| D07 | PH-Herabstufung | direkte Primärbelege und faire komplette Baselines; weder Überlegenheit noch Unterlegenheit aus Suchnegativen |
| D08 | Part-C-Profilreduktion | existierende Standardfunktionen vs. Trust-Modell und konkreter NEXUS-Rest |
| D09 | Claim-Ceiling-Monotonie | definierte Ordnung und Vergleich mit Attenuation/ABAC/MAC/Labels |
| D10 | Self-contained order | Komponentenreduktion und ungetestete Kompositionshypothese getrennt |

## Return-Integrität und innere Konsistenz

Prüfe ZIP-SHA, CRC, alle 29 extrahierten Dateien und 28 G24-Bindungen. Vergleiche G00/G25 auf Urteil, Scope, Freigaben, nächste Schritte und Datums-/Versionsbindung. G01 hat nach lokalem Intake 193 Datensätze und 15 Spalten. Die behaupteten 12 Duplikatannotationen und 181 verschiedenen Quellenrecord-Einträge sind separat semantisch zu prüfen; 181 bedeutet nicht automatisch 181 unabhängige Quellen. Die drei Lane-Ledger bleiben unverändert vorhanden.

Die in G25 zusätzlich erwähnten `work/...`-Dateien gehören nicht zum ZIP. Sie werden nicht erfunden und sind nicht nötig, um BOT-Rechnungen unabhängig neu zu erstellen. Behauptungen, die ausschließlich auf nicht gelieferten Arbeitsdateien beruhen, bleiben ausdrücklich unbestätigt. Private R27-/R9-/E0-Referenzen sind nicht durch den nun gefundenen R10R9-Entwurf automatisch geschlossen.

N04-Spalten: `dispute_id,bot_file,bot_location,bot_claim,review_finding,evidence,relation,materiality,correction,affected_lane`. Relation ist CONCUR, PARTIAL, DISAGREE oder NOT_COMPUTABLE. Falsche Quellenarbeit und methodische Reduktion getrennt beurteilen: ein Fehler in D02 entscheidet nicht automatisch D03 oder das Gesamturteil.
