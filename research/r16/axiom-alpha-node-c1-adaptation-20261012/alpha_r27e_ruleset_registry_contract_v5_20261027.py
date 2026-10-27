#!/usr/bin/env python3
"""Isolated C1 V5: fail closed on R27-E registry contract drift.

Pinned to the public 2026-10-27 registry fields at main 91f79dbb...;
caller-supplied snapshots are not authenticated GitHub API evidence.
No access-control, CI, runtime or model mutation is performed.
"""
import json
import sys

from alpha_r27e_ruleset_ref_exclusion_audit_v3_20261027 import (
    MAX_BYTES, fail, nonfinite, unique_pairs,
)
from alpha_r27e_ruleset_validate_source_and_ref_v4_20261027 import audit as audit_v4

EXPECTED_PROHIBITIONS = frozenset({
    "AUTO_MERGE", "AUTO_RUNTIME", "NEW_WORKER",
    "EXTERNAL_PATCH_GOVERNANCE_CODE_CI", "EXTERNAL_EDIT_EXISTING_FILES",
})


def registry_contract_matches(registry):
    assignments = registry.get("assignments")
    prohibited = registry.get("prohibited")
    if (type(assignments) is not list or len(assignments) != 1 or
            type(assignments[0]) is not dict or type(prohibited) is not list or
            any(type(x) is not str for x in prohibited) or
            len(prohibited) != len(set(prohibited))):
        return False
    assignment = assignments[0]
    return (
        registry.get("status") ==
        "C1_OPERATOR_PREALLOCATED_SLOTS_EXTERNAL_ACTORS_NOT_AUTHORIZED" and
        registry.get("authority") == "NEXUS_OPERATOR_GOVERNED_ONLY" and
        registry.get("owner_github_login") == "nexusomegac27" and
        assignment.get("assignment_id") == "R27-E-20261011" and
        assignment.get("returns_path") ==
        "research/r27/www-extern-wake-isolation-20261011/returns/" and
        assignment.get("status") == "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED" and
        EXPECTED_PROHIBITIONS.issubset(prohibited)
    )


def audit(data):
    result = audit_v4(data)
    pinned = registry_contract_matches(data["registry"])
    result["registry_contract_fields_pinned"] = pinned
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
