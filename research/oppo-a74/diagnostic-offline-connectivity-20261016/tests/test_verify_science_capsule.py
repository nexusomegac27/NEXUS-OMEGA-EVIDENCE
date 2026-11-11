"""NEXUS OMEGA C1 offline scientific capsule adversarial fixtures.
No device, network or Hostinger access is used.
"""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reference"))
from verify_science_capsule import verify, CapsuleError

class VerifyScienceCapsuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.file = self.root / "original.bin"
        self.data = b"nexus-science-test-only-not-device-data"
        self.file.write_bytes(self.data)
        self.mf = self.root / "manifest.json"
        self.entry = {"relative_path":"original.bin","role":"SENSOR_ORIGINAL",
                      "privacy_class":"PRIVATE_ORIGINAL","bytes":len(self.data),
                      "sha256":hashlib.sha256(self.data).hexdigest()}
        self.write([self.entry])

    def write(self, entries, capsule_id="TEST_CAPSULE_A"):
        self.mf.write_text(json.dumps({"schema":"nexus-science-capsule/v1",
                                       "capsule_id":capsule_id,"files":entries}))

    def test_01_source_matches(self):
        self.assertEqual(verify(self.root,self.mf)["count"],1)
    def test_02_no_receiver_ack_promotion(self):
        self.assertEqual(verify(self.root,self.mf)["receiver_ack"],"NOT_ESTABLISHED")
    def test_03_no_remote_promotion(self):
        self.assertEqual(verify(self.root,self.mf)["remote_readback"],"NOT_ESTABLISHED")
    def test_04_no_science_promotion(self):
        self.assertEqual(verify(self.root,self.mf)["scientific_validation"],"NOT_ESTABLISHED")
    def test_05_tamper_rejected(self):
        self.file.write_bytes(self.data + b"X")
        with self.assertRaisesRegex(CapsuleError,"SOURCE_BYTE_MISMATCH"):verify(self.root,self.mf)
    def test_06_traversal_rejected(self):
        self.write([{**self.entry,"relative_path":"../outside"}])
        with self.assertRaisesRegex(CapsuleError,"TRAVERSAL"):verify(self.root,self.mf)
    def test_07_duplicate_path_rejected(self):
        self.write([self.entry,self.entry])
        with self.assertRaisesRegex(CapsuleError,"DUPLICATE_FILE_PATH"):verify(self.root,self.mf)
    def test_08_private_in_public_rejected(self):
        with self.assertRaisesRegex(CapsuleError,"PRIVATE_FILE_IN_PUBLIC_CAPSULE"):verify(self.root,self.mf,public=True)
    def test_09_missing_source_rejected(self):
        self.file.unlink()
        with self.assertRaisesRegex(CapsuleError,"ORIGINAL_BYTES_MISSING"):verify(self.root,self.mf)
    def test_10_symlink_rejected(self):
        (self.root/"alias").symlink_to(self.file)
        self.write([{**self.entry,"relative_path":"alias"}])
        with self.assertRaisesRegex(CapsuleError,"SYMLINK_FORBIDDEN"):verify(self.root,self.mf)
    def test_11_lfs_pointer_rejected(self):
        data=b"version https://git-lfs.github.com/spec/v1\n" + b"oid sha256:" + b"0"*64 + b"\nsize 42\n"
        self.file.write_bytes(data)
        self.write([{**self.entry,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}])
        with self.assertRaisesRegex(CapsuleError,"LFS_POINTER_NOT_ORIGINAL_BYTES"):verify(self.root,self.mf)
    def test_12_duplicate_json_key_rejected(self):
        self.mf.write_text('{"schema":"nexus-science-capsule/v1","schema":"forged","files":[]}')
        with self.assertRaisesRegex(CapsuleError,"DUPLICATE_JSON_KEY"):verify(self.root,self.mf)
    def test_13_manifest_self_hash_rejected(self):
        self.write([{**self.entry,"relative_path":"manifest.json"}])
        with self.assertRaisesRegex(CapsuleError,"MANIFEST_SELF_HASH_FORBIDDEN"):verify(self.root,self.mf)
    def test_14_missing_privacy_class_rejected(self):
        self.write([{**self.entry,"privacy_class":None}])
        with self.assertRaisesRegex(CapsuleError,"ROLE_OR_PRIVACY_INVALID"):verify(self.root,self.mf)

if __name__ == "__main__":
    unittest.main()
