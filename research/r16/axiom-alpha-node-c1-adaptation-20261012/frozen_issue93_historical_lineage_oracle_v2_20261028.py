#!/usr/bin/env python3
"""Frozen, independently authored black-box oracle for historical main ancestry.
Run against candidate via subprocess; no network, no repository writes.
"""
import copy
import json
import subprocess
import sys
import unittest

SCRIPT = sys.argv[1] if len(sys.argv) > 1 else 'alpha_issue93_historical_lineage_guard_v2_20261028.py'
MERGE = '6e700be6fd408c3d78d3d7e08619b635de92966f'
MAIN = '59bc5b6aeeda70e11f342f3cb745c4da4b651146'
OTHER = 'f' * 40


def fixture():
    return {
        'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_HISTORICAL_LINEAGE_V2',
        'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
        'receipt': {'id': 6478246029, 'pr': 178, 'merge_commit_sha': MERGE},
        'main': {'sha': MAIN},
        'compare': {'base': MERGE, 'head': MAIN, 'status': 'ahead',
                    'ahead_by': 1, 'behind_by': 0, 'total_commits': 1,
                    'base_commit': {'sha': MERGE},
                    'merge_base_commit': {'sha': MERGE}},
    }


def call(obj, raw=None):
    data = raw if raw is not None else json.dumps(obj)
    return subprocess.run([sys.executable, SCRIPT], input=data, text=True,
                          capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def test_01_valid_descendant(self):
        r = call(fixture())
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out['historical_main_readback'], 'ANCESTOR_CONFIRMED_IN_SUPPLIED_COMPARE')
        self.assertFalse(out['api_origin_authenticated'])
        self.assertEqual(out['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')

    def test_02_valid_equal(self):
        x = fixture()
        x['main']['sha'] = MERGE
        x['compare'].update(head=MERGE, status='identical', ahead_by=0, total_commits=0)
        self.assertEqual(call(x).returncode, 0)

    def test_03_wrong_merge_base(self):
        x = fixture(); x['compare']['merge_base_commit']['sha'] = OTHER
        self.assertNotEqual(call(x).returncode, 0)

    def test_04_diverged(self):
        x = fixture(); x['compare']['status'] = 'diverged'
        self.assertNotEqual(call(x).returncode, 0)

    def test_05_behind(self):
        x = fixture(); x['compare']['behind_by'] = 1
        self.assertNotEqual(call(x).returncode, 0)

    def test_06_wrong_base(self):
        x = fixture(); x['compare']['base_commit']['sha'] = OTHER
        self.assertNotEqual(call(x).returncode, 0)

    def test_07_wrong_head(self):
        x = fixture(); x['compare']['head'] = OTHER
        self.assertNotEqual(call(x).returncode, 0)

    def test_08_wrong_receipt(self):
        x = fixture(); x['receipt']['merge_commit_sha'] = OTHER
        self.assertNotEqual(call(x).returncode, 0)

    def test_09_wrong_count(self):
        x = fixture(); x['compare']['total_commits'] = 2
        self.assertNotEqual(call(x).returncode, 0)

    def test_10_negative_count(self):
        x = fixture(); x['compare']['ahead_by'] = -1
        self.assertNotEqual(call(x).returncode, 0)

    def test_11_boolean_count(self):
        x = fixture(); x['compare']['ahead_by'] = True
        self.assertNotEqual(call(x).returncode, 0)

    def test_12_equal_with_ahead(self):
        x = fixture(); x['compare']['status'] = 'identical'
        self.assertNotEqual(call(x).returncode, 0)

    def test_13_ahead_with_zero(self):
        x = fixture(); x['compare']['ahead_by'] = 0; x['compare']['total_commits'] = 0
        self.assertNotEqual(call(x).returncode, 0)

    def test_14_duplicate_json_key(self):
        raw = json.dumps(fixture()).replace('"repository":', '"repository": "bad", "repository":', 1)
        self.assertNotEqual(call(None, raw).returncode, 0)

    def test_15_nonfinite(self):
        raw = json.dumps(fixture()).replace('"ahead_by": 1', '"ahead_by": NaN')
        self.assertNotEqual(call(None, raw).returncode, 0)

    def test_16_wrong_scope(self):
        x = fixture(); x['repository'] = 'somebody/other'
        self.assertNotEqual(call(x).returncode, 0)

    def test_17_extra_fields(self):
        x = fixture(); x['compare']['invented'] = 'AUTHENTICATED'
        self.assertNotEqual(call(x).returncode, 0)

    def test_18_empty_input(self):
        self.assertNotEqual(call(None, '').returncode, 0)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=0)
