# NEXUS OMEGA · R21R1 · WP-G3 — Offline-Routing-Engine-Vergleich (Pilot Hamburg)

```text
OBJECT        = NEXUS_OMEGA_MISTRAL_VIBE_R21R1_OFFLINE_ROUTING_ENGINE_COMPARISON_20261010_R0
DATE_UTC      = 2026-10-10
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = RESEARCH_NOTE_C1 (kein Runtime-Claim, kein Pack gebaut)
PILOT_SCOPE   = Region Hamburg (eine Region; kein globaler Anspruch in R21R1)
```

## 1. Kandidatenvergleich

| Engine | Lizenz (laut Projekt) | Offline-Modell | Einschätzung für R21R1 |
|---|---|---|---|
| Valhalla | MIT | Graph-Tiles serverseitig; On-Device möglich, aber schwer | Stark für zentrale Pack-Produktion; hoher Betriebsaufwand für P0 |
| GraphHopper | Apache-2.0 | Server und Android; Offlinedaten möglich | Solide Alternative; größere Integration als P0 benötigt |
| BRouter | eigene Lizenz im Repository (GPL-Basis, Lizenztext prüfen) | Offline-first; fertige Routing-Dateien für Android | Beste Passung für einen On-Device-Pilot mit kleinen Packs |

Kein Ausschluss der nicht gewählten Engines; die Bewertung ist revidierbar (lebendes Artefakt, keine Besitzstände).

## 2. Empfehlung für den Pilot

BRouter als Pilot-Engine für ein On-Device-Routing-Pack der Region Hamburg, weil das Design offline-first ist, kompakte Routing-Dateien existieren und keine Serverkomponente im P0 entsteht. Valhalla bleibt Kandidat für eine spätere zentrale Pack-Produktion. Diese Empfehlung ist eine Ingenieurbewertung unter C1, keine fertiggestellte Plattformentscheidung.

## 3. Fail-closed-Regel (implementiert und getestet)

NO_PACK_NO_ROUTE: Ohne verifiziertes Pack existiert kein Routing-Claim. Implementiert in examples/r21/r21r1/offline-pack.mjs und erzwungen im Node-Ereignisvertrag (ROUTE_COMPUTED_REQUIRES_PACK_REVISION). Ein Netzwerk-Fallback, der als Offline getarnt wäre, ist vertraglich ausgeschlossen.

## 4. Provenance-Pflichten je Pack

- Jedes Pack trägt eine provenance_atom_ref auf das R21.1-Herkunftsatom (Asset-ID, SHA-256).
- Archive je Rolle (routing_graph, map_tiles, attribution_manifest) mit SHA-256 und Bytezahl.
- produced_utc, min_client_version, update_policy mit rollback_supported = true.
- Input-Daten aus OpenStreetMap unterliegen der ODbL 1.0: sichtbare Quellenangabe der OpenStreetMap-Mitwirkenden und Weitergabe der Lizenzbedingungen bei abgeleiteten Datenbankauszügen.

## 5. Budgets (allesamt ESTIMATE, keine Claims)

- Routing-Pack Hamburg (BRouter, Rad und Auto): ESTIMATE im niedrigen zweistelligen Megabyte-Bereich; verifizierbar erst nach tatsächlichem Pack-Bau.
- Vector-Map-Pack Hamburg (PMTiles, Zoom 10 bis 14): ESTIMATE im Bereich von etwa 100 bis 300 Megabyte; messbar erst nach echtem Pack.
- Update-Budget: wöchentliche Packs sind plausibel (ESTIMATE); verbindlich erst mit einem realen Produktionsprozess.

## 6. Negative Evidence (implementiert und per Tests erzwungen)

- Fehlendes Pack: NO_PACK_NO_ROUTE.
- Pack ohne Routing-Graph: NO_ROUTING_GRAPH_IN_PACK.
- Andere Pack-Revision: PACK_REVISION_MISMATCH.
- Abgelaufenes Pack: PACK_EXPIRED.
- Außerhalb der Coverage: OUT_OF_COVERAGE.
- Pack ohne Provenance-Atom-Referenz: PROVENANCE_ATOM_REF_REQUIRED.
- Update-Policy ohne Rollback: BAD_UPDATE_POLICY.

## 7. Quellen (keine Rechtsberatung; Lizenzen anhand der Lizenztexte prüfen)

- Valhalla: https://github.com/valhalla/valhalla
- GraphHopper: https://github.com/graphhopper/graphhopper
- BRouter: https://github.com/abrensch/brouter
- ODbL 1.0: https://opendatacommons.org/licenses/odbl/summary/
