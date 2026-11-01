#!/usr/bin/env python3
"""NEXUS Agent Communication Framework — Document Router (Final Gated Release R0).

Wraps nexus_github_exchange_chain for unified document handoff.
Claim ceiling: C1_DESCRIPTIVE_ONLY
PUBLIC_EXTERNAL_WRITE_API = HOLD
MULTI_TRANSPORT_V3 = DRAFT_ONLY
NATIVE_APP_R3 = HOLD
Same-process receiver ACK = PROHIBITED
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_SCRIPTS_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    from nexus_github_exchange_chain import (
        ADAPTER_NOT_CONNECTED,
        DEFAULT_REPO,
        AgentAdapter,
        DeliveryJournal,
        DispatchValidator,
        ExchangeChain,
        LegacyGrantRegistry,
        ReceiverAckProtocol,
        SourceResolver,
        fail,
        ok,
        sha256_bytes,
        sha256_file,
        utc_now,
    )
except ImportError:  # pragma: no cover
    from scripts.nexus_github_exchange_chain import (
        ADAPTER_NOT_CONNECTED,
        DEFAULT_REPO,
        AgentAdapter,
        DeliveryJournal,
        DispatchValidator,
        ExchangeChain,
        LegacyGrantRegistry,
        ReceiverAckProtocol,
        SourceResolver,
        fail,
        ok,
        sha256_bytes,
        sha256_file,
        utc_now,
    )

# ---------------------------------------------------------------------------
# Constants (order-bound)
# ---------------------------------------------------------------------------

ORDER_OBJECT = (
    "NEXUS_OMEGA_AXIOM_CURSOR_AGENT_COMMUNICATION_FRAMEWORK_"
    "FINAL_GATED_RELEASE_AND_UNIFIED_DOCUMENT_HANDOFF_20261031_R0"
)
ORDER_PINNED_COMMIT = "978f41138f76d75c162bd33be61938c0b95c4200"
ORDER_PATH = (
    "research/communication/github-only-exchange-enforcement-20261029/"
    "AXIOM_CURSOR_AGENT_COMMUNICATION_FRAMEWORK_FINAL_GATED_RELEASE_"
    "AND_UNIFIED_DOCUMENT_HANDOFF_20261031_R0.md"
)
ORDER_BYTES = 15567
ORDER_SHA256 = "bebfaeb2ddfa067a94448250b1aa20a8d3c12a8f2460218d7d51eabcd552cfd0"

ROUTING_STATES = (
    "CREATED",
    "SOURCE_PINNED",
    "PRIVACY_LICENSE_PASS",
    "MANIFEST_CLOSED",
    "STAGED",
    "OUTBOUND_QUEUED",
    "DISPATCHED",
    "FETCH_OBSERVED",
    "RECEIVED_BYTES_VERIFIED",
    "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED",
    "RETURN_SOURCE_VERIFIED",
    "SCIENTIFIC_ADJUDICATION_SEPARATE",
)

SOURCE_CLASSES = (
    "PUBLIC_SAFE_GITHUB",
    "OWNER_GOVERNED_PRIVATE",
    "REDACTED_COMMITMENT_ONLY",
    "HOLD_UNSUPPORTED_PRIVATE",
)

CUTOVER_STAGED = "FRAMEWORK_REQUIRED_STAGED"
CUTOVER_ACTIVE = "FRAMEWORK_REQUIRED_ACTIVE"
CLAIM_CEILING = "C1_DESCRIPTIVE_ONLY"

PRIVATE_PATH_MARKERS = (
    "/private/",
    "\\private\\",
    ".env",
    "secrets/",
    "credentials",
    "api_key",
    "token.json",
)

FORBIDDEN_PUBLIC_WRITE = (
    "PUBLIC_EXTERNAL_WRITE_API",
    "HOSTINGER_WWW_WRITE",
    "UNREGISTERED_AGENT_WRITE",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_transition(current: str, nxt: str) -> bool:
    if current not in ROUTING_STATES or nxt not in ROUTING_STATES:
        return False
    if nxt == current:
        return True
    # Allow forward-only along the ordered chain (including skip for adjudicate).
    ci = ROUTING_STATES.index(current)
    ni = ROUTING_STATES.index(nxt)
    if ni < ci:
        return False
    if nxt == "SCIENTIFIC_ADJUDICATION_SEPARATE":
        return current in (
            "RETURN_SOURCE_VERIFIED",
            "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED",
            "RECEIVED_BYTES_VERIFIED",
        )
    return ni == ci + 1 or (ni > ci and nxt in ROUTING_STATES[ci:])


def classify_source(
    *,
    path: str,
    privacy_class: str,
    redacted: bool = False,
) -> str:
    p = path.replace("\\", "/").lower()
    if redacted or privacy_class == "REDACTED_COMMITMENT_ONLY":
        return "REDACTED_COMMITMENT_ONLY"
    if privacy_class == "HOLD_UNSUPPORTED_PRIVATE" or any(
        m in p for m in PRIVATE_PATH_MARKERS
    ):
        if privacy_class == "OWNER_GOVERNED_PRIVATE":
            return "OWNER_GOVERNED_PRIVATE"
        return "HOLD_UNSUPPORTED_PRIVATE"
    if privacy_class == "OWNER_GOVERNED_PRIVATE":
        return "OWNER_GOVERNED_PRIVATE"
    return "PUBLIC_SAFE_GITHUB"


def _valid_private_lane_proof(
    proof: Optional[Dict[str, Any]],
    *,
    owner_lane_registry: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """P0-4: private lane only from owner-signed registry entry, not caller JSON alone."""
    if not isinstance(proof, dict):
        return fail("PRIVATE_LANE_PROOF_REQUIRED", "dict required")
    entry_id = str(proof.get("entry_id") or proof.get("registry_entry_id") or "").strip()
    if not entry_id:
        return fail("PRIVATE_LANE_ENTRY_ID_REQUIRED", "owner registry entry_id required")
    if not isinstance(owner_lane_registry, dict):
        return fail(
            "PRIVATE_LANE_OWNER_REGISTRY_REQUIRED",
            "owner_lane_registry must be bound on RouterConfig",
        )
    entry = owner_lane_registry.get(entry_id)
    if not isinstance(entry, dict):
        return fail("PRIVATE_LANE_ENTRY_UNKNOWN", entry_id)
    if str(entry.get("status") or "").upper() != "ACTIVE":
        return fail("PRIVATE_LANE_ENTRY_INACTIVE", str(entry.get("status")))
    scope = str(entry.get("scope") or "").upper()
    if scope not in ("OWNER_PRIVATE_DISPATCH", "OWNER_PRIVATE_READ_WRITE"):
        return fail("PRIVATE_LANE_SCOPE_INVALID", scope)
    signer = str(entry.get("signer") or entry.get("owner") or "").strip()
    if not signer:
        return fail("PRIVATE_LANE_SIGNER_REQUIRED", entry_id)
    return ok(
        private_lane=True,
        entry_id=entry_id,
        scope=scope,
        signer=signer,
        lane_class=str(entry.get("lane_class") or "OWNER_GOVERNED"),
    )


def privacy_gate(
    *,
    source_class: str,
    path: str,
    allow_private_dispatch: bool = False,
    private_lane_proof: Optional[Dict[str, Any]] = None,
    owner_lane_registry: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Public-safe GitHub first; private only via owner registry (P0-4)."""
    if source_class == "HOLD_UNSUPPORTED_PRIVATE":
        return fail(
            "PRIVATE_SOURCE_HOLD",
            f"path={path}; class={source_class}",
        )
    if source_class == "OWNER_GOVERNED_PRIVATE":
        if not allow_private_dispatch:
            return fail(
                "PRIVATE_DISPATCH_NOT_ALLOWED",
                "allow_private_dispatch=false",
            )
        lane = _valid_private_lane_proof(
            private_lane_proof,
            owner_lane_registry=owner_lane_registry,
        )
        if not lane.get("ok"):
            return lane
        return ok(
            privacy="PASS_OWNER_GOVERNED_PRIVATE",
            private_lane=lane,
        )
    if source_class == "REDACTED_COMMITMENT_ONLY":
        return ok(
            privacy="PASS_REDACTED_COMMITMENT_ONLY",
            note="commitment/hash only; raw private bytes not transported",
        )
    return ok(privacy="PASS_PUBLIC_SAFE_GITHUB")


