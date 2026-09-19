# NEXUS OMEGA R8.0 — Custody / R8.1 Protocol Cross-Validation

```text
OBJECT = NEXUS_OMEGA_AXIOM_R8_0_R8_1_CUSTODY_AND_PROTOCOL_CROSSVALIDATION_20260919_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_CUSTODY_VALIDATED_PROTOCOL_HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
```

This lane is a public-safe, append-only validation derivative of the supplied
`nexus-omega-r8-0-custody-bind-r7-1-2-→-r8-transition-R1.zip` package.
The raw package is **not** published here because it contains chat/history and local-path material.
Only independently verified scientific/provenance findings are exposed.

## Terminal scientific state

- R7.1.2 corrected C1 derivative remains the immutable public predecessor.
- R7.2 correctly terminates at `HOLD_C1_PHYSICAL_RASTER_EVIDENCE_ABSENT`.
- No B04/B08/SCL raster bytes, source-exact STAC item, product metadata, or processing-baseline evidence are present in the supplied R8 package.
- Therefore pixel-level radiometry, valid-pixel fraction, NDVI, NDVI uncertainty, independent raster replication, and REANA execution remain **not established**.
- The R8.1 multi-run material is a research-design candidate only. It is not executable/validated as supplied.

## Physical custody facts

Outer source package:

- bytes: `131090`
- SHA-256: `dc4b6a9664ae6bd2ceb8af5cd908d799d7a649d5d2a9876c28c10116ce8267b4`
- ZIP entries: `10`
- ZIP CRC: `PASS`
- path traversal: `NONE_FOUND`

Nested R8.1 package:

- bytes: `10078`
- SHA-256: `1614a7be408b4fdeb744f35a14375dd00a7e285d7710985d8c6608e5f762a135`
- ZIP entries: `8`
- ZIP CRC: `PASS`

The physically supplied R7.2 Cursor order file hashes to:

`01ade359c7a962ab91526cb5369527d71611ffc85b570e84dc29012ce5e95b8d`

This is distinct from the inherited R7 parent-order hash `d053289e...`; both refer to different objects and must not be conflated.

## Material validation findings

1. The custody document refers to a `02_SHA256SUMS.txt` validation, but no such file is present in either the outer package or nested R8.1 ZIP. R8.0 is therefore **not a sealed checksum-manifest package as supplied**.
2. The nested `17_REANA_R8_1.yaml` fails YAML parsing and is not executable as supplied.
3. The REANA specification references `ndvi_mapper_r7_1_2_radiometric.py` and `sample_stac_item_enhanced.json`; neither file is present in the nested ZIP.
4. Container digest pins and both implementation method hashes are placeholders.
5. The workflow contains hard-coded `valid_fraction=0.87`, NDVI summaries and uncertainty values despite the absence of raster inputs. Those values are examples only and must never be ingested as measurements.
6. The nested uncertainty model does not numerically follow its own propagation equation: for Red=0.08, NIR=0.25 and sigma=0.02 per band, first-order propagation yields approximately `0.09641436`, not `0.025`; for the stated 0.15% relative example it yields approximately `0.00077918`, not `0.005`.
7. The `CE90 ±8 m` value is not accepted as a generic current Sentinel-2 L2A Collection-1 product characteristic.
8. The proposed universal SCL valid set `[4,5,6,7,11]` is not accepted as a general scientific NDVI validity mask. Mask semantics must be preregistered for the research question.
9. The deep-research source-discovery lane correctly identifies public discovery/access routes, but its statement that CDSE raster download requires no registration is too broad: CDSE metadata discovery can be public, while official product download/API processing routes require authentication. AWS Sentinel-2 COG public S3 access supports anonymous `--no-sign-request` access.

## Publication rule

```text
CUSTODY_HASH_FACTS = PUBLICATION_ELIGIBLE_C1
R7_2_HOLD_STATE = PUBLICATION_ELIGIBLE_C1
PROVENANCE_DISTINCTION = PUBLICATION_ELIGIBLE_C1
OPEN_DATA_SOURCE_DISCOVERY = PUBLICATION_ELIGIBLE_WITH_CORRECTIONS_C1
R8_1_MULTI_RUN_PROTOCOL = HOLD_METHOD_REMEDIATION_REQUIRED
PIXEL_RESULT = NO
NDVI_RESULT = NO
UNCERTAINTY_RESULT = NO
REANA_EXECUTION = NO
```

A future R8.1 successor must begin with physical source acquisition and a new closed checksum manifest; it must not promote the supplied draft workflow.
