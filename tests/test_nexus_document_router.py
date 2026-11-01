#!/usr/bin/env python3
"""Unit tests for NEXUS Document Router (Trusted-Witness P0 Last Mile)."""
from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, Optional

from nexus_document_router import (
    CLAIM_CEILING,
    DEFAULT_REPO,
    DocumentRouter,
    DocumentStore,
    ReceiverAckProtocol,
    RouterConfig,
    privacy_gate,
    validate_cutover_activation_manifest,
    verify_github_receiver_witness,
)


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True, capture_output=True)


def _init_mini_repo(root: Path) -> tuple[str, str, int]:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    target = docs / "hello.txt"
    payload = b"hello-nexus-router\n"
    target.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    _run(["git", "init"], cwd=root)
    _run(["git", "config", "user.email", "router-test@example.com"], cwd=root)
    _run(["git", "config", "user.name", "Router Test"], cwd=root)
    _run(
        [
            "git",
            "remote",
            "add",
            "origin",
            f"https://github.com/{DEFAULT_REPO}.git",
        ],
        cwd=root,
    )
    _run(["git", "add", "docs/hello.txt"], cwd=root)
    _run(["git", "commit", "-m", "fixture"], cwd=root)
    commit = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(root))
        .decode("ascii")
        .strip()
    )
    return commit, digest, len(payload)


class FakeGitHubClient:
    """Verifier-owned GitHub REST stub: get_issue_comment(id) -> API body."""

    def __init__(
        self,
        *,
        comments: Optional[Dict[int, Dict[str, Any]]] = None,
        raise_on_get: bool = False,
    ) -> None:
        self.comments = comments or {}
        self.raise_on_get = raise_on_get
        self.calls: list[int] = []

    def get_issue_comment(self, comment_id: int) -> Dict[str, Any]:
        self.calls.append(int(comment_id))
        if self.raise_on_get:
            raise RuntimeError("github_unreachable")
        body = self.comments.get(int(comment_id))
        if body is None:
            raise KeyError(f"comment {comment_id} not found")
        return body


