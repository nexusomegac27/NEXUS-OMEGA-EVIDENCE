#!/usr/bin/env python3
"""Separate black-box evaluator for the read-only fixture collision audit candidate."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CANDIDATE = Path(__file__).with_name('alpha_oracle_fixture_collision_audit_v1_20261026.py')
RECORD = '''def record(id, **kwargs):
    r = {"id": id, "scope": "PUBLIC", "accessible": True, "authorized": True}
    r.update(kwargs)
    return r
'''

def source(positive='record("a",scope="PRIVATE")', negative='record("a",scope="PRIVATE",accessible=True)', negative_method='assertNotEqual'):
    return RECORD + f'''\ndef output(x): pass\ndef run(x): pass\nclass TestOracle:\n    def test_positive(self):\n        r = output({{"records":[{positive}]}})\n    def test_negative(self):\n        self.{negative_method}(run({{"records":[{negative}]}}).returncode,0)\n'''

def check(src):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'oracle.py'
        p.write_text(src,encoding='utf-8')
        proc=subprocess.run([sys.executable,str(CANDIDATE),str(p)],capture_output=True,text=True,timeout=5)
        return proc.returncode,json.loads(proc.stdout)

class FrozenOracleCollisionAudit(unittest.TestCase):
    def test_implicit_explicit_default_conflict(self):
        code,data=check(source())
        self.assertEqual((code,data['status'],data['supported_cases'],len(data['conflicts'])),(1,'CONFLICT',2,1))
    def test_explicit_default_conflict(self):
        code,data=check(source('record("a",scope="PRIVATE",accessible=True)'))
        self.assertEqual((code,data['status']), (1,'CONFLICT'))
    def test_distinct_payload_not_conflict(self):
        code,data=check(source(negative='record("a",scope="PRIVATE",accessible=False)'))
        self.assertEqual((code,data['status']), (0,'NO_CONFLICT_IN_SUPPORTED_CASES'))
    def test_same_expectation_not_conflict(self):
        code,data=check(source(negative_method='assertEqual'))
        self.assertEqual((code,data['status']), (0,'NO_CONFLICT_IN_SUPPORTED_CASES'))
    def test_key_order_canonicalized(self):
        code,data=check(source(positive='record("a",accessible=True,scope="PRIVATE")'))
        self.assertEqual((code,data['status']), (1,'CONFLICT'))
    def test_nonliteral_fails_closed(self):
        code,data=check(source(positive='record("a",scope=lookup())'))
        self.assertEqual((code,data['status']), (1,'INCOMPLETE'))
    def test_missing_record_rejected(self):
        code,data=check(source().replace(RECORD,''))
        self.assertEqual((code,data['status']), (2,'SOURCE_UNSUPPORTED'))
    def test_syntax_error_rejected(self):
        code,data=check('def record(:')
        self.assertEqual((code,data['status']), (2,'SOURCE_UNSUPPORTED'))
    def test_malicious_expression_not_executed(self):
        code,data=check(source(positive='record("a",scope=__import__("os").system("touch /tmp/axiom-should-not-exist"))'))
        self.assertEqual((code,data['status']), (1,'INCOMPLETE'))
        self.assertFalse(Path('/tmp/axiom-should-not-exist').exists())
    def test_oracle_source_not_executed(self):
        code,data=check(source()+'\nraise RuntimeError("if executed")\n')
        self.assertEqual((code,data['status']), (1,'CONFLICT'))
        self.assertEqual(data['source_execution'],'NOT_PERFORMED')
    def test_no_supported_cases_incomplete(self):
        code,data=check(RECORD+'\nclass TestOracle:\n def test_x(self):\n  pass\n')
        self.assertEqual((code,data['status']), (1,'INCOMPLETE'))
    def test_changed_record_default_changes_identity(self):
        s=source().replace('"accessible": True','"accessible": False')
        code,data=check(s)
        self.assertEqual((code,data['status']), (0,'NO_CONFLICT_IN_SUPPORTED_CASES'))
    def test_positive_exit_equal_recognized(self):
        s=RECORD+'''\ndef run(x): pass\nclass TestOracle:\n def test_a(self): self.assertEqual(run({"records":[record("a")]}).returncode,0)\n def test_b(self): self.assertNotEqual(run({"records":[record("a")]}).returncode,0)\n'''
        code,data=check(s)
        self.assertEqual((code,data['status']), (1,'CONFLICT'))
    def test_duplicate_input_different_id_no_collision(self):
        code,data=check(source(negative='record("b",scope="PRIVATE")'))
        self.assertEqual((code,data['status']), (0,'NO_CONFLICT_IN_SUPPORTED_CASES'))
    def test_no_self_approval(self):
        _,data=check(source())
        self.assertNotIn('ACCEPTED',str(data))
        self.assertEqual(data['claim_ceiling'],'C1_DESCRIPTIVE_ONLY')

if __name__=='__main__':
    unittest.main()
