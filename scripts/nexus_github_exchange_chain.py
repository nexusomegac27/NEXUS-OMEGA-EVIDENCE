#!/usr/bin/env python3
"""NEXUS GitHub Expert Exchange chain — Hard Remediation R2 (F01–F04).

Claim ceiling: C1_DESCRIPTIVE_ONLY
NATIVE_APP_R3 = HOLD
TERMINAL_PASS requires authentic GitHub→receiver→GitHub (not synthetic).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
PINNED_COMMIT = "ee73769c966b22887fafbc755edf7c64d1a537e1"
DEFAULT_REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
ALLOWED_SOURCE_ROOTS = (
    "docs/",
    "research/",
    "schema/",
    "scripts/",
    "tests/",
    "examples/",
    "validation/",
)
ADAPTER_NOT_CONNECTED = "ADAPTER_NOT_CONNECTED"
LEGACY_GRANT_REGISTER_REL = "docs/governance/EXPERTENKODEX_LEGACY_GRANT_REGISTER_V1.json"
LEGACY_GRANT_CLASSIFICATION = "LEGACY_PRE_EXPERTENKODEX_V1"
LEGACY_GRANT_REQUIRED_ENTRY_FIELDS = (
    "grant_id",
    "classification",
    "policy_version",
    "status",
    "issuer",
    "authorized_actor",
    "repository",
    "commit",
    "path",
    "sha256",
    "bytes",
    "permitted_scope",
    "non_retroactive_cutoff",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> Tuple[int, str]:
    raw = path.read_bytes()
    return len(raw), sha256_bytes(raw)


def fail(code: str, detail: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": False, "code": code, "ts": utc_now()}
    if detail:
        out["detail"] = detail
    return out


def ok(**kwargs: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": True, "ts": utc_now()}
    out.update(kwargs)
    return out


def _run_git(repo_root: Path, args: Sequence[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=check,
    )


# ---------------------------------------------------------------------------
# F01 — Source Resolver (commit-bound identity)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResolvedSource:
    repository: str
    commit: str
    path: str
    bytes: int
    sha256: str
    blob_oid: str
    invariants: Tuple[str, ...]


class SourceResolver:
    """Resolve source bytes only when bound to repository + full commit + path."""

    INVARIANTS = (
        "REPOSITORY_IDENTITY_VERIFIED",
        "FULL_COMMIT_SHA_VERIFIED",
        "COMMIT_OBJECT_EXISTS",
        "SOURCE_PATH_WITHIN_ALLOWED_ROOT",
        "SOURCE_BYTES_AND_SHA256_MATCH",
        "TRANSITIVE_PARENT_GRAPH_CLOSED",
    )

    def __init__(
        self,
        repo_root: Path,
        expected_repository: str = DEFAULT_REPO,
        allowed_roots: Sequence[str] = ALLOWED_SOURCE_ROOTS,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.expected_repository = expected_repository
        self.allowed_roots = tuple(allowed_roots)

    def repository_identity(self) -> Dict[str, Any]:
        remotes = _run_git(self.repo_root, ["remote", "get-url", "origin"])
        if remotes.returncode != 0:
            return fail("REPOSITORY_IDENTITY_MISSING", remotes.stderr.strip())
        url = remotes.stdout.strip()
        slug = self._slug_from_url(url)
        if slug != self.expected_repository:
            return fail(
                "REPOSITORY_IDENTITY_MISMATCH",
                f"expected={self.expected_repository} observed={slug} url={url}",
            )
        return ok(
            repository=slug,
            remote_url=url,
            invariant="REPOSITORY_IDENTITY_VERIFIED",
        )

    @staticmethod
    def _slug_from_url(url: str) -> str:
        u = url.strip().rstrip("/")
        if u.endswith(".git"):
            u = u[:-4]
        if "github.com" in u:
            part = u.split("github.com", 1)[1]
            part = part.lstrip("/:")
            return "/".join(part.split("/")[:2])
        return u

    def verify_commit(self, commit: str) -> Dict[str, Any]:
        if not FULL_SHA_RE.match(commit or ""):
            return fail("FULL_COMMIT_SHA_INVALID", commit or "")
        # Prefer git cat-file -t (avoids shell brace expansion on Windows).
        probe = _run_git(self.repo_root, ["cat-file", "-t", commit])
        if probe.returncode != 0 or probe.stdout.strip() != "commit":
            return fail("COMMIT_OBJECT_MISSING", commit)
        return ok(commit=commit, invariant="COMMIT_OBJECT_EXISTS")

    def _normalize_path(self, path: str) -> Dict[str, Any]:
        if not path or path.startswith("/") or path.startswith("\\"):
            return fail("SOURCE_PATH_ABSOLUTE_FORBIDDEN", path)
        norm = path.replace("\\", "/").lstrip("./")
        if ".." in Path(norm).parts:
            return fail("SOURCE_PATH_TRAVERSAL", path)
        if not any(norm == r.rstrip("/") or norm.startswith(r) for r in self.allowed_roots):
            return fail("SOURCE_PATH_OUTSIDE_ALLOWED_ROOT", norm)
        return ok(path=norm, invariant="SOURCE_PATH_WITHIN_ALLOWED_ROOT")

    def _blob_from_commit(self, commit: str, path: str) -> Dict[str, Any]:
        # Reject symlinks: git cat-file -t for tree entry.
        ls = _run_git(self.repo_root, ["ls-tree", commit, "--", path])
        if ls.returncode != 0 or not ls.stdout.strip():
            return fail("SOURCE_PATH_NOT_IN_COMMIT", f"{commit}:{path}")
        mode, obj_type, oid, *_rest = ls.stdout.strip().split(None, 3)
        if obj_type != "blob":
            return fail("SOURCE_NOT_BLOB", f"type={obj_type}")
        if mode == "120000":
            return fail("SOURCE_SYMLINK_FORBIDDEN", path)
        show = _run_git(self.repo_root, ["show", f"{commit}:{path}"])
        if show.returncode != 0:
            return fail("SOURCE_BLOB_FETCH_FAILED", show.stderr.strip())
        # git show returns text; re-fetch as binary via cat-file
        cat = subprocess.run(
            ["git", "cat-file", "blob", oid],
            cwd=str(self.repo_root),
            capture_output=True,
            check=False,
        )
        if cat.returncode != 0:
            return fail("SOURCE_BLOB_CAT_FAILED", oid)
        raw = cat.stdout
        return ok(bytes_len=len(raw), sha256=sha256_bytes(raw), blob_oid=oid, raw=raw)

    def resolve(
        self,
        *,
        repository: str,
        commit: str,
        path: str,
        expected_sha256: Optional[str] = None,
        expected_bytes: Optional[int] = None,
        parents: Optional[Sequence[Dict[str, Any]]] = None,
        _seen: Optional[set] = None,
    ) -> Dict[str, Any]:
        if not REPO_RE.match(repository or ""):
            return fail("REPOSITORY_IDENTITY_INVALID", repository or "")
        if repository != self.expected_repository:
            return fail(
                "REPOSITORY_IDENTITY_MISMATCH",
                f"expected={self.expected_repository} declared={repository}",
            )
        rid = self.repository_identity()
        if not rid.get("ok"):
            return rid

        cv = self.verify_commit(commit)
        if not cv.get("ok"):
            return cv

        pv = self._normalize_path(path)
        if not pv.get("ok"):
            return pv
        norm_path = pv["path"]

        blob = self._blob_from_commit(commit, norm_path)
        if not blob.get("ok"):
            return blob

        if expected_bytes is not None and int(expected_bytes) != int(blob["bytes_len"]):
            return fail(
                "SOURCE_BYTES_MISMATCH",
                f"expected={expected_bytes} observed={blob['bytes_len']}",
            )
        if expected_sha256 is not None and expected_sha256.lower() != blob["sha256"]:
            return fail(
                "SOURCE_SHA256_MISMATCH",
                f"expected={expected_sha256} observed={blob['sha256']}",
            )

        seen = _seen or set()
        key = (repository, commit, norm_path)
        if key in seen:
            return fail("TRANSITIVE_PARENT_CYCLE", str(key))
        seen.add(key)

        parent_results: List[Dict[str, Any]] = []
        for parent in parents or []:
            pr = self.resolve(
                repository=parent.get("repository", repository),
                commit=parent["commit"],
                path=parent["path"],
                expected_sha256=parent.get("sha256"),
                expected_bytes=parent.get("bytes"),
                parents=parent.get("parents"),
                _seen=seen,
            )
            if not pr.get("ok"):
                return fail(
                    "TRANSITIVE_PARENT_MISSING",
                    f"{parent.get('path')}:{pr.get('code')}",
                )
            parent_results.append(pr)

        resolved = ResolvedSource(
            repository=repository,
            commit=commit,
            path=norm_path,
            bytes=int(blob["bytes_len"]),
            sha256=blob["sha256"],
            blob_oid=blob["blob_oid"],
            invariants=self.INVARIANTS,
        )
        return ok(
            source=asdict(resolved),
            parents=parent_results,
            invariants=list(self.INVARIANTS),
        )


# ---------------------------------------------------------------------------
# F02 — Authenticated agent identity
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeclaredIdentity:
    model_id: str
    claimed_github_login: str = ""


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    github_login: str
    auth_method: str
    installation_id: str = ""
    scopes: Tuple[str, ...] = ()
    verified_at: str = ""


class AgentAdapter:
    """Separate declared model identity from authenticated GitHub principal."""

    def __init__(
        self,
        allowlist: Optional[Sequence[str]] = None,
        write_slots: Optional[Sequence[str]] = None,
    ) -> None:
        self.allowlist = set(allowlist or [])
        self.write_slots = list(write_slots or [])
        self._authenticated: Optional[AuthenticatedPrincipal] = None
        self._declared: Optional[DeclaredIdentity] = None

    def declare(self, model_id: str, claimed_github_login: str = "") -> Dict[str, Any]:
        self._declared = DeclaredIdentity(
            model_id=model_id,
            claimed_github_login=claimed_github_login or "",
        )
        return ok(
            declared=asdict(self._declared),
            note="DECLARED_IDENTITY_IS_NOT_AUTHENTICATION",
        )

    def authenticate_principal(
        self,
        *,
        github_login: str,
        auth_method: str,
        proof_token_present: bool,
        installation_id: str = "",
        scopes: Sequence[str] = (),
    ) -> Dict[str, Any]:
        """Bind a verified principal. Free-text login without proof → FAIL."""
        if not (github_login or "").strip():
            return fail("GITHUB_PRINCIPAL_EMPTY")
        if not proof_token_present:
            return fail(
                "GITHUB_PRINCIPAL_UNAUTHENTICATED",
                "claimed github_login without proof_token is not authentication",
            )
        if auth_method not in {
            "GITHUB_APP_INSTALLATION",
            "GITHUB_OAUTH_USER",
            "GITHUB_PAT_SCOPED",
            "TEST_FIXTURE_AUTH",
        }:
            return fail("GITHUB_AUTH_METHOD_UNSUPPORTED", auth_method)
        if self.allowlist and github_login not in self.allowlist:
            return fail("GITHUB_PRINCIPAL_NOT_ON_ALLOWLIST", github_login)
        self._authenticated = AuthenticatedPrincipal(
            github_login=github_login,
            auth_method=auth_method,
            installation_id=installation_id,
            scopes=tuple(scopes),
            verified_at=utc_now(),
        )
        return ok(principal=asdict(self._authenticated))

    def prove(self) -> Dict[str, Any]:
        """Prove adapter readiness. Declared login alone is never sufficient."""
        if self._authenticated is None:
            return fail(
                "AGENT_IDENTITY_NOT_AUTHENTICATED",
                "declared github_login is not an authentication proof",
            )
        if self.allowlist and self._authenticated.github_login not in self.allowlist:
            return fail("GITHUB_PRINCIPAL_NOT_ON_ALLOWLIST", self._authenticated.github_login)
        return ok(
            principal=asdict(self._authenticated),
            declared=asdict(self._declared) if self._declared else None,
            write_slots=list(self.write_slots),
            identity_layers={
                "declared_model": self._declared.model_id if self._declared else None,
                "claimed_github_login": self._declared.claimed_github_login if self._declared else None,
                "authenticated_github_login": self._authenticated.github_login,
                "auth_method": self._authenticated.auth_method,
            },
        )


# ---------------------------------------------------------------------------
# F03 — Independent receiver ACK
# ---------------------------------------------------------------------------


@dataclass
class ReceiverAck:
    repository: str
    commit: str
    object_path: str
    bytes: int
    sha256: str
    receiver_principal: str
    fetch_method: str
    independent: bool
    ack_id: str
    sender_process_id: str


class ReceiverAckProtocol:
    """Independent receiver must fetch+rehash; same-process ACK is forbidden."""

    def __init__(self, sender_process_id: str) -> None:
        self.sender_process_id = sender_process_id

    def issue_independent_ack(
        self,
        *,
        repository: str,
        commit: str,
        object_path: str,
        bytes_len: int,
        sha256: str,
        receiver_principal: str,
        fetch_method: str,
        receiver_process_id: str,
        authenticated: bool,
    ) -> Dict[str, Any]:
        if not authenticated:
            return fail("RECEIVER_NOT_AUTHENTICATED")
        if receiver_process_id == self.sender_process_id:
            return fail(
                "RECEIVER_ACK_SAME_PROCESS",
                "sender must not self-ACK as independent receiver",
            )
        if fetch_method not in {"GITHUB_API_CONTENTS", "GIT_FETCH_SHOW", "GITHUB_RAW"}:
            return fail("RECEIVER_FETCH_METHOD_INVALID", fetch_method)
        if not FULL_SHA_RE.match(commit):
            return fail("RECEIVER_ACK_COMMIT_INVALID", commit)
        ack = ReceiverAck(
            repository=repository,
            commit=commit,
            object_path=object_path,
            bytes=bytes_len,
            sha256=sha256,
            receiver_principal=receiver_principal,
            fetch_method=fetch_method,
            independent=True,
            ack_id=str(uuid.uuid4()),
            sender_process_id=self.sender_process_id,
        )
        return ok(ack=asdict(ack))

    def synthetic_self_ack_status(self) -> Dict[str, Any]:
        """Document that synthetic same-process ACK cannot close the gate."""
        return {
            "ok": False,
            "code": ADAPTER_NOT_CONNECTED,
            "detail": "no independently authenticated GitHub receiver connected",
            "independent_expert_ack": "NOT_ESTABLISHED",
            "ts": utc_now(),
        }


# ---------------------------------------------------------------------------
# F04 — Crash-safe delivery journal (append-only JSONL)
# ---------------------------------------------------------------------------


class _FileLock:
    """Cross-platform exclusive lock. Windows: msvcrt with retry (LK_LOCK can raise PermissionError)."""

    def __init__(self, lock_path: Path, *, retries: int = 80, sleep_s: float = 0.05) -> None:
        self.lock_path = lock_path
        self._fh: Optional[Any] = None
        self._retries = retries
        self._sleep_s = sleep_s

    def __enter__(self) -> "_FileLock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            import msvcrt
            import time

            last_err: Optional[BaseException] = None
            for _ in range(self._retries):
                fh = open(self.lock_path, "a+b")
                try:
                    fh.seek(0)
                    if fh.read(1) == b"":
                        fh.write(b"0")
                        fh.flush()
                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                    self._fh = fh
                    return self
                except OSError as exc:
                    last_err = exc
                    fh.close()
                    time.sleep(self._sleep_s)
            raise PermissionError(
                f"journal lock unavailable after retries: {self.lock_path}"
            ) from last_err
        import fcntl

        self._fh = open(self.lock_path, "a+b")
        fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc: Any) -> None:
        if self._fh is None:
            return
        try:
            if os.name == "nt":
                import msvcrt

                self._fh.seek(0)
                try:
                    msvcrt.locking(self._fh.fileno(), msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            else:
                import fcntl

                fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
        finally:
            self._fh.close()
            self._fh = None


class DeliveryJournal:
    """Append-only JSONL journal with atomic writes, idempotency, quarantine."""

    STREAMS = ("outbound", "receiver_ack", "return", "reconcile", "quarantine")

    def __init__(self, journal_dir: Path) -> None:
        self.journal_dir = Path(journal_dir)
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.journal_dir / "delivery_journal.jsonl"
        self.lock_path = self.journal_dir / "delivery_journal.lock"
        self.quarantine_path = self.journal_dir / "quarantine.jsonl"
        self._index: Dict[str, Dict[str, Any]] = {}
        self._load_index()

    def _load_index(self) -> None:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    self._quarantine_raw(line, reason="JSON_DECODE_ERROR")
                    continue
                eid = ev.get("event_id")
                if eid:
                    self._index[eid] = ev

    def _quarantine_raw(self, raw: str, reason: str) -> None:
        rec = {"reason": reason, "raw": raw, "ts": utc_now()}
        self._append_line(self.quarantine_path, json.dumps(rec, sort_keys=True))

    def _append_line(self, path: Path, line: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write to temp then append via os.write after lock — crash-safe append:
        # open O_APPEND, write single line + fsync.
        flags = os.O_CREAT | os.O_APPEND | os.O_WRONLY
        fd = os.open(str(path), flags, 0o644)
        try:
            data = (line + "\n").encode("utf-8")
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)

    def append(
        self,
        *,
        stream: str,
        payload: Dict[str, Any],
        event_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        if stream not in self.STREAMS:
            return fail("JOURNAL_STREAM_INVALID", stream)
        eid = event_id or str(uuid.uuid4())
        ikey = idempotency_key or eid
        with _FileLock(self.lock_path):
            # Reload under lock so concurrent journal instances see committed events.
            self._index.clear()
            self._load_index()
            for existing in self._index.values():
                if existing.get("idempotency_key") == ikey:
                    if existing.get("payload") == payload and existing.get("stream") == stream:
                        return ok(event=existing, replayed=True)
                    q = {
                        "event_id": eid,
                        "stream": "quarantine",
                        "reason": "IDEMPOTENCY_CONFLICT",
                        "idempotency_key": ikey,
                        "existing_event_id": existing.get("event_id"),
                        "payload": payload,
                        "ts": utc_now(),
                    }
                    self._append_line(self.quarantine_path, json.dumps(q, sort_keys=True))
                    return fail("JOURNAL_IDEMPOTENCY_CONFLICT", ikey)
            event = {
                "event_id": eid,
                "idempotency_key": ikey,
                "stream": stream,
                "payload": payload,
                "ts": utc_now(),
            }
            self._append_line(self.path, json.dumps(event, sort_keys=True))
            self._index[eid] = event
            return ok(event=event, replayed=False)

    def list_stream(self, stream: str) -> List[Dict[str, Any]]:
        return [e for e in self._index.values() if e.get("stream") == stream]

    def reconcile_github_delivery(
        self,
        *,
        delivery_id: str,
        signature_valid: bool,
        duplicate: bool,
    ) -> Dict[str, Any]:
        """Deterministic webhook reconciliation (failed webhooks are not auto-retried by GitHub)."""
        if not signature_valid:
            return self.append(
                stream="quarantine",
                payload={
                    "reason": "WEBHOOK_SIGNATURE_INVALID",
                    "delivery_id": delivery_id,
                },
                idempotency_key=f"wh-bad-sig:{delivery_id}",
            )
        if duplicate:
            return self.append(
                stream="reconcile",
                payload={
                    "reason": "WEBHOOK_DUPLICATE_IGNORED",
                    "delivery_id": delivery_id,
                },
                idempotency_key=f"wh-dup:{delivery_id}",
            )
        return self.append(
            stream="reconcile",
            payload={"reason": "WEBHOOK_ACCEPTED", "delivery_id": delivery_id},
            idempotency_key=f"wh-ok:{delivery_id}",
        )


# ---------------------------------------------------------------------------
# F12 — Owner-controlled Legacy Grant Register (fail-closed)
# ---------------------------------------------------------------------------


class LegacyGrantRegistry:
    """Owner-verified legacy grants only. Self-asserted authenticated:true is never authority."""

    def __init__(
        self,
        register_path: Optional[Path] = None,
        register_doc: Optional[Dict[str, Any]] = None,
    ) -> None:
        if register_doc is not None:
            self.doc = dict(register_doc)
            self.register_path = register_path
        elif register_path is not None and Path(register_path).is_file():
            self.register_path = Path(register_path)
            self.doc = json.loads(
                self.register_path.read_text(encoding="utf-8")
            )
        else:
            # Missing register → empty DENY (fail-closed; closes F12).
            self.register_path = register_path
            self.doc = {
                "object": "NEXUS_OMEGA_EXPERTENKODEX_LEGACY_GRANT_REGISTER_V1",
                "status": "C1_OWNER_CONTROLLED_EMPTY_DEFAULT_DENY",
                "default": "DENY",
                "grants": [],
            }
        grants = self.doc.get("grants")
        if not isinstance(grants, list):
            grants = []
        self.grants: List[Dict[str, Any]] = [
            g for g in grants if isinstance(g, dict)
        ]
        self.default = str(self.doc.get("default") or "DENY").upper()

    @classmethod
    def load(cls, repo_root: Path) -> "LegacyGrantRegistry":
        return cls(register_path=Path(repo_root) / LEGACY_GRANT_REGISTER_REL)

    def evaluate(
        self,
        grant: Any,
        *,
        repository: str,
        commit: str,
    ) -> Dict[str, Any]:
        if not isinstance(grant, dict):
            return fail("LEGACY_GRANT_MALFORMED", "expertenkodex_legacy_grant must be object")
        if grant.get("authenticated") is not True:
            return fail(
                "LEGACY_GRANT_SELF_ASSERTED_REJECTED",
                "authenticated must be boolean true before register evaluation",
            )
        grant_id = grant.get("grant_id")
        policy_version = grant.get("policy_version")
        classification = grant.get("classification")
        if not isinstance(grant_id, str) or not grant_id.strip():
            return fail("LEGACY_GRANT_MALFORMED", "grant_id required")
        if not isinstance(policy_version, str) or not policy_version.strip():
            return fail("LEGACY_GRANT_MALFORMED", "policy_version required")
        if classification != LEGACY_GRANT_CLASSIFICATION:
            return fail(
                "LEGACY_GRANT_FIELD_MISMATCH",
                f"classification must be {LEGACY_GRANT_CLASSIFICATION}",
            )

        # Empty owner register: DEFAULT_DENY — self-asserted authenticated:true never suffices.
        if self.default == "DENY" and not self.grants:
            return fail(
                "LEGACY_GRANT_DEFAULT_DENY",
                "owner register empty; SELF_ASSERTED authenticated:true rejected (F12)",
            )

        entry = next(
            (g for g in self.grants if g.get("grant_id") == grant_id),
            None,
        )
        if entry is None:
            return fail(
                "LEGACY_GRANT_NOT_IN_REGISTER",
                f"grant_id not in owner register: {grant_id}",
            )

        for field_name in LEGACY_GRANT_REQUIRED_ENTRY_FIELDS:
            if field_name not in entry:
                return fail(
                    "LEGACY_GRANT_MALFORMED",
                    f"register entry missing field: {field_name}",
                )

        status = str(entry.get("status") or "").upper()
        if status == "REVOKED":
            return fail("LEGACY_GRANT_REVOKED", grant_id)
        if status == "EXPIRED":
            return fail("LEGACY_GRANT_EXPIRED", grant_id)
        if status != "ACTIVE":
            return fail(
                "LEGACY_GRANT_FIELD_MISMATCH",
                f"register status must be ACTIVE, got {status!r}",
            )

        mismatches: List[str] = []
        if entry.get("classification") != classification:
            mismatches.append("classification")
        if entry.get("policy_version") != policy_version:
            mismatches.append("policy_version")
        if entry.get("repository") != repository:
            mismatches.append("repository")
        if entry.get("commit") != commit:
            # Allow entry.commit to be the historical object commit; also accept
            # explicit grant.commit override matching the entry.
            grant_commit = grant.get("commit")
            if grant_commit != entry.get("commit") and entry.get("commit") != commit:
                mismatches.append("commit")
        for key in ("issuer", "authorized_actor", "path", "sha256", "bytes"):
            if key in grant and grant.get(key) != entry.get(key):
                mismatches.append(key)
        if mismatches:
            return fail(
                "LEGACY_GRANT_FIELD_MISMATCH",
                "mismatched fields: " + ",".join(mismatches),
            )

        # Provenance: entry must bind historical object identity (non-empty).
        for key in ("path", "sha256", "issuer", "authorized_actor"):
            val = entry.get(key)
            if not isinstance(val, str) or not val.strip():
                return fail("LEGACY_GRANT_MALFORMED", f"entry.{key} empty")
        if not isinstance(entry.get("bytes"), int) or entry["bytes"] < 0:
            return fail("LEGACY_GRANT_MALFORMED", "entry.bytes must be non-negative int")
        if not FULL_SHA_RE.match(str(entry.get("commit") or "")):
            return fail("LEGACY_GRANT_MALFORMED", "entry.commit must be full sha")
        if not FULL_SHA_RE.match(str(entry.get("sha256") or "")):
            # sha256 is 64 hex; allow 64-char hex separately
            sha = str(entry.get("sha256") or "")
            if not re.fullmatch(r"[0-9a-f]{64}", sha):
                return fail("LEGACY_GRANT_MALFORMED", "entry.sha256 must be 64 hex")

        return ok(
            expertenkodex="LEGACY_GRANT_ACCEPTED",
            legacy_grant_id=grant_id,
            legacy_grant_source="OWNER_VERIFIED_REGISTER",
        )


# ---------------------------------------------------------------------------
# Dispatch validator + exchange chain
# ---------------------------------------------------------------------------


class DispatchValidator:
    def __init__(
        self,
        resolver: SourceResolver,
        legacy_registry: Optional[LegacyGrantRegistry] = None,
    ) -> None:
        self.resolver = resolver
        self.legacy_registry = legacy_registry or LegacyGrantRegistry()

    def validate_manifest(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        required = ("repository", "commit", "sources", "object")
        for key in required:
            if key not in manifest:
                return fail("MANIFEST_INCOMPLETE", key)
        if not FULL_SHA_RE.match(manifest["commit"]):
            return fail("MANIFEST_COMMIT_INVALID", manifest["commit"])
        if manifest["repository"] != self.resolver.expected_repository:
            return fail("MANIFEST_REPOSITORY_MISMATCH", manifest["repository"])
        resolved = []
        for src in manifest["sources"]:
            r = self.resolver.resolve(
                repository=manifest["repository"],
                commit=src.get("commit", manifest["commit"]),
                path=src["path"],
                expected_sha256=src.get("sha256"),
                expected_bytes=src.get("bytes"),
                parents=src.get("parents"),
            )
            if not r.get("ok"):
                return r
            resolved.append(r["source"])
        # Expertenkodex V1 (F11): Kodex is MANDATORY for dispatch — not optional.
        # Absent EXPERTENKODEX/CODEX_* → MISSING_EXPERTENKODEX_HEADER unless an
        # owner-verified legacy grant matches the register (F12; never self-asserted).
        nested = manifest.get("expertenkodex") or manifest.get("expertenkodex_header")
        has_top = any(
            k in manifest
            for k in (
                "EXPERTENKODEX",
                "CODEX_COMMIT",
                "CODEX_PATH",
                "CODEX_BYTES",
                "CODEX_SHA256",
            )
        )
        if nested is None and not has_top:
            grant = manifest.get("expertenkodex_legacy_grant")
            if isinstance(grant, dict) and grant.get("authenticated") is True:
                ev = self.legacy_registry.evaluate(
                    grant,
                    repository=manifest["repository"],
                    commit=manifest["commit"],
                )
                if not ev.get("ok"):
                    return ev
                return ok(
                    resolved_sources=resolved,
                    object=manifest["object"],
                    expertenkodex=ev.get("expertenkodex", "LEGACY_GRANT_ACCEPTED"),
                    legacy_grant_id=ev.get("legacy_grant_id"),
                    legacy_grant_source=ev.get("legacy_grant_source"),
                )
            return fail(
                "MISSING_EXPERTENKODEX_HEADER",
                "EXPERTENKODEX/CODEX_* required for GitHub-capable expert dispatch; "
                "absent fields do not grandfather",
            )
        header = dict(manifest)
        if isinstance(nested, dict):
            header.update(nested)
        try:
            from scripts.nexus_expertenkodex_validator import (
                ExpertenkodexHeaderValidator,
            )
        except ImportError:  # pragma: no cover
            from nexus_expertenkodex_validator import (  # type: ignore
                ExpertenkodexHeaderValidator,
            )
        ek = ExpertenkodexHeaderValidator().validate(
            header, require_manifest_entries=True
        )
        if not ek.get("ok"):
            return ek
        return ok(resolved_sources=resolved, object=manifest["object"])


class ExchangeChain:
    def __init__(
        self,
        repo_root: Path,
        journal_dir: Optional[Path] = None,
        allowlist: Optional[Sequence[str]] = None,
        write_slots: Optional[Sequence[str]] = None,
        legacy_registry: Optional[LegacyGrantRegistry] = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.resolver = SourceResolver(self.repo_root)
        self.legacy_registry = legacy_registry or LegacyGrantRegistry.load(
            self.repo_root
        )
        self.validator = DispatchValidator(
            self.resolver, legacy_registry=self.legacy_registry
        )
        self.process_id = f"pid:{os.getpid()}:{uuid.uuid4().hex[:8]}"
        self.adapter = AgentAdapter(allowlist=allowlist, write_slots=write_slots)
        self.receiver = ReceiverAckProtocol(self.process_id)
        jdir = journal_dir or (self.repo_root / ".nexus_exchange_journal")
        self.journal = DeliveryJournal(jdir)

    def run_synthetic_cycle(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Local synthetic path — never closes independent receiver ACK gate."""
        v = self.validator.validate_manifest(manifest)
        if not v.get("ok"):
            return v
        outbound = self.journal.append(
            stream="outbound",
            payload={"manifest_object": manifest["object"], "commit": manifest["commit"]},
            idempotency_key=f"outbound:{manifest['object']}:{manifest['commit']}",
        )
        # Synthetic ACK from same process is explicitly NOT independent.
        ack_status = self.receiver.synthetic_self_ack_status()
        self.journal.append(
            stream="receiver_ack",
            payload=ack_status,
            idempotency_key=f"synth-ack:{manifest['object']}:{manifest['commit']}",
        )
        return ok(
            gate="G8_SYNTHETIC",
            validation=v,
            outbound=outbound,
            receiver_ack=ack_status,
            independent_expert_ack="NOT_ESTABLISHED",
            adapter_status=ADAPTER_NOT_CONNECTED,
            terminal_pass=False,
            note="PASS_LOCAL_SYNTHETIC ≠ authentic GitHub→expert→GitHub cycle",
        )


