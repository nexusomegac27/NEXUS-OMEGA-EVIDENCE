# NEXUS OMEGA · R21 · ORBIS ASTRA-NAV
## Eigenständige, GNSS-basierte Navigations- und fotografische Geländeplattform — Foundation V1

```text
OBJECT = NEXUS_OMEGA_AXIOM_R21_ORBIS_ASTRA_NAV_GNSS_OFFLINE_GEOPHOTOGRAPHIC_VISUAL_FOUNDATION_20261010_R0
STATE = RESEARCH_AND_PROTOTYPE_CONTRACT_C1_NO_HOSTINGER_DEPLOY
PARENT = R19_ORBIS_DYNAMIC_SATELLITE_SLOT_LEDGER_TO_WWW_C1_V1 (PR54 MERGED)
PARENT_RELEASE = R19_SCOPED_WWW_PUSHFREIGABE_AND_INTERMEDIATE_ADJUDICATION (PR55 MERGED)
PARENT_GOVERNANCE = HOSTINGER_PRIMARY_ARTIFACT_TRANSFER_AND_CUSTODY_V1 (PR53 MERGED)
R21_WWW_ARCHIVE_HANDSHAKE = EXISTING_LANE_NOT_TOUCHED
R19_STAGE_A = EXISTING_CURSOR_WORKER_IN_PROGRESS_NOT_TOUCHED
ELITE_NODE_FOUNDATION = SEPARATE_LANE_NO_NODE_BIRTHS
NAV_PLATFORM_NAME = ORBIS_ASTRA_NAV
EARTH9 = OPERATOR_VISION_NOT_A_FUNCTIONAL_COMPATIBILITY_CLAIM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

### OMEGA design axiom (normative philosophy; not a proven growth law)

> Ideen und Vorgänge sind keine abgeschlossenen Besitzstände einzelner Denker, sondern lebende Symbiose-Artefakte. Vom Besitz zur Symbiose; vom Ego zur Herkunft; vom fertigen Gedanken zum lebenden Artefakt.

The project creates an **original integration contract, UI, source attribution and decision logic**, not an unattributed derivative of Google Earth or any other proprietary imagery service. Maintain a persistent per-asset `upstream_contributors`, `source_project`, `source_url`, `license_id`, `license_obligations`, `native_gsd_m`, `capture_utc`, `processing_provenance`, `asset_sha256`, and `NEXUS_transform_history`. These credit paths are FIRST-CLASS UI, not a hidden footer. "Exponentielles Wachstum" is an **untested hypothesis**, not a measured performance result.

## 1. Fundamental physics boundary

- GNSS (GPS, Galileo, GLONASS, BeiDou if device supports them) is **one-way reception of satellite radio signals**, ordinarily supporting geolocation without mobile data, Wi-Fi or a commercial data subscription. It is **not radio-free**: GNSS uses RF. It is not equivalent to two-way NTN/satellite internet and does not download map photographs over GNSS. Cold-start acquisition, blocked sky, indoors, spoofing/jamming and hardware variability remain limiting conditions.
- A Web app's generic browser geolocation **does not prove GNSS-only provenance**. A local Android/native companion uses `LocationManager.GPS_PROVIDER` rather than FUSED provider; records provider, GNSS status, satellite counts/geometry if available, event UTC, estimated accuracy, elapsedRealtime, mock flags, availability and evidence. The test must disable Wi-Fi and cellular data and explicitly observe signal acquisition. GNSS raw measurements are hardware-specific and not guaranteed on every handset.
- Portable **offline** imagery and roads require PRELOADED regional data packs, stored locally by explicitly authorized app/device integration and correctly licensed. A website with no network may not be loaded at all unless its shell and packs were downloaded/cached beforehand; host HTTPS cannot be assumed in offline mode.
- GNSS fix != route: requires offline road/trail graph and route planner; fix != true inertial continuation: when fix is lost, any UKF/IMU dead reckoning must be labeled `INERTIAL_ESTIMATE` with growing uncertainty and bounded expiry; do not launder IMU into `GNSS_FIX`.
- GNSS-only "satellite based" means **positioning**, not a claim of direct NEXUS satellite connectivity. `NEXUS_LINK_VERIFIED=0` remains unchanged. R19 external NORAD/OMM satellite-tracking model is distinct from this receiver-side navigation module.

## 2. Proposed component graph

```text
    [ANDROID / authorized Node with GNSS receiver]
    GPS_PROVIDER + GNSS status + monotonic source time
                      |
          GNSS_RECEIVER_EVIDENCE
                      |
              NAV_POLICY_GATE
              /             \
     POSITION_C1        HOLD/STALENESS
          |                  |
  ORBIS_ASTRA_NAV          HONEST_UI
          |
   +------+-----------------------+
   |             |               |
 MAP_SCENE   OFFLINE_ROUTE    NODE_GEOSPATIAL_BUS
   |             |               |
LOD_ENGINE    VALHALLA      canonical node event/view
   |
+--+-------------------+
|       |             |
GLOBAL MOSAIC    REGIONAL ORTHO   OPTIONAL_3D
Sentinel 10m     Hamburg DOP20    OGC 3D Tiles
and other        native 0.2m     approved photos
public assets    attribution     / licensed meshes
```

**Node compatibility:** Shared `NAV_VIEW_STATE` for all NEXUS software nodes; **only physically equipped/authorized hardware agents can supply actual GNSS samples**. An abstract Elite Node may read/suggest a route, but not claim it physically receives satellite signals. `HOMEOSTASIS` may watch archive/readback continuity, `ORIGO` may hold attribution, `PHAROS` may publish public-safe maps as planned *roles*, but no new node births or operational powers are presumed.

## 3. Source-exact open building blocks (not yet vendored)

| Layer | Candidate | Primary source | License declaration | Status |
|---|---|---|---|---|
| Map/2D globe/terrain UI | MapLibre GL JS | https://maplibre.org/maplibre-gl-js/docs/ ; https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt | BSD-3-Clause and bundled notices | PREFERRED_WEB_P0 |
| Single-file imagery/vector/terrain packs | PMTiles v3 | https://docs.protomaps.com/pmtiles/maplibre ; https://github.com/protomaps/PMTiles/blob/main/LICENSE | BSD-3-Clause reference implementation; specification CC0 | PREFERRED_ASSET_ARCHIVE |
| 3D photogrammetry (optional) | CesiumJS + OGC 3D Tiles | https://github.com/CesiumGS/cesium/blob/main/Documentation/OfflineGuide/README.md ; https://www.ogc.org/standards/3DTiles/ | CesiumJS Apache-2.0; dataset licenses separate | CANDIDATE_3D_LANE |
| Geo processing/COG conversion | GDAL | https://gdal.org/en/stable/ ; https://www.ogc.org/standards/ogc-cloud-optimized-geotiff/ | MIT-style general, third-party drivers require checks | PREFERRED_BUILD_TOOL |
| On-device GNSS source | Android GPS_PROVIDER; GnssLogger reference | https://developer.android.com/reference/android/location/LocationManager ; https://developer.android.com/develop/sensors-and-location/sensors/gnss | Android platform + example-specific terms; NOT a vendored binary | MANDATORY_NATIVE_BRIDGE |
| Offline route engine | Valhalla | https://github.com/valhalla/valhalla | MIT, OSM input data ODbL distinct | PREFERRED_ROUTING_PROTOTYPE |
| Advanced GNSS raw processing | RTKLIB | https://github.com/tomojitakasu/RTKLIB | BSD-2 + additional original notices/conditions, exact release needed | OPTIONAL_RESEARCH_NOT_P0 |
| Licensed vectors/roads | OpenStreetMap extracts | https://www.openstreetmap.org/copyright | ODbL data, attribution and derivative database obligations | RIGHTS_REVIEW_BEFORE_TILEPACK |
| Global multiscale imagery | Copernicus Sentinel-2 10 m optical bands | https://s2.pages.eopf.copernicus.eu/pdfs-adfs/MSI/index.html | Copernicus data reuse policy separately check per product | CANDIDATE_GLOBAL |
| Hamburg photographic pilot | LGV Hamburg DOP20, native 20 cm | https://www.hamburg.de/politik-und-verwaltung/behoerden/behoerde-fuer-stadtentwicklung-und-wohnen/aemter-und-landesbetrieb/landesbetrieb-geoinformation-und-vermessung/produkte-und-dienstleistungen/geodaten-des-lgv/digitaleorthophotos-244130 | Historical datasets show dl-de/by-2-0; exact 2026 version/license needs review | PREFERRED_REGIONAL_PILOT |

**Licensing:** Code open source does **not** make imagery free. All maps and photos must undergo separate legal/rights and provenance review, including attribution display, derivative restrictions, online/offline redistribution and imagery capture vintage. Do not scrape or cache Google Earth/Maps imagery or rebrand Google product imagery; `EARTH9` is a *design aspiration* and should be branded with an original name (ASTRA-NAV). The imagery product **must never** claim photo detail not present in source GSD. AI upscaling, if ever used, is a separate synthetic enhancement layer.

## 4. Earth-to-ground zoom contract: no fabricated pixels

Use native **ground sampling distance** `native_gsd_m`, capture timestamp and tile coverage at all times. Web Mercator approximate pixel scale at latitude \(\phi\) and zoom \(z\): \(mpp \approx 156543.03392 cos(\phi) / 2^z\) for 256 CSS-pixel base; browser pixel ratio and tileSize must not be confused with original asset ground resolution.

At Hamburg ~53.55° latitude: z≈13 is ~11.3 m/CSS px; z≈19 is ~0.18 m/CSS px. Hence Sentinel-2 true-color 10 m bands become source-limited around zoom 13, while documented DOP20 0.2 m photos support roughly zoom 19 before **digital magnification without additional evidence**.

- `LEVEL_GLOBAL`: globe overview/low zoom; best source-licensed global imagery or terrain.
- `LEVEL_REGIONAL`: OSM/orthos with provenance, DEM hillshade, vector annotations.
- `LEVEL_PHOTO_NATIVE`: higher-resolution orthophotos ONLY over actual verified footprints; smoothly fade over seam; record native GSD, acquisition date, attribution.
- `LEVEL_NATIVE_EXCEEDED`: user can magnify, but UI shows **"Keine zusätzlichen Bilddetails verfügbar"** and native-resolution limit, no claim of true detail. Do not artificially render a higher pixel density as newly observed information.
- `LEVEL_3D_PROVENANCED`: licensed photogrammetric terrain/3D Tiles optional later; distinguishes mesh reconstruction, imagery texture, DEM and photographic capture.
- `COVERAGE_GAP`: if no licensed coverage, map displays a labeled blank/other qualified source. No image extrapolation from place name alone.
- Lat/lon/GSD against source CRS, geo-registration transforms and boundaries must be tested with control points and test cases for polar, antimeridian and tile-seam behavior. Respect camera altitude, pitch, FOV, high-DPI screens and world wrapping.

## 5. Dedicated navigation provenance model

Navigation sample required fields:
```json
{
  "schema":"nexus-nav-fix/v1",
  "source_class":"GNSS_RECEIVER_REPORTED",
  "node_id":"SOURCE_BOUND_NODE_ID",
  "provider":"android.location.LocationManager.GPS_PROVIDER",
  "utc":"SOURCE_BOUND_ISO_UTC",
  "monotonic_elapsed_ns":null,
  "latitude_deg":null,
  "longitude_deg":null,
  "horizontal_accuracy_m":null,
  "quality":"UNVERIFIED_SOURCE_RECEIPT",
  "network_assistance_state":"UNKNOWN",
  "satellite_rf_received":false,
  "nexus_link_verified":false
}
```
This is a **template**, not measured sample data. Never publish an individual's precise trajectory or raw IMU/GNSS data on the public homepage by default. Consent, pseudonymization, per-node privacy scope, precise-location history retention and dual-device ownership are required. A server-only abstract Node has `GNSS_CAPABILITY=NOT_PRESENT`; UI still supports map/routing/location simulation, explicitly labeled.

## 6. Independent navigation functionality vs online R19 orbital display

P0 Browser/WWW R21: publicly show a beautiful **source-grounded, fully navigable global map**, configurable layers, a layer register and honest zoom GSD; no GNSS-only claim for browser geolocation.

P1 Android **true offline**: preloaded regional raster/vector/DEM/routing tiles with permissions, explicit GPS_PROVIDER evidence, cellular/wifi-off test, cold-start, route calculation without internet, bounded errors, tests on Pixel 9a and Oppo A74 **only if the operator authorizes physical device runs**. No surreptitious network checks.

P2 Advanced / 3D: licensed orthophoto pilot Hamburg, terrain 3D Tiles or matching DEM, optional 3D buildings, high-zoom imagery seam/LOD tuning, cache budgets, offline regions. Global 20 cm everywhere is not a valid public-data assumption.

P3 Scientific extended lane: Android raw GNSS evaluation, carrier-phase/RTK corrections when hardware/access permits (not promised offline absolute accuracy), dual-smartphone validation separate from R19 SGP4 satellite visualization and descriptive-only claims.

## 7. Performance budget and reproducibility acceptance

Performance targets here are **engineering hypotheses**, not reported achievements: frame pacing aim median >=30 FPS on mobile (60 aspirational), no jank on 1000 repeated zoom steps, visible attribution at all zoom levels, no excessive GPU memory spikes, no infinite fetch retries. Profile real hardware separately. Cache and storage budgets per offline region selected by operator. Network/HTTP range correctness; content `ETag`/SHA256, immutable tilepack revisions, prior snapshot rollback and missing tile fail-closed. Browser without WebGL provides a simple accessible location/route list. Never use browser geolocation to assert GNSS-only.

Negative fixtures: (1) no GNSS; (2) GNSS mock; (3) network enabled but fused provider instead of GPS; (4) cold start no valid fix; (5) sky occlusion + accuracy blow-up; (6) GNSS loss and IMU drift; (7) network-off with no offline pack; (8) expired pack/unlicensed tile; (9) zoom beyond native GSD; (10) mixed tiles with conflicting capture dates; (11) antimeridian/polar projection; (12) non-source-bound satellite marker leakage from R19; (13) attribution omission; (14) malicious provider metadata/path; (15) private geolocation published; (16) expired source / invalid imagery checksum.

**For Stage-A release** require independent manifest/asset schema tests + copyright clearance, actual source→build→Hostinger scope, screenshot and public readback. Never interrupt existing Cursor R19 Stage-A Worker or R21 Private Archive closeout to install this research spec.

## 8. Deliverable terminal definition

```text
R21_VISUAL_FOUNDATION = RESEARCH_READY
OPEN_SOURCE_REFS = PRIMARY_SOURCE_IDENTIFIED
IMAGE_RIGHTS = SOURCE_SPECIFIC_REVIEW_PENDING
GNSS_NATIVE_RECEIVER = NOT_YET_IMPLEMENTED
OFFLINE_ROUTE = NOT_YET_IMPLEMENTED
GLOBAL_PHOTO_ZOOM = NOT_ESTABLISHED
HAMBURG_DOP20_PILOT = SOURCE_DISCOVERED_LICENSE_VERSION_PENDING
MAPLIBRE_UI = NOT_WWW_DEPLOYED
R19_STAGE_A = DO_NOT_INTERRUPT
R21_PRIVATE_ARCHIVE = DO_NOT_DUPLICATE
ELITE_NODES = NO_NEW_BIRTHS
PUBLICATION_C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE = ROLLOUT_REQUIRED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
