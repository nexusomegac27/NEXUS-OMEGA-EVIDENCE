import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

class FileProtocolTests(unittest.TestCase):
    def test_file_event_schema_is_strict_json(self):
        p=ROOT/"schema/r5/file-protocol/nexus-file-event-v1.schema.json"
        d=json.loads(p.read_text(encoding="utf-8"))
        self.assertIs(d["additionalProperties"],False)
        self.assertEqual(d["properties"]["claim_ceiling"]["const"],"C1")
        self.assertEqual(d["properties"]["digest_domain"]["const"],"SHA256_RAW_BYTES_V1")

    def test_capability_profile_denies_self_validation_and_force_push(self):
        p=ROOT/"schema/r5/agent-governance/nexus-agent-capability-profile-v1.schema.json"
        d=json.loads(p.read_text(encoding="utf-8"))
        self.assertIs(d["properties"]["git"]["properties"]["force_push"]["const"],False)
        self.assertIs(d["properties"]["authority"]["properties"]["self_validation"]["const"],False)

    def test_file_event_archive_declares_recursion_boundary(self):
        p=ROOT/"docs/r5/file-protocol/CANONICAL_FILE_EVENT_ARCHIVE_V1.md"
        t=p.read_text(encoding="utf-8")
        self.assertIn("LEDGER_DERIVED_METADATA",t)
        self.assertIn("COMMIT_A",t); self.assertIn("COMMIT_B",t)

if __name__=="__main__": unittest.main()
