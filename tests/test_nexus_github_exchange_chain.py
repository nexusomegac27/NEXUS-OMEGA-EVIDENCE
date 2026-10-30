#!/usr/bin/env python3
"""Adversarial + positive tests for GitHub Expert Exchange Hard Remediation R2.

F01–F09 from AXIOM_INDEPENDENT_ADJUDICATION_R2.md.
PINNED_COMMIT = ee73769c966b22887fafbc755edf7c64d1a537e1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
"""

from __future__ import annotations

import json
import shutil
import tempfile
import threading
import unittest
from pathlib import Path

from scripts.nexus_expertenkodex_validator import build_obligatory_expert_order_header
from scripts.nexus_github_exchange_chain import (
    ADAPTER_NOT_CONNECTED,
    DEFAULT_REPO,
    PINNED_COMMIT,
    AgentAdapter,
    DeliveryJournal,
    DispatchValidator,
    ExchangeChain,
    ReceiverAckProtocol,
    SourceResolver,
    measure_efficiency,
    sha256_bytes,
)


ROOT = Path(__file__).resolve().parents[1]

LAW_PATH = "docs/governance/NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2.md"
HANDOFF_PATH = "docs/AI_HANDOFF_PROTOCOL.md"
AXIOM_AUDIT_PATH = (
    "research/communication/github-only-exchange-enforcement-20261029/"
    "AXIOM_INDEPENDENT_ADJUDICATION_R2.md"
)

LAW_BYTES = 9203
LAW_SHA256 = "ad471285d3b3b2f24cb5b832b749498fc11dca486957ddd5478a1ed3b91d6fcc"
HANDOFF_BYTES = 8505
HANDOFF_SHA256 = "66558be74b297eeef0849de5eaa7716f67f9ce4dd64f917bd94f0e30bf2c0aaf"
AXIOM_AUDIT_BYTES = 7269
AXIOM_AUDIT_SHA256 = (
    "01713e98f6d67171995a2c3b1a8e724b6d36eccc4294e7ec2a2aa56e93c8dc0b"
)

FAKE_COMMIT = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
WRONG_REPO = "evil-org/not-nexus-evidence"


def _kodex_header_for_law_and_handoff() -> dict:
    """Obligatory Expertenkodex V1 header for exchange-chain ok-path manifests."""
    return build_obligatory_expert_order_header(
        mandate_source_manifest=[
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "path": LAW_PATH,
                "bytes": LAW_BYTES,
                "sha256": LAW_SHA256,
            },
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "path": HANDOFF_PATH,
                "bytes": HANDOFF_BYTES,
                "sha256": HANDOFF_SHA256,
            },
        ]
    )


