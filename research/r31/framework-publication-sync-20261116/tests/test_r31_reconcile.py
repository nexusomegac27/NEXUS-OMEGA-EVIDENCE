"""R31 independent offline positive, mutation and fail-closed tests.
All keys and observations here are synthetic fixtures; they authorize NOTHING.
"""
from __future__ import annotations
import copy
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / "src" / "r31_reconcile.py"
spec = importlib.util.spec_from_file_location("r31_reconcile", MODULE)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
ROUTE = "/bodytwin/updates/events.json"
DIGEST = "a" * 64

class R31ScienceTests(unittest.TestCase):
    def setUp(self):
        self.keys = {
            "operator-test-fixture": {"role": "operator_release", "key": b"nonproduction-r31-test-only-operator"},
            "observer-test-fixture": {"role": "independent_observer", "key": b"nonproduction-r31-test-only-observer"},
            "unauthorized-test-fixture": {"role": "untrusted", "key": b"nonproduction-untrusted"}
        }
        self.registry = {ROUTE: {"visibility": "public_metadata_only", "topics": ["bodytwin"]},
                         "/forum/updates/": {"visibility": "public_metadata_only", "topics": ["forum"]}}
        self.event = {
            "specversion": "1.0", "id": "r31-test-event-0001",
            "source": "urn:nexus:publication:operator",
            "type": "nexus.publication.candidate.v1",
            "time": "2026-11-16T06:00:00Z",
            "data": {
                "release_id": "R31-PUBLIC-C1-SYNTHETIC-1",
                "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
                "source_class": "C1_VERIFIED_PUBLIC_SAFE",
                "public_safe": True,
                "reversible": True,
                "visibility": "public_metadata_only",
                "source_sha256": "b" * 64,
                "review_sha256": "c" * 64,
                "release_seq": 8, "topics": ["bodytwin"], "targets": {ROUTE: DIGEST}
            }
        }
        self.grant = self.grant_for()
        self.witness = self.witness_for()

    def grant_for(self):
        return R.sign_test_receipt({
            "signer": "operator-test-fixture", "event_sha256": R.sha(self.event),
            "release_id": self.event["data"]["release_id"], "release_seq": self.event["data"]["release_seq"],
            "allowed_routes": [ROUTE]
        }, self.keys["operator-test-fixture"]["key"])

    def witness_for(self):
        return R.sign_test_receipt({
            "observer": "observer-test-fixture", "event_sha256": R.sha(self.event),
            "release_id": self.event["data"]["release_id"], "route": ROUTE,
            "observed_sha256": DIGEST, "http_status": 200,
            "content_type": "application/json", "observed_at": "2026-11-16T06:10:00Z"
        }, self.keys["observer-test-fixture"]["key"])

    def status(self, event=None, grant=None, witnesses=None, registry=None, prior=None, static_flags=None):
        result = R.reconcile(self.event if event is None else event,
            self.grant if grant is None else grant, [self.witness] if witnesses is None else witnesses,
            self.registry if registry is None else registry, {} if prior is None else prior,
            self.keys, static_flags)
        return result["surfaces"][ROUTE]["state"]

    def invalid_event(self, key, value, reason):
        event = copy.deepcopy(self.event);event["data"][key] = value
        with self.assertRaisesRegex(R.Refusal, reason):
            self.status(event=event)

    def test_01_verified_witness_reconciles(self):
        self.assertEqual(self.status(), "RECONCILED")

    def test_02_stale_static_published_flag_detected(self):
        self.assertEqual(self.status(static_flags={ROUTE: False}), "RECONCILED_WITH_STATIC_METADATA_DRIFT")

    def test_35_aggregate_drift_never_full_pass(self):
        # AXIOM self-falsification: previously all(RECONCILED*) counted drift as ALL_RECONCILED.
        result = R.reconcile(self.event, self.grant, [self.witness],
                             self.registry, {}, self.keys, {ROUTE: False})
        self.assertEqual(result["surfaces"][ROUTE]["state"], "RECONCILED_WITH_STATIC_METADATA_DRIFT")
        self.assertEqual(result["state"], "WWW_OBSERVED_METADATA_DRIFT_OPEN")
        self.assertEqual(result["metadata_drift_routes"], [ROUTE])
        self.assertNotEqual(result["state"], "ALL_RECONCILED")

    def test_36_hold_plus_drift_cannot_promote_to_overall_success(self):
        result = R.reconcile(self.event, self.grant, [],
                             self.registry, {}, self.keys, {ROUTE: False})
        self.assertEqual(result["state"], "PARTIAL_OR_HOLD")
        self.assertEqual(result["metadata_drift_routes"], [])

    def test_37_clean_observed_route_retains_scoped_success(self):
        result = R.reconcile(self.event, self.grant, [self.witness],
                             self.registry, {}, self.keys, {ROUTE: True})
        self.assertEqual(result["state"], "ALL_RECONCILED")
        self.assertEqual(result["metadata_drift_routes"], [])
        self.assertFalse(result["www_write_performed"])

    def test_03_no_witness_pending_not_published(self):
        self.assertEqual(self.status(witnesses=[]), "PENDING_INDEPENDENT_WWW_WITNESS")

    def test_04_absent_grant_is_hold(self):
        self.assertEqual(self.status(grant={}), "HOLD_NO_VERIFIED_OPERATOR_GRANT")

    def test_05_forged_grant_no_signature_is_hold(self):
        grant = dict(self.grant); grant.pop("signature")
        self.assertEqual(self.status(grant=grant), "HOLD_NO_VERIFIED_OPERATOR_GRANT")

    def test_06_modified_signed_grant_is_hold(self):
        grant = dict(self.grant); grant["release_seq"] = 999
        self.assertEqual(self.status(grant=grant), "HOLD_NO_VERIFIED_OPERATOR_GRANT")

    def test_07_wrong_approver_role_is_hold(self):
        grant = R.sign_test_receipt(dict(self.grant, signer="unauthorized-test-fixture", signature=""),
                                    self.keys["unauthorized-test-fixture"]["key"])
        self.assertEqual(self.status(grant=grant), "HOLD_NO_VERIFIED_OPERATOR_GRANT")

    def test_08_unrelated_surface_is_denied(self):
        reg = {ROUTE: {"visibility": "public_metadata_only", "topics": ["forum"]}}
        self.assertEqual(self.status(registry=reg), "HOLD_UNRELATED_SURFACE")

    def test_09_unknown_route_is_denied(self):
        self.assertEqual(self.status(registry={}), "HOLD_UNKNOWN_OR_PRIVATE_SURFACE")

    def test_10_private_route_is_denied(self):
        self.assertEqual(self.status(registry={ROUTE: {"visibility": "private", "topics": ["bodytwin"]}}),
                         "HOLD_UNKNOWN_OR_PRIVATE_SURFACE")

    def test_11_unauthorized_grant_destination_denied(self):
        grant = R.sign_test_receipt(dict(self.grant, allowed_routes=["/forum/updates/"]),
                                    self.keys["operator-test-fixture"]["key"])
        self.assertEqual(self.status(grant=grant), "HOLD_GRANT_ROUTE_OR_SEQUENCE")

    def test_12_wrong_event_binding_denied(self):
        grant = R.sign_test_receipt(dict(self.grant, event_sha256="d"*64),
                                    self.keys["operator-test-fixture"]["key"])
        self.assertEqual(self.status(grant=grant), "HOLD_GRANT_EVENT_BINDING")

    def test_13_observer_signature_missing_denied(self):
        witness = dict(self.witness); witness["signature"] = "0"*64
        self.assertEqual(self.status(witnesses=[witness]), "HOLD_WWW_WITNESS_UNVERIFIED_OR_MISMATCH")

    def test_14_wrong_http_denied(self):
        witness = R.sign_test_receipt(dict(self.witness, http_status=404),
                                      self.keys["observer-test-fixture"]["key"])
        self.assertEqual(self.status(witnesses=[witness]), "HOLD_WWW_WITNESS_UNVERIFIED_OR_MISMATCH")

    def test_15_wrong_content_type_denied(self):
        witness = R.sign_test_receipt(dict(self.witness, content_type="text/plain"),
                                      self.keys["observer-test-fixture"]["key"])
        self.assertEqual(self.status(witnesses=[witness]), "HOLD_WWW_WITNESS_UNVERIFIED_OR_MISMATCH")

    def test_16_signed_wrong_digest_causes_conflict_hold(self):
        witness = R.sign_test_receipt(dict(self.witness, observed_sha256="d"*64),
                                      self.keys["observer-test-fixture"]["key"])
        self.assertEqual(self.status(witnesses=[witness]), "HOLD_CONFLICTING_WWW_WITNESS")

    def test_17_two_contradictory_signed_witnesses_hold(self):
        wrong = R.sign_test_receipt(dict(self.witness, observed_sha256="d"*64),
                                    self.keys["observer-test-fixture"]["key"])
        self.assertEqual(self.status(witnesses=[self.witness, wrong]), "HOLD_CONFLICTING_WWW_WITNESS")

    def test_18_release_sequence_rollback_denied(self):
        self.assertEqual(self.status(prior={ROUTE: {"release_seq": 9, "sha256": "e"*64}}), "HOLD_ROLLBACK")

    def test_19_same_sequence_different_hash_denied(self):
        self.assertEqual(self.status(prior={ROUTE: {"release_seq": 8, "sha256": "d"*64}}), "HOLD_SEQUENCE_EQUIVOCATION")

    def test_20_same_sequence_same_hash_idempotent(self):
        self.assertEqual(self.status(prior={ROUTE: {"release_seq": 8, "sha256": DIGEST}}), "RECONCILED")

    def test_21_source_not_reviewed_fail_closed(self):
        self.invalid_event("source_class", "CI_GREEN_ONLY", "SOURCE_NOT_VERIFIED")

    def test_22_private_evidence_blocked(self):
        self.invalid_event("visibility", "private_sensor_raw", "PRIVATE_OR_UNSCOPED_VISIBILITY")

    def test_23_claim_promotion_blocked(self):
        self.invalid_event("claim_ceiling", "C2_VALIDATED", "CLAIM_CEILING")

    def test_24_no_reversible_rollback_blocked(self):
        self.invalid_event("reversible", False, "PUBLIC_OR_ROLLBACK")

    def test_25_no_actual_review_digest_blocked(self):
        self.invalid_event("review_sha256", None, "SOURCE_OR_REVIEW_DIGEST")

    def test_26_mutated_target_digest_is_not_accepted_as_original_release(self):
        event=copy.deepcopy(self.event)
        event["data"]["targets"][ROUTE] = "d"*64
        self.assertEqual(self.status(event=event), "HOLD_GRANT_EVENT_BINDING")

    def test_27_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(R.Refusal, "DUPLICATE_JSON_KEY"):
            R.strict_load(b'{"id":"a","id":"b"}')

    def test_28_nonfinite_json_rejected(self):
        with self.assertRaisesRegex(R.Refusal, "NONFINITE_JSON"):
            R.strict_load(b'{"value":NaN}')

    def test_29_padded_oversize_input_rejected(self):
        with self.assertRaisesRegex(R.Refusal, "JSON_INPUT_TOO_LARGE"):
            R.strict_load(b" " * 262145)

    def test_30_foreign_event_type_rejected(self):
        event=copy.deepcopy(self.event);event["type"]="nexus.sensor.capture.v1"
        with self.assertRaisesRegex(R.Refusal, "UNSUPPORTED_EVENT"):
            self.status(event=event)

    def test_31_bad_timestamp_rejected(self):
        event=copy.deepcopy(self.event);event["time"]="2026-11-16"
        with self.assertRaisesRegex(R.Refusal, "INVALID_EVENT_TIME"):
            self.status(event=event)

    def test_32_target_with_sensor_raw_marker_denied(self):
        self.invalid_event("release_id", "patient_record_secret", "PRIVATE_MARKER_IN_PUBLIC_EVENT")

    def test_33_mismatch_witness_synthetically_authorized_but_not_true_www(self):
        # Reconciler trusts configured observer, not an unknown public source.
        witness = dict(self.witness);witness["observer"]="unknown-self-hosted-feed"
        self.assertEqual(self.status(witnesses=[witness]), "HOLD_WWW_WITNESS_UNVERIFIED_OR_MISMATCH")

    def test_34_no_side_effects_and_no_claim_promotion(self):
        result = R.reconcile(self.event, self.grant, [self.witness], self.registry, {}, self.keys)
        self.assertFalse(result["www_write_performed"])
        self.assertFalse(result["claim_promotion"])
        self.assertEqual(result["state"], "ALL_RECONCILED")

if __name__ == "__main__":
    unittest.main(verbosity=2)
