import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from test_feed import RECEIPT,STATE,put
ROOT=Path(__file__).resolve().parents[1]

class PHPFeedTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();put(self.root,Path('research/bodytwin/state.json'),STATE)
  put(self.root,Path('bodytwin/live/receipts.public.json'),RECEIPT)
 def run_php(self):
  return subprocess.run(['php',str(ROOT/'ops/refresh_public_feed.php'),'--document-root',str(self.root)],capture_output=True,text=True,timeout=5)
 def test_first_tick(self):
  r=self.run_php();self.assertEqual(r.returncode,0,r.stderr)
  x=json.loads((self.root/'bodytwin/live/current.json').read_text())
  self.assertEqual(x['producer']['seq'],1)
  self.assertTrue(x['producer']['source_changed'])
  self.assertEqual(x['bodytwin']['validated'],'NO')
 def test_followon_same_source(self):
  a=self.run_php();self.assertEqual(a.returncode,0,a.stderr)
  # Host timestamps have seconds granularity: no racing second run, which must HOLD.
  b=self.run_php();self.assertNotEqual(b.returncode,0)
  self.assertIn('CLOCK_ROLLBACK',b.stderr)
 def test_public_source_missing(self):
  (self.root/'research/bodytwin/state.json').unlink();r=self.run_php()
  self.assertNotEqual(r.returncode,0);self.assertIn('SOURCE',r.stderr)
 def test_fake_consent(self):
  v=dict(STATE);v['CONSENT_BIND']='GRANTED';put(self.root,Path('research/bodytwin/state.json'),v)
  r=self.run_php();self.assertNotEqual(r.returncode,0)
 def test_phi_injection(self):
  v=dict(RECEIPT);v['private_medical_record']='secret';put(self.root,Path('bodytwin/live/receipts.public.json'),v)
  r=self.run_php();self.assertNotEqual(r.returncode,0)
 def test_untrusted_future_date(self):
  v=dict(RECEIPT);v['source_date']='2099-11-07';put(self.root,Path('bodytwin/live/receipts.public.json'),v)
  r=self.run_php();self.assertNotEqual(r.returncode,0)
 def test_output_not_replaced_on_bad_input(self):
  r=self.run_php();self.assertEqual(r.returncode,0,r.stderr)
  old=(self.root/'bodytwin/live/current.json').read_bytes()
  v=dict(STATE);v['BODYTWIN_VALIDATED']='YES';put(self.root,Path('research/bodytwin/state.json'),v)
  r=self.run_php();self.assertNotEqual(r.returncode,0)
  self.assertEqual((self.root/'bodytwin/live/current.json').read_bytes(),old)
 def test_output_expected_schema(self):
  self.assertEqual(self.run_php().returncode,0)
  obj=json.loads((self.root/'bodytwin/live/current.json').read_text())
  self.assertEqual(set(obj),{'schema','claim_ceiling','trust','producer','sources','bodytwin','research','gates'})
 def test_nonexistent_docroot(self):
  r=subprocess.run(['php',str(ROOT/'ops/refresh_public_feed.php'),'--document-root',str(self.root/'MISSING')],capture_output=True,text=True)
  self.assertNotEqual(r.returncode,0)
 def test_missing_receipt(self):
  (self.root/'bodytwin/live/receipts.public.json').unlink()
  self.assertNotEqual(self.run_php().returncode,0)

if __name__=='__main__':unittest.main()
