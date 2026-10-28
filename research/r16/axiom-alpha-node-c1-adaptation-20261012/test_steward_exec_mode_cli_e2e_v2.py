#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen evaluator for isolated full CLI executable-bit consistency.

This suite must be committed before the patch constructor. It only uses
synthetic POSIX Git repositories, never the actual repository worktree.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / 'scripts/nexus_repository_steward.py'
CANDIDATE = HERE / 'steward_exec_mode_cli_patch_candidate_v2.py'
PINNED_SHA256 = '94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998'


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True)


def patch(source):
    spec = importlib.util.spec_from_file_location('isolated_mode_patch', CANDIDATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.patch_steward_source(source)


def fixture(tree_exec, observed_exec, source):
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name) / 'checkout'
    path = root / 'scripts' / 'tool.sh'
    path.parent.mkdir(parents=True)
    path.write_bytes(b'#!/bin/sh\nexit 0\n')
    path.chmod(0o755 if tree_exec else 0o644)
    contract = root / 'docs/architecture/REPOSITORY_STRUCTURE.json'
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps({'version': 'fixture', 'root_files': [],
        'root_directories': ['docs', 'scripts'], 'active_research_lanes': {}}))
    git(root, 'init', '-q')
    git(root, 'config', 'core.filemode', 'true')
    git(root, 'add', '.')
    git(root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-qm', 'fixture')
    expected_mode = '100755' if tree_exec else '100644'
    tree = git(root, 'ls-tree', 'HEAD', 'scripts/tool.sh').stdout.decode()
    assert tree.startswith(expected_mode + ' blob '), tree
    path.chmod(0o755 if observed_exec else 0o644)
    script = Path(temp.name) / 'isolated_steward.py'
    script.write_text(source, encoding='utf-8')
    run = subprocess.run([sys.executable, str(script), '--root', str(root),
                          '--fail-on-integrity'], capture_output=True, text=True)
    if run.returncode == 2:
        raise AssertionError('SOURCE_HOLD: ' + run.stderr)
    return temp, run.returncode, json.loads(run.stdout)


@unittest.skipUnless(os.name == 'posix', 'POSIX executable-bit semantics only')
class IndependentFullCLIEvaluator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = SOURCE.read_text(encoding='utf-8')
        assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == PINNED_SHA256

    def run_case(self, tree_exec, observed_exec, patched=False, source=None):
        src = source if source is not None else (patch(self.original) if patched else self.original)
        tmp, rc, report = fixture(tree_exec, observed_exec, src)
        self.addCleanup(tmp.cleanup)
        return rc, report

    def assert_clean(self, case):
        self.assertEqual((case[0], case[1]['integrity_error_count']), (0, 0))

    def assert_mode_fault(self, case):
        rc, report = case
        self.assertEqual(rc, 1)
        self.assertIn('GIT_WORKTREE_EXEC_MODE_MISMATCH',
                      {f['code'] for f in report['findings']})

    def test_01_source_pin(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), PINNED_SHA256)

    def test_02_baseline_exec_positive(self):
        self.assert_clean(self.run_case(True, True))

    def test_03_baseline_nonexec_positive(self):
        self.assert_clean(self.run_case(False, False))

    def test_04_baseline_removed_exec_false_accept(self):
        self.assert_clean(self.run_case(True, False))

    def test_05_baseline_added_exec_false_accept(self):
        self.assert_clean(self.run_case(False, True))

    def test_06_candidate_exec_positive(self):
        self.assert_clean(self.run_case(True, True, patched=True))

    def test_07_candidate_nonexec_positive(self):
        self.assert_clean(self.run_case(False, False, patched=True))

    def test_08_candidate_removed_exec_rejected(self):
        self.assert_mode_fault(self.run_case(True, False, patched=True))

    def test_09_candidate_added_exec_rejected(self):
        self.assert_mode_fault(self.run_case(False, True, patched=True))

    def test_10_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'PINNED_SOURCE_DRIFT'):
            patch(self.original + '\n# mutated')

    def test_11_original_not_modified(self):
        before = SOURCE.read_bytes()
        patch(self.original)
        self.assertEqual(SOURCE.read_bytes(), before)

    def test_12_positive_output_parity(self):
        for mode in (False, True):
            baseline = self.run_case(mode, mode)
            candidate = self.run_case(mode, mode, patched=True)
            baseline[1].pop('source_commit')
            candidate[1].pop('source_commit')
            self.assertEqual(baseline, candidate)


if __name__ == '__main__':
    unittest.main(verbosity=2)
