import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_SRC / "scripts"))

from append_scientific_record import append_record
from validate_scientific_ledger import validate_ledger

def base_record(record_id, record_type="event"):
    return {
      "schema_version":"1.0.0","record_id":record_id,"record_type":record_type,
      "observed_at_utc":"2026-08-31T00:00:00Z","recorded_at_utc":"2026-08-31T00:00:01Z",
      "actor_class":"NEXUS_AI_ROLE","actor_asserted_identity":"AXIOM","actor_verified_identity":None,
      "provider":"OpenAI","transport_class":"GITHUB","observability_class":"OBS3_MEDIATED_EVENT",
      "receipt_assurance":"RA3_AUTHENTICATED_PLATFORM","scientific_relevance_class":"SR1_PROVENANCE_SUPPORT",
      "privacy_class":"METADATA_ONLY","claim_ceiling":"C1","claim_promotion":False,
      "content_sha256":None,"content_bytes":None,"canonicalization_method":"NONE",
      "causal_parent_record_ids":[],"previous_record_sha256":None,"external_witness_refs":[],
      "completeness_status":"COMPLETE","uncertainty":[],
      "event_type":"PR_MERGED","source_locator":"https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/2"
    }

def write_record(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")

class TestScientificLedger(unittest.TestCase):
    def test_append_and_validate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/"r1.json"
            write_record(source, base_record("event:test:00000001"))
            receipt=append_record(root, source, "2026-08-31T00:01:00Z")
            self.assertEqual(receipt["sequence"],1)
            self.assertEqual(validate_ledger(root),[])

    def test_tampered_object_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/"r1.json"
            write_record(source, base_record("event:test:00000001"))
            receipt=append_record(root, source, "2026-08-31T00:01:00Z")
            obj=root/receipt["record_path"]
            obj.write_bytes(obj.read_bytes()+b" ")
            errs=validate_ledger(root)
            self.assertTrue(any("OBJECT_BYTES" in e or "OBJECT_SHA256" in e for e in errs))

    def test_chain_break_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for n in (1,2):
                source=root/f"r{n}.json"
                write_record(source, base_record(f"event:test:{n:08d}"))
                append_record(root, source, f"2026-08-31T00:0{n}:00Z")
            index=root/"communication/index/v1/records.jsonl"
            lines=index.read_text(encoding="utf-8").splitlines()
            second=json.loads(lines[1])
            second["previous_index_line_sha256"]="0"*64
            lines[1]=json.dumps(second, sort_keys=True, separators=(",", ":"))
            index.write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
            errs=validate_ledger(root)
            self.assertTrue(any("PREVIOUS_HASH" in e for e in errs))

    def test_duplicate_record_id_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/"r1.json"
            write_record(source, base_record("event:test:00000001"))
            append_record(root, source, "2026-08-31T00:01:00Z")
            with self.assertRaises(ValueError):
                append_record(root, source, "2026-08-31T00:02:00Z")

if __name__=="__main__":
    unittest.main()
