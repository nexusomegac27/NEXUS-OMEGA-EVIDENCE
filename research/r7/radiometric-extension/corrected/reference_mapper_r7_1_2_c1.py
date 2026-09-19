#!/usr/bin/env python3
"""NEXUS OMEGA R7.1.2 corrected C1 metadata reference mapper.

This mapper does not claim to process Sentinel-2 raster pixels. It binds a STAC-like
fixture, extracts declared raster scale/offset from assets, records the official
L2A BOA conversion relation, and explicitly marks all pixel-derived quantities as
NOT_COMPUTED when raster assets are absent.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ORDER_SHA256 = "d053289ee688ef14363df80f5d862d19d5a760e83d23009ef22cb0347a179d1e"
DIMS = ("B04", "B08")

def canonical_bytes(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha256_obj(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def band_transform(item, asset_name):
    asset = item.get("assets", {}).get(asset_name, {})
    bands = asset.get("raster:bands", [])
    if not bands:
        return None
    b = bands[0]
    scale = b.get("raster:scale", b.get("scale"))
    offset = b.get("raster:offset", b.get("offset"))
    nodata = b.get("raster:nodata", b.get("nodata"))
    return {"scale": scale, "offset": offset, "nodata": nodata}

def map_item(item):
    props = item.get("properties", {})
    fixture = bool(props.get("nexus:fixture"))
    q = props.get("nexus:quantification_value")
    boa_offset = props.get("nexus:boa_add_offset")
    transforms = {name: band_transform(item, name) for name in DIMS}
    equivalent = None
    if q and boa_offset is not None:
        equivalent = {"scale": 1 / q, "offset": boa_offset / q}
    source_hash = sha256_obj(item)
    return {
        "object": "NEXUS_OMEGA_R7_1_2_RADIOMETRIC_REFERENCE_ATOM_R1",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "truth_authority": "NONE",
        "source_kind": "SYNTHETIC_FIXTURE" if fixture else "DECLARED_STAC_OBJECT",
        "source_sha256_canonical_json": source_hash,
        "reference_order_sha256": ORDER_SHA256,
        "radiometric": {
            "official_l2a_relation": "BOA = (DN + BOA_ADD_OFFSET) / QUANTIFICATION_VALUE",
            "fixture_boa_add_offset": boa_offset,
            "fixture_quantification_value": q,
            "equivalent_scale_offset": equivalent,
            "asset_band_transforms": transforms,
            "pixel_processing_performed": False
        },
        "pixel_derived": {
            "ndvi": {"status": "NOT_COMPUTED", "reason": "B04/B08 raster bytes are not supplied"},
            "valid_pixel_fraction": {"status": "NOT_COMPUTED", "reason": "SCL raster bytes are not supplied"},
            "ndvi_uncertainty": {"status": "NOT_ESTABLISHED", "reason": "No empirical band uncertainty inputs or raster observations are supplied"}
        },
        "stac": {
            "declared_extension_count": len(item.get("stac_extensions", [])),
            "declared_extensions": item.get("stac_extensions", []),
            "quality_extension_declared": any("quality" in x.lower() for x in item.get("stac_extensions", []))
        },
        "geometry": {
            "declared_epsg": props.get("proj:epsg"),
            "display_coordinate_check": {
                "input_epsg4326": [10.6890, 53.8694],
                "expected_epsg25832": [611054.534, 5970313.421],
                "status": "INDEPENDENTLY_REPRODUCED_BY_AXIOM_WITH_PYPROJ_3_7_2"
            },
            "current_collection1_l2a_absolute_geolocation_characteristic": "<12 m at 95.5% confidence",
            "ce90_8m_claim": "NOT_USED_IN_CORRECTED_DERIVATIVE"
        },
        "provenance": {
            "source_package_sha256": "1a758589480533fc703281c2c03f04ff74bf5723153f4e0178ad88132a6231b9",
            "original_r2_zip_sha256": "270ad395c6d4676358f78cd0846cb14769142028c67f8024c39961a8ae388ef9",
            "correction_model": "APPEND_ONLY_DERIVATIVE_DO_NOT_REWRITE_ORIGINAL"
        }
    }

def main():
    p = Path(sys.argv[1] if len(sys.argv)>1 else "sample_fixture_r7_1_2.json")
    obj = json.loads(p.read_text(encoding="utf-8"))
    out = map_item(obj)
    outp = Path(sys.argv[2] if len(sys.argv)>2 else "reference_result_r7_1_2.json")
    outp.write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(out["source_sha256_canonical_json"])
if __name__ == "__main__": main()
