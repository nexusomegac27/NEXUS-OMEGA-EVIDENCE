"""Independent frozen subprocess oracle for isolated V10 GitHub contents readback.
Commit/pin this file before candidate; do not change after candidate exists.
Offline fixtures emulate REST payloads; they do not prove HTTPS/API authentication.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile

COMMIT = "a" * 40
PATH = "research/r16/axiom-alpha-node-c1-adaptation-20261012/fixture.json"
RAW = b'{"inventory":["a","b"],"coverage_complete":true}'
OTHER = b'{"inventory":["a"],"coverage_complete":true}'


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def envelope(raw=RAW):
    return {"source_b64": base64.b64encode(raw).decode("ascii"),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "source_commit": COMMIT, "source_path": PATH,
            "source_git_blob_sha1": blob(raw)}


def response(raw=RAW):
    return {"type": "file", "path": PATH, "size": len(raw),
            "sha": blob(raw), "encoding": "base64",
            "content": base64.b64encode(raw).decode("ascii")}


def evaluate(target, env, api, *, raw_env=None, raw_api=None, commit=COMMIT, path=PATH):
    with tempfile.TemporaryDirectory() as tmp:
        fp = os.path.join(tmp, "api.json")
        with open(fp, "wb") as out:
            out.write(raw_api if raw_api is not None else json.dumps(api).encode("utf-8"))
        cmd = [sys.executable, target, "--trusted-commit", commit,
               "--trusted-path", path, "--offline-fixture-test", "--fixture-response", fp]
        p = subprocess.run(cmd, input=(raw_env if raw_env is not None else json.dumps(env).encode("utf-8")),
                           capture_output=True, timeout=8)
        if p.returncode:
            return "CRASH"
        try:
            result = json.loads(p.stdout)
            return result["status"]
        except (ValueError, KeyError, TypeError):
            return "INVALID_OUTPUT"


def baseline_v9_accepts_joint_forgery(path):
    data = envelope(OTHER)
    cmd = [sys.executable, path, "--trusted-commit", COMMIT,
           "--trusted-path", PATH, "--trusted-blob", blob(OTHER)]
    p = subprocess.run(cmd, input=json.dumps(data).encode("utf-8"), capture_output=True, timeout=8)
    if p.returncode:
        return False
    try:
        return json.loads(p.stdout)["status"] == "BOUND_C1_BYTES_ONLY"
    except (ValueError, KeyError):
        return False


def main():
    if len(sys.argv) != 3:
        print("USAGE: evaluator V10_CANDIDATE V9_BASELINE", file=sys.stderr)
        return 2
    target, baseline = sys.argv[1:]
    good = envelope()
    api = response()
    cases = [
        ("positive_original", good, api, {}, True),
        ("coforged_source_sha_blob", envelope(OTHER), api, {}, False),
        ("wrong_commit", {**good, "source_commit": "b"*40}, api, {}, False),
        ("wrong_path", {**good, "source_path": "research/r16/wrong.json"}, api, {}, False),
        ("wrong_source_sha", {**good, "source_sha256": "0"*64}, api, {}, False),
        ("wrong_source_blob", {**good, "source_git_blob_sha1": "0"*40}, api, {}, False),
        ("invalid_source_b64", {**good, "source_b64": "!"}, api, {}, False),
        ("empty_source", envelope(b""), api, {}, False),
        ("missing_field", {k:v for k,v in good.items() if k != "source_commit"}, api, {}, False),
        ("extra_field", {**good, "auto_success": True}, api, {}, False),
        ("source_sha_boolean", {**good, "source_sha256": True}, api, {}, False),
        ("api_wrong_sha", good, {**api, "sha": "0"*40}, {}, False),
        ("api_wrong_path", good, {**api, "path": "wrong.json"}, {}, False),
        ("api_wrong_size", good, {**api, "size": len(RAW)+1}, {}, False),
        ("api_type_directory", good, {**api, "type": "dir"}, {}, False),
        ("api_encoding_utf8", good, {**api, "encoding": "utf-8"}, {}, False),
        ("api_bad_base64", good, {**api, "content": "!"}, {}, False),
        ("api_missing_content", good, {k:v for k,v in api.items() if k != "content"}, {}, False),
        ("api_size_boolean", good, {**api, "size": True}, {}, False),
        ("duplicate_api_key", good, api, {"raw_api": b'{"type":"file","type":"file"}'}, False),
        ("duplicate_envelope_key", good, api, {"raw_env": b'{"source_b64":"x","source_b64":"y"}'}, False),
        ("invalid_trusted_commit", good, api, {"commit": "z"*40}, False),
        ("invalid_trusted_path", good, api, {"path": "../escape"}, False),
        # Deliberate falsifier: jointly forge the *offline fixture* itself.
        # This MUST NOT be presented as authenticated GitHub provenance.
        ("falsifier_coforged_offline_api_fixture", envelope(OTHER), response(OTHER), {}, True),
    ]
    passed = 0
    for name, env, resp, opts, should_accept in cases:
        status = evaluate(target, env, resp, **opts)
        observed = status == "FIXTURE_BOUND_C1_BYTES_ONLY"
        ok = observed == should_accept and status not in ("CRASH", "INVALID_OUTPUT")
        passed += ok
        print(json.dumps({"fixture": name, "expected_accept": should_accept,
                          "observed": status, "pass": ok}, sort_keys=True))
    baseline_accepts = baseline_v9_accepts_joint_forgery(baseline)
    print(json.dumps({"baseline_v9_coforged_trusted_blob_accepted": baseline_accepts,
                      "expected": True, "pass": baseline_accepts}, sort_keys=True))
    passed += baseline_accepts
    total = len(cases)+1
    print(json.dumps({"passed": passed, "total": total,
                      "result": "PASS" if passed == total else "FAIL",
                      "offline_fixture_only": True}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
