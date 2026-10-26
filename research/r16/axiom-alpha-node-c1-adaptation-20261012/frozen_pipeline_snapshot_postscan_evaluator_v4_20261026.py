#!/usr/bin/env python3
"""Frozen black-box V4 evaluation: post-inventory race on a pinned POSIX dir.

The test fixture is independent of the candidate's implementation. Baseline
acceptance is intentionally recorded, never relabeled as a positive control.
A separate evaluator file is pinned before any candidate commit.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BASE = HERE / 'alpha_pipeline_snapshot_fixity_budget_v3_20261026.py'
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_pipeline_snapshot_fixity_inventory_v4_20261026.py'))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FrozenPostscanEvaluator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'snapshot'
        self.root.mkdir()

    def seal(self, files):
        lines = []
        for name, data in sorted(files.items()):
            (self.root / name).write_bytes(data)
            lines.append(hashlib.sha256(data).hexdigest() + '  ' + name + '\n')
        (self.root / 'SHA256SUMS.txt').write_text(''.join(lines), encoding='ascii')

    def audit_with_injection(self, path, operation):
        module = load(path, 'frozen_' + str(id(self)))
        original = module.safe_open
        done = False

        def injected(fd, name):
            nonlocal done
            if name != 'SHA256SUMS.txt' and not done:
                done = True
                operation()
            return original(fd, name)

        module.safe_open = injected
        return module.audit(str(self.root))

    def deny(self, operation, message):
        with self.assertRaises((ValueError, OSError)) as caught:
            self.audit_with_injection(CANDIDATE, operation)
        self.assertIn(message, str(caught.exception))

    def test_01_baseline_accepts_postscan_unsealed_file(self):
        self.seal({'a': b'good'})
        result = self.audit_with_injection(BASE, lambda: (self.root / 'extra').write_bytes(b'x'))
        self.assertEqual(result['verified_files'], 1)
        self.assertTrue((self.root / 'extra').exists())

    def test_02_candidate_rejects_same_postscan_unsealed_file(self):
        self.seal({'a': b'good'})
        self.deny(lambda: (self.root / 'extra').write_bytes(b'x'), 'SNAPSHOT_INVENTORY_CHANGED_AFTER_HASH')

    def test_03_candidate_rejects_postscan_symlink(self):
        self.seal({'a': b'good'})
        outside = Path(self.temp.name) / 'outside'
        outside.write_bytes(b'other')
        self.deny(lambda: (self.root / 'extra').symlink_to(outside), 'SNAPSHOT_NONREGULAR_ENTRY')

    def test_04_baseline_accepts_removed_already_hashed_file(self):
        self.seal({'a': b'a', 'b': b'b'})
        # Remove a after it has been hashed but before b is opened.
        module = load(BASE, 'base_remove')
        original = module.safe_open
        def injected(fd, name):
            if name == 'b':
                (self.root / 'a').unlink()
            return original(fd, name)
        module.safe_open = injected
        self.assertEqual(module.audit(str(self.root))['verified_files'], 2)

    def test_05_candidate_rejects_removed_already_hashed_file(self):
        self.seal({'a': b'a', 'b': b'b'})
        module = load(CANDIDATE, 'candidate_remove')
        original = module.safe_open
        def injected(fd, name):
            if name == 'b':
                (self.root / 'a').unlink()
            return original(fd, name)
        module.safe_open = injected
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_INVENTORY_CHANGED_AFTER_HASH'):
            module.audit(str(self.root))

    def test_06_candidate_accepts_unchanged_snapshot(self):
        self.seal({'a': b'good', 'b': b'valid'})
        result = load(CANDIDATE, 'valid').audit(str(self.root))
        self.assertEqual((result['verified_files'], result['verified_bytes']), (2, 9))

    def test_07_candidate_accepts_exact_file_limit(self):
        self.seal({'a': b'z' * 1048576})
        self.assertEqual(load(CANDIDATE, 'boundary').audit(str(self.root))['verified_bytes'], 1048576)

    def test_08_candidate_rejects_corrupted_file(self):
        self.seal({'a': b'good'})
        (self.root / 'a').write_bytes(b'bad')
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_SHA256_MISMATCH'):
            load(CANDIDATE, 'corrupt').audit(str(self.root))

    def test_09_candidate_preserves_claim_ceiling(self):
        self.seal({'a': b'good'})
        result = load(CANDIDATE, 'ceiling').audit(str(self.root))
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
        self.assertEqual(result['external_source_binding'], 'NOT_ESTABLISHED_BY_THIS_TOOL')

    def test_10_candidate_rejects_129_files(self):
        self.seal({f'f{i:03}': b'z' for i in range(129)})
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_TOO_MANY_FILES'):
            load(CANDIDATE, 'many').audit(str(self.root))

    def test_11_candidate_does_not_modify_snapshot(self):
        self.seal({'a': b'good'})
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        load(CANDIDATE, 'readonly').audit(str(self.root))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_12_candidate_rejects_postscan_added_empty_file(self):
        self.seal({'a': b'good'})
        self.deny(lambda: (self.root / 'extra').write_bytes(b''), 'SNAPSHOT_INVENTORY_CHANGED_AFTER_HASH')


if __name__ == '__main__':
    unittest.main()
