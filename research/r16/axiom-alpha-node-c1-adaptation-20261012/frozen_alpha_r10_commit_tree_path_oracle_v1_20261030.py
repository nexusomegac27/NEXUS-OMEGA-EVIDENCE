#!/usr/bin/env python3
"""Independent black-box subprocess regression for R10 C1 commit/path gate."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

COMMIT = "dab7c59070d67e7e2a244bd6d05db9a4d37460e3"
ROOT = "d743c5d926d469470afa0d7331d5c56b8262d56c"
BLOB = "4e31f92be1f673f49a2c27e570b5849e754cca78"
SHA = "60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5"
PATH = "research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt"


def run(candidate, source, proof, overrides=None, raw_proof=None):
    overrides = overrides or {}
    with tempfile.TemporaryDirectory() as temp:
        src = Path(temp, "source.bin")
        src.write_bytes(source)
        pf = Path(temp, "proof.json")
        pf.write_bytes(raw_proof if raw_proof is not None else json.dumps(proof, ensure_ascii=False).encode())
        pins = {"expected-commit": COMMIT, "expected-root-tree": ROOT,
                "expected-source-sha256": SHA, "expected-blob": BLOB,
                "expected-bytes": "4380", "expected-path": PATH}
        pins.update(overrides)
        argv = [sys.executable, "-S", str(candidate), "--source", str(src), "--proof", str(pf)]
        for k, v in pins.items():
            argv += ["--" + k, str(v)]
        result = subprocess.run(argv, capture_output=True, text=True, timeout=8)
        try:
            out = json.loads(result.stdout)
        except json.JSONDecodeError:
            out = {}
        return result.returncode, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("source")
    ap.add_argument("proof")
    args = ap.parse_args()
    candidate = Path(args.candidate).resolve()
    source = Path(args.source).read_bytes()
    proof = json.loads(Path(args.proof).read_text())
    if (len(source), hashlib.sha256(source).hexdigest(),
        hashlib.sha1(b"blob " + str(len(source)).encode() + b"\0" + source).hexdigest()) != (4380, SHA, BLOB):
        raise SystemExit("INDEPENDENT_SOURCE_PRECONDITION_FAILED")
    if proof["commit_sha"] != COMMIT or proof["root_tree_sha"] != ROOT:
        raise SystemExit("INDEPENDENT_PROOF_PRECONDITION_FAILED")
    cases = []
    cases.append(("real_source_positive", source, proof, {}, None, True))
    mutated = bytearray(source); mutated[99] ^= 1
    cases.append(("same_length_source_mutation", bytes(mutated), proof, {}, None, False))
    cases.append(("source_truncated", source[:-1], proof, {}, None, False))
    cases.append(("source_appended", source + b"X", proof, {}, None, False))
    for key, val in [("expected-source-sha256", "0" * 64), ("expected-blob", "0" * 40),
                     ("expected-bytes", "4381"), ("expected-commit", "0" * 40),
                     ("expected-root-tree", "0" * 40), ("expected-path", "research/r10/../returns/file.txt")]:
        cases.append(("bad_pin_" + key, source, proof, {key: val}, None, False))
    def mutate(name, fn):
        p = copy.deepcopy(proof); fn(p)
        cases.append((name, source, p, {}, None, False))
    mutate("path_mutation", lambda p: p["hops"][2]["entry"].update(path="other-topic"))
    mutate("tree_link_mutation", lambda p: p["hops"][3].update(parent_tree_sha="0" * 40))
    mutate("leaf_blob_mutation", lambda p: p["hops"][-1]["entry"].update(sha="0" * 40))
    mutate("leaf_size_mutation", lambda p: p["hops"][-1]["entry"].update(size=4379))
    mutate("leaf_mode_symlink", lambda p: p["hops"][-1]["entry"].update(mode="120000"))
    mutate("tree_truncated", lambda p: p["hops"][1].update(truncated=True))
    mutate("missing_hop", lambda p: p["hops"].pop(2))
    mutate("extra_hop", lambda p: p["hops"].append(copy.deepcopy(p["hops"][-1])))
    mutate("bad_directory_mode", lambda p: p["hops"][0]["entry"].update(mode="100644"))
    mutate("duplicate_hop_field", lambda p: p["hops"][0].update(rogue="claim"))
    cases.append(("duplicate_json_keys", source, proof, {}, b'{"commit_sha":"x","commit_sha":"y"}', False))
    cases.append(("nonfinite_json", source, proof, {}, b'{"commit_sha":NaN}', False))
    cases.append(("invalid_json", source, proof, {}, b'{not-json', False))
    results = []
    for name, src, pf, pins, raw, should_pass in cases:
        rc, out = run(candidate, src, pf, pins, raw)
        passed = (rc == 0 and out.get("source_bytes_sha256_git_blob") == "MATCH" and
                  out.get("independent_receiver_ack") == "NOT_ESTABLISHED" and
                  out.get("authenticated_github_actor") == "NOT_ESTABLISHED") if should_pass else (
                      rc != 0 and out.get("status") == "FAIL_CLOSED")
        results.append((name, passed))
    print(json.dumps({"tests": len(results), "passed": sum(ok for _, ok in results),
                      "failures": [name for name, ok in results if not ok]}, sort_keys=True))
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())
