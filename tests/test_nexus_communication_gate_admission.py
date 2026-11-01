"""Negative-conformance checks for the C1 communication pre-entry *policy*.

These tests intentionally do not authorize an external receiver, owner cutover,
private material or Pixel 9a twin activation. The policy validator is an
additional fail-closed CI lint, NOT a runtime security verifier.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/validate_nexus_communication_gate_admission.py"
STATE=ROOT/"research/communication/github-only-exchange-enforcement-20261029/NEXUS_COMMUNICATION_GATE_ADMISSION_STATE_V1_20261101.json"

spec=importlib.util.spec_from_file_location("nexus_communication_gate_admission", SCRIPT)
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class CommunicationGatePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state=json.loads(STATE.read_text(encoding="utf-8"))

    def assertRejects(self, lane, key, wrong):
        data=copy.deepcopy(self.state)
        data[lane][key]=wrong
        with self.assertRaises(m.GatePolicyError):
            m.validate(data)

    def test_known_historical_public_read_only_and_all_holds(self):
        out=m.validate(self.state)
        self.assertEqual(out["policy_preentry"],"PASS_STAGED_CONTRACT")
        self.assertEqual(out["document_transport"],"HOLD_NOT_LIVE_ATTESTED")
        self.assertEqual(out["external_receiver"],"NOT_ESTABLISHED")
        self.assertEqual(out["pixel9a_second_twin"],"NOT_ADMITTED")
        self.assertEqual(out["cutover_authorization"],"NOT_GRANTED_BY_POLICY_VALIDATION")

    def test_tampered_claim_ceiling_rejected(self):
        dat=copy.deepcopy(self.state);dat["claim_ceiling"]="C2_AUTONOMOUS_PROVEN"
        with self.assertRaises(m.GatePolicyError):m.validate(dat)

    def test_public_post_rejected(self):
        self.assertRejects("public_www","write_api","ON")

    def test_public_read_claim_not_turned_into_runtime_live_check(self):
        self.assertRejects("public_www","state","LIVE_CONTINUOUSLY_VERIFIED")

    def test_router_not_activated_by_ci_flags(self):
        self.assertRejects("github_document_router","state","ACTIVE")

    def test_unverified_receiver_boolean_does_not_count(self):
        self.assertRejects("real_receiver","state",True)

    def test_fake_receiver_identity_promotion_rejected(self):
        self.assertRejects("real_receiver","github_distinct_principal","VERIFIED")

    def test_unverified_return_source_promotion_rejected(self):
        self.assertRejects("real_receiver","return_source_independently_verified","VERIFIED")

    def test_unverified_external_delivery_promotion_rejected(self):
        self.assertRejects("owner_cutover","platform_delivery","ESTABLISHED")

    def test_self_claimed_owner_authority_rejected(self):
        self.assertRejects("owner_cutover","authorization","AUTHORIZED")

    def test_cutover_active_from_json_rejected(self):
        self.assertRejects("owner_cutover","state","ACTIVE")

    def test_private_lane_without_verified_permission_rejected(self):
        self.assertRejects("private_source","permission","AUTHORIZED")

    def test_private_material_public_write_rejected(self):
        self.assertRejects("private_source","raw_to_public_github","ALLOWED")

    def test_pixel9a_activation_without_oppo_evidence_rejected(self):
        self.assertRejects("pixel9a_second_twin","state","ACTIVE")

    def test_pixel9a_dual_sync_rejected(self):
        self.assertRejects("pixel9a_second_twin","dual_device_sync","ENABLED")

    def test_pixel9a_live_relay_rejected(self):
        self.assertRejects("pixel9a_second_twin","live_sensor_relay","AUTHORIZED")

    def test_pixel9a_raw_cloud_upload_rejected(self):
        self.assertRejects("pixel9a_second_twin","raw_sensor_cloud_upload","ON")

    def test_pixel9a_opt_in_requires_explicit_consent(self):
        self.assertRejects("pixel9a_second_twin","opt_in",False)

    def test_agent_model_name_does_not_attest_identity(self):
        self.assertRejects("symbiosis","agent_identity","ATTESTED_BY_MODEL_LABEL")

    def test_claim_of_consciousness_not_promoted(self):
        self.assertRejects("symbiosis","claim_of_consciousness","CONFIRMED")

    def test_mutating_required_falsifier_inventory_rejected(self):
        dat=copy.deepcopy(self.state);dat["violations_always_fail"]=["PUBLIC_POST_ENABLED"]
        with self.assertRaises(m.GatePolicyError):m.validate(dat)

    def test_shallow_or_wrong_type_rejected(self):
        with self.assertRaises(m.GatePolicyError):m.validate([])
        self.assertRejects("public_www","no_account_required_for_public_read","true")

    def test_missing_release_separation_rejected(self):
        dat=copy.deepcopy(self.state);dat["publication_policy"]="LIVE_NOW"
        with self.assertRaises(m.GatePolicyError):m.validate(dat)

if __name__=="__main__":unittest.main()
