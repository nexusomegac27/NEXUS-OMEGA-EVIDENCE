# AXIOM — GROK R21R1 / R19 / R10R22 Postmodule Independent Adjudication · 2026-10-10 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_ADJUDICATION_OF_GROK_R21R1_R19_R10R22_POSTMODULE_RETURN_AND_SGP4_BRIDGE_20261010_R0
PARENT_EXTERNAL_RETURN = NEXUS_OMEGA_GROK_R21R1_R19_R10R22_POSTMODULE_ADVERSARIAL_VALIDATION_RETURN_20261010_R0
PARENT_GROK_ORDER = PR61_MERGED_7e1b1484ee5456ba95fc623eaaa0c650978bd8fd
PARENT_MISTRAL = PR60_MERGED_2e4169cc6393db766a0107464c32bc65ab72e4aa
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_EXTERNAL_RETURN_ACCEPTED
SGP4_OLD_PRODUCER_TO_PUBLIC_SCHEMA = FAIL_REPRODUCED_SOURCE_SHAPE
SGP4_NEW_SOURCE_EXACT_ADAPTER = IMPLEMENTED_AND_SYNTHETICALLY_TESTED
WWW_VISUAL_TILES = NOT_INDEPENDENTLY_VERIFIED
HOSTINGER_WRITE = CURSOR_ONLY_NOT_OBSERVED_HERE
R19_STAGE_A = NON_INTERFERENCE
R21R1_CURSOR_WWW_CLOSEOUT = EXISTING_WORKER_NON_INTERFERENCE
R21_FULL_NAVIGATION = OPEN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## I. Exact GROK return intake

Two operator-attached documents were opened from physical local original bytes and independently SHA-256-hashed:

| Original file | Size | SHA-256 | Meaning |
|---|---:|---|---|
| `NEXUS_~1(9).MD` | 10115 bytes | `c18be6803771173dee47adef9bc73662b7cba987eb15ea6948b387fd4fd46e84` | GROK full adversarial report; reported source facts must be separately graded |
| `NEXUS_~3(3).TXT` | 2515 bytes | `e8ac0cd5942a63e72564f1620b0b7e3ec35c10eae9467bad97854b8198f56e0e` | GROK short handoff, not an independent second validation |

Supporting earlier operator originals (already rehashed for PR61 source receipt):
- SGP4 reference ZIP `89ce11741a79ad28973185072b58746b35a40264064b21d5ca6bdc7a895a0514`; full ZIP content SHA 7/7; 7 isolated SGP4 tests are **source-reported**, not rerun in this adjudication against freshly installed satellite.js.
- R19 Ledger ZIP `0086701b2b9392dfd2d0c0f7dc7959edb6cac358b5bb2e4af390bc7541f0e6b1`; SHA 9/9.
- Symbiose-Lab extension ZIP with expected SHA `32c9fb52d9b81a2007f499d28a48e830b333ccd53ba939512b7184bee7062b45` is still not part of current original intake; the old 25/25 self-test remains SOURCE_REPORTED_ONLY.

Only this public-safe report, code, test cases and SHA metadata are published in GitHub. Neither sensitive source ZIP payloads nor private Hostinger credentials are committed.

## II. Independent assessment of GROK

GROK's **FAIL** is legitimate for the old standalone SGP4 source. Original `src/orbis-sgp4-position.mjs` in the operator's SGP4 ZIP was inspected by AXIOM: `buildOrbitPredictedBlock` returns `height_km`, `epoch_utc`, `source_url` and `eci_km` while canonical `schema/r19/orbis-satellites-manifest.schema.json` requires `alt_km`, `element_epoch_utc`, `calculated_utc` and strict additionalProperties:false. The original `loadOmm` also silently selects array index zero, and serializes object inputs before hashing them. These are material **integration and original-byte provenance** hazards, not evidence of SGP4 numerical model falsity.

Public `https://www.nexus-mobile.de/orbis/astra-nav/` currently returns crawlable ASTRA-NAV P0 page text (independently observed), and `/orbis/satellites/satellites.json` contains zero admitted slots and `nexus_link_verified:false`. GROK additionally reports independent HTTP byte matches for all four P0 source files using the pinned fileset manifest; this remains GROK's SOURCE_REPORTED_BYTE_MATCH until actual original HTTP bytes are independently rehashed by AXIOM. No browser WebGL rendered-tile, zoom/pan, mobile, keyboard or full independent three-proof closeout is established from the textual fetch alone.

GROK did not execute all 24 originally demanded adversarial fixtures or independently reproduce 25 Symbiose-Lab tests. **C1 scoped acceptance of the report does not mean FULL_MAXI_EXECUTED_ALL_TESTS**, GNSS ready, offline navigation, lawful photographic imagery or validated direct NEXUS satellite communication.

R10R22 attached manuscript is a proposal. It confers no new AXIOM/OMEGA deployment rights, does not supersede the live R19/R21 scopes and provides no mathematical proof of claimed astronomical/network breakthroughs.

