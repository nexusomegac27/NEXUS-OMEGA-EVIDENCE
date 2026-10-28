#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent POSIX Git fixture evaluator. Frozen before candidate publication."""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / 'steward_exec_mode_witness_v1.py'


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL)


def fixture(git_exec, worktree_exec):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    p = root / 'scripts' / 'tool.sh'
    p.parent.mkdir()
    p.write_bytes(b'#!/bin/sh\nexit 0\n')
    p.chmod(0o755 if git_exec else 0o644)
    git(root, 'init', '-q')
    git(root, 'add', '.')
    git(root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'mode fixture')
    row = git(root, 'ls-tree', '-r', '-l', 'HEAD').decode().strip()
    header, path = row.split('\t', 1)
    mode, kind, oid, size = header.split()
    p.chmod(0o755 if worktree_exec else 0o644)
    return tmp, root, [(path, mode, kind, oid, int(size))]


def witness():
    spec = importlib.util.spec_from_file_location('isolated_mode_witness', CANDIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check


@unittest.skipUnless(os.name == 'posix', 'POSIX fixture only')
class IndependentModeEvaluator(unittest.TestCase):
    def run_case(self, ge, we):
        tmp, root, rows = fixture(ge, we)
        self.addCleanup(tmp.cleanup)
        return root, rows, witness()(root, rows)

    def test_01_git_tree_records_executable(self):
        _, rows, _ = self.run_case(True, True)
        self.assertEqual(rows[0][1], '100755')

    def test_02_positive_executable(self):
        self.assertEqual(self.run_case(True, True)[2], [])

    def test_03_positive_nonexecutable(self):
        self.assertEqual(self.run_case(False, False)[2], [])

    def test_04_negative_removed_executable(self):
        self.assertEqual(self.run_case(True, False)[2][0]['code'], 'GIT_WORKTREE_EXEC_MODE_MISMATCH')

    def test_05_negative_added_executable(self):
        self.assertEqual(self.run_case(False, True)[2][0]['code'], 'GIT_WORKTREE_EXEC_MODE_MISMATCH')

    def test_06_source_bytes_still_match_blob(self):
        root, rows, findings = self.run_case(True, False)
        b = (root / rows[0][0]).read_bytes()
        self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), rows[0][3])
        self.assertEqual(len(b), rows[0][4])
        self.assertEqual(len(findings), 1)

    def test_07_symlink_parent_not_assessed(self):
        tmp, root, rows = fixture(True, True)
        self.addCleanup(tmp.cleanup)
        import shutil
        outside = root / 'outside'
        outside.mkdir()
        (outside / 'tool.sh').write_bytes(b'#!/bin/sh\nexit 0\n')
        shutil.rmtree(root / 'scripts')
        (root / 'scripts').symlink_to(outside, target_is_directory=True)
        self.assertEqual(witness()(root, rows)[0]['code'], 'UNSAFE_COMPONENT_NOT_ASSESSED')

    def test_08_traversal_not_assessed(self):
        root, rows, _ = self.run_case(True, True)
        self.assertEqual(witness()(root, [('../outside', *rows[0][1:])])[0]['code'], 'UNSAFE_COMPONENT_NOT_ASSESSED')


if __name__ == '__main__':
    unittest.main(verbosity=2)
