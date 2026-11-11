#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent frozen C1 evaluator: PR base/head boundary drift.

Run before/after against --baseline or --candidate. Fixtures use deterministic
synthetic GitHub API replies; this evaluator neither imports the candidate's
logic nor changes its assertions based on candidate results.
"""
import argparse
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEAD = 'a' * 40
BASE = 'b' * 40
DRIFT = 'c' * 40


def load(name):
    p = ROOT / name
    spec = importlib.util.spec_from_file_location('target_under_test', p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows(n):
    return [{'filename': f'research/r16/alpha-{i:04d}.txt', 'status': 'added'}
            for i in range(n)]


class Case(unittest.TestCase):
    def call(self, *, count=126, actor='nexusomegac27', allow=(), base_seq=(BASE, BASE),
             head_seq=(HEAD, HEAD), payload=None, expected_base=BASE, fetch_base=True):
        payload = rows(count) if payload is None else payload
        bases = iter(base_seq)
        heads = iter(head_seq)
        def page(n):
            return payload[(n - 1) * 100:n * 100]
        def base():
            return next(bases)
        def head():
            return next(heads)
        kwargs = dict(fetch_page=page, fetch_head=head, actor=actor,
                      owner='nexusomegac27', external_allowlist=allow,
                      expected_count=count, expected_head_sha=HEAD)
        if TARGET_KIND == 'candidate':
            kwargs.update(fetch_base=base if fetch_base else None,
                          expected_base_sha=expected_base)
            return TARGET.enumerate_pr_files_with_base_head_recheck(**kwargs)
        return TARGET.enumerate_pr_files_with_boundary_recheck(**kwargs)

    def test_01_owner_126_complete(self):
        out = self.call()
        self.assertEqual(len(out['files']), 126)
        self.assertEqual(out['atomic_snapshot'], 'NOT_ESTABLISHED')

    def test_02_owner_201_complete(self):
        self.assertEqual(len(self.call(count=201)['files']), 201)

    def test_03_registered_external_7(self):
        self.assertEqual(len(self.call(count=7, actor='expert1', allow=('expert1',))['files']), 7)

    def test_04_unregistered_external_denied(self):
        with self.assertRaisesRegex(ValueError, 'UNREGISTERED_EXTERNAL'):
            self.call(count=1, actor='expert1')

    def test_05_external_eight_denied(self):
        with self.assertRaisesRegex(ValueError, 'EXTERNAL_FILE_COUNT'):
            self.call(count=8, actor='expert1', allow=('expert1',))

    def test_06_head_drift_before_denied(self):
        with self.assertRaisesRegex(ValueError, 'HEAD_DRIFT_BEFORE'):
            self.call(head_seq=(DRIFT, HEAD))

    def test_07_head_drift_after_denied(self):
        with self.assertRaisesRegex(ValueError, 'HEAD_DRIFT_AFTER'):
            self.call(head_seq=(HEAD, DRIFT))

    def test_08_duplicate_file_denied(self):
        bad = rows(126)
        bad[125] = bad[0].copy()
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_PR_FILE_PATH'):
            self.call(payload=bad)

    def test_09_incomplete_file_list_denied(self):
        with self.assertRaisesRegex(ValueError, 'INCOMPLETE_PR_FILE_CENSUS'):
            self.call(payload=rows(125))

    def test_10_invalid_file_status_denied(self):
        bad = rows(126)
        bad[2]['status'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'INVALID_PR_FILE_RECORD'):
            self.call(payload=bad)

    def test_11_zero_expected_denied(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_OR_UNVERIFIABLE_EXPECTED_COUNT'):
            self.call(count=0)

    def test_12_base_drift_before_denied(self):
        with self.assertRaisesRegex(ValueError, 'BASE_DRIFT_BEFORE'):
            self.call(base_seq=(DRIFT, BASE))

    def test_13_base_drift_after_denied(self):
        with self.assertRaisesRegex(ValueError, 'BASE_DRIFT_AFTER'):
            self.call(base_seq=(BASE, DRIFT))

    def test_14_base_not_callable_denied(self):
        with self.assertRaisesRegex(ValueError, 'BASE_READBACK_REQUIRED'):
            self.call(fetch_base=False)

    def test_15_base_sha_not_pinned_denied(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_PINNED_BASE_SHA'):
            self.call(expected_base='not-a-sha')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', choices=('baseline', 'candidate'), required=True)
    args = parser.parse_args()
    TARGET_KIND = args.target
    TARGET = load('alpha_r27e_owner_pr_head_boundary_guard_v2_20261026.py' if
                  args.target == 'baseline' else
                  'alpha_r27e_owner_pr_base_boundary_guard_v3_20261026.py')
    unittest.main(argv=['frozen_evaluator', '-v'], exit=False)
