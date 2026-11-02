"""Independent predeclared Alpha V6 decode-budget oracle; synthetic offline fixtures.

Freeze before creating V6 candidate. Does not authenticate GitHub or claim E2E.
"""
import base64
import copy
import hashlib
import importlib.util
import json
import sys


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location("subject", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(path):
    subject = load(path)
    commit = "a" * 40
    payload = b"source A\n"
    path_a = "research/r16/test/a.txt"
    manifest = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY", "prs": [{
        "merge_commit": commit, "files": [{"path": path_a, "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(), "git_blob_sha1": blob(payload)}]}]}
    raw = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    anchor = hashlib.sha256(raw).hexdigest()
    good = {"commit": commit, "path": path_a,
            "content_b64": base64.b64encode(payload).decode(), "github_blob_sha1": blob(payload)}
    cases = [
        ("valid_source", raw, [good], anchor, "PASS"),
        ("corrupt_source", raw, [{**good, "content_b64": base64.b64encode(b"source X\n").decode()}], anchor, "FAIL_CLOSED"),
        ("missing_source", raw, [], anchor, "FAIL_CLOSED"),
        ("duplicate_source", raw, [good, good], anchor, "FAIL_CLOSED"),
        ("wrong_commit", raw, [{**good, "commit": "b" * 40}], anchor, "FAIL_CLOSED"),
        ("invalid_base64", raw, [{**good, "content_b64": "%%%"}], anchor, "FAIL_CLOSED"),
        ("wrong_anchor", raw, [good], "f" * 64, "FAIL_CLOSED"),
        ("noncanonical_base64", raw, [{**good, "content_b64": good["content_b64"] + "\n"}], anchor, "FAIL_CLOSED"),
        ("unexpected_source", raw, [{**good, "path": "research/r16/test/b.txt"}], anchor, "FAIL_CLOSED"),
        ("nonstring_b64", raw, [{**good, "content_b64": 1}], anchor, "FAIL_CLOSED"),
        ("coforged_anchor_falsifier", raw, [good], anchor, "PASS"),
    ]
    results = []
    for name, manifest_bytes, records, digest, expected in cases:
        try:
            actual = subject.evaluate(manifest_bytes, records, digest)["status"]
        except Exception as exc:
            actual = "EXCEPTION_" + type(exc).__name__
        results.append({"name": name, "expected": expected, "actual": actual,
                        "ok": actual == expected})
    huge = {**good, "content_b64": "A" * 1600000}
    original = subject.base64.b64decode
    decode_calls = [0]
    def counted(*args, **kwargs):
        decode_calls[0] += 1
        return original(*args, **kwargs)
    subject.base64.b64decode = counted
    try:
        outcome = subject.evaluate(raw, [huge], anchor)["status"]
    finally:
        subject.base64.b64decode = original
    results.append({"name": "oversized_base64_rejected_before_decode", "expected": "FAIL_CLOSED;calls=0",
                    "actual": outcome + ";calls=" + str(decode_calls[0]),
                    "ok": outcome == "FAIL_CLOSED" and decode_calls[0] == 0})
    return results


if __name__ == "__main__":
    results = run(sys.argv[1])
    print(json.dumps({"passed": sum(r["ok"] for r in results), "total": len(results),
                      "results": results}, indent=2))
    sys.exit(0 if all(r["ok"] for r in results) else 1)
