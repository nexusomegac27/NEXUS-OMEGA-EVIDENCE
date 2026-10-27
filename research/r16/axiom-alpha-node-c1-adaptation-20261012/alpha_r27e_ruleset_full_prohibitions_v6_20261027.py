#!/usr/bin/env python3
"""Isolated C1 V6: require every R27-E external-write prohibition in registry.

Extends the immutable V5 research auditor without modifying its source.
Only caller-supplied snapshots are inspected; no GitHub API authentication,
external actor registration, branch rule, or runtime change is implied.
"""
import json
import sys

from alpha_r27e_ruleset_ref_exclusion_audit_v3_20261027 import (
    MAX_BYTES, fail, nonfinite, unique_pairs,
)
from alpha_r27e_ruleset_registry_contract_v5_20261027 import audit as audit_v5

# Exact prohibitions in docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json
# at pinned main 36d712268072d0252a94ebd699113ee151c80f1f.
FULL_PROHIBITIONS = frozenset({
    "EXTERNAL_ROOT_OR_NAMESPACE_CREATION",
    "EXTERNAL_EDIT_EXISTING_FILES",
    "EXTERNAL_RENAME_DELETE_MOVE",
    "EXTERNAL_CREATE_SUBDIRECTORY",
    "EXTERNAL_PATCH_GOVERNANCE_CODE_CI",
    "EXTERNAL_CREATE_OWN_TEMPLATE",
    "AUTO_MERGE", "AUTO_RUNTIME", "NEW_WORKER",
})


def audit(data):
    result = audit_v5(data)
    prohibited = data["registry"].get("prohibited")
    complete = (type(prohibited) is list and
                all(type(x) is str for x in prohibited) and
                len(prohibited) == len(set(prohibited)) and
                FULL_PROHIBITIONS.issubset(prohibited))
    result["registry_full_prohibitions_pinned"] = complete
    if not complete:
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
