#!/usr/bin/env python3
"""Frozen independent black-box evaluation of isolated C1 handoff sample census V2.
Not a scientific oracle; test expectations precede candidate publication.
Historical V1 evaluator is preserved and explicitly superseded for this distinct fixture set.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

CANDIDATE = os.environ.get('AXIOM_CANDIDATE', str(Path(__file__).with_name('alpha_handoff_coverage_census_v2_20261026.py')))

def record(id, **changes):
    r = {'id': id, 'scope': 'PUBLIC', 'accessible': True, 'authorized': True,
         'routine': True, 'automated': True, 'outcome': 'SUCCESS',
         'source_readback': 'MATCH', 'publication_readback': 'MATCH'}
    r.update(changes)
    return r

def run(value):
    payload = value if isinstance(value, str) else json.dumps(value, allow_nan=False)
    return subprocess.run([sys.executable, CANDIDATE], input=payload,
                          text=True, capture_output=True, timeout=5)

def valid(*records):
    proc = run({'schema_version': 2, 'records': list(records)})
    if proc.returncode:
        raise AssertionError((proc.returncode, proc.stdout, proc.stderr))
    return json.loads(proc.stdout)

class FrozenCoverageV2(unittest.TestCase):
    def test_manual_in_denominator(self):
        r=valid(record('a'),record('b',automated=False))
        self.assertEqual((r['eligible_denominator'],r['automated_numerator'],r['sample_rate']), (2,1,'1/2'))
    def test_failed_in_denominator(self):
        r=valid(record('a',outcome='FAILED'),record('b'))
        self.assertEqual((r['eligible_denominator'],r['automated_numerator']), (2,1))
    def test_pending_in_denominator(self):
        self.assertEqual(valid(record('a',outcome='PENDING'),record('b'))['sample_rate'],'1/2')
    def test_source_gap_in_denominator(self):
        self.assertEqual(valid(record('a',source_readback='GAP'),record('b'))['sample_rate'],'1/2')
    def test_publication_gap_in_denominator(self):
        self.assertEqual(valid(record('a',publication_readback='GAP'),record('b'))['sample_rate'],'1/2')
    def test_private_and_local_inaccessible_excluded(self):
        r=valid(record('a'),record('b',scope='PRIVATE',accessible=False),record('c',scope='LOCAL',accessible=False))
        self.assertEqual((r['eligible_denominator'],r['excluded_count'],r['automated_numerator']),(1,2,1))
    def test_public_inaccessible_excluded(self):
        self.assertEqual(valid(record('a',accessible=False),record('b'))['eligible_denominator'],1)
    def test_explicit_private_accessible_true_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a',scope='PRIVATE',accessible=True)]}).returncode,0)
    def test_unknown_eligibility_withheld(self):
        r=valid(record('a'),record('b',authorized=None))
        self.assertEqual((r['unknown_eligibility_count'],r['sample_rate']),(1,'WITHHELD_UNKNOWN_ELIGIBILITY'))
    def test_empty_denominator_withheld(self):
        self.assertEqual(valid(record('a',scope='PRIVATE',accessible=False))['sample_rate'],'NOT_COMPUTABLE_ZERO_DENOMINATOR')
    def test_perfect_sample_not_project_claim(self):
        r=valid(record('a'))
        self.assertEqual((r['sample_rate'],r['project_rate'],r['evidence_class']),('1/1','NOT_COMPUTABLE','UNVERIFIED_SAMPLE_ONLY'))
    def test_duplicate_id_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a'),record('a')]}).returncode,0)
    def test_duplicate_json_key_rejected(self):
        self.assertNotEqual(run('{"schema_version":2,"records":[],"records":[]}').returncode,0)
    def test_nonfinite_rejected(self):
        self.assertNotEqual(run('{"schema_version":2,"records":[],"x":NaN}').returncode,0)
    def test_bool_version_rejected(self):
        self.assertNotEqual(run({'schema_version':True,'records':[]}).returncode,0)
    def test_missing_field_rejected(self):
        x=record('a'); del x['authorized']
        self.assertNotEqual(run({'schema_version':2,'records':[x]}).returncode,0)
    def test_unknown_extra_field_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a',admin_override=True)]}).returncode,0)
    def test_untrusted_inventory_complete_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a')],'inventory_complete':True}).returncode,0)
    def test_invalid_scope_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a',scope='SECRET')]}).returncode,0)
    def test_invalid_readback_rejected(self):
        self.assertNotEqual(run({'schema_version':2,'records':[record('a',source_readback='MAYBE')]}).returncode,0)

if __name__ == '__main__':
    unittest.main()
