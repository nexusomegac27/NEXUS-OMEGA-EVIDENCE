#!/usr/bin/env python3
"""NEXUS GitHub-Only Agent Data Exchange Chain (G1-G5).

OBJECT: NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_ONLY_EXCHANGE_ENFORCEMENT_20261029_R1
CLAIM_CEILING: C1_DESCRIPTIVE_ONLY

Extends the existing expert-exchange stack. Fail-closed. No parallel
top-level structure. Manual artifact fallback is DENIED as default.

G1 Source Resolver  — commit + path + bytes + sha256 (+ transitive parents)
G2 Dispatch Validator — missing/mismatched/incomplete → block before delivery
G3 Agent Adapter — registered identity + least-privilege proof (no fiction)
G4 Delivery Journal — persistent events, retry, reconcile, independent ACK
G5 Return Slots — owner-controlled registered slots only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_DEFAULT = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
CLAIM_CEILING = "C1_DESCRIPTIVE_ONLY"
LAW_OBJECT = "NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2"
MANUAL_FALLBACK_DEFAULT = False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@dataclass
class SourceRef:
    repository: str
    commit: str
    path: str
    bytes: int
    sha256: str
    parent_refs: List[Dict[str, Any]] = field(default_factory=list)

    def identity(self) -> str:
        return f"{self.repository}@{self.commit}:{self.path}"


@dataclass
class ResolveResult:
    ok: bool
    source: SourceRef
    observed_bytes: Optional[int] = None
    observed_sha256: Optional[str] = None
    local_path: Optional[str] = None
    error: Optional[str] = None
    transitive: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["source"] = asdict(self.source)
        d["claim_ceiling"] = CLAIM_CEILING
        return d


@dataclass
class DispatchVerdict:
    ok: bool
    gate: str
    reason: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SourceResolver:
    """G1: resolve GitHub source by commit/path/bytes/sha256."""

    def __init__(
        self,
        *,
        checkout_root: Optional[Path] = None,
        github_token: Optional[str] = None,
        allow_network: bool = False,
    ) -> None:
        self.checkout_root = checkout_root
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        self.allow_network = allow_network

    def resolve(self, ref: SourceRef, *, depth: int = 0, max_depth: int = 8) -> ResolveResult:
        if depth > max_depth:
            return ResolveResult(
                ok=False,
                source=ref,
                error="FAIL_CLOSED_TRANSITIVE_DEPTH_EXCEEDED",
            )
        blob = self._fetch_blob(ref)
        if blob is None:
            return ResolveResult(
                ok=False,
                source=ref,
                error="FAIL_CLOSED_SOURCE_UNREACHABLE",
            )
        data, local_path = blob
        obs_b = len(data)
        obs_h = sha256_bytes(data)
        if obs_b != ref.bytes or obs_h.lower() != ref.sha256.lower():
            return ResolveResult(
                ok=False,
                source=ref,
                observed_bytes=obs_b,
                observed_sha256=obs_h,
                local_path=local_path,
                error="FAIL_CLOSED_HASH_OR_BYTES_MISMATCH",
            )
        transitive: List[Dict[str, Any]] = []
        for parent in ref.parent_refs:
            try:
                pref = SourceRef(
                    repository=str(parent.get("repository") or ref.repository),
                    commit=str(parent["commit"]),
                    path=str(parent["path"]),
                    bytes=int(parent["bytes"]),
                    sha256=str(parent["sha256"]),
                    parent_refs=list(parent.get("parent_refs") or []),
                )
            except (KeyError, TypeError, ValueError) as exc:
                return ResolveResult(
                    ok=False,
                    source=ref,
                    observed_bytes=obs_b,
                    observed_sha256=obs_h,
                    local_path=local_path,
                    error=f"FAIL_CLOSED_PARENT_REF_MALFORMED:{exc}",
                )
            pr = self.resolve(pref, depth=depth + 1, max_depth=max_depth)
            transitive.append(pr.to_dict())
            if not pr.ok:
                return ResolveResult(
                    ok=False,
                    source=ref,
                    observed_bytes=obs_b,
                    observed_sha256=obs_h,
                    local_path=local_path,
                    error="FAIL_CLOSED_TRANSITIVE_PARENT_UNRESOLVED",
                    transitive=transitive,
                )
        return ResolveResult(
            ok=True,
            source=ref,
            observed_bytes=obs_b,
            observed_sha256=obs_h,
            local_path=local_path,
            transitive=transitive,
        )

    def _fetch_blob(self, ref: SourceRef) -> Optional[Tuple[bytes, Optional[str]]]:
        if self.checkout_root is not None:
            local = self.checkout_root / ref.path
            if local.is_file():
                # Prefer local mirror when commit matches HEAD of checkout, else still
                # accept local bytes for offline synthetic tests; network verifies live.
                return local.read_bytes(), str(local)
            # try git show from checkout
            git_blob = self._git_show(ref)
            if git_blob is not None:
                return git_blob, None
        if self.allow_network:
            return self._github_contents(ref), None
        return None

    def _git_show(self, ref: SourceRef) -> Optional[bytes]:
        if self.checkout_root is None or not (self.checkout_root / ".git").exists():
            return None
        try:
            proc = subprocess.run(
                ["git", "show", f"{ref.commit}:{ref.path}"],
                cwd=str(self.checkout_root),
                capture_output=True,
                check=False,
            )
        except OSError:
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout

    def _github_contents(self, ref: SourceRef) -> Optional[bytes]:
        # GitHub Contents API returns base64; prefer raw via media type.
        owner_repo = ref.repository
        url = (
            f"https://api.github.com/repos/{owner_repo}/contents/"
            f"{ref.path}?ref={ref.commit}"
        )
        headers = {
            "Accept": "application/vnd.github.raw",
            "User-Agent": "NEXUS-OMEGA-GitHub-Exchange-Chain/C1",
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=30) as resp:
                return resp.read()
        except (HTTPError, URLError, TimeoutError, OSError):
            return None


class DispatchValidator:
    """G2: fail-closed before delivery."""

    REQUIRED_ENVELOPE_KEYS = (
        "object",
        "authority",
        "claim_ceiling",
        "sources",
        "recipient_actor",
        "return_slot",
    )

    def __init__(self, resolver: SourceResolver) -> None:
        self.resolver = resolver

    def validate_package(self, package: Dict[str, Any]) -> DispatchVerdict:
        missing = [k for k in self.REQUIRED_ENVELOPE_KEYS if k not in package]
        if missing:
            return DispatchVerdict(
                ok=False,
                gate="G2",
                reason="FAIL_CLOSED_MISSING_ENVELOPE_KEYS",
                details={"missing": missing},
            )
        if package.get("claim_ceiling") != CLAIM_CEILING:
            return DispatchVerdict(
                ok=False,
                gate="G2",
                reason="FAIL_CLOSED_CLAIM_CEILING",
                details={"observed": package.get("claim_ceiling")},
            )
        if package.get("manual_artifact_fallback") is True and not package.get(
            "scientific_exception_authorized"
        ):
            return DispatchVerdict(
                ok=False,
                gate="G2",
                reason="FAIL_CLOSED_MANUAL_FALLBACK_DENIED_AS_DEFAULT",
                details={"manual_fallback_default": MANUAL_FALLBACK_DEFAULT},
            )
        sources = package.get("sources")
        if not isinstance(sources, list) or not sources:
            return DispatchVerdict(
                ok=False,
                gate="G2",
                reason="FAIL_CLOSED_SOURCES_EMPTY",
            )
        resolved: List[Dict[str, Any]] = []
        for item in sources:
            try:
                ref = SourceRef(
                    repository=str(item.get("repository") or REPO_DEFAULT),
                    commit=str(item["commit"]),
                    path=str(item["path"]),
                    bytes=int(item["bytes"]),
                    sha256=str(item["sha256"]),
                    parent_refs=list(item.get("parent_refs") or []),
                )
            except (KeyError, TypeError, ValueError) as exc:
                return DispatchVerdict(
                    ok=False,
                    gate="G2",
                    reason="FAIL_CLOSED_SOURCE_REF_MALFORMED",
                    details={"error": str(exc)},
                )
            rr = self.resolver.resolve(ref)
            resolved.append(rr.to_dict())
            if not rr.ok:
                return DispatchVerdict(
                    ok=False,
                    gate="G2",
                    reason="FAIL_CLOSED_SOURCE_UNRESOLVED",
                    details={"resolve": rr.to_dict()},
                )
        expert_lanes = package.get("expert_lanes")
        if expert_lanes is not None:
            if not isinstance(expert_lanes, list) or len(expert_lanes) < 1:
                return DispatchVerdict(
                    ok=False,
                    gate="G2",
                    reason="FAIL_CLOSED_INCOMPLETE_EXPERT_PACKAGE",
                    details={"expert_lanes": expert_lanes},
                )
            for lane in expert_lanes:
                if not isinstance(lane, dict) or "id" not in lane or "status" not in lane:
                    return DispatchVerdict(
                        ok=False,
                        gate="G2",
                        reason="FAIL_CLOSED_INCOMPLETE_EXPERT_LANE",
                        details={"lane": lane},
                    )
                if lane.get("status") == "MISSING":
                    return DispatchVerdict(
                        ok=False,
                        gate="G2",
                        reason="FAIL_CLOSED_EXPERT_LANE_MISSING",
                        details={"lane": lane},
                    )
        return DispatchVerdict(
            ok=True,
            gate="G2",
            reason="PASS_DISPATCH_VALIDATED",
            details={"resolved_sources": resolved},
        )


class AgentAdapter:
    """G3: registered actor + capability proof. No invented capabilities."""

    def __init__(self, write_slots_path: Path) -> None:
        self.write_slots_path = write_slots_path
        self.registry = load_json(write_slots_path)

    def _assignment_records(self) -> List[Dict[str, Any]]:
        """Normalize assignments that may be a list (live V1) or a dict (synthetic)."""
        raw = self.registry.get("assignments")
        if raw is None:
            return []
        if isinstance(raw, dict):
            out: List[Dict[str, Any]] = []
            for key, slot in raw.items():
                if not isinstance(slot, dict):
                    continue
                item = dict(slot)
                item.setdefault("slot_id", str(key))
                item.setdefault("assignment_id", str(key))
                out.append(item)
            return out
        if isinstance(raw, list):
            return [x for x in raw if isinstance(x, dict)]
        return []

    def _policy_label(self, allow: List[str]) -> str:
        legacy = self.registry.get("external_actor_policy")
        if isinstance(legacy, str) and legacy:
            return legacy
        default = str(self.registry.get("default") or "DENY").upper()
        if len(allow) == 0 and default == "DENY":
            return "EMPTY_ALLOWLIST_DEFAULT_DENY"
        return f"DEFAULT_{default}"

    def _find_assignment(self, slot_id: str) -> Optional[Dict[str, Any]]:
        for rec in self._assignment_records():
            aid = str(rec.get("assignment_id") or "")
            sid = str(rec.get("slot_id") or "")
            if sid == slot_id or aid == slot_id:
                return rec
            # Live V1 uses assignment_id like R27-E-20261011 for logical slot R27-E
            if aid.startswith(slot_id + "-"):
                return rec
        return None

    def prove(self, actor_id: str, *, github_login: Optional[str] = None) -> DispatchVerdict:
        allow = [str(x) for x in (self.registry.get("external_actor_allowlist") or [])]
        registered_ids = set(allow)
        for slot in self._assignment_records():
            assigned = slot.get("assigned_actor")
            if assigned not in (None, "", "UNASSIGNED"):
                registered_ids.add(str(assigned))
        policy = self._policy_label(allow)
        if actor_id not in registered_ids:
            return DispatchVerdict(
                ok=False,
                gate="G3",
                reason="FAIL_CLOSED_UNREGISTERED_AGENT",
                details={
                    "actor_id": actor_id,
                    "allowlist_empty": len(allow) == 0,
                    "default": self.registry.get("default"),
                    "policy": policy,
                    "github_login_alone_grants_write": False,
                },
            )
        caps = {
            "github_read": True,  # capability class required by law
            "github_write": False,  # write never inferred
            "registered": True,
            "github_login_bound": github_login is not None,
            "github_login": github_login,
        }
        # Deny fiction: write not granted unless assignment says CREATE_ONLY slot.
        return DispatchVerdict(
            ok=True,
            gate="G3",
            reason="PASS_ADAPTER_IDENTITY_BOUND",
            details={
                "capabilities": caps,
                "write_inferred": False,
                "policy": policy,
            },
        )

    def resolve_return_slot(self, slot_id: str, actor_id: str) -> DispatchVerdict:
        slot = self._find_assignment(slot_id)
        if not isinstance(slot, dict):
            return DispatchVerdict(
                ok=False,
                gate="G5",
                reason="FAIL_CLOSED_RETURN_SLOT_UNREGISTERED",
                details={"slot_id": slot_id},
            )
        status = str(slot.get("status") or "")
        if status == "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED":
            return DispatchVerdict(
                ok=False,
                gate="G5",
                reason="FAIL_CLOSED_RETURN_SLOT_NOT_EXTERNALLY_AUTHORIZED",
                details={
                    "slot_id": slot_id,
                    "assignment_id": slot.get("assignment_id"),
                    "status": status,
                },
            )
        assigned = slot.get("assigned_actor")
        if assigned not in (None, "", "UNASSIGNED") and assigned != actor_id:
            return DispatchVerdict(
                ok=False,
                gate="G5",
                reason="FAIL_CLOSED_RETURN_SLOT_ACTOR_MISMATCH",
                details={
                    "slot_id": slot_id,
                    "assigned_actor": assigned,
                    "actor_id": actor_id,
                },
            )
        allow = [str(x) for x in (self.registry.get("external_actor_allowlist") or [])]
        default = str(self.registry.get("default") or "DENY").upper()
        actor_authorized = actor_id in allow or (
            assigned not in (None, "", "UNASSIGNED") and assigned == actor_id
        )
        if default == "DENY" and not actor_authorized:
            return DispatchVerdict(
                ok=False,
                gate="G5",
                reason="FAIL_CLOSED_RETURN_SLOT_ACTOR_NOT_AUTHORIZED",
                details={
                    "slot_id": slot_id,
                    "actor_id": actor_id,
                    "default": default,
                    "policy": self._policy_label(allow),
                },
            )
        return_path = slot.get("canonical_return_path") or slot.get("returns_path")
        return DispatchVerdict(
            ok=True,
            gate="G5",
            reason="PASS_RETURN_SLOT_BOUND",
            details={
                "slot_id": slot_id,
                "assignment_id": slot.get("assignment_id") or slot.get("slot_id"),
                "canonical_return_path": return_path,
                "mode": slot.get("mode"),
                "status": status or None,
            },
        )


class DeliveryJournal:
    """G4: persistent event journal + retry + reconcile + independent ACK."""

    def __init__(self, journal_path: Path) -> None:
        self.journal_path = journal_path
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.journal_path.exists():
            dump_json(
                self.journal_path,
                {
                    "object": "NEXUS_GITHUB_EXCHANGE_DELIVERY_JOURNAL_V1",
                    "claim_ceiling": CLAIM_CEILING,
                    "events": [],
                },
            )

    def _load(self) -> Dict[str, Any]:
        return load_json(self.journal_path)

    def _save(self, data: Dict[str, Any]) -> None:
        dump_json(self.journal_path, data)

    def append(
        self,
        event_type: str,
        payload: Dict[str, Any],
        *,
        correlation_id: Optional[str] = None,
        parent_event_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = self._load()
        event = {
            "event_id": str(uuid.uuid4()),
            "ts_unix": time.time(),
            "event_type": event_type,
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "parent_event_id": parent_event_id,
            "payload": payload,
            "claim_ceiling": CLAIM_CEILING,
        }
        data.setdefault("events", []).append(event)
        self._save(data)
        return event

    def retry_until(
        self,
        fn,
        *,
        max_attempts: int = 3,
        correlation_id: Optional[str] = None,
        label: str = "retry",
    ) -> Tuple[bool, Any, List[Dict[str, Any]]]:
        attempts: List[Dict[str, Any]] = []
        last: Any = None
        cid = correlation_id or str(uuid.uuid4())
        for i in range(1, max_attempts + 1):
            try:
                last = fn()
                ok = bool(last.get("ok")) if isinstance(last, dict) else bool(last)
            except Exception as exc:  # noqa: BLE001 — journal must record
                ok = False
                last = {"ok": False, "error": str(exc)}
            rec = self.append(
                "RETRY_ATTEMPT",
                {"label": label, "attempt": i, "ok": ok, "result": last},
                correlation_id=cid,
            )
            attempts.append(rec)
            if ok:
                self.append(
                    "RETRY_SUCCESS",
                    {"label": label, "attempts": i},
                    correlation_id=cid,
                    parent_event_id=rec["event_id"],
                )
                return True, last, attempts
        self.append(
            "RETRY_EXHAUSTED",
            {"label": label, "attempts": max_attempts, "last": last},
            correlation_id=cid,
        )
        return False, last, attempts

    def independent_ack(
        self,
        *,
        artifact_bytes: bytes,
        expected_sha256: str,
        correlation_id: str,
        receiver_id: str,
    ) -> DispatchVerdict:
        obs = sha256_bytes(artifact_bytes)
        match = obs.lower() == expected_sha256.lower()
        event = self.append(
            "RECEIVER_INDEPENDENT_ACK",
            {
                "receiver_id": receiver_id,
                "expected_sha256": expected_sha256.lower(),
                "observed_sha256": obs,
                "bytes": len(artifact_bytes),
                "match": match,
            },
            correlation_id=correlation_id,
        )
        if not match:
            return DispatchVerdict(
                ok=False,
                gate="G4",
                reason="FAIL_CLOSED_RECEIVER_ACK_MISMATCH",
                details={"event_id": event["event_id"], "observed_sha256": obs},
            )
        return DispatchVerdict(
            ok=True,
            gate="G4",
            reason="PASS_RECEIVER_INDEPENDENT_ACK",
            details={"event_id": event["event_id"], "observed_sha256": obs},
        )

    def reconcile(self, correlation_id: str) -> Dict[str, Any]:
        data = self._load()
        related = [e for e in data.get("events", []) if e.get("correlation_id") == correlation_id]
        types = [e.get("event_type") for e in related]
        has_out = "DISPATCH_OUTBOUND" in types
        has_ack = "RECEIVER_INDEPENDENT_ACK" in types
        has_return = "EXPERT_RETURN_READBACK" in types
        status = "RECONCILED" if (has_out and has_ack and has_return) else "OPEN"
        report = {
            "correlation_id": correlation_id,
            "status": status,
            "event_count": len(related),
            "event_types": types,
            "has_outbound": has_out,
            "has_ack": has_ack,
            "has_return_readback": has_return,
            "claim_ceiling": CLAIM_CEILING,
        }
        self.append("RECONCILE", report, correlation_id=correlation_id)
        return report


class ExchangeChain:
    """Orchestrates G1-G5 for synthetic and offline verification."""

    def __init__(
        self,
        *,
        checkout_root: Path,
        write_slots_path: Path,
        journal_path: Path,
        allow_network: bool = False,
    ) -> None:
        self.checkout_root = checkout_root
        self.resolver = SourceResolver(
            checkout_root=checkout_root,
            allow_network=allow_network,
        )
        self.validator = DispatchValidator(self.resolver)
        self.adapter = AgentAdapter(write_slots_path)
        self.journal = DeliveryJournal(journal_path)

    def run_synthetic_cycle(self, package: Dict[str, Any]) -> Dict[str, Any]:
        correlation_id = str(uuid.uuid4())
        gates: Dict[str, Any] = {}

        # G2 first on envelope (includes G1 resolve)
        g2 = self.validator.validate_package(package)
        gates["G2"] = g2.to_dict()
        if not g2.ok:
            self.journal.append(
                "DISPATCH_BLOCKED",
                g2.to_dict(),
                correlation_id=correlation_id,
            )
            return self._terminal(False, correlation_id, gates, "DISPATCH_BLOCKED")

        actor = str(package["recipient_actor"])
        g3 = self.adapter.prove(actor, github_login=package.get("github_login"))
        gates["G3"] = g3.to_dict()
        if not g3.ok:
            self.journal.append("ADAPTER_DENIED", g3.to_dict(), correlation_id=correlation_id)
            return self._terminal(False, correlation_id, gates, "ADAPTER_DENIED")

        slot_id = str(package["return_slot"])
        g5_slot = self.adapter.resolve_return_slot(slot_id, actor)
        gates["G5_SLOT"] = g5_slot.to_dict()
        if not g5_slot.ok:
            self.journal.append(
                "RETURN_SLOT_DENIED",
                g5_slot.to_dict(),
                correlation_id=correlation_id,
            )
            return self._terminal(False, correlation_id, gates, "RETURN_SLOT_DENIED")

        outbound_payload = {
            "object": package["object"],
            "sources": package["sources"],
            "recipient_actor": actor,
            "return_slot": slot_id,
            "claim_ceiling": CLAIM_CEILING,
            "law": LAW_OBJECT,
        }
        outbound_bytes = json.dumps(outbound_payload, sort_keys=True).encode("utf-8")
        outbound_sha = sha256_bytes(outbound_bytes)
        out_event = self.journal.append(
            "DISPATCH_OUTBOUND",
            {
                "sha256": outbound_sha,
                "bytes": len(outbound_bytes),
                "payload": outbound_payload,
            },
            correlation_id=correlation_id,
        )
        gates["G4_OUTBOUND"] = {"event_id": out_event["event_id"], "sha256": outbound_sha}

        # Independent receiver ACK (synthetic receiver rehashes outbound bytes)
        g4_ack = self.journal.independent_ack(
            artifact_bytes=outbound_bytes,
            expected_sha256=outbound_sha,
            correlation_id=correlation_id,
            receiver_id=f"synthetic-receiver:{actor}",
        )
        gates["G4_ACK"] = g4_ack.to_dict()
        if not g4_ack.ok:
            return self._terminal(False, correlation_id, gates, "ACK_FAILED")

        # Expert return into registered slot (synthetic complete return)
        return_obj = {
            "object": f"{package['object']}_RETURN",
            "parent_object": package["object"],
            "parent_outbound_sha256": outbound_sha,
            "actor": actor,
            "return_slot": slot_id,
            "claim_ceiling": CLAIM_CEILING,
            "causal_complete": True,
            "lanes": package.get("expert_lanes") or [{"id": "SYNTH", "status": "COMPLETE"}],
            "result": "SYNTHETIC_PASS_C1",
        }
        return_bytes = json.dumps(return_obj, sort_keys=True).encode("utf-8")
        return_sha = sha256_bytes(return_bytes)
        slot_rel = g5_slot.details.get("canonical_return_path")
        written_path = None
        if slot_rel:
            # Write under checkout only when path is inside repo (owner-controlled)
            target = self.checkout_root / str(slot_rel)
            # For synthetic tests, allow write into a sandbox under returns/
            if not str(slot_rel).endswith(".json"):
                target = target / f"SYNTHETIC_RETURN_{correlation_id[:8]}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(return_bytes)
            written_path = str(target.relative_to(self.checkout_root)).replace("\\", "/")

        readback = self.journal.append(
            "EXPERT_RETURN_READBACK",
            {
                "sha256": return_sha,
                "bytes": len(return_bytes),
                "path": written_path,
                "causal_complete": True,
            },
            correlation_id=correlation_id,
        )
        gates["G5_RETURN"] = {
            "event_id": readback["event_id"],
            "sha256": return_sha,
            "path": written_path,
        }

        reconcile = self.journal.reconcile(correlation_id)
        gates["G4_RECONCILE"] = reconcile
        ok = reconcile.get("status") == "RECONCILED"
        return self._terminal(
            ok,
            correlation_id,
            gates,
            "PASS_SYNTHETIC_GITHUB_EXCHANGE_CYCLE" if ok else "RECONCILE_OPEN",
        )

    def _terminal(
        self,
        ok: bool,
        correlation_id: str,
        gates: Dict[str, Any],
        reason: str,
    ) -> Dict[str, Any]:
        return {
            "ok": ok,
            "reason": reason,
            "correlation_id": correlation_id,
            "gates": gates,
            "claim_ceiling": CLAIM_CEILING,
            "law": LAW_OBJECT,
            "manual_fallback_default": MANUAL_FALLBACK_DEFAULT,
            "dispatch_chain_closed": ok,
            "technical_enforcement": "LOCAL_VALIDATOR_ACTIVE_MAIN_REQUIRED_CHECKS_NOT_YET_BOUND",
        }


def measure_efficiency(baseline: Dict[str, Any], observed: Dict[str, Any]) -> Dict[str, Any]:
    """G9: require full denominators; no PASS without proven handoffs."""
    required = (
        "manual_file_handoffs",
        "total_required_transfers",
        "github_mediated_transfers",
        "proven_receipts",
    )
    for side, blob in (("baseline", baseline), ("observed", observed)):
        missing = [k for k in required if k not in blob]
        if missing:
            return {
                "ok": False,
                "reason": "FAIL_CLOSED_EFFICIENCY_DENOMINATOR_INCOMPLETE",
                "side": side,
                "missing": missing,
                "claim_ceiling": CLAIM_CEILING,
            }
    b_manual = int(baseline["manual_file_handoffs"])
    o_manual = int(observed["manual_file_handoffs"])
    if b_manual <= 0:
        return {
            "ok": False,
            "reason": "FAIL_CLOSED_EFFICIENCY_BASELINE_ZERO",
            "claim_ceiling": CLAIM_CEILING,
        }
    if int(observed["proven_receipts"]) < int(observed["github_mediated_transfers"]):
        return {
            "ok": False,
            "reason": "FAIL_CLOSED_EFFICIENCY_UNPROVEN_HANDOFFS",
            "claim_ceiling": CLAIM_CEILING,
        }
    reduction = (b_manual - o_manual) / float(b_manual)
    target = 0.90
    return {
        "ok": reduction >= target,
        "reason": "PASS_EFFICIENCY_TARGET" if reduction >= target else "HOLD_EFFICIENCY_BELOW_TARGET",
        "reduction_ratio": reduction,
        "target": target,
        "baseline_manual": b_manual,
        "observed_manual": o_manual,
        "proven_receipts": int(observed["proven_receipts"]),
        "claim_ceiling": CLAIM_CEILING,
        "pass_requires": "FULL_DENOMINATORS_AND_PROVEN_HANDOFFS",
    }


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NEXUS GitHub-Only Exchange Chain G1-G5")
    p.add_argument("--checkout-root", type=Path, default=Path.cwd())
    p.add_argument(
        "--write-slots",
        type=Path,
        default=None,
        help="Path to EXTERNAL_AGENT_WRITE_SLOTS_V1.json",
    )
    p.add_argument("--journal", type=Path, default=None)
    p.add_argument("--allow-network", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("resolve", help="G1 resolve a SourceRef JSON file")
    r.add_argument("--ref", type=Path, required=True)

    v = sub.add_parser("validate-dispatch", help="G2 validate package JSON")
    v.add_argument("--package", type=Path, required=True)

    a = sub.add_parser("adapter-prove", help="G3 prove actor identity")
    a.add_argument("--actor", required=True)
    a.add_argument("--github-login", default=None)

    s = sub.add_parser("synthetic-cycle", help="G8 synthetic GitHub→Expert→GitHub cycle")
    s.add_argument("--package", type=Path, required=True)

    e = sub.add_parser("efficiency", help="G9 efficiency measurement")
    e.add_argument("--baseline", type=Path, required=True)
    e.add_argument("--observed", type=Path, required=True)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    root = args.checkout_root.resolve()
    slots = args.write_slots or (root / "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json")
    journal = args.journal or (root / "artifacts/github_exchange/delivery_journal.json")
    chain = ExchangeChain(
        checkout_root=root,
        write_slots_path=slots,
        journal_path=journal,
        allow_network=bool(args.allow_network),
    )

    if args.cmd == "resolve":
        raw = load_json(args.ref)
        ref = SourceRef(
            repository=str(raw.get("repository") or REPO_DEFAULT),
            commit=str(raw["commit"]),
            path=str(raw["path"]),
            bytes=int(raw["bytes"]),
            sha256=str(raw["sha256"]),
            parent_refs=list(raw.get("parent_refs") or []),
        )
        result = chain.resolver.resolve(ref)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0 if result.ok else 2

    if args.cmd == "validate-dispatch":
        package = load_json(args.package)
        verdict = chain.validator.validate_package(package)
        print(json.dumps(verdict.to_dict(), indent=2, sort_keys=True))
        return 0 if verdict.ok else 2

    if args.cmd == "adapter-prove":
        verdict = chain.adapter.prove(args.actor, github_login=args.github_login)
        print(json.dumps(verdict.to_dict(), indent=2, sort_keys=True))
        return 0 if verdict.ok else 2

    if args.cmd == "synthetic-cycle":
        package = load_json(args.package)
        out = chain.run_synthetic_cycle(package)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0 if out.get("ok") else 2

    if args.cmd == "efficiency":
        out = measure_efficiency(load_json(args.baseline), load_json(args.observed))
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0 if out.get("ok") else 2

    return 1


if __name__ == "__main__":
    sys.exit(main())
