#!/usr/bin/env python3
"""Isolated C1 attempt denominator reducer. Producer declarations are NOT authenticated evidence."""
import json
import re
import sys

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
STATES = ("eligible", "excluded", "unknown")
FIELDS = ("public", "routine", "authorized", "accessible")
FLAGS = ("unauthorized_write", "hidden_source_gap", "source_overwrite", "claim_promotion")


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def reject_constant(value):
    raise ValueError("NONFINITE_JSON")


def check_bool(value, name):
    if value is not None and type(value) is not bool:
        raise ValueError("INVALID_TRI_BOOL:" + name)


def reduce(data):
    if type(data) is not dict or data.get("schema") != "ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1":
        raise ValueError("INVALID_SCHEMA")
    if type(data.get("scope")) is not str or not data["scope"].strip():
        raise ValueError("INVALID_SCOPE")
    if not isinstance(data.get("pinned_main"), str) or not HEX40.fullmatch(data["pinned_main"]):
        raise ValueError("INVALID_MAIN")
    if data.get("coverage") not in ("INCOMPLETE", "DECLARED_COMPLETE_NOT_AUTHENTICATED"):
        raise ValueError("INVALID_COVERAGE")
    rows = data.get("attempts")
    if type(rows) is not list:
        raise ValueError("INVALID_ATTEMPTS")
    seen = set()
    result = {"eligible": 0, "excluded": 0, "unknown": 0, "autonomous_verified": 0,
              "safety_qualified_autonomous": 0, "published": 0, "complete_readback": 0,
              "observed_violations": 0, "unknown_safety_rows": 0}
    for row in rows:
        if type(row) is not dict:
            raise ValueError("INVALID_ROW")
        ident = row.get("attempt_id")
        if type(ident) is not str or not ident.strip() or ident in seen:
            raise ValueError("DUPLICATE_OR_INVALID_ATTEMPT_ID")
        seen.add(ident)
        if not isinstance(row.get("source_ref"), str) or not row["source_ref"].startswith("https://github.com/"):
            raise ValueError("SOURCE_REF_MISSING")
        if not isinstance(row.get("source_commit"), str) or not HEX40.fullmatch(row["source_commit"]):
            raise ValueError("SOURCE_COMMIT_MISSING")
        for key in (*FIELDS, "autonomous", "handoff_verified", "published", "full_readback", *FLAGS):
            check_bool(row.get(key), key)
        if row.get("published") is True:
            result["published"] += 1
            if row.get("full_readback") is True:
                result["complete_readback"] += 1
        violation = any(row.get(f) is True for f in FLAGS)
        if violation:
            result["observed_violations"] += 1
        if any(row.get(f) is None for f in FLAGS):
            result["unknown_safety_rows"] += 1
        vals = [row.get(k) for k in FIELDS]
        if False in vals:
            classification = "excluded"
        elif None in vals:
            classification = "unknown"
        else:
            classification = "eligible"
        result[classification] += 1
        if classification == "eligible" and row.get("autonomous") is True and row.get("handoff_verified") is True:
            result["autonomous_verified"] += 1
            if not violation and all(row.get(f) is False for f in FLAGS):
                result["safety_qualified_autonomous"] += 1
    denominator = result["eligible"]
    pub = result["published"]
    result.update({"schema": "ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_RESULT_V1", "scope": data["scope"],
                   "pinned_main": data["pinned_main"], "coverage": data["coverage"],
                   "attempts_seen": len(rows),
                   "sample_autonomous_rate": result["autonomous_verified"] / denominator if denominator else None,
                   "sample_safety_qualified_rate": result["safety_qualified_autonomous"] / denominator if denominator else None,
                   "sample_readback_rate": result["complete_readback"] / pub if pub else None,
                   "project_automation_rate": None, "project_full_readback_rate": None,
                   "project_zero_violation_claim": "NOT_ESTABLISHED",
                   "provenance": "DECLARED_SOURCE_REFS_NOT_INDEPENDENTLY_AUTHENTICATED",
                   "claim_ceiling": "C1_DESCRIPTIVE_ONLY"})
    return result


def main():
    try:
        data = json.load(sys.stdin, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
        result = reduce(data)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "state": "FAIL_CLOSED"}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
