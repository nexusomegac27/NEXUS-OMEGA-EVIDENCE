"""NEXUS V1.2 bounded independent research fixtures; no network, no production keys."""
import base64,copy,datetime,importlib,io,json,os,pathlib,sys,tempfile,unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import nexus_anchor_v12 as n

class DeltaTest(unittest.TestCase):
    def setUp(self):
        self.key=Ed25519PrivateKey.generate();self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.payload=pathlib.Path(self.t.name)/'sample.zip';self.payload.write_bytes(b'NEXUS sample bytes only')
        self.f=self.payload.name
    def sample(self,host='github.com'):
        return n.sign({'schema':n.SCHEMA,'object':'NEXUS_ARCHIVE_DELTA_TEST_01','lane':'test-01',
          'sequence':1,'previous_manifest_sha256':None,
          'issued_at':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
          'claim_ceiling':'C1_DESCRIPTIVE_ONLY','classification':'PUBLIC_SAFE',
          'payload':{'filename':self.f,'bytes':self.payload.stat().st_size,
            'sha256':n.file_info(self.payload)[1],'url':'https://'+host+'/payload.zip'}},self.key)
    def test_01_decimal_loopback_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('2130706433'))
    def test_02_short_ip_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('127.1'))
    def test_03_hex_loopback_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('0x7f.0.0.1'))
    def test_04_internal_domain_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('metadata.google.internal'))
    def test_05_trailing_dot_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('localhost.'))
    def test_06_single_label_denied(self):
        with self.assertRaises(n.HandshakeError):n.check_schema(self.sample('intranet'))
    def test_07_valid_host_allowed(self):
        n.check_schema(self.sample('github.com'))
    def test_08_signature_padding_bits_denied(self):
        m=self.sample();b=m['signature']['base64']; chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        idx=chars.index(b[-3]); alt=(idx//16)*16+((idx%16+1)%16)
        assert alt!=idx
        m['signature']['base64']=b[:-3]+chars[alt]+b[-2:]
        # Valid decoding unchanged, despite altered representation
        self.assertEqual(base64.b64decode(b,validate=True),base64.b64decode(m['signature']['base64'],validate=True))
        with self.assertRaises(n.HandshakeError):n.check_schema(m)
    def test_09_future_timestamp_denied(self):
        m=self.sample();m['issued_at']='2099-01-01T00:00:00Z'
        with self.assertRaises(n.HandshakeError):n.check_schema(m)
    def test_10_reserved_device_name_denied(self):
        m=self.sample();m['payload']['filename']='CON.txt'
        with self.assertRaises(n.HandshakeError):n.check_schema(m)
    def test_11_ads_stream_filename_denied(self):
        m=self.sample();m['payload']['filename']='payload:stream.zip'
        with self.assertRaises(n.HandshakeError):n.check_schema(m)
    def test_12_rtl_control_filename_denied(self):
        m=self.sample();m['payload']['filename']='saf\u202ee.zip'
        with self.assertRaises(n.HandshakeError):n.check_schema(m)
    def test_13_wrong_signed_filename_denied(self):
        m=self.sample();other=pathlib.Path(self.t.name)/'changed.zip';other.write_bytes(self.payload.read_bytes())
        args=type('A',(),{'manifest':str(pathlib.Path(self.t.name)/'m.json'),'pubkey':str(pathlib.Path(self.t.name)/'pk.pem'),
            'pinned_key_sha256':n.spki_hash(self.key.public_key()),'payload':str(other),'witness_only':False,'record':False,'state_file':None})
        from cryptography.hazmat.primitives import serialization
        pathlib.Path(args.pubkey).write_bytes(self.key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
        pathlib.Path(args.manifest).write_text(json.dumps(m))
        with self.assertRaises(n.HandshakeError):n.verify(args)
    def test_14_witness_only_no_ack(self):
        m=self.sample();args=type('A',(),{'manifest':str(pathlib.Path(self.t.name)/'m.json'),'pubkey':str(pathlib.Path(self.t.name)/'pk.pem'),
            'pinned_key_sha256':n.spki_hash(self.key.public_key()),'payload':None,'witness_only':True,'record':True,'state_file':None})
        from cryptography.hazmat.primitives import serialization
        pathlib.Path(args.pubkey).write_bytes(self.key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
        pathlib.Path(args.manifest).write_text(json.dumps(m))
        with self.assertRaises(n.HandshakeError):n.verify(args)
    def test_15_host_validator_no_network(self):
        n.validate_shared_host('raw.githubusercontent.com')
    def test_16_reserved_future_block_preserves_archival_past(self):
        m=self.sample();m['issued_at']='2025-01-01T00:00:00Z';n.check_schema(m)

if __name__=='__main__':unittest.main()
