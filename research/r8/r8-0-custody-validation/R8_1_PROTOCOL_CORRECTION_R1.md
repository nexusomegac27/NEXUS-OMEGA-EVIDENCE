# R8.1 Protocol Correction R1 — Gate before computation

This correction supersedes the supplied R8.1 draft **for execution eligibility only**. The source draft remains preserved as historical research material.

## Gate 0 — physical evidence first

No radiometric/NDVI workflow may start until all of the following are physically present and SHA-256 bound:

```text
B04 raster bytes
B08 raster bytes
SCL raster bytes
source-exact STAC item or equivalent product catalogue object
product/tile metadata
processing baseline metadata
closed SHA256SUMS manifest
```

If any mandatory object is absent:

`HOLD_C1_PHYSICAL_RASTER_EVIDENCE_ABSENT`

## Gate 1 — source acquisition

Validated source options include:

- Copernicus Data Space Ecosystem for authoritative Sentinel-2 catalogue/product access. Metadata/STAC discovery may be public; product download/processing routes that require authentication must be represented as such.
- AWS Registry of Open Data Sentinel-2 L2A COGs / Earth Search for an independently hosted access path. Anonymous S3 access is explicitly documented by AWS for the public dataset.

No source is promoted by brand. Exact scene/product identity and byte hashes control the experiment.

## Gate 2 — radiometric relation

For Sentinel-2 L2A PB >= 04.00, recover BOA reflectance from product metadata using:

```text
BOA_i = (DN_i + BOA_ADD_OFFSET_i) / QUANTIFICATION_VALUE_i
```

Do not hard-code offset or quantification values if the physical product metadata are available. DN=0 remains NO_DATA for the documented PB>=04.00 encoding.

## Gate 3 — mask semantics

There is no universal `[4,5,6,7,11] = valid NDVI` law.

The experiment must define and preregister the analysis population. SCL categories such as water, snow/ice and unclassified pixels must be explicitly included, excluded or analyzed separately according to the scientific question. The chosen policy must be applied identically by independent implementations.

## Gate 4 — uncertainty

Do not publish fixed `±0.005` or `±0.025` NDVI uncertainty tiers from the supplied draft.

The current Sentinel-2 performance documentation gives product-level radiometric/surface-reflectance performance requirements and measured performance, not a universal per-pixel independent Gaussian sigma for B04/B08 suitable for direct NDVI propagation.

For NDVI:

```text
NDVI = (NIR - RED) / (NIR + RED)

dNDVI/dNIR = 2 RED / (NIR + RED)^2
dNDVI/dRED = -2 NIR / (NIR + RED)^2
```

If band variance/covariance inputs are not physically supported for the selected product and uncertainty model:

`NDVI_UNCERTAINTY = NOT_ESTABLISHED`

## Gate 5 — executable workflow

The supplied `17_REANA_R8_1.yaml` is not execution eligible because it fails YAML parsing, references missing inputs, contains placeholder container digests/method hashes, and hard-codes example output values.

A successor workflow must:

1. parse under the declared REANA/YAML schema;
2. pin executable images by real digest where supported;
3. include or fetch only authorized, hash-bound inputs;
4. compute every statistic from raster bytes;
5. produce run receipts/logs/output hashes;
6. execute twice from fresh workspaces before any reproducibility claim.

## Gate 6 — independence

Separate toolchains are a useful toolchain-diversity control but are not automatically source-independent evidence. Report source independence, implementation independence and execution-environment independence as separate dimensions.

## Publication eligibility

Only the following are publishable from the current package:

```text
physical custody hashes
R7.2 HOLD state
provenance distinctions / corrections
source-discovery findings after correction
methodological defects and falsifiers
```

The following remain blocked:

```text
pixel-level radiometry
valid-pixel fraction
NDVI statistics
NDVI uncertainty
REANA execution
C3/C4 empirical replication atoms
```
