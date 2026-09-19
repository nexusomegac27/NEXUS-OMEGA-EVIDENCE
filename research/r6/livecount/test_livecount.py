#!/usr/bin/env python3
import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("livecount",ROOT/"build_livecount.py")
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
class LivecountTests(unittest.TestCase):
    def test_payload_hash(self):
        x=json.loads((ROOT/"current.json").read_text(encoding="utf-8"))
        self.assertEqual(M.sha(x["payload"]),x["payload_sha256"])
    def test_source_hash(self):
        x=json.loads((ROOT/"current.json").read_text(encoding="utf-8"))
        s=json.loads((ROOT/"sources.json").read_text(encoding="utf-8"))
        self.assertEqual(M.sha(s),x["payload"]["source_manifest_sha256"])
    def test_no_truth_score(self):
        x=json.loads((ROOT/"current.json").read_text(encoding="utf-8"))
        self.assertFalse(x["payload"]["interpretation"]["majority_equals_truth"])
        self.assertFalse(x["payload"]["interpretation"]["hash_match_equals_truth"])
        self.assertNotIn("trust_score", json.dumps(x).lower())
    def test_unestimable_without_empirical_observations(self):
        x=json.loads((ROOT/"current.json").read_text(encoding="utf-8"))
        self.assertEqual(x["payload"]["counts"]["external_empirical_observations_raw_n"],0)
        self.assertEqual(x["payload"]["estimands"]["effective_n"]["status"],"NOT_ESTIMABLE")
        self.assertEqual(x["payload"]["estimands"]["ksm"]["status"],"NOT_ESTIMABLE")
        self.assertEqual(x["payload"]["estimands"]["kse"]["status"],"NOT_ESTIMABLE")
    def test_source_count(self):
        x=json.loads((ROOT/"current.json").read_text(encoding="utf-8"))
        self.assertEqual(x["payload"]["counts"]["hash_verified_input_artifacts"],6)
        self.assertEqual(x["payload"]["counts"]["stability_vector_dimensions"],10)
        self.assertEqual(x["payload"]["counts"]["independence_classes"],8)
if __name__=="__main__": unittest.main()
