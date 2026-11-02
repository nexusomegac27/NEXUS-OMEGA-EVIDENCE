"""Frozen independent subprocess oracle for the research-only V9 Git blob guard.

Create/commit this file BEFORE the candidate; do not edit after candidate exists.
Expected outcomes derive from independent fixed fixtures, not target code.
"""
import base64
import hashlib
import json
import subprocess
import sys

COMMIT = "a" * 40
PATH = "research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen-fixture.json"
RAW = b'{"inventory":["a","b"],"coverage_complete":true}'
OTHER = b'{"inventory":["a"],"coverage_complete":true}'


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def envelope(raw=RAW):
    return {"source_b64": base64.b64encode(raw).decode(),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "source_commit": COMMIT, "source_path": PATH,
            "source_git_blob_sha1": blob(RAW)}


def run(target, data, args=None, raw_json=None):
    cmd = [sys.executable, target, "--trusted-commit", COMMIT,
           "--trusted-path", PATH, "--trusted-blob", blob(RAW)]
    if args:
        for k, v in args.items():
            cmd[cmd.index(k) + 1] = v
    proc = subprocess.run(cmd, input=(raw_json if raw_json is not None else
                          json.dumps(data).encode()), capture_output=True, timeout=5)
    if proc.returncode:
        return "CRASH"
    try:
        return json.loads(proc.stdout)["status"]
    except (ValueError, KeyError):
        return "INVALID_OUTPUT"


def main():
    target = sys.argv[1]
    good = envelope()
    fixtures = [
        ("positive_pinned_blob", good, None, None, True),
        ("coforged_bytes_and_sha", envelope(OTHER), None, None, False),
        ("coforged_blob_in_envelope", {**envelope(OTHER), "source_git_blob_sha1": blob(OTHER)}, None, None, False),
        ("missing_blob", {k:v for k,v in good.items() if k != "source_git_blob_sha1"}, None, None, False),
        ("wrong_commit", {**good, "source_commit": "b" * 40}, None, None, False),
        ("wrong_path", {**good, "source_path": "research/r16/wrong.json"}, None, None, False),
        ("wrong_sha256", {**good, "source_sha256": "0" * 64}, None, None, False),
        ("wrong_git_blob", {**good, "source_git_blob_sha1": "0" * 40}, None, None, False),
        ("wrong_b64", {**good, "source_b64": "!"}, None, None, False),
        ("empty_bytes", envelope(b""), None, None, False),
        ("unknown_extra_field", {**good, "coverage_complete": True}, None, None, False),
        ("missing_commit", {k:v for k,v in good.items() if k != "source_commit"}, None, None, False),
        ("invalid_trusted_blob", good, {"--trusted-blob": "z"*40}, None, False),
        ("invalid_trusted_path", good, {"--trusted-path": "../escape"}, None, False),
        ("duplicate_json_key", good, None, b'{"source_b64":"x","source_b64":"y"}', False),
        ("source_sha_type_bool", {**good, "source_sha256": True}, None, None, False),
    ]
    passed = 0
    for name, data, args, raw_json, expected in fixtures:
        status = run(target, data, args, raw_json)
        actual = status == "BOUND_C1_BYTES_ONLY"
        ok = actual == expected
        passed += ok
        print(json.dumps({"fixture": name, "expected": expected,
                          "observed": status, "pass": ok}, sort_keys=True))
    print(json.dumps({"passed": passed, "total": len(fixtures),
                      "result": "PASS" if passed == len(fixtures) else "FAIL"}, sort_keys=True))
    return 0 if passed == len(fixtures) else 1


if __name__ == "__main__":
    sys.exit(main())
