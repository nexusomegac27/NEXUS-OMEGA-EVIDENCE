#!/usr/bin/env python3
"""Separate frozen subprocess oracle for the isolated census candidate."""
import json
import subprocess
import sys

COMMIT = "a" * 40
BLOB = "b" * 40
SHA = "c" * 64
SRC = {"commit": COMMIT, "git_blob": BLOB, "sha256": SHA, "bytes": 7, "path": "research/r16/example.txt"}
BASE = {"kind": "HANDOFF_ATTEMPT", "scope": "PUBLIC_ROUTINE_AUTHORIZED_ACCESSIBLE", "source": SRC,
        "evidence_ref": "https://github.com/example/receipt/1", "result": "SUCCESS", "manual_restart": False,
        "sender_actor": "owner", "receiver_actor": "reviewer", "receiver_ack": "VERIFIED", "readback": "COMPLETE"}


def event(identifier, **changes):
    return dict(BASE, event_id=identifier, **changes)


def run(script, events=None, raw=None):
    if raw is None:
        raw = json.dumps({"schema_version": "1", "events": events})
    proc = subprocess.run([sys.executable, script], input=raw, text=True, capture_output=True, timeout=10)
    return proc.returncode, json.loads(proc.stdout)


def main(script):
    tests = 0
    def check(ok, label):
        nonlocal tests
        tests += 1
        if not ok:
            raise AssertionError(label)
    rc, out = run(script, [event("ok"), event("failed", result="FAILURE")])
    check(rc == 0 and out["handoff"]["eligible_attempts"] == 2, "failure_in_denominator")
    check(out["handoff"]["automated_with_structural_ack"] == 1 and out["handoff"]["rate_percent"] == 50, "rate")
    check(out["operational_claim"].startswith("NOT_COMPUTABLE"), "no_operational_claim")
    rc, out = run(script, [event("same"), event("same")])
    check(rc == 0 and out["handoff"]["eligible_attempts"] == 1 and out["duplicate_events"] == 1, "duplicate_dedup")
    rc, out = run(script, [event("same"), event("same", result="FAILURE")])
    check(rc == 2 and out["reason"] == "conflicting_event_id", "conflict_fail_closed")
    rc, out = run(script, [event("fake", receiver_actor="owner")])
    check(rc == 0 and out["handoff"]["automated_with_structural_ack"] == 0, "self_ack_denied")
    rc, out = run(script, [event("missing", source=None)])
    check(rc == 0 and out["unresolved"] == 1 and out["handoff"]["rate_percent"] is None, "missing_source_not_excluded")
    rc, out = run(script, [event("private", scope="OUT_OF_SCOPE", exclusion_reason="PRIVATE_INACCESSIBLE")])
    check(rc == 0 and out["excluded_with_declared_reason"] == 1 and out["handoff"]["eligible_attempts"] == 0, "private_not_success")
    rc, out = run(script, [event("noreadback", readback="INCOMPLETE")])
    check(rc == 0 and out["handoff"]["automated_with_structural_ack"] == 0, "no_readback_no_success")
    rc, out = run(script, [event("manual", manual_restart=True)])
    check(rc == 0 and out["handoff"]["automated_with_structural_ack"] == 0, "manual_not_automated")
    rc, out = run(script, [event("p", kind="PUBLICATION", readback="INCOMPLETE"), event("q", kind="PUBLICATION")])
    check(rc == 0 and out["publication"]["observed_published"] == 2 and out["publication"]["complete_readbacks"] == 1, "publication_failure_in_denominator")
    rc, out = run(script, [event("unknown", result="UNKNOWN")])
    check(rc == 0 and out["unresolved"] == 1 and out["handoff"]["rate_percent"] is None, "unknown_not_ignored")
    rc, out = run(script, raw='{"schema_version":"1","events":[],"events":[]}')
    check(rc == 2 and out["status"] == "FAIL_CLOSED", "duplicate_json_key")
    rc, out = run(script, raw='{"schema_version":"1","events":[],"x":NaN}')
    check(rc == 2 and out["status"] == "FAIL_CLOSED", "nonfinite_json")
    rc, out = run(script, [event("boolbytes", source=dict(SRC, bytes=True))])
    check(rc == 0 and out["unresolved"] == 1, "bool_not_integer_bytes")
    print(json.dumps({"oracle": "FROZEN_CENSUS_SUBPROCESS_V1", "tests": tests, "passed": tests}))


if __name__ == "__main__":
    main(sys.argv[1])
