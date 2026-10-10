# R19 ORBIS — Dynamic Satellite Slot Ledger → Public Manifest → Globe/Detail Contract V1

```text
OBJECT = NEXUS_OMEGA_AXIOM_R19_ORBIS_DYNAMIC_SATELLITE_SLOT_LEDGER_TO_WWW_C1_V1
DATE = 2026-10-10
AUTHORITY = OPERATOR_OMEGA / AXIOM_SOFT_GOVERNANCE
STATUS = IMPLEMENTATION_REFERENCE_READY_NOT_WWW_DEPLOYED
PARENT = NEXUS_OMEGA_OMEGA_C1_WWW_PUSH_AUTHORITY_V1
PARENT_TRANSPORT = NEXUS_OMEGA_OMEGA_HOSTINGER_PRIMARY_ARTIFACT_TRANSPORT_AND_CUSTODY_V1
R20 = CLOSED_BY_OPERATOR_WITH_CAVEATS_NON_INTERFERENCE
ELITE_NODE_FOUNDATION = SEPARATE_LANE_NO_NEW_BIRTHS
R21_PRIVATE_HOSTINGER_ARCHIVE = WORKER_IN_PROGRESS_SOURCE_REPORTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Outcome

The operator's architecture is accepted: `/orbis/` is the visual overview and `/orbis/satellites/?id=<slug>` is the source/telemetry/detail view. A single public same-origin snapshot `/orbis/satellites/satellites.json`, generated **from the verified Slot Ledger**, drives both interfaces. An added satellite appears without a manually edited HTML list. Absence of a calculable position leaves an *unpositioned satellite entry*, not a fabricated map marker.

**Do not publish the operator's illustrative GOES-16/-75.2 or AO-73/Berlin lat/lng fields as facts or `PASS` telemetry.** NOAA's 2025 GOES-East switch was from GOES-16 to GOES-19; bind XRS satellite identity from SWPC `instrument-sources.json` and each observation record, not from a fixed GOES name. AO-73 is not a NOAA GOES-XRS observation source. Current spacecraft operational/communications statuses require their own source. `TLE/OMM != TELEMETRY != NEXUS_LINK_VERIFIED`.

## Logical components, no fabricated production paths

- L0 `SLOT_LEDGER`: persistent private authorization/custody object, identifying admissions, withdrawals and revision IDs; **not itself a publicly trusted browser file**.
- L1 `INGEST`: CelesTrak CATNR→OMM JSON or CSV; NOAA SWPC GOES XRS only by cross-matched instrument/source and declared license; independent sources only when traceable. Prefer OMM: TLE 5-digit catalog limit was passed in July 2026; NORAD catalog IDs are strings (1–9 digits).
- L2 `VALIDATE`: schema, ID slug, NORAD/COSPAR, exact record association, times/UTC, license, instrument link, SGP4 reference/test vectors if actual positions, source freshness, SHA-256, quality; rights and expiry. Fail closed **per satellite**, not entire app.
- L3 `BUILD`: generate a complete, deduplicated, immutable-versioned manifest snapshot; record source hashes, build/revision/timestamp; update only when input changed or at permitted source cadence.
- L4 `WWW_PUBLIC`: atomic publish `/orbis/satellites/satellites.json` plus additive JS/CSS routes only; no direct browser fan-out to upstream on each visitor. Keep last known good and `STALE`/unavailable statuses. Hostinger private archive is distinct from public content.
- L5 `UI`: same-origin manifest consumed by ORBIS canvas adapter and detail route; accessible per-satellite list must work even without WebGL/Canvas; preserve existing illustrative Doctrine scene as a clearly labeled layer (not real satellite data).
- L6 `READBACK`: record origin URL HTTP status, exact source/public asset SHA, actual visible satellite list/marker count, desktop/mobile screenshots, missing/invalid ID behavior, rollback witness. Update global `NAVIGATION_ROUTE_AUDIT.md` only at real site source.

## Supported event-trigger state machine

```text
SLOT_CANDIDATE_RECEIVED
  → SOURCE_IDENTITY_CHECKED
  → PUBLIC_RIGHTS_AND_LICENSE_CHECKED
  → SOURCE_DATA_ACCEPTED_C1
  → SLOT_ADMITTED_C1
  → MANIFEST_BUILD_REQUESTED
  → MANIFEST_HASH_AND_SCHEMA_PASSED
  → HOST_WWW_ATOMIC_PUBLISH
  → PUBLIC_HTTP_AND_BROWSER_READBACK
  → DISPLAYED_C1
