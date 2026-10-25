#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent C1 oracle: unknown rows invalidate a complete sample-rate claim.
Synthetic reducer outputs only; no real handoff or project-wide rate measured.
"""
import copy, importlib.util, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
P = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('HANDOFF_CANDIDATE', str(P/'alpha_handoff_uncertainty_rate_guard_v1_20261025.py')))
spec = importlib.util.spec_from_file_location('candidate_under_test', TARGET)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def fixture(statuses):
    d = sum(s.startswith('ELIGIBLE_') for s in statuses)
    n = statuses.count('ELIGIBLE_AUTOMATED')
    return dict(claim_ceiling='C1_DESCRIPTIVE_ONLY',
        measurement_scope='CALLER_ASSERTED_SAMPLE_ONLY_NOT_INDEPENDENTLY_AUDITED',
        project_handoff_automation_rate='NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS',
        sample_eligible_denominator=d, sample_automated_numerator=n,
        sample_rate_percent=round(100*n/d,2) if d else None,
        unknown_or_unverified=statuses.count('UNKNOWN'),
        excluded_out_of_scope=statuses.count('EXCLUDED'),
        outcomes=[dict(index=i,id='h'+str(i),status=s,reason='SYNTHETIC') for i,s in enumerate(statuses)])

class FrozenOracle(unittest.TestCase):
    def test_01_complete(self):
        for statuses, rate in [(['ELIGIBLE_AUTOMATED'],100.0),(['ELIGIBLE_FAILED'],0.0),
                               (['ELIGIBLE_AUTOMATED','ELIGIBLE_FAILED'],50.0),
                               (['ELIGIBLE_AUTOMATED','EXCLUDED'],100.0)]:
            r=module.guard_reducer_result(fixture(statuses)); self.assertEqual(r['sample_rate_percent'],rate)
            self.assertEqual(r['sample_rate_status'],'COMPLETE_CALLER_ASSERTED_SAMPLE')
    def test_02_unknown_withheld(self):
        for statuses in [['ELIGIBLE_AUTOMATED','UNKNOWN','UNKNOWN'],['ELIGIBLE_AUTOMATED','UNKNOWN'],
                         ['UNKNOWN'],['ELIGIBLE_FAILED','UNKNOWN'],['EXCLUDED','UNKNOWN']]:
            r=module.guard_reducer_result(fixture(statuses)); self.assertIsNone(r['sample_rate_percent'])
            self.assertEqual(r['sample_rate_status'],'WITHHELD_UNRESOLVED_ROWS')
    def test_03_no_denominator(self):
        for statuses in [[],['EXCLUDED']]:
            r=module.guard_reducer_result(fixture(statuses)); self.assertIsNone(r['sample_rate_percent'])
            self.assertEqual(r['sample_rate_status'],'NO_ELIGIBLE_ROWS')
    def test_04_counts_forged(self):
        for key,value in [('sample_eligible_denominator',99),('sample_automated_numerator',99),
                          ('unknown_or_unverified',1),('excluded_out_of_scope',1)]:
            r=fixture(['ELIGIBLE_AUTOMATED']);r[key]=value
            with self.assertRaisesRegex(ValueError,'REDUCER_COUNT_MISMATCH'):module.guard_reducer_result(r)
    def test_05_invalid_counts(self):
        for value in [True,-1,1.5,'1',None]:
            r=fixture(['ELIGIBLE_AUTOMATED']);r['sample_eligible_denominator']=value
            with self.assertRaisesRegex(ValueError,'INVALID_REDUCER_COUNT'):module.guard_reducer_result(r)
    def test_06_bad_outcomes(self):
        for change in [dict(status='MAGIC_PASS'),dict(index=99),dict(index=True)]:
            r=fixture(['UNKNOWN']);r['outcomes'][0].update(change)
            with self.assertRaisesRegex(ValueError,'INVALID_REDUCER_OUTCOME'):module.guard_reducer_result(r)
        r=fixture(['UNKNOWN']);r['outcomes']={}
        with self.assertRaisesRegex(ValueError,'INVALID_REDUCER_OUTCOMES'):module.guard_reducer_result(r)
    def test_07_claim_guards(self):
        for key,value,error in [('claim_ceiling','C2','CLAIM_CEILING_MISMATCH'),
                                ('measurement_scope','INDEPENDENTLY_AUDITED','MEASUREMENT_SCOPE_MISMATCH'),
                                ('project_handoff_automation_rate',100,'UNAUTHORIZED_PROJECT_RATE')]:
            r=fixture(['ELIGIBLE_AUTOMATED']);r[key]=value
            with self.assertRaisesRegex(ValueError,error):module.guard_reducer_result(r)
    def test_08_forged_rate(self):
        r=fixture(['ELIGIBLE_AUTOMATED','ELIGIBLE_FAILED']);r['sample_rate_percent']=100
        with self.assertRaisesRegex(ValueError,'REPORTED_RATE_MISMATCH'):module.guard_reducer_result(r)
    def test_09_immutable_and_deterministic(self):
        r=fixture(['ELIGIBLE_AUTOMATED','UNKNOWN']);old=copy.deepcopy(r)
        self.assertEqual(module.guard_reducer_result(r),module.guard_reducer_result(r));self.assertEqual(r,old)
    def test_10_cli(self):
        for statuses,expected in [(['ELIGIBLE_AUTOMATED','UNKNOWN'],None),(['ELIGIBLE_AUTOMATED'],100.0)]:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'result.json';p.write_text(json.dumps(fixture(statuses)),encoding='utf-8')
                cp=subprocess.run([sys.executable,str(TARGET),str(p)],capture_output=True,text=True)
                self.assertEqual(cp.returncode,0,cp.stderr)
                self.assertEqual(json.loads(cp.stdout)['sample_rate_percent'],expected)
    def test_11_cli_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'result.json';p.write_text('{}',encoding='utf-8')
            cp=subprocess.run([sys.executable,str(TARGET),str(p)],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0);self.assertEqual(cp.stdout,'')

if __name__=='__main__':unittest.main(verbosity=2)