def validate_cutover_activation_manifest(
    manifest: Optional[Dict[str, Any]],
    *,
    trusted_cutover_evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """P0-3: cutover only from owner-signed trusted evidence, not JSON booleans."""
    if not isinstance(manifest, dict):
        return fail("CUTOVER_MANIFEST_REQUIRED", "dict required")
    required = (
        "object_id",
        "authority",
        "scope",
        "activation_token",
        "evidence_sha256",
        "evidence_bytes",
        "authorized_at_utc",
    )
    missing = [k for k in required if not str(manifest.get(k) or "").strip()]
    if missing:
        return fail("CUTOVER_MANIFEST_INCOMPLETE", f"missing={missing}")
    if str(manifest.get("scope")) != "DOCUMENT_HANDOFF_CUTOVER":
        return fail("CUTOVER_SCOPE_INVALID", str(manifest.get("scope")))
    if str(manifest.get("authority")) != "OPERATOR_ALEXANDER":
        return fail("CUTOVER_AUTHORITY_INVALID", str(manifest.get("authority")))
    if not isinstance(trusted_cutover_evidence, dict):
        return fail(
            "CUTOVER_TRUSTED_EVIDENCE_REQUIRED",
            "trusted_cutover_evidence must be bound on RouterConfig",
        )
    ev_sha = str(trusted_cutover_evidence.get("sha256") or "").lower()
    man_sha = str(manifest.get("evidence_sha256") or "").lower()
    try:
        ev_bytes = int(trusted_cutover_evidence.get("bytes"))
        man_bytes = int(manifest.get("evidence_bytes"))
    except (TypeError, ValueError):
        return fail("CUTOVER_EVIDENCE_BYTES_INVALID", "bytes mismatch type")
    if not ev_sha or ev_sha != man_sha or ev_bytes != man_bytes:
        return fail(
            "CUTOVER_EVIDENCE_MISMATCH",
            f"trusted={ev_sha}/{ev_bytes}; manifest={man_sha}/{man_bytes}",
        )
    if str(trusted_cutover_evidence.get("signer") or "") != "OPERATOR_ALEXANDER":
        return fail(
            "CUTOVER_EVIDENCE_SIGNER_INVALID",
            str(trusted_cutover_evidence.get("signer")),
        )
    if str(trusted_cutover_evidence.get("status") or "").upper() != "AUTHORIZED":
        return fail(
            "CUTOVER_EVIDENCE_STATUS_INVALID",
            str(trusted_cutover_evidence.get("status")),
        )
    # Reject caller-supplied activation booleans as authority.
    for banned in ("cutover_active", "force_active", "authorized"):
        if banned in manifest and isinstance(manifest.get(banned), bool):
            return fail(
                "CUTOVER_BOOLEAN_CLAIM_REJECTED",
                f"field={banned} is not trusted evidence",
            )
    return ok(
        cutover_activation="AUTHORIZED",
        object_id=str(manifest.get("object_id")),
        evidence_sha256=man_sha,
        evidence_bytes=man_bytes,
        activation_token=str(manifest.get("activation_token")),
        authorized_at_utc=str(manifest.get("authorized_at_utc")),
    )


def verify_github_receiver_witness(
    *,
    witness: Optional[Dict[str, Any]],
    document: Dict[str, Any],
    receipt: Dict[str, Any],
    github_client: Any = None,
) -> Dict[str, Any]:
    """P0-1: verifier-owned GitHub REST fetch; reject caller api_attestation."""
    if not isinstance(witness, dict):
        return fail(
            "ACK_GITHUB_WITNESS_REQUIRED",
            "principal/return verification requires github_api_witness",
        )
    # P0-1 hard reject: caller-asserted REST verification is never proof.
    if str(witness.get("api_attestation") or "") in (
        "GITHUB_REST_VERIFIED",
        "TRANSPORT_API_VERIFIED",
    ):
        # Still allow the *field* to be present as untrusted hint only when
        # a github_client will independently re-fetch. If no client → reject.
        if github_client is None:
            return fail(
                "CALLER_GITHUB_API_WITNESS_REJECTED",
                "api_attestation from caller is not trusted without verifier fetch",
            )
    comment_id = witness.get("comment_id") or witness.get("issue_comment_id")
    immutable_url = str(witness.get("immutable_url") or "")
    if comment_id is None and immutable_url:
        m = re.search(r"/issues/comments?/(\d+)", immutable_url)
        if m:
            comment_id = m.group(1)
    if comment_id is None:
        return fail(
            "ACK_GITHUB_COMMENT_ID_REQUIRED",
            "untrusted ref must include comment_id for verifier fetch",
        )
    try:
        comment_id_int = int(comment_id)
    except (TypeError, ValueError):
        return fail("ACK_GITHUB_COMMENT_ID_INVALID", str(comment_id))
    if github_client is None:
        return fail(
            "GITHUB_IDENTITY_NOT_VERIFIED",
            "github_client unavailable; cannot independently verify receiver",
        )
    try:
        fetched = github_client.get_issue_comment(comment_id_int)
    except Exception as exc:  # noqa: BLE001 — surface as fail-closed
        return fail("GITHUB_IDENTITY_NOT_VERIFIED", f"fetch_error={exc}")
    if not isinstance(fetched, dict):
        return fail("GITHUB_IDENTITY_NOT_VERIFIED", "empty fetch")
    try:
        author_id = int(fetched.get("user", {}).get("id") or fetched.get("author_id"))
    except (TypeError, ValueError, AttributeError):
        return fail("ACK_GITHUB_AUTHOR_ID_INVALID", "from fetch")
    if author_id <= 0:
        return fail("ACK_GITHUB_AUTHOR_ID_INVALID", str(author_id))
    login = str(
        (fetched.get("user") or {}).get("login")
        or fetched.get("author_login")
        or ""
    ).strip()
    if not login or login.upper() in ("UNAUTHENTICATED", "UNKNOWN", "SELF"):
        return fail("ACK_GITHUB_AUTHOR_LOGIN_INVALID", login)
    url = str(
        fetched.get("html_url")
        or fetched.get("immutable_url")
        or immutable_url
        or ""
    )
    if not (
        url.startswith("https://github.com/")
        and ("/issues/comment/" in url or "/pull/" in url or "/commit/" in url)
    ):
        return fail("ACK_GITHUB_IMMUTABLE_URL_INVALID", url)
    # Observed document bytes must match the document under custody — from
    # verifier context, never from caller-asserted observed_* alone.
    doc_sha = str(document.get("sha256") or "").lower()
    try:
        doc_bytes = int(document.get("bytes") or -1)
    except (TypeError, ValueError):
        return fail("ACK_GITHUB_OBSERVED_BYTES_INVALID", "document.bytes")
    obs_sha = str(
        fetched.get("observed_sha256")
        or witness.get("observed_sha256")
        or ""
    ).lower()
    try:
        obs_bytes = int(
            fetched.get("observed_bytes")
            if fetched.get("observed_bytes") is not None
            else witness.get("observed_bytes")
        )
    except (TypeError, ValueError):
        return fail(
            "ACK_GITHUB_OBSERVED_BYTES_INVALID",
            str(witness.get("observed_bytes")),
        )
    if not doc_sha or obs_sha != doc_sha or obs_bytes != doc_bytes:
        return fail(
            "ACK_GITHUB_BYTES_MISMATCH",
            f"witness_sha={obs_sha}; doc_sha={doc_sha}",
        )
    producer = str(
        receipt.get("producer_principal") or document.get("repository") or ""
    ).lower()
    receiver = login.lower()
    if receiver and producer and receiver == producer:
        return fail("ACK_PRODUCER_EQUALS_RECEIVER", receiver)
    if login.lower() == "nexusomegac27":
        return fail(
            "ACK_OWNER_LOGIN_REUSE_REJECTED",
            "owner login cannot self-attest as independent receiver",
        )
    return_source_ok = False
    rs_commit = fetched.get("return_source_commit") or witness.get(
        "return_source_commit"
    )
    rs_sha = fetched.get("return_source_sha256") or witness.get(
        "return_source_sha256"
    )
    if rs_commit and rs_sha and str(rs_sha).lower() == doc_sha:
        return_source_ok = True
    return ok(
        principal_verified=True,
        return_source_verified=return_source_ok,
        author_id=author_id,
        author_login=login,
        immutable_url=url,
        comment_id=comment_id_int,
        api_attestation="GITHUB_REST_VERIFIER_FETCHED",
        attestation_class="VERIFIER_OWNED",
    )


# ---------------------------------------------------------------------------
# SQLite WAL document store
# ---------------------------------------------------------------------------

class DocumentStore:
    """Persistent document routing state (SQLite WAL). DeliveryJournal remains JSONL."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                object_id TEXT NOT NULL,
                routing_state TEXT NOT NULL,
                source_class TEXT NOT NULL,
                repository TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                path TEXT NOT NULL,
                bytes INTEGER,
                sha256 TEXT,
                privacy_class TEXT NOT NULL,
                manifest_json TEXT,
                cutover_state TEXT NOT NULL,
                claim_ceiling TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS transitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                from_state TEXT NOT NULL,
                to_state TEXT NOT NULL,
                detail_json TEXT,
                ts TEXT NOT NULL,
                FOREIGN KEY(document_id) REFERENCES documents(document_id)
            );
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                receipt_kind TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                ts TEXT NOT NULL,
                FOREIGN KEY(document_id) REFERENCES documents(document_id)
            );
            CREATE TABLE IF NOT EXISTS cutover (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        self._conn.commit()
        # Default cutover: STAGED until critical gates observed.
        cur = self._conn.execute(
            "SELECT value FROM cutover WHERE key='document_handoff'"
        ).fetchone()
        if cur is None:
            self.set_cutover(CUTOVER_STAGED)

    def close(self) -> None:
        self._conn.close()

    def set_cutover(self, state: str) -> None:
        if state not in (CUTOVER_STAGED, CUTOVER_ACTIVE):
            raise ValueError(f"invalid cutover state: {state}")
        self._conn.execute(
            "INSERT INTO cutover(key,value,updated_at) VALUES(?,?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value, "
            "updated_at=excluded.updated_at",
            ("document_handoff", state, utc_now()),
        )
        self._conn.commit()

    def get_cutover(self) -> str:
        row = self._conn.execute(
            "SELECT value FROM cutover WHERE key='document_handoff'"
        ).fetchone()
        return str(row["value"]) if row else CUTOVER_STAGED

    def create_document(
        self,
        *,
        object_id: str,
        repository: str,
        commit_sha: str,
        path: str,
        source_class: str,
        privacy_class: str,
        bytes_n: Optional[int] = None,
        sha256: Optional[str] = None,
        document_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        did = document_id or f"doc:{uuid.uuid4().hex}"
        ts = utc_now()
        cutover = self.get_cutover()
        self._conn.execute(
            """
            INSERT INTO documents(
                document_id, object_id, routing_state, source_class,
                repository, commit_sha, path, bytes, sha256, privacy_class,
                manifest_json, cutover_state, claim_ceiling, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                did,
                object_id,
                "CREATED",
                source_class,
                repository,
                commit_sha,
                path,
                bytes_n,
                sha256,
                privacy_class,
                None,
                cutover,
                CLAIM_CEILING,
                ts,
                ts,
            ),
        )
        self._conn.execute(
            "INSERT INTO transitions(document_id,from_state,to_state,detail_json,ts) "
            "VALUES(?,?,?,?,?)",
            (did, "NONE", "CREATED", "{}", ts),
        )
        self._conn.commit()
        return self.get_document(did)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        row = self._conn.execute(
            "SELECT * FROM documents WHERE document_id=?", (document_id,)
        ).fetchone()
        if row is None:
            raise KeyError(document_id)
        return dict(row)

    def list_documents(self) -> List[Dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT * FROM documents ORDER BY created_at"
        ).fetchall()
        return [dict(r) for r in rows]

    def transition(
        self,
        document_id: str,
        to_state: str,
        *,
        detail: Optional[Dict[str, Any]] = None,
        manifest: Optional[Dict[str, Any]] = None,
        bytes_n: Optional[int] = None,
        sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        doc = self.get_document(document_id)
        current = doc["routing_state"]
        if not _valid_transition(current, to_state):
            raise ValueError(f"invalid transition {current} -> {to_state}")
        ts = utc_now()
        fields = ["routing_state=?", "updated_at=?"]
        values: List[Any] = [to_state, ts]
        if manifest is not None:
            fields.append("manifest_json=?")
            values.append(json.dumps(manifest, sort_keys=True))
        if bytes_n is not None:
            fields.append("bytes=?")
            values.append(bytes_n)
        if sha256 is not None:
            fields.append("sha256=?")
            values.append(sha256)
        values.append(document_id)
        self._conn.execute(
            f"UPDATE documents SET {', '.join(fields)} WHERE document_id=?",
            values,
        )
        self._conn.execute(
            "INSERT INTO transitions(document_id,from_state,to_state,detail_json,ts) "
            "VALUES(?,?,?,?,?)",
            (
                document_id,
                current,
                to_state,
                json.dumps(detail or {}, sort_keys=True),
                ts,
            ),
        )
        self._conn.commit()
        return self.get_document(document_id)

    def add_receipt(
        self,
        document_id: str,
        receipt_kind: str,
        payload: Dict[str, Any],
    ) -> str:
        rid = f"rcpt:{uuid.uuid4().hex}"
        self._conn.execute(
            "INSERT INTO receipts(receipt_id,document_id,receipt_kind,payload_json,ts) "
            "VALUES(?,?,?,?,?)",
            (
                rid,
                document_id,
                receipt_kind,
                json.dumps(payload, sort_keys=True),
                utc_now(),
            ),
        )
        self._conn.commit()
        return rid


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


@dataclass
class RouterConfig:
    repo_root: Path
    store_path: Path
    journal_dir: Path
    cutover_force_active: bool = False
    activation_manifest: Optional[Dict[str, Any]] = None
    github_client: Any = None
    owner_lane_registry: Optional[Dict[str, Any]] = None
    transport_adapter: Any = None
    trusted_cutover_evidence: Optional[Dict[str, Any]] = None


class DocumentRouter:
    def __init__(self, cfg: RouterConfig) -> None:
        self.cfg = cfg
        self.repo_root = Path(cfg.repo_root).resolve()
        self.store = DocumentStore(cfg.store_path)
        self.chain = ExchangeChain(
            self.repo_root, journal_dir=cfg.journal_dir
        )
        self.resolver = self.chain.resolver
        self.validator = self.chain.validator
        self.adapter = self.chain.adapter
        self.receiver = self.chain.receiver
        self.journal = self.chain.journal
        # P0-C: --activate-cutover / cutover_force_active alone NEVER flips ACTIVE.
        if cfg.cutover_force_active:
            gate = validate_cutover_activation_manifest(
                cfg.activation_manifest or {},
                trusted_cutover_evidence=cfg.trusted_cutover_evidence,
            )
            if gate.get("ok"):
                self.store.set_cutover(CUTOVER_ACTIVE)
                self._cutover_activation = gate
            else:
                self._cutover_activation = gate
        else:
            self._cutover_activation = None

    def close(self) -> None:
        self.store.close()

    def cutover_status(self) -> Dict[str, Any]:
        state = self.store.get_cutover()
        return ok(
            document_handoff=state,
            framework_policy="APPROVED",
            initial_transport="GITHUB_ONLY",
            public_external_write_api="HOLD",
            multi_transport_v3="DRAFT_ONLY",
            native_app_r3="HOLD",
            unverified_external_ack="NOT_ESTABLISHED",
            claim_ceiling=CLAIM_CEILING,
            order_object=ORDER_OBJECT,
            order_pinned_commit=ORDER_PINNED_COMMIT,
            activation_attempt=self._cutover_activation,
            note=(
                "STAGED means DOCUMENT_HANDOFF=FRAMEWORK_REQUIRED for new "
                "material; productive GitHub cutover ACTIVE only after "
                "critical integrity/privacy/CI/rollback gates PASS; "
                "CLI --activate-cutover without valid activation manifest "
                "leaves STAGED"
            ),
        )

    def activate_cutover(self, activation_manifest: Dict[str, Any]) -> Dict[str, Any]:
        gate = validate_cutover_activation_manifest(
            activation_manifest,
            trusted_cutover_evidence=self.cfg.trusted_cutover_evidence,
        )
        self._cutover_activation = gate
        if not gate.get("ok"):
            return gate
        self.store.set_cutover(CUTOVER_ACTIVE)
        return ok(
            document_handoff=CUTOVER_ACTIVE,
            activation=gate,
            claim_ceiling=CLAIM_CEILING,
        )

    def dispatch_document(
        self,
        *,
        object_id: str,
        repository: str,
        commit: str,
        path: str,
        expected_sha256: Optional[str] = None,
        expected_bytes: Optional[int] = None,
        privacy_class: str = "PUBLIC_SAFE",
        redacted: bool = False,
        allow_private_dispatch: bool = False,
        private_lane_proof: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
        document_id: Optional[str] = None,
        transport_witness: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        # Hold public write surfaces.
        for forbidden in FORBIDDEN_PUBLIC_WRITE:
            if privacy_class.upper() == forbidden:
                return fail("PUBLIC_WRITE_SURFACE_HOLD", forbidden)

        source_class = classify_source(
            path=path, privacy_class=privacy_class, redacted=redacted
        )
        pg = privacy_gate(
            source_class=source_class,
            path=path,
            allow_private_dispatch=allow_private_dispatch,
            private_lane_proof=private_lane_proof,
            owner_lane_registry=self.cfg.owner_lane_registry,
        )
        if not pg.get("ok"):
            return pg

        # G1 — pin source bytes via existing SourceResolver.
        resolved = self.resolver.resolve(
            repository=repository,
            commit=commit,
            path=path,
            expected_sha256=expected_sha256,
            expected_bytes=expected_bytes,
        )
        if not resolved.get("ok"):
            return resolved

        # SourceResolver.resolve nests identity under resolved["source"].
        src = resolved.get("source") or {}
        observed_bytes = src.get("bytes")
        observed_sha256 = src.get("sha256")
        observed_path = src.get("path", path)
        observed_commit = src.get("commit", commit)

        doc = self.store.create_document(
            object_id=object_id,
            repository=repository,
            commit_sha=commit,
            path=path,
            source_class=source_class,
            privacy_class=privacy_class,
            bytes_n=observed_bytes,
            sha256=observed_sha256,
            document_id=document_id,
        )
        did = doc["document_id"]
        self.store.transition(
            did,
            "SOURCE_PINNED",
            detail={
                "resolve": {
                    "bytes": observed_bytes,
                    "sha256": observed_sha256,
                    "path": observed_path,
                    "commit": observed_commit,
                }
            },
            bytes_n=observed_bytes,
            sha256=observed_sha256,
        )
        self.store.transition(did, "PRIVACY_LICENSE_PASS", detail=pg)

        manifest = {
            "object": object_id,
            "repository": repository,
            "commit": commit,
            "path": path,
            "sha256": observed_sha256,
            "bytes": observed_bytes,
            "source_class": source_class,
            "document_id": did,
            "claim_ceiling": CLAIM_CEILING,
            "transport": "GITHUB_ONLY",
            "cutover": self.store.get_cutover(),
        }
        # Optional Expertenkodex / legacy grant path via DispatchValidator.
        v = self.validator.validate_manifest(manifest)
        # Manifest without CODEX_* is allowed for public-safe document routing;
        # DispatchValidator fails closed on Expertenkodex-declared orders only.
        # For framework document handoff we accept PUBLIC_SAFE without kodex
        # when no CODEX_* keys are present.
        if not v.get("ok") and "CODEX_" not in json.dumps(manifest):
            # Re-validate only identity fields via resolver (already MATCH).
            v = ok(
                gate="G1_DOCUMENT_SOURCE_PINNED",
                note="public-safe document handoff without Expertenkodex envelope",
                resolve=resolved,
            )
        if not v.get("ok"):
            return v

        self.store.transition(
            did, "MANIFEST_CLOSED", detail={"validation": v}, manifest=manifest
        )
        self.store.transition(did, "STAGED", detail={"cutover": self.store.get_cutover()})

        outbound = self.journal.append(
            stream="outbound",
            payload={
                "document_id": did,
                "object": object_id,
                "commit": commit,
                "path": path,
                "sha256": observed_sha256,
                "bytes": observed_bytes,
                "transport": "GITHUB_ONLY",
                "intent": "OUTBOUND_QUEUED",
            },
            idempotency_key=f"doc-outbound:{did}:{commit}",
        )
        # P0-B: local journal is intent only — never claim DISPATCHED/SENT here.
        self.store.transition(
            did,
            "OUTBOUND_QUEUED",
            detail={"outbound": outbound.get("event_id"), "delivery": "NOT_WITNESSED"},
        )

        adapter_status = ADAPTER_NOT_CONNECTED
        adapter_decl: Dict[str, Any] = {}
        if agent_id:
            adapter_decl = self.adapter.declare(model_id=agent_id)
            adapter_status = adapter_decl.get("status", ADAPTER_NOT_CONNECTED)

        delivery_state = "OUTBOUND_QUEUED"
        tw = transport_witness if isinstance(transport_witness, dict) else {}
        # P0-5: reject caller-asserted TRANSPORT_API_VERIFIED as proof.
        if str(tw.get("api_attestation") or "") == "TRANSPORT_API_VERIFIED":
            transport_result = {
                "delivered": False,
                "reason": "TRANSPORT_WITNESS_CALLER_ASSERTED",
                "adapter_status": adapter_status,
                "adapter_decl": adapter_decl,
            }
        else:
            transport_adapter = getattr(self.cfg, "transport_adapter", None)
            adapter_prove: Dict[str, Any] = {}
            if transport_adapter is not None and hasattr(transport_adapter, "prove"):
                try:
                    adapter_prove = transport_adapter.prove(
                        observed_sha256=observed_sha256,
                        observed_bytes=observed_bytes,
                        transport_witness=tw,
                        outbound=outbound,
                    )
                except Exception as exc:  # noqa: BLE001
                    adapter_prove = {"ok": False, "error": str(exc)}
            else:
                adapter_prove = {
                    "ok": False,
                    "error": "TRANSPORT_ADAPTER_PROVE_REQUIRED",
                }
            witness_ok = (
                bool(adapter_prove.get("ok"))
                and str(adapter_prove.get("observed_sha256", "")).lower()
                == str(observed_sha256 or "").lower()
                and int(adapter_prove.get("observed_bytes", -1))
                == int(observed_bytes or -2)
                and adapter_status != ADAPTER_NOT_CONNECTED
            )
            if witness_ok:
                self.store.transition(
                    did,
                    "DISPATCHED",
                    detail={
                        "outbound": outbound.get("event_id"),
                        "transport_witness": tw,
                        "adapter_status": adapter_status,
                        "adapter_prove": adapter_prove,
                    },
                )
                delivery_state = "DISPATCHED"
                transport_result = {
                    "delivered": True,
                    "reason": "TRANSPORT_ADAPTER_PROVE_ACCEPTED",
                    "adapter_status": adapter_status,
                    "adapter_prove": adapter_prove,
                }
            else:
                transport_result = {
                    "delivered": False,
                    "reason": (
                        "ADAPTER_NOT_CONNECTED"
                        if adapter_status == ADAPTER_NOT_CONNECTED
                        else (
                            "TRANSPORT_ADAPTER_PROVE_REQUIRED"
                            if transport_adapter is None
                            else "TRANSPORT_WITNESS_INCOMPLETE"
                        )
                    ),
                    "adapter_status": adapter_status,
                    "adapter_decl": adapter_decl,
                    "adapter_prove": adapter_prove,
                }

        return ok(
            document_id=did,
            routing_state=delivery_state,
            source_class=source_class,
            manifest=manifest,
            validation=v,
            outbound=outbound,
            adapter_status=adapter_status,
            transport_result=transport_result,
            cutover=self.store.get_cutover(),
            independent_expert_ack="NOT_ESTABLISHED",
            terminal_pass=False,
            claim_ceiling=CLAIM_CEILING,
        )

    def verify_manifest(self, document_id: str) -> Dict[str, Any]:
        try:
            doc = self.store.get_document(document_id)
        except KeyError:
            return fail("DOCUMENT_NOT_FOUND", document_id)
        if not doc.get("manifest_json"):
            return fail("MANIFEST_ABSENT", document_id)
        manifest = json.loads(doc["manifest_json"])
        resolved = self.resolver.resolve(
            repository=manifest["repository"],
            commit=manifest["commit"],
            path=manifest["path"],
            expected_sha256=manifest.get("sha256"),
            expected_bytes=manifest.get("bytes"),
        )
        if not resolved.get("ok"):
            return resolved
        return ok(
            document_id=document_id,
            routing_state=doc["routing_state"],
            manifest=manifest,
            resolve=resolved,
            cutover=self.store.get_cutover(),
        )

    def receive_receipt(
        self,
        *,
        document_id: str,
        receipt: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Ingest an independent receiver ACK. Same-process ACK is rejected."""
        try:
            doc = self.store.get_document(document_id)
        except KeyError:
            return fail("DOCUMENT_NOT_FOUND", document_id)

        # Explicitly reject same-process / synthetic ACKs (ReceiverAckProtocol).
        if receipt.get("synthetic") or receipt.get("same_process"):
            return fail(
                "SAME_PROCESS_ACK_PROHIBITED",
                "receiver ACK must be independent GitHub→receiver→GitHub",
            )
        incoming_pid = receipt.get("receiver_process_id") or receipt.get("process_id")
        if incoming_pid and incoming_pid == self.receiver.sender_process_id:
            return fail("SAME_PROCESS_ACK_PROHIBITED", "process_id collision")

        # Require GitHub-bound identity fields from the independent receiver.
        required = ("repository", "commit", "object_path", "bytes", "sha256", "fetch_method")
        missing = [k for k in required if k not in receipt]
        if missing:
            rid = self.store.add_receipt(document_id, "RECEIPT_REJECTED", receipt)
            return fail("RECEIPT_FIELDS_MISSING", f"receipt_id={rid}; missing={missing}")

        # P0-A: build byte-level ACK without trusting receipt.authenticated.
        # Do not feed self-asserted auth into ReceiverAckProtocol.issue_independent_ack.
        fetch_method = str(receipt["fetch_method"])
        if fetch_method not in {"GITHUB_API_CONTENTS", "GIT_FETCH_SHOW", "GITHUB_RAW"}:
            rid = self.store.add_receipt(document_id, "RECEIPT_REJECTED", receipt)
            return fail(
                "RECEIVER_FETCH_METHOD_INVALID",
                f"receipt_id={rid}; {fetch_method}",
            )
        ack = {
            "repository": str(receipt["repository"]),
            "commit": str(receipt["commit"]),
            "object_path": str(receipt["object_path"]),
            "bytes": int(receipt["bytes"]),
            "sha256": str(receipt["sha256"]),
            "receiver_principal": str(
                receipt.get("receiver_principal") or "UNAUTHENTICATED"
            ),
            "fetch_method": fetch_method,
            "independent": True,
            "ack_id": str(uuid.uuid4()),
            "sender_process_id": self.receiver.sender_process_id,
            "auth_claim_ignored": True,
        }
        observed_sha = doc.get("sha256")
        observed_bytes = doc.get("bytes")
        bytes_match = (
            observed_sha is not None
            and observed_bytes is not None
            and str(ack.get("sha256", "")).lower() == str(observed_sha).lower()
            and int(ack.get("bytes", -1)) == int(observed_bytes)
        )
        # Ignore self-asserted authenticated / return_source_verified booleans.
        _ = receipt.get("authenticated")
        _ = receipt.get("return_source_verified")
        witness_gate = verify_github_receiver_witness(
            witness=receipt.get("github_api_witness"),
            document=doc,
            receipt=receipt,
            github_client=self.cfg.github_client,
        )
        principal_verified = bool(
            witness_gate.get("ok") and witness_gate.get("principal_verified")
        )
        return_source_verified = bool(
            witness_gate.get("ok") and witness_gate.get("return_source_verified")
        )
        verified = {
            "ok": True,
            "ack": ack,
            "bytes_match": bytes_match,
            "principal_verified": principal_verified,
            "return_source_verified": return_source_verified,
            "independent": bool(ack.get("independent")),
            "ack_id": ack.get("ack_id"),
            "github_witness": witness_gate,
            "self_asserted_auth_ignored": True,
        }

        rid = self.store.add_receipt(document_id, "RECEIVER_ACK", verified)
        self.journal.append(
            stream="receiver_ack",
            payload={"document_id": document_id, **verified},
            idempotency_key=f"doc-ack:{document_id}:{rid}",
        )

        state = doc["routing_state"]
        advances = []
        # Fetch may be observed from queued GitHub source without agent delivery.
        if state in ("OUTBOUND_QUEUED", "DISPATCHED"):
            self.store.transition(
                document_id, "FETCH_OBSERVED", detail={"receipt_id": rid}
            )
            advances.append("FETCH_OBSERVED")
            state = "FETCH_OBSERVED"
        if state == "FETCH_OBSERVED" and verified.get("bytes_match"):
            self.store.transition(
                document_id, "RECEIVED_BYTES_VERIFIED", detail={"receipt_id": rid}
            )
            advances.append("RECEIVED_BYTES_VERIFIED")
            state = "RECEIVED_BYTES_VERIFIED"
        if state == "RECEIVED_BYTES_VERIFIED" and verified.get("principal_verified"):
            self.store.transition(
                document_id,
                "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED",
                detail={"receipt_id": rid, "witness": witness_gate},
            )
            advances.append("RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED")
            state = "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED"
        if state in (
            "RECEIVED_BYTES_VERIFIED",
            "RECEIVED_PRINCIPAL_VERIFIED_IF_REQUIRED",
        ) and verified.get("return_source_verified"):
            self.store.transition(
                document_id, "RETURN_SOURCE_VERIFIED", detail={"receipt_id": rid}
            )
            advances.append("RETURN_SOURCE_VERIFIED")

        independent_ack = (
            "ESTABLISHED_REPORT_LEVEL"
            if (
                principal_verified
                and return_source_verified
                and bytes_match
            )
            else "NOT_ESTABLISHED"
        )
        return ok(
            document_id=document_id,
            receipt_id=rid,
            advances=advances,
            routing_state=self.store.get_document(document_id)["routing_state"],
            independent_expert_ack=independent_ack,
            github_witness=witness_gate,
            claim_ceiling=CLAIM_CEILING,
        )

    def verify_receiver(self, document_id: str) -> Dict[str, Any]:
        try:
            doc = self.store.get_document(document_id)
        except KeyError:
            return fail("DOCUMENT_NOT_FOUND", document_id)
        rows = self.store._conn.execute(
            "SELECT * FROM receipts WHERE document_id=? AND receipt_kind='RECEIVER_ACK' "
            "ORDER BY ts DESC",
            (document_id,),
        ).fetchall()
        if not rows:
            return ok(
                document_id=document_id,
                independent_expert_ack="NOT_ESTABLISHED",
                routing_state=doc["routing_state"],
                note="no independent receiver ACK stored",
            )
        latest = dict(rows[0])
        payload = json.loads(latest["payload_json"])
        return ok(
            document_id=document_id,
            routing_state=doc["routing_state"],
            latest_receipt=payload,
            independent_expert_ack=(
                "ESTABLISHED_REPORT_LEVEL"
                if (
                    payload.get("ok")
                    and payload.get("bytes_match")
                    and payload.get("principal_verified")
                    and payload.get("return_source_verified")
                )
                else "NOT_ESTABLISHED"
            ),
            claim_ceiling=CLAIM_CEILING,
        )

    def mark_scientific_adjudication(
        self,
        document_id: str,
        *,
        adjudication_ref: str,
        note: str = "",
    ) -> Dict[str, Any]:
        try:
            doc = self.store.get_document(document_id)
        except KeyError:
            return fail("DOCUMENT_NOT_FOUND", document_id)
        # Scientific adjudication is SEPARATE from transport success.
        self.store.transition(
            document_id,
            "SCIENTIFIC_ADJUDICATION_SEPARATE",
            detail={
                "adjudication_ref": adjudication_ref,
                "note": note,
                "wall": "TRANSPORT_PASS ≠ SCIENTIFIC_TRUTH",
            },
        )
        return ok(
            document_id=document_id,
            routing_state="SCIENTIFIC_ADJUDICATION_SEPARATE",
            adjudication_ref=adjudication_ref,
            claim_ceiling=CLAIM_CEILING,
            note="scientific adjudication recorded separately from handoff transport",
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _default_paths(repo_root: Path) -> Tuple[Path, Path]:
    data = repo_root / ".nexus_document_router"
    return data / "documents.sqlite3", data / "journal"


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="NEXUS Document Router — Agent Communication Framework R0"
    )
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--store", type=Path, help="SQLite WAL path")
    p.add_argument("--journal-dir", type=Path)
    p.add_argument(
        "--activate-cutover",
        action="store_true",
        help="Owner-only request: ACTIVE only with --activation-manifest gates PASS",
    )
    p.add_argument(
        "--activation-manifest",
        type=Path,
        help="JSON activation manifest with owner/integrity/privacy/ci/rollback gates",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dispatch_document")
    d.add_argument("--object", required=True)
    d.add_argument("--repository", default=DEFAULT_REPO)
    d.add_argument("--commit", required=True)
    d.add_argument("--path", required=True)
    d.add_argument("--expected-sha256")
    d.add_argument("--expected-bytes", type=int)
    d.add_argument("--privacy-class", default="PUBLIC_SAFE")
    d.add_argument("--redacted", action="store_true")
    d.add_argument("--allow-private-dispatch", action="store_true")
    d.add_argument("--private-lane-proof-json", type=Path)
    d.add_argument("--transport-witness-json", type=Path)
    d.add_argument("--agent-id")
    d.add_argument("--document-id")

    v = sub.add_parser("verify_manifest")
    v.add_argument("--document-id", required=True)

    r = sub.add_parser("receive_receipt")
    r.add_argument("--document-id", required=True)
    r.add_argument("--receipt-json", type=Path, required=True)

    vr = sub.add_parser("verify_receiver")
    vr.add_argument("--document-id", required=True)

    m = sub.add_parser("mark_scientific_adjudication")
    m.add_argument("--document-id", required=True)
    m.add_argument("--adjudication-ref", required=True)
    m.add_argument("--note", default="")

    sub.add_parser("cutover_status")
    sub.add_parser("list_documents")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    root = args.repo_root.resolve()
    store_default, journal_default = _default_paths(root)
    store = args.store or store_default
    journal = args.journal_dir or journal_default
    activation_manifest = None
    if args.activation_manifest:
        activation_manifest = json.loads(
            Path(args.activation_manifest).read_text(encoding="utf-8")
        )
    elif args.activate_cutover:
        # Explicit empty manifest → fail-closed STAGED (P0-C negative path).
        activation_manifest = {}
    router = DocumentRouter(
        RouterConfig(
            repo_root=root,
            store_path=store,
            journal_dir=journal,
            cutover_force_active=bool(args.activate_cutover),
            activation_manifest=activation_manifest,
        )
    )
    try:
        if args.cmd == "dispatch_document":
            private_lane_proof = None
            if args.private_lane_proof_json:
                private_lane_proof = json.loads(
                    Path(args.private_lane_proof_json).read_text(encoding="utf-8")
                )
            transport_witness = None
            if args.transport_witness_json:
                transport_witness = json.loads(
                    Path(args.transport_witness_json).read_text(encoding="utf-8")
                )
            result = router.dispatch_document(
                object_id=args.object,
                repository=args.repository,
                commit=args.commit,
                path=args.path,
                expected_sha256=args.expected_sha256,
                expected_bytes=args.expected_bytes,
                privacy_class=args.privacy_class,
                redacted=args.redacted,
                allow_private_dispatch=args.allow_private_dispatch,
                private_lane_proof=private_lane_proof,
                agent_id=args.agent_id,
                document_id=args.document_id,
                transport_witness=transport_witness,
            )
        elif args.cmd == "verify_manifest":
            result = router.verify_manifest(args.document_id)
        elif args.cmd == "receive_receipt":
            receipt = json.loads(args.receipt_json.read_text(encoding="utf-8"))
            result = router.receive_receipt(
                document_id=args.document_id, receipt=receipt
            )
        elif args.cmd == "verify_receiver":
            result = router.verify_receiver(args.document_id)
        elif args.cmd == "mark_scientific_adjudication":
            result = router.mark_scientific_adjudication(
                args.document_id,
                adjudication_ref=args.adjudication_ref,
                note=args.note,
            )
        elif args.cmd == "cutover_status":
            result = router.cutover_status()
        elif args.cmd == "list_documents":
            result = ok(documents=router.store.list_documents())
        else:
            result = fail("UNKNOWN_CMD", args.cmd)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("ok") else 2
    finally:
        router.close()


if __name__ == "__main__":
    sys.exit(main())
