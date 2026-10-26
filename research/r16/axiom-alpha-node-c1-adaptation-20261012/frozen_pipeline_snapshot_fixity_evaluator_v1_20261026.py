#!/usr/bin/env python3
"""Frozen black-box C1 fixture suite for read-only pipeline snapshot fixity.

Oracle is independent of candidate implementation: mutate only fixture bytes,
call candidate in subprocess, inspect exit code and JSON. No candidate imports.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

DIR = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', DIR / 'alpha_pipeline_snapshot_fixity_audit_v1_20261026.py'))


class FrozenSnapshotFixityOracle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'snapshots' / 'v1'
        self.root.mkdir(parents=True)
        (self.root / 'manifest.json').write_bytes(b'{"claim_ceiling":"C1"}\n')
        (self.root / 'items.json').write_bytes(b'{"items":[]}\n')
        self.reseal()

    def reseal(self):
        entries = []
        for p in sorted(self.root.iterdir()):
            if p.name != 'SHA256SUMS.txt':
                entries.append(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n')
        (self.root / 'SHA256SUMS.txt').write_text(''.join(entries), encoding='ascii')

    def run_candidate(self):
        return subprocess.run([sys.executable, str(CANDIDATE), str(self.root)],
                              capture_output=True, timeout=10)

    def assert_fail(self, marker):
        p = self.run_candidate()
        self.assertEqual(p.returncode, 2, p.stdout)
        self.assertIn(marker.encode(), p.stderr)
        self.assertEqual(p.stdout, b'')

    def test_01_positive_two_file_snapshot(self):
        p = self.run_candidate()
        self.assertEqual(p.returncode, 0, p.stderr)
        obj = json.loads(p.stdout)
        self.assertEqual(obj['verified_files'], 2)
        self.assertEqual(obj['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
        self.assertEqual(obj['external_source_binding'], 'NOT_ESTABLISHED_BY_THIS_TOOL')

    def test_02_changed_original_file_is_detected(self):
        (self.root / 'manifest.json').write_bytes(b'CORRUPTED')
        self.assert_fail('SNAPSHOT_SHA256_MISMATCH')

    def test_03_missing_bound_file_is_detected(self):
        (self.root / 'items.json').unlink()
        self.assert_fail('SNAPSHOT_INVENTORY_MISMATCH')

    def test_04_unlisted_extra_file_is_detected(self):
        (self.root / 'new.txt').write_text('unlisted')
        self.assert_fail('SNAPSHOT_INVENTORY_MISMATCH')

    def test_05_duplicate_checksum_entry_is_detected(self):
        p = self.root / 'SHA256SUMS.txt'
        p.write_bytes(p.read_bytes() + p.read_bytes().splitlines(keepends=True)[0])
        self.assert_fail('SUMS_DUPLICATE_NAME')

    def test_06_traversal_entry_is_detected(self):
        p = self.root / 'SHA256SUMS.txt'
        p.write_text('0'*64 + '  ../escape\n')
        self.assert_fail('SUMS_MALFORMED_ENTRY')

    def test_07_wrong_digest_is_detected(self):
        p = self.root / 'SHA256SUMS.txt'
        raw = p.read_text()
        p.write_text('0'*64 + raw[64:])
        self.assert_fail('SNAPSHOT_SHA256_MISMATCH')

    def test_08_missing_checksum_file_is_detected(self):
        (self.root / 'SHA256SUMS.txt').unlink()
        self.assert_fail('SUMS_NOT_REGULAR_FILE')

    def test_09_symlinked_file_is_detected(self):
        (self.root / 'items.json').unlink()
        try:
            (self.root / 'items.json').symlink_to(self.root / 'manifest.json')
        except (OSError, NotImplementedError):
            self.skipTest('symlink unavailable')
        self.assert_fail('SNAPSHOT_NONREGULAR_ENTRY')

    def test_10_case_colliding_names_are_detected(self):
        p = self.root / 'SHA256SUMS.txt'
        raw = p.read_text()
        p.write_text(raw + hashlib.sha256(b'').hexdigest() + '  MANIFEST.JSON\n')
        self.assert_fail('SUMS_DUPLICATE_NAME')

    def test_11_malformed_hash_is_detected(self):
        p = self.root / 'SHA256SUMS.txt'
        raw = p.read_text()
        p.write_text('g' + raw[1:])
        self.assert_fail('SUMS_MALFORMED_ENTRY')

    def test_12_extra_directory_is_detected(self):
        (self.root / 'unlisted').mkdir()
        self.assert_fail('SNAPSHOT_NONREGULAR_ENTRY')

    def test_13_audit_never_mutates_snapshot(self):
        before = {p.name:p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(self.run_candidate().returncode, 0)
        after = {p.name:p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(before, after)

    def test_14_empty_checksum_inventory_is_rejected(self):
        (self.root / 'SHA256SUMS.txt').write_text('')
        self.assert_fail('SUMS_NONCANONICAL_LINES')

    def test_15_missing_trailing_newline_is_rejected(self):
        p = self.root / 'SHA256SUMS.txt'
        p.write_bytes(p.read_bytes().rstrip(b'\n'))
        self.assert_fail('SUMS_NONCANONICAL_LINES')

    def test_16_positive_one_file_snapshot(self):
        (self.root / 'items.json').unlink()
        self.reseal()
        p = self.run_candidate()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['verified_files'], 1)


if __name__ == '__main__':
    unittest.main()