```

The trigger is a real **Slot Ledger revision event**, not a timer in HTML. The public front-end refreshes/checks manifests at an appropriate TTL or `ETag`; refresh is not an evidence-generating event. A failed data retrieval or source identity check produces `STALE` or `HOLD_SOURCE_GAP`, not imaginary coordinates. No autonomous Node birth, no permission escalation by `KAIROS` name.

## Semantics and timestamp dimensions

- `ORBIT_ELEMENTS_EXTERNAL`: source OMM/TLE epoch (model input) + source fetch; not actual real-time observed position.
- `ORBIT_PREDICTED`: actual position from a tested SGP4 propagation of a specific elements digest at a `target_utc`, frame conversion ECI→geodetic, units degrees/km, method/version and propagation error; not a measured satellite location.
- `LIVE_MEASURED_EXTERNAL`: actual instrument output with satellite NORAD identity, instrument, observed UTC, fetched UTC, units, and provider quality interpretation; SWPC observation only to the instrument's genuine source satellite.
- `NEXUS_LINK_VERIFIED=0`: persists unless independently proved end-to-end; map count has no bearing on this.
- T1 `source_event_or_element_epoch_utc` (origin), T2 `source_fetched_utc` (ingress), T3 `validated_utc` (source-exact check), T4 `published_utc` (verified public snapshot). Client `rendered_utc`/independent `readback_utc` are **distinct later times**, not evidence of source freshness.
- `quality_flag` is the upstream literal plus legend; no invented `PASS` generic flag. “ACTIVE” as a CelesTrak group label is **not** a verified spacecraft operational status. A satellite can be listed, stale, unpositioned or holding publication independently.

## Identity, URLs, events, security

`id` is a stable ASCII slug, `norad_cat_id` a 1–9 digit string, not a frontend-generated integer; `detail_url` must be constructed as an internal relative path from the canonical slug, never accepted from untrusted manifest content. Use `URLSearchParams`, reject malformed unknown IDs with non-200-like explanatory view or explicit `not found`; preserve keyboard accessibility and focus states. No HTML injection from `name`, upstream text, labels or error strings; use `textContent`.

`PUBLIC_ADMISSION=ADMITTED_C1` is not scientific truth. In a single compiled snapshot, identity must be unique by slug **and** NORAD ID, mapping sources must match, position must be fully source-linked, and the public UI must display source/provider/epoch/measurement/method and `STALE` when applicable. If source fetch fails do not make every browser fetch upstream; preserve cached snapshot with provenance or show unavailable.

For CelesTrak follow official cadence: GP changes approx once every **two hours**. Do not force one fetch per browser or every page load. Respect 429/50x/backoff and rights. NOAA time series have separate cadence and may change which GOES satellite is primary.

## Browser integration contract (Reference, not production implementation)

- Reference module: `examples/r19/orbis-satellite-directory.mjs`; pure manifest validation, identity lookup, marker eligibility, safe detail URL, accessible list/detail mount.
- Public manifest contract: `schema/r19/orbis-satellites-manifest.schema.json`; `examples/r19/orbis-satellites-empty.fixture.json` is a deliberate no-satellite startup fixture and must **never** be presented as live satellite data.
- `/orbis/`: create additive list mount and attach callback to existing globe renderer (unknown site-specific Canvas2D interface); call `selectPlottableSatellites()` for true position markers only; leave illustrative fixtures visually separate.
- `/orbis/satellites/`: read `?id=`, show exactly bound source/observation; if `id` absent preserve current aggregate TLE resource page rather than break it; do not overlay an incompatible new renderer.
- No source exact website code/tree is accessible in AXIOM's connector; Cursor alone must perform site-source integration, CSS, route audit, origin asset/permissions reconciliation and Hostinger public deploy under its existing authorized lane.

## Primary source witness links

1. NOAA GOES-19 operational as GOES East since 2025-04-07: https://www.nesdis.noaa.gov/news/noaas-goes-19-now-operational-goes-east-providing-critical-new-data-forecasters
2. NOAA SWPC XRS instrument source mapping: https://www.spaceweather.gov/products/goes-x-ray-flux and https://services.swpc.noaa.gov/json/goes/instrument-sources.json
3. CelesTrak OMM/CSV/JSON and 1–9 digit CATNR: https://celestrak.org/NORAD/documentation/gp-data-formats.php
4. CelesTrak source access policy (GP ~2h cadence): https://celestrak.org/usage-policy.php
5. Satellite.js parse/SGP4/ECI-geodetic documentation: https://shashwatak.github.io/satellite-js/docs/initialization

## Cursor acceptance & nondisruption

1. Confirm target site source, route IDs and document selectors; identify actual manifest ingress root and public asset write scope from its own permitted environment. Never guess Hostinger private paths.
2. Run negative fixtures (no coordinates, duplicate IDs, cross-satellite NOAA observation, old epoch, unknown query slug, unsafe HTML/name, upstream 429/50x, corrupted snapshot, cache stale); static tests `node --test tests/r19/orbis-satellite-directory.test.mjs` where Node supports ESM.
3. Implement the **smallest reversible additive** `/orbis/` directory/marker integration and `/orbis/satellites/?id=` detail, unmodified old /orbis/ illustrative layers; test desktop/mobile.
4. Check true source-accepted live slots. If none exists, publish a transparent `No admitted satellite yet` state, NOT fake data; independent approved C1 UI may still ship.
5. Once authorized scope established, publish and independently read back site files + manifest + screenshots + rollback; log `PRODUCTION_FILESET`, `WWW_WRITE`, `INDEPENDENT_PUBLIC_READBACK`. This R19 task is distinct from R21 private archive handshakes and Elite Node Foundation; **no second worker**.
6. Private hoster transfer follows existing canonical policy `docs/governance/HOSTINGER_PRIMARY_ARTIFACT_TRANSFER_AND_CUSTODY_V1.md`; the work does not require manual operator ZIP handoffs.
