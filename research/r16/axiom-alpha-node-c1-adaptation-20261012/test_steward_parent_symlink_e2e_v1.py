#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent full-CLI steward evaluator, synthetic Git fixtures only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / 'scripts/nexus_repository_steward.py'
CANDIDATE = HERE / 'steward_parent_symlink_e2e_patch_candidate_v1.py'
PIN = '94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998'


def run_git(root, *args):
    subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)


def patch(source):
    spec = importlib.util.spec_from_file_location('isolated_candidate', CANDIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.patch_steward_source(source)


def fixture(kind, source):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name) / 'checkout'
    p = root / 'research/r5/alpha/README.md'
    p.parent.mkdir(parents=True)
    p.write_bytes(b'# alpha fixture\n')
    contract = root / 'docs/architecture/REPOSITORY_STRUCTURE.json'
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({'version': 'fixture', 'root_files': [],
        'root_directories': ['docs', 'research'],
        'active_research_lanes': {'alpha': {'path': 'research/r5/alpha'}}}))
    run_git(root, 'init', '-q')
    run_git(root, 'add', '.')
    run_git(root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
            'commit', '-qm', 'fixture')
    outside = Path(tmp.name) / 'outside'
    outside.mkdir()
    (outside / 'README.md').write_bytes(b'# alpha fixture\n')
    if kind in ('parent', 'parent_changed'):
        if kind == 'parent_changed':
            (outside / 'README.md').write_bytes(b'changed outside\n')
        shutil.rmtree(p.parent)
        os.symlink(outside, p.parent, target_is_directory=True)
    elif kind == 'leaf':
        p.unlink()
        os.symlink(outside / 'README.md', p)
    elif kind == 'changed':
        p.write_bytes(b'changed inside\n')
    script = root / 'steward_under_test.py'
    script.write_text(source)
    proc = subprocess.run([sys.executable, str(script), '--root', str(root),
                           '--fail-on-integrity'], capture_output=True, text=True)
    if proc.returncode == 2:
        raise AssertionError(proc.stderr)
    return tmp, proc.returncode, json.loads(proc.stdout)


class IndependentE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = SOURCE.read_text()
        assert hashlib.sha256(cls.original.encode()).hexdigest() == PIN

    def check(self, kind='normal', patched=False):
        tmp, rc, report = fixture(kind, patch(self.original) if patched else self.original)
        self.addCleanup(tmp.cleanup)
        return rc, report

    def test_01_pinned_bytes(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), PIN)

    def test_02_baseline_positive(self):
        rc, r = self.check()
        self.assertEqual((rc, r['integrity_error_count']), (0, 0))

    def test_03_baseline_parent_symlink_false_accept(self):
        rc, r = self.check('parent')
        self.assertEqual((rc, r['integrity_error_count']), (0, 0))

    def test_04_candidate_positive(self):
        rc, r = self.check(patched=True)
        self.assertEqual((rc, r['integrity_error_count']), (0, 0))

    def test_05_candidate_parent_symlink_rejected(self):
        rc, r = self.check('parent', True)
        self.assertEqual(rc, 1)
        self.assertIn('UNSAFE_PATH_COMPONENT', {x['code'] for x in r['findings']})

    def test_06_candidate_changed_parent_symlink_rejected(self):
        rc, r = self.check('parent_changed', True)
        self.assertEqual(rc, 1)
        self.assertIn('UNSAFE_PATH_COMPONENT', {x['code'] for x in r['findings']})

    def test_07_candidate_leaf_symlink_rejected(self):
        rc, r = self.check('leaf', True)
        self.assertEqual(rc, 1)
        self.assertIn('TRACKED_FILE_NOT_PRESENT', {x['code'] for x in r['findings']})

    def test_08_candidate_changed_regular_file_rejected(self):
        rc, r = self.check('changed', True)
        self.assertEqual(rc, 1)
        self.assertIn('WORKTREE_GIT_BLOB_MISMATCH', {x['code'] for x in r['findings']})

    def test_09_no_source_mutation(self):
        before = SOURCE.read_bytes()
        patch(self.original)
        self.assertEqual(SOURCE.read_bytes(), before)

    def test_10_source_drift_fails_closed(self):
        with self.assertRaises(ValueError):
            patch(self.original + '\n# drift')

    def test_11_positive_parity(self):
        base_rc, base = self.check()
        patched_rc, patched = self.check(patched=True)
        base.pop('source_commit')
        patched.pop('source_commit')
        self.assertEqual((base_rc, base), (patched_rc, patched))


if __name__ == '__main__':
    unittest.main(verbosity=2)
