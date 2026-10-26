#!/usr/bin/env python3
"""Frozen C1 black-box oracle for post-hash same-name content/identity drift.

Independent test fixtures are committed before the V5 candidate. Original V4
and candidate are loaded from distinct paths. Tests assert narrow deterministic
mutations only; no atomic snapshot or live security claim is implied.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BASE = HERE / 'alpha_pipeline_snapshot_fixity_inventory_v4_20261026.py'
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_pipeline_snapshot_fixity_identity_v5_20261026.py'))


def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrozenIdentityEvaluator(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'snapshot'
        self.root.mkdir()

    def seal(self, files):
        lines = []
        for name, data in sorted(files.items()):
            (self.root / name).write_bytes(data)
            lines.append(hashlib.sha256(data).hexdigest() + '  ' + name + '\n')
        (self.root / 'SHA256SUMS.txt').write_text(''.join(lines), encoding='ascii')

    def audit_injected(self, path, trigger, operation):
        module = load(path, 'test_' + str(id(self)))
        original = module.safe_open
        done = False

        def hooked(directory, name):
            nonlocal done
            if name == trigger and not done:
                done = True
                operation()
            return original(directory, name)

        module.safe_open = hooked
        return module.audit(str(self.root))

    def deny(self, trigger, operation, marker):
        with self.assertRaises((ValueError, OSError)) as raised:
            self.audit_injected(CANDIDATE, trigger, operation)
        self.assertIn(marker, str(raised.exception))

    def swap_a(self):
        tmp = self.root.parent / 'replacement'
        tmp.write_bytes(b'EVIL')
        os.replace(tmp, self.root / 'a')

    def mutate_a(self):
        path = self.root / 'a'
        path.write_bytes(b'EVIL')
        # Force a distinguishable mtime even on coarse-clock filesystems.
        st = path.stat()
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))

    def mutate_manifest(self):
        path = self.root / 'SHA256SUMS.txt'
        path.write_text(hashlib.sha256(b'EVIL').hexdigest() + '  a\n', encoding='ascii')
        st = path.stat()
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))

    def test_01_baseline_accepts_same_name_inode_swap(self):
        self.seal({'a': b'good', 'b': b'fine'})
        result = self.audit_injected(BASE, 'b', self.swap_a)
        self.assertEqual(result['state'], 'PASS_FIXITY_C1')
        self.assertEqual((self.root / 'a').read_bytes(), b'EVIL')

    def test_02_candidate_denies_same_name_inode_swap(self):
        self.seal({'a': b'good', 'b': b'fine'})
        self.deny('b', self.swap_a, 'SNAPSHOT_FILE_IDENTITY_CHANGED_AFTER_HASH')

    def test_03_baseline_accepts_inplace_mutation_after_hash(self):
        self.seal({'a': b'good', 'b': b'fine'})
        self.assertEqual(self.audit_injected(BASE, 'b', self.mutate_a)['state'], 'PASS_FIXITY_C1')

    def test_04_candidate_denies_inplace_mutation_after_hash(self):
        self.seal({'a': b'good', 'b': b'fine'})
        self.deny('b', self.mutate_a, 'SNAPSHOT_FILE_IDENTITY_CHANGED_AFTER_HASH')

    def test_05_baseline_accepts_manifest_mutation_after_read(self):
        self.seal({'a': b'good'})
        self.assertEqual(self.audit_injected(BASE, 'a', self.mutate_manifest)['state'], 'PASS_FIXITY_C1')

    def test_06_candidate_denies_manifest_mutation_after_read(self):
        self.seal({'a': b'good'})
        self.deny('a', self.mutate_manifest, 'SNAPSHOT_MANIFEST_IDENTITY_CHANGED_AFTER_READ')

    def test_07_candidate_accepts_clean_two_file_snapshot(self):
        self.seal({'a': b'good', 'b': b'fine'})
        result = load(CANDIDATE, 'clean').audit(str(self.root))
        self.assertEqual((result['verified_files'], result['verified_bytes']), (2, 8))
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')

    def test_08_candidate_accepts_exact_one_mib_boundary(self):
        self.seal({'a': b'z' * 1048576})
        self.assertEqual(load(CANDIDATE, 'limit').audit(str(self.root))['verified_bytes'], 1048576)

    def test_09_candidate_rejects_corrupted_data(self):
        self.seal({'a': b'good'})
        (self.root / 'a').write_bytes(b'bad!')
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_SHA256_MISMATCH'):
            load(CANDIDATE, 'corrupt').audit(str(self.root))

    def test_10_candidate_rejects_added_file_after_hash(self):
        self.seal({'a': b'good'})
        self.deny('a', lambda: (self.root / 'extra').write_bytes(b'x'), 'SNAPSHOT_INVENTORY_CHANGED_AFTER_HASH')

    def test_11_candidate_rejects_symlink(self):
        self.seal({'a': b'good'})
        (self.root / 'link').symlink_to(self.root / 'a')
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_NONREGULAR_ENTRY'):
            load(CANDIDATE, 'link').audit(str(self.root))

    def test_12_candidate_rejects_129_files(self):
        self.seal({f'f{i:03}': b'x' for i in range(129)})
        with self.assertRaisesRegex(ValueError, 'SNAPSHOT_TOO_MANY_FILES'):
            load(CANDIDATE, 'many').audit(str(self.root))

    def test_13_candidate_does_not_mutate_snapshot(self):
        self.seal({'a': b'good'})
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        load(CANDIDATE, 'readonly').audit(str(self.root))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_14_candidate_retains_external_source_gap(self):
        self.seal({'a': b'good'})
        result = load(CANDIDATE, 'gap').audit(str(self.root))
        self.assertEqual(result['external_source_binding'], 'NOT_ESTABLISHED_BY_THIS_TOOL')


if __name__ == '__main__':
    unittest.main()
