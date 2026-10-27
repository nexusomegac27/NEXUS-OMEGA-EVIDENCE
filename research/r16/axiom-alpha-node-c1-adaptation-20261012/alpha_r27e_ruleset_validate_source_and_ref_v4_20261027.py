#!/usr/bin/env python3
"""Isolated C1 V4: compose V3 ref/registry guards with pinned validate app source.

Uses caller-supplied snapshots only; no API authentication, runtime, or ruleset
mutation. The historical V3 is imported unchanged, never overwritten.
"""
import json
import sys

from alpha_r27e_ruleset_ref_exclusion_audit_v3_20261027 import (
    MAX_BYTES, audit as audit_v3, fail, nonfinite, unique_pairs,
)

EXPECTED_VALIDATE_APP_ID = 15368  # GitHub ruleset 21252293 read 2026-10-27


def audit(data):
    result = audit_v3(data)
    pinned = False
    for rule in data["ruleset"]["rules"]:
        if type(rule) is dict and rule.get("type") == "required_status_checks":
            for item in rule["parameters"]["required_status_checks"]:
                if item["context"] == "validate":
                    pinned = (type(item.get("integration_id")) is int and
                              item["integration_id"] == EXPECTED_VALIDATE_APP_ID)
    result["validate_expected_app_source_pinned"] = pinned
    if not pinned:
        result["state"] = "HOLD_SCOPED_ENFORCEMENT_GAP"
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail("INPUT_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=nonfinite)
        print(json.dumps(audit(data), sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