## III. AXIOM immediate bridge remediation: actual working source, no site side effects

The following new additive artifacts implement the narrow GROK critical finding:

- `examples/r19/orbis-sgp4-public-contract-bridge.mjs` (Node.js server build-step, **not** frontend or private ledger mutator).
- `tests/r19/orbis-sgp4-public-contract-bridge.test.mjs` with **16 independently locally executed tests** (Node v22.16.0: 16 PASS, 0 FAIL before GitHub CI); baseline old SGP4 dependency not installed/re-executed.
- `.github/workflows/validate-r19-orbis.yml` updated so GitHub checks the new module and all 16 tests.

Deterministic contract of the bridge:
1. Require original raw OMM JSON `Buffer/Uint8Array`, compute SHA-256 directly from the bytes, never from reserialized object.
2. Require exactly one OMM record (single object or array length one) and an independently supplied exact expected NORAD CATNR string 1–9 digits; fail on ambiguous multi-element array or producer/OMM identity disagreement.
3. Verify producer success, C1 ceiling, `nexus_link_verified=false`, the raw response digest and original UTC element epoch; no auto admission.
4. Map `height_km→alt_km` and `epoch_utc→element_epoch_utc`; inject explicit `calculated_utc` from the actual invoking build time, distinct from `target_utc`.
5. Return **only** schema-permitted position keys; require finite geodetic values, exact pinned SGP4 model version and a configurable target/epoch offset upper bound (default 48 hours, a conservative **engineering release policy**, not a physics accuracy proof).
6. Fail-closed `{ok:false,position:null,reason}` on a bad fixture and leave the public satellite snapshot unchanged until a genuinely admitted and independently sourced satellite exists.
7. `model_version` becomes explicit so the numerical propagator reference can later be independently pinned and challenged. **This is an adapter and proof boundary, not an end-to-end satellite.js validation.**

The test scenarios cover positive exact-byte mapping; missing original bytes; multi-OMM ambiguity; NORAD mismatch; producer identity mismatch; raw digest mismatch; reserialized mismatched digest; naive UTC; calculation time; over-stale target; invalid geo; model version pin; NEXUS link integrity; 6-digit CATNR; no source and no position. Test fixture positions are synthetic **never publish as real orbit markers**.

## IV. Immediate publication and continuing owner

**GITHUB_RELEASE:** Publish the validated C1 code reference and scientific adjudication via scoped PR; this is public-safe and reversible. It requires no further operator approval.

**HOSTINGER_SITE:** Cursor has explicitly reported the **existing R21R1 Worker** executing `ASTRA-NAV → Hostinger → browser readback`; do not start a duplicate worker or overwrite the live `/orbis/` or `/orbis/satellites/` resources from this R19 source-only patch. No production execution by AXIOM. Existing Node birth count unchanged.

**INTERFACE NEXT:** Cursor (or the already authorized R19 science/build owner) may integrate the additive adapter only after its current Stage A closeout, matching live/host source revisions, exact source/original bytes, package pinned version and validator across both source-level and actual schema. Do not substitute source zip for a working actual site pipeline.

**PROOF REMAINS OPEN:** The legitimate website terminal still requires (A) production exact fileset, (B) authenticated Hostinger write, (C) independent public HTTP and true visual browser execution. No `WWW_LIVE_VERIFIED` from GitHub merge alone.

## V. Terminal object

```text
GROK_RETURN = PASS_WITH_MATERIAL_CAVEATS_C1
GROK_MD_BYTES_SHA256 = c18be6803771173dee47adef9bc73662b7cba987eb15ea6948b387fd4fd46e84
GROK_TXT_BYTES_SHA256 = e8ac0cd5942a63e72564f1620b0b7e3ec35c10eae9467bad97854b8198f56e0e
SGP4_PRODUCER_ORIGINAL = SOURCE_SHAPE_CONFIRMED_FAIL_BRIDGE
SGP4_BRIDGE_REFERENCE = C1_CODE_TESTED_16_OF_16_LOCALLY_PASS
SGP4_NUMERICAL_SCIENCE = NOT_INDEPENDENTLY_REPRODUCED_HERE
SGP4_PUBLIC_LIVE_MARKERS = ZERO_ADMISSIONS
ASTRA_NAV_PUBLIC_TEXT = RETRIEVABLE
ASTRA_NAV_PUBLIC_ASSET_BYTES = GROK_SOURCE_REPORTED_MATCH
ASTRA_NAV_VISUAL_BROWSER = NOT_YET_VERIFIED
R21R1_HOSTINGER_WWW_TERMINAL = PENDING_CURSOR_RECEIPT
GNSS_NATIVE_OFFLINE_PHOTO_TERMINAL = OPEN
R10R22_PROPOSAL = SOURCE_REVIEW_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

The citable next step is genuine browser/Cursor receipt evidence, not another general authorization loop. No claim promotion; no new Node births.
