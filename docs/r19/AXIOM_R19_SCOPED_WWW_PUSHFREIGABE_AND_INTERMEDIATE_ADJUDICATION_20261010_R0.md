# NEXUS OMEGA — AXIOM R19 ORBIS C1 Scoped WWW Push Adjudication · 2026-10-10 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_R19_ORBIS_INTERMEDIATE_ADJUDICATION_AND_SCOPED_WWW_PUSH_RELEASE_20261010_R0
AUTHORITY = OPERATOR_OMEGA_C1_WWW_PUSH_AUTHORITY_V1 → AXIOM_SOFT_GOVERNANCE
DATE = 2026-10-10
STATE = PASS_WITH_MATERIAL_INTEGRATION_CAVEATS_C1_SCOPED_WWW_RELEASE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PARENT_R19_PR54 = MERGED_a6ae27953bdf7904e68de7fefd3769445079db58
PARENT_CUSTODY = NEXUS_OMEGA_OMEGA_HOSTINGER_PRIMARY_ARTIFACT_TRANSPORT_AND_CUSTODY_V1
R20 = CLOSED_BY_OPERATOR_WITH_CAVEATS_NON_INTERFERENCE
R21_PRIVATE_HOSTINGER_ARCHIVE = EXISTING_WORKER_ONLY_PENDING_TERMINAL_PROOF
ELITE_NODE_FOUNDATION = SEPARATE_LANE_NO_NEW_BIRTHS
PUBLICATION_RULE = C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE_ROLLOUT_REQUIRED
PRODUCTION_WWW_DEPLOY_BY_AXIOM = NOT_EXECUTED
```

## I. Exact input custody and independent checks

The operator provided four physical original uploads for this check. Their **locally independently calculated** full-file SHA-256 values are:

| Ingress original file | Bytes | SHA-256 | Interpretation |
|---|---:|---|---|
| `NEXUS_~1(20261010-020316).TXT` | 22512 | `4c8cc947de5dfdeff1c05583df0713c4826b657a73527a843a07d9e1c2e65503` | Combined prior R19 discussion and external research/handshakes; reported claims, not standalone execution evidence |
| `NEXUS_~1(5).ZIP` | 24426 | `0086701b2b9392dfd2d0c0f7dc7959edb6cac358b5bb2e4af390bc7541f0e6b1` | R19 enclosed Slot Ledger/reference-stack archival copy |
| `NEXUS_~2(2).ZIP` | 8152 | `89ce11741a79ad28973185072b58746b35a40264064b21d5ca6bdc7a895a0514` | New SGP4 reference build module with synthetic test input |
| `PROTOK~1.MD` | 5935 | `98a714d4705b7f8de32b44bfa80bce864d20f0f814619ad55faf91de591eeced` | Symbiose-Lab source-reported results; 25/25 tests NOT independently reproduced here |

Both ZIPs: `testzip()=NONE`, all 9 and 7 respectively hashed entries `MATCH`, declared `PACKAGE_ROOT_SHA256` equals SHA-256 of included `NEXUS_HASH_MANIFEST.txt`. All counted entries are source exact for those archives. This **does not** verify an unprovided Symbiose-Lab module ZIP `32c9fb52…`, a GROK full return, licenses, external-source meaning or scientific truth.

Baseline 14/14 test fixtures from R19 ZIP independently run on Node.js v22.16.0: `PASS=14 FAIL=0`. The SGP4 package's source/fixtures and 7 tests exist; dependency-installed SGP4 runtime was **not independently reproduced** in this adjudication. Upstream fetches and origin browser simulation are not validated.

## II. Actual public website state (independent text retrieval; not pixel test)

- `https://www.nexus-mobile.de/orbis/` is publicly accessible but continues showing explicitly **illustrative** Doctrine NF-D1–NF-D5 markers, NOT validated dynamic orbit positions.
- `https://www.nexus-mobile.de/orbis/satellites/` is publicly accessible as C1 source-labelled TLE information. The page itself states `ORBIS_LIVE_SATELLITE_VIEW=NOT_VISIBLE`, `COMPUTED_ORBITAL_POSITION=HOLD_NOT_SHIPPED_P0`, `NEXUS_LINK_VERIFIED=0`.
- **New:** `https://www.nexus-mobile.de/orbis/satellites/satellites.json` is now publicly retrievable. Its root `schema_version=nexus-orbis-satellites/1`, `generated_utc=2026-10-10T01:21:19Z`, `slot_ledger_revision=r19-empty-admitted-20261010-r0`, `satellites=[]` means no admitted live satellite. It is a useful truthful empty snapshot, NOT the completed live-marker loop.
- Live text fetched by external public web accessor; no independently acquired exact HTTP original bytes, origin asset checksums, full browser JS execution or desktop/mobile screenshots by AXIOM. Retain terminal requirements for Cursor.

