#!/usr/bin/env python3
"""Frozen candidate-agnostic POSIX snapshot resource-budget evaluator.

Test specification fixed before V3 implementation. A local passing evaluator is
not an external expert audit, runtime approval or source authentication.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BASE = HERE / 'alpha_pipeline_snapshot_fixity_nofollow_v2_20261026.py'
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_pipeline_snapshot_fixity_budget_v3_20261026.py'))
ONE_MIB = 1048576
FOUR_MIB = 4194304


def load(path, tag):
    spec = importlib.util.spec_from_file_location(tag, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrozenResourceBudgetEvaluator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'snapshot'
        self.root.mkdir()

    def seal(self, files):
        sums = []
        for name, data in sorted(files.items()):
            (self.root / name).write_bytes(data)
            sums.append(hashlib.sha256(data).hexdigest() + '  ' + name + '\n')
        (self.root / 'SHA256SUMS.txt').write_text(''.join(sums), encoding='ascii')

    def audit(self, path):
        return load(path, 'frozen_' + str(id(self))).audit(str(self.root))

    def assert_denied(self, expected):
        with self.assertRaises((ValueError, OSError)) as ctx:
            self.audit(CANDIDATE)
        self.assertIn(expected, str(ctx.exception))

    def test_01_baseline_accepts_file_over_1mib(self):
        self.seal({'a': b'x' * (ONE_MIB + 1)})
        self.assertEqual(self.audit(BASE)['verified_bytes'], ONE_MIB + 1)

    def test_02_candidate_denies_file_over_1mib(self):
        self.seal({'a': b'x' * (ONE_MIB + 1)})
        self.assert_denied('SNAPSHOT_FILE_TOO_LARGE')

    def test_03_baseline_accepts_total_over_4mib(self):
        self.seal({'a': b'x' * ONE_MIB, 'b': b'x' * ONE_MIB,
                   'c': b'x' * ONE_MIB, 'd': b'x' * ONE_MIB, 'e': b'x'})
        self.assertEqual(self.audit(BASE)['verified_bytes'], FOUR_MIB + 1)

    def test_04_candidate_denies_total_over_4mib(self):
        self.seal({'a': b'x' * ONE_MIB, 'b': b'x' * ONE_MIB,
                   'c': b'x' * ONE_MIB, 'd': b'x' * ONE_MIB, 'e': b'x'})
        self.assert_denied('SNAPSHOT_TOTAL_TOO_LARGE')

    def test_05_baseline_accepts_129_files(self):
        self.seal({f'f{i:03}': b'z' for i in range(129)})
        self.assertEqual(self.audit(BASE)['verified_files'], 129)

    def test_06_candidate_denies_129_files(self):
        self.seal({f'f{i:03}': b'z' for i in range(129)})
        self.assert_denied('SNAPSHOT_TOO_MANY_FILES')

    def test_07_candidate_accepts_valid(self):
        self.seal({'manifest.json': b'{"claim":"C1"}\n'})
        self.assertEqual(self.audit(CANDIDATE)['verified_files'], 1)

    def test_08_candidate_accepts_exact_file_limit(self):
        self.seal({'one.bin': b'a' * ONE_MIB})
        self.assertEqual(self.audit(CANDIDATE)['verified_bytes'], ONE_MIB)

    def test_09_candidate_accepts_exact_total_limit(self):
        self.seal({str(i) + '.bin': b'a' * ONE_MIB for i in range(4)})
        self.assertEqual(self.audit(CANDIDATE)['verified_bytes'], FOUR_MIB)

    def test_10_candidate_accepts_exact_file_count(self):
        self.seal({f'f{i:03}': b'z' for i in range(128)})
        self.assertEqual(self.audit(CANDIDATE)['verified_files'], 128)

    def test_11_candidate_denies_extra_unsealed_file(self):
        self.seal({'a': b'x'})
        (self.root / 'unsealed').write_bytes(b'1')
        with self.assertRaises(ValueError):
            self.audit(CANDIDATE)

    def test_12_candidate_denies_corruption(self):
        self.seal({'a': b'x'})
        (self.root / 'a').write_bytes(b'y')
        self.assert_denied('SNAPSHOT_SHA256_MISMATCH')

    def test_13_candidate_denies_symlink(self):
        self.seal({'a': b'x'})
        outside = Path(self.temp.name) / 'outside'
        outside.write_bytes(b'x')
        (self.root / 'a').unlink()
        (self.root / 'a').symlink_to(outside)
        with self.assertRaises((OSError, ValueError)):
            self.audit(CANDIDATE)

    def test_14_candidate_denies_malformed_manifest(self):
        self.seal({'a': b'x'})
        (self.root / 'SHA256SUMS.txt').write_text('bad\n', encoding='ascii')
        with self.assertRaises(ValueError):
            self.audit(CANDIDATE)

    def test_15_candidate_does_not_modify_snapshot(self):
        self.seal({'a': b'x'})
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.audit(CANDIDATE)
        after = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(before, after)

    def test_16_candidate_never_claims_external_provenance(self):
        self.seal({'a': b'x'})
        result = self.audit(CANDIDATE)
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
        self.assertEqual(result['external_source_binding'], 'NOT_ESTABLISHED_BY_THIS_TOOL')
        self.assertEqual(result['evidence_class'], 'LOCAL_SNAPSHOT_ONLY')


if __name__ == '__main__':
    unittest.main()
