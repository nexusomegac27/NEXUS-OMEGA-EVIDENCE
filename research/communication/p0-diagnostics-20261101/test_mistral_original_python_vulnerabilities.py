#!/usr/bin/env python3
"""NEXUS OMEGA — isolated original-Python P0 vulnerability regression witness.

This suite deliberately asserts that specific defects exist in the PINNED
2026-11-01 Cursor router. A PASS means the defect was REPRODUCED, never that
production is secure. It is a scientific baseline, NOT a merge/release gate,
and must not be reused to certify patched code.

Run from a detached source checkout with:
  python3 test_mistral_original_python_vulnerabilities.py <pinned_checkout_path>

No network, credentials, real GitHub comments, public POST, or privileged
system modifications. sqlite tests use only tempfile.TemporaryDirectory.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
    SOURCE_ROOT = Path(sys.argv.pop(1)).resolve()
else:
    SOURCE_ROOT = Path("subject").resolve()
sys.path.insert(0, str(SOURCE_ROOT / "scripts"))

from nexus_document_router import (  # noqa: E402
    DocumentStore,
    _valid_private_lane_proof,
    _valid_transition,
    validate_cutover_activation_manifest,
    verify_github_receiver_witness,
)
from nexus_github_exchange_chain import AgentAdapter  # noqa: E402

PINNED_COMMIT = "986b9af8f4bcfb341a188cbb6ed7d8da3d500e98"
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
SOURCE_SHA = "a" * 64
SOURCE_BYTES = 5


class FakeGitHubClient:
    """An injected *stub*, not proof of a connected authenticated GitHub API."""
    def __init__(self, fetched: dict):
        self.fetched = fetched
        self.calls = []

    def get_issue_comment(self, comment_id: int) -> dict:
        self.calls.append(comment_id)
        return dict(self.fetched)


def api_comment(comment_id: int, html_url: str, author: str = "external-test") -> dict:
    # Real GitHub REST response shape has no observed_sha256/observed_bytes.
    return {
        "id": comment_id,
        "user": {"id": 9012, "login": author},
        "html_url": html_url,
        "issue_url": f"https://api.github.com/repos/{REPO}/issues/42",
        "author_association": "NONE",
        "body": "I copied the source but this text is untrusted",
        "created_at": "2026-11-01T00:00:00Z",
    }


def untrusted_witness(comment_id: int, claimed_commit: str = "b" * 40) -> dict:
    return {
        "comment_id": comment_id,
        "observed_sha256": SOURCE_SHA,
        "observed_bytes": SOURCE_BYTES,
        "return_source_commit": claimed_commit,
        "return_source_sha256": SOURCE_SHA,
    }


def verify(comment: dict, witness: dict) -> dict:
    return verify_github_receiver_witness(
        witness=witness,
        document={
            "sha256": SOURCE_SHA,
            "bytes": SOURCE_BYTES,
            "repository": REPO,
            "commit_sha": PINNED_COMMIT,
            "path": "docs/one.md",
        },
        receipt={"producer_principal": "operator-owner", "repository": REPO},
        github_client=FakeGitHubClient(comment),
    )


class PinnedOriginalPythonDefectReproductions(unittest.TestCase):
    def test_01_genuine_issue_comment_html_url_rejected_X8(self):
        comment_id = 501
        actual_github_html_url = (
            f"https://github.com/{REPO}/issues/42#issuecomment-{comment_id}"
        )
        result = verify(
            api_comment(comment_id, actual_github_html_url),
            untrusted_witness(comment_id),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_IMMUTABLE_URL_INVALID")

    def test_02_unrelated_repository_pr_comment_accepted_F04(self):
        comment_id = 502
        result = verify(
            api_comment(
                comment_id,
                "https://github.com/unrelated/other-repo/pull/12#issuecomment-502",
            ),
            untrusted_witness(comment_id),
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["principal_verified"])
        self.assertTrue(result["return_source_verified"])

    def test_03_caller_only_hashes_promoted_with_real_api_schema_F02(self):
        comment_id = 503
        api_reply = api_comment(
            comment_id,
            f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}",
        )
        self.assertNotIn("observed_sha256", api_reply)
        self.assertNotIn("observed_bytes", api_reply)
        result = verify(api_reply, untrusted_witness(comment_id))
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["return_source_verified"])

    def test_04_unrelated_return_commit_treated_as_verified_F14(self):
        comment_id = 504
        result = verify(
            api_comment(
                comment_id,
                f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}",
            ),
            untrusted_witness(comment_id, claimed_commit="f" * 40),
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["return_source_verified"])

    def test_05_unregistered_author_association_none_passes_F05(self):
        comment_id = 505
        result = verify(
            api_comment(
                comment_id,
                f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}",
                author="unregistered-outsider",
            ),
            untrusted_witness(comment_id),
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["principal_verified"])

    def test_06_direct_state_skip_is_accepted_X3(self):
        self.assertTrue(_valid_transition("CREATED", "DISPATCHED"))
        self.assertTrue(_valid_transition("STAGED", "RETURN_SOURCE_VERIFIED"))

    def test_07_self_consistent_injected_cutover_authorizes_F09(self):
        manifest = {
            "object_id": "FORGED_CUTOVER_DIAGNOSTIC",
            "authority": "OPERATOR_ALEXANDER",
            "scope": "DOCUMENT_HANDOFF_CUTOVER",
            "activation_token": "NOT_A_REAL_OWNER_AUTHORIZATION",
            "evidence_sha256": "a" * 64,
            "evidence_bytes": 123,
            "authorized_at_utc": "2026-11-01T00:00:00Z",
            "authorized": "true",
        }
        injected = {
            "sha256": "a" * 64,
            "bytes": 123,
            "signer": "OPERATOR_ALEXANDER",
            "status": "AUTHORIZED",
        }
        self.assertTrue(
            validate_cutover_activation_manifest(
                manifest, trusted_cutover_evidence=injected
            )["ok"]
        )

    def test_08_private_registry_arbitrary_signer_passes_F10(self):
        result = _valid_private_lane_proof(
            {"entry_id": "attacker-lane"},
            owner_lane_registry={
                "attacker-lane": {
                    "status": "ACTIVE",
                    "scope": "OWNER_PRIVATE_DISPATCH",
                    "signer": "ATTACKER_NOT_VERIFIED",
                }
            },
        )
        self.assertTrue(result["ok"], result)

    def test_09_adapter_declare_does_not_return_router_status_X2(self):
        result = AgentAdapter().declare(model_id="test-model")
        self.assertTrue(result["ok"])
        self.assertNotIn("status", result)

    def test_10_sqlite_replay_raises_integrity_error_X1(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DocumentStore(Path(tmp) / "test.sqlite")
            try:
                kwargs = {
                    "object_id": "TEST_SOURCE",
                    "repository": REPO,
                    "commit_sha": PINNED_COMMIT,
                    "path": "docs/one.md",
                    "source_class": "PUBLIC_SAFE_GITHUB",
                    "privacy_class": "PUBLIC_SAFE_GITHUB",
                    "bytes_n": SOURCE_BYTES,
                    "sha256": SOURCE_SHA,
                    "document_id": "replayed-id",
                }
                store.create_document(**kwargs)
                with self.assertRaises(sqlite3.IntegrityError):
                    store.create_document(**kwargs)
            finally:
                store.close()

    def test_11_wal_normal_confirmed_X7_related(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DocumentStore(Path(tmp) / "test.sqlite")
            try:
                sync = store._conn.execute("PRAGMA synchronous").fetchone()[0]
                journal = store._conn.execute("PRAGMA journal_mode").fetchone()[0]
                self.assertEqual(journal.lower(), "wal")
                self.assertEqual(sync, 1, "SQLite synchronous=NORMAL = 1")
            finally:
                store.close()

    def test_12_positive_transport_test_contains_vacuous_or_true_X2(self):
        source = (SOURCE_ROOT / "tests" / "test_nexus_document_router.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("self.assertTrue(tr.get(\"ok\") or tr.get(\"adapter_proved\") or True)", source)


if __name__ == "__main__":
    print(json.dumps({
        "CLASSIFICATION": "EXPECTED_DEFECT_REPRODUCTIONS_NOT_SECURITY_PASS",
        "SUBJECT_COMMIT": PINNED_COMMIT,
        "EXTERNAL_API_CALLS": "NONE",
        "SOURCE_ROOT": str(SOURCE_ROOT),
    }, sort_keys=True), flush=True)
    unittest.main(verbosity=2)
