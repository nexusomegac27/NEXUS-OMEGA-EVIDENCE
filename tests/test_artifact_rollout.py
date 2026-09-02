#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("artifact_rollout", ROOT / "scripts" / "artifact_rollout.py")
AR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AR)

BASE_PATH = (
    ROOT
    / "research"
    / "pipeline"
    / "rollout"
    / "plans"
    / "NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0"
    / "rollout.json"
)


def deep_merge(target, patch):
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


class ArtifactRolloutTests(unittest.TestCase):
    def load_base(self):
        return json.loads(BASE_PATH.read_text(encoding="utf-8"))

    def test_current_repository_rollouts_pass(self):
        result = AR.validate(ROOT)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["status"], "PASS")

    def test_negative_fixture_corpus_fails_closed(self):
        count = 0
        for line in (ROOT / "validation" / "artifact-rollout-negative-fixtures-v1.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            fixture = json.loads(line)
            plan = deep_merge(copy.deepcopy(self.load_base()), fixture["mutation"])
            errors = AR.validate_plan_obj(ROOT, plan)
            self.assertIn(fixture["expected_error"], errors, fixture["id"])
            count += 1
        self.assertGreaterEqual(count, 12)

    def test_process_generates_rollout_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            result = AR.process(ROOT, Path(td), write_repo=False)
            self.assertEqual(result["errors"], [])
            rollout_id = "NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0"
            base = Path(td) / rollout_id
            self.assertTrue((base / "READINESS_RECEIPT.json").is_file())
            self.assertTrue((base / "AUTHORITY_GATE_PACKET.json").is_file())
            self.assertTrue((base / "ROLL_OUT_ACK.json").is_file())
            self.assertTrue((base / "ROLLOUT_WORKFLOW_EVENTS.jsonl").is_file())

    def test_seed_rollout_is_required(self):
        self.assertEqual(AR.SEED_ROLLOUT_ID, "NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0")


if __name__ == "__main__":
    unittest.main()
