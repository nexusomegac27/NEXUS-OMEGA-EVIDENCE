# NEXUS OMEGA | R15 Final Scientific Adjudication and R16 Interface

**Object:** `NEXUS_OMEGA_AXIOM_R15_FINAL_SCIENTIFIC_ADJUDICATION_20261018_R0`  
**Date:** 2026-10-18 | **Authorial role:** AXIOM, source audit and scientific adjudication  
**Scope:** R15 GPS/FOV 3D GIS research, including R0, R1, R2 and externally reported crossvalidation  
**Authority:** Human operator; GitHub repository rules govern placement and publication  
**Claim ceiling:** `C1_DESCRIPTIVE_ONLY` | `GIS_RAIL != SOFTTWIN_GRAPH` | `FRAME != MEASUREMENT`

**Scientific verdict:** `PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_SCOPE_CLOSABLE`.

The R15 *research foundation* can be closed in C1 as a reproducible design-and-isolated-test record. This is **not** a finding that GPS/FOV 3D maps are integrated, offline-certified, empirically more efficient, safe on actual devices, independently scientifically accepted, or approved for release. Finality applies to the specified research corpus and its residual-risk register. Unfinished experimental gates are carried explicitly to R16 and/or independent specialist lanes. The pre-existing R14/R15 Node PR #90 is a different subject and remains undisturbed.

---

## 1. What was physically inspected

### 1.1 Operator-provided parent archive

The newly supplied file `/mnt/data/NEXUS-~1.zip` was opened and independently SHA-256 hashed; no extraction outside a controlled working directory and no arbitrary execution of archive scripts was performed. Each nested ZIP was separately integrity checked and its manifest rehashed against actual child bytes.

| Object / source layer | Actual bytes | SHA-256 | Independent finding |
|---|---:|---|---|
| R15 crossvalidation & R16-preparation outer archive | 173053 | `9e215a6eb990fb61e8524a2f5b2d85405b55a1a9889368b34b06526052691574` | 14 ZIP entries, no CRC fault |
| R15-R0 open-source 3D mapping foundation | 6917 | `0b32132b6a529edc441a3f929401fcfb77bcf54b37978f17dcb2dc8ebaefa58b` | Real separate R0 original |
| R15-R1 GPS/FOV parent ZIP | 110827 | `a725dbc35fcc6d8a5524460bd6217e3355a7517cf269a00a2f71160553eb7229` | 12 entries, 11/11 manifest children MATCH |
| `FOUNDATION_R15_R1.md` **inside R1 ZIP** | 25683 | `2a1e05cf4d633df6a8729eb1dc793239900ad60c6d2e6c1f74c00367f158cad5` | Real separate R1 original |
| R15-R2 adversarial research & expert order ZIP | 28881 | `72a429fd2a61b3c1b388720a6e68846c41b2d0ef6eb3c8a22cf6ca2bda8a7858` | 10 entries, 9/9 manifest children MATCH |
| GROK verification handshake | 4090 | `e3ffc151848de09a4c88301e4b82aac97ac7dd3eec4710ccb55801d3ba1cdccf` | Original bytes available; agent-reported scientific claims not promoted |
| MANUS/VIBE adjudication note | 20366 | `c43604617082829faa0edde9320b3cacdbad9bb950303b9629fab951bb313c8d` | Original bytes available; report-level external assertions |
| GROK symbiotic causal-canonical artifact | 17820 | `28b24395f46de94e0d4817e9f2a67f292d5e07df10fe49dc04398b8cfe52d88f` | Original bytes available; not independent authority |

**K4 identification adjudication:** The earlier apparent 6917 B/25683 B “foundation conflict” is definitively **a different-object distinction in the inspected materials**: R0 (module survey) versus R1 (GPS/FOV detailed foundation). No source overwrite, mis-hash or semantic synonymity is warranted. The distinction is documented append-only. Publishing an identity ledger does not imply that any third party has independently adjudicated the scientific content.

### 1.2 Public GitHub source check

