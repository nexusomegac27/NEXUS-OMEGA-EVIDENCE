#!/usr/bin/env python3
"""Isolated C1 handoff-census arithmetic gate, not a GitHub authenticator.

This research scaffold consumes caller-supplied records only. Its conditional
fractions cannot establish the project-wide 90% / 100% targets or actor identity.
No network, file writes, runtime, or publication operations.
"""
import json
import re
import sys
from datetime import datetime

MAX_BYTES = 262144
MAX_EVENTS = 1000
OBJECT = "NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_V1"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
UTC = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z")
FIELDS = frozenset(("id", "timestamp_utc", "routine", "public", "authorized", "accessible",
                    "manual_nudge", "published", "source_sha256", "main_commit",
                    "source_readback", "test_readback", "main_readback", "receipt_readback"))
FLAGS = ("routine", "public", "authorized", "accessible", "manual_nudge",
         "published", "source_readback", "test_readback", "main_readback", "receipt_readback")


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def nonfinite(_):
    raise ValueError("NONFINITE_JSON")


def valid_hex(value, pattern):
    return type(value) is str and pattern.fullmatch(value) is not None


def parse_utc(value):
    if type(value) is not str or not UTC.fullmatch(value):
        raise ValueError("INVALID_UTC_TIMESTAMP")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("INVALID_UTC_TIMESTAMP") from exc


def audit(data):
    if type(data) is not dict or data.get("object") != OBJECT:
        raise ValueError("INVALID_OBJECT")
    if type(data.get("census_complete")) is not bool:
        raise ValueError("INVALID_CENSUS_COMPLETENESS")
    start = parse_utc(data.get("window_start_utc"))
    end = parse_utc(data.get("window_end_utc"))
    if end <= start:
        raise ValueError("INVALID_WINDOW_ORDER")
    events = data.get("events")
    if type(events) is not list or len(events) > MAX_EVENTS:
        raise ValueError("INVALID_EVENTS")
    seen = set()
    eligible = automated = published = full_readback = 0
    incomplete_ids = []
    for e in events:
        if type(e) is not dict or not set(e).issubset(FIELDS):
            raise ValueError("INVALID_EVENT_FIELDS")
        identifier = e.get("id")
        if (type(identifier) is not str or not 1 <= len(identifier) <= 128
                or identifier in seen):
            raise ValueError("INVALID_OR_DUPLICATE_EVENT_ID")
        seen.add(identifier)
        timestamp = parse_utc(e.get("timestamp_utc"))
        if not start <= timestamp < end:
            raise ValueError("EVENT_OUTSIDE_CENSUS_WINDOW")
        if any(type(e.get(k)) is not bool for k in FLAGS):
            raise ValueError("INVALID_EVENT_BOOLEAN")
        sha = e.get("source_sha256")
        commit = e.get("main_commit")
        if sha is not None and not valid_hex(sha, HEX64):
            raise ValueError("INVALID_SOURCE_HASH")
        if commit is not None and not valid_hex(commit, HEX40):
            raise ValueError("INVALID_MAIN_COMMIT")
        complete = (valid_hex(sha, HEX64) and valid_hex(commit, HEX40)
                    and all(e[k] for k in ("source_readback", "test_readback",
                                             "main_readback", "receipt_readback")))
        if e["published"]:
            published += 1
            if complete:
                full_readback += 1
            else:
                incomplete_ids.append(identifier)
        if all(e[k] for k in ("routine", "public", "authorized", "accessible")):
            eligible += 1
            if e["published"] and not e["manual_nudge"] and complete:
                automated += 1
    census_complete = data["census_complete"]
    status = ("NOT_COMPUTABLE_INCOMPLETE_CENSUS" if not census_complete else
              "NOT_COMPUTABLE_ZERO_DENOMINATOR" if not eligible else
              "CONDITIONAL_CALLER_SUPPLIED_RECORDS_ONLY")
    return {
        "state": status,
        "window_start_utc": data["window_start_utc"],
        "window_end_utc": data["window_end_utc"],
        "observed_events": len(events),
        "eligible_denominator_observed": eligible,
        "automated_numerator_observed": automated,
        "conditional_automation_rate": (automated / eligible if census_complete and eligible else None),
        "published_denominator_observed": published,
        "complete_readback_numerator_observed": full_readback,
        "conditional_readback_rate": (full_readback / published if census_complete and published else None),
        "incomplete_published_event_ids": sorted(incomplete_ids),
        "caller_records_authenticated": False,
        "project_90_percent_verified": False,
        "project_100_percent_readback_verified": False,
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("INPUT_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=nonfinite)
        print(json.dumps(audit(data), sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