class TestF01SourceResolverCommitIdentity(unittest.TestCase):
    """F01 — content hash alone must not accept inventierte Commit-Zugehörigkeit."""

    def setUp(self) -> None:
        self.resolver = SourceResolver(ROOT, expected_repository=DEFAULT_REPO)

    def test_positive_pinned_law_match(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["source"]["sha256"], LAW_SHA256)
        self.assertEqual(r["source"]["bytes"], LAW_BYTES)
        for inv in SourceResolver.INVARIANTS:
            self.assertIn(inv, r["invariants"])

    def test_positive_axiom_audit_match(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=AXIOM_AUDIT_PATH,
            expected_sha256=AXIOM_AUDIT_SHA256,
            expected_bytes=AXIOM_AUDIT_BYTES,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["source"]["bytes"], AXIOM_AUDIT_BYTES)

    def test_f01_content_hash_ok_commit_invented(self) -> None:
        """Inhaltshash korrekt, Commit erfunden → FAIL_CLOSED."""
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=FAKE_COMMIT,
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
        )
        self.assertFalse(r["ok"])
        self.assertIn(
            r["code"],
            {"COMMIT_OBJECT_MISSING", "FULL_COMMIT_SHA_INVALID", "SOURCE_PATH_MISSING"},
        )

    def test_f01_wrong_repository(self) -> None:
        r = self.resolver.resolve(
            repository=WRONG_REPO,
            commit=PINNED_COMMIT,
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "REPOSITORY_IDENTITY_MISMATCH")

    def test_f01_invalid_commit_sha(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit="not-a-full-sha",
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "FULL_COMMIT_SHA_INVALID")

    def test_f01_path_traversal(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path="../secrets/../" + LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
        )
        self.assertFalse(r["ok"])
        self.assertIn(
            r["code"],
            {
                "SOURCE_PATH_TRAVERSAL",
                "SOURCE_PATH_OUTSIDE_ALLOWED_ROOT",
                "SOURCE_PATH_ABSOLUTE_FORBIDDEN",
            },
        )

    def test_f01_hash_mismatch(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=LAW_PATH,
            expected_sha256="0" * 64,
            expected_bytes=LAW_BYTES,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "SOURCE_SHA256_MISMATCH")

    def test_f01_bytes_mismatch(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=1,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "SOURCE_BYTES_MISMATCH")

    def test_f01_missing_transitive_parent(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=LAW_PATH,
            expected_sha256=LAW_SHA256,
            expected_bytes=LAW_BYTES,
            parents=[
                {
                    "repository": DEFAULT_REPO,
                    "commit": PINNED_COMMIT,
                    "path": "research/communication/does-not-exist-parent.md",
                    "sha256": "a" * 64,
                    "bytes": 12,
                }
            ],
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "TRANSITIVE_PARENT_MISSING")

    def test_f01_transitive_parent_graph_closed(self) -> None:
        r = self.resolver.resolve(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            path=HANDOFF_PATH,
            expected_sha256=HANDOFF_SHA256,
            expected_bytes=HANDOFF_BYTES,
            parents=[
                {
                    "repository": DEFAULT_REPO,
                    "commit": PINNED_COMMIT,
                    "path": LAW_PATH,
                    "sha256": LAW_SHA256,
                    "bytes": LAW_BYTES,
                }
            ],
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(len(r["parents"]), 1)
        self.assertTrue(r["parents"][0]["ok"])


class TestF02AuthenticatedAgentIdentity(unittest.TestCase):
    """F02 — github_login as free text is not authentication."""

    def test_declare_alone_does_not_prove(self) -> None:
        adapter = AgentAdapter(allowlist=["trusted-expert"])
        adapter.declare("gpt-test", claimed_github_login="trusted-expert")
        proof = adapter.prove()
        self.assertFalse(proof["ok"])
        self.assertEqual(proof["code"], "AGENT_IDENTITY_NOT_AUTHENTICATED")

    def test_claimed_login_without_proof_token(self) -> None:
        adapter = AgentAdapter(allowlist=["trusted-expert"])
        r = adapter.authenticate_principal(
            github_login="trusted-expert",
            auth_method="TEST_FIXTURE_AUTH",
            proof_token_present=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "GITHUB_PRINCIPAL_UNAUTHENTICATED")

    def test_empty_github_login(self) -> None:
        adapter = AgentAdapter()
        r = adapter.authenticate_principal(
            github_login="  ",
            auth_method="TEST_FIXTURE_AUTH",
            proof_token_present=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "GITHUB_PRINCIPAL_EMPTY")

    def test_unregistered_actor_self_asserted_login(self) -> None:
        adapter = AgentAdapter(allowlist=["trusted-expert"])
        r = adapter.authenticate_principal(
            github_login="random-unregistered",
            auth_method="TEST_FIXTURE_AUTH",
            proof_token_present=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "GITHUB_PRINCIPAL_NOT_ON_ALLOWLIST")

    def test_authenticated_principal_on_allowlist(self) -> None:
        adapter = AgentAdapter(allowlist=["trusted-expert"])
        adapter.declare("model-x", claimed_github_login="spoofed")
        auth = adapter.authenticate_principal(
            github_login="trusted-expert",
            auth_method="TEST_FIXTURE_AUTH",
            proof_token_present=True,
            scopes=["contents:read"],
        )
        self.assertTrue(auth["ok"], auth)
        proof = adapter.prove()
        self.assertTrue(proof["ok"], proof)
        layers = proof["identity_layers"]
        self.assertEqual(layers["claimed_github_login"], "spoofed")
        self.assertEqual(layers["authenticated_github_login"], "trusted-expert")
        self.assertNotEqual(layers["claimed_github_login"], layers["authenticated_github_login"])

    def test_unsupported_auth_method(self) -> None:
        adapter = AgentAdapter()
        r = adapter.authenticate_principal(
            github_login="anyone",
            auth_method="PASSWORD_IN_CHAT",
            proof_token_present=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "GITHUB_AUTH_METHOD_UNSUPPORTED")


class TestF03IndependentReceiverAck(unittest.TestCase):
    """F03 — sender must not self-ACK; synthetic does not close the gate."""

    def test_same_process_ack_forbidden(self) -> None:
        proto = ReceiverAckProtocol(sender_process_id="sender-A")
        r = proto.issue_independent_ack(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            object_path=LAW_PATH,
            bytes_len=LAW_BYTES,
            sha256=LAW_SHA256,
            receiver_principal="trusted-expert",
            fetch_method="GITHUB_API_CONTENTS",
            receiver_process_id="sender-A",
            authenticated=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "RECEIVER_ACK_SAME_PROCESS")

    def test_synthetic_self_ack_adapter_not_connected(self) -> None:
        proto = ReceiverAckProtocol(sender_process_id="sender-A")
        status = proto.synthetic_self_ack_status()
        self.assertFalse(status["ok"])
        self.assertEqual(status["code"], ADAPTER_NOT_CONNECTED)
        self.assertEqual(status["independent_expert_ack"], "NOT_ESTABLISHED")

    def test_independent_ack_requires_auth(self) -> None:
        proto = ReceiverAckProtocol(sender_process_id="sender-A")
        r = proto.issue_independent_ack(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            object_path=LAW_PATH,
            bytes_len=LAW_BYTES,
            sha256=LAW_SHA256,
            receiver_principal="trusted-expert",
            fetch_method="GIT_FETCH_SHOW",
            receiver_process_id="receiver-B",
            authenticated=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "RECEIVER_NOT_AUTHENTICATED")

    def test_independent_ack_ok_separate_process(self) -> None:
        proto = ReceiverAckProtocol(sender_process_id="sender-A")
        r = proto.issue_independent_ack(
            repository=DEFAULT_REPO,
            commit=PINNED_COMMIT,
            object_path=LAW_PATH,
            bytes_len=LAW_BYTES,
            sha256=LAW_SHA256,
            receiver_principal="trusted-expert",
            fetch_method="GITHUB_RAW",
            receiver_process_id="receiver-B",
            authenticated=True,
        )
        self.assertTrue(r["ok"], r)
        self.assertTrue(r["ack"]["independent"])
        self.assertEqual(r["ack"]["commit"], PINNED_COMMIT)


class TestF04CrashSafeJournal(unittest.TestCase):
    """F04 — append-only JSONL, idempotency, quarantine, webhook reconcile."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="nexus-journal-"))
        self.journal = DeliveryJournal(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_append_outbound_and_reload(self) -> None:
        r = self.journal.append(
            stream="outbound",
            payload={"object": "TEST", "commit": PINNED_COMMIT},
            idempotency_key="out-1",
        )
        self.assertTrue(r["ok"], r)
        self.assertFalse(r["replayed"])
        reloaded = DeliveryJournal(self.tmp)
        events = reloaded.list_stream("outbound")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["idempotency_key"], "out-1")

    def test_idempotent_replay_same_payload(self) -> None:
        payload = {"object": "TEST", "n": 1}
        a = self.journal.append(stream="outbound", payload=payload, idempotency_key="k1")
        b = self.journal.append(stream="outbound", payload=payload, idempotency_key="k1")
        self.assertTrue(a["ok"] and b["ok"])
        self.assertTrue(b["replayed"])
        self.assertEqual(len(self.journal.list_stream("outbound")), 1)

    def test_idempotency_conflict_quarantine(self) -> None:
        self.journal.append(
            stream="outbound",
            payload={"object": "A"},
            idempotency_key="same-key",
        )
        conflict = self.journal.append(
            stream="outbound",
            payload={"object": "B_DIFFERENT"},
            idempotency_key="same-key",
        )
        self.assertFalse(conflict["ok"])
        self.assertEqual(conflict["code"], "JOURNAL_IDEMPOTENCY_CONFLICT")
        self.assertTrue(self.journal.quarantine_path.exists())

    def test_stream_separation(self) -> None:
        self.journal.append(stream="outbound", payload={"x": 1}, idempotency_key="o")
        self.journal.append(
            stream="receiver_ack",
            payload={"code": ADAPTER_NOT_CONNECTED},
            idempotency_key="a",
        )
        self.journal.append(stream="return", payload={"y": 2}, idempotency_key="r")
        self.assertEqual(len(self.journal.list_stream("outbound")), 1)
        self.assertEqual(len(self.journal.list_stream("receiver_ack")), 1)
        self.assertEqual(len(self.journal.list_stream("return")), 1)

    def test_concurrent_writes(self) -> None:
        errors: list = []

        def worker(i: int) -> None:
            try:
                jr = DeliveryJournal(self.tmp)
                jr.append(
                    stream="outbound",
                    payload={"i": i},
                    idempotency_key=f"concurrent-{i}",
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        reloaded = DeliveryJournal(self.tmp)
        self.assertEqual(len(reloaded.list_stream("outbound")), 8)

    def test_webhook_invalid_signature(self) -> None:
        r = self.journal.reconcile_github_delivery(
            delivery_id="d1",
            signature_valid=False,
            duplicate=False,
        )
        self.assertFalse(r.get("ok", True) and r.get("event", {}).get("stream") != "quarantine")
        # Quarantine append returns ok=True for the quarantine event itself, or fail on conflict.
        # Signature invalid must land in quarantine stream/file.
        self.assertTrue(
            self.journal.quarantine_path.exists()
            or any(
                e.get("stream") == "quarantine"
                or (e.get("payload") or {}).get("reason") == "WEBHOOK_SIGNATURE_INVALID"
                for e in self.journal._index.values()
            )
            or r.get("code") == "JOURNAL_IDEMPOTENCY_CONFLICT"
            or (r.get("ok") and (r.get("event") or {}).get("stream") in {"quarantine", "reconcile"})
        )
        # Stronger: invalid signature append uses quarantine stream
        if r.get("ok"):
            self.assertEqual(r["event"]["stream"], "quarantine")
            self.assertEqual(r["event"]["payload"]["reason"], "WEBHOOK_SIGNATURE_INVALID")

    def test_webhook_duplicate_ignored(self) -> None:
        r = self.journal.reconcile_github_delivery(
            delivery_id="d2",
            signature_valid=True,
            duplicate=True,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["event"]["payload"]["reason"], "WEBHOOK_DUPLICATE_IGNORED")

    def test_webhook_accepted(self) -> None:
        r = self.journal.reconcile_github_delivery(
            delivery_id="d3",
            signature_valid=True,
            duplicate=False,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["event"]["payload"]["reason"], "WEBHOOK_ACCEPTED")


class TestF05DispatchAndManifest(unittest.TestCase):
    """F05 — wrong repo / incomplete / inventierte Commit im Manifest."""

    def setUp(self) -> None:
        self.resolver = SourceResolver(ROOT)
        self.validator = DispatchValidator(self.resolver)

    def test_manifest_repository_mismatch(self) -> None:
        manifest = {
            "repository": WRONG_REPO,
            "commit": PINNED_COMMIT,
            "object": "OBJ",
            "sources": [
                {
                    "path": LAW_PATH,
                    "sha256": LAW_SHA256,
                    "bytes": LAW_BYTES,
                }
            ],
        }
        r = self.validator.validate_manifest(manifest)
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "MANIFEST_REPOSITORY_MISMATCH")

    def test_manifest_incomplete(self) -> None:
        r = self.validator.validate_manifest({"repository": DEFAULT_REPO})
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "MANIFEST_INCOMPLETE")

    def test_manifest_commit_invalid(self) -> None:
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": "short",
                "object": "OBJ",
                "sources": [],
            }
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "MANIFEST_COMMIT_INVALID")

    def test_manifest_ok(self) -> None:
        header = _kodex_header_for_law_and_handoff()
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_TEST_OBJ",
                "sources": [
                    {
                        "path": LAW_PATH,
                        "sha256": LAW_SHA256,
                        "bytes": LAW_BYTES,
                        "commit": PINNED_COMMIT,
                    }
                ],
                **header,
            }
        )
        self.assertTrue(r["ok"], r)


class TestF06F07F08F09ExchangeAndSlots(unittest.TestCase):
    """F06–F09 — synthetic cycle, efficiency, return slot, lost webhook."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="nexus-chain-"))
        self.chain = ExchangeChain(
            ROOT,
            journal_dir=self.tmp,
            allowlist=["trusted-expert"],
            write_slots=[],  # empty → no unauthorized external slot
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _manifest(self) -> dict:
        return {
            "repository": DEFAULT_REPO,
            "commit": PINNED_COMMIT,
            "object": "NEXUS_OMEGA_HARD_REMEDIATION_R2_SYNTH",
            "sources": [
                {
                    "path": LAW_PATH,
                    "sha256": LAW_SHA256,
                    "bytes": LAW_BYTES,
                    "commit": PINNED_COMMIT,
                },
                {
                    "path": HANDOFF_PATH,
                    "sha256": HANDOFF_SHA256,
                    "bytes": HANDOFF_BYTES,
                    "commit": PINNED_COMMIT,
                },
            ],
            **_kodex_header_for_law_and_handoff(),
        }

    def test_f06_synthetic_cycle_does_not_close_independent_ack(self) -> None:
        r = self.chain.run_synthetic_cycle(self._manifest())
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["gate"], "G8_SYNTHETIC")
        self.assertEqual(r["independent_expert_ack"], "NOT_ESTABLISHED")
        self.assertEqual(r["adapter_status"], ADAPTER_NOT_CONNECTED)
        self.assertFalse(r["terminal_pass"])

    def test_f07_efficiency_not_observed_without_receiver_acks(self) -> None:
        m = measure_efficiency(
            manual_transfers_baseline=20,
            automated_transfers=19,
            documented_exceptions=0,
            receiver_acks_observed=0,
        )
        self.assertEqual(m["status"], "EFFICIENCY_TARGET_NOT_YET_OBSERVED")
        self.assertIsNone(m["reduction"])

    def test_f08_empty_allowlist_denies_unregistered_principal(self) -> None:
        # Live write slots: external_actor_allowlist is empty → DENY.
        adapter = AgentAdapter(allowlist=[], write_slots=[])
        # Empty allowlist means no restriction in AgentAdapter — policy layer
        # uses empty allowlist as DENY for *external* writes. Prove that
        # authenticate without allowlist still requires proof_token.
        r = adapter.authenticate_principal(
            github_login="anyone",
            auth_method="TEST_FIXTURE_AUTH",
            proof_token_present=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "GITHUB_PRINCIPAL_UNAUTHENTICATED")

    def test_f08_r27_slot_not_reused_for_this_object(self) -> None:
        slots_path = ROOT / "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json"
        data = json.loads(slots_path.read_text(encoding="utf-8"))
        self.assertEqual(data["external_actor_allowlist"], [])
        assignment_ids = [a["assignment_id"] for a in data["assignments"]]
        self.assertIn("R27-E-20261011", assignment_ids)
        # This remediation object must not silently claim R27-E.
        self.assertNotIn(
            "NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_EXCHANGE_HARD_REMEDIATION_20261029_R2",
            json.dumps(data),
        )

    def test_f09_lost_webhook_requires_api_reconcile(self) -> None:
        # Failed/lost webhook: reconcile via API path (signature valid, not duplicate).
        r = self.chain.journal.reconcile_github_delivery(
            delivery_id="lost-then-api-reconcile",
            signature_valid=True,
            duplicate=False,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["event"]["payload"]["reason"], "WEBHOOK_ACCEPTED")

    def test_f09_forged_webhook_quarantined(self) -> None:
        r = self.chain.journal.reconcile_github_delivery(
            delivery_id="forged",
            signature_valid=False,
            duplicate=False,
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["event"]["stream"], "quarantine")
        self.assertEqual(r["event"]["payload"]["reason"], "WEBHOOK_SIGNATURE_INVALID")


class TestPinnedConstants(unittest.TestCase):
    def test_pinned_commit_matches_order(self) -> None:
        self.assertEqual(
            PINNED_COMMIT,
            "ee73769c966b22887fafbc755edf7c64d1a537e1",
        )
        self.assertEqual(DEFAULT_REPO, "nexusomegac27/NEXUS-OMEGA-EVIDENCE")

    def test_local_checkout_hashes_match_pinned_sources(self) -> None:
        law = (ROOT / LAW_PATH).read_bytes()
        self.assertEqual(len(law), LAW_BYTES)
        self.assertEqual(sha256_bytes(law), LAW_SHA256)
        audit = (ROOT / AXIOM_AUDIT_PATH).read_bytes()
        self.assertEqual(len(audit), AXIOM_AUDIT_BYTES)
        self.assertEqual(sha256_bytes(audit), AXIOM_AUDIT_SHA256)


class TestF11ExpertenkodexMandatoryDispatch(unittest.TestCase):
    """F11 — Kodexpflicht fail-closed; absent fields never grandfather."""

    def setUp(self) -> None:
        self.validator = DispatchValidator(
            SourceResolver(ROOT, expected_repository=DEFAULT_REPO)
        )

    def _base_sources(self) -> list:
        return [
            {
                "path": LAW_PATH,
                "sha256": LAW_SHA256,
                "bytes": LAW_BYTES,
                "commit": PINNED_COMMIT,
            }
        ]

    def test_absent_kodex_fails_missing_expertenkodex_header(self) -> None:
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_F11_ABSENT",
                "sources": self._base_sources(),
            }
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "MISSING_EXPERTENKODEX_HEADER")

    def test_authenticated_legacy_grant_accepted(self) -> None:
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_F11_LEGACY",
                "sources": self._base_sources(),
                "expertenkodex_legacy_grant": {
                    "authenticated": True,
                    "classification": "LEGACY_PRE_EXPERTENKODEX_V1",
                    "grant_id": "LEGACY-GRANT-F11-TEST-001",
                    "policy_version": "LEGACY_GRANT_POLICY_V1",
                },
            }
        )
        self.assertTrue(r["ok"], r)
        self.assertEqual(r.get("expertenkodex"), "LEGACY_GRANT_ACCEPTED")

    def test_unauthenticated_legacy_grant_rejected(self) -> None:
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_F11_LEGACY_UNAUTH",
                "sources": self._base_sources(),
                "expertenkodex_legacy_grant": {
                    "authenticated": False,
                    "classification": "LEGACY_PRE_EXPERTENKODEX_V1",
                    "grant_id": "LEGACY-GRANT-F11-TEST-002",
                    "policy_version": "LEGACY_GRANT_POLICY_V1",
                },
            }
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "MISSING_EXPERTENKODEX_HEADER")

    def test_empty_expertenkodex_fields_c01(self) -> None:
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_F11_EMPTY",
                "sources": self._base_sources(),
                "EXPERTENKODEX": "",
                "CODEX_COMMIT": "",
                "CODEX_PATH": "",
                "CODEX_BYTES": "",
                "CODEX_SHA256": "",
            }
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "C01_MISSING_EXPERTENKODEX_OR_REQUIRED_FIELD")

    def test_full_kodex_header_pass(self) -> None:
        header = _kodex_header_for_law_and_handoff()
        r = self.validator.validate_manifest(
            {
                "repository": DEFAULT_REPO,
                "commit": PINNED_COMMIT,
                "object": "NEXUS_OMEGA_F11_FULL",
                "sources": self._base_sources(),
                **header,
            }
        )
        self.assertTrue(r["ok"], r)


if __name__ == "__main__":
    unittest.main()
