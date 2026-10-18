# NEXUS OMEGA — R15/R2 · Adversarial GIS 3D, GPS/FOV and byte-true measurement research

```text
OBJECT = NEXUS_OMEGA_AXIOM_R15_ADVERSARIAL_GPS_FOV_DEEP_RESEARCH_20261018_R2
CLASS = CONTRADICTION_APPEND + EXTERNAL_DEEP_RESEARCH + ISOLATED_QUALITY_SCAFFOLD
STATE = PASS_WITH_CAVEATS_C1_RESEARCH_LEVEL
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = OPERATOR_GOVERNED
PARENT_OBJECT = NEXUS_OMEGA_AXIOM_R15_GPS_FOV_3D_GIS_DEEP_RESEARCH_FOUNDATION_20261018_R1
PARENT_ZIP_BYTES = 110827
PARENT_ZIP_SHA256 = a725dbc35fcc6d8a5524460bd6217e3355a7517cf269a00a2f71160553eb7229
PUBLIC_MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
EXISTING_R14_R15_NODE_PR90 = OPEN_UNMERGED_PRESERVE
EXISTING_R11_PR116 = OPEN_UNMERGED_PRESERVE
NO_RUNTIME_CHANGE = TRUE
NO_REAL_GPS = TRUE
NO_EXTERNAL_WRITER_REGISTRATION = TRUE
C2_AUTHORITATIVE = REJECTED
```

## 1. Research purpose and provenance

This is the second R15 research iteration, preceding an expert MAXI order. It does **not** create a new runtime agent, start GNSS capture, dispatch Cursor, install 3D engines, push to Hostinger, or claim actual bandwidth savings. It preserves R13→R14→R15 and the separate existing R14/R15 node implementation lane.

The *physically accessible* parent R15 ZIP was independently opened: **110,827 bytes**, **12 archive members**, ZIP CRC integrity valid and SHA-256 `a725dbc35fcc6d8a5524460bd6217e3355a7517cf269a00a2f71160553eb7229`. Its internal `FOUNDATION_R15_R1.md` is **25,683 bytes**, SHA-256 `2a1e05cf4d633df6a8729eb1dc793239900ad60c6d2e6c1f74c00367f158cad5`; a standalone matching copy exists. Cursor's separate return states `FOUNDATION_MD=6917 / 0b3213…`. **These are not equal byte identities.** Until the source path for the 6,917-byte object is resolved, preserve `SOURCE_IDENTITY_GAP_SCOPED`; do not reinterpret its hash as matching the 25,683-byte R15 foundation. This does not invalidate the parent archive hash.

The parent P0 is a synthetic, local-ENU two-dimensional conservative wedge raster selector, not GPS, 3D camera occlusion, device telemetry or a web viewer. Its prior results are **29/29 candidate; 28/29 negative mutant; 88 circular vs 28 FOV tile IDs** on one fixed 16×16 grid. An independently replayed Browser/GPU/RAM/network/real-GPS result does not exist. A smaller tile-ID count is neither a count of HTTP requests nor necessarily a saving in transferred bytes.

The public repository `nexusomegac27/NEXUS-OMEGA-EVIDENCE` main remained `d355400dabed3c280e1fce5030cab69ea099428b` at this research fetch. Read-only inspection of `AGENTS.md`, `GOVERNANCE.md`, `docs/governance/REPOSITORY_ORDER_POLICY.md`, `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` and the Steward confirmed the external actor allowlist is empty. `research/r15` was **not** in main's research directory listing; a new phase directory therefore requires owner governance and structure registry/README review, not stealth creation by an external actor. PR #90 already uses R14/R15 in the **node** domain; this research has the distinct name `R15_SOFT_GEOGRAPHY_GIS`. PR #116 (R11) remains separate and unmerged.

## 2. Target architecture and staged choice

**Rail A (default, 2.5D):** MapLibre GL JS with locally packaged styles, CSS, Worker, fonts/glyphs/sprites and data. PMTiles V3 single-file archive, with explicit local-only `addProtocol()` handler or verified file-backed reader. MapLibre's vendor examples include HTTP demo styles/CDN modules: none are permitted as silent runtime dependencies in the offline path. PMTiles uses header, root/leaf directories and byte offsets. Offsets, ranges, cache behavior and actual downloaded bytes must be observed, not inferred from selected tile IDs.

