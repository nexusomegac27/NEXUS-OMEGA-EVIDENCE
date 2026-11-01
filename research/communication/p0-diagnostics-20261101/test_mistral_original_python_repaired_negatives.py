#!/usr/bin/env python3
"""NEXUS OMEGA — repaired-negative original-Python suite (PASS = DEFECT FIXED).

Companion to test_mistral_original_python_vulnerabilities.py, which remains the
historical EXPECTED_DEFECT_REPRODUCED baseline against pin 986b9af8….

This suite asserts the opposite contracts after the Cursor hard-repair tip:
PASS means the previously reproduced defect no longer occurs. It is still
C1_DESCRIPTIVE_ONLY and is NOT a production security seal, merge authority,
or EXTERNAL_ACK / CUTOVER / PUBLIC_WRITE authorization.

Run from the repaired checkout:
  python3 test_mistral_original_python_repaired_negatives.py <repaired_checkout_path>

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
    SOURCE_ROOT = Path(".").resolve()
sys.path.insert(0, str(SOURCE_ROOT / "scripts"))

from nexus_document_router import (  # noqa: E402
    DocumentStore,
    _valid_private_lane_proof,
    _valid_transition,
    validate_cutover_activation_manifest,
    verify_github_receiver_witness,
)
from nexus_github_exchange_chain import AgentAdapter  # noqa: E402

HISTORICAL_DEFECT_PIN = "986b9af8f4bcfb341a188cbb6ed7d8da3d500e98"
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
SOURCE_SHA = "a" * 64
SOURCE_BYTES = 5
DOC_COMMIT = "4bb65994a28ec2afc58384edd24b29a2dc680b44"


class FakeGitHubClient:
    """Injected stub — not proof of a connected authenticated GitHub API."""

    def __init__(self, fetched: dict):
        self.fetched = fetched
        self.calls = []

    def get_issue_comment(self, comment_id: int) -> dict:
        self.calls.append(comment_id)
        return dict(self.fetched)


def claim_body(
    *,
    commit: str = DOC_COMMIT,
    sha: str = SOURCE_SHA,
    nbytes: int = SOURCE_BYTES,
) -> str:
    return (
        "CLAIM_COMMIT="
        + commit
        + "\nCLAIM_SHA256="
        + sha
        + "\nCLAIM_BYTES="
        + str(nbytes)
        + "\n"
    )


def trusted_comment(
    comment_id: int,
    html_url: str,
    *,
    author: str = "trusted-collaborator",
    association: str = "COLLABORATOR",
    commit: str = DOC_COMMIT,
    sha: str = SOURCE_SHA,
    nbytes: int = SOURCE_BYTES,
) -> dict:
    return {
        "id": comment_id,
        "user": {"id": 9012, "login": author},
        "html_url": html_url,
        "issue_url": f"https://api.github.com/repos/{REPO}/issues/42",
        "author_association": association,
        "body": claim_body(commit=commit, sha=sha, nbytes=nbytes),
        "created_at": "2026-11-01T00:00:00Z",
    }


def bare_api_comment(comment_id: int, html_url: str, author: str = "external-test") -> dict:
    """Real GitHub REST shape: no observed_sha256/observed_bytes and no CLAIM_*."""
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


def verify(comment: dict, witness: dict, **extra) -> dict:
    w = dict(witness)
    # Caller attestation is an envelope field — never a verifier kwarg.
    if "api_attestation" in extra:
        w["api_attestation"] = extra.pop("api_attestation")
    if extra:
        raise TypeError(f"unexpected verify() kwargs: {sorted(extra)}")
    return verify_github_receiver_witness(
        witness=w,
        document={
            "sha256": SOURCE_SHA,
            "bytes": SOURCE_BYTES,
            "repository": REPO,
            "commit_sha": DOC_COMMIT,
            "path": "docs/one.md",
        },
        receipt={"producer_principal": "operator-owner", "repository": REPO},
        github_client=FakeGitHubClient(comment),
    )


class RepairedOriginalPythonNegatives(unittest.TestCase):
    """PASS = previously reproduced defect is FIXED on the repaired tip."""

    def test_01_genuine_issue_comment_html_url_accepted_X8_fixed(self):
        comment_id = 601
        genuine = f"https://github.com/{REPO}/issues/42#issuecomment-{comment_id}"
        result = verify(
            trusted_comment(comment_id, genuine),
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result.get("principal_verified"))
        self.assertTrue(result.get("return_source_verified"))

    def test_01b_bare_issues_comments_api_html_still_rejected_X8_bound(self):
        comment_id = 6011
        bad = f"https://github.com/{REPO}/issues/comments/{comment_id}"
        result = verify(
            trusted_comment(comment_id, bad),
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_IMMUTABLE_URL_INVALID")

    def test_02_unrelated_repository_pr_comment_rejected_F04_fixed(self):
        comment_id = 602
        result = verify(
            trusted_comment(
                comment_id,
                "https://github.com/unrelated/other-repo/pull/12#issuecomment-602",
            ),
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_REPO_MISMATCH")

    def test_03_caller_only_hashes_without_claim_fields_rejected_F02_fixed(self):
        comment_id = 603
        api_reply = bare_api_comment(
            comment_id,
            f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}",
        )
        api_reply["author_association"] = "COLLABORATOR"
        self.assertNotIn("observed_sha256", api_reply)
        self.assertNotIn("observed_bytes", api_reply)
        result = verify(
            api_reply,
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_CLAIM_FIELDS_MISSING")

    def test_03b_caller_api_attestation_always_rejected_F02_bound(self):
        comment_id = 6032
        genuine = f"https://github.com/{REPO}/issues/42#issuecomment-{comment_id}"
        result = verify(
            trusted_comment(comment_id, genuine),
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
            api_attestation="GITHUB_REST_VERIFIED",
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_CALLER_ATTESTATION_REJECTED")

    def test_04_unrelated_return_commit_rejected_F14_fixed(self):
        comment_id = 604
        foreign_commit = "f" * 40
        genuine = f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}"
        result = verify(
            trusted_comment(comment_id, genuine, commit=foreign_commit),
            untrusted_witness(comment_id, claimed_commit=foreign_commit),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_RETURN_COMMIT_MISMATCH")

    def test_05_unregistered_author_association_none_rejected_F05_fixed(self):
        comment_id = 605
        genuine = f"https://github.com/{REPO}/pull/185#issuecomment-{comment_id}"
        result = verify(
            trusted_comment(
                comment_id,
                genuine,
                author="unregistered-outsider",
                association="NONE",
            ),
            untrusted_witness(comment_id, claimed_commit=DOC_COMMIT),
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "ACK_GITHUB_ASSOCIATION_REJECTED")

    def test_06_direct_state_skip_rejected_X3_fixed(self):
        self.assertFalse(_valid_transition("CREATED", "DISPATCHED"))
        self.assertFalse(_valid_transition("STAGED", "RETURN_SOURCE_VERIFIED"))
        self.assertFalse(
            _valid_transition("OUTBOUND_QUEUED", "SCIENTIFIC_ADJUDICATION_SEPARATE")
        )

    def test_07_boolean_cutover_claim_rejected_F09_fixed(self):
        manifest = {
            "object_id": "FORGED_CUTOVER_DIAGNOSTIC",
            "authority": "OPERATOR_ALEXANDER",
            "scope": "DOCUMENT_HANDOFF_CUTOVER",
            "activation_token": "NOT_A_REAL_OWNER_AUTHORIZATION",
            "evidence_sha256": "a" * 64,
            "evidence_bytes": 123,
            "authorized_at_utc": "2026-11-01T00:00:00Z",
            "authorized": "true",
            "attestation_kind": "OWNER_CUTOVER_ATTESTATION",
            "attestation_ref": "urn:nexus:cutover:test",
        }
        injected = {
            "sha256": "a" * 64,
            "bytes": 123,
            "signer": "OPERATOR_ALEXANDER",
            "status": "AUTHORIZED",
        }
        result = validate_cutover_activation_manifest(
            manifest, trusted_cutover_evidence=injected
        )
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "CUTOVER_BOOLEAN_CLAIM_REJECTED")

    def test_08_private_registry_arbitrary_signer_rejected_F10_fixed(self):
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
        self.assertFalse(result["ok"], result)

    def test_08b_private_lane_without_owner_registry_rejected_F10_bound(self):
        result = _valid_private_lane_proof({"entry_id": "any"})
        self.assertFalse(result["ok"], result)
        self.assertEqual(result.get("code"), "PRIVATE_LANE_OWNER_REGISTRY_REQUIRED")

    def test_09_adapter_declare_returns_declared_status_X2_fixed(self):
        result = AgentAdapter().declare(model_id="test-model")
        self.assertTrue(result["ok"])
        self.assertIn("status", result)
        self.assertEqual(result["status"], "DECLARED")

    def test_10_sqlite_identical_replay_idempotent_X1_fixed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DocumentStore(Path(tmp) / "test.sqlite")
            try:
                kwargs = {
                    "object_id": "TEST_SOURCE",
                    "repository": REPO,
                    "commit_sha": DOC_COMMIT,
                    "path": "docs/one.md",
                    "source_class": "PUBLIC_SAFE_GITHUB",
                    "privacy_class": "PUBLIC_SAFE_GITHUB",
                    "bytes_n": SOURCE_BYTES,
                    "sha256": SOURCE_SHA,
                    "document_id": "replayed-id",
                }
                first = store.create_document(**kwargs)
                second = store.create_document(**kwargs)
                self.assertEqual(first["document_id"], second["document_id"])
                self.assertEqual(first["sha256"], second["sha256"])
            finally:
                store.close()

    def test_11_wal_full_confirmed_X7_fixed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DocumentStore(Path(tmp) / "test.sqlite")
            try:
                sync = store._conn.execute("PRAGMA synchronous").fetchone()[0]
                journal = store._conn.execute("PRAGMA journal_mode").fetchone()[0]
                self.assertEqual(journal.lower(), "wal")
                self.assertEqual(sync, 2, "SQLite synchronous=FULL = 2")
            finally:
                store.close()

    def test_12_positive_transport_test_vacuous_or_true_absent_X2_fixed(self):
        source = (SOURCE_ROOT / "tests" / "test_nexus_document_router.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn(
            'self.assertTrue(tr.get("ok") or tr.get("adapter_proved") or True)',
            source,
        )
        self.assertNotIn(" or True)", source)


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "CLASSIFICATION": "REPAIRED_NEGATIVE_PASS_EQUALS_DEFECT_FIXED",
                "HISTORICAL_DEFECT_PIN": HISTORICAL_DEFECT_PIN,
                "CLAIM_CEILING": "C1_DESCRIPTIVE_ONLY",
                "P0_SECURITY_SEAL": "NOT_YET_ESTABLISHED",
                "EXTERNAL_API_CALLS": "NONE",
                "SOURCE_ROOT": str(SOURCE_ROOT),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    unittest.main(verbosity=2)
