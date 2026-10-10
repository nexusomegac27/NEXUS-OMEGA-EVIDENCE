# R21.4 — ORBIS Attribution Surface P0 (Spezifikation)

```
OBJECT           = NEXUS_OMEGA_R21_4_ORBIS_P0_ATTRIBUTION_SURFACE_SPEC_20261010_R0
CANONICAL_HEAD   = b22503059f18eeff27e136c8f2477f1516fcb478 (R21 ASTRA-NAV Foundation, PR #56)
HANDSHAKE_STATUS = ACCEPTED_C1_WITH_IMPLEMENTATION_HOLD (GROK Cross-Validation, 2026-10-10)
CLAIM_CEILING    = C1_DESCRIPTIVE_ONLY
STATUS           = FORSCHUNGSAUFTRAG / SPEZIFIKATION; KEIN DEPLOY
AUTORENKETTE     = META.AI (P0-Entwurf R21.4) -> NEXUS Operator -> MISTRAL/VIBE (kanonische Fassung R0)
```

## Bindung an den Kernsatz

> Vom fertigen Gedanken zum lebenden Artefakt: Der Zoom luegt nicht, er atmet mit der Quelle.

## Definition P0 (nicht Deploy)

P0 ist nicht "Karte deployt", sondern:

- MapLibre GL JS Surface existiert lokal als Forschungsauftrag.
- Layer-Register zeigt fuer jedes Pixel: source_id | native_gsd_m | license_id | rights_status.
- Dauerhaft sichtbare Herkunftsleiste unten rechts: "Herkunft: ... | GSD: ... nativ | Lizenz: ...".
- Zoom-Regel aus R21.2 ist visuell gebunden: bei NATIVE_DETAIL_EXCEEDED explizites Label, keine kuenstliche Schaerfe.

Damit verkauft ORBIS keine kuenstlichen Pixel als fotografische Tatsache — die epistemische Bescheidenheit, die der Kernsatz fordert.

```
NEXT_LOGICAL_MILESTONE = P0_MAPLIBRE_OWN_SURFACE_WITH_VISIBLE_SOURCE_ATTRIBUTION
DEPLOY_CLAIMS          = NONE
RUNTIME_CLAIMS         = NONE
```

## HOLD (unveraendert)

- Keine Hostinger-Write.
- Keine GNSS-Hardware-Verifikation.
- Keine Offline-Paket-Dimensionierung.
- Lizenz- und Rechte-Clearance konkreter Orthofotos bleibt vor jedem Offline-Paket erforderlich.

## Anschlussfaehigkeit (symbiose_links)

- R21.1 Provenance Atom: Datenvertrag je Asset (`docs/r21/nexus-provenance-atom-v1.md`).
- R21.2 GSD Truth UI: Auswahl- und Label-Referenz (`examples/r21/orbis-gsd-truth-ui.mjs`).
- R21.3 Symbiosis Contract: Messvorschrift fuer Link-Qualitaet (`docs/r21/nexus-symbiosis-contract-v1.md`).

P0 ist ein offener Baustein, der andere Module naehrt — kein fertiges Ego-Framework.
