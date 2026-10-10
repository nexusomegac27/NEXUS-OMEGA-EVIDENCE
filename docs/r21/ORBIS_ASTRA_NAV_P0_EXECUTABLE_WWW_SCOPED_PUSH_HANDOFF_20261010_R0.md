# R21 ORBIS ASTRA-NAV · P0 Executable WWW Handoff · 2026-10-10

```text
OBJECT = NEXUS_OMEGA_AXIOM_R21_ASTRA_NAV_P0_EXECUTABLE_WWW_SCOPED_PUSH_HANDOFF_20261010_R0
SOURCE = PR57_R21_1_TO_R21_4_MERGED_598de3faf1a6c2dc1a59c5e258ff03219d7936a4
STATE = PUBLIC_SAFE_VECTOR_MAP_P0_SOURCE_READY_NOT_HOSTINGER_DEPLOYED
PRIMARY_TARGET = https://www.nexus-mobile.de/orbis/astra-nav/
EXISTING_R19_ORBIS_HOME = PRESERVE
R19_STAGE_A = NO_INTERRUPTION
R21_PRIVATE_ARCHIVE = NO_DUPLICATE_WORKER
ELITE_NODE_BIRTHS = NONE
C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE = WWW_ROLLOUT_REQUIRED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Executable source bundle

```text
examples/r21/astra-nav-p0/
  index.html     # standalone public navigation & attribution surface
  app.mjs        # MapLibre 6.13.0 + OpenFreeMap vector map + dynamic R19 safe markers
  ui-model.mjs   # pure source-bound public satellite contract and camera semantics
  style.css      # responsive mobile/desktop source panel
tests/r21/orbis-astra-nav-p0-surface.test.mjs
```

After merging this PR, these are public repository source artifacts, **not publicly served host files**. Before a new Hostinger route is declared operational, Cursor/PRAXIS must inspect the **actual** source tree/site account, find the permitted public webroot and route registry, confirm exact paths, create a rollback snapshot and preserve all R19/R21 predecessor files.

## Exact additive deploy (Cursor, authorized site access only)

1. Verify live site root and existing ORBIS routes and allowed write surface. Do not assume Evidence repo is the website repo.
2. Consume GitHub main at a pinned merge commit; copy the **four** P0 files as a single adjacent file set into a new isolated target route `/orbis/astra-nav/`. Keep `index.html` as index; `app.mjs`, `ui-model.mjs`, `style.css` resolve relative to the new page. Do NOT overwrite `/orbis/`, `/orbis/satellites/` or `/orbis/satellites/satellites.json`.
3. Add a small discoverable link on ORBIS main if the actual site markup and route audit permit it; source-bound, rollbackable. Do not register a new Elite Node or physically admit a satellite.
4. MapLibre dependency is pinned to `6.13.0` over the public jsDelivr release; OpenFreeMap Liberty source is `https://tiles.openfreemap.org/styles/liberty`. Site stays **online-dependent**. Prefer verified local hosting of exact MapLibre JS/CSS with upstream LICENSE/notice and exact SHA; **do not silently relax site-wide Content Security Policy** to make CDN work. Verify CSP/worker/img/connect permissions for site-selected host.
5. OpenFreeMap provides an online vector map under its publicly documented conditions and required attribution; underlying OpenStreetMap / OpenMapTiles credits must remain visible in the source bar and map native controls. Map tiles are *vectors*, not photographically measured pixels; there is NO licensed regional orthophoto pack in this P0 code.
6. The app reads the **same-origin** `/orbis/satellites/satellites.json`. A valid zero-element manifest yields **zero ORBIT_PREDICTED markers**, which is correct; an invalid or unavailable snapshot leaves the independent vector map and a visible error. Do not substitute fictional markers. User clicks use internal slug-bound detail links.
7. Independent predeploy test: `node --check` both modules and `node --test tests/r21/orbis-astra-nav-p0-surface.test.mjs`. CI pass validates pure code but not third-party tile URL reachability, CSP, browser pixel quality, offline mode, hardware GNSS or site source compatibility.
8. Browser test real public website at desktop 1440×900 and mobile 390×844: zoom, pan, OpenFreeMap vector layers, keyboard navigation, external tile load errors, permanent visible attribution, manifest count = 0, no fake satellite marker, R19 page unaffected, rollback. Capture public HTTP status and original body/assets SHA. Record accessibility and privacy.
9. Terminal receipts: `ACTUAL_PRODUCTION_FILESET_HASH`, `HOSTINGER_SCOPED_WRITE_RECEIPT`, `INDEPENDENT_PUBLIC_BROWSER_AND_HTTP_READBACK`; then optional screenshot + navigation route audit. Only when **all three** match may `P0_VECTOR_MAP_WWW=LIVE_VERIFIED` be declared.
10. Private Hostinger archive handshakes stay separate per `docs/governance/HOSTINGER_PRIMARY_ARTIFACT_TRANSFER_AND_CUSTODY_V1.md`; website asset publicity is not archive verification.

## Hard scope

- No GNSS-only claim: browser has no verified receiver source.
- No offline-navigation claim: map uses live external vector tiles and MapLibre CDN.
- No true photographic zoom claim: source has no licensed raster imagery.
- No `NEXUS_LINK_VERIFIED`, no direct satellite RF/data connection, no measured orbital position unbacked by OMM/SGP4.
- No personal location access or history; this P0 app does NOT request `navigator.geolocation`.
- No generic `true` or `LIVE` status from the act of merging a GitHub PR.
- No unauthorized production writes or new Cursor worker. Existing scoped deployment lane must import this new candidate when it reaches the relevant stage.

## Program terminal definition (R21 broader than P0)

```text
R21_FOUNDATION = GITHUB_MERGED_C1
R21_1_TO_R21_4 = GITHUB_MERGED_C1
P0_VECTOR_MAP = BROWSER_IMPLEMENTATION_CANDIDATE
P0_SITE_LIVE = NOT_YET_VERIFIED
P1_GNSS_ONLY_NO_CELL_WIFI = NOT_HARDWARE_TESTED
P1_OFFLINE_ROUTING = NOT_IMPLEMENTED
P2_PHOTO_ORTHOS = RIGHTS_AND_PACKAGES_NOT_PREPARED
P3_NODE_NAV_SYMBIOSIS = CONCEPT_ONLY
R21_FULL_PROGRAM_TERMINAL = NO
```

No new operator download handoff. Source/receipts via GitHub, byte archives via authenticated Hostinger private data plane by Cursor. All public-safe validated reversible P0 assets are automatically eligible for scoped WWW push once environment and actual license/CSP checks pass.
