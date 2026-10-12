# NEXUS OMEGA — Forschungsregister: Clarity V1 (2026-10-12)

```text
OBJECT = NEXUS_OMEGA_PUBLIC_RESEARCH_CATALOG_CLARITY_C1_20261012_R0
AUTHORITY = OPERATOR_DIRECT_C1_PUBLIC_SAFE_RESEARCH_AND_WEBSITE_DESIGN
CANONICAL_WWW_ROUTE = https://www.nexus-mobile.de/research/catalog/
CANONICAL_DATA = /research/catalog.json
PREDECESSOR = NEXUS_OMEGA_CONTROLLED_PUBLIC_SCIENCE_CATALOG_20260922_R1
STATUS = SOURCE_READY_SITE_MOUNT_REQUIRES_EXISTING_AUTHORIZED_HOSTINGER_TRANSPORT
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Why extend, not replace the research system

The operator-supplied **NEXUS_WEBSITE_MOBILE_MIRROR** archive (ZIP container, 2026-10-12 snapshot) contains the *existing* live-site route `/research/catalog/`, the canonical `/research/catalog.json` and search `/research/search/`. The archived canonical catalog has **9 public records, 7 explicitly withheld records**, four exact publication classes, nine stable `/research/record/<PUBLIC_ID>/` links and a declared snapshot date of 2026-09-22. This page does **not** create new records, change their scientific status, or define a parallel publication state.

Its original JSON snapshot is 6,041 bytes, SHA256 `3a9523de0de020b95aca597e6d2191ff6dcae65efc31063585f5be4d45508670`. The sourced fallback `site/catalog-snapshot.json` includes only the nine already-public records and the numeric withheld count (not the withheld original bytes). Source is explicitly HISTORICAL_NON_CANONICAL_FALLBACK. A source fetch on the actual website is preferred and validated; a failed fetch never gets a false LIVE label.

## User research inputs / selection

- **nexus-sky-system.zip** original archive 3,726,984 bytes, SHA-256 `e57cfc095c9254c9e7ba805503a75320e7f8737e2900d22a9d3613efdd499fd9`: 23 ZIP entries with valid CRC and safe paths; contains deterministic Python-generated SVG/CSS, accessibility and reduced-motion approaches, and illustrative screenshots. Its *production* register has **one BORN / LIVE node and zero registered node-to-node edges**. Its **300-node DEMO** is synthetic and must never enter a productive C1 record catalog or public Node status. The unpublished Sky redesign also reports a different deterministic star position from the existing site's unknown formula; do not overwrite the homepage's production sky or animate fictitious relationships. Adopted design language only: restrained frosted blue typography and gold focus, low-amplitude decorative single-point orbit, reduced-motion and responsive spacing.
- **NEXUS_WEBSITE_MOBILE_MIRROR** original archive 1,960,710 bytes, SHA-256 `dd3c9d43ecbddc540c5d4d09cfb2e7cf1f145afe39d293d2b3f5c52537e90873`: 238 ZIP entries; offline site mirror, not a verification of today's host bytes, no upload of its bundled third-party fonts or Next.js compiled assets. Design found existing global `r16-` palette (`#0d1216`, `#34434a`, `#b6d6df`, focus `#e3b87d`), an established `/research/catalog/` and distinct publication-state index. These are extended, not reinvented.

## Selection from leading research platforms

- **Zenodo:** metadata-first records; type/date/identifier as primary findability surfaces. C1 records here carry PUBLIC_ID, title, publication class, evidence status and linked detailed source page. A NEXUS PUBLIC_ID is not mislabeled a DOI.
- **Open Science Framework:** object-type filters and search across heterogeneous research material. NEXUS uses its existing four PUBLICATION_CLASS values, no new scientific classes.
- **Hugging Face:** searchable cards and high-value filters with clear metadata and source links. NEXUS retains one light-weight textual result row per record rather than proliferating cards, graphs or trackers.

References: https://help.zenodo.org/docs/deposit/about-records/, https://help.osf.io/article/588-getting-started-with-osf-search, https://huggingface.co/docs/hub/search and https://huggingface.co/docs/hub/datasets-cards.

## Interface and behavior

- **One route, one list, one search, four class filters, one sort selector.** No secondary top navigation tier, homepage replacement, extra forum rail, standalone truth state, database, account or backend.
- User-readable labels map 1:1 onto existing exact classes `SCIENTIFIC_RESULT`, `ENGINEERING_RESULT`, `NEGATIVE_RESULT`, `OPEN_STATUS`. `EVIDENCE_STATE` is preserved verbatim in machine data and gently humanized for visual display; this is **not** claim promotion or a new grade.
- Source-backed filtering, sorting and URL-shareable query state. All user/source strings reach the DOM via `textContent`; `href` is allowlisted to `/research/record/<id>/`. No inline scripts, no external fonts, no tracker, no unsafe HTML renderer.
- Original data accessible at `/research/catalog.json`. All nine public record links also appear in initial plain HTML for no-JS and search engine fallback, labelled as the dated 2026-09-22 snapshot. The dynamic canonical catalog takes precedence on successful read. On error, `catalog-snapshot.json` yields a **prominent ARCHIVE-SNAPSHOT · NOT LIVE** warning; no silent stale truth.
- Seven withheld entries are summarized as a numeric count behind a collapsed disclosure; no withheld original file bodies are mirrored or promoted. Negative findings remain discoverable, not hidden behind default filters.
- Mobile min-width 320px, 44px-ish touch affordances, visible keyboard focus, `prefers-reduced-motion`, `forced-colors` fallback.
- The homepage Sky remains unchanged. The research catalog's ornamental glow has no Node data or status semantics.

## WWW mount — existing Hostinger site only, never parallel

See `SITE_EXISTING_RESEARCH_CATALOG_MOUNT.txt`. Deploy only into **the existing** `/research/catalog/` route:
```text
<existing_public_html>/research/catalog/index.html   <= site/index.html
<existing_public_html>/research/catalog/catalog.css  <= site/catalog.css
<existing_public_html>/research/catalog/catalog.js   <= site/catalog.js
<existing_public_html>/research/catalog/catalog-snapshot.json <= site/catalog-snapshot.json
```
Back up existing `index.html` first and record its SHA-256, source effective route and rollback point. Preserve `/research/catalog.json`, `/research/search/`, all record details, global Homepage, Forum, ORBIS, Nodes and anything else unchanged. Use the already authorized existing Hostinger hPanel/site channel, not an invented website. The existing research index **already links to Public science catalog**; do not add clutter to the homepage merely to duplicate that navigation.

Verify 200/HTTPS of route plus three assets, mobile 390px and desktop 1440px screenshot/keyboard, actual `catalog.json` load and no-JS fallback, false-live visibility when network blocked, total 9 and withheld 7 for the archived source, and no claim promotion. Record real before/after homepage and research status hashes. Source presence on GitHub is not a website deploy receipt.

## No unauthorized promotions

```text
SOURCE_CATALOG_ROWS = 9_PUBLIC_OBSERVED_IN_USER_SNAPSHOT
WITHHELD = 7_PRESERVED
SCIENCE = C1_DESCRIPTIVE_ONLY
SOURCE_CODE_GITHUB = PUBLISH_NOW
HOSTINGER_LIVE = NOT_ESTABLISHED_UNTIL_REAL_HTTPS_RECEIPT
NEW_PUBLICATIONS = NONE
NODE_ACTIVATION = NONE
SKY_DEMO_PRODUCTION = NO
R19_SCOPE = UNCHANGED
```
