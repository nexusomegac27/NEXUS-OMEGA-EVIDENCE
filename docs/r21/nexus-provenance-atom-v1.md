# R21.1 — NEXUS Provenance Atom v1 (Herkunfts-Atom)

```
OBJECT           = NEXUS_OMEGA_R21_1_PROVENANCE_ATOM_SPEC_V1_20261010_R0
CANONICAL_HEAD   = b22503059f18eeff27e136c8f2477f1516fcb478 (R21 ASTRA-NAV Foundation, PR #56, merged 2026-10-10T07:02:15Z)
HANDSHAKE_STATUS = ACCEPTED_C1_WITH_IMPLEMENTATION_HOLD (GROK Cross-Validation, 2026-10-10)
CLAIM_CEILING    = C1_DESCRIPTIVE_ONLY
STATUS           = SPEC + JSON SCHEMA + REFERENCE VALIDATOR + FAIL-CLOSED TESTS
RUNTIME          = NONE (kein Deploy, keine Bildkacheln, kein Hostinger-Write, keine GNSS-Laufzeit)
AUTORENKETTE     = META.AI (Spec-Entwurf R21.1) -> NEXUS Operator -> MISTRAL/VIBE (kanonische Implementierung R0)
```

## Bindung an den Kernsatz

> Vom Ego zur Herkunft. Der Name bleibt, aber als Spur, nicht als Besitz.

Jedes ASTRA-NAV-Asset wird ein lebendes Symbiose-Artefakt. Das Herkunfts-Atom ist der versionierte Datenvertrag, der diese Forderung pruefbar macht:

**Symbiose-Regel: Kein Asset ohne Atom. Kein Atom ohne sichtbare Herkunft.**

Damit werden Denker und Quellen nicht geloescht, sondern als bleibende Herkunfts-Spuren im Artefakt selbst mitgefuehrt.

## Datenvertrag (v1)

```json
{
  "asset_id": "hamburg-dop20-2021-tile-research",
  "upstream_contributors": ["Landesbetrieb Geoinformation und Vermessung Hamburg", "Copernicus Sentinel-2"],
  "source_url": "https://example.org/original",
  "license_id": "DL-DE-BY-2.0",
  "native_gsd_m": 0.20,
  "acquired_utc": "2021-03-15T10:00:00Z",
  "asset_sha256": "<64 Hex-Zeichen ueber die exakten Bytes>",
  "rights_status": "RESEARCH_ONLY_UNTIL_CLEARANCE",
  "attribution": {
    "first_class": true,
    "visible_label": "Hamburg DOP20 (0,20 m) - LGV Hamburg",
    "expiry_check_required": true
  },
  "nexus_transformation": "PMTiles repack, no resampling beyond native GSD",
  "symbiose_links": ["orbis-surface-p0", "gsd-gate", "offline-packet-p1"],
  "is_living_artifact": true
}
```

Maschinenlesbares Schema (kanonische Domain `schema`, siehe REPOSITORY_PATH_RULES): `schema/r21/nexus-provenance-atom-v1.schema.json`
Referenz-Validator: `examples/r21/nexus-provenance-atom.mjs`

## Feldregeln (fail-closed)

- `asset_id` — kanonischer Kebab-Case-Bezeichner.
- `upstream_contributors` — nicht-leer; jeder benannte Contributor bleibt als Herkunfts-Spur erhalten.
- `source_url` — HTTPS-Ursprung der Primaerquelle.
- `license_id` — zwingend (z. B. DL-DE-BY-2.0, CC-BY-4.0).
- `native_gsd_m` — endlich und groesser 0; die Wahrheits-Grenze des Assets.
- `acquired_utc` — ISO-8601 Z-Zeitstempel der Erfassung.
- `asset_sha256` — 64 Hex-Zeichen ueber die exakten Bytes. Kein Platzhalter akzeptiert.
- `rights_status` — RESEARCH_ONLY_UNTIL_CLEARANCE | APPROVED_FOR_THIS_USE | DENIED.
- `attribution.first_class = true` zwingend; `visible_label` nicht leer; `expiry_check_required` boolean, bei RESEARCH_ONLY_UNTIL_CLEARANCE zwingend true.
- `nexus_transformation` — beschriebene, ueberpruefbare Transformation; keine Erfindung von Details.
- `declared_output_gsd_m` (optional) — darf niemals kleiner als `native_gsd_m` sein, sonst INVENTED_DETAIL_BEYOND_NATIVE_GSD (fail-closed).
- `symbiose_links` — Liste gueltiger Modul-Verweise; Qualitaet wächst durch Beziehung, nicht durch Isolation.
- `is_living_artifact = true` zwingend.

## Abgrenzung zur R21-LOD-Rechtepruefung

Das Atom projiziert RESEARCH_ONLY_UNTIL_CLEARANCE fuer die Bildauswahl (`selectPhotoLayer`) als PENDING_REVIEW; ein solches Asset wird von der Auswahl nie freigegeben. Keine semantische Lueckenreparatur nach dem Fact — die Systemregel bleibt bindend.

## Pruefprogramm (C1, Code-Ebene)

`tests/r21/nexus-provenance-atom.test.mjs` — vier Negativfaelle, alle fail-closed:

1. Fehlende `license_id` -> BAD_LICENSE
2. Fehlende `native_gsd_m` -> BAD_GSD
3. Unsichtbare Attribution (`first_class = false` oder leeres `visible_label`) -> INVISIBLE_ATTRIBUTION
4. Erfundene Pixel jenseits der nativen GSD (`declared_output_gsd_m < native_gsd_m`) -> INVENTED_DETAIL_BEYOND_NATIVE_GSD

CI: `.github/workflows/validate-r21-astra-nav.yml` (erweitert). Geprueft wird nur Dokument- und Code-Ebene: keine Bildkacheln geladen, keine Schreiboperationen, keine GNSS-Laufzeit.
