#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, isolated C1 evaluator for an API-derived PR/receipt census.

Input is an explicitly scoped, non-authenticating API snapshot. This evaluator
cannot prove completeness outside PR #184..#199 or original source byte readback.
"""
import copy
import json
import pathlib
import sys
import unittest

SCOPE = set(range(184, 200))
OWNER = 'nexusomegac27'
SHA40 = set('0123456789abcdef')


def valid_sha(x):
    return isinstance(x, str) and len(x) == 40 and set(x) <= SHA40


def audit(rows, pinned_main):
    if not isinstance(rows, list) or len(rows) != 16 or not valid_sha(pinned_main):
        raise ValueError('INVALID_SCOPE')
    if any(not isinstance(r, dict) or set(r) != {
        'pr', 'merged', 'merge_sha', 'parent', 'signature_valid', 'receipt_id',
        'receipt_pr', 'receipt_main', 'receipt_actor', 'receipt_created',
        'receipt_updated', 'merged_at'} for r in rows):
        raise ValueError('INVALID_ROW_SCHEMA')
    by_pr = {r['pr']: r for r in rows if type(r['pr']) is int}
    if len(by_pr) != 16 or set(by_pr) != SCOPE:
        raise ValueError('INCOMPLETE_OR_DUPLICATE_SCOPE')
    ordered = [by_pr[i] for i in sorted(SCOPE)]
    merged = [r for r in ordered if r['merged'] is True]
    if len(merged) != 15 or by_pr[185]['merged'] is not False:
        raise ValueError('MERGE_POPULATION_CHANGED')
    if any(not valid_sha(r['merge_sha']) or not valid_sha(r['parent'])
           or r['signature_valid'] is not True for r in merged):
        raise ValueError('INVALID_COMMIT_PROVENANCE')
    if any(merged[i]['parent'] != merged[i-1]['merge_sha'] for i in range(1, len(merged))):
        raise ValueError('PARENT_CHAIN_BROKEN')
    if merged[-1]['merge_sha'] != pinned_main:
        raise ValueError('MAIN_NOT_LAST_MERGE')
    if any(by_pr[185][k] is not None for k in ('receipt_id', 'receipt_pr', 'receipt_main')):
        raise ValueError('UNMERGED_PR_RECEIPT')
    ids = [r['receipt_id'] for r in merged]
    if any(type(x) is not int or x <= 0 for x in ids) or len(set(ids)) != 15:
        raise ValueError('MISSING_OR_DUPLICATE_RECEIPT')
    for r in merged:
        if (r['receipt_pr'] != r['pr'] or r['receipt_main'] != r['merge_sha']
            or r['receipt_actor'] != OWNER or r['receipt_created'] != r['receipt_updated']
            or not isinstance(r['receipt_created'], str)
            or r['receipt_created'] < r['merged_at']):
            raise ValueError('RECEIPT_PROVENANCE_MISMATCH')
    return {'scope': 'PR184_199_API_DERIVED_NOT_COMPLETE_PROJECT',
            'pr_population': len(ordered), 'merged_denominator': len(merged),
            'unmerged_excluded': 1, 'verified_merge_chain': 15,
            'github_signature_valid': 15, 'owner_receipt_sha_matches': 15,
            'receipt_not_edited_at_snapshot': 15, 'receipt_coverage': '15/15',
            'source_test_full_readback': 'NOT_ESTABLISHED',
            'eligible_handoff_automation': 'NOT_COMPUTABLE',
            'project_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


class FrozenOracle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads(pathlib.Path(sys.argv[1]).read_text('utf-8'))
        cls.rows = data['rows']
        cls.main = data['main']

    def check_mutation(self, edit):
        rows = copy.deepcopy(self.rows)
        edit(rows)
        with self.assertRaises(ValueError):
            audit(rows, self.main)

    def test_01_positive_source_scoped(self):
        result = audit(self.rows, self.main)
        self.assertEqual((result['merged_denominator'], result['owner_receipt_sha_matches']), (15, 15))
        self.assertEqual(result['project_readback_rate'], 'NOT_COMPUTABLE')

    def test_02_missing_receipt(self):
        self.check_mutation(lambda r: r[0].update(receipt_id=None))

    def test_03_wrong_receipt_sha(self):
        self.check_mutation(lambda r: r[0].update(receipt_main='0'*40))

    def test_04_predecessor_pr_misattribution(self):
        self.check_mutation(lambda r: r[0].update(receipt_pr=185))

    def test_05_duplicate_receipt(self):
        self.check_mutation(lambda r: r[1].update(receipt_id=r[0]['receipt_id']))

    def test_06_wrong_actor(self):
        self.check_mutation(lambda r: r[0].update(receipt_actor='unknown-agent'))

    def test_07_edited_receipt(self):
        self.check_mutation(lambda r: r[0].update(receipt_updated='2026-10-30T00:00:00Z'))

    def test_08_false_signature(self):
        self.check_mutation(lambda r: r[0].update(signature_valid=False))

    def test_09_broken_parent_chain(self):
        self.check_mutation(lambda r: r[2].update(parent='f'*40))

    def test_10_missing_pr(self):
        self.check_mutation(lambda r: r.pop(0))

    def test_11_open_pr_as_merged(self):
        self.check_mutation(lambda r: r[1].update(merged=True))

    def test_12_receipt_before_merge(self):
        self.check_mutation(lambda r: r[0].update(receipt_created='2026-10-28T00:00:00Z', receipt_updated='2026-10-28T00:00:00Z'))


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=2)