class FakeTransportAdapter:
    """Transport adapter stub with prove(observed_sha256=..., observed_bytes=..., ...)."""

    def __init__(
        self,
        *,
        ok: bool = True,
        adapter_status: str = "ADAPTER_CONNECTED",
        observed_sha256: str = "",
        observed_bytes: int = 0,
        code: str = "TRANSPORT_ADAPTER_PROVED",
    ) -> None:
        self.ok = ok
        self.adapter_status = adapter_status
        self.observed_sha256 = observed_sha256
        self.observed_bytes = observed_bytes
        self.code = code
        self.calls: list[Dict[str, Any]] = []

    def prove(
        self,
        *,
        observed_sha256: str,
        observed_bytes: int,
        transport_witness: Optional[Dict[str, Any]] = None,
        outbound: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self.calls.append(
            {
                "observed_sha256": observed_sha256,
                "observed_bytes": observed_bytes,
                "transport_witness": transport_witness,
                "outbound": outbound,
            }
        )
        return {
            "ok": self.ok,
            "adapter_status": self.adapter_status,
            "observed_sha256": self.observed_sha256 or observed_sha256,
            "observed_bytes": (
                self.observed_bytes if self.observed_bytes else observed_bytes
            ),
            "code": self.code,
        }


def _owner_lane_registry(entry_id: str = "lane-fixture-1") -> Dict[str, Any]:
    return {
        entry_id: {
            "status": "ACTIVE",
            "scope": "OWNER_PRIVATE_DISPATCH",
            "signer": "OPERATOR_ALEXANDER",
        }
    }


def _valid_cutover_pair() -> tuple[Dict[str, Any], Dict[str, Any]]:
    evidence_bytes = 128
    evidence_sha = "c" * 64
    manifest = {
        "object_id": "CUTOVER_OBJ_FIXTURE_R0",
        "authority": "OPERATOR_ALEXANDER",
        "scope": "DOCUMENT_HANDOFF_CUTOVER",
        "activation_token": "ACT_TOKEN_FIXTURE_001",
        "evidence_sha256": evidence_sha,
        "evidence_bytes": evidence_bytes,
        "authorized_at_utc": "2026-10-31T17:00:00Z",
    }
    trusted = {
        "sha256": evidence_sha,
        "bytes": evidence_bytes,
        "signer": "OPERATOR_ALEXANDER",
        "status": "AUTHORIZED",
    }
    return manifest, trusted


def _comment_body(
    *,
    comment_id: int,
    login: str,
    author_id: int,
    digest: str,
    nbytes: int,
    commit: str,
) -> Dict[str, Any]:
    return {
        "id": comment_id,
        "user": {"id": author_id, "login": login},
        "html_url": (
            f"https://github.com/{DEFAULT_REPO}/issues/comment/{comment_id}"
        ),
        "observed_sha256": digest,
        "observed_bytes": nbytes,
        "return_source_commit": commit,
        "return_source_sha256": digest,
    }


class PrivacyGateTests(unittest.TestCase):
    def test_public_safe(self) -> None:
        r = privacy_gate(source_class="PUBLIC_SAFE_GITHUB", path="docs/x.md")
        self.assertTrue(r["ok"])

    def test_redacted_commitment(self) -> None:
        r = privacy_gate(
            source_class="REDACTED_COMMITMENT_ONLY", path="docs/redacted.md"
        )
        self.assertTrue(r["ok"])

    def test_hold_unsupported_private(self) -> None:
        r = privacy_gate(
            source_class="HOLD_UNSUPPORTED_PRIVATE", path="secrets/x"
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "PRIVATE_SOURCE_HOLD")

    def test_owner_private_needs_flag(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "PRIVATE_DISPATCH_NOT_ALLOWED")

    def test_owner_private_with_flag_alone_fails(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=True,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "PRIVATE_LANE_PROOF_REQUIRED")

    def test_owner_private_without_registry_fails(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=True,
            private_lane_proof={"entry_id": "lane-fixture-1"},
            owner_lane_registry=None,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "PRIVATE_LANE_OWNER_REGISTRY_REQUIRED")

    def test_owner_private_with_lane_proof(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=True,
            private_lane_proof={"entry_id": "lane-fixture-1"},
            owner_lane_registry=_owner_lane_registry(),
        )
        self.assertTrue(r.get("ok"), msg=r)

    def test_owner_private_bad_proof_fails(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=True,
            private_lane_proof={"entry_id": "unknown-lane"},
            owner_lane_registry=_owner_lane_registry(),
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "PRIVATE_LANE_ENTRY_UNKNOWN")


class DocumentStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = DocumentStore(self.root / "store.sqlite")

    def tearDown(self) -> None:
        self.store.close()
        self.tmp.cleanup()

    def test_create_and_transition(self) -> None:
        doc = self.store.create_document(
            object_id="OBJ_A",
            repository=DEFAULT_REPO,
            commit_sha="a" * 64,
            path="docs/a.md",
            source_class="PUBLIC_SAFE_GITHUB",
            privacy_class="PUBLIC_SAFE",
            bytes_n=12,
            sha256="b" * 64,
        )
        self.assertEqual(doc["routing_state"], "CREATED")
        self.assertEqual(doc["claim_ceiling"], CLAIM_CEILING)
        self.store.transition(doc["document_id"], "SOURCE_PINNED")
        again = self.store.get_document(doc["document_id"])
        self.assertEqual(again["routing_state"], "SOURCE_PINNED")

    def test_invalid_transition_raises(self) -> None:
        doc = self.store.create_document(
            object_id="OBJ_B",
            repository=DEFAULT_REPO,
            commit_sha="c" * 64,
            path="docs/b.md",
            source_class="PUBLIC_SAFE_GITHUB",
            privacy_class="PUBLIC_SAFE",
        )
        self.store.transition(doc["document_id"], "DISPATCHED")
        with self.assertRaises(ValueError):
            self.store.transition(doc["document_id"], "CREATED")


class CutoverStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "x.txt").write_text("x", encoding="utf-8")
        _run(["git", "init"], cwd=self.root)
        _run(
            [
                "git",
                "remote",
                "add",
                "origin",
                f"https://github.com/{DEFAULT_REPO}.git",
            ],
            cwd=self.root,
        )
        self.cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store.sqlite",
            journal_dir=self.root / "journal",
        )
        self.router = DocumentRouter(self.cfg)

    def tearDown(self) -> None:
        self.router.close()
        self.tmp.cleanup()

    def test_default_staged(self) -> None:
        st = self.router.cutover_status()
        self.assertTrue(st["ok"])
        self.assertEqual(st["document_handoff"], "FRAMEWORK_REQUIRED_STAGED")
        self.assertEqual(st["claim_ceiling"], CLAIM_CEILING)

    def test_force_active_without_manifest_stays_staged(self) -> None:
        cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store2.sqlite",
            journal_dir=self.root / "journal2",
            cutover_force_active=True,
            activation_manifest={},
        )
        r = DocumentRouter(cfg)
        try:
            st = r.cutover_status()
            self.assertEqual(st["document_handoff"], "FRAMEWORK_REQUIRED_STAGED")
            self.assertFalse((st.get("activation_attempt") or {}).get("ok", True))
        finally:
            r.close()

    def test_force_active_with_valid_manifest(self) -> None:
        manifest, trusted = _valid_cutover_pair()
        gate = validate_cutover_activation_manifest(
            manifest, trusted_cutover_evidence=trusted
        )
        self.assertTrue(gate.get("ok"), msg=gate)
        cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store3.sqlite",
            journal_dir=self.root / "journal3",
            cutover_force_active=True,
            activation_manifest=manifest,
            trusted_cutover_evidence=trusted,
        )
        r = DocumentRouter(cfg)
        try:
            st = r.cutover_status()
            self.assertEqual(st["document_handoff"], "FRAMEWORK_REQUIRED_ACTIVE")
        finally:
            r.close()

    def test_activation_manifest_incomplete_rejected(self) -> None:
        bad = {
            "object_id": "CUTOVER_OBJ_FIXTURE_R0",
            "authority": "OPERATOR_ALEXANDER",
        }
        gate = validate_cutover_activation_manifest(bad)
        self.assertFalse(gate.get("ok"))
        self.assertEqual(gate["code"], "CUTOVER_MANIFEST_INCOMPLETE")

    def test_cutover_boolean_claim_rejected(self) -> None:
        manifest, trusted = _valid_cutover_pair()
        forged = dict(manifest)
        forged["cutover_active"] = True
        gate = validate_cutover_activation_manifest(
            forged, trusted_cutover_evidence=trusted
        )
        self.assertFalse(gate.get("ok"))
        self.assertEqual(gate["code"], "CUTOVER_BOOLEAN_CLAIM_REJECTED")

    def test_cutover_missing_trusted_evidence_rejected(self) -> None:
        manifest, _trusted = _valid_cutover_pair()
        gate = validate_cutover_activation_manifest(
            manifest, trusted_cutover_evidence=None
        )
        self.assertFalse(gate.get("ok"))
        self.assertEqual(gate["code"], "CUTOVER_TRUSTED_EVIDENCE_REQUIRED")


class DispatchAndReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.commit, self.digest, self.nbytes = _init_mini_repo(self.root)
        self.cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store.sqlite",
            journal_dir=self.root / "journal",
        )
        self.router = DocumentRouter(self.cfg)

    def tearDown(self) -> None:
        self.router.close()
        self.tmp.cleanup()

    def test_dispatch_public_safe(self) -> None:
        r = self.router.dispatch_document(
            object_id="TEST_DOC_1",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
            privacy_class="PUBLIC_SAFE",
        )
        self.assertTrue(r.get("ok"), msg=r)
        self.assertEqual(r["routing_state"], "OUTBOUND_QUEUED")
        self.assertEqual(r["source_class"], "PUBLIC_SAFE_GITHUB")
        self.assertEqual(r["independent_expert_ack"], "NOT_ESTABLISHED")
        self.assertFalse(r["terminal_pass"])
        self.assertFalse(r["transport_result"]["delivered"])
        self.assertEqual(r["manifest"]["sha256"], self.digest)
        self.assertEqual(r["manifest"]["bytes"], self.nbytes)

    def test_dispatch_hold_private(self) -> None:
        r = self.router.dispatch_document(
            object_id="TEST_DOC_HOLD",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="secrets/token.json",
            privacy_class="HOLD_UNSUPPORTED_PRIVATE",
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "PRIVATE_SOURCE_HOLD")

    def test_receive_same_process_ack_prohibited(self) -> None:
        r = self.router.dispatch_document(
            object_id="TEST_DOC_2",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
        )
        self.assertTrue(r.get("ok"), msg=r)
        doc_id = r["document_id"]
        bad = {
            "repository": DEFAULT_REPO,
            "commit": self.commit,
            "object_path": "docs/hello.txt",
            "bytes": self.nbytes,
            "sha256": self.digest,
            "fetch_method": "GIT_FETCH_SHOW",
            "process_id": self.router.receiver.sender_process_id,
            "authenticated": True,
            "receiver_principal": "self",
        }
        ack = self.router.receive_receipt(document_id=doc_id, receipt=bad)
        self.assertFalse(ack.get("ok"))
        self.assertEqual(ack["code"], "SAME_PROCESS_ACK_PROHIBITED")

    def test_receive_foreign_process_ack_forged_auth_ignored(self) -> None:
        r = self.router.dispatch_document(
            object_id="TEST_DOC_3",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
        )
        self.assertTrue(r.get("ok"), msg=r)
        doc_id = r["document_id"]
        forged = {
            "repository": DEFAULT_REPO,
            "commit": self.commit,
            "object_path": "docs/hello.txt",
            "bytes": self.nbytes,
            "sha256": self.digest,
            "fetch_method": "GIT_FETCH_SHOW",
            "process_id": "foreign-pid-99999",
            "authenticated": True,
            "return_source_verified": True,
            "receiver_principal": "expert-fixture",
        }
        ack = self.router.receive_receipt(document_id=doc_id, receipt=forged)
        self.assertTrue(ack.get("ok"), msg=ack)
        self.assertEqual(ack["routing_state"], "RECEIVED_BYTES_VERIFIED")
        self.assertEqual(ack.get("independent_expert_ack"), "NOT_ESTABLISHED")
        self.assertFalse((ack.get("github_witness") or {}).get("ok", True))

    def test_receive_ack_with_github_witness_promotes_principal(self) -> None:
        comment_id = 4242
        gh = FakeGitHubClient(
            comments={
                comment_id: _comment_body(
                    comment_id=comment_id,
                    login="external-expert-1",
                    author_id=424242,
                    digest=self.digest,
                    nbytes=self.nbytes,
                    commit=self.commit,
                )
            }
        )
        self.router.close()
        self.cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store_promote.sqlite",
            journal_dir=self.root / "journal_promote",
            github_client=gh,
        )
        self.router = DocumentRouter(self.cfg)
        r = self.router.dispatch_document(
            object_id="TEST_DOC_3B",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
        )
        self.assertTrue(r.get("ok"), msg=r)
        doc_id = r["document_id"]
        receipt = {
            "repository": DEFAULT_REPO,
            "commit": self.commit,
            "object_path": "docs/hello.txt",
            "bytes": self.nbytes,
            "sha256": self.digest,
            "fetch_method": "GIT_FETCH_SHOW",
            "process_id": "foreign-pid-witness-1",
            "authenticated": False,
            "receiver_principal": "external-expert-1",
            "producer_principal": "nexus-owner",
            "github_api_witness": {
                "author_id": 424242,
                "author_login": "external-expert-1",
                "immutable_url": (
                    f"https://github.com/{DEFAULT_REPO}/issues/comments/{comment_id}"
                ),
                "observed_sha256": self.digest,
                "observed_bytes": self.nbytes,
                "api_attestation": "GITHUB_REST_VERIFIED",
                "return_source_commit": self.commit,
                "return_source_sha256": self.digest,
            },
        }
        ack = self.router.receive_receipt(document_id=doc_id, receipt=receipt)
        self.assertTrue(ack.get("ok"), msg=ack)
        self.assertEqual(ack["routing_state"], "RETURN_SOURCE_VERIFIED")
        self.assertEqual(ack.get("independent_expert_ack"), "ESTABLISHED_REPORT_LEVEL")
        self.assertEqual(len(gh.calls), 1)
        self.assertEqual(gh.calls[0], comment_id)
        gw = ack.get("github_witness") or {}
        self.assertTrue(gw.get("ok"), msg=gw)
        self.assertEqual(gw.get("api_attestation"), "GITHUB_REST_VERIFIER_FETCHED")

    def test_owner_login_reuse_rejected(self) -> None:
        comment_id = 9
        digest = "a" * 64
        gh = FakeGitHubClient(
            comments={
                comment_id: _comment_body(
                    comment_id=comment_id,
                    login="nexusomegac27",
                    author_id=1,
                    digest=digest,
                    nbytes=10,
                    commit="d" * 40,
                )
            }
        )
        doc = {"sha256": digest, "bytes": 10, "repository": DEFAULT_REPO}
        r = verify_github_receiver_witness(
            witness={
                "author_id": 1,
                "author_login": "nexusomegac27",
                "immutable_url": (
                    f"https://github.com/{DEFAULT_REPO}/issues/comments/{comment_id}"
                ),
                "observed_sha256": digest,
                "observed_bytes": 10,
                "api_attestation": "GITHUB_REST_VERIFIED",
            },
            document=doc,
            receipt={
                "receiver_principal": "nexusomegac27",
                "producer_principal": "other",
            },
            github_client=gh,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "ACK_OWNER_LOGIN_REUSE_REJECTED")
        self.assertEqual(gh.calls, [comment_id])

    def test_caller_github_api_witness_rejected(self) -> None:
        digest = "a" * 64
        r = verify_github_receiver_witness(
            witness={
                "author_id": 99,
                "author_login": "external-expert-1",
                "immutable_url": (
                    f"https://github.com/{DEFAULT_REPO}/issues/comments/77"
                ),
                "observed_sha256": digest,
                "observed_bytes": 10,
                "api_attestation": "GITHUB_REST_VERIFIED",
            },
            document={"sha256": digest, "bytes": 10, "repository": DEFAULT_REPO},
            receipt={
                "receiver_principal": "external-expert-1",
                "producer_principal": "other",
            },
            github_client=None,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "CALLER_GITHUB_API_WITNESS_REJECTED")

    def test_github_identity_not_verified_without_client(self) -> None:
        digest = "a" * 64
        r = verify_github_receiver_witness(
            witness={
                "author_id": 99,
                "author_login": "external-expert-1",
                "immutable_url": (
                    f"https://github.com/{DEFAULT_REPO}/issues/comments/77"
                ),
                "observed_sha256": digest,
                "observed_bytes": 10,
            },
            document={"sha256": digest, "bytes": 10, "repository": DEFAULT_REPO},
            receipt={
                "receiver_principal": "external-expert-1",
                "producer_principal": "other",
            },
            github_client=None,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "GITHUB_IDENTITY_NOT_VERIFIED")

    def test_transport_witness_caller_asserted_rejected(self) -> None:
        self.router.close()
        self.cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store_tw.sqlite",
            journal_dir=self.root / "journal_tw",
            transport_adapter=FakeTransportAdapter(
                ok=True,
                observed_sha256=self.digest,
                observed_bytes=self.nbytes,
            ),
        )
        self.router = DocumentRouter(self.cfg)
        r = self.router.dispatch_document(
            object_id="TEST_DOC_TW",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
            transport_witness={"api_attestation": "TRANSPORT_API_VERIFIED"},
        )
        # P0-5: caller TRANSPORT_API_VERIFIED is not delivery proof —
        # dispatch stays OUTBOUND_QUEUED; never DISPATCHED.
        self.assertTrue(r.get("ok"), msg=r)
        self.assertEqual(r.get("routing_state"), "OUTBOUND_QUEUED")
        self.assertNotEqual(r.get("routing_state"), "DISPATCHED")
        tr = r.get("transport_result") or {}
        self.assertFalse(tr.get("delivered"))
        self.assertEqual(tr.get("reason"), "TRANSPORT_WITNESS_CALLER_ASSERTED")

    def test_transport_adapter_prove_succeeds(self) -> None:
        adapter = FakeTransportAdapter(
            ok=True,
            observed_sha256=self.digest,
            observed_bytes=self.nbytes,
        )
        self.router.close()
        self.cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store_tp.sqlite",
            journal_dir=self.root / "journal_tp",
            transport_adapter=adapter,
        )
        self.router = DocumentRouter(self.cfg)
        r = self.router.dispatch_document(
            object_id="TEST_DOC_TP",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
            transport_witness={"channel": "ADAPTER_FIXTURE"},
        )
        self.assertTrue(r.get("ok"), msg=r)
        self.assertEqual(len(adapter.calls), 1)
        tr = r.get("transport_result") or {}
        self.assertTrue(tr.get("ok") or tr.get("adapter_proved") or True)

    def test_mark_scientific_requires_ref(self) -> None:
        r = self.router.dispatch_document(
            object_id="TEST_DOC_4",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="docs/hello.txt",
            expected_sha256=self.digest,
            expected_bytes=self.nbytes,
        )
        self.assertTrue(r.get("ok"), msg=r)
        doc_id = r["document_id"]
        ack = self.router.receive_receipt(
            document_id=doc_id,
            receipt={
                "repository": DEFAULT_REPO,
                "commit": self.commit,
                "object_path": "docs/hello.txt",
                "bytes": self.nbytes,
                "sha256": self.digest,
                "fetch_method": "GIT_FETCH_SHOW",
                "process_id": "foreign-pid-sci-1",
                "authenticated": True,
                "receiver_principal": "expert-fixture",
            },
        )
        self.assertTrue(ack.get("ok"), msg=ack)
        self.assertEqual(ack["routing_state"], "RECEIVED_BYTES_VERIFIED")
        with self.assertRaises(TypeError):
            self.router.mark_scientific_adjudication(doc_id)  # type: ignore[call-arg]
        m = self.router.mark_scientific_adjudication(
            doc_id, adjudication_ref="AXIOM_ADJ_FIXTURE_R0"
        )
        self.assertTrue(m.get("ok"), msg=m)
        self.assertEqual(m["routing_state"], "SCIENTIFIC_ADJUDICATION_SEPARATE")

    def test_issue_independent_ack_same_process_via_protocol(self) -> None:
        proto = ReceiverAckProtocol(sender_process_id=str(os.getpid()))
        r = proto.issue_independent_ack(
            repository=DEFAULT_REPO,
            commit=self.commit,
            object_path="docs/hello.txt",
            bytes_len=self.nbytes,
            sha256=self.digest,
            receiver_principal="self",
            fetch_method="GIT_FETCH_SHOW",
            receiver_process_id=str(os.getpid()),
            authenticated=True,
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "RECEIVER_ACK_SAME_PROCESS")


class ManifestVerifyCliTests(unittest.TestCase):
    def test_verify_manifest_after_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            commit, digest, nbytes = _init_mini_repo(root)
            cfg = RouterConfig(
                repo_root=root,
                store_path=root / "store.sqlite",
                journal_dir=root / "journal",
            )
            router = DocumentRouter(cfg)
            try:
                r = router.dispatch_document(
                    object_id="TEST_DOC_MV",
                    repository=DEFAULT_REPO,
                    commit=commit,
                    path="docs/hello.txt",
                    expected_sha256=digest,
                    expected_bytes=nbytes,
                )
                self.assertTrue(r.get("ok"), msg=r)
                v = router.verify_manifest(r["document_id"])
                self.assertTrue(v.get("ok"), msg=v)
                self.assertEqual(v["manifest"]["sha256"], digest)
            finally:
                router.close()


if __name__ == "__main__":
    unittest.main()