**Rail B (optional true 3D):** NASA-AMMOS/3DTilesRendererJS + 3D Tiles 1.1, using one small local tileset with known rights, bounded SSE/error, `maxDepth`, byte cache and download-queue limits. `loadAncestors` and `loadSiblings` can enlarge the loaded set. A local strict pre-I/O gate must account for the renderer's **actual** requests; naively disabling siblings can create visible gaps, and a bounded cache may force coarser geometry. Include a visual-coverage and geometry-quality gate, not just a memory gate.

**Comparison only:** CesiumJS for geodetic globe/curvature/horizon situations. iTowns/Giro3D when heterogeneous real GIS/point-cloud data demonstrate a scientific advantage; deck.gl for optional read-only annotations. No simultaneous mandatory installation of several engines. GDAL/PROJ/PDAL/Planetiler are lawful offline ETL/build tools, not default Android services. COPC 1.0 provides octree/range-aware point-cloud storage, but it is not a rendering or positional-trust policy.

### Scientific source anchors (read-only, pinned code heads observed 2026-10-18)

| Subject | Pinned commit or standard | Source | Evidence / open limit |
|---|---|---|---|
| MapLibre GL JS | `fc1aa1cd7539ab50e4451d7175e30fa95f41ddf3` | https://github.com/maplibre/maplibre-gl-js | API supports local Worker bundling; runtime version and third-party asset audit required |
| PMTiles | `aec8fa1341222fdddb3318e9ffa8e18e19b312f7` | https://github.com/protomaps/PMTiles | v3 header/directories/range structure; reader performance not measured |
| NASA 3D Tiles renderer | `3febfcff2869771a9152084b80312ae5e244133e` | https://github.com/NASA-AMMOS/3DTilesRendererJS | default sibling/ancestor loading, cache caps documented; no NEXUS benchmark |
| CesiumJS | `85500087b890479ffa3bf0b4cf0db55887c2d89a` | https://github.com/CesiumGS/cesium | alternative 3D globe; higher/lower cost unmeasured |
| iTowns | `1f2371ce506ffac9c5f11d0c3f45ceb5d822373d` | https://github.com/iTowns/itowns | research alternative; licences/data sources must be independently examined |
| deck.gl | `051896dcb7477eee169e211aedea28aa9ce964e4` | https://github.com/visgl/deck.gl | optional analytical overlays, no I/O guarantee |
| OGC 3D Tiles 1.1 | `22-025r4` | https://docs.ogc.org/cs/22-025r4/22-025r4.html | HLOD/implicit quadtree and octree; neither online policy nor numerical accuracy certified |
| W3C Geolocation | W3C specification | https://www.w3.org/TR/geolocation/ | movement heading may be `null` when stationary; not camera orientation |
| COPC 1.0 | format specification | https://copc.io/ | partial reading of clustered LAZ point clouds; no rendering contract |
| MapLibre custom protocol | official API | https://maplibre.org/maplibre-gl-js/docs/API/functions/addProtocol/ | resource substitution possible; negative tests mandatory |
| OSM public tile usage | OSMF policy | https://operations.osmfoundation.org/policies/tiles/ | prohibits offline bulk-preload from its public raster tile host; vector-policy separately scoped |

**Upstream licensing caveat:** Repository API license codes can be `NOASSERTION`; a permissive label is not proof of compatibility across transitive packages, icons, datasets, fonts, DEM, styles or 3D models. Review exact files/versions, attribution and distribution obligations before vendoring. Code copyright and geodata rights are separate.

## 3. New independent falsification findings

**F1 — Count ≠ bytes.** The parent's 88→28 comparison is a cardinality result on an identical synthetic tile-ID representation, not an HTTP ledger. At different LOD, compression, request metadata or prefetch settings, fewer tile IDs may produce more response-body bytes. A fair experiment must pin the same scene, rights-cleared original dataset, cache state, rendering-error target, LOD quality, position/orientation and coverage oracle. The new isolated `synthetic_byte_ledger_guard.py` makes mismatched experimental context a `HOLD_SCOPED`, and refuses to label its synthetic responses as real network traffic.

**F2 — Orientation insufficiency.** Real GNSS supplies position, optional speed and course-over-ground, **not a stationary phone camera's azimuth and pitch**. IMU/magnetometer based yaw has calibration error and magnetic-vs-true-north issues. Mark source, calibration epoch, timestamp and uncertainty; camera FOV optimization cannot depend solely on `coords.heading`. Missing heading → deliberate manual overview, enlarged uncertain coverage or HOLD, never fabricate azimuth.

**F3 — 2D-versus-3D visibility.** A sampled 2D fan cannot establish 3D frustum intersection for buildings, terrain, pitch, horizon or vertical datum. The independent expert lane must specify conservative 3D bounding-volume intersection, near/far clipping, partial occlusion uncertainty, screen-space error and swept camera motion without false negatives. Occlusion-based deletion requires an independent geometric oracle.

