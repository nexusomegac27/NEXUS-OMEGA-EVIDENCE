"""Pure stdlib adversarial regression for offline bytes+Git blob verification."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
SRC=Path(__file__).resolve().parents[1]/"scripts"/"verify_expert_hash_handshake_v1.py"
spec=importlib.util.spec_from_file_location("check",SRC)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
S="a"*64
class TestExpertHashHandshake(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        self.prefix="research/r26/owner-approved-return-slot"
        self.path=self.prefix+"/evidence.md"
        d=self.root/self.path;d.parent.mkdir(parents=True)
        d.write_bytes(b"original evidence\\n")
        b=d.read_bytes()
        self.m={"schema_version":"1.0.0","object":"EXPERT_TEST_OBJECT","recipient":"NEXUS_OPERATOR_AXIOM",
            "order_object":"EXPERT_ORDER_OBJECT","order_sha256":S,"order_bytes":13150,
            "repo":"nexusomegac27/NEXUS-OMEGA-EVIDENCE","transport_class":"OPERATOR_TO_AXIOM_BRIDGE",
            "sender_role":"GROK","github_actor":"NOT_ESTABLISHED","predecessor":"PR92_MAIN",
            "claim_ceiling":"C1_DESCRIPTIVE_ONLY","runtime":"NOT_AUTHORIZED",
            "receiver_ack":"PENDING_AXIOM_INDEPENDENT_REHASH",
            "children":[{"path":self.path,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
                         "git_blob_sha1":hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\x00"+b).hexdigest()}]}
    def check(self):
        return v.verify(json.dumps(self.m).encode(),self.root,self.prefix,S)
    def assertRejected(self):
        with self.assertRaises(ValueError): self.check()
    def test_positive_bytes_only(self):
        x=self.check();self.assertEqual(x["result"],"BYTE_MATCH_ONLY")
        self.assertEqual(x["actor_auth"],"NOT_ESTABLISHED_OFFLINE")
    def test_modified_file_fails(self):
        (self.root/self.path).write_bytes(b"tampered")
        self.assertRejected()
    def test_parent_escape_fails(self):
        self.m["children"][0]["path"]=self.prefix+"/../secret.md"
        self.assertRejected()
    def test_wrong_order_fails(self):
        self.m["order_sha256"]="b"*64
        self.assertRejected()
    def test_forged_receiver_ack_fails(self):
        self.m["receiver_ack"]="AXIOM_PASS"
        self.assertRejected()
    def test_forged_runtime_fails(self):
        self.m["runtime"]="EXECUTED"
        self.assertRejected()
    def test_duplicate_child_fails(self):
        self.m["children"].append(dict(self.m["children"][0]))
        self.assertRejected()
    def test_git_blob_mismatch_fails(self):
        self.m["children"][0]["git_blob_sha1"]="b"*40
        self.assertRejected()
    def test_claim_promotion_fails(self):
        self.m["claim_ceiling"]="C2"
        self.assertRejected()
    def test_duplicate_json_key_fails(self):
        raw=json.dumps(self.m)
        raw=raw.replace('"object": "EXPERT_TEST_OBJECT"', '"object": "A", "object": "EXPERT_TEST_OBJECT"')
        with self.assertRaises(ValueError):v.verify(raw.encode(),self.root,self.prefix,S)
    def test_nested_symlink_fails(self):
        new=self.root/"research"/"r26"/"alias"
        new.symlink_to(self.root/self.prefix,target_is_directory=True)
        self.m["children"][0]["path"]="research/r26/alias/evidence.md"
        self.assertRejected()
    def test_hard_uppercase_sha_fails(self):
        self.m["children"][0]["sha256"]="F"*64
        self.assertRejected()
if __name__=="__main__":unittest.main()
