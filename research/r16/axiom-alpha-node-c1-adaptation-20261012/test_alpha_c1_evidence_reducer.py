#!/usr/bin/env python3
"""Deterministic one-defect fixtures for Alpha-Node C1 evidence intake."""
import hashlib
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).with_name("alpha_c1_evidence_reducer.py")
spec = importlib.util.spec_from_file_location("alpha_c1_evidence_reducer", MODULE)
reducer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reducer)
PAYLOAD = b"verified c1 sample\n"
SHA = hashlib.sha256(PAYLOAD).hexdigest()


def baseline():
    return {"sha256": SHA, "bytes": len(PAYLOAD), "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
            "public_safe": True, "publication_rights": True, "kind": "research"}


class TestAlphaC1EvidenceReducer(unittest.TestCase):
    def test_good_public_research(self):
        r = reducer.decide(baseline(), PAYLOAD)
        self.assertEqual((r["decision"], r["research_push_eligible"]), ("KNOWLEDGE_APPEND", True))

    def test_duplicate(self):
        self.assertEqual(reducer.decide(baseline(), PAYLOAD, [SHA])["reason"], "NOOP_DUPLICATE")

    def test_source_absent(self):
        self.assertEqual(reducer.decide(baseline(), None)["reason"], "SOURCE_GAP")

    def test_byte_mismatch(self):
        c = baseline(); c["bytes"] += 1
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "SOURCE_MISMATCH")

    def test_digest_mismatch(self):
        c = baseline(); c["sha256"] = "0" * 64
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "SOURCE_MISMATCH")

    def test_claim_ceiling(self):
        c = baseline(); c["claim_ceiling"] = "C2"
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "CLAIM_CEILING_OR_SCOPE_INVALID")

    def test_no_public_safe(self):
        c = baseline(); c["public_safe"] = False
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "PRIVACY_OR_PUBLICATION_RIGHTS_UNPROVEN")

    def test_no_publication_rights(self):
        c = baseline(); c["publication_rights"] = False
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "PRIVACY_OR_PUBLICATION_RIGHTS_UNPROVEN")

    def test_code_candidate_is_not_auto_pushable(self):
        c = baseline(); c["kind"] = "code_change"
        r = reducer.decide(c, PAYLOAD)
        self.assertEqual(r["decision"], "PATCH_CANDIDATE")
        self.assertFalse(r["research_push_eligible"])
        self.assertFalse(r["runtime_modified"])

    def test_contradiction_is_preserved(self):
        c = baseline(); c["kind"] = "contradiction"
        self.assertEqual(reducer.decide(c, PAYLOAD)["decision"], "CONTRADICTION_APPEND")

    def test_unknown_kind(self):
        c = baseline(); c["kind"] = "configuration_escalation"
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "UNKNOWN_MATERIAL_KIND")

    def test_invalid_hash_shape(self):
        c = baseline(); c["sha256"] = "short"
        self.assertEqual(reducer.decide(c, PAYLOAD)["reason"], "INVALID_EXPECTED_BYTES_OR_SHA256")


if __name__ == "__main__":
    unittest.main()
