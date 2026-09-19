import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("mapper",ROOT/"corrected/reference_mapper_r7_1_2_c1.py")
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
ITEM=json.loads((ROOT/"corrected/sample_fixture_r7_1_2.json").read_text(encoding="utf-8"))
class Tests(unittest.TestCase):
    def test_order_bind(self):
        self.assertEqual(M.ORDER_SHA256,"d053289ee688ef14363df80f5d862d19d5a760e83d23009ef22cb0347a179d1e")
    def test_formula_equivalence(self):
        x=M.map_item(ITEM)["radiometric"]
        self.assertEqual(x["equivalent_scale_offset"],{"scale":0.0001,"offset":-0.1})
        self.assertAlmostEqual((2500-1000)/10000,2500*0.0001-0.1)
    def test_no_pixel_claims_without_pixels(self):
        x=M.map_item(ITEM)["pixel_derived"]
        self.assertEqual(x["ndvi"]["status"],"NOT_COMPUTED")
        self.assertEqual(x["valid_pixel_fraction"]["status"],"NOT_COMPUTED")
        self.assertEqual(x["ndvi_uncertainty"]["status"],"NOT_ESTABLISHED")
    def test_six_declared_extensions_no_quality(self):
        x=M.map_item(ITEM)["stac"]
        self.assertEqual(x["declared_extension_count"],6)
        self.assertFalse(x["quality_extension_declared"])
    def test_asset_raster_transform(self):
        x=M.map_item(ITEM)["radiometric"]["asset_band_transforms"]
        self.assertEqual(x["B04"]["scale"],0.0001)
        self.assertEqual(x["B08"]["offset"],-0.1)
    def test_no_truth_authority(self):
        self.assertEqual(M.map_item(ITEM)["truth_authority"],"NONE")
if __name__=="__main__": unittest.main()