## III. Two real material interface defects verified independent of vendor claims

**D01 PUBLIC_MANIFEST_SCHEMA_CONFLICT**. Actual production manifest has `nexus_link_verified:0` (number), but GitHub `schema/r19/orbis-satellites-manifest.schema.json` requires JSON boolean `false`. Its `additionalProperties:false` disallows production fields `claim_promotion`, `scientific_walls`, and `empty_surface_copy`. Normalizing production manifest to the existing versioned contract is preferred; if fields are truly required, propose a new **versioned schema**, tests and backwards-compat notes. Never silently relax a security invariant or pretend currently published JSON already validates.

**D02_SGP4_POSITION_CONTRACT_MISMATCH**. Incoming new `src/orbis-sgp4-position.mjs` returns `height_km`, `epoch_utc`, `source_url`, `eci_km`; R19 position schema requires `alt_km`, `element_epoch_utc`, `calculated_utc`, plus exact elements-source hash and strictly defined fields. Standalone schema-check of the producer's shape yields four unexpected properties and three missing required fields. Producer currently supplies an OMM timestamp without guaranteed terminal Z; time normalization needs an explicit UTC provenance rule. Add a **source-bound adapter**, pinned dependency/lockfile, coordinate and epoch checks, and two-way test: produced object must pass both the canonical JSON Schema validator and the browser adapter. Synthetic ISS test coordinates are never permission to publish live ISS marker.

**D03_SOURCE_RETURN_CAVEATS**. Symbiose-Lab report says 25/25 PASS and 6 of 9 upstream source groups returned material. Its underlying extension ZIP, original upstream raw responses, Ajv execution, and exact rights ledger are not included in current operator upload; treat status as `SOURCE_REPORTED_NOT_INDEPENDENTLY_BYTE_VERIFIED`. Within the ten rows of its table, 7 endpoint rows show SOURCE_OK and 3 HOLD; its “6 of 9” counts **grouped sources**, not one-to-one HTTP endpoints, so preserve per-endpoint and per-provider breakdown. Only declared C1 source-class separation receives preliminary acceptance.

## IV. Scoped C1 publication authority

**RELEASE_GRANTED_ALREADY:** public-safe **text/documentation**, route navigation, accessible satellite directory empty state, properly normalized `satellites.json`, provenance caveat badges, reversible frontend wiring in *the actual* site repository after exact source/host path identity and a backup/rollback are confirmed. Validate schema and visibly preserve old `/orbis/` Doctrine fixtures as illustrations. No renewed general C1 approval loop. Any purely presentational correction that passes scope/source/security gates should be published promptly.

**RELEASE_AUTOMATIC_AFTER_NARROW_REPAIR:** SGP4 computed positions and clickable real spacecraft markers *only per admitted satellite* after D02 resolved and passed real-source exact-byte identity, OMM epoch, correct NORAD association, bounded propagation/freshness policy, actual verified `ORBIT_PREDICTED` timestamp, JSON Schema validation, rights and policy verification and independent post-publication browser readback. This standing rule is the advance permission: **do not return to Operator for another abstract C1 approval** when measurable requirements have been met.

