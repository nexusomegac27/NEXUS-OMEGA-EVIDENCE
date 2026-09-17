# SPDX-License-Identifier: Apache-2.0
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_delivery import verify, EXCLUDED

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='nexus-delivery-fixture-')
        self.root=Path(self.temp.name)
        self.payload=b'public synthetic fixture'
        (self.root/'payload.txt').write_bytes(self.payload)
        self.seal()

    def tearDown(self):
        self.temp.cleanup()

    def seal(self, ceiling='C1_DESCRIPTIVE_ONLY'):
        def write(name,obj):
            data=json.dumps(obj,sort_keys=True).encode()
            (self.root/name).write_bytes(data)
            return hashlib.sha256(data).hexdigest()
        mh=write('OUTPUT_MANIFEST.json',{'claim_ceiling':ceiling,'excludes':sorted(EXCLUDED),
          'files':[{'path':'payload.txt','bytes':len(self.payload),'sha256':hashlib.sha256(self.payload).hexdigest()}]})
        rh=write('RETURN.json',{'claim_ceiling':ceiling,'output_manifest_sha256':mh,
          'live_publication':False,'merge':False,'claim_promotion':False,'foundation_promotion':False,
          'scientific_validation_established':False,'remaining_gaps':['fixture-gap']})
        write('DELIVERY_HANDSHAKE.json',{'claim_ceiling':ceiling,'output_manifest_sha256':mh,'return_sha256':rh})

    def test_valid_delivery(self):
        self.assertEqual(verify(self.root)['status'],'PASS')

    def test_byte_tampering_rejected(self):
        (self.root/'payload.txt').write_bytes(b'tampered')
        self.assertEqual(verify(self.root)['status'],'FAIL')

    def test_undeclared_file_rejected(self):
        (self.root/'extra.txt').write_bytes(b'extra')
        self.assertIn('INVENTORY_MISMATCH',verify(self.root)['errors'])

    def test_claim_promotion_rejected(self):
        self.seal('C2')
        self.assertIn('CEILING_MISMATCH',verify(self.root)['errors'])

    def test_return_tampering_rejected(self):
        data=json.loads((self.root/'RETURN.json').read_text())
        data['live_publication']=True
        (self.root/'RETURN.json').write_text(json.dumps(data))
        self.assertIn('HANDSHAKE_MISMATCH',verify(self.root)['errors'])
