"""Independent predeclared offline oracle for Alpha V5. Freeze before candidate commit.

This oracle is a separate source file. It tests exact candidate behavior on
synthetic fixtures, not live GitHub transport or provider authenticity.
"""
import base64
import copy
import hashlib
import importlib.util
import json
import sys


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def record(commit, path, b):
    return {"commit": commit, "path": path,
            "content_b64": base64.b64encode(b).decode(), "github_blob_sha1": blob(b)}


def run(candidate_path):
    spec = importlib.util.spec_from_file_location("candidate", candidate_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    commit = "a" * 40
    files = [("research/r16/test/source_a.txt", b"source A\n"),
             ("research/r16/test/source_b.txt", b"source B\n")]
    manifest = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY", "prs": [{"merge_commit": commit,
        "files": [{"path": p, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                   "git_blob_sha1": blob(b)} for p, b in files]}]}
    raw = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    anchor = hashlib.sha256(raw).hexdigest()
    good = [record(commit, p, b) for p, b in files]
    cases = []
    cases.append(("positive_two_original_bytes", raw, good, anchor, "PASS"))
    cases.append(("positive_reordered_records", raw, good[::-1], anchor, "PASS"))
    tampered = copy.deepcopy(good)
    tampered[0]["content_b64"] = base64.b64encode(b"source X\n").decode()
    cases.append(("negative_one_byte_changed", raw, tampered, anchor, "FAIL_CLOSED"))
    coforged = copy.deepcopy(tampered)
    coforged[0]["github_blob_sha1"] = blob(b"source X\n")
    cases.append(("negative_payload_and_provider_blob_coforged", raw, coforged, anchor, "FAIL_CLOSED"))
    cases.append(("negative_missing_file", raw, good[:1], anchor, "FAIL_CLOSED"))
    cases.append(("negative_duplicate_file", raw, [good[0], good[0]], anchor, "FAIL_CLOSED"))
    wrong_commit = copy.deepcopy(good)
    wrong_commit[0]["commit"] = "b" * 40
    cases.append(("negative_wrong_immutable_commit", raw, wrong_commit, anchor, "FAIL_CLOSED"))
    invalid_b64 = copy.deepcopy(good)
    invalid_b64[0]["content_b64"] = "%%%"
    cases.append(("negative_invalid_base64", raw, invalid_b64, anchor, "FAIL_CLOSED"))
    forged_manifest = copy.deepcopy(manifest)
    forged_manifest["prs"][0]["files"][0]["sha256"] = hashlib.sha256(b"source X\n").hexdigest()
    forged_manifest["prs"][0]["files"][0]["git_blob_sha1"] = blob(b"source X\n")
    forged_raw = json.dumps(forged_manifest, sort_keys=True, separators=(",", ":")).encode()
    cases.append(("negative_manifest_and_payload_forged_anchor_fixed", forged_raw, coforged, anchor, "FAIL_CLOSED"))
    cases.append(("negative_unexpected_record", raw, good+[record(commit, "research/r16/test/x", b"x")], anchor, "FAIL_CLOSED"))
    cases.append(("falsifier_coforged_manifest_and_anchor", forged_raw, coforged,
                  hashlib.sha256(forged_raw).hexdigest(), "PASS"))
    out = []
    for name, manifest_bytes, records, trusted, expected in cases:
        result = mod.evaluate(manifest_bytes, records, trusted)
        out.append({"case": name, "expected": expected, "actual": result["status"],
                    "ok": result["status"] == expected})
    return out


if __name__ == "__main__":
    results = run(sys.argv[1])
    print(json.dumps({"tests": len(results), "passed": sum(r["ok"] for r in results),
                      "results": results}, indent=2))
    sys.exit(0 if all(r["ok"] for r in results) else 1)
