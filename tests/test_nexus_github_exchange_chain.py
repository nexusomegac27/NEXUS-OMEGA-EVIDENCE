#!/usr/bin/env python3
"""Offline unit + synthetic tests for GitHub-Only Exchange Chain (G1-G5/G8/G9)."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.nexus_github_exchange_chain import (
    CLAIM_CEILING,
    AgentAdapter,
    DeliveryJournal,
    DispatchValidator,
    ExchangeChain,
    SourceRef,
    SourceResolver,
    measure_efficiency,
    sha256_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/governance/NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2.md"
HANDOFF = ROOT / "docs/AI_HANDOFF_PROTOCOL.md"
WRITE_SLOTS = ROOT / "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json"
PINNED_COMMIT = "0b1f88d8f359e9fd2e50a909b07f0fbd155e11f4"


def _policy_ref() -> SourceRef:
    b = POLICY.read_bytes()
    return SourceRef(
        repository="nexusomegac27/NEXUS-OMEGA-EVIDENCE",
        commit=PINNED_COMMIT,
        path="docs/governance/NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2.md",
        bytes=len(b),
        sha256=sha256_bytes(b),
    )


def _handoff_ref() -> SourceRef:
    b = HANDOFF.read_bytes()
    return SourceRef(
        repository="nexusomegac27/NEXUS-OMEGA-EVIDENCE",
        commit=PINNED_COMMIT,
        path="docs/AI_HANDOFF_PROTOCOL.md",
        bytes=len(b),
        sha256=sha256_bytes(b),
    )


class TestG1SourceResolver(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = SourceResolver(checkout_root=ROOT, allow_network=False)

    def test_resolve_policy_match(self) -> None:
        rr = self.resolver.resolve(_policy_ref())
        self.assertTrue(rr.ok, rr.error)
        self.assertEqual(rr.observed_bytes, 9203)
        self.assertEqual(
            rr.observed_sha256,
            "ad471285d3b3b2f24cb5b832b749498fc11dca486957ddd5478a1ed3b91d6fcc",
        )

    def test_resolve_handoff_match(self) -> None:
        rr = self.resolver.resolve(_handoff_ref())
        self.assertTrue(rr.ok, rr.error)
        self.assertEqual(rr.observed_bytes, 8505)
        self.assertEqual(
            rr.observed_sha256,
            "66558be74b297eeef0849de5eaa7716f67f9ce4dd64f917bd94f0e30bf2c0aaf",
        )

    def test_fail_closed_hash_mismatch(self) -> None:
        ref = _policy_ref()
        ref.sha256 = "0" * 64
        rr = self.resolver.resolve(ref)
        self.assertFalse(rr.ok)
        self.assertEqual(rr.error, "FAIL_CLOSED_HASH_OR_BYTES_MISMATCH")

    def test_transitive_parent(self) -> None:
        child = _policy_ref()
        child.parent_refs = [
            {
                "repository": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
                "commit": PINNED_COMMIT,
                "path": "docs/AI_HANDOFF_PROTOCOL.md",
                "bytes": 8505,
                "sha256": "66558be74b297eeef0849de5eaa7716f67f9ce4dd64f917bd94f0e30bf2c0aaf",
            }
        ]
        rr = self.resolver.resolve(child)
        self.assertTrue(rr.ok, rr.error)
        self.assertEqual(len(rr.transitive), 1)
        self.assertTrue(rr.transitive[0]["ok"])

    def test_transitive_parent_unreachable(self) -> None:
        child = _policy_ref()
        child.parent_refs = [
            {
                "repository": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
                "commit": PINNED_COMMIT,
                "path": "docs/governance/DOES_NOT_EXIST.md",
                "bytes": 1,
                "sha256": "0" * 64,
            }
        ]
        rr = self.resolver.resolve(child)
        self.assertFalse(rr.ok)
        self.assertEqual(rr.error, "FAIL_CLOSED_TRANSITIVE_PARENT_UNRESOLVED")


class TestG2DispatchValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = DispatchValidator(
            SourceResolver(checkout_root=ROOT, allow_network=False)
        )

    def _ok_package(self) -> dict:
        pref = _policy_ref()
        return {
            "object": "NEXUS_SYNTHETIC_DISPATCH_PACKAGE_R1",
            "authority": "OPERATOR_ALEXANDER_VIA_AXIOM",
            "claim_ceiling": CLAIM_CEILING,
            "recipient_actor": "agt-SYNTHETIC-EXCHANGE-R1",
            "return_slot": "R27-E",
            "sources": [
                {
                    "repository": pref.repository,
                    "commit": pref.commit,
                    "path": pref.path,
                    "bytes": pref.bytes,
                    "sha256": pref.sha256,
                }
            ],
            "expert_lanes": [{"id": "E01", "status": "COMPLETE"}],
        }

    def test_pass_complete_package(self) -> None:
        v = self.validator.validate_package(self._ok_package())
        self.assertTrue(v.ok, v.reason)

    def test_fail_missing_keys(self) -> None:
        pkg = self._ok_package()
        del pkg["sources"]
        v = self.validator.validate_package(pkg)
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_MISSING_ENVELOPE_KEYS")

    def test_fail_manual_fallback_default(self) -> None:
        pkg = self._ok_package()
        pkg["manual_artifact_fallback"] = True
        v = self.validator.validate_package(pkg)
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_MANUAL_FALLBACK_DENIED_AS_DEFAULT")

    def test_fail_missing_expert_lane(self) -> None:
        pkg = self._ok_package()
        pkg["expert_lanes"] = [{"id": "E01", "status": "MISSING"}]
        v = self.validator.validate_package(pkg)
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_EXPERT_LANE_MISSING")

    def test_fail_hash_mismatch_in_source(self) -> None:
        pkg = self._ok_package()
        pkg["sources"][0]["sha256"] = "1" * 64
        v = self.validator.validate_package(pkg)
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_SOURCE_UNRESOLVED")


class TestG3Adapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = AgentAdapter(WRITE_SLOTS)

    def test_unregistered_denied(self) -> None:
        v = self.adapter.prove("agt-NOT-REGISTERED")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_UNREGISTERED_AGENT")

    def test_empty_allowlist_default_deny(self) -> None:
        reg = json.loads(WRITE_SLOTS.read_text(encoding="utf-8"))
        self.assertEqual(reg.get("external_actor_allowlist"), [])
        self.assertEqual(reg.get("default"), "DENY")
        self.assertIsInstance(reg.get("assignments"), list)
        v = self.adapter.prove("agt-SYNTHETIC-EXCHANGE-R1")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_UNREGISTERED_AGENT")
        self.assertEqual(v.details.get("policy"), "EMPTY_ALLOWLIST_DEFAULT_DENY")
        self.assertTrue(v.details.get("allowlist_empty"))

    def test_allowlisted_actor_passes_on_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slots.json"
            path.write_text(
                json.dumps(
                    {
                        "default": "DENY",
                        "external_actor_allowlist": ["agt-SYNTHETIC-EXCHANGE-R1"],
                        "assignments": {
                            "R27-E": {
                                "assigned_actor": "agt-SYNTHETIC-EXCHANGE-R1",
                                "canonical_return_path": "research/r27/returns",
                                "mode": "CREATE_ONLY_EXACT_REGISTERED_FILE",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            adapter = AgentAdapter(path)
            v = adapter.prove("agt-SYNTHETIC-EXCHANGE-R1", github_login="synthetic-test-only")
            self.assertTrue(v.ok, v.reason)
            self.assertFalse(v.details["capabilities"]["github_write"])


class TestG4Journal(unittest.TestCase):
    def test_ack_and_reconcile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            journal = DeliveryJournal(Path(tmp) / "journal.json")
            cid = "corr-test-1"
            payload = b'{"hello":"nexus"}'
            h = sha256_bytes(payload)
            journal.append(
                "DISPATCH_OUTBOUND",
                {"sha256": h, "bytes": len(payload)},
                correlation_id=cid,
            )
            ack = journal.independent_ack(
                artifact_bytes=payload,
                expected_sha256=h,
                correlation_id=cid,
                receiver_id="synthetic",
            )
            self.assertTrue(ack.ok)
            journal.append(
                "EXPERT_RETURN_READBACK",
                {"sha256": h, "bytes": len(payload)},
                correlation_id=cid,
            )
            rec = journal.reconcile(cid)
            self.assertEqual(rec["status"], "RECONCILED")

    def test_ack_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            journal = DeliveryJournal(Path(tmp) / "journal.json")
            ack = journal.independent_ack(
                artifact_bytes=b"abc",
                expected_sha256="0" * 64,
                correlation_id="c2",
                receiver_id="synthetic",
            )
            self.assertFalse(ack.ok)


class TestG5ReturnSlot(unittest.TestCase):
    def test_unregistered_slot(self) -> None:
        adapter = AgentAdapter(WRITE_SLOTS)
        v = adapter.resolve_return_slot("DOES-NOT-EXIST", "agt-X")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_RETURN_SLOT_UNREGISTERED")

    def test_live_r27e_preallocated_not_authorized(self) -> None:
        """Live WRITE_SLOTS: R27-E exists as PREALLOCATED — external write DENY."""
        adapter = AgentAdapter(WRITE_SLOTS)
        v = adapter.resolve_return_slot("R27-E", "agt-SYNTHETIC-EXCHANGE-R1")
        self.assertFalse(v.ok)
        self.assertEqual(v.reason, "FAIL_CLOSED_RETURN_SLOT_NOT_EXTERNALLY_AUTHORIZED")
        self.assertEqual(v.details.get("assignment_id"), "R27-E-20261011")

    def test_authorized_fixture_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slots.json"
            path.write_text(
                json.dumps(
                    {
                        "default": "DENY",
                        "external_actor_allowlist": ["agt-SYNTHETIC-EXCHANGE-R1"],
                        "assignments": {
                            "R27-E": {
                                "assigned_actor": "agt-SYNTHETIC-EXCHANGE-R1",
                                "canonical_return_path": "research/r27/returns",
                                "mode": "CREATE_ONLY_EXACT_REGISTERED_FILE",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            adapter = AgentAdapter(path)
            v = adapter.resolve_return_slot("R27-E", "agt-SYNTHETIC-EXCHANGE-R1")
            self.assertTrue(v.ok, v.reason)
            self.assertEqual(
                v.details.get("canonical_return_path"), "research/r27/returns"
            )


class TestG8SyntheticCycle(unittest.TestCase):
    def test_full_cycle_with_fixture_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Sandbox checkout containing pinned policy + handoff copies
            checkout = tmp_path / "checkout"
            (checkout / "docs/governance").mkdir(parents=True)
            (checkout / "docs").mkdir(parents=True, exist_ok=True)
            shutil.copy2(POLICY, checkout / "docs/governance/NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2.md")
            shutil.copy2(HANDOFF, checkout / "docs/AI_HANDOFF_PROTOCOL.md")
            (checkout / "research/r27/www-extern-wake-isolation-20261011/returns").mkdir(
                parents=True
            )

            slots = {
                "schema_version": "1.0.0-r27e",
                "external_actor_policy": "TEST_ALLOWLIST_SYNTHETIC_ONLY",
                "external_actor_allowlist": ["agt-SYNTHETIC-EXCHANGE-R1"],
                "assignments": {
                    "R27-E": {
                        "slot_id": "R27-E",
                        "canonical_return_path": "research/r27/www-extern-wake-isolation-20261011/returns",
                        "mode": "CREATE_ONLY_EXACT_REGISTERED_FILE",
                        "assigned_actor": "agt-SYNTHETIC-EXCHANGE-R1",
                    }
                },
            }
            slots_path = checkout / "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json"
            slots_path.write_text(json.dumps(slots, indent=2), encoding="utf-8")

            pref = _policy_ref()
            package = {
                "object": "NEXUS_SYNTHETIC_GITHUB_EXCHANGE_CYCLE_R1",
                "authority": "OPERATOR_ALEXANDER_VIA_AXIOM",
                "claim_ceiling": CLAIM_CEILING,
                "recipient_actor": "agt-SYNTHETIC-EXCHANGE-R1",
                "github_login": "synthetic-test-only",
                "return_slot": "R27-E",
                "sources": [
                    {
                        "repository": pref.repository,
                        "commit": pref.commit,
                        "path": pref.path,
                        "bytes": pref.bytes,
                        "sha256": pref.sha256,
                        "parent_refs": [
                            {
                                "repository": pref.repository,
                                "commit": PINNED_COMMIT,
                                "path": "docs/AI_HANDOFF_PROTOCOL.md",
                                "bytes": 8505,
                                "sha256": "66558be74b297eeef0849de5eaa7716f67f9ce4dd64f917bd94f0e30bf2c0aaf",
                            }
                        ],
                    }
                ],
                "expert_lanes": [{"id": f"E{i:02d}", "status": "COMPLETE"} for i in range(1, 11)],
            }
            chain = ExchangeChain(
                checkout_root=checkout,
                write_slots_path=slots_path,
                journal_path=tmp_path / "journal.json",
                allow_network=False,
            )
            out = chain.run_synthetic_cycle(package)
            self.assertTrue(out["ok"], out)
            self.assertTrue(out["dispatch_chain_closed"])
            self.assertEqual(out["gates"]["G4_RECONCILE"]["status"], "RECONCILED")


class TestG9Efficiency(unittest.TestCase):
    def test_incomplete_denominator(self) -> None:
        out = measure_efficiency({"manual_file_handoffs": 10}, {"manual_file_handoffs": 1})
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "FAIL_CLOSED_EFFICIENCY_DENOMINATOR_INCOMPLETE")

    def test_target_pass(self) -> None:
        baseline = {
            "manual_file_handoffs": 100,
            "total_required_transfers": 100,
            "github_mediated_transfers": 0,
            "proven_receipts": 0,
        }
        observed = {
            "manual_file_handoffs": 5,
            "total_required_transfers": 100,
            "github_mediated_transfers": 95,
            "proven_receipts": 95,
        }
        out = measure_efficiency(baseline, observed)
        self.assertTrue(out["ok"])
        self.assertGreaterEqual(out["reduction_ratio"], 0.90)

    def test_unproven_handoffs(self) -> None:
        baseline = {
            "manual_file_handoffs": 100,
            "total_required_transfers": 100,
            "github_mediated_transfers": 0,
            "proven_receipts": 0,
        }
        observed = {
            "manual_file_handoffs": 5,
            "total_required_transfers": 100,
            "github_mediated_transfers": 95,
            "proven_receipts": 10,
        }
        out = measure_efficiency(baseline, observed)
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "FAIL_CLOSED_EFFICIENCY_UNPROVEN_HANDOFFS")


if __name__ == "__main__":
    unittest.main()