**F4 — Offline ≠ no external HTTP in a warm browser.** Test cold cache, cleared service workers/storage, disabled DNS/network, explicit local worker URL, all styles/fonts/sprites/tilesets/tiles, and fallback behavior. A failed network request still counts as an attempted prohibited request. Record blocked/aborted/retried/range reads, background preload, CORS, redirect, 206-vs-200 and full-object fallback. `LOCAL_BLOB` or `PMTILES` label without an observed resource ledger does not establish no remote calls.

**F5 — GPS and tile request privacy.** A geolocation-based subset of a tile matrix may reveal location through tile IDs, IP or cache logs if a remote endpoint participates. Never publish raw GPS fixes, device IDs, geofenced user history or pseudonymous tile trails in public receipts; synthetic or responsibly quantized summaries only after independent privacy review.

**F6 — Energy / workload not monotonically proportional to tiles.** Frustum updates can increase CPU, GPU and battery due to sensor wakeups, cache thrashing, texture upload and rapid camera motion. Comparative device measurements require matched visual quality, warm/cold scenarios, explicit battery/thermal confounders, and independent replay. No inferred real-world 68.18% saving.

**F7 — PMTiles range-file and 3D Tiles ancestor costs.** PMTiles V3's header is 127 bytes; the root directory must reside in the first 16,384 bytes. A local reader still incurs directory lookup, decompression and tile decoding. 3D Tiles may require nonvisible ancestors/siblings; `requested_bytes`, `received_body_bytes`, `decoded_bytes`, `RAM`, and `GPU resident bytes` must have separate accounting. A 200 response to a Range request may unexpectedly return the whole archive: test and log this as a potential budget breach.

**F8 — 3D/GIS measurements vs symbolic graph.** A real DEM's metres and vertical datum are distinct from symbolic `elevation_tier`; projection joins are typed, read-only, and source-bound. A map click never mutates original node state, writes a scientific claim or executes physical sensors. Any `E0∧E3∧E4⇒C2_AUTHORITATIVE` rule is prohibited, as explicitly rejected in the R14-R1 PDF-page-9 adjudication.

**F9 — Early cost of sensor accuracy.** A radius derived from confidence interval may explode tile coverage in urban canyons. A cap may silently drop geometrically necessary tiles if implemented by truncation. Cap overflow must fail closed or intentionally lower resolution with declared coverage/quality degradation, not fabricate completeness. Test antimeridian/poles/geodetic unit conversions before any real GIS pose adapter.

**F10 — Historical-bound provenance ambiguity.** Cursor's R15 `FOUNDATION_MD` return claims 6,917 bytes; the actual R15 ZIP/standalone R15 R1 foundation is 25,683 bytes. Keep both identities separate pending a pinpointed independent source path; do not overwrite archives or silently substitute a digest.

## 4. R15-R2 new isolated executable scaffold — *synthetic body-byte claim guard*

Frozen-before-implementation evaluator: `frozen_byte_ledger_evaluator.py` SHA-256 **`bb193dc5921edc58a0cce2bc02a983d4f26d7fb69d93a8c5fbd38628b1199f24`**.
Candidate: `synthetic_byte_ledger_guard.py` SHA-256 **`ea713838011ce85dfc2840ad9d5c855823d48cfe82e67a345ed3ff762951f6d7`**.

- Baseline: previous R15 P0 has **tile-cardinality-only** output, `measured_network_bytes=null` and no pairwise response-body ledger; therefore baseline byte-comparison defensibility: **0 executable comparison gates**, not a numeric failure rate.
- New isolated result: **22/22 frozen independent synthetic evaluator**. It requires paired synthetic runs with same dataset SHA-256, view SHA-256, LOD, cold-cache state and declared coverage oracle. Rejects privacy input, origin changes, duplicate/remote requests, missing traces, invalid bytes and claim promotion.
- Synthetic paired example: 88 × 100 = **8,800 invented response-body bytes**, 28 × 100 = **2,800**, 68.18% decrease **only under these invented equal-size conditions**. Opposing fixture: 28 × 400 = **11,200**, i.e. a 27.27% **increase** despite fewer tiles. This second fixture is a constructive counterexample to `tile_count_reduction⇒byte_reduction` when LOD/data sizes differ; in the executable comparator the same declared LOD permits different synthetic sizes, and this is a synthetic modelling example, **not observed NEXUS traffic**.
- Mutant without cross-run dataset/view identity comparison: **20/22 PASS**, expected failure on 2 negative fixtures. This tests the evaluator's ability to detect context mixing; it is not an independent human scientific review.
- All output identifies `real_network_bytes_verified=false`, `real_savings_claim=false` and only `SYNTHETIC_ACCOUNTED_C1`. No requests leave the process; no GNSS accessed, no real location accepted.

