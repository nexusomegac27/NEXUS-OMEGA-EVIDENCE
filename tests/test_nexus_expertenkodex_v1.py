#!/usr/bin/env python3
"""Expertenkodex V1 — C01–C16 adversarial fixtures + positive source-bind tests.

OBJECT: NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED order commit: 63721950b3c0818e7f6892f83e9b5ee4fd0a5762
CODEX_COMMIT: b17d38266777bad61178e608d09e41726b9f4769
"""
from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, Dict, List

from scripts.nexus_expertenkodex_validator import (
    CANONICAL_PIN,
    CODEX_BYTES,
    CODEX_COMMIT,
    CODEX_OBJECT,
    CODEX_PATH,
    CODEX_SHA256,
    ExpertenkodexAdversarialGate,
    ExpertenkodexCausalMachine,
    ExpertenkodexHeaderValidator,
    build_obligatory_expert_order_header,
    verify_local_codex_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
ORDER_COMMIT = "63721950b3c0818e7f6892f83e9b5ee4fd0a5762"
ORDER_PATH = (
    "research/communication/github-only-exchange-enforcement-20261029/"
    "AXIOM_CURSOR_EXPERTENKODEX_V1_INTEGRATION_ORDER_R0.md"
)
ORDER_BYTES = 5176
ORDER_SHA256 = "94c6c9226d2f0ac3f1edeb9f29886b28c5ab8005ebea732c45e5178ad9ffdd32"
DEFAULT_REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"


def _manifest() -> List[Dict[str, Any]]:
    return [
        {
            "repository": DEFAULT_REPO,
            "commit": ORDER_COMMIT,
            "path": ORDER_PATH,
            "bytes": ORDER_BYTES,
            "sha256": ORDER_SHA256,
        },
        {
            "repository": DEFAULT_REPO,
            "commit": CODEX_COMMIT,
            "path": CODEX_PATH,
            "bytes": CODEX_BYTES,
            "sha256": CODEX_SHA256,
        },
    ]


def _valid_header(**overrides: Any) -> Dict[str, Any]:
    h: Dict[str, Any] = {
        "EXPERTENKODEX": CODEX_OBJECT,
        "CODEX_COMMIT": CODEX_COMMIT,
        "CODEX_PATH": CODEX_PATH,
        "CODEX_BYTES": CODEX_BYTES,
        "CODEX_SHA256": CODEX_SHA256,
        "DATA_ROUTE": "GITHUB_ONLY",
        "MANUAL_OPERATOR_ROUTE": "PURE_WORK_ORDER_TEXT_ONLY",
        "MANDATE_SOURCE_MANIFEST": _manifest(),
        "ACK_REQUIRED": True,
    }
    h.update(overrides)
    return h


class TestPositiveSourceBind(unittest.TestCase):
    def test_positive_header_pass(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(_valid_header())
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["header"]["CODEX_SHA256"], CODEX_SHA256)

    def test_positive_local_codex_bytes_match(self) -> None:
        path = ROOT / CODEX_PATH
        self.assertTrue(path.is_file(), f"missing {path}")
        raw = path.read_bytes()
        r = verify_local_codex_bytes(raw)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["bytes"], CODEX_BYTES)
        self.assertEqual(r["sha256"], CODEX_SHA256)

    def test_positive_order_bytes_match(self) -> None:
        path = ROOT / ORDER_PATH
        self.assertTrue(path.is_file(), f"missing {path}")
        raw = path.read_bytes()
        self.assertEqual(len(raw), ORDER_BYTES)
        import hashlib

        self.assertEqual(hashlib.sha256(raw).hexdigest(), ORDER_SHA256)

    def test_generator_emits_valid_header(self) -> None:
        h = build_obligatory_expert_order_header(mandate_source_manifest=_manifest())
        self.assertEqual(h["EXPERTENKODEX"], CODEX_OBJECT)
        self.assertEqual(h["MANUAL_OPERATOR_ROUTE"], "PURE_WORK_ORDER_TEXT_ONLY")
        self.assertEqual(h["DATA_ROUTE"], "GITHUB_ONLY")


class TestC01MissingExpertenkodex(unittest.TestCase):
    def test_c01_missing_expertenkodex(self) -> None:
        h = _valid_header()
        del h["EXPERTENKODEX"]
        r = ExpertenkodexHeaderValidator().validate(h)
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C01")


