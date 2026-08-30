import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_scientific_communication import errors, run_fixtures

class TestScientificCommunication(unittest.TestCase):
    def test_negative_fixtures(self):
        self.assertEqual(run_fixtures(ROOT/"validation/scientific-communication-negative-fixtures-v1.jsonl"),0)

    def test_positive_minimal_event(self):
        record={
          "schema_version":"1.0.0","record_id":"event:positive:00000001","record_type":"event",
          "observed_at_utc":"2026-08-31T00:00:00Z","recorded_at_utc":"2026-08-31T00:00:01Z",
          "actor_class":"VALIDATOR","actor_asserted_identity":"example-validator","actor_verified_identity":None,
          "provider":"example","transport_class":"API","observability_class":"OBS2_PROVIDER_EVENT",
          "receipt_assurance":"RA1_SELF_ASSERTED","scientific_relevance_class":"SR1_PROVENANCE_SUPPORT",
          "privacy_class":"METADATA_ONLY","claim_ceiling":"C1","claim_promotion":False,
          "content_sha256":None,"content_bytes":None,"canonicalization_method":"NONE",
          "causal_parent_record_ids":[],"previous_record_sha256":None,"external_witness_refs":[],
          "completeness_status":"PARTIAL","uncertainty":[]
        }
        self.assertEqual(errors(record),[])

if __name__=="__main__":
    unittest.main()