**Inescapable caveat:** `capture_complete=true`, `coverage_passed=true`, and SHA strings are input assertions, not independently authenticated receipts. Even 22/22 cannot validate real capture completeness, source authority or browser behavior. The expert MAXI must develop an independent browser-network oracle and signed/not-self-approved source provenance before any public measured savings claim.

## 5. New hypothesis register for expert falsification

| ID | Falsifiable hypothesis / target | Minimal independent negative control |
|---|---|---|
| H01 | FOV tile selection covers all view-visible features within declared uncertainty | camera at grid edge, sub-tile slivers, angle 359°→0°, large location uncertainty |
| H02 | GPS pose cannot override independently sourced view heading | stationary course null; phone rotated while GPS course unchanged |
| H03 | Pre-I/O budget truly covers every initiated external/local read | ancestor/sibling prefetch, 206 range fallback 200 full download, retries/redirects |
| H04 | COLD_OFFLINE runtime emits **zero attempted remote requests** | empty cache, disabled network and DNS, CSS/fonts/worker/sprites, service-worker reset |
| H05 | Joint constraints reduce **measured** body bytes without degrading geometry coverage | equal-view/LOD data, permutation of tile sizes, cold/warm swap |
| H06 | Cross-runtime tile sets are byte-for-byte identical for typed input | Python vs independent JS; signed-zero, NaN, antimeridian and projection edge cases |
| H07 | Positional privacy is not exposed through tile requests or public receipts | external-host URL / local logs containing raw lat/lon or tile trail |
| H08 | Real GIS and abstract Softtwin graph do not mix trust/units | `elevation_tier` presented as metres, missing vertical datum, C2 auto-rule |
| H09 | Resource use on dual Android devices stays within predeclared budgets | rapid rotation, battery saver, thermally throttled CPU/GPU; no claims absent authorization |
| H10 | Open-source supply chain is reproducible and deployable offline | tampered asset SHA, missing license, remote font fallback, worker loaded from CDN |

## 6. Execution and authority gating

**G0 E0/E1** Rehash R13/R14/R15 original package and current GitHub source snapshots; classify licensed upstream assets; preserve R15 Foundation identity discrepancy as scoped. **G1** formal pose/fov/CRS model with independent spatial coverage oracle. **G2** cold offline mini-map browser with synthetic or licensed small city tile set, trace all attempted outbound traffic including hidden resources. **G3** independent JS/Python golden replay and mutation tests. **G4** optional NASA vs Cesium 3D comparison only under matched inputs and fidelity. **G5** privacy, CPU/GPU/RAM/energy validation only on authorized devices. **G6** human usability/provenance comprehension study. **G7** publication via existing owner GitHub branch/PR/CI, independent main readback and separate public WWW receipt if truly deployed.

No new always-on agent, Windows service, worker, external write slot, Hostinger runtime, sensor capture, camera access, phone reboot, protected-path move, auto-merge, license adoption, unverifiable source repair or C2 promotion. `DRIFT_RESET=NON_DESTRUCTIVE`, `BLOCKED_LANE != BLOCKED_SYSTEM`, `R9_SCIENCE=PRESERVED`, `R14_NODE_PR90=PRESERVED`, `R11_PR116=PRESERVED`.

## 7. Acceptance rubric and decision

A stage passes only if: (1) original bytes and hashes; (2) source/license/privacy clearance; (3) independent falsification fixture; (4) separate evaluator with a frozen evaluation definition; (5) actual test log and denominator; (6) negative results preserved; (7) exact commit+main readback when published. `REPORT_LEVEL_RESEARCH` != `VALIDATED_DEVICE_OPTIMIZATION` != `SCIENTIFIC_TRUTH`.

**Decision:** `PASS_WITH_CAVEATS_C1_R15_R2_RESEARCH_COMPLETE + TESTED_ISOLATED_SYNTHETIC_QUALITY_GUARD`. Authorizes **only preparation/publication of public-safe research and read-only expert orders**, within repository rights. Actual external actor returns and real GIS/device behavior are not established. The accompanying maximal order is **prepared, not autonomously dispatched**; the empty GitHub external actor allowlist prohibits self-registration or direct external writes.
