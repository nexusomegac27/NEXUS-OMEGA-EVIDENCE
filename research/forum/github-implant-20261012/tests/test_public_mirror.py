#!/usr/bin/env python3
"""Offline contract tests for GitHub Implant mirror, including exclusion and nonoverwrite."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "mirror_public_git.py"

def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        assert run("git","init","-q",str(self.repo)).returncode == 0
        run("git","config","user.email","test@example.invalid",cwd=self.repo)
        run("git","config","user.name","Fixture",cwd=self.repo)
        (self.repo/"README.md").write_text("C1_DESCRIPTIVE_ONLY\n")
        (self.repo/"normal.txt").write_text("Original content\n")
        (self.repo/".env").write_text("TOKEN=do-not-mirror")
        (self.repo/"danger.txt").write_text("-----BEGIN OPENSSH PRIVATE KEY-----")
        assert run("git","add",".",cwd=self.repo).returncode == 0
        assert run("git","commit","-qm","fixture",cwd=self.repo).returncode == 0
        self.out = self.root/"out"
    def test_copies_verifiable_public_files(self):
        r=run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.out))
        self.assertEqual(r.returncode,0,r.stderr)
        m=json.loads((self.out/"manifest.json").read_text())
        self.assertEqual(m["file_count"],2)
        self.assertFalse(m["complete_unfiltered_mirror"])
        self.assertEqual(m["source_git_tracked_count"],4)
        self.assertEqual(hashlib.sha256((self.out/"README.md").read_bytes()).hexdigest(),next(x["sha256"] for x in m["files"] if x["path"]=="README.md"))
        self.assertFalse((self.out/".env").exists())
        self.assertFalse((self.out/"danger.txt").exists())
    def test_refuses_overwrite_and_mutation(self):
        r=run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.out))
        self.assertEqual(r.returncode,0)
        again=run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.out))
        self.assertEqual(again.returncode,2)
        (self.repo/"README.md").write_text("uncommitted\n")
        fail=run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.root/"new"))
        self.assertEqual(fail.returncode,2)
    def test_refuses_inside_source(self):
        r=run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.repo/"mirror"))
        self.assertEqual(r.returncode,2)
    def test_no_secret_content_in_manifest(self):
        run(sys.executable,str(SCRIPT),"--source",str(self.repo),"--output",str(self.out))
        m=(self.out/"manifest.json").read_text()
        self.assertNotIn("TOKEN=do-not-mirror",m)
        self.assertNotIn("PRIVATE KEY-----",m)

if __name__=="__main__":
    unittest.main()
