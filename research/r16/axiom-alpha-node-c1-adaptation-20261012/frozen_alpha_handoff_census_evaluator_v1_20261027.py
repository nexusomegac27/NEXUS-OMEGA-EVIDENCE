#!/usr/bin/env python3
"""Independent black-box oracle for the C1 handoff-census research candidate.

The oracle does not import the candidate, nor treat a caller-provided receipt as
an authenticated GitHub event. Tests are synthetic, not operational evidence.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get("AXIOM_CANDIDATE", Path(__file__).with_name(
    "alpha_handoff_census_gate_v1_20261027.py")))
H40 = "a" * 40
H64 = "b" * 64


def event(identifier, **changes):
    e = {"id": identifier, "timestamp_utc": "2026-10-27T12:00:00Z", "routine": True, "public": True,
         "authorized": True, "accessible": True, "manual_nudge": False,
         "published": True, "source_sha256": H64, "main_commit": H40,
         "source_readback": True, "test_readback": True,
         "main_readback": True, "receipt_readback": True}
    e.update(changes)
    return e


def census(events, complete=True):
    return {"object": "NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1",
            "census_complete": complete, "events": events,
            "window_start_utc": "2026-10-27T00:00:00Z",
            "window_end_utc": "2026-10-28T00:00:00Z"}


def run(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj).encode("utf-8")
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def check(self, obj, state, eligible, automated, rate, published, readbacks, readback_rate):
        p = run(obj)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        r = json.loads(p.stdout)
        self.assertEqual(r["state"], state)
        self.assertEqual(r["eligible_denominator_observed"], eligible)
        self.assertEqual(r["automated_numerator_observed"], automated)
        self.assertEqual(r["conditional_automation_rate"], rate)
        self.assertEqual(r["published_denominator_observed"], published)
        self.assertEqual(r["complete_readback_numerator_observed"], readbacks)
        self.assertEqual(r["conditional_readback_rate"], readback_rate)
        self.assertIs(r["caller_records_authenticated"], False)
        self.assertIs(r["project_90_percent_verified"], False)
        self.assertIs(r["project_100_percent_readback_verified"], False)
        self.assertEqual(r["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        return r

    def reject(self, obj, code):
        p = run(obj)
        self.assertEqual(p.returncode, 2)
        self.assertIn(code.encode(), p.stderr)

    def test_incomplete_census_even_with_one_success(self):
        self.check(census([event("e1")], False), "NOT_COMPUTABLE_INCOMPLETE_CENSUS",
                   1, 1, None, 1, 1, None)

    def test_zero_denominator(self):
        self.check(census([]), "NOT_COMPUTABLE_ZERO_DENOMINATOR", 0, 0, None, 0, 0, None)

    def test_ten_with_nine_complete(self):
        x = [event(str(i)) for i in range(9)] + [event("9", manual_nudge=True)]
        self.check(census(x), "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY",
                   10, 9, 0.9, 10, 10, 1.0)

    def test_eight_of_ten(self):
        x = [event(str(i)) for i in range(8)] + [event("8", manual_nudge=True), event("9", published=False)]
        self.check(census(x), "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY",
                   10, 8, 0.8, 9, 9, 1.0)

    def test_missing_receipt_excludes_numerator(self):
        r = self.check(census([event("e", receipt_readback=False)]),
                       "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 0, 0.0, 1, 0, 0.0)
        self.assertEqual(r["incomplete_published_event_ids"], ["e"])

    def test_private_inaccessible_excluded(self):
        self.check(census([event("ok"), event("private", public=False, accessible=False)]),
                   "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 1, 1.0, 2, 2, 1.0)

    def test_unauthorized_published_excluded_from_automation_not_readback(self):
        self.check(census([event("bad", authorized=False), event("ok")]),
                   "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 1, 1.0, 2, 2, 1.0)

    def test_missing_source_hash_excludes_numerator(self):
        self.check(census([event("e", source_sha256=None)]),
                   "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 0, 0.0, 1, 0, 0.0)

    def test_missing_main_commit_excludes_numerator(self):
        self.check(census([event("e", main_commit=None)]),
                   "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 0, 0.0, 1, 0, 0.0)

    def test_missing_test_readback_excludes_numerator(self):
        self.check(census([event("e", test_readback=False)]),
                   "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY", 1, 0, 0.0, 1, 0, 0.0)

    def test_outside_window_fail_closed(self):
        self.reject(census([event("e", timestamp_utc="2026-10-28T12:00:00Z")]), "EVENT_OUTSIDE_CENSUS_WINDOW")

    def test_invalid_window_order_fail_closed(self):
        x = census([event("e")]); x["window_end_utc"] = x["window_start_utc"]
        self.reject(x, "INVALID_WINDOW_ORDER")

    def test_invalid_timestamp_fail_closed(self):
        self.reject(census([event("e", timestamp_utc="2026-02-30T12:00:00Z")]), "INVALID_UTC_TIMESTAMP")

    def test_duplicate_event_id_fail_closed(self):
        self.reject(census([event("e"), event("e")]), "INVALID_OR_DUPLICATE_EVENT_ID")

    def test_duplicate_json_key_fail_closed(self):
        self.reject(b'{"object":"NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1","census_complete":true,"census_complete":false,"events":[]}', "DUPLICATE_JSON_KEY")

    def test_nonfinite_json_fail_closed(self):
        self.reject(b'{"object":"NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1","census_complete":true,"events":[],"junk":NaN}', "NONFINITE_JSON")

    def test_boolean_type_fail_closed(self):
        self.reject(census([event("e", authorized=1)]), "INVALID_EVENT_BOOLEAN")

    def test_incorrect_source_hash_fail_closed(self):
        self.reject(census([event("e", source_sha256="abc")]), "INVALID_SOURCE_HASH")

    def test_oversized_input_fail_closed(self):
        self.reject(b" " * 262145, "INPUT_TOO_LARGE")

    def test_missing_flag_fail_closed(self):
        x = event("e"); del x["manual_nudge"]
        self.reject(census([x]), "INVALID_EVENT_BOOLEAN")

    def test_unexpected_event_field_fail_closed(self):
        self.reject(census([event("e", self_approved=True)]), "INVALID_EVENT_FIELDS")


if __name__ == "__main__":
    unittest.main()
