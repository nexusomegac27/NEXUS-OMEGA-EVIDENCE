#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Research-only strict JSON entrypoint for the pinned handoff sample reducer V2.

Reject duplicate object keys *before* classification: last-wins parsing can turn
conflicting manual-reprompt or authorization evidence into apparent success.
No live inventory, actor authentication, network calls or project-wide metrics.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

PINNED_V2_NAME = "alpha_handoff_eligibility_reducer_v2_20261025.py"
PINNED_V2_SHA256 = "26addc7ca8252f86879b508c4d51cae33f5d9296496ae91d1191cdf53ed44057"


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            # Never echo untrusted field names or private values to diagnostics.
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _pinned_reducer():
    path = Path(__file__).resolve().with_name(PINNED_V2_NAME)
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINNED_V2_SHA256:
        raise ValueError("PINNED_V2_SOURCE_DRIFT_FAIL_CLOSED")
    spec = importlib.util.spec_from_file_location("pinned_handoff_v2", path)
    if spec is None or spec.loader is None:
        raise ValueError("PINNED_V2_LOADER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduce_json_text(text):
    if type(text) is not str:
        raise ValueError("INPUT_MUST_BE_JSON_TEXT")
    rows = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    return _pinned_reducer().reduce_sample(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="UTF-8 JSON array of caller-asserted handoffs")
    args = parser.parse_args()
    data = Path(args.json_file).read_text(encoding="utf-8")
    print(json.dumps(reduce_json_text(data), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
