#!/usr/bin/env python3
"""Independent, candidate-agnostic TOCTOU evaluator for a flat snapshot audit.

Deterministically changes one checked path between inventory and read.
Tests both pinned baseline and candidate; no candidate imports in oracle logic.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

DIR = Path(__file__).resolve().parent
BASE = DIR / 'alpha_pipeline_snapshot_fixity_audit_v1_20261026.py'
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', DIR / 'alpha_pipeline_snapshot_fixity_nofollow_v2_20261026.py'))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IndependentBoundaryEvaluator(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'snap'
        self.root.mkdir()
        self.target = self.root / 'manifest.json'
        self.target.write_bytes(b'{"claim":"C1"}\n')
        self.outside = Path(self.tmp.name) / 'outside.json'
        self.outside.write_bytes(self.target.read_bytes())
        self.reseal()

    def reseal(self):
        digest = hashlib.sha256(self.target.read_bytes()).hexdigest()
        (self.root / 'SHA256SUMS.txt').write_text(digest + '  manifest.json\n', encoding='ascii')

    def run_audit(self, module_path, race_name=None):
        module = load(module_path, 'testmod_' + str(id(self)))
        original_path_open = Path.open
        original_os_open = os.open
        fired = [False]
        def mutate():
            if not fired[0]:
                fired[0] = True
                victim = self.root / race_name
                original = victim.read_bytes()
                self.outside.write_bytes(original)
                victim.unlink()
                victim.symlink_to(self.outside)
        def patched_path_open(path, *args, **kwargs):
            if race_name and Path(path) == self.root / race_name:
                mutate()
            return original_path_open(path, *args, **kwargs)
        def patched_os_open(path, *args, **kwargs):
            if race_name and path == race_name and kwargs.get('dir_fd') is not None:
                mutate()
            return original_os_open(path, *args, **kwargs)
        try:
            with patch.object(Path, 'open', patched_path_open), patch.object(os, 'open', patched_os_open):
                result = module.audit(str(self.root))
            return ('PASS', result, fired[0])
        except (OSError, ValueError, UnicodeError) as exc:
            return ('FAIL', str(exc), fired[0])

    def test_01_baseline_accepts_swapped_manifest_symlink(self):
        status, _, fired = self.run_audit(BASE, 'manifest.json')
        self.assertTrue(fired)
        self.assertEqual(status, 'PASS')

    def test_02_candidate_rejects_swapped_manifest_symlink(self):
        status, _, fired = self.run_audit(CANDIDATE, 'manifest.json')
        self.assertTrue(fired)
        self.assertEqual(status, 'FAIL')

    def test_03_baseline_rejects_swapped_checksum_symlink_at_inventory(self):
        status, _, fired = self.run_audit(BASE, 'SHA256SUMS.txt')
        self.assertTrue(fired)
        self.assertEqual(status, 'FAIL')

    def test_04_candidate_rejects_swapped_checksum_symlink(self):
        status, _, fired = self.run_audit(CANDIDATE, 'SHA256SUMS.txt')
        self.assertTrue(fired)
        self.assertEqual(status, 'FAIL')

    def test_05_candidate_accepts_valid_snapshot(self):
        status, obj, _ = self.run_audit(CANDIDATE)
        self.assertEqual(status, 'PASS', obj)
        self.assertEqual(obj['verified_files'], 1)

    def test_06_baseline_accepts_valid_snapshot(self):
        status, obj, _ = self.run_audit(BASE)
        self.assertEqual(status, 'PASS', obj)

    def test_07_candidate_rejects_corrupt_file(self):
        self.target.write_bytes(b'changed')
        self.assertEqual(self.run_audit(CANDIDATE)[0], 'FAIL')

    def test_08_candidate_rejects_extra_file(self):
        (self.root / 'extra.json').write_bytes(b'{}')
        self.assertEqual(self.run_audit(CANDIDATE)[0], 'FAIL')

    def test_09_candidate_rejects_preexisting_symlink(self):
        self.target.unlink()
        self.target.symlink_to(self.outside)
        self.assertEqual(self.run_audit(CANDIDATE)[0], 'FAIL')

    def test_10_candidate_preserves_source_bytes(self):
        before = {p.name:p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(self.run_audit(CANDIDATE)[0], 'PASS')
        after = {p.name:p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(before, after)

    def test_11_candidate_rejects_malformed_sums(self):
        (self.root / 'SHA256SUMS.txt').write_text('bad\n')
        self.assertEqual(self.run_audit(CANDIDATE)[0], 'FAIL')

    def test_12_candidate_rejects_root_symlink(self):
        link = Path(self.tmp.name) / 'alias'
        link.symlink_to(self.root, target_is_directory=True)
        module = load(CANDIDATE, 'root_test')
        with self.assertRaises(OSError):
            module.audit(str(link))


if __name__ == '__main__':
    unittest.main()
