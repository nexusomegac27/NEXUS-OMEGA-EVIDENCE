import copy
from datetime import datetime,timedelta,timezone
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'ops'))
import refresh_public_feed as F

RECEIPT=json.loads((pathlib.Path(__file__).resolve().parents[1]/'site/receipts.public.json').read_text())
STATE={'schema':'nexus-research-bodytwin-state/1','object':'BODYTWIN_PUBLIC_SURFACE',
 'BODYTWIN':'RESEARCH_FOUNDATION_C1','BODYTWIN_VALIDATED':'NO','CONSENT_BIND':'OPEN','TRIAL_001':'DESIGNED_NOT_EXECUTED',
 'layers':['L0','L1','L2','L3','UNKNOWN_UNOBSERVED'],'pipeline':['Capture','Normalize','Align','Refine','Metrics'],
 'invariants':['RAW_NE_REFINED','PHOTOREALISM_GAIN_MAY_CAUSE_IDENTITY_LOSS','NO_PRIVATE_HUMAN_REFERENCE_MEDIA'],
 'claim_ceiling':'C1_DESCRIPTIVE_ONLY','claim_promotion':False}
NOW=datetime(2026,11,7,19,0,0,tzinfo=timezone.utc)

def put(root,p,v):
 f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,sort_keys=True)+'\n',encoding='utf8')

class FeedTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=pathlib.Path(self.tmp.name).resolve()
  put(self.root,F.PUB_STATUS,STATE);put(self.root,F.PUB_RECEIPT,RECEIPT)
 def update(self, s=None,r=None):
  if s is not None:put(self.root,F.PUB_STATUS,s)
  if r is not None:put(self.root,F.PUB_RECEIPT,r)
 def reject(self,s=None,r=None):
  self.update(s,r)
  with self.assertRaises(F.ContractError): F.build(self.root,NOW)
 def test_initial(self):
  o=F.build(self.root,NOW);self.assertEqual(o['producer']['seq'],1)
  self.assertTrue(o['producer']['source_changed'])
  self.assertEqual(o['bodytwin']['validated'],'NO')
  self.assertEqual(o['research']['node_pass'],177)
 def test_atomic_write_and_stable_sha(self):
  v=F.build(self.root,NOW);h=F.write_atomic(self.root,v)
  self.assertEqual(h, __import__('hashlib').sha256((self.root/F.OUTPUT).read_bytes()).hexdigest())
  self.assertEqual(json.loads((self.root/F.OUTPUT).read_bytes())['producer']['seq'],1)
 def test_sequence_second_tick_no_change(self):
  a=F.build(self.root,NOW);F.write_atomic(self.root,a)
  b=F.build(self.root,NOW+timedelta(minutes=5));self.assertEqual(b['producer']['seq'],2)
  self.assertFalse(b['producer']['source_changed']);self.assertEqual(a['producer']['last_change_utc'],b['producer']['last_change_utc'])
 def test_actual_changed_source_updates_change_time(self):
  a=F.build(self.root,NOW);F.write_atomic(self.root,a)
  s=copy.deepcopy(STATE);s['layers'].reverse();self.update(s=s)
  b=F.build(self.root,NOW+timedelta(minutes=5));self.assertTrue(b['producer']['source_changed'])
  self.assertEqual(b['producer']['last_change_utc'],'2026-11-07T19:05:00Z')
 def test_existing_unrecognized_feed_failclosed(self):
  (self.root/F.OUTPUT).write_text('{}')
  with self.assertRaises(F.ContractError):F.build(self.root,NOW)
 def test_missing_status(self):
  (self.root/F.PUB_STATUS).unlink();self.reject()
 def test_missing_receipt(self):
  (self.root/F.PUB_RECEIPT).unlink();self.reject()
 def test_extra_phi_field(self):
  s=copy.deepcopy(STATE);s['patient']='SECRET';self.reject(s=s)
 def test_promote_c2(self):
  s=copy.deepcopy(STATE);s['claim_ceiling']='C2_PROVEN';self.reject(s=s)
 def test_false_validation(self):
  s=copy.deepcopy(STATE);s['BODYTWIN_VALIDATED']='YES';self.reject(s=s)
 def test_false_consent(self):
  s=copy.deepcopy(STATE);s['CONSENT_BIND']='GRANTED';self.reject(s=s)
 def test_false_trial(self):
  s=copy.deepcopy(STATE);s['TRIAL_001']='EXECUTED';self.reject(s=s)
 def test_duplicate_layers(self):
  s=copy.deepcopy(STATE);s['layers'][0]=s['layers'][1];self.reject(s=s)
 def test_missing_invariant(self):
  s=copy.deepcopy(STATE);s['invariants'].pop();self.reject(s=s)
 def test_mutation_raw_ne_refined(self):
  s=copy.deepcopy(STATE);s['invariants'][0]='RAW_EQUALS_REFINED';self.reject(s=s)
 def test_bogus_bool(self):
  s=copy.deepcopy(STATE);s['claim_promotion']='false';self.reject(s=s)
 def test_extra_receipt_secret(self):
  r=copy.deepcopy(RECEIPT);r['email']='x@example.com';self.reject(r=r)
 def test_false_sensor(self):
  r=copy.deepcopy(RECEIPT);r['gates']['physical_imu']='ACTIVE';self.reject(r=r)
 def test_false_a72(self):
  r=copy.deepcopy(RECEIPT);r['gates']['a72']='CLOSED';self.reject(r=r)
 def test_false_hostinger_stage(self):
  r=copy.deepcopy(RECEIPT);r['gates']['r13_stage_ii']='PASS';self.reject(r=r)
 def test_counter_overflow(self):
  r=copy.deepcopy(RECEIPT);r['windows']['mutation_pass']=999;self.reject(r=r)
 def test_counter_type_bool(self):
  r=copy.deepcopy(RECEIPT);r['windows']['schema_pass']=True;self.reject(r=r)
 def test_future_source_date(self):
  r=copy.deepcopy(RECEIPT);r['source_date']='2027-11-07';self.reject(r=r)
 def test_bad_date(self):
  r=copy.deepcopy(RECEIPT);r['source_date']='2026-02-30';self.reject(r=r)
 def test_missing_public_state_file_prevents_overwrite(self):
  prior=F.build(self.root,NOW);F.write_atomic(self.root,prior)
  original=(self.root/F.OUTPUT).read_bytes();(self.root/F.PUB_STATUS).unlink()
  with self.assertRaises(F.ContractError):F.build(self.root,NOW+timedelta(minutes=5))
  self.assertEqual((self.root/F.OUTPUT).read_bytes(),original)
 def test_symlink_source_rejected(self):
  p=self.root/F.PUB_STATUS;p.unlink();p.symlink_to(self.root/F.PUB_RECEIPT)
  self.reject()
 def test_symlink_output_rejected(self):
  (self.root/F.OUTPUT).symlink_to(self.root/F.PUB_RECEIPT)
  self.reject()
 def test_nonsensical_clock_rejected(self):
  with self.assertRaises(F.ContractError):F.build(self.root,datetime(2026,11,7))
 def test_no_network_code(self):
  txt=pathlib.Path(F.__file__).read_text()
  self.assertNotIn('requests.get',txt);self.assertNotIn('urllib.request',txt)
 def test_correct_source_urls(self):
  a=F.build(self.root,NOW)
  self.assertEqual(a['sources']['bodytwin_state']['url'],'/research/bodytwin/state.json')
  self.assertEqual(a['sources']['research_receipt']['url'],'/bodytwin/live/receipts.public.json')

if __name__=='__main__':unittest.main()