class TestC02WrongObject(unittest.TestCase):
    def test_c02_wrong_object(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(EXPERTENKODEX="WRONG_OBJECT")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C02")


class TestC03Commit(unittest.TestCase):
    def test_c03_short_commit(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(CODEX_COMMIT="b17d382")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C03")

    def test_c03_wrong_full_commit(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(CODEX_COMMIT="0" * 40)
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C03")


class TestC04Path(unittest.TestCase):
    def test_c04_path_mismatch(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(CODEX_PATH="docs/governance/WRONG.md")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C04")


class TestC05Bytes(unittest.TestCase):
    def test_c05_bytes_mismatch(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(_valid_header(CODEX_BYTES=1))
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C05")


class TestC06Sha256(unittest.TestCase):
    def test_c06_sha_mismatch(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(CODEX_SHA256="a" * 64)
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C06")


class TestC07DataRoute(unittest.TestCase):
    def test_c07_chat_route(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(DATA_ROUTE="CHAT_ATTACH")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C07")


class TestC08ManualRoute(unittest.TestCase):
    def test_c08_full_paste_route(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(MANUAL_OPERATOR_ROUTE="FULL_DOCUMENT_PASTE")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C08")


class TestC09AckRequired(unittest.TestCase):
    def test_c09_ack_false(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(_valid_header(ACK_REQUIRED=False))
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C09")


class TestC10Manifest(unittest.TestCase):
    def test_c10_empty_manifest(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(MANDATE_SOURCE_MANIFEST=[])
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C10")

    def test_c10_string_manifest_insufficient(self) -> None:
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(MANDATE_SOURCE_MANIFEST="a.md,b.md")
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C10")

    def test_c10_short_commit_in_entry(self) -> None:
        m = _manifest()
        m[0]["commit"] = "6372195"
        r = ExpertenkodexHeaderValidator().validate(
            _valid_header(MANDATE_SOURCE_MANIFEST=m)
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C10")


class TestC11IndependentAck(unittest.TestCase):
    def test_c11_adapter_not_connected(self) -> None:
        r = ExpertenkodexAdversarialGate().check_receiver_ack(
            adapter_connected=False,
            independent_ack=False,
            same_process_synthetic=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C11")
        self.assertEqual(r["status"], "ADAPTER_NOT_CONNECTED")

    def test_c11_synthetic_same_process(self) -> None:
        r = ExpertenkodexAdversarialGate().check_receiver_ack(
            adapter_connected=True,
            independent_ack=True,
            same_process_synthetic=True,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C11")


class TestC12DeclaredVsAuthenticated(unittest.TestCase):
    def test_c12_declared_ne_authenticated(self) -> None:
        r = ExpertenkodexAdversarialGate().check_declared_vs_authenticated(
            declared_identity="agent-grok",
            authenticated_principal="agent-cursor",
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C12")

    def test_c12_missing_authenticated(self) -> None:
        r = ExpertenkodexAdversarialGate().check_declared_vs_authenticated(
            declared_identity="agent-grok",
            authenticated_principal=None,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C12")


class TestC13ResearchBoundary(unittest.TestCase):
    def test_c13_video_as_proof(self) -> None:
        r = ExpertenkodexAdversarialGate().check_research_claims(
            ["VIDEO_AS_SCIENTIFIC_PROOF"]
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C13")

    def test_c13_optogenetics_overclaim(self) -> None:
        r = ExpertenkodexAdversarialGate().check_research_claims(
            ["OPTOGENETICS_TECHNICAL_EQUIVALENCE_PROVEN"]
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C13")

    def test_c13_secondary_reference_allowed_absence(self) -> None:
        # No prohibited token → PASS (OPERATOR_REFERENCED_SECONDARY is not a claim upgrade)
        r = ExpertenkodexAdversarialGate().check_research_claims(
            ["OPERATOR_REFERENCED_SECONDARY", "THREAT_MODEL_NOTE"]
        )
        self.assertTrue(r["ok"], r)


class TestC14CovertChannel(unittest.TestCase):
    def test_c14_cache_timing_transport(self) -> None:
        r = ExpertenkodexAdversarialGate().check_covert_channels(
            ["CACHE_TIMING_AS_TRANSPORT"]
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C14")

    def test_c14_authorized_github_only_ok(self) -> None:
        r = ExpertenkodexAdversarialGate().check_covert_channels(["GITHUB_ONLY"])
        self.assertTrue(r["ok"], r)


class TestC15CiEnforcement(unittest.TestCase):
    def test_c15_listed_not_wired(self) -> None:
        r = ExpertenkodexAdversarialGate().check_ci_enforcement(
            listed_in_docs=True,
            workflow_runs_tests=False,
            required_check_enforced=False,
            executed=False,
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C15")

    def test_c15_configured_not_executed(self) -> None:
        r = ExpertenkodexAdversarialGate().check_ci_enforcement(
            listed_in_docs=True,
            workflow_runs_tests=True,
            required_check_enforced=False,
            executed=False,
        )
        self.assertFalse(r["ok"])
        self.assertIn("CI_CONFIGURED≠EXECUTED", r.get("note", ""))

    def test_c15_executed_not_required(self) -> None:
        r = ExpertenkodexAdversarialGate().check_ci_enforcement(
            listed_in_docs=True,
            workflow_runs_tests=True,
            required_check_enforced=False,
            executed=True,
        )
        self.assertFalse(r["ok"])
        self.assertIn("EXECUTED≠REQUIRED_CHECK_ENFORCED", r.get("note", ""))


class TestC16StateMachine(unittest.TestCase):
    def test_c16_skip_transition(self) -> None:
        r = ExpertenkodexCausalMachine().validate_transition(
            "ORDER_AUTHORED", "AGENT_EXECUTED"
        )
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C16")

    def test_c16_valid_edge(self) -> None:
        r = ExpertenkodexCausalMachine().validate_transition(
            "ORDER_AUTHORED", "ORDER_PUBLISHED"
        )
        self.assertTrue(r["ok"], r)

    def test_c16_unknown_state(self) -> None:
        r = ExpertenkodexCausalMachine().validate_transition("ORDER_AUTHORED", "DONE")
        self.assertFalse(r["ok"])
        self.assertEqual(r["fixture"], "C16")


class TestCanonicalPinImmutables(unittest.TestCase):
    def test_pin_constants(self) -> None:
        self.assertEqual(CANONICAL_PIN.commit, CODEX_COMMIT)
        self.assertEqual(CANONICAL_PIN.bytes, 15388)
        self.assertEqual(
            CANONICAL_PIN.sha256,
            "adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab",
        )
        self.assertEqual(CANONICAL_PIN.path, CODEX_PATH)


if __name__ == "__main__":
    unittest.main()
