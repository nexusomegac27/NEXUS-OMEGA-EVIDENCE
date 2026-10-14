import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from nexus_artifact_triage_v01 import triage, Denied, _kind

class ArtifactTriage(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p=Path(self.tmp.name)
        self.f=self.p/"app.bin"
        self.f.write_bytes(b"\x7fELF\x02"+b"\x00"*20)
        self.case="NEXUS_TEST_ARTIFACT_01"
    def good(self): return triage(self.p,self.f,self.case)
    def test_01_elf_static_detection(self):self.assertEqual(self.good()["artifact_type"],"ELF")
    def test_02_no_execution(self):self.assertFalse(self.good()["execution_performed"])
    def test_03_no_authorization(self):self.assertEqual(self.good()["authority"],"NONE_NOT_AN_AUTHORIZATION_GATE")
    def test_04_sha_source_byte_change(self):
        a=self.good()["source_sha256"];self.f.write_bytes(b"\x7fELF\x02\x01");self.assertNotEqual(a,self.good()["source_sha256"])
    def test_05_reject_empty(self):self.f.write_bytes(b"");self.assertRaises(Denied,self.good)
    def test_06_reject_outside_root(self):
        with tempfile.TemporaryDirectory() as other:
            f=Path(other)/"out";f.write_bytes(b"abc")
            with self.assertRaisesRegex(Denied,"OUTSIDE"):triage(self.p,f,self.case)
    def test_07_reject_symlink(self):
        link=self.p/"link";link.symlink_to(self.f)
        with self.assertRaisesRegex(Denied,"SYMLINK"):triage(self.p,link,self.case)
    def test_08_reject_traversal(self):
        with tempfile.TemporaryDirectory() as other:
            f=Path(other)/"out";f.write_bytes(b"abc")
            with self.assertRaises(Denied):triage(self.p,self.p/".."/Path(other).name/"out",self.case)
    def test_09_reject_invalid_case_id(self):
        with self.assertRaisesRegex(Denied,"CASE_ID"):triage(self.p,self.f,"rm -rf /")
    def test_10_unknown_data_not_source_claim(self):
        self.f.write_bytes(b"simple text")
        self.assertEqual(self.good()["artifact_type"],"UNCLASSIFIED_STATIC_BYTES")
        self.assertIn("NOT_BEHAVIOR_VERIFIED",self.good()["claim"])
    def test_11_wasm_magic(self):self.assertEqual(_kind(b"\0asm\x01\0\0\0","a.wasm"),"WASM")
    def test_12_mz_not_proven_pe(self):self.assertEqual(_kind(b"MZ\x00\x00","a.exe"),"PE_CANDIDATE_MZ_ONLY")
    def test_13_valid_zip_no_extraction(self):
        with zipfile.ZipFile(self.f,"w") as z:z.writestr("safe/file.txt",b"safe")
        r=self.good();self.assertEqual(r["artifact_type"],"ZIP");self.assertFalse(r["zip_summary"]["entries_extracted"])
    def test_14_zip_traversal(self):
        with zipfile.ZipFile(self.f,"w") as z:z.writestr("../outside",b"evil")
        with self.assertRaisesRegex(Denied,"ZIP_PATH"):self.good()
    def test_15_zip_duplicate(self):
        with zipfile.ZipFile(self.f,"w") as z:
            z.writestr("a",b"x");z.writestr("a",b"y")
        with self.assertRaisesRegex(Denied,"ZIP_PATH"):self.good()
    def test_16_zip_windows_drive(self):
        with zipfile.ZipFile(self.f,"w") as z:z.writestr("C:/Windows/file",b"x")
        with self.assertRaisesRegex(Denied,"ZIP_PATH"):self.good()
    def test_17_zip_symlink(self):
        with zipfile.ZipFile(self.f,"w") as z:
            info=zipfile.ZipInfo("link");info.create_system=3;info.external_attr=(0o120777<<16)
            z.writestr(info,"../../etc/passwd")
        with self.assertRaisesRegex(Denied,"ZIP_UNSAFE"):self.good()
    def test_18_zip_bomb_ratio(self):
        with zipfile.ZipFile(self.f,"w",compression=zipfile.ZIP_DEFLATED) as z:z.writestr("a.bin",b"A"*1000000)
        with self.assertRaisesRegex(Denied,"ZIP_COMPRESSION_RATIO"):self.good()
    def test_19_invalid_zip_header(self):
        self.f.write_bytes(b"PK\x03\x04"+b"NO-CENTRAL-DIR")
        with self.assertRaisesRegex(Denied,"ZIP_MALFORMED"):self.good()
    def test_20_no_network_in_source(self):
        code=(ROOT/"src/nexus_artifact_triage_v01.py").read_text()
        self.assertNotIn("import socket",code);self.assertNotIn("import requests",code);self.assertNotIn("import urllib",code)
    def test_21_cli_json_output(self):
        p=subprocess.run([sys.executable,str(ROOT/"src/nexus_artifact_triage_v01.py"),"--root",str(self.p),"--artifact",str(self.f),"--case-id",self.case],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertIn('"source_sha256"',p.stdout)
    def test_22_cli_fail_closed(self):
        p=subprocess.run([sys.executable,str(ROOT/"src/nexus_artifact_triage_v01.py"),"--root",str(self.p),"--artifact",str(self.p/"missing"),"--case-id",self.case],capture_output=True,text=True)
        self.assertEqual(p.returncode,2)

if __name__=="__main__":unittest.main()
