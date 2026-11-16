"""NEXUS R31 BodyTwin science release C1 offline safety/contract tests."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"src"/"render_science_snapshot.py"
FILE=ROOT/"data"/"bodytwin_science_source_census_20261116_R0.json"
spec=importlib.util.spec_from_file_location("bt_science_render",SRC)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

class BodyTwinScienceCandidateTests(unittest.TestCase):
    def setUp(self):
        self.doc=M.load_bytes(FILE.read_bytes())
    def failure(self,doc,why):
        with self.assertRaisesRegex(M.ContractError,why):
            M.render(doc)
    def test_01_census_is_source_level_valid(self):
        self.assertIs(M.validate(self.doc),self.doc)
    def test_02_all_nine_events_deduplicated(self):
        self.assertEqual(len(self.doc["events"]),9)
        self.assertEqual(len({e["id"] for e in self.doc["events"]}),9)
    def test_03_deterministic_candidate_output(self):
        a=M.render(self.doc);b=M.render(copy.deepcopy(self.doc))
        self.assertEqual(a,b)
    def test_04_current_json_is_public_candidate_not_witness(self):
        _,raw=M.render(self.doc)
        j=json.loads(raw)
        self.assertEqual(j["publication_status"],"CANDIDATE_NOT_WWW_WITNESSED")
        self.assertEqual(j["bodytwin_validated"],"NO")
        self.assertEqual(j["event_count"],9)
    def test_05_no_claim_promotion(self):
        _,raw=M.render(self.doc);j=json.loads(raw)
        self.assertEqual(j["claim_ceiling"],"C1_DESCRIPTIVE_ONLY")
        self.assertFalse(j["claim_promotion"])
    def test_06_bodytwin_NO_hard_fence(self):
        d=copy.deepcopy(self.doc);d["bodytwin_validated"]="YES"
        self.failure(d,"UNAUTHORIZED_SCIENCE_PROMOTION")
    def test_07_consent_open_hard_fence(self):
        d=copy.deepcopy(self.doc);d["consent_bind"]="GRANTED"
        self.failure(d,"UNAUTHORIZED_SCIENCE_PROMOTION")
    def test_08_trial_not_executed_hard_fence(self):
        d=copy.deepcopy(self.doc);d["trial_001"]="PASS"
        self.failure(d,"UNAUTHORIZED_SCIENCE_PROMOTION")
    def test_09_clinical_validation_hard_fence(self):
        d=copy.deepcopy(self.doc);d["clinical_validated"]=True
        self.failure(d,"UNAUTHORIZED_SCIENCE_PROMOTION")
    def test_10_whole_body_validation_hard_fence(self):
        d=copy.deepcopy(self.doc);d["whole_body_pose_validated"]=True
        self.failure(d,"UNAUTHORIZED_SCIENCE_PROMOTION")
    def test_11_no_auto_execution_claim(self):
        d=copy.deepcopy(self.doc);d["auto_execution_authorized"]=True
        self.failure(d,"PUBLICATION_PERMISSION_CLAIM")
    def test_12_release_not_implicitly_published(self):
        d=copy.deepcopy(self.doc);d["publication_status"]="LIVE_WWW_PASS"
        self.failure(d,"CLAIM_OR_WWW_PROMOTION")
    def test_13_R21_raw_source_unrehash_cannot_be_hidden(self):
        d=copy.deepcopy(self.doc)
        r=next(e for e in d["events"] if e["class"]=="PHYSICAL_CAPTURE_PRODUCER_REPORTED_NOT_SECOND_PARTY")
        r["summary"]="Authentischer physischer Ganzkörperzwilling wurde hergestellt."
        self.failure(d,"R21_PHYSICAL_ORIGINAL_GAP")
    def test_14_private_marker_blocked(self):
        d=copy.deepcopy(self.doc)
        d["events"][0]["summary"]+=" api_token=EXAMPLE"
        self.failure(d,"PUBLIC_SENSITIVE_MARKER")
    def test_15_non_allowlisted_source_domain_denied(self):
        d=copy.deepcopy(self.doc)
        d["events"][0]["source"]="https://attacker.example/fake"
        self.failure(d,"SOURCE_ORIGIN")
    def test_16_git_source_must_be_pinned_or_pr(self):
        d=copy.deepcopy(self.doc)
        d["events"][0]["source"]="https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/main/README.md"
        self.failure(d,"SOURCE_COMMIT_NOT_PINNED")
    def test_17_duplicate_event_denied(self):
        d=copy.deepcopy(self.doc)
        d["events"][1]["id"]=d["events"][0]["id"]
        self.failure(d,"EVENT_DUPLICATE")
    def test_18_disordered_chronology_denied(self):
        d=copy.deepcopy(self.doc)
        d["events"][0]["date"]="2026-11-20"
        self.failure(d,"EVENT_ORDER")
    def test_19_invalid_date_denied(self):
        d=copy.deepcopy(self.doc)
        d["events"][0]["date"]="2026-02-30"
        self.failure(d,"DATE_INVALID")
    def test_20_duplicate_json_object_keys_denied(self):
        with self.assertRaisesRegex(M.ContractError,"DUPLICATE_FIELD"):
            M.load_bytes(b'{"schema":"a","schema":"b"}')
    def test_21_nonfinite_json_denied(self):
        with self.assertRaisesRegex(M.ContractError,"NONFINITE_JSON"):
            M.load_bytes(b'{"a":NaN}')
    def test_22_input_size_bounded(self):
        with self.assertRaisesRegex(M.ContractError,"BAD_INPUT_SIZE"):
            M.load_bytes(b" " * 64001)
    def test_23_all_current_science_statuses_are_descriptive(self):
        self.assertEqual(self.doc["claim_ceiling"],"C1_DESCRIPTIVE_ONLY")
        self.assertIn("A72_ORIGINAL_SOURCE_GAP",self.doc["open_gates"])
        self.assertIn("R31_PRODUCTION_OUTBOX_NOT_ESTABLISHED",self.doc["open_gates"])
        self.assertFalse(self.doc["auto_execution_authorized"])
    def test_24_accessible_no_JS_no_external_assets(self):
        doc,_=M.render(self.doc);x=doc.decode("utf8")
        self.assertIn('lang="de"',x)
        self.assertIn('name="viewport"',x)
        self.assertIn('aria-label="Chronologie"',x)
        self.assertNotIn("<script",x.lower())
        self.assertNotIn("<iframe",x.lower())
        self.assertIn("/bodytwin/",x)
    def test_25_documented_3_roles_not_self_certification(self):
        h,b=M.render(self.doc);j=json.loads(b)
        self.assertIn("not a signed publication",j["source_ledger_note"])
        self.assertIn("publication_status",j)
        self.assertIn("kein",h.decode("utf8").lower())
    def test_26_header_links_no_sensitive_data(self):
        page,_=M.render(self.doc)
        self.assertNotIn(b"ghp_",page)
        self.assertNotIn(b"sk-proj-",page)
    def test_27_release_payload_hash_stable(self):
        h,j=M.render(self.doc)
        self.assertEqual(M.digest(h),M.digest(M.render(self.doc)[0]))
        self.assertEqual(M.digest(j),M.digest(M.render(self.doc)[1]))
    def test_28_claim_class_of_R31_separate_infrastructure(self):
        row=next(e for e in self.doc["events"] if e["id"]=="BT-SCI-20261116-R31")
        self.assertFalse(row["bodytwin_science"])
        self.assertEqual(row["class"],"SCIENTIFIC_PUBLICATION_INFRASTRUCTURE_C1")

if __name__=="__main__":
    unittest.main(verbosity=2)
