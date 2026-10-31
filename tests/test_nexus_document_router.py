#!/usr/bin/env python3
"""Isolated tests for scripts/nexus_document_router.py (Final Gated Release R0).

Bound to live APIs:
  DocumentRouter / DocumentStore / ReceiverAckProtocol / SourceResolver
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.nexus_document_router import (  # noqa: E402
    CLAIM_CEILING,
    DocumentRouter,
    DocumentStore,
    RouterConfig,
    classify_source,
    privacy_gate,
)
from scripts.nexus_github_exchange_chain import (  # noqa: E402
    DEFAULT_REPO,
    ReceiverAckProtocol,
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _run(cmd, cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True, capture_output=True)


def _init_mini_repo(tmpdir: Path) -> tuple[str, str, int]:
    """Create a tiny git repo with docs/hello.txt; origin matches DEFAULT_REPO."""
    _run(["git", "init"], cwd=tmpdir)
    _run(["git", "config", "user.email", "test@nexus.local"], cwd=tmpdir)
    _run(["git", "config", "user.name", "NEXUS Test"], cwd=tmpdir)
    # SourceResolver.repository_identity requires origin remote = DEFAULT_REPO.
    _run(
        [
            "git",
            "remote",
            "add",
            "origin",
            f"https://github.com/{DEFAULT_REPO}.git",
        ],
        cwd=tmpdir,
    )
    docs = tmpdir / "docs"
    docs.mkdir()
    payload = b"hello-router-fixture-v1\n"
    (docs / "hello.txt").write_bytes(payload)
    _run(["git", "add", "docs/hello.txt"], cwd=tmpdir)
    _run(["git", "commit", "-m", "fixture"], cwd=tmpdir)
    commit = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(tmpdir))
        .decode()
        .strip()
    )
    return commit, _sha256(payload), len(payload)


class ClassifySourceTests(unittest.TestCase):
    def test_public_safe(self) -> None:
        self.assertEqual(
            classify_source(path="docs/a.md", privacy_class="PUBLIC_SAFE"),
            "PUBLIC_SAFE_GITHUB",
        )

    def test_hold_private_marker(self) -> None:
        self.assertEqual(
            classify_source(path="secrets/token.json", privacy_class="PUBLIC_SAFE"),
            "HOLD_UNSUPPORTED_PRIVATE",
        )

    def test_redacted(self) -> None:
        self.assertEqual(
            classify_source(
                path="docs/a.md", privacy_class="PUBLIC_SAFE", redacted=True
            ),
            "REDACTED_COMMITMENT_ONLY",
        )


class PrivacyGateTests(unittest.TestCase):
    def test_hold_blocks(self) -> None:
        r = privacy_gate(
            source_class="HOLD_UNSUPPORTED_PRIVATE", path="secrets/x"
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "PRIVACY_HOLD_UNSUPPORTED_PRIVATE")

    def test_owner_private_needs_flag(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "PRIVACY_OWNER_PRIVATE_REQUIRES_EXPLICIT_FLAG")

    def test_owner_private_with_flag(self) -> None:
        r = privacy_gate(
            source_class="OWNER_GOVERNED_PRIVATE",
            path="private/x",
            allow_private_dispatch=True,
        )
        self.assertTrue(r["ok"])


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
        # Forward skip CREATED->DISPATCHED is valid; reverse is not.
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

    def test_force_active(self) -> None:
        cfg = RouterConfig(
            repo_root=self.root,
            store_path=self.root / "store2.sqlite",
            journal_dir=self.root / "journal2",
            cutover_force_active=True,
        )
        r = DocumentRouter(cfg)
        try:
            st = r.cutover_status()
            self.assertEqual(st["document_handoff"], "FRAMEWORK_REQUIRED_ACTIVE")
        finally:
            r.close()


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
        self.assertEqual(r["routing_state"], "DISPATCHED")
        self.assertEqual(r["source_class"], "PUBLIC_SAFE_GITHUB")
        self.assertEqual(r["independent_expert_ack"], "NOT_ESTABLISHED")
        self.assertFalse(r["terminal_pass"])
        self.assertEqual(r["manifest"]["sha256"], self.digest)
        self.assertEqual(r["manifest"]["bytes"], self.nbytes)

    def test_dispatch_hold_private(self) -> None:
        # privacy_gate runs before SourceResolver — HOLD without needing secrets/ in tree.
        r = self.router.dispatch_document(
            object_id="TEST_DOC_HOLD",
            repository=DEFAULT_REPO,
            commit=self.commit,
            path="secrets/token.json",
            privacy_class="HOLD_UNSUPPORTED_PRIVATE",
        )
        self.assertFalse(r.get("ok"))
        self.assertEqual(r["code"], "PRIVACY_HOLD_UNSUPPORTED_PRIVATE")

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

    def test_receive_foreign_process_ack(self) -> None:
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
        good = {
            "repository": DEFAULT_REPO,
            "commit": self.commit,
            "object_path": "docs/hello.txt",
            "bytes": self.nbytes,
            "sha256": self.digest,
            "fetch_method": "GIT_FETCH_SHOW",
            "process_id": "foreign-pid-99999",
            "authenticated": True,
            "receiver_principal": "expert-fixture",
        }
        ack = self.router.receive_receipt(document_id=doc_id, receipt=good)
        self.assertTrue(ack.get("ok"), msg=ack)
        self.assertEqual(ack["routing_state"], "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED")
        self.assertEqual(ack.get("independent_expert_ack"), "ESTABLISHED_REPORT_LEVEL")

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
        # Advance to RECEIVED_BYTES_VERIFIED — SCIENTIFIC_* not valid from DISPATCHED.
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
