# NEXUS OMEGA — R15 Finalabschluss und kausaler R16-Anschluss

```text
OBJECT = NEXUS_OMEGA_AXIOM_R15_ABSCHLUSS_UND_R16_ANSCHLUSS_20261018_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_SCOPE_CLOSABLE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = HUMAN_OPERATOR
EXECUTION_ORDER = NOT_ISSUED
MAIN_SOURCE = d355400dabed3c280e1fce5030cab69ea099428b
R15_PUBLICATION_PARENT = PR119_DRAFT
```

## HARD — AXIOM-Entscheidung

R15 ist **als C1-Forschungs-, Quellen- und isoliertes Prüffundament abschließbar**, nicht als produktiv validierte 3D-GIS-Kartierung. Die endgültige Forschungsadjudikation umfasst R0/R1/R2, die operatorvermittelten MANUS-/GROK-Prüftexte und einen neuen unabhängigen, retrospektiven 2D-Abdeckungscheck.

| Original | Gebundener Befund |
|---|---|
| R15-R0-Symbiose-Fundament | 6.917 B; SHA256 `0b32132b6a529edc441a3f929401fcfb77bcf54b37978f17dcb2dc8ebaefa58b` |
| R15-R1 GPS/FOV-Fundament | 25.683 B; SHA256 `2a1e05cf4d633df6a8729eb1dc793239900ad60c6d2e6c1f74c00367f158cad5` |
| R15-R1-ZIP | 110.827 B; Manifest 11/11 MATCH |
| R15-R2-ZIP | 28.881 B; Manifest 9/9 MATCH |
| R15-R1 Wiederholung | 29/29 PASS; Mutante 28/29 |
| R15-R2 Wiederholung | 22/22 PASS; Mutante 20/22 |
| Zusätzliches AXIOM-2D-Orakel | 64/64 Szenen, 190.254 synthetische Punktzeugen, kein beobachteter Fehlpunkt |

**Forschung geschlossen heißt nicht wissenschaftliche Wahrheit bestätigt:** Es wurde weder echtes GPS verarbeitet noch eine 3D-Engine integriert, ein Offline-Browserlauf durchgeführt, reales Übertragungsvolumen gemessen oder ein Energieeffekt ermittelt. Keine externe unabhängige wissenschaftliche Freigabe. Die 2D-Prüfung ist kein analytischer Vollständigkeitsbeweis.

## Eigenständige wissenschaftliche Korrekturen

1. **W3C/Heading:** Der Norm-Pin lautet `https://www.w3.org/TR/2026/CR-geolocation-20260326/` (26.03.2026). `heading` bezeichnet Bewegungsrichtung, nicht optische Kamerarichtung; bei Stillstand kann es fehlen.
2. **3D-Tiles-Cache:** Der Fall NASA-AMMOS #1689 betrifft eine dokumentierte 0.5.1-Konfiguration. Das Issue ist geschlossen und der v0.5.3-Meilenstein/Release existiert. Ohne neue reproduzierbare Regression darf keine unbehobene aktuelle Sicherheits- oder Performance-Lücke behauptet werden.
3. **Entscheidende Leistungsgröße:** `tile_count != request_count != transferred_bytes != decoded_bytes != GPU_bytes != joules`. Ein geringerer Tile-Count beweist keine Bandbreitenreduktion. Browser-Resource-Timing alleine ist bei ServiceWorker/CORS nicht vollständig.
4. **Foundation-Identitäten:** Die 6.917- und 25.683-Byte-Dokumente sind **verschiedene Runden** und werden append-only getrennt geführt. Kein Source-Overwrite.
5. **Kanal:** R15-R2-Tests und Mutanten konnten durch AXIOM unabhängig aus dem Nutzer-Originalarchiv ausgeführt werden. Die originalen MANUS-/GROK-Returns kamen dennoch über Chat/ZIP, nicht über einen authentifizierten externen GitHub-Akteur.

## Forschungsentscheid für die GIS-Architektur

