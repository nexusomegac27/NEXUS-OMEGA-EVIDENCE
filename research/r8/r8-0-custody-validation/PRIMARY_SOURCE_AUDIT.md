# R8 primary-source audit — public-safe correction

Primary/authoritative sources checked on 2026-09-19.

## Sentinel-2 L2A encoding

ESA/Copernicus L2A Data Quality documentation for Processing Baseline 04.00 states that the BOA reflectance is recovered as:

`L2A_BOA_i = (L2A_DN_i + BOA_ADD_OFFSET_i) / QUANTIFICATION_VALUE_i`

with `DN=0` reserved for NO_DATA and `BOA_ADD_OFFSET=-1000` DN for the documented PB 04.00 change.

## Radiometric / surface-reflectance uncertainty

Current Sentinel-2 mission/performance material describes Level-1 absolute radiometric uncertainty at the percent level and the Level-2A surface-reflectance uncertainty goal as `U(rho) <= 0.05*rho_ref + 0.005`. The supplied R8 draft's `0.15% relative` assumption and fixed NDVI tiers `±0.005 / ±0.025` are therefore not accepted as universal Sentinel-2 L2A uncertainty inputs.

## Current product family

Sentinel-2 Collection-1 Level-2A is the current L2A product family starting from Processing Baseline 05.xx. Any experiment must record the exact processing baseline of its physical scene rather than assuming `05.11`.

## Open-data access

Copernicus Data Space Ecosystem exposes a STAC catalogue at `https://stac.dataspace.copernicus.eu/v1/`. Public catalogue discovery does not imply anonymous product download: CDSE documentation requires authentication for official OData product downloads and for several processing/access APIs.

The AWS Registry of Open Data Sentinel-2 L2A COG dataset documents public S3 access with `--no-sign-request` and Earth Search STAC discovery. It is therefore a useful independent acquisition route for a future physical-raster replication lane.

## SCL masking

Scene Classification Layer values have defined semantic classes, but a generic scientific validity mask is analysis-dependent. CDSE examples use different class exclusions for different products/workflows. R8 must preregister its mask policy rather than treating `[4,5,6,7,11]` as a universal law.
