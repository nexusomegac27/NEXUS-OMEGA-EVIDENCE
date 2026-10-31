#!/usr/bin/env python3
"""Independent subprocess oracle: exclusions without authenticated proof must not yield rates.
Frozen before the additive candidate; neither imports nor edits the candidate.
"""
import json
import subprocess
import sys

SOURCE = {"commit": "a"*40, "git_blob": "b"*40, "sha256": "c"*64,
          "bytes": 10, "path": "research/r16/source.txt"}
BASE = {"kind": "HANDOFF_ATTEMPT", "scope": "PUBLIC_ROUTINE_AUTHORIZED_ACCESSIBLE",
        "source": SOURCE, "evidence_ref": "https://github.com/example/receipt/1",
        "result": "SUCCESS", "manual_restart": False, "sender_actor": "owner",
        "receiver_actor": "reviewer", "receiver_ack": "VERIFIED", "readback": "COMPLETE"}

def event(identifier, **changes):
    return dict(BASE, event_id=identifier, **changes)

def run(script, events=None, raw=None):
    if raw is None:
        raw = json.dumps({"schema_version": "1", "events": events})
    p = subprocess.run([sys.executable, script], input=raw, text=True,
                       capture_output=True, timeout=10)
    if not p.stdout.strip():
        raise AssertionError("missing_stdout:" + p.stderr[:200])
    return p.returncode, json.loads(p.stdout)

def main(script):
    tests = 0
    def check(condition, label):
        nonlocal tests
        tests += 1
        if not condition:
            raise AssertionError(label)
    ok = event("success")
    failed = event("failed", result="FAILURE")
    excluded = event("excluded", scope="OUT_OF_SCOPE", exclusion_reason="NOT_AUTHORIZED")
    private = event("private", scope="OUT_OF_SCOPE", exclusion_reason="PRIVATE_INACCESSIBLE")
    pub_ok = event("pub-ok", kind="PUBLICATION", readback="COMPLETE")
    pub_bad = event("pub-bad", kind="PUBLICATION", readback="INCOMPLETE")
    rc, r = run(script, [ok, failed])
    check(rc == 0 and r["handoff"]["eligible_attempts"] == 2, "failed_attempt_in_denominator")
    check(r["handoff"]["rate_percent"] == 50, "no_exclusion_rate_preserved")
    check(r["operational_claim"].startswith("NOT_COMPUTABLE"), "operational_not_promoted")
    rc, r = run(script, [ok, excluded])
    check(rc == 0 and r["excluded_with_declared_reason"] == 1, "exclusion_recorded")
    check(r["handoff"]["rate_percent"] is None, "unverified_exclusion_must_not_yield_100_percent")
    check(r.get("exclusion_verification") == "NOT_INDEPENDENTLY_VERIFIED", "explicit_provenance_gap")
    rc, r = run(script, [ok, private])
    check(rc == 0 and r["handoff"]["rate_percent"] is None, "private_exclusion_unverified")
    rc, r = run(script, [pub_ok, pub_bad])
    check(rc == 0 and r["publication"]["rate_percent"] == 50, "publication_no_exclusion_rate")
    rc, r = run(script, [pub_ok, excluded])
    check(rc == 0 and r["publication"]["rate_percent"] is None, "publication_rate_exclusion_guard")
    rc, r = run(script, [ok, event("missing", source=None)])
    check(rc == 0 and r["handoff"]["rate_percent"] is None, "missing_source_blocks_rate")
    rc, r = run(script, [ok, event("success", result="FAILURE")])
    check(rc == 2 and r["status"] == "FAIL_CLOSED", "conflicting_duplicate")
    rc, r = run(script, raw='{"schema_version":"1","events":[],"events":[]}')
    check(rc == 2 and r["status"] == "FAIL_CLOSED", "duplicate_json_key")
    rc, r = run(script, raw='{"schema_version":"1","events":[],"x":NaN}')
    check(rc == 2 and r["status"] == "FAIL_CLOSED", "nonfinite_json")
    rc, r = run(script, [ok, ok])
    check(rc == 0 and r["handoff"]["eligible_attempts"] == 1, "identical_duplicate_dedup")
    print(json.dumps({"oracle":"FROZEN_EXCLUSION_RATE_ORACLE_V1", "tests":tests,"passed":tests}))

if __name__ == "__main__":
    main(sys.argv[1])
