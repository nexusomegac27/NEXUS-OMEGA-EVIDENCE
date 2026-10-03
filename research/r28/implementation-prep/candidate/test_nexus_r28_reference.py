import tempfile
import unittest
from pathlib import Path

import nexus_r28_reference as n

class R28ReferenceTests(unittest.TestCase):
    def test_capability_bundle_passes(self):
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "bundle"
            r = n.issue_capability_challenge(b, "AXIOM", seed="fixture")
            self.assertEqual(r["status"], "PASS")

    def test_tampered_payload_fails(self):
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "bundle"
            n.issue_capability_challenge(b, "AXIOM", seed="fixture")
            (b / "payload.bin").write_bytes((b / "payload.bin").read_bytes() + b"x")
            self.assertEqual(n.verify_capability_bundle(b)["status"], "FAIL")

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "bundle"
            n.issue_capability_challenge(b, "AXIOM", seed="fixture")
            (b / "challenge.txt").unlink()
            self.assertEqual(n.verify_capability_bundle(b)["status"], "FAIL")

    def test_capability_receipt_passes(self):
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "bundle"
            n.issue_capability_challenge(b, "AXIOM", seed="fixture")
            receipt = n.make_capability_receipt(b, "TEST_AGENT", "python-local", "AXIOM")
            self.assertEqual(n.verify_capability_receipt(b, receipt)["status"], "PASS")

    def test_wrong_challenge_receipt_fails(self):
        with tempfile.TemporaryDirectory() as td:
            b = Path(td) / "bundle"
            n.issue_capability_challenge(b, "AXIOM", seed="fixture")
            receipt = n.make_capability_receipt(b, "TEST_AGENT", "python-local", "AXIOM")
            receipt["challenge_id"] = "NEXUS-WRONG"
            self.assertEqual(n.verify_capability_receipt(b, receipt)["status"], "FAIL")

    def test_local_handshake_passes(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / "source.bin"
            src.write_bytes(b"nexus-r28-fixture")
            tr = n.LocalDirectoryTransport(td / "transport")
            result = n.local_handshake(src, tr, td / "work", "obj-r28-test", "AXIOM", "RECEIVER")
            self.assertEqual(result["sender_verification"]["status"], "PASS")
            self.assertFalse(result["real_online_handshake"])

    def test_modified_received_artifact_fails(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / "source.bin"
            src.write_bytes(b"original")
            manifest = n.build_handshake_manifest(
                src, "obj-r28-test", "AXIOM", challenge_id="NEXUS-HS-FIXED"
            )
            recv = td / "recv.bin"
            recv.write_bytes(b"modified")
            receipt = n.receive_artifact(recv, manifest, "RECEIVER")
            self.assertEqual(receipt["status"], "FAIL")
            self.assertEqual(n.verify_handshake_receipt(manifest, receipt)["status"], "FAIL")

    def test_manifest_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / "source.bin"
            src.write_bytes(b"original")
            manifest = n.build_handshake_manifest(src, "obj-r28-test", "AXIOM")
            manifest["size_bytes"] += 1
            self.assertFalse(n.validate_handshake_manifest(manifest))

if __name__ == "__main__":
    unittest.main()