**NOT RELEASED:** unverified GOES-16 XRS static primary mapping; catalog group membership inferred as physical ACTIVE status; auto-admission from mere HTTP 200; AO-73 fake Berlin coordinates; direct `NEXUS_LINK_VERIFIED`; synthetic ISS fixture posing as externally sourced orbit data; cross-satellite NOAA observations; unreviewed source licenses; ESA token-protected data; mass upstream scraping; live RF/direct smartphone-to-satellite claims; high-impact host write beyond existing Cursor scope. `HOLD` remains **per component/slot**, not a global ORBIS or C1 system hold.

## V. Cursor/PRAXIS — existing worker / no duplicate

This document is the **authorization and reconciliation object for the already existing scoped R19 WWW deployment lane**, not the startup of a second worker. Reconcile under R21 WWW Three Proofs / ongoing Hostinger archive without interrupting them. ELITE node taxonomy runs independently and no new BORN nodes are inferred.

Required Cursor terminal receipts in priority:

1. `PUBLIC_CURRENT_FILESET`: real site source + exact production file set + byte-level hashes and allowed host account/path scope, provenance, predeploy backup/rollback.
2. `SCHEMA_REMEDIATION`: live manifest boolean/canonical allowed field fix plus exact validated bytes and immutable archive receipt; independent AJV or equivalent Draft 2020-12 full schema check.
3. `POSITION_ADAPTER_REMEDIATION`: normalized SGP4 output schema and integration tests with real upstream identity, tested source/target timestamps, bounded freshness and stale fallback; if not possible promptly publish approved empty/public C1 surface without fictional markers.
4. `WWW_PUSH`: correct scoped Hostinger upload only by authorized Cursor identity; no speculative writes by AXIOM.
5. `POST_DEPLOY_WITNESS`: independent live endpoint fetch, actual DOM/marker click `/orbis/` → detail by ID, mobile & desktop screenshots, unknown-ID graceful response, no token leaks, readable metadata and SHA across origin build/public bytes.
6. `HOSTINGER_PRIVATE_ARCHIVE`: *existing* R21 closeout must separately produce authenticated archive-ingress and SHA-256 independent readback; no assumption the public `satellites.json` is a private archive.
7. `RECEIPT_PUBLICATION`: public-safe final report to canonical GitHub `docs/r19`, `validation/r19` only as needed, with exact lineage and no private paths/credentials.

If exact host write scope is missing, `WWW_WRITE=HOLD_SCOPE_ONLY`; independently safe C1 publication keeps progressing through source/governance lane. Hostinger data plane remains private and no physical user-download relay is required.

## VI. Determination

```text
R19_INPUT_ZIPS = BYTE_VERIFIED
ZIP_CRC_AND_CONTENT_MANIFEST = PASS
R19_BASE_TESTS = PASS_14_OF_14_INDEPENDENT
R19_SGP4_TESTS = SOURCE_REPORTED_7_OF_7_NOT_REPRODUCED
SYMBIOSE_LAB_TESTS = SOURCE_REPORTED_25_OF_25_NOT_REPRODUCED
PUBLIC_MANIFEST = PRESENT_EMPTY_0_SATELLITES
D01_LIVE_MANIFEST_SCHEMA = FAIL_MATERIAL_LOCALIZED
D02_SGP4_TO_POSITION_SCHEMA = FAIL_MATERIAL_LOCALIZED
C1_PUBLIC_SAFE_REVERSIBLE_UI_AND_DOCS = PUSH_GRANTED
C1_COMPUTED_POSITION = CONDITIONAL_AUTOMATIC_RELEASE_AFTER_D02_AND_SOURCE_WITNESS
HOSTINGER_PUBLIC_DEPLOY_BY_AXIOM = NOT_EXECUTED
CURSOR_LIVE_SITE_INTEGRATION = PENDING_RECEIPTS
NEXUS_LINK_VERIFIED = 0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