Canonical public repository: [nexusomegac27/NEXUS-OMEGA-EVIDENCE](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE). The readback of `main` at the audit was `d355400dabed3c280e1fce5030cab69ea099428b`; the R15 publication remained [Draft PR #119](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/119), head `b644227067cee2f1de782f5430bd2cb7bc07dae9`, OPEN, NOT MERGED. The pinned R15-R2 report and expert order are present on that commit as the Git blobs below.

| GitHub object | Independent Git blob SHA-1 | Independent local original SHA-256 |
|---|---|---|
| `NEXUS_OMEGA_AXIOM_R15_ADVERSARIAL_GPS_FOV_DEEP_RESEARCH_20261018_R2.md`, 17770 B | `d3c198fe0724dfd8f2e354d912a338571b225e72` | `91485b957b802d37d345c7c78d9abf983e6382f276e2a927b59f0015166bb33f` |
| `NEXUS_OMEGA_AXIOM_R15_GPS_FOV_3D_GIS_EXPERT_MAXIMAL_ORDER_20261018_R0.md`, 19751 B | `789c4bacf82520cd2156fddb5eeccc2f8562441a` | `a5ba0516deda50b8c599a9033c769e0da43c59703dd5a25d59a7d1b537bb17b0` |

The research lane is on the PR branch, and machine structure registry v1.7.16 exists there, not on main. Other prior PRs #90 and #116 are open. PR #119 is a publication/preparation event, not authorization for experts, node execution, merge, or Hostinger. Owner-authored issue #93 receipts must not be mistaken for independent expert acknowledgements. The external-agent allowlist at the pinned main is empty.

### 1.3 Replay, test independence and limits

| Audit | Candidate | Deliberate defective control | Independence class |
|---|---:|---:|---|
| R15-R1 producer's frozen synthetic evaluator | **29/29 PASS** | **28/29**, expected direction-heading failure | Original test design, independently re-executed by AXIOM |
| R15-R2 producer's frozen synthetic ledger evaluator | **22/22 PASS** | **20/22**, expected `wrong_dataset` and `wrong_view` failure | Original test design, independently re-executed by AXIOM |
| Additional AXIOM retrospective 2D point oracle | **64/64 scenarios** with **190254 sampled witnesses**, 0 observed misses | No independent mutation for this new oracle | New independent implementation, but not a pre-registered external acceptance |

The supplementary reference implementation samples points inside a synthetic 2D circular field-of-view sector, with position and heading uncertainty offsets, independently of the R1 code's triangle-vs-axis-aligned-bounding-box predicate. **No observed missed sample is not a mathematical proof** of continuous spatial coverage. No tested sample came from live GPS, a 3D engine, a browser, or user location.

The distinction `REEXECUTED_ORIGINAL_TESTS != INDEPENDENT_DESIGN_OF_TEST_ORACLE != EXTERNAL_SCIENTIFIC_ACCEPTANCE` is mandatory. The new additional check is retrospective and explicitly exploratory.

---

## 2. Primary-source scientific findings

### 2.1 GPS heading, camera orientation and pose validity

The W3C Candidate Recommendation **dated 26 March 2026** is a now-grounded, immutable reference: https://www.w3.org/TR/2026/CR-geolocation-20260326/. The `heading` coordinate denotes **motion direction relative to true north**; it may be null at rest. The API does not provide a certified camera optical axis. Its `accuracy` and `altitudeAccuracy` represent uncertainty of the reported location, not a bound on all future device motion, camera rotation or map registration errors. The API is source-agnostic: an implementation may derive a position from networks and user input, not just GNSS.

**R15 invariant:** Camera pose is a separately authorized, timestamped, provenance-bound object containing orientation source and uncertainty. If orientation is absent, wrong-source, stale, or incompatible with the GNSS/CRS record, fine-grained directional selection must fail closed or degrade conservatively. Do not infer north-referenced yaw from a device-course field while stationary. Real position is a private data class, not a prerequisite for the research prototype.

For a later controlled real pilot, include clock synchronization and device-coordinate frame definitions (true north vs magnetic, screen rotation, orientation reference); preserve spatial reference, units, height datum and license. The currently verified R15-R1 prototype only handles **invented 2D ENU coordinates** and must not be fed real WGS84 coordinates.

### 2.2 View-dependent geometry: what the research actually implies

The OGC **3D Tiles 1.1** standard (22-025r4) defines bounding volumes, hierarchical levels of detail, tile metadata and geometric error. Screen-space error (SSE) is used to decide whether coarser geometry is adequate for the current camera. This does not guarantee that a client will request *only* currently visible leaf tiles: parents, sibling support tiles, textures, glyphs, styles, implicit subtree files and other ancillary resources may also be fetched. [OGC 3D Tiles 1.1](https://docs.ogc.org/cs/22-025r4/22-025r4.html).

The foundational view-dependent LOD literature (H. Hoppe, SIGGRAPH 1997, DOI 10.1145/258734.258843) uses view frustum, surface orientation and screen-space error to refine/coarsen meshes. This supports the design approach, **not a measured NEXUS bandwidth reduction**. Later mobile 3D engine selection requires a complete geometric/occlusion oracle, not only a synthetic flat-sector test.

**Failure modes to preregister:** close-range tile corners, camera pitch and roll, optical FOV vs display aspect ratio, horizon/altitude, parent REPLACE vs ADD refinement, screen-space-error inflation, geodetic curvature, antimeridian, high-latitude projection and uncertain heading. Always require a complete, independently generated visibility oracle for the declared finite benchmark.

### 2.3 Tile storage, range requests and real bytes

PMTiles V3 describes a single-file archive with a 127-byte header and directory hierarchy; the root directory is constrained to the first 16 KiB. Its readers use HTTP range requests where supported, but **range support is not an egress-minimality guarantee**. Clients and servers may batch, over-fetch, cache or ignore ranges; a server replying `200` to an intended `206` partial fetch may transfer the full object. PMTiles also can be served locally, which is preferable for the research pilot when proper permissions and source licenses exist. [PMTiles V3 spec](https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md); [PMTiles guide](https://docs.protomaps.com/pmtiles/).

Separate **selected tiles**, **requested assets**, **fulfilled response bytes**, **compressed bytes**, **browser transfer accounting**, **server egress**, **resident CPU/GPU memory** and **displayed pixels**. No single one measures the others. For an offline test, all runtime inputs must be local or specifically allowed; tiles alone do not establish offline behavior.

### 2.4 Browser telemetry can be incomplete

W3C Resource Timing defines `transferSize`, `encodedBodySize` and `decodedBodySize`, but cross-origin data can be opaque or zeroed; service-worker responses may describe only the client-worker interaction. Chromium's DevTools Protocol supplies request/response/cache metadata and `Network.loadingFinished.encodedDataLength` for observable network requests. **Neither is a universal device-level byte/energy oracle**. [Resource Timing](https://www.w3.org/TR/resource-timing/); [Chromium Network protocol](https://chromedevtools.github.io/devtools-protocol/tot/Network/).

For valid empirical conclusions, collect independent server-side or OS-level transfer counters when available and document differences and unobservable paths. A request must retain origin class, redirect history, HTTP status (`200`, `206`, `304`), range/Content-Range, cache source (network, memory, disk, service worker), completion/cancellation, asset class and per-resource byte fields. Distinguish incomplete traces and omitted worker streams. Preserve privacy by using scrubbed synthetic trace IDs and by excluding actual fine-grained GPS from public receipts.

### 2.5 3DTilesRendererJS cache incident: historically grounded, not universal

[Issue #1689](https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/1689) documents a **user-reported** `3d-tiles-renderer 0.5.1` cache starvation/refetch issue under specified load; the report describes 13848 requests for 5684 models (around 2.4 times) and a stuck refinement state with a capped cache. The issue is now **closed** (2026-09-14), assigned to milestone v0.5.3. [Release v0.5.3](https://github.com/NASA-AMMOS/3DTilesRendererJS/releases/tag/v0.5.3), published 2026-09-18, lists additional `stats.refused` instrumentation and cache fixes. An issue's closure and release association do **not** by themselves prove that the reported scenario is eliminated on every configuration.

**Scientific consequence:** Retain a version-tagged starvation/churn regression and a separate post-fix retest, while explicitly refusing to label the current upstream as proven vulnerable based on a 0.5.1 issue. Cache caps and pruning policies must be measured together with total requests, discarded decoded tiles, memory and visual convergence.

### 2.6 Open-source module and rights boundary

| Module | Audited source class | R15 use | Mandatory limitation |
|---|---|---|---|
| MapLibre GL JS @ `fc1aa1cd7539ab50e4451d7175e30fa95f41ddf3` | Root `LICENSE.txt` is a BSD-style three-condition license; GitHub API reports NOASSERTION | Primary optional 2.5D cartographic viewer | Localize styles, scripts, worker, sprites, glyphs; strict CSP and request logging; not a 3D globe science oracle |
| Protomaps PMTiles @ `aec8fa1341222fdddb3318e9ffa8e18e19b312f7` | LICENSE says reference implementations BSD-3; PMTiles spec CC0/public domain where applicable; sample tiles may have separate licenses | Local read-only archive | Byte-range overfetch, HTTP status and rights to the **data** must be verified separately |
| NASA-AMMOS 3DTilesRendererJS @ `3febfcff2869771a9152084b80312ae5e244133e` | Apache-2.0 | Optional actual 3D Tiles HLOD path | SSE/parents/cache/version-tag, error budget, 0.5.1 issue replay; never presume only visible tiles fetched |
| CesiumJS | Apache-2.0 | Independent comparison only | Larger functional scope; external ion not mandatory; source rights and offline closure still needed |
| iTowns | Dual MIT / CeCILL-B noted in upstream LICENSE.md | Alternative for heterogeneous GIS datasets | License compatibility and dependency runtime need exact integration review |
| deck.gl | MIT | Optional separate analytic overlay | Should not become a source of epistemic state or visual status proof |

The OSM database license (ODbL) and attribution duties attach to incorporated OSM data regardless of renderer code license. This study did not ingest real OSM data or external 3D models. No third-party library or payload was vendored. A checkout pin, license file and software SBOM/lockfile are prerequisites to actual code use; nested dependencies need separate review.

### 2.7 Interpretation firewall: the map is not an instrument for AXIOM claims

The GIS rail stores source-exact geodata, CRS, datum, time range, copyright/license, confidence or accuracy definition, and provenance state. The Softtwin rail carries a versioned abstract graph and its claim state. A `GIS→Softtwin` bridge must be typed, read-only and demonstrably non-authoritative. DEM altitude **in metres** cannot be converted to Softtwin `elevation_tier`, scientific confidence, cognition rank or consciousness metrics. A click, hover, scene LOD or camera path cannot modify the canonical graph or issue an agent command.

Provenance states must remain separately readable (e.g. `SOURCE_NOT_PRESENT`, `REPORTED`, `VERIFIED_BYTES`, `TESTED_SYNTHETIC`, `HOLD_SCOPED`) and visible in text export. Use a neutral legend that does not suggest `VERIFIED_BYTES` means scientific truth. Accessibility demands non-color-only status indications and an audit-friendly ledger alongside any visually compelling display.

---

## 3. Final adversarial falsification matrix

| ID | Falsifiable hypothesis / attack | Independent evidence required | R15 final status |
|---|---|---|---|
| F01 | Same tile count implies the same transmission cost | Full request ledger with received encoded lengths, redirects, cache and response categories | **REJECTED** in synthetic countercase; no empirical value established |
| F02 | Only in-frustum tiles ever incur I/O | Instrument ancestor/sibling/texture/worker/glyph/subtree fetches before and after selection | **OPEN_EMPIRICAL** |
| F03 | A heading fix proves camera direction | Attested heading source, frame, uncertainty, clock age; negative stationary case | **REJECTED** by W3C semantics and R15-R1 tests |
| F04 | Tested sampled coverage proves a continuous-volume guarantee | Independent geometric proof, boundary fixtures and 3D frustum oracle | **OPEN_MATHEMATICAL / 3D** |
| F05 | Smaller cache implies less network/energy | Post-fix versioned starvation trace, dropped tiles and retransfers | **OPEN_EMPIRICAL** |
| F06 | The app is offline because tiles are local | Cold profile, network isolation, complete JS/worker/style/font inventory, full-request capture | **OPEN_BROWSER** |
| F07 | Browser `transferSize` equals cellular/device bytes | Independent OS/server counters, Timing-Allow-Origin & ServiceWorker handling | **REJECTED_AS_UNCONDITIONAL** |
| F08 | Renderer source license grants rights to the map data | Per-dataset license, attribution and redistribution ledger | **OPEN_LICENSE_PER_DATASET** |
| F09 | Source SHA means scientifically valid camera pose | Independently generated reference, accuracy model and reproducibility | **REJECTED** |
| F10 | PR success or owner ACK equals scientific confirmation | Independent reviewer, source-exact third-party return and adjudication | **REJECTED** |
| F11 | Synthetic 2D ENU behavior transfers automatically to WGS84/3D | Antimeridian, high-latitude, height datum and camera pitch/roll tests | **OPEN_CROSS_GEODETIC** |
| F12 | R16 can inherit R15 as an execution permission | Explicit new task anchor, actor rights and real API checks | **PROHIBITED_INHERITANCE** |

### Falsifier definition for R16 experimental design

For identical immutable data source, viewport sequence, quality budget, device state, timing, and cache regime, let:

- `B_baseline` be independently observed complete received transfer bytes of the circle selection or full-frustum default;
- `B_candidate` be independently observed complete received transfer bytes under conservative pre-I/O visibility selection;
- `S = 1 - B_candidate / B_baseline` for `B_baseline > 0`.

An **unqualified** claim of increased efficiency is falsified by `S <= 0`, missing traffic or non-comparable quality. For any statistical claim, preregister the exact estimand (e.g. median paired transfer difference), uncertainty estimator, number of scenes/runs and a quality non-inferiority tolerance **before** looking at real results. Do not adopt the synthetic 68.18% tile-ID reduction as a prior empirical saving or a scientific effect size.

Minimum measured dimensions per run: selected candidates, actual asset requests and HTTP status, encoded received bytes (plus method and counter source), decoded bytes, duplicate/retried bytes, peak CPU/GPU memory, tile-cache refusals, visual convergence time, task correctness/visible coverage, approximate battery energy **only with a calibrated measurement source**. Browser API counters alone cannot establish battery joules.

Before claiming `OFFLINE_VERIFIED` require cold-cache browser execution on a permitted local/sandbox origin, forced network denial, complete request log including worker/service-worker fetches, zero unexpected remote requests, and explicit evidence about the scope of device/OS background networking. The criterion concerns the *application under observation*, not all background networking on the device.

---

## 4. R15 final verdict: what closes and what does not

| Scope | Verdict | Justification |
|---|---|---|
| R15 R0/R1/R2 research corpus and parent chain | **CLOSED_C1_SOURCE_EXACT_LOCAL** | All provided original bytes checked; parent identities disambiguated; independent R1/R2 replay passes |
| R15 pure synthetic 2D scheduler / byte-ledger design | **CLOSED_C1_TESTED_ISOLATED** | 29/29 and 22/22 rerun, mutations fail appropriately; 64-case supplementary probe has no observed witness miss |
| R15 open-source architectural shortlist | **CLOSED_C1_RESEARCH_REFERENCE** | Versioned primary source, license and failure modes audited; optional engines not adopted |
| Manus/GROK private scientific authority or independent external acceptance | **NOT_ESTABLISHED** | Agent text/bytes verified, but origin/method/independent scientific acceptance not authenticated by those hashes |
| R15 R2 expert research dispatch or independent expert ACK | **NOT_EXECUTED / SOURCE_NOT_PRESENT** | External actor registry empty, orders prepared only |
| GitHub main publication / release | **NOT_MERGED** | PR #119 remains draft/open; source and registry live only on branch |
| Live GPS, true 3D/frustum renderer, cold-cache offline, device power/network improvements | **NOT_ESTABLISHED** | No physical run, external traffic oracle, browser trace, or cross-device replay |

**Closing rule:** This resolves the R15 research *definition and evidence accounting* without silently promoting unresolved deployment/validation gaps into PASS. No further repetitive R15 research round is necessary solely to restate the existing limits. Empirical closure is a separate R16 experimental gate, not a condition for preserving R15 C1 research results.

---

## 5. R16 entry — precise non-execution handoff

R16 may inherit the **versioned R15 research references and falsifiers**, never permission to execute. The newly uploaded R15 handoff contains a GROK reference to an `R16_ATTENTION_FRAGMENTATION...` sibling, but **the sibling's original bytes were not present in this attachment**. Do not treat that mention as original-byte intake or presume R16's contents.

1. **R16-E0 / source & ethics:** Owner authorization, precise source roots and licensing, data locality, source SHA-256, machine registry position, synthetic coordinates by default. Explicit map/data rights and privacy/retention contract.
2. **R16-E1 / pre-I/O geometric oracle:** Independently implement camera pose + frustum/LOD coverage, prove or bound 2D/3D selection with worst cases. Reference results locked before optimizations. Verify no false negatives on the declared finite benchmark.
3. **R16-E2 / local mini-map runtime:** Read-only, no new daemon, local/loopback mini-dataset with licensed tiles; detect network requests through browser CDP plus origin/proxy counters. Negative fixtures for `200` on a range request, missing worker/sprite, external glyph, redirect and ServiceWorker replay.
4. **R16-E3 / paired performance study:** Cold/warm separate, randomized paired view sequences, equal accuracy/LOD/quality and documented device conditions; time/bandwidth/energy and error bars. Publish only reversible C1 descriptions once validated under owner rules.
5. **R16-E4 / optional actual 3D & human factors:** Compare 3DTilesRendererJS/Cesium only if E1–E3 justify cost; evaluate map comprehension against a plain evidence ledger, accessibility and absence of mistaken truth/rank inferences.

**No R16 automatic launch or operator rights change.** Cursor remains PRAXIS only when separately authorized. External QWEN/GROK/MISTRAL/GEMINI reports remain research hypotheses unless an authentically independent, source-exact return exists. R9 science, R11 PR #116, R14/R15 node PR #90, R12, R13 and the previous R14/R15 GIS boundaries are untouched.

---

## 6. Reproducibility and exact source citations

### Public GitHub and standards

1. R15-R2 owner research: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/b644227067cee2f1de782f5430bd2cb7bc07dae9/research/r15/soft-geography-gps-fov-20261018/NEXUS_OMEGA_AXIOM_R15_ADVERSARIAL_GPS_FOV_DEEP_RESEARCH_20261018_R2.md
2. R15-R2 prepared expert MAXI order: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/b644227067cee2f1de782f5430bd2cb7bc07dae9/research/r15/soft-geography-gps-fov-20261018/NEXUS_OMEGA_AXIOM_R15_GPS_FOV_3D_GIS_EXPERT_MAXIMAL_ORDER_20261018_R0.md
3. R15 research Draft PR: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/119
4. W3C Geolocation Candidate Recommendation, exact snapshot 2026-03-26: https://www.w3.org/TR/2026/CR-geolocation-20260326/
5. OGC 3D Tiles 1.1, OGC 22-025r4: https://docs.ogc.org/cs/22-025r4/22-025r4.html
6. PMTiles V3 technical specification: https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md
7. PMTiles concepts and local serving: https://docs.protomaps.com/pmtiles/
8. W3C Resource Timing: https://www.w3.org/TR/resource-timing/
9. Chrome DevTools Protocol, Network domain: https://chromedevtools.github.io/devtools-protocol/tot/Network/
10. 3DTilesRendererJS issue 1689 (user-reported version 0.5.1): https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/1689
11. 3DTilesRendererJS v0.5.3 release: https://github.com/NASA-AMMOS/3DTilesRendererJS/releases/tag/v0.5.3
12. Hugues Hoppe, *View-dependent refinement of progressive meshes*, SIGGRAPH 1997: https://doi.org/10.1145/258734.258843
13. MapLibre GL JS licence pinned at `fc1aa1cd7539ab50e4451d7175e30fa95f41ddf3`: https://github.com/maplibre/maplibre-gl-js/blob/fc1aa1cd7539ab50e4451d7175e30fa95f41ddf3/LICENSE.txt
14. PMTiles LICENSE pinned at `aec8fa1341222fdddb3318e9ffa8e18e19b312f7`: https://github.com/protomaps/PMTiles/blob/aec8fa1341222fdddb3318e9ffa8e18e19b312f7/LICENSE
15. 3DTilesRendererJS LICENSE pinned at `3febfcff2869771a9152084b80312ae5e244133e`: https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/3febfcff2869771a9152084b80312ae5e244133e/LICENSE
16. OSM data license & attribution: https://www.openstreetmap.org/copyright

### Local independently checked, not automatically public on GitHub

- `NEXUS-~1.zip`: exact nested R15-R0/R1/R2 originals + MANUS/GROK operator-mediated reports.
- R15-R1 `frozen_evaluator.py` / `gps_fov_tile_preflight.py` / `mutant_unchecked_camera_heading.py`.
- R15-R2 `frozen_byte_ledger_evaluator.py` / `synthetic_byte_ledger_guard.py` / `mutant_missing_pairwise_context_guard.py`.
- AXIOM retrospective `r15_supplementary_2d_coverage_probe.py` and its JSON outcome.

All local proof should be published as *new* versioned files, never overwrite original documents, and only if source disclosure and owner repository policy allow it. A GitHub commit or PR is a transport event, not scientific truth.

---

## Canonical closure object

```text
OBJECT = NEXUS_OMEGA_AXIOM_R15_FINAL_SCIENTIFIC_ADJUDICATION_20261018_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_SCOPE_CLOSABLE

R15_RESEARCH_FOUNDATION = C1_COMPLETED
R15_PARENT_SOURCE_IDENTITY = R0_6917_AND_R1_25683_DISTINCT_VERIFIED
R15_R1_ZIP = 110827_SHA256_MATCH_MANIFEST_11_OF_11
R15_R2_ZIP = 28881_SHA256_MATCH_MANIFEST_9_OF_9
R15_R1_REPLAY = 29_OF_29_PASS
R15_R1_MUTANT = 28_OF_29_EXPECTED_FAIL
R15_R2_REPLAY = 22_OF_22_PASS
R15_R2_MUTANT = 20_OF_22_EXPECTED_FAIL
R15_RETROSPECTIVE_2D_WITNESS = 64_OF_64_190254_SAMPLES_ZERO_OBSERVED_MISSES

SCIENTIFIC_EXTERNAL_ACCEPTANCE = NOT_ESTABLISHED
REAL_GPS = NOT_USED
REAL_NETWORK_SAVINGS = NOT_ESTABLISHED
REAL_DEVICE_ENERGY = NOT_MEASURED
3D_FRUSTUM_ORACLE = NOT_EXECUTED
COLD_BROWSER_OFFLINE = NOT_EXECUTED
R15_MAIN_MERGE = NOT_ESTABLISHED
EXPERT_DISPATCH = NOT_EXECUTED
R16_ORIGINAL_FOUNDATION_BYTES = NOT_RECEIVED_IN_THIS_ARCHIVE

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
CURSOR_RUNTIME = UNCHANGED
HOSTINGER = NO
R9_R11_R12_R13_R14 = PRESERVED
```

**Source > narrative; coverage sample != proof; successful upload != acceptance; research closure != production release.**
