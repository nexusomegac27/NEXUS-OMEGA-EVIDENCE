# NEXUS OMEGA · R21R1 · WP-G1 — Cursor Scoped Deploy Handoff (ASTRA-NAV P0)

```text
OBJECT        = NEXUS_OMEGA_MISTRAL_VIBE_R21R1_CURSOR_SCOPED_DEPLOY_HANDOFF_20261010_R0
DATE_UTC      = 2026-10-10
TARGET        = https://www.nexus-mobile.de/orbis/astra-nav/ (additive, ausschliesslich diese Route)
WRITER        = CURSOR (operative Instanz fuer autorisierte Hostinger-Deploys)
SOURCE_PIN    = Merge-Commit des Implementierungs-PR R21R1 (im PR genannt)
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

Wichtig: Ein erfolgreicher Deploy allein ist kein WWW_LIVE_VERIFIED. Die drei Nachweise sind getrennt zu erbringen: Produktionsdateisatz-Hash, autorisierter Hostinger-Write-Receipt, unabhängiger Browser- und HTTP-Readback.

## 1. Vorbedingungen

1. Merge des Implementierungs-PR oder Checkout des gepinnten Commits.
2. CI grün auf genau diesem Commit (Workflow validate-r21-astra-nav.yml), insbesondere: node scripts/r21r1/verify-production-fileset-manifest.mjs mit PASS.
3. Manifest vorhanden: validation/r21/r21r1/astra-nav-p0-production-fileset-manifest.json.

## 2. Deploy (ein Schritt)

```bash
git fetch origin <pinned-commit>
git checkout <pinned-commit>
node scripts/r21r1/verify-production-fileset-manifest.mjs
# muss PASS ausgeben, danach exakt diese vier Dateien ausliefern:
#   examples/r21/astra-nav-p0/index.html   -> /orbis/astra-nav/index.html
#   examples/r21/astra-nav-p0/app.mjs      -> /orbis/astra-nav/app.mjs
#   examples/r21/astra-nav-p0/ui-model.mjs -> /orbis/astra-nav/ui-model.mjs
#   examples/r21/astra-nav-p0/style.css    -> /orbis/astra-nav/style.css
```

Nur diese vier Dateien. Keine anderen Routen, keine Überschreibung von R19 oder bestehenden Inhalten.

## 3. CSP- und Header-Checkliste

- script-src: self; MapLibre bevorzugt lokal ausgeliefert (oder erlaubtes CDN mit Subresource-Integrity).
- style-src: self; keine externen CSS-Hosts.
- img-src und worker-src: Kachel- und Style-Endpunkte des P0 (OpenFreeMap) sowie data-URLs.
- connect-src: nur die benötigten Kachel- und Style-Endpunkte; keine unnötigen Hosts.
- Keine Nutzung von navigator.geolocation im P0 (Quelltext geprüft; kein Standort-Feature).
- Relative Pfade bleiben relativ; keine absoluten Hostnamen im HTML.

## 4. Unberührte Substanz

- R19 Stage A: keine Änderung.
- Private R21-Hostinger-Archive: keine Änderung.
- Elite-Nodes: keine Änderung, keine Neugeburten.
- Rollback: Route-Ordner /orbis/astra-nav/ entfernen oder vorherigen Stand wiederherstellen; danach den Readback erneut prüfen.

## 5. Unabhängiger Readback (Nachweis C)

- Desktop 1440 x 900 und Mobil 390 x 844: Karte sichtbar, Zoom und Pan bedienbar, Attribution sichtbar, R19-Satellitenanzeige ungestört.
- HTTP-Readback: GET auf https://www.nexus-mobile.de/orbis/astra-nav/ mit Status 200; Body-SHA-256 aufzeichnen.
- Asset-SHA-Receipt: SHA-256 der tatsächlich geladenen Assets erfassen (Entwicklerwerkzeuge oder Mitschnitt).

## 6. Closeout-Receipt

Vorlage im Repository: validation/r21/r21r1/www-closeout-receipt.pending-example.json. Nach erfolgreichem Deploy füllt Cursor:

- production_fileset: state PASS, rollback_witness, observed_utc.
- hostinger_scoped_write: state PASS, writer_role, write_receipt_id, file_hashes_match = true, observed_utc.
- independent_public_readback: state PASS, unabhängiger Reviewer, alle booleschen Flags true.
- terminal_state: WWW_LIVE_VERIFIED nur, wenn alle drei Nachweise vollständig erbracht sind; andernfalls bleibt NOT_LIVE_VERIFIED.

Validierer: examples/r21/r21r1/www-closeout-receipt.mjs; Schema: schema/r21/r21r1/www-closeout-receipt.schema.json.

## 7. Negative Evidence (was nicht als LIVE gilt)

- Ein GitHub-Merge ohne Hostinger-Write.
- HTTP 200 ohne Content-Match der Hashes.
- Fehlende oder nicht sichtbare Attribution.
- Prüfskript-Fehler im Produktionsdateisatz-Manifest.
- Störung von R19 Stage A.
- Readback ohne unabhängigen Reviewer.
