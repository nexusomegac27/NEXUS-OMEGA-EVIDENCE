#!/usr/bin/env python3
"""Independent black-box C1 evaluation of short-circuit exclusion V3.
Expectations specified before candidate publication; do not edit to make candidate pass.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

CANDIDATE = os.environ.get('AXIOM_CANDIDATE',str(Path(__file__).with_name('alpha_handoff_coverage_census_v3_20261026.py')))

def record(id, **changes):
    value = {'id':id,'scope':'PUBLIC','accessible':True,'authorized':True,'routine':True,
             'automated':True,'outcome':'SUCCESS','source_readback':'MATCH','publication_readback':'MATCH'}
    value.update(changes)
    return value

def execute(payload):
    value = payload if isinstance(payload,str) else json.dumps(payload,allow_nan=False)
    return subprocess.run([sys.executable,CANDIDATE],input=value,text=True,capture_output=True,timeout=5)

def census(*records):
    result = execute({'schema_version':2,'records':list(records)})
    if result.returncode:
        raise AssertionError((result.returncode,result.stderr))
    return json.loads(result.stdout)

class FrozenShortCircuitV3(unittest.TestCase):
    def test_known_private_over_unknown_authorization(self):
        x=census(record('ok'),record('private',scope='PRIVATE',accessible=False,authorized=None))
        self.assertEqual((x['sample_rate'],x['excluded_count'],x['unknown_eligibility_count']),('1/1',1,0))
    def test_known_local_over_unknown_routine(self):
        x=census(record('ok'),record('local',scope='LOCAL',accessible=False,routine=None))
        self.assertEqual((x['sample_rate'],x['excluded_count']),('1/1',1))
    def test_known_public_inaccessible_over_unknown_authorization(self):
        x=census(record('ok'),record('no',accessible=False,authorized=None))
        self.assertEqual((x['sample_rate'],x['excluded_count']),('1/1',1))
    def test_known_unauthorized_over_unknown_accessibility(self):
        x=census(record('ok'),record('no',accessible=None,authorized=False))
        self.assertEqual((x['sample_rate'],x['excluded_count']),('1/1',1))
    def test_known_nonroutine_over_unknown_accessibility(self):
        x=census(record('ok'),record('no',accessible=None,routine=False))
        self.assertEqual((x['sample_rate'],x['excluded_count']),('1/1',1))
    def test_genuinely_unknown_still_withheld(self):
        x=census(record('ok'),record('uncertain',authorized=None))
        self.assertEqual((x['sample_rate'],x['unknown_eligibility_count']),('WITHHELD_UNKNOWN_ELIGIBILITY',1))
    def test_unknown_does_not_override_known_manual_failure(self):
        x=census(record('ok'),record('manual',automated=False),record('pending',outcome='PENDING'))
        self.assertEqual((x['sample_rate'],x['eligible_denominator'],x['automated_numerator']),('1/3',3,1))
    def test_readback_gap_remains_in_denominator(self):
        self.assertEqual(census(record('ok'),record('gap',source_readback='GAP'))['sample_rate'],'1/2')
    def test_conflicting_private_access_still_rejected(self):
        self.assertNotEqual(execute({'schema_version':2,'records':[record('x',scope='PRIVATE',accessible=True,authorized=None)]}).returncode,0)
    def test_duplicate_id_rejected(self):
        self.assertNotEqual(execute({'schema_version':2,'records':[record('x'),record('x')]}).returncode,0)
    def test_duplicate_json_key_rejected(self):
        self.assertNotEqual(execute('{"schema_version":2,"records":[],"records":[]}').returncode,0)
    def test_no_project_promotion(self):
        x=census(record('ok'))
        self.assertEqual((x['project_rate'],x['evidence_class'],x['claim_ceiling']),('NOT_COMPUTABLE','UNVERIFIED_SAMPLE_ONLY','C1_DESCRIPTIVE_ONLY'))
    def test_empty_denominator(self):
        self.assertEqual(census(record('x',authorized=False))['sample_rate'],'NOT_COMPUTABLE_ZERO_DENOMINATOR')

if __name__ == '__main__':
    unittest.main()
