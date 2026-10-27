#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 wrapper: malformed JSON delivery values cannot abort a whole sample.

Preserves v1 untouched and verifies its exact source bytes before delegation.
Caller assertions remain unverified; no project-wide automation rate is inferred.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

PINNED_V1_SHA256 = "118098276a26a12ca8a7c90c1692ce72eeafbe3702eb5e5ec89c5d81064115f9"
PINNED_V1_NAME = "alpha_handoff_eligibility_reducer_v1_20261025.py"


def _load_pinned_v1():
    path = Path(__file__).resolve().with_name(PINNED_V1_NAME)
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINNED_V1_SHA256:
        raise ValueError("PINNED_V1_SOURCE_DRIFT_FAIL_CLOSED")
    spec = importlib.util.spec_from_file_location("pinned_handoff_v1", path)
    if spec is None or spec.loader is None:
        raise ValueError("PINNED_V1_LOADER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduce_sample(rows):
    base = _load_pinned_v1()
    if not isinstance(rows, list):
        return base.reduce_sample(rows)
    normalized = []
    malformed_delivery_indices = set()
    for index, row in enumerate(rows):
        if isinstance(row, dict) and "delivery" in row and type(row["delivery"]) is not str:
            # JSON arrays/objects are unhashable in v1's set-membership test.
            # Normalize on a fresh shallow copy; never change original evidence.
            normalized.append({**row, "delivery": "INVALID_DELIVERY_TYPE"})
            malformed_delivery_indices.add(index)
        else:
            normalized.append(row)
    result = base.reduce_sample(normalized)
    for item in result["outcomes"]:
        if (item["index"] in malformed_delivery_indices
                and item["reason"] == "DELIVERY_STATE_UNKNOWN"):
            item["reason"] = "DELIVERY_STATE_INVALID_TYPE"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="JSON array of handoff records")
    args = parser.parse_args()
    with open(args.json_file, encoding="utf-8") as stream:
        data = json.load(stream)
    print(json.dumps(reduce_sample(data), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
