#!/usr/bin/env python3
"""Frozen black-box C1 oracle for unauthorized-publication signal; not a GitHub authenticator.

This evaluator is independent of the candidate implementation and uses only
synthetic, explicitly caller-supplied fixtures. No oracle self-approval.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get("AXIOM_CANDIDATE", Path(__file__).with_name(
    "alpha_handoff_census_unauthorized_witness_v2_20261027.py")))
H40 = "a" * 40
H64 = "b" * 64


def event(identifier, **kwargs):
    e = {"id": identifier, "timestamp_utc": "2026-10-27T12:00:00Z",
         "routine": True, "public": True, "authorized": True, "accessible": True,
         "manual_nudge": False, "published": True, "source_sha256": H64,
         "main_commit": H40, "source_readback": True, "test_readback": True,
         "main_readback": True, "receipt_readback": True}
    e.update(kwargs)
    return e


def census(events, complete=True):
    return {"object": "NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1",
            "census_complete": complete, "events": events,
            "window_start_utc": "2026-10-27T00:00:00Z",
            "window_end_utc": "2026-10-28T00:00:00Z"}


def run(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class FrozenSecurityOracle(unittest.TestCase):
    def check(self, events, expected_ids, complete=True):
        p = run(census(events, complete))
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        out = json.loads(p.stdout)
        self.assertEqual(out["caller_reported_unauthorized_published_ids"], expected_ids)
        self.assertEqual(out["caller_reported_unauthorized_published_count"], len(expected_ids))
        self.assertEqual(out["security_signal"],
                         "CALLER_REPORTED_UNAUTHORIZED_PUBLICATION" if expected_ids
                         else "NO_CALLER_REPORTED_UNAUTHORIZED_PUBLICATION")
        self.assertIs(out["zero_unauthorized_writes_verified"], False)
        self.assertIs(out["caller_records_authenticated"], False)
        self.assertIs(out["project_90_percent_verified"], False)
        self.assertIs(out["project_100_percent_readback_verified"], False)
        self.assertEqual(out["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        return out

    def test_unauthorized_published_with_complete_readback(self):
        x = self.check([event("u", authorized=False)], ["u"])
        self.assertEqual(x["eligible_denominator_observed"], 0)
        self.assertEqual(x["published_denominator_observed"], 1)
        self.assertEqual(x["complete_readback_numerator_observed"], 1)

    def test_unauthorized_published_without_readback(self):
        x = self.check([event("u", authorized=False, receipt_readback=False)], ["u"])
        self.assertEqual(x["complete_readback_numerator_observed"], 0)

    def test_authorized_published_control(self):
        x = self.check([event("ok")], [])
        self.assertEqual(x["automated_numerator_observed"], 1)
        self.assertEqual(x["conditional_readback_rate"], 1.0)

    def test_unauthorized_unpublished_control(self):
        self.check([event("u", authorized=False, published=False)], [])

    def test_mixed_and_sorted(self):
        x = self.check([event("z", authorized=False), event("ok"),
                        event("a", authorized=False, routine=False)], ["a", "z"])
        self.assertEqual(x["eligible_denominator_observed"], 1)
        self.assertEqual(x["published_denominator_observed"], 3)

    def test_incomplete_census_does_not_suppress_security_signal(self):
        x = self.check([event("u", authorized=False)], ["u"], complete=False)
        self.assertEqual(x["state"], "NOT_COMPUTABLE_INCOMPLETE_CENSUS")
        self.assertIsNone(x["conditional_readback_rate"])

    def test_duplicate_event_id_fail_closed(self):
        p = run(census([event("x"), event("x", authorized=False)]))
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"INVALID_OR_DUPLICATE_EVENT_ID", p.stderr)

    def test_non_boolean_authorization_fail_closed(self):
        p = run(census([event("u", authorized=0)]))
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"INVALID_EVENT_BOOLEAN", p.stderr)

    def test_duplicate_json_key_fail_closed(self):
        p = run(b'{"object":"NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1","census_complete":true,"census_complete":false,"events":[]}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"DUPLICATE_JSON_KEY", p.stderr)

    def test_missing_source_hash_still_flags_unauthorized(self):
        x = self.check([event("u", authorized=False, source_sha256=None)], ["u"])
        self.assertEqual(x["complete_readback_numerator_observed"], 0)


if __name__ == "__main__":
    unittest.main()
