#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only standalone negative fixture suite for NEXUS research continuity."""
import json
import tempfile
from pathlib import Path
import unittest
from datetime import datetime, timezone
import importlib.util

script = Path(__file__).resolve().parents[1] / "scripts/archive_continuity_guard.py"
spec = importlib.util.spec_from_file_location("nexus_continuity_guard", script)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class ContinuityGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.as_of = datetime(2026, 10, 13, tzinfo=timezone.utc)
        self.structure = self.root / "docs/architecture/REPOSITORY_STRUCTURE.json"
        self.index = self.root / "research/pipeline/index/latest.json"
        self.pkg = self.root / "research/pipeline/packages/2026/09/NEXUS_RP_20260901T035600Z_fixture_abcdef12/manifest.json"
        self.event = self.root / "research/pipeline/events/2026/09/01/20260901T035700Z_E01.json"
        for p in (self.structure, self.index, self.pkg, self.event):
            p.parent.mkdir(parents=True, exist_ok=True)
        self.write(self.structure, {"version":"1.7.13","active_research_lanes":{"fixture":{"path":"research/fixture/x","state":"READY_FOR_CURSOR"}}})
        (self.root / "research/fixture/x").mkdir(parents=True)
        (self.root / "research/fixture/x/README.md").write_text("C1\n")
        self.write(self.index, {"generated_at_utc":"2026-09-01T04:03:02Z"})
        self.write(self.pkg, {"package_id":self.pkg.parent.name,"state":"READY_FOR_CURSOR","updated_at_utc":"2026-09-01T04:03:00Z"})
        self.write(self.event, {"event_id":"E01","package_id":self.pkg.parent.name,"recorded_at_utc":"2026-09-01T03:57:00Z"})

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_old_open_package_and_index_are_reviewed_not_global_failure(self):
        report = g.audit(self.root, self.as_of)
        self.assertEqual(report["registered_lane_count"], 1)
        self.assertEqual(report["observed_event_count"], 1)
        self.assertEqual(report["derived_index"]["age_days"], 41)
        codes = {x["code"] for x in report["findings"]}
        self.assertIn("AGING_OPEN_REVIEW", codes)
        self.assertIn("DERIVED_INDEX_AGE_EXCEEDS_BUDGET", codes)
        self.assertEqual(report["findings_by_severity"]["INTEGRITY"], 0)

    def test_closed_package_does_not_trigger_open_age(self):
        doc = json.loads(self.pkg.read_text())
        doc["state"] = "PROCESSED"
        self.write(self.pkg, doc)
        self.assertNotIn("AGING_OPEN_REVIEW", [x["code"] for x in g.audit(self.root,self.as_of)["findings"]])

    def test_missing_lane_readme_is_integrity_error(self):
        (self.root/"research/fixture/x/README.md").unlink()
        self.assertEqual(g.audit(self.root,self.as_of)["findings_by_severity"]["INTEGRITY"], 1)

    def test_duplicate_registered_path_detected(self):
        doc = json.loads(self.structure.read_text())
        doc["active_research_lanes"]["other"] = {"path":"research/fixture/x"}
        self.write(self.structure, doc)
        self.assertIn("DUPLICATE_REGISTERED_PATH", [x["code"] for x in g.audit(self.root,self.as_of)["findings"]])

    def test_path_traversal_rejected(self):
        doc = json.loads(self.structure.read_text())
        doc["active_research_lanes"]["fixture"]["path"] = "research/../private"
        self.write(self.structure, doc)
        with self.assertRaisesRegex(ValueError, "INVALID_LANE_PATH"):
            g.audit(self.root,self.as_of)

    def test_duplicate_json_key_rejected(self):
        self.structure.write_text('{"active_research_lanes":{},"active_research_lanes":{}}')
        with self.assertRaisesRegex(ValueError, "DUPLICATE_KEY"):
            g.audit(self.root,self.as_of)

    def test_invalid_event_identity_detected(self):
        self.write(self.event, {"event_id":"E01","recorded_at_utc":"2026-09-01T03:57:00Z"})
        self.assertEqual(g.audit(self.root,self.as_of)["event_error_count"], 1)

    def test_invalid_derived_index_does_not_block_events(self):
        self.write(self.index, {"generated_at_utc":"invalid"})
        r=g.audit(self.root,self.as_of)
        self.assertEqual(r["observed_event_count"], 1)
        self.assertIn("DERIVED_INDEX_TIMESTAMP_INVALID", [x["code"] for x in r["findings"]])

    def test_readonly_does_not_mutate_sources(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result=g.audit(self.root,self.as_of)
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before,after)
        self.assertEqual(result["tokenneutral_external_llm_calls_in_audit"],0)
        self.assertEqual(result["runtime_mcp_node_bus"],"NOT_ASSESSED")

    def test_open_age_boundary_not_terminal_age(self):
        self.assertEqual(g.severity("ACTIVE",30,30),"AGING_OPEN_REVIEW")
        self.assertEqual(g.severity("ACTIVE",29,30),"NO_TIME_ESCALATION")
        self.assertEqual(g.severity("PROCESSED",100,30),"NO_TIME_ESCALATION")


if __name__ == "__main__":
    unittest.main()
