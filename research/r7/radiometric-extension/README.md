# NEXUS OMEGA R7.1.2 — Radiometric Extension Cross-Validation

```text
OBJECT = NEXUS_OMEGA_AXIOM_R7_1_2_RADIOMETRIC_FULL_CROSSVALIDATION_20260919_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
SOURCE_PACKAGE_PUBLICATION = BLOCKED_AS_VALIDATED_SOURCE
PUBLIC_SAFE_CORRECTED_DERIVATIVE = ACCEPTED_WITH_CAVEATS_C1
```

This public research lane preserves the supplied R7.1.2 package as a hash-bound source state and publishes an append-only corrected derivative. It does not rewrite the source package and does not claim empirical Sentinel-2 processing, production readiness, agent stabilization, or truth authority.

## Source package

- Outer ZIP SHA-256: `1a758589480533fc703281c2c03f04ff74bf5723153f4e0178ad88132a6231b9`
- Outer ZIP bytes: `743085`
- R7.1.2 core ZIP SHA-256: `270ad395c6d4676358f78cd0846cb14769142028c67f8024c39961a8ae388ef9`
- R7 parent order SHA-256 physically present in the package: `d053289ee688ef14363df80f5d862d19d5a760e83d23009ef22cb0347a179d1e`

## Accepted findings

- ZIP CRC/integrity checks pass and no path traversal was found.
- The R7.1.2 inner manifest verifies all four bound core files.
- The Lübeck EPSG:4326 → EPSG:25832 coordinate correction reproduces independently: approximately `611054.534, 5970313.421` for `10.6890, 53.8694`.
- The Sentinel-2 L2A BOA relation using `BOA_ADD_OFFSET` and `QUANTIFICATION_VALUE` is supported by ESA documentation; for the supplied fixture values it is equivalent to `DN * 0.0001 - 0.1` for non-NODATA DN.
- Claim ceiling `C1_DESCRIPTIVE_ONLY` and `TRUTH_AUTHORITY=NONE` are preserved.

## Material source-package defects

Direct publication of the supplied package as a fully validated scientific implementation is blocked because:

1. The final receipt binds `Order SHA256 = 2e8f...`, while the physically supplied R7 order hashes to `d053...`.
2. The deep-research report simplifies the radiometric relation as `DN * 0.001 - 0.1`; the correct equivalent for `QUANTIFICATION_VALUE=10000` is `DN * 0.0001 - 0.1`.
3. No B04/B08/SCL raster bytes are present. The mapper does not perform raster normalization or NDVI computation; it creates a metadata/provenance object from a JSON fixture.
4. `valid_pixel_fraction = 0.87` is hard-coded as an example, not measured from an SCL raster.
5. The generated AIU contains NDVI uncertainty values `0.00008` and `0.09641`, inconsistent with the receipt/report claims `±0.005` and `±0.025`.
6. The sample declares six STAC extension URIs; `quality` is not declared as a seventh extension. The mapper synthesizes a local `quality` object.
7. The source mapper reads `properties.raster:bands` and consequently assigns reflectance scale/offset to the SCL classification band; the corrected derivative reads scale/offset from raster assets and does not transform SCL classification values.
8. The sample `proj:transform` mixes projected EPSG:32632 metadata with degree-like origin values and is not accepted in the corrected fixture.
9. The REANA workflow was not executed in the supplied evidence. Image references are tag-pinned rather than digest-pinned, and the “second-run” step only echoes SNAP/FORCE intent; no SNAP graph/output is supplied.
10. The package uses `CE90 ±8m` as a generic current geometry statement. The corrected derivative uses the current Sentinel-2 Collection-1 L2A published characteristic `<12 m at 95.5% confidence` and does not promote the 8 m statement.

## Corrected derivative

`corrected/reference_mapper_r7_1_2_c1.py` is deliberately narrower. It is a deterministic metadata reference mapper, not a pixel processor. Pixel-derived outputs remain `NOT_COMPUTED`/`NOT_ESTABLISHED` until actual raster bytes and a declared uncertainty model are supplied.

Run:

```bash
python corrected/reference_mapper_r7_1_2_c1.py corrected/sample_fixture_r7_1_2.json corrected/reference_result_r7_1_2.json
python -m unittest tests.test_reference_mapper_r7_1_2 -v
```

## Scientific boundary

```text
HASH_MATCH != CLAIM_TRUTH
METADATA_PIPELINE != RASTER_PROCESSING
FIXTURE != OBSERVATION
EXAMPLE_VALUE != MEASURED_VALUE
WORKFLOW_SPEC != WORKFLOW_EXECUTION
CROSSVALIDATION != PRODUCTION_VALIDATION
```
