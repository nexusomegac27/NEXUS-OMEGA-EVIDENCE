#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent subprocess oracle for offline C1 receipt-file byte binding.

Frozen before candidate publication. No candidate import or live GitHub trust.
All fixtures synthetic; positive controls and one-defect negatives.
"""
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get("AXIOM_CANDIDATE", Path(__file__).with_name(
    "alpha_receipt_file_digest_witness_v1_20261028.py")))
P = "research/r16/axiom-alpha-node-c1-adaptation-20261012/"


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def fixture():
    files = [(P + "a.txt", b"alpha\n"), (P + "b.py", b"beta\x00\xff\n"), (P + "c.md", "café\n".encode())]
    return {"object": "NEXUS_OMEGA_ALPHA_RECEIPT_FILE_DIGEST_WITNESS_V1",
            "repository": "nexusomegac27/NEXUS-OMEGA-EVIDENCE", "commit_sha": "a" * 40,
            "commit_files": [{"filename": p, "status": "added", "sha": blob(data)} for p, data in files],
            "receipt_files": [{"path": p, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                               "git_blob_sha1": blob(data)} for p, data in files],
            "original_bytes_b64": [{"path": p, "content_base64": base64.b64encode(data).decode()} for p, data in files]}


def run(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj, ensure_ascii=False).encode()
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def reject(self, obj, code):
        p = run(obj)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors="replace"))
        self.assertIn(code.encode(), p.stderr)

    def test_positive_three_files(self):
        p = run(fixture())
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        out = json.loads(p.stdout)
        self.assertEqual(out["verified_files"], 3)
        self.assertEqual([x["path"] for x in out["files"]], sorted(x["path"] for x in fixture()["receipt_files"]))
        self.assertFalse(out["api_origin_authenticated"])
        self.assertFalse(out["live_main_verified"])
        self.assertFalse(out["receipt_authenticity_verified"])
        self.assertEqual(out["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def test_content_tamper(self):
        x = fixture(); x["original_bytes_b64"][0]["content_base64"] = base64.b64encode(b"ALPHA\n").decode()
        self.reject(x, "SHA256_MISMATCH")

    def test_declared_sha_tamper(self):
        x = fixture(); x["receipt_files"][0]["sha256"] = "0" * 64
        self.reject(x, "SHA256_MISMATCH")

    def test_declared_blob_tamper(self):
        x = fixture(); x["receipt_files"][0]["git_blob_sha1"] = "0" * 40
        self.reject(x, "GIT_BLOB_MISMATCH")

    def test_commit_blob_tamper(self):
        x = fixture(); x["commit_files"][0]["sha"] = "0" * 40
        self.reject(x, "GIT_BLOB_MISMATCH")

    def test_declared_length_tamper(self):
        x = fixture(); x["receipt_files"][0]["bytes"] += 1
        self.reject(x, "BYTE_COUNT_MISMATCH")

    def test_missing_original(self):
        x = fixture(); x["original_bytes_b64"].pop()
        self.reject(x, "FILE_SET_MISMATCH")

    def test_duplicate_original(self):
        x = fixture(); x["original_bytes_b64"].append(copy.deepcopy(x["original_bytes_b64"][0]))
        self.reject(x, "DUPLICATE_ORIGINAL_PATH")

    def test_status_modified(self):
        x = fixture(); x["commit_files"][0]["status"] = "modified"
        self.reject(x, "UNEXPECTED_COMMIT_STATUS")

    def test_noncanonical_base64(self):
        x = fixture(); x["original_bytes_b64"][0]["content_base64"] = "YWxwaGEK="
        self.reject(x, "INVALID_BASE64")

    def test_path_traversal(self):
        x = fixture(); x["receipt_files"][0]["path"] = "../bad"
        self.reject(x, "INVALID_PATH")

    def test_extra_file(self):
        x = fixture(); x["commit_files"].pop()
        self.reject(x, "FILE_SET_MISMATCH")

    def test_duplicate_json_key(self):
        self.reject(b'{"object":1,"object":2}', "DUPLICATE_JSON_KEY")

    def test_nonfinite_json(self):
        self.reject(b'{"junk":NaN}', "NONFINITE_JSON")

    def test_oversized_input(self):
        self.reject(b" " * 2_097_153, "INPUT_TOO_LARGE")

    def test_invalid_commit(self):
        x = fixture(); x["commit_sha"] = "not-a-sha"
        self.reject(x, "INVALID_SHA")


if __name__ == "__main__":
    unittest.main()
