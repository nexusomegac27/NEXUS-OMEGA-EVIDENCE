# Primary-source cross-check

Validated against primary/authoritative sources on 2026-09-19.

- ESA Sentinel-2 Product Specification / L2A data-quality documentation: L2A BOA reflectance is recovered as `(DN + BOA_ADD_OFFSET) / QUANTIFICATION_VALUE`; BOA_ADD_OFFSET is `-1000` for PB >= 04.00.
  - https://sentinels.copernicus.eu/documents/d/sentinel/s2-pdgs-cs-di-psd-v15-0
  - https://sentinels.copernicus.eu/documents/247904/4862382/OMPC.CS.DQR.002.11-2022%20-%20i56r0%20-%20MSI%20L2A%20DQR%20December%202022.pdf/6c26f8fc-0377-0af4-62dd-bf9cb1d858fd
- ESA Sentinel-2 Collection-1 L2A current product characteristics: absolute geolocation `<12 m at 95.5% confidence`.
  - https://sentinels.copernicus.eu/data-products/-/asset_publisher/fp37fc19FN8F/content/id/4715515
- ESA SCL classes confirm 4 vegetation, 5 not vegetated, 6 water, 7 unclassified, 11 snow/ice. This classification does not by itself justify treating all of those classes as a universal “valid NDVI” mask.
  - https://sentinels.copernicus.eu/documents/d/sentinel/s2-pdgs-cs-di-psd-v15-0
- STAC Raster Extension v2.0.0 defines raster scale/offset for raster bands and recommends application of provided scale/offset. The corrected derivative uses asset-level band metadata rather than treating SCL as a reflectance band.
  - https://github.com/stac-extensions/raster
- REANA is a CERN-made reproducible analysis platform, but presence of a REANA YAML file does not prove execution of the supplied workflow.
  - https://reanahub.io/
