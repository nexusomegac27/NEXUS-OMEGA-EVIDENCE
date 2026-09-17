# NEXUS FORUM — Symbiose-Fundament R0

Status: **REVIEWABLE_BLUEPRINT_WITH_REFERENCE_TESTS_C1** · 2026-09-17.

Ein Forum, in dem Menschen entscheiden, Maschinen nachvollziehbar unterstützen und Widerspruch sichtbar bleibt. „Symbiose“ bezeichnet Zusammenarbeit mit getrennten Rollen; weder Bewusstsein noch wissenschaftliche Überlegenheit werden behauptet.

Dieses Paket ist eine umsetzungsorientierte, **noch nicht in R10 integrierte** Blaupause. Der lokale Referenzkern prüft ausgewählte Speicher- und Entscheidungsregeln; er ist kein produktives Forum. Der autorisierte Git-Branch transportiert diesen Kandidaten. Kein Merge, kein Website-Deployment, keine Foundation- oder Claim-Promotion.

## Einstieg

1. [Blaupause](docs/BLUEPRINT.md): Architektur, Datenfluss, API, Migration und Implementierungsplan.
2. [Zehn Fundamentverträge](docs/FOUNDATION.md): Governance, Epistemik, Review, Recovery und UI.
3. [Quellenentscheidungen](docs/SOURCE_ADJUDICATION.md): Herkunft, Konflikte, verworfene Claims.
4. [Forschungsabgleich](docs/RESEARCH.md): nachgelesene Primärquellen und eigene Ableitungen.
5. [Abnahmekatalog](docs/ACCEPTANCE.md): ausführbare und noch offene Tests.
6. [Cursor/Mistral-Handoff](docs/HANDOFF.md): getrennte Review- und Umsetzungsschritte.
7. [Eingangsprüfung](validation/INPUT_AUDIT.json), [lokale Tests](validation/TEST_RESULTS.json), [Return](RETURN.json), [Handshake](DELIVERY_HANDSHAKE.json).

## Inhalt und Reproduktion

Alle Pfade unten sind relativ zu diesem Kandidatenordner. Die eigenen Python-Dateien benötigen Python 3.12+; nur die Schemaprüfung benötigt zusätzlich `jsonschema` (in der Prüfungsumgebung bereits vorhanden). Keine fremden Installationsskripte werden ausgeführt.

```sh
python -m unittest discover -s research/r5/forum-symbiosis/tests -v
python research/r5/forum-symbiosis/scripts/verify_delivery.py research/r5/forum-symbiosis
python scripts/validate_repository_structure.py --root .
python -m unittest tests.test_repository_structure
```

- `schema/`: JSON Schema 2020-12 für Einträge/Reviews sowie SQLite-DDL.
- `scripts/reference.py`: eigener, isolierter Prüfadapter für kanonische Bytes, additive SQLite-Ereignisse und C1-Entscheidungstore.
- `tests/`: Negativfälle und positive Kontrollen. Kein Nachweis der historischen NF-F01–F10-Abdeckung.
- `examples/`: synthetisches, ausdrücklich als Beispiel markiertes Datenmaterial und UI-Token.
- `validation/`: aktuelle, begrenzte lokale Befunde; historische Cursor-Returns bleiben Fremdbelege.
- `scripts/audit_inputs.py`: optionaler Rehash der vier Originaleingaben; Originale sind nicht öffentlich mitgeliefert.

## Grenzen

Mistral/Vibe-Review dieser konkreten Fassung: **nicht vorhanden**. V0-Originale 00–08 und die vollständige MODEL-C-Review-Lieferung fehlen im Paket. Trial 001 bleibt **SPECIFIED_NOT_EXECUTED**. Vollständige Browser-/Accessibility-, Authentifizierungs-, Betriebs- und Wiederherstellungsabnahme steht aus.

Die Originalarchive bleiben lokal unverändert. Öffentliche Lieferung enthält eigene Synthese, Metadaten/Hashes und eigenen Referenzcode, keine privaten Dialoge, absoluten Benutzerpfade, Zugangsdaten oder kopierten Fremd-Scaffolds. Lizenzen nach Repository-Regeln: eigener Code Apache-2.0, eigene Dokumentation CC BY 4.0. Keine Aussage über Weiterveröffentlichungsrechte an den Originalarchiven.
