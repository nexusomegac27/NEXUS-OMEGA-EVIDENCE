#!/usr/bin/env python3
"""NEXUS Expertenkodex V1 — obligatory header + C01–C16 negative fixture gate.

OBJECT: NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CODEX_COMMIT = b17d38266777bad61178e608d09e41726b9f4769
CODEX_SHA256 = adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab
DATA_ROUTE = GITHUB_ONLY
MANUAL_OPERATOR_ROUTE = PURE_WORK_ORDER_TEXT_ONLY
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

DEFAULT_REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
CODEX_OBJECT = "NEXUS_OMEGA_AXIOM_EXPERTENKODEX_GITHUB_COMMUNICATION_20261029_V1"
CODEX_COMMIT = "b17d38266777bad61178e608d09e41726b9f4769"
CODEX_PATH = "docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md"
CODEX_BYTES = 15388
CODEX_SHA256 = "adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab"

REQUIRED_HEADER_KEYS: Tuple[str, ...] = (
    "EXPERTENKODEX",
    "CODEX_COMMIT",
    "CODEX_PATH",
    "CODEX_BYTES",
    "CODEX_SHA256",
    "DATA_ROUTE",
    "MANUAL_OPERATOR_ROUTE",
    "MANDATE_SOURCE_MANIFEST",
    "ACK_REQUIRED",
)

VALID_SM_STATES: Set[str] = {
    "ORDER_AUTHORED",
    "ORDER_PUBLISHED",
    "ORDER_BOUND",
    "AGENT_DISPATCHED",
    "AGENT_RECEIVED",
    "AGENT_EXECUTED",
    "AGENT_RETURNED",
    "RECEIVER_ACKED",
    "CURSOR_REHASHED",
    "AXIOM_ADJUDICATED",
    "OPERATOR_NEXT_DECISION",
}

SM_EDGES: Set[Tuple[str, str]] = {
    ("ORDER_AUTHORED", "ORDER_PUBLISHED"),
    ("ORDER_PUBLISHED", "ORDER_BOUND"),
    ("ORDER_BOUND", "AGENT_DISPATCHED"),
    ("AGENT_DISPATCHED", "AGENT_RECEIVED"),
    ("AGENT_RECEIVED", "AGENT_EXECUTED"),
    ("AGENT_EXECUTED", "AGENT_RETURNED"),
    ("AGENT_RETURNED", "RECEIVER_ACKED"),
    ("RECEIVER_ACKED", "CURSOR_REHASHED"),
    ("CURSOR_REHASHED", "AXIOM_ADJUDICATED"),
    ("AXIOM_ADJUDICATED", "OPERATOR_NEXT_DECISION"),
}

PROHIBITED_COVERT_CHANNEL_TOKENS: Tuple[str, ...] = (
    "CACHE_TIMING_AS_TRANSPORT",
    "SIDE_CHANNEL_AS_TRANSPORT",
    "COVERT_CHANNEL_AS_DATA_ROUTE",
    "TIMING_CHANNEL_AS_ACK",
)

PROHIBITED_BIOLOGY_CLAIM_TOKENS: Tuple[str, ...] = (
    "OPTOGENETICS_EQUALS_NEXUS_TRIGGER",
    "BIOLOGY_PROVES_TECHNICAL_EQUIVALENCE",
    "VIDEO_AS_SCIENTIFIC_PROOF",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(code: str, detail: str = "", **extra: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": False, "code": code, "ts": utc_now()}
    if detail:
        out["detail"] = detail
    out.update(extra)
    return out


def ok(**kwargs: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": True, "ts": utc_now()}
    out.update(kwargs)
    return out


def _norm_header(raw: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k).strip().upper(): v for k, v in raw.items()}


def _as_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


@dataclass(frozen=True)
class CodexPin:
    object_id: str = CODEX_OBJECT
    commit: str = CODEX_COMMIT
    path: str = CODEX_PATH
    bytes: int = CODEX_BYTES
    sha256: str = CODEX_SHA256

    def as_dict(self) -> Dict[str, Any]:
        return {
            "EXPERTENKODEX": self.object_id,
            "CODEX_COMMIT": self.commit,
            "CODEX_PATH": self.path,
            "CODEX_BYTES": self.bytes,
            "CODEX_SHA256": self.sha256,
            "DATA_ROUTE": "GITHUB_ONLY",
            "MANUAL_OPERATOR_ROUTE": "PURE_WORK_ORDER_TEXT_ONLY",
        }


CANONICAL_PIN = CodexPin()


class ExpertenkodexHeaderValidator:
    """Obligatory EXPERTENKODEX header gate for future expert orders (K1)."""

    REQUIRED_KEYS = REQUIRED_HEADER_KEYS

    def validate(
        self,
        header: Mapping[str, Any],
        *,
        pin: CodexPin = CANONICAL_PIN,
        require_manifest_entries: bool = True,
    ) -> Dict[str, Any]:
        h = _norm_header(header)
        missing = [k for k in self.REQUIRED_KEYS if k not in h or h[k] in ("", None)]
        if missing:
            return fail(
                "C01_MISSING_EXPERTENKODEX_OR_REQUIRED_FIELD",
                f"missing={','.join(missing)}",
                fixture="C01",
            )

        expertenkodex = _as_str(h.get("EXPERTENKODEX"))
        if expertenkodex != pin.object_id:
            return fail(
                "C02_WRONG_EXPERTENKODEX_OBJECT",
                f"got={expertenkodex}",
                fixture="C02",
            )

        commit = _as_str(h.get("CODEX_COMMIT")).lower()
        if not FULL_SHA_RE.match(commit):
            return fail(
                "C03_SHORT_OR_INVALID_CODEX_COMMIT",
                f"got={commit}",
                fixture="C03",
            )
        if commit != pin.commit:
            return fail(
                "C03_CODEX_COMMIT_MISMATCH",
                f"got={commit} expected={pin.commit}",
                fixture="C03",
            )

        path = _as_str(h.get("CODEX_PATH")).replace("\\", "/")
        if path != pin.path:
            return fail(
                "C04_CODEX_PATH_MISMATCH",
                f"got={path}",
                fixture="C04",
            )

        nbytes = _as_int(h.get("CODEX_BYTES"))
        if nbytes is None:
            return fail("C05_CODEX_BYTES_INVALID", fixture="C05")
        if nbytes != pin.bytes:
            return fail(
                "C05_CODEX_BYTES_MISMATCH",
                f"got={nbytes} expected={pin.bytes}",
                fixture="C05",
            )

        digest = _as_str(h.get("CODEX_SHA256")).lower()
        if not HEX64_RE.match(digest):
            return fail("C06_CODEX_SHA256_INVALID", fixture="C06")
        if digest != pin.sha256:
            return fail(
                "C06_CODEX_SHA256_MISMATCH",
                f"got={digest}",
                fixture="C06",
            )

        data_route = _as_str(h.get("DATA_ROUTE")).upper()
        if data_route != "GITHUB_ONLY":
            return fail(
                "C07_DATA_ROUTE_NOT_GITHUB_ONLY",
                f"got={data_route}",
                fixture="C07",
            )

        manual_route = _as_str(h.get("MANUAL_OPERATOR_ROUTE")).upper()
        if manual_route != "PURE_WORK_ORDER_TEXT_ONLY":
            return fail(
                "C08_MANUAL_OPERATOR_ROUTE_INVALID",
                f"got={manual_route}",
                fixture="C08",
            )

        ack_required = h.get("ACK_REQUIRED")
        if isinstance(ack_required, str):
            ack_ok = ack_required.strip().upper() in {"YES", "TRUE", "1", "REQUIRED"}
        else:
            ack_ok = bool(ack_required)
        if not ack_ok:
            return fail("C09_ACK_REQUIRED_FALSE", fixture="C09")

        manifest = h.get("MANDATE_SOURCE_MANIFEST")
        if require_manifest_entries:
            entries = self._normalize_manifest(manifest)
            if entries is None:
                return fail(
                    "C10_MANDATE_SOURCE_MANIFEST_INVALID",
                    "manifest must be non-empty list of {repository,commit,path,bytes,sha256}",
                    fixture="C10",
                )
            for i, entry in enumerate(entries):
                v = self._validate_manifest_entry(entry, index=i)
                if not v["ok"]:
                    return v
        else:
            entries = []

        return ok(
            header={
                "EXPERTENKODEX": expertenkodex,
                "CODEX_COMMIT": commit,
                "CODEX_PATH": path,
                "CODEX_BYTES": nbytes,
                "CODEX_SHA256": digest,
                "DATA_ROUTE": data_route,
                "MANUAL_OPERATOR_ROUTE": manual_route,
                "ACK_REQUIRED": True,
                "MANDATE_SOURCE_MANIFEST_COUNT": len(entries),
            },
            pin=pin.as_dict(),
            gate="CODEX_HEADER_VALIDATOR",
        )

    def _normalize_manifest(self, manifest: Any) -> Optional[List[Dict[str, Any]]]:
        if isinstance(manifest, str):
            # Allow comma-separated path list only as structural presence; entries still required.
            parts = [p.strip() for p in manifest.split(",") if p.strip()]
            if not parts:
                return None
            return None  # strings alone are insufficient — need structured entries
        if not isinstance(manifest, list) or not manifest:
            return None
        out: List[Dict[str, Any]] = []
        for item in manifest:
            if not isinstance(item, Mapping):
                return None
            out.append(dict(item))
        return out

    def _validate_manifest_entry(
        self, entry: Mapping[str, Any], *, index: int
    ) -> Dict[str, Any]:
        repo = _as_str(entry.get("repository") or entry.get("REPOSITORY"))
        commit = _as_str(entry.get("commit") or entry.get("COMMIT")).lower()
        path = _as_str(entry.get("path") or entry.get("PATH")).replace("\\", "/")
        nbytes = _as_int(entry.get("bytes") or entry.get("BYTES"))
        digest = _as_str(entry.get("sha256") or entry.get("SHA256")).lower()
        if not REPO_RE.match(repo):
            return fail(
                "C10_MANIFEST_REPOSITORY_INVALID",
                f"index={index}",
                fixture="C10",
            )
        if not FULL_SHA_RE.match(commit):
            return fail(
                "C10_MANIFEST_COMMIT_INVALID",
                f"index={index}",
                fixture="C10",
            )
        if not path or ".." in path.split("/"):
            return fail(
                "C10_MANIFEST_PATH_INVALID",
                f"index={index}",
                fixture="C10",
            )
        if nbytes is None or nbytes < 0:
            return fail(
                "C10_MANIFEST_BYTES_INVALID",
                f"index={index}",
                fixture="C10",
            )
        if not HEX64_RE.match(digest):
            return fail(
                "C10_MANIFEST_SHA256_INVALID",
                f"index={index}",
                fixture="C10",
            )
        return ok(index=index)


class ExpertenkodexCausalMachine:
    """Causal state machine transitions (C16 + SM contract)."""

    def validate_transition(self, current: str, nxt: str) -> Dict[str, Any]:
        cur = _as_str(current).upper()
        nxt_s = _as_str(nxt).upper()
        if cur not in VALID_SM_STATES or nxt_s not in VALID_SM_STATES:
            return fail(
                "C16_SM_STATE_UNKNOWN",
                f"current={cur} next={nxt_s}",
                fixture="C16",
            )
        if (cur, nxt_s) not in SM_EDGES:
            return fail(
                "C16_SM_TRANSITION_INVALID",
                f"current={cur} next={nxt_s}",
                fixture="C16",
            )
        return ok(current=cur, next=nxt_s)


class ExpertenkodexAdversarialGate:
    """C11–C15 semantic / security negative fixtures."""

    def check_receiver_ack(
        self,
        *,
        adapter_connected: bool,
        independent_ack: bool,
        same_process_synthetic: bool,
    ) -> Dict[str, Any]:
        if not adapter_connected:
            return fail(
                "C11_ADAPTER_NOT_CONNECTED",
                "independent external receiver cycle not established",
                fixture="C11",
                status="ADAPTER_NOT_CONNECTED",
            )
        if same_process_synthetic:
            return fail(
                "C11_SYNTHETIC_ACK_NOT_INDEPENDENT",
                "same-process ACK ≠ independent external handshake",
                fixture="C11",
            )
        if not independent_ack:
            return fail(
                "C11_INDEPENDENT_ACK_MISSING",
                fixture="C11",
            )
        return ok(fixture="C11", status="INDEPENDENT_ACK_ESTABLISHED")

    def check_declared_vs_authenticated(
        self, *, declared_identity: str, authenticated_principal: Optional[str]
    ) -> Dict[str, Any]:
        declared = _as_str(declared_identity)
        auth = _as_str(authenticated_principal) if authenticated_principal else ""
        if not auth:
            return fail(
                "C12_AUTHENTICATED_PRINCIPAL_MISSING",
                f"declared={declared}",
                fixture="C12",
            )
        if declared and declared != auth:
            return fail(
                "C12_DECLARED_NE_AUTHENTICATED",
                f"declared={declared} authenticated={auth}",
                fixture="C12",
            )
        return ok(fixture="C12", principal=auth)

    def check_research_claims(self, claims: Iterable[str]) -> Dict[str, Any]:
        normalized = {_as_str(c).upper() for c in claims}
        for tok in PROHIBITED_BIOLOGY_CLAIM_TOKENS:
            if tok in normalized:
                return fail(
                    "C13_VIDEO_OR_BIOLOGY_AS_PROOF",
                    f"token={tok}",
                    fixture="C13",
                )
        # Optogenetics / side-channel may only appear as OPERATOR_REFERENCED_SECONDARY
        if "OPTOGENETICS_TECHNICAL_EQUIVALENCE_PROVEN" in normalized:
            return fail(
                "C13_OPTOGENETICS_OVERCLAIM",
                fixture="C13",
            )
        if "CACHE_SIDECHANNEL_PROVES_AGENT_COMMUNICATION" in normalized:
            return fail(
                "C13_SIDECHANNEL_OVERCLAIM",
                fixture="C13",
            )
        return ok(fixture="C13")

    def check_covert_channels(self, tokens: Iterable[str]) -> Dict[str, Any]:
        normalized = {_as_str(t).upper() for t in tokens}
        for tok in PROHIBITED_COVERT_CHANNEL_TOKENS:
            if tok in normalized:
                return fail(
                    "C14_COVERT_CHANNEL_AS_TRANSPORT",
                    f"token={tok}",
                    fixture="C14",
                )
        if "UNAUTHORIZED_DATA_ROUTE" in normalized:
            return fail("C14_UNAUTHORIZED_DATA_ROUTE", fixture="C14")
        return ok(fixture="C14")

    def check_ci_enforcement(
        self,
        *,
        listed_in_docs: bool,
        workflow_runs_tests: bool,
        required_check_enforced: bool,
        executed: bool,
    ) -> Dict[str, Any]:
        if listed_in_docs and not workflow_runs_tests:
            return fail(
                "C15_CODEX_LISTED_NOT_CI_WIRED",
                fixture="C15",
            )
        if workflow_runs_tests and not executed:
            # CI_CONFIGURED ≠ EXECUTED — informational hold, not false PASS
            return fail(
                "C15_CI_CONFIGURED_NOT_EXECUTED",
                fixture="C15",
                note="CI_CONFIGURED≠EXECUTED",
            )
        if executed and not required_check_enforced:
            return fail(
                "C15_EXECUTED_NOT_REQUIRED_CHECK",
                fixture="C15",
                note="EXECUTED≠REQUIRED_CHECK_ENFORCED",
            )
        return ok(
            fixture="C15",
            listed_in_docs=listed_in_docs,
            workflow_runs_tests=workflow_runs_tests,
            executed=executed,
            required_check_enforced=required_check_enforced,
        )


def build_obligatory_expert_order_header(
    *,
    mandate_source_manifest: Sequence[Mapping[str, Any]],
    pin: CodexPin = CANONICAL_PIN,
) -> Dict[str, Any]:
    """Task-order generator helper — always emit full EXPERTENKODEX pin (K1)."""
    header = {
        **pin.as_dict(),
        "MANDATE_SOURCE_MANIFEST": [dict(x) for x in mandate_source_manifest],
        "ACK_REQUIRED": True,
        "CLAIM_CEILING": "C1_DESCRIPTIVE_ONLY",
        "AUTO_MERGE": "NO",
        "NATIVE_APP_R3": "HOLD",
    }
    v = ExpertenkodexHeaderValidator().validate(header, pin=pin)
    if not v["ok"]:
        raise ValueError(f"generated header failed validation: {v}")
    return header


def verify_local_codex_bytes(raw: bytes, pin: CodexPin = CANONICAL_PIN) -> Dict[str, Any]:
    digest = sha256_bytes(raw)
    if len(raw) != pin.bytes:
        return fail(
            "CODEX_BYTES_MISMATCH",
            f"got={len(raw)} expected={pin.bytes}",
        )
    if digest != pin.sha256:
        return fail(
            "CODEX_SHA256_MISMATCH",
            f"got={digest}",
        )
    return ok(bytes=len(raw), sha256=digest, commit=pin.commit, path=pin.path)


__all__ = [
    "CANONICAL_PIN",
    "CODEX_BYTES",
    "CODEX_COMMIT",
    "CODEX_OBJECT",
    "CODEX_PATH",
    "CODEX_SHA256",
    "CodexPin",
    "ExpertenkodexAdversarialGate",
    "ExpertenkodexCausalMachine",
    "ExpertenkodexHeaderValidator",
    "REQUIRED_HEADER_KEYS",
    "SM_EDGES",
    "VALID_SM_STATES",
    "build_obligatory_expert_order_header",
    "verify_local_codex_bytes",
]