Primär `MapLibre GL JS` plus lizenzgeprüfte **lokale PMTiles** für Basiskarten und flächige Höhendaten. Optional `3DTilesRendererJS` für tatsächliches 3D und HLOD, nach separatem Performance-/Sicherheitsgate. `CesiumJS` als Vergleich bei begründetem Globus-/3D-Bedarf, nicht zwingende Runtime-Abhängigkeit. Alle Abhängigkeiten, Glyphen, Styles, Worker und Sprites lokal und reproduzierbar versionieren; Rollback bereitstellen. Sichtbereich muss **vor I/O** begrenzen, nicht nur beim Zeichnen.

## R16 — einzeln abnehmbarer Übergabekorridor

**E0: Originale und Rechte.** Nur autorisierte Datenquellen, CRS-/Einheiten-/Höhendatum, Zeitstand und Lizenz, genaue Commit-/Blob-/SHA256-Identitäten. R16-Eigenartefakte zuerst originalbytegenau lesen; ein GROK-Hinweis auf ein R16-„Attention“-Objekt ist kein Byteeingang.

**E1: Formale 3D-Sichtbarkeit.** Kamera-/GNSS-Zeitstempel, optische Ausrichtung getrennt von Kurs, Unsicherheit, horizontales und vertikales FOV, Frustum-AABB-/BoundingVolume-Test, SSE/LOD und mathematisch begrenzter Schutz gegen false negatives. Kritische Fixtures: nahe Kachelkanten, Pol-/Antimeridian-Fälle, Höhen, Pitch/Roll, Kameraschwenk, Eltern-/Geschwisterkacheln.

**E2: Echt offline.** Eigenständiger lesender Mini-Datensatz, kalter Browserkontext, alle CSS-/JS-/Worker-/Sprite-/Glyph-Quellen lokal, kontrollierte Netzwerkisolierung und vollständiges Request-Ledger inklusive ServiceWorker. Negativfixtures: HTTP 200 statt 206, unerwartetes CDN, Cache-Verdeckung, fehlender Font und Netzwerk-Redirect. Nur Anwendungsoffline bestätigen, keine absolute Behauptung über Betriebssystem-Hintergrundverkehr.

**E3: Gemessene Effizienz.** Gepaarter, vorregistrierter Versuchsplan auf unveränderlichen Ansichten, identischer Qualität/LOD, Cachebedingungen und Datensatz; übertragenen encoded Bytes aus unabhängigen Zählern, Requests, Refetches, visuelle Abdeckung, Latenz, CPU/GPU-Speicher und nur mit kalibrierter Quelle reale Energie messen. Nullhypothese „keine Byteersparnis“ nicht post hoc ändern. Quoten und Konfidenzintervalle ohne Ergebnis-Selektion.

**E4: Menschliche Symbiose.** Ansicht bleibt read-only und C1-illustrativ. Evidenzstatus textuell abrufbar; keine Ableitung von wissenschaftlicher Autorität aus visuellen Höhen, Flüssen, Farben oder GPS-Orten. Verständlichkeitsvergleich Karte vs. Quellenledger, Barrierefreiheit, subjektive Belastung, Datenschutz.

## Verbote und Kausalität

- Kein Import von echten Bewegungsprofilen, keine neue Node, kein Reset, kein Hostinger-Deploy und kein R16-Autostart.
- Keine Änderung von R9, R11/PR116, R12, R13, R14 oder R14/R15-Node-PR90.
- PR119 ist nur eine Draft-Research-Veröffentlichung; Merge und damit Main-Publikation bleiben gesondert zu beobachten.
- Externe Akteure erhalten ohne Owner-Allowlist keine Schreibrechte. Korrektur/Validierung erfolgt append-only, unabhängig von Produzentenbezeichnungen.

```text
R15_RESEARCH_C1 = CLOSED_WITH_MATERIAL_CAVEATS
R15_PRODUCTION = NOT_ESTABLISHED
R16_RESEARCH_ENTRY = PREPARED_NOT_EXECUTED
R16_ORIGINAL_BYTES = NOT_PRESENT_IN_THIS_USER_ARCHIVE
CLAIM_PROMOTION = NO
CURSOR_ACTION = NONE
```

`EVIDENCE > AGREEMENT · GPS_COURSE != CAMERA_HEADING · GIS_RAIL != SOFTTWIN_GRAPH`
