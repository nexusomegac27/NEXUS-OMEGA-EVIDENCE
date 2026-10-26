#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, isolated contract tests for the R27-E owner PR file census candidate.
Run: python frozen_r27e_owner_pr_pagination_evaluator_v1_20261026.py PATH_TO_CANDIDATE
All GitHub responses below are synthetic; this is NOT a live CI authorization test.
"""
import importlib.util
import sys
import unittest

spec = importlib.util.spec_from_file_location('candidate_under_test', sys.argv[1])
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)
sys.argv = sys.argv[:1]
HEAD = 'a' * 40


def pages(n, corrupt=None):
    entries = [{'filename': f'research/r16/fixture/file_{i:04d}.md', 'status': 'added'} for i in range(n)]
    batches = [entries[i:i+100] for i in range(0, len(entries), 100)] + [[]]
    if corrupt:
        corrupt(batches)
    return lambda page: batches[page - 1] if page <= len(batches) else []


def census(n, actor='nexusomegac27', allowlist=(), source=None, observed=HEAD, expected=HEAD):
    return subject.enumerate_pr_files(
        fetch_page=source or pages(n), actor=actor, owner='nexusomegac27',
        external_allowlist=allowlist, expected_count=n, expected_head_sha=expected,
        observed_head_sha=observed, max_external_files=7)


class FrozenOwnerCensus(unittest.TestCase):
    def test_owner_126(self): self.assertEqual(len(census(126)), 126)
    def test_owner_101(self): self.assertEqual(len(census(101)), 101)
    def test_owner_100(self): self.assertEqual(len(census(100)), 100)
    def test_owner_200(self): self.assertEqual(len(census(200)), 200)
    def test_owner_2999(self): self.assertEqual(len(census(2999)), 2999)
    def test_owner_3000_denied(self): self.assertRaises(ValueError, census, 3000)
    def test_owner_zero_denied(self): self.assertRaises(ValueError, census, 0)
    def test_external_unregistered_denied(self): self.assertRaises(ValueError, census, 2, 'unknown')
    def test_external_registered_7(self): self.assertEqual(len(census(7, 'registered', ('registered',))), 7)
    def test_external_registered_8_denied(self): self.assertRaises(ValueError, census, 8, 'registered', ('registered',))
    def test_external_registered_126_denied(self): self.assertRaises(ValueError, census, 126, 'registered', ('registered',))
    def test_head_drift_denied(self): self.assertRaises(ValueError, census, 126, observed='b'*40)
    def test_missing_head_denied(self): self.assertRaises(ValueError, census, 126, expected='')
    def test_short_page_denied(self): self.assertRaises(ValueError, census, 126, source=lambda p: pages(99)(p))
    def test_count_overflow_denied(self): self.assertRaises(ValueError, census, 126, source=pages(127))
    def test_duplicate_path_denied(self):
        def corrupt(b): b[1][0]['filename'] = b[0][0]['filename']
        self.assertRaises(ValueError, census, 126, source=pages(126, corrupt))
    def test_malformed_response_denied(self): self.assertRaises(ValueError, census, 126, source=lambda p: {'error': 'rate limited'})
    def test_bad_file_record_denied(self):
        def corrupt(b): b[0][0] = {'filename': 'x'}
        self.assertRaises(ValueError, census, 126, source=pages(126, corrupt))
    def test_boolean_count_denied(self): self.assertRaises(ValueError, census, True)
    def test_no_write_surface(self):
        self.assertFalse(any(hasattr(subject, attr) for attr in ('update_ref','create_file','merge_pull_request','approve')))


if __name__ == '__main__': unittest.main(verbosity=1)
