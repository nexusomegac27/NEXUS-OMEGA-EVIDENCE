#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 handoff census *sample* reducer. No network, writes, or authority.

Inputs are caller assertions; upstream independent source/receiver byte readback is
required. A complete project-wide denominator is NEVER inferred from a sample.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import re

ID = re.compile(r"[A-Za-z0-9._:-]{1,128}\Z")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
VALID_DELIVERY = {"RECEIVER_VERIFIED", "FAILED", "PENDING", "BRANCH_ONLY"}


def _valid_sha(v):
    return isinstance(v, str) and HEX64.fullmatch(v) is not None


def _valid_commit(v):
    return isinstance(v, str) and HEX40.fullmatch(v) is not None


def classify(row, duplicated=False):
    """Return (status, reason). Eligible failures remain in the denominator."""
    if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not ID.fullmatch(row["id"]):
        return "UNKNOWN", "INVALID_ID"
    if duplicated:
        return "UNKNOWN", "DUPLICATE_ID"
    for key in ("public", "routine", "authorized"):
        if type(row.get(key)) is not bool:
            return "UNKNOWN", "MISSING_OR_INVALID_SCOPE_" + key.upper()
    if not row["public"] or not row["routine"] or not row["authorized"]:
        return "EXCLUDED", "OUTSIDE_PUBLIC_ROUTINE_AUTHORIZED_SCOPE"
    if row.get("source_access") != "BYTE_VERIFIED":
        return "UNKNOWN", "SOURCE_NOT_BYTE_VERIFIED"
    if (row.get("source_readback") is not True or not _valid_sha(row.get("source_sha256"))
            or type(row.get("source_bytes")) is not int or row["source_bytes"] < 0
            or not _valid_commit(row.get("source_commit"))):
        return "UNKNOWN", "SOURCE_PROVENANCE_INCOMPLETE"
    if row.get("delivery") not in VALID_DELIVERY:
        return "ELIGIBLE_FAILED", "DELIVERY_STATE_UNKNOWN"
    if row["delivery"] != "RECEIVER_VERIFIED":
        return "ELIGIBLE_FAILED", "DELIVERY_" + row["delivery"]
    if (row.get("receiver_readback") is not True or not _valid_commit(row.get("receiver_commit"))
            or not _valid_sha(row.get("receiver_sha256"))
            or type(row.get("receiver_bytes")) is not int or row["receiver_bytes"] < 0):
        return "ELIGIBLE_FAILED", "RECEIVER_PROVENANCE_INCOMPLETE"
    if (row["source_sha256"] != row["receiver_sha256"]
            or row["source_bytes"] != row["receiver_bytes"]):
        return "ELIGIBLE_FAILED", "RECEIVER_SOURCE_MISMATCH"
    if row.get("manual_reprompt") is not False:
        return "ELIGIBLE_FAILED", "AUTOMATION_NOT_PROVEN"
    return "ELIGIBLE_AUTOMATED", "SOURCE_RECEIVER_MATCH_NO_REPROMPT_DECLARED"


def reduce_sample(rows):
    if not isinstance(rows, list):
        raise ValueError("INPUT_MUST_BE_LIST")
    ids = Counter(row.get("id") for row in rows if isinstance(row, dict)
                  and isinstance(row.get("id"), str))
    outcomes = []
    for idx, row in enumerate(rows):
        dup = isinstance(row, dict) and isinstance(row.get("id"), str) and ids[row["id"]] > 1
        status, reason = classify(row, dup)
        outcomes.append({"index": idx, "id": row.get("id") if isinstance(row, dict) else None,
                         "status": status, "reason": reason})
    denominator = sum(x["status"].startswith("ELIGIBLE_") for x in outcomes)
    numerator = sum(x["status"] == "ELIGIBLE_AUTOMATED" for x in outcomes)
    return {
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "measurement_scope": "CALLER_ASSERTED_SAMPLE_ONLY_NOT_INDEPENDENTLY_AUDITED",
        "project_handoff_automation_rate": "NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS",
        "sample_eligible_denominator": denominator,
        "sample_automated_numerator": numerator,
        "sample_rate_percent": round(100 * numerator / denominator, 2) if denominator else None,
        "unknown_or_unverified": sum(x["status"] == "UNKNOWN" for x in outcomes),
        "excluded_out_of_scope": sum(x["status"] == "EXCLUDED" for x in outcomes),
        "outcomes": outcomes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="JSON array of handoff records")
    args = parser.parse_args()
    with open(args.json_file, encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(reduce_sample(data), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
