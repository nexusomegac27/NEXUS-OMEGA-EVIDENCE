#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen C1 synthetic oracle: strict JSON intake must compose with outcome/rate guard.
No actual project census, external actor authentication or production claim.
"""
import importlib.util, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('HANDOFF_CANDIDATE', str(HERE/'alpha_handoff_composed_strict_intake_v1_20261026.py')))
spec = importlib.util.spec_from_file_location('tested', TARGET)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def row(i='ok'):
    return dict(id=i, public=True, routine=True, authorized=True, source_access='BYTE_VERIFIED',
                source_readback=True, source_sha256='a'*64, source_bytes=18, source_commit='b'*40,
                delivery='RECEIVER_VERIFIED', receiver_readback=True, receiver_sha256='a'*64,
                receiver_bytes=18, receiver_commit='b'*40, manual_reprompt=False)

def run(rows): return module.reduce_json_text(json.dumps(rows))

class FrozenOracle(unittest.TestCase):
    def test_unknown_withholds_100_percent(self):
        x=row('unknown'); x['source_access']='METADATA_ONLY'
        y=run([row(),x]); self.assertEqual((y['sample_automated_numerator'],y['sample_eligible_denominator'],y['unknown_or_unverified']),(1,1,1))
        self.assertIsNone(y['sample_rate_percent']); self.assertEqual(y['sample_rate_status'],'WITHHELD_UNRESOLVED_ROWS')
    def test_valid_sample_preserved(self):
        y=run([row()]); self.assertEqual(y['sample_rate_percent'],100.0)
        self.assertEqual(y['sample_rate_status'],'COMPLETE_CALLER_ASSERTED_SAMPLE')
    def test_eligible_failure_denominator(self):
        x=row('failed');x['delivery']='FAILED';y=run([row(),x]);self.assertEqual((y['sample_automated_numerator'],y['sample_eligible_denominator'],y['sample_rate_percent']),(1,2,50.0))
    def test_malformed_delivery_isolated(self):
        x=row('bad');x['delivery']=[];y=run([row(),x]);self.assertEqual(y['outcomes'][1]['reason'],'DELIVERY_STATE_INVALID_TYPE')
        self.assertEqual(y['sample_eligible_denominator'],2)
    def test_duplicate_json_key(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY'):module.reduce_json_text('[{"public":true,"public":false}]')
    def test_nonfinite_json(self):
        for token in ('NaN','Infinity','-Infinity','1e400','-1e400'):
            with self.subTest(token=token):
                with self.assertRaisesRegex(ValueError,'NONFINITE_JSON_NUMBER'):module.reduce_json_text('[{"extra":'+token+'}]')
    def test_duplicate_ids_unknown(self):
        y=run([row('dup'),row('dup')]);self.assertEqual(y['unknown_or_unverified'],2);self.assertIsNone(y['sample_rate_percent'])
    def test_manual_reprompt_not_success(self):
        x=row();x['manual_reprompt']=True;y=run([x]);self.assertEqual((y['sample_automated_numerator'],y['sample_eligible_denominator']),(0,1))
    def test_project_rate_never_promoted(self):
        y=run([row()]);self.assertEqual(y['project_handoff_automation_rate'],'NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS')
    def test_nonarray_and_empty(self):
        self.assertIsNone(module.reduce_json_text('[]')['sample_rate_percent'])
        with self.assertRaises(ValueError):module.reduce_json_text('{}')
    def test_fuzz_mixed_unknown(self):
        for i in range(100):
            x=row('u'+str(i));x['source_access']='METADATA_ONLY';y=run([row('v'+str(i)),x]);self.assertIsNone(y['sample_rate_percent'])
    def test_cli_unknown_withheld(self):
        x=row('unknown');x['source_access']='METADATA_ONLY'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text(json.dumps([row(),x]),encoding='utf-8')
            cp=subprocess.run([sys.executable,str(TARGET),str(p)],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr);self.assertIsNone(json.loads(cp.stdout)['sample_rate_percent'])
    def test_pinned_source_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            names=('alpha_handoff_composed_strict_intake_v1_20261026.py','alpha_handoff_strict_json_intake_v2_20261025.py',
                   'alpha_handoff_strict_json_intake_v1_20261025.py','alpha_handoff_eligibility_reducer_v2_20261025.py',
                   'alpha_handoff_eligibility_reducer_v1_20261025.py','alpha_handoff_outcome_identity_guard_v2_20261025.py',
                   'alpha_handoff_uncertainty_rate_guard_v1_20261025.py')
            for name in names:
                p=HERE/name
                if p.exists():(root/name).write_bytes(p.read_bytes())
            p=root/'alpha_handoff_outcome_identity_guard_v2_20261025.py';p.write_bytes(p.read_bytes()+b'\n# tampered\n')
            sample=root/'x.json';sample.write_text(json.dumps([row()]),encoding='utf-8')
            cp=subprocess.run([sys.executable,str(root/names[0]),str(sample)],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0);self.assertEqual(cp.stdout,'')

if __name__=='__main__':unittest.main(verbosity=2)
