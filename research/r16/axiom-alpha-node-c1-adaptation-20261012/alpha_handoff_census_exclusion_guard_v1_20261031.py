#!/usr/bin/env python3
"""Additive, isolated C1 guard for unverified exclusions in census V1.1.
No API calls, no authentication claim, no production integration.
"""
import json
import sys
from alpha_handoff_census_v1_1 import census, unique_object


def guarded_census(payload):
    result = census(payload)
    if result.get("status") == "STRUCTURAL_ONLY_NOT_AUTHENTICATED":
        excluded = result.get("excluded_with_declared_reason", 0)
        result["exclusion_verification"] = "NOT_INDEPENDENTLY_VERIFIED"
        if excluded:
            result["handoff"]["rate_percent"] = None
            result["publication"]["rate_percent"] = None
            result["rate_block_reason"] = "EXCLUSION_SCOPE_NOT_AUTHENTICATED"
    return result


def main():
    try:
        data = json.loads(sys.stdin.read(), object_pairs_hook=unique_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite_json")))
        result = guarded_census(data)
    except (ValueError, TypeError, RecursionError, UnicodeError) as exc:
        result = {"status": "FAIL_CLOSED", "reason": type(exc).__name__}
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    sys.exit(main())
