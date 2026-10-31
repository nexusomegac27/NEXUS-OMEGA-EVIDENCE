#!/usr/bin/env python3
"""Frozen black-box oracle for the isolated publication readback preflight candidate."""
import base64
import copy
import hashlib
import json
import subprocess
import sys


def source(path, data):
    return {"path": path, "status": "added", "content_b64": base64.b64encode(data).decode(),
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def fixture():
    main = "a" * 40
    parent = "b" * 40
    number = 239
    return {"schema_version": "1", "main_commit": main, "parent_commit": parent,
            "pr": {"number": number, "merged": True, "merge_commit": main,
                   "base_commit": parent, "head_commit": "c" * 40},
            "declared_changed_files": 2,
            "changed_files": [source("research/r16/alpha/a.txt", b"alpha\n"),
                              source("research/r16/alpha/b.txt", b"beta\r\n")],
            "declared_checks": 2,
            "ci_checks": [{"name": "validate", "conclusion": "success"},
                          {"name": "security", "conclusion": "success"}],
            "receipt": {"id": 6542955861, "actor": "nexusomegac27",
                        "body": ("ACTUAL_MAIN_READBACK=" + main + "\nACTUAL_MAIN_PARENT=" + parent
                                 + "\nPR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/239"
                                 + "\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n")}}


def run(script, obj=None, raw=None):
    if raw is None:
        raw = json.dumps(obj, sort_keys=True)
    p = subprocess.run([sys.executable, script], input=raw, text=True,
                       capture_output=True, timeout=10)
    if not p.stdout.strip():
        raise AssertionError("missing_output:" + p.stderr[:100])
    return p.returncode, json.loads(p.stdout)


def main(script):
    tests = 0
    def check(condition, label):
        nonlocal tests
        tests += 1
        if not condition:
            raise AssertionError(label)
    valid = fixture()
    rc, result = run(script, valid)
    check(rc == 0 and result["status"] == "LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT", "positive")
    check(result["local_file_matches"] == 2 and result["declared_changed_files"] == 2, "both_files")
    check(result["project_full_readback_rate"] == "NOT_COMPUTABLE", "no_project_promotion")
    check(result["receipt_actor_authenticated"] is False, "actor_not_authenticated")
    check(result["api_transport_authenticated"] is False, "api_not_authenticated")
    mutations = [
        ("missing_file", lambda x: x["changed_files"].pop()),
        ("wrong_sha256", lambda x: x["changed_files"][0].update(sha256="f" * 64)),
        ("wrong_git_blob", lambda x: x["changed_files"][0].update(git_blob="f" * 40)),
        ("wrong_byte_count", lambda x: x["changed_files"][0].update(bytes=100)),
        ("duplicate_path", lambda x: x["changed_files"][1].update(path=x["changed_files"][0]["path"])),
        ("path_traversal", lambda x: x["changed_files"][1].update(path="research/../secret")),
        ("wrong_main", lambda x: x.update(main_commit="d" * 40)),
        ("wrong_parent", lambda x: x.update(parent_commit="d" * 40)),
        ("unmerged", lambda x: x["pr"].update(merged=False)),
        ("receipt_wrong_commit", lambda x: x["receipt"].update(body=x["receipt"]["body"].replace("a"*40, "d"*40))),
        ("receipt_wrong_actor", lambda x: x["receipt"].update(actor="external-expert")),
        ("missing_ci", lambda x: x["ci_checks"].pop()),
        ("failed_ci", lambda x: x["ci_checks"][0].update(conclusion="failure")),
        ("claim_promotion", lambda x: x["receipt"].update(body=x["receipt"]["body"].replace("C1_DESCRIPTIVE_ONLY", "C2_VALIDATED"))),
        ("invalid_base64", lambda x: x["changed_files"][0].update(content_b64="%%%")),
    ]
    for label, mutate in mutations:
        x = copy.deepcopy(valid)
        mutate(x)
        rc, r = run(script, x)
        check(rc == 2 and r["status"] == "FAIL_CLOSED", label)
    for label, raw in [
        ("duplicate_json_key", '{"schema_version":"1","schema_version":"1"}'),
        ("nonfinite_json", '{"schema_version":"1","x":NaN}'),
        ("malformed_json", '{broken'),
    ]:
        rc, r = run(script, raw=raw)
        check(rc == 2 and r["status"] == "FAIL_CLOSED", label)
    print(json.dumps({"oracle": "FROZEN_PUBLICATION_READBACK_ORACLE_V1",
                      "tests": tests, "passed": tests}, sort_keys=True))

if __name__ == "__main__":
    main(sys.argv[1])
