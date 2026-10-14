"""NEXUS Anchor V1.1 deterministic tests; generated keys are ephemeral SANDBOX ONLY."""
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

TOOL=Path(__file__).resolve().parents[1]/'nexus_anchor_v11.py'
sys.path.insert(0,str(TOOL.parent))
import nexus_anchor_v11 as nx


class HandoffV11(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.key=Ed25519PrivateKey.generate()
        self.priv=self.root/'sign.pem'
        self.pub=self.root/'verify.pem'
        self.priv.write_bytes(self.key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        self.pub.write_bytes(self.key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
        self.pin=nx.spki_hash(self.key.public_key())
        self.payload=self.root/'public-synthetic.zip'
        with zipfile.ZipFile(self.payload,'w') as z:
            z.writestr('README.md',b'non-sensitive example')
            z.writestr('.hidden',b'protected inside raw ZIP bytes')
        self.manifest=self.root/'manifest.json'
        self.state=self.root/'replay.json'
        self.obj='NEXUS_TEST_ONLINE_HANDOFF_01'
        self.lane='nexus-anchor-test'

    def runcli(self,*args,expected=0):
        p=subprocess.run([sys.executable,str(TOOL),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode,expected,(p.stdout,p.stderr,args))
        return p

    def make(self,seq=1,prev=None,payload=None,klass='PUBLIC_SAFE',url='https://example.org/public-safe.zip',key=None,output=None):
        args=['make','--payload',payload or self.payload,'--object',self.obj,'--lane',self.lane,'--classification',klass,'--sign-key',key or self.priv,'--output',output or self.manifest,'--sequence',str(seq)]
        if url is not None: args+=['--url',url]
        if prev:args+=['--prev-hash',prev]
        return self.runcli(*args)

    def verify(self,payload=True,state=False,record=False,witness=False,pin=None,pub=None,expected=0):
        args=['verify','--manifest',self.manifest,'--pubkey',pub or self.pub,'--pinned-key-sha256',pin or self.pin]
        if payload:args+=['--payload',self.payload]
        if state:args+=['--state-file',self.state]
        if record:args.append('--record')
        if witness:args.append('--witness-only')
        return self.runcli(*args,expected=expected)

    def test_01_hash_is_exact_zip_bytes_including_hidden(self):
        self.make(); m=nx.read_json(self.manifest)
        self.assertEqual(m['payload']['sha256'],nx.file_info(self.payload)[1])
        self.assertEqual(m['payload']['bytes'],self.payload.stat().st_size)
        self.verify(payload=True,state=True,record=True)
        with zipfile.ZipFile(self.payload,'a') as z:z.writestr('.hidden-new',b'changed')
        self.verify(payload=True,state=True,expected=2)

    def test_02_no_payload_no_ack(self):
        self.make(); self.verify(payload=False,expected=2)

    def test_03_witness_explicit_cannot_record(self):
        self.make(); x=self.verify(payload=False,witness=True)
        self.assertIn('WITNESS_ONLY_NO_PAYLOAD',x.stdout)
        self.verify(payload=False,witness=True,record=True,expected=2)

    def test_04_signature_tamper_denied(self):
        self.make();m=nx.read_json(self.manifest);m['lane']='swapped';self.manifest.write_text(json.dumps(m))
        self.verify(expected=2)

    def test_05_unpinned_key_denied(self):
        self.make();self.verify(pin='0'*64,expected=2)

    def test_06_rogue_signer_denied(self):
        other=Ed25519PrivateKey.generate()
        bad=self.root/'rogue.pem';bad.write_bytes(other.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        self.make(key=bad);self.verify(expected=2)

    def test_07_claim_ceiling_is_fixed(self):
        self.make();m=nx.read_json(self.manifest);m['claim_ceiling']='C3';self.manifest.write_text(json.dumps(m))
        self.verify(expected=2)

    def test_08_seq_1_genesis_valid_record(self):
        self.make();x=self.verify(state=True,record=True)
        self.assertIn('CONTENT_SIGNATURE_AND_CHAIN_MATCH',x.stdout)
        st=nx.read_json(self.state);self.assertEqual(st['sequence'],1)

    def test_09_same_receipt_idempotent_no_new_action(self):
        self.make();self.verify(state=True,record=True)
        x=self.verify(state=True,record=True)
        self.assertIn('ALREADY_VERIFIED_IDEMPOTENT',x.stdout)

    def test_10_same_sequence_changed_manifest_denied(self):
        self.make();self.verify(state=True,record=True)
        self.make(seq=1)
        # second make within same second may be same signature, force later timestamp and resign
        m=nx.read_json(self.manifest)
        m['issued_at']='2026-10-14T12:00:00Z'
        m=nx.sign({k:v for k,v in m.items() if k!='signature'},self.key)
        self.manifest.write_text(json.dumps(m))
        self.verify(state=True,expected=2)

    def test_11_replay_older_sequence_denied(self):
        self.make();self.verify(state=True,record=True)
        h=nx.read_json(self.state)['manifest_sha256']
        self.make(seq=2,prev=h);self.verify(state=True,record=True)
        self.make(seq=1);self.verify(state=True,expected=2)

    def test_12_next_valid_chain(self):
        self.make();self.verify(state=True,record=True)
        h=nx.read_json(self.state)['manifest_sha256']
        self.make(seq=2,prev=h)
        x=self.verify(state=True,record=True)
        self.assertIn('CONTENT_SIGNATURE_AND_CHAIN_MATCH',x.stdout)
        self.assertEqual(nx.read_json(self.state)['sequence'],2)

    def test_13_wrong_previous_hash(self):
        self.make();self.verify(state=True,record=True)
        self.make(seq=2,prev='0'*64);self.verify(state=True,expected=2)

    def test_14_duplicate_json_fields_rejected(self):
        self.make();text=self.manifest.read_text();self.manifest.write_text(text.replace('"schema":', '"schema":"malicious", "schema":'))
        self.verify(expected=2)

    def test_15_unknown_field_rejected(self):
        self.make();m=nx.read_json(self.manifest);m['malicious']=1;self.manifest.write_text(json.dumps(m))
        self.verify(expected=2)

    def test_16_symlink_payload_rejected(self):
        link=self.root/'link.zip';link.symlink_to(self.payload)
        self.runcli('make','--payload',link,'--object',self.obj,'--lane',self.lane,'--classification','PUBLIC_SAFE','--url','https://example.org/a.zip','--sign-key',self.priv,'--output',self.manifest,expected=2)

    def test_17_directory_payload_rejected(self):
        self.runcli('make','--payload',self.root,'--object',self.obj,'--lane',self.lane,'--classification','PUBLIC_SAFE','--url','https://example.org/a.zip','--sign-key',self.priv,'--output',self.manifest,expected=2)

    def test_18_unsigned_origin_not_trusted_even_with_hash(self):
        self.make();m=nx.read_json(self.manifest);m['signature']['base64']=base64.b64encode(b'X'*64).decode();self.manifest.write_text(json.dumps(m))
        self.verify(expected=2)

    def test_19_bad_witness_url(self):
        self.runcli('make','--payload',self.payload,'--object',self.obj,'--lane',self.lane,'--classification','PRIVATE_WITNESS_ONLY','--url','https://example.org/a','--sign-key',self.priv,'--output',self.manifest,expected=2)

    def test_20_invalid_http_url(self):
        self.runcli('make','--payload',self.payload,'--object',self.obj,'--lane',self.lane,'--classification','PUBLIC_SAFE','--url','http://example.org/a','--sign-key',self.priv,'--output',self.manifest,expected=2)

    def test_21_private_encrypted_requires_age(self):
        self.runcli('make','--payload',self.payload,'--object',self.obj,'--lane',self.lane,'--classification','PRIVATE_ENCRYPTED','--url','https://example.org/a','--sign-key',self.priv,'--output',self.manifest,expected=2)

    def test_22_private_encrypted_refuses_false_security(self):
        ciphertext=self.root/'file.age';ciphertext.write_bytes(b'FAKE-ENCRYPTION-NOT-REAL')
        self.runcli('make','--payload',ciphertext,'--object',self.obj,'--lane',self.lane,
                    '--classification','PRIVATE_ENCRYPTED','--url','https://example.org/file.age',
                    '--sign-key',self.priv,'--output',self.manifest,expected=2)
        self.assertFalse(self.manifest.exists())

    def test_23_invalid_sequence(self):
        self.runcli('make','--payload',self.payload,'--object',self.obj,'--lane',self.lane,'--classification','PUBLIC_SAFE','--url','https://example.org/a','--sign-key',self.priv,'--output',self.manifest,'--sequence','0',expected=2)

    def test_24_state_file_no_ack_if_no_payload(self):
        self.make();self.verify(payload=False,state=True,record=True,expected=2)
        self.assertFalse(self.state.exists())

    def test_25_untrusted_object_wont_match_state(self):
        self.make();self.verify(state=True,record=True)
        m=nx.read_json(self.manifest);m['object']='NEXUS_OTHER_OBJECT_001';m['sequence']=2;m['previous_manifest_sha256']=nx.read_json(self.state)['manifest_sha256']
        m=nx.sign({k:v for k,v in m.items() if k!='signature'},self.key)
        self.manifest.write_text(json.dumps(m))
        self.verify(state=True,record=True,expected=2)

if __name__=='__main__':unittest.main()
