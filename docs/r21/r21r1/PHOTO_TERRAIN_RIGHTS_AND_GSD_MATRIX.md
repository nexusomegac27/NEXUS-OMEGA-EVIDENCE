# NEXUS OMEGA · R21R1 · WP-G4 — Fotografisches Gelände: Rechte- und GSD-Matrix

```text
OBJECT        = NEXUS_OMEGA_MISTRAL_VIBE_R21R1_PHOTO_TERRAIN_RIGHTS_AND_GSD_MATRIX_20261010_R0
DATE_UTC      = 2026-10-10
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = RIGHTS_MATRIX_C1 (Dokumentation; keine Rechtsberatung)
```

## 1. Quellenmatrix

| Quelle | Rechte-Lage | Lizenz | Native GSD | Pflichten | Produktions-Gate |
|---|---|---|---|---|---|
| Hamburg DOP20 (LGV, Befliegungen 2017 und 2018, laubfrei) | Lizenzgrundlage offen dokumentiert; formale Freigabe bleibt Operator-Entscheidung | DL-DE-BY-2.0 | 0,20 m | Quellenvermerk: Freie und Hansestadt Hamburg, LGV; keine Änderung der Herkunftsaussage | NO_PUBLISH, solange rights_status = RESEARCH_ONLY_UNTIL_CLEARANCE; erst nach dokumentierter Freigabe PUBLISH_ALLOWED mit sichtbarer Attribution |
| Sentinel-2 (Copernicus) | Lizenzgrundlage frei (free, full and open); formale Freigabe bleibt Operator-Entscheidung | Copernicus-Datennutzungsbestimmungen | 10 m (sichtbares Spektrum und NIR) | Copernicus-Bestimmungen; keine erfundene Auflösung jenseits von 10 m | gleiche Atom-Regel; GSD-Gate bei 10 m |
| Proprietäre Orthofotos ohne Herkunftskette (Beispiel: Google Earth) | PROHIBITED | keine Nutzungsrechte für Kachelauslieferung nachweisbar | nicht belegbar | keine belegbare Herkunft | DENIED_NO_PUBLISH; keine Ausnahme |

Fail-closed-Standard: jede neue Fotoquelle startet bei RESEARCH_ONLY_UNTIL_CLEARANCE und bleibt so lange unpublizierbar.

## 2. GSD-Wahrheit

- DOP20: native 0,20 m. Oberhalb der nativen Auflösung (bei 53,55 Grad Nord etwa ab Zoom 19) gilt NATIVE_DETAIL_EXCEEDED: es entstehen keine neuen fotografischen Details, nur digitale Vergrößerung. Implementiert in zoomTruth und getestet.
- Hochskalierung oder Super-Resolution unter die native GSD: INVENTED_DETAIL_BEYOND_NATIVE_GSD, fail-closed über die Transformation-Chain-Prüfung.
- Ein gleichzeitiges Erscheinen von nicht freigegebenen Assets und Zoom über nativ ist ausgeschlossen: das Publishing-Gate greift vor jedem Zoom.

## 3. Transportformat-Anforderungen (PMTiles/COG)

Begleitendes, maschinenlesbares Manifest je Tileset (implementiert in photo-tile-provenance.mjs und im JSON-Schema):

- provenance_atom: Asset-ID, Contributors, Quell-URL, Lizenz-ID, native GSD, acquired_utc, asset_sha256, rights_status, sichtbare Attribution (first_class = true).
- transformation_chain: je Schritt step, method, output_gsd_m; die Output-GSD darf nie unter die native GSD fallen.
- derived: tile_format (PMTILES oder COG), tileset_sha256, tile_size_px (256 oder 512), zoom_min/zoom_max, footprint_wsen.
- visible_attribution_label muss exakt dem Label des Atoms entsprechen (ATTRIBUTION_MISMATCH sonst).

## 4. Negative Evidence (implementiert und per Tests erzwungen)

- RESEARCH_ONLY_UNTIL_CLEARANCE: NO_PUBLISH_RESEARCH_ONLY_UNTIL_CLEARANCE.
- DENIED: DENIED_RIGHTS_NO_PUBLISH.
- Erfundene Details unter nativer GSD: INVENTED_DETAIL_BEYOND_NATIVE_GSD.
- Zoom über nativ: NATIVE_DETAIL_EXCEEDED, new_photographic_detail = false.
- Attribution-Abweichung: ATTRIBUTION_MISMATCH.
- Research-only Assets erzeugen in der Produktionsauswahl eine COVERAGE_GAP, nie eine Kachelanzeige.

## 5. Quellen (keine Rechtsberatung)

- Transparenzportal Hamburg (DOP20-Metadaten, DL-DE-BY-2.0, Quellenvermerk Freie und Hansestadt Hamburg, LGV): https://suchen.transparenz.hamburg.de/
- Copernicus Data Space Ecosystem: https://dataspace.copernicus.eu/
- GovData, DL-DE-BY-2.0: https://www.govdata.de/dl-de/by-2-0