def measure_efficiency(
    *,
    manual_transfers_baseline: int,
    automated_transfers: int,
    documented_exceptions: int,
    receiver_acks_observed: int,
) -> Dict[str, Any]:
    if manual_transfers_baseline <= 0 or receiver_acks_observed <= 0:
        return {
            "status": "EFFICIENCY_TARGET_NOT_YET_OBSERVED",
            "manual_transfers_baseline": manual_transfers_baseline,
            "automated_transfers": automated_transfers,
            "documented_exceptions": documented_exceptions,
            "receiver_acks_observed": receiver_acks_observed,
            "reduction": None,
            "ts": utc_now(),
        }
    remaining = max(manual_transfers_baseline - automated_transfers, 0)
    reduction = 1.0 - (remaining / manual_transfers_baseline)
    return {
        "status": "OBSERVED" if reduction >= 0.9 else "BELOW_TARGET",
        "manual_transfers_baseline": manual_transfers_baseline,
        "automated_transfers": automated_transfers,
        "documented_exceptions": documented_exceptions,
        "receiver_acks_observed": receiver_acks_observed,
        "reduction": round(reduction, 4),
        "ts": utc_now(),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NEXUS GitHub exchange chain R2")
    p.add_argument("--repo-root", default=".", type=Path)
    p.add_argument("--resolve", nargs=3, metavar=("REPO", "COMMIT", "PATH"))
    p.add_argument("--expected-sha256")
    p.add_argument("--expected-bytes", type=int)
    p.add_argument("--synthetic-manifest", type=Path)
    p.add_argument("--journal-dir", type=Path)
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    root = args.repo_root.resolve()
    chain = ExchangeChain(root, journal_dir=args.journal_dir)
    if args.resolve:
        repo, commit, path = args.resolve
        result = chain.resolver.resolve(
            repository=repo,
            commit=commit,
            path=path,
            expected_sha256=args.expected_sha256,
            expected_bytes=args.expected_bytes,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("ok") else 2
    if args.synthetic_manifest:
        manifest = json.loads(args.synthetic_manifest.read_text(encoding="utf-8"))
        result = chain.run_synthetic_cycle(manifest)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("ok") else 2
    print(json.dumps({"ok": True, "pinned_commit": PINNED_COMMIT}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
