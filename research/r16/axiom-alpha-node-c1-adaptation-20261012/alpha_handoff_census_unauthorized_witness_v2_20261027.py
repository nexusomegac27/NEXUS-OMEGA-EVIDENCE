#!/usr/bin/env python3
"""Additive C1 witness: flag caller-reported unauthorized published handoffs.

Does NOT authenticate caller events, assert a real-world incident, or verify zero
unauthorized writes. The immutable V1 census arithmetic remains unchanged.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE / "alpha_handoff_census_gate_v1_20261027.py"
BASE_SHA256 = "9c324f5805d5a64b686238d9c2f6145f966f963b575858645acadaefbf6a95f8"


def main():
    try:
        if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA256:
            raise ValueError("PINNED_BASELINE_HASH_MISMATCH")
        spec = importlib.util.spec_from_file_location("pinned_handoff_census_v1", BASE)
        baseline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(baseline)
        raw = sys.stdin.buffer.read(baseline.MAX_BYTES + 1)
        if len(raw) > baseline.MAX_BYTES:
            raise ValueError("INPUT_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=baseline.unique_pairs,
                          parse_constant=baseline.nonfinite)
        result = baseline.audit(data)
        unauthorized_ids = sorted(e["id"] for e in data["events"]
                                  if e["published"] and not e["authorized"])
        result.update({
            "caller_reported_unauthorized_published_ids": unauthorized_ids,
            "caller_reported_unauthorized_published_count": len(unauthorized_ids),
            "security_signal": ("CALLER_REPORTED_UNAUTHORIZED_PUBLICATION"
                                if unauthorized_ids else "NO_CALLER_REPORTED_UNAUTHORIZED_PUBLICATION"),
            "zero_unauthorized_writes_verified": False,
        })
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
