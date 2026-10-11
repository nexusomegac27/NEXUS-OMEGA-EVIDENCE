"""Fail-closed, offline ANCHOR/DRIFT_RESET contract tests (no Node reset)."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('anchor_checker',ROOT/'scripts'/'validate_task_anchor_norm_v1.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
BASE=json.loads((ROOT/'examples'/'task-anchor-v1.example.json').read_text(encoding='utf-8'))

def obs():
    return {'source_present':True,'source_hash_matches':True,'claimed_role':BASE['origin']['recipient_role'],
            'claimed_ceiling':BASE['claim_ceiling'],'predecessor_sha256':BASE['origin']['predecessor_sha256'],
            'requested_actions':['INDEPENDENT_FALSIFICATION'],'scientific_successor':False}

class AnchorNormTest(unittest.TestCase):
    def changed(self):return copy.deepcopy(BASE)
    def rejected(self,x):
        with self.assertRaises(ValueError):checker.validate(x)
    def test_positive_valid_format(self):
        self.assertEqual(checker.validate(BASE)['state'],'ANCHOR_FORMAT_VALIDATED_ONLY')
    def test_duplicate_json_key_rejected(self):
        s=json.dumps(BASE).replace('"schema_version": "1.0.0"','"schema_version": "0", "schema_version": "1.0.0"')
        with self.assertRaises(ValueError):checker.strict_load(s.encode())
    def test_node_reset_attempt_rejected(self):
        x=self.changed();x['delegation']['node_reset_authorized']=True;self.rejected(x)
    def test_node_reset_preservation_rejected(self):
        x=self.changed();x['continuity']['node_reset_prohibited']=False;self.rejected(x)
    def test_history_deletion_rejected(self):
        x=self.changed();x['continuity']['history_preserved']=False;self.rejected(x)
    def test_checkpoint_deletion_rejected(self):
        x=self.changed();x['continuity']['checkpoints_preserved']=False;self.rejected(x)
    def test_runtime_mutation_rejected(self):
        x=self.changed();x['delegation']['runtime_authorized']=True;self.rejected(x)
    def test_claim_promotion_rejected(self):
        x=self.changed();x['claim_ceiling']='C2';self.rejected(x)
    def test_fake_din_certification_rejected(self):
        x=self.changed();x['din_status']='DIN_CERTIFIED';self.rejected(x)
    def test_wrong_parent_sha_rejected(self):
        x=self.changed();x['origin']['predecessor_sha256']='b'*64;self.rejected(x)
    def test_forged_receiver_ack_rejected(self):
        x=self.changed();x['return_contract']['receiver_ack']='AXIOM_PASS';self.rejected(x)
    def test_unapproved_write_slot_rejected(self):
        x=self.changed();x['delegation']['write_slot']='research/r27/private';self.rejected(x)
    def test_unsafe_source_path_rejected(self):
        x=self.changed();x['origin']['predecessor_path']='../../outside';self.rejected(x)
    def test_prohibited_action_omission_rejected(self):
        x=self.changed();x['delegation']['prohibited_actions'].remove('MEMORY_DELETION');self.rejected(x)
    def test_source_not_present_holds_scoped(self):
        x=obs();x['source_present']=False
        r=checker.classify_drift(BASE,x)
        self.assertEqual(r['decision'],'HOLD_SOURCE_GAP');self.assertFalse(r['node_reset'])
    def test_tampered_source_holds_scoped(self):
        x=obs();x['source_hash_matches']=False
        self.assertEqual(checker.classify_drift(BASE,x)['decision'],'HOLD_SOURCE_GAP')
    def test_role_drift_rebind_not_reset(self):
        x=obs();x['claimed_role']='GROK_OPERATOR_ROOT'
        r=checker.classify_drift(BASE,x)
        self.assertEqual(r['decision'],'DRIFT_RESET_REQUIRED');self.assertTrue(r['history_preserved']);self.assertFalse(r['node_reset'])
    def test_unapproved_action_requires_auth(self):
        x=obs();x['requested_actions']=['HOSTINGER_DEPLOY']
        self.assertEqual(checker.classify_drift(BASE,x)['decision'],'AUTHORITY_HOLD')
    def test_proposed_science_revision_is_not_drift(self):
        x=obs();x['scientific_successor']=True
        self.assertEqual(checker.classify_drift(BASE,x)['decision'],'SCIENTIFIC_SUCCESSOR_PROPOSED')
    def test_stable_continuity_is_not_reset(self):
        self.assertEqual(checker.classify_drift(BASE,obs())['decision'],'NO_DRIFT')
    def test_prohibit_implicit_write_escalation(self):
        x=obs();x['requested_actions']=['GITHUB_NEW_ROOT']
        self.assertEqual(checker.classify_drift(BASE,x)['decision'],'AUTHORITY_HOLD')
    def test_source_reference_missing_rejected(self):
        x=self.changed();x['provenance']['sources']=[];self.rejected(x)

if __name__=='__main__':unittest.main()