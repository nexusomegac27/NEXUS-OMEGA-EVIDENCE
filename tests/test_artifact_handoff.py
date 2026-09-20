#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("artifact_handoff", ROOT / "scripts" / "artifact_handoff.py")
AH = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AH)

BASE_PATH = (
    ROOT
    / "research"
    / "pipeline"
    / "handoff"
    / "inbox"
    / "NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0"
    / "handoff.json"
)


def deep_merge(target, patch):
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


class ArtifactHandoffTests(unittest.TestCase):
    def load_base(self):
        return json.loads(BASE_PATH.read_text(encoding="utf-8"))

    def test_current_repository_handoffs_pass(self):
        result = AH.validate(ROOT)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["status"], "PASS")

    def test_negative_fixture_corpus_fails_closed(self):
        count = 0
        for line in (ROOT / "validation" / "artifact-handoff-negative-fixtures-v1.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            fixture = json.loads(line)
            env = deep_merge(copy.deepcopy(self.load_base()), fixture["mutation"])
            errors = AH.validate_envelope_obj(ROOT, env)
            self.assertIn(fixture["expected_error"], errors, fixture["id"])
            count += 1
        self.assertGreaterEqual(count, 8)

    def test_process_generates_bind_relay_ack_receipts(self):
        with tempfile.TemporaryDirectory() as td:
            result = AH.process(ROOT, Path(td), write_repo=False)
            self.assertEqual(result["errors"], [])
            handoff_id = "NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0"
            base = Path(td)
            self.assertTrue((base / "bound" / handoff_id / "BIND_RECEIPT.json").is_file())
            self.assertTrue((base / "relay" / handoff_id / "RELAY_PACKET.json").is_file())
            self.assertTrue((base / "ack" / handoff_id / "ACK_RECEIPT.json").is_file())
            self.assertTrue((base / "ack" / handoff_id / "HANDOFF_WORKFLOW_EVENTS.jsonl").is_file())

    def test_seed_handoff_is_required(self):
        self.assertEqual(AH.SEED_HANDOFF_ID, "NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0")


if __name__ == "__main__":
    unittest.main()
