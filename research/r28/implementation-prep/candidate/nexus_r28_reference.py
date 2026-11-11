#!/usr/bin/env python3
"""NEXUS OMEGA R28 pre-integration reference candidate.

Implements local deterministic primitives only:
- NEXUS_CAPABILITY_CHALLENGE_V1.1 issue/verify
- NEXUS_REAL_HANDSHAKE_V1 local manifest/receipt verify
- provider-neutral transport protocol with local-directory test backend

Not implemented: online backend, signing, authorization, SCITT/KERI, deployment,
node activation, architecture finalization, scientific claim promotion.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import mimetypes
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

REQUIRED_CHALLENGE_FILES = (
    "challenge.txt", "payload.bin", "manifest.sha256", "expected_receipt.json"
)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

def deterministic_bytes(seed: str, n: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < n:
        out.extend(hashlib.sha256(f"{seed}:{counter}".encode()).digest())
        counter += 1
    return bytes(out[:n])

def _parse_sha_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ValueError("invalid manifest line")
        digest, name = parts
        name = name.lstrip("*")
        if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
            raise ValueError("invalid sha256")
        result[name] = digest.lower()
    return result

def _challenge_id(bundle: Path) -> str:
    for line in (bundle / "challenge.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("challenge_id="):
            return line.split("=", 1)[1]
    raise ValueError("challenge_id missing")

def issue_capability_challenge(
    out: Path,
    issuer_id: str,
    payload_size: int = 1024,
    challenge_id: str | None = None,
    seed: str | None = None,
) -> dict:
    out.mkdir(parents=True, exist_ok=False)
    challenge_id = challenge_id or f"NEXUS-{secrets.token_hex(12)}"
    payload = (
        deterministic_bytes(seed, payload_size)
        if seed is not None
        else secrets.token_bytes(payload_size)
    )
    challenge = (
        "NEXUS_CAPABILITY_CHALLENGE_V1.1\n"
        f"challenge_id={challenge_id}\n"
        f"issuer={issuer_id}\n"
        f"created_at_utc={utc_now()}\n"
        "steps=READ_BYTES,HASH_SHA256,VERIFY_MANIFEST,RETURN_RECEIPT,REPORT_SUBSTRATE\n"
        "rule=DECLARED_CAPABILITY!=MEASURED_CAPABILITY\n"
    ).encode("utf-8")
    (out / "payload.bin").write_bytes(payload)
    (out / "challenge.txt").write_bytes(challenge)
    (out / "manifest.sha256").write_text(
        f"{sha256_bytes(payload)}  payload.bin\n"
        f"{sha256_bytes(challenge)}  challenge.txt\n",
        encoding="utf-8",
    )
    expected = {
        "receipt_type": "NEXUS_CAPABILITY_CHALLENGE_V1.1",
        "challenge_id": challenge_id,
        "issuer": issuer_id,
        "required_fields": [
            "agent_id", "payload_size_bytes", "payload_sha256",
            "manifest_match", "method", "test_vector_status",
            "C1_byte_access", "C2_sha256_computation", "C3_verification",
            "C4_response_format", "C5_integrity", "substrate_profile",
            "timestamp_utc", "issuer"
        ],
        "note": "Expected values are bound in the bundle; agent memory is not a source.",
    }
    (out / "expected_receipt.json").write_text(
        json.dumps(expected, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return verify_capability_bundle(out)

def verify_capability_bundle(bundle: Path) -> dict:
    missing = [f for f in REQUIRED_CHALLENGE_FILES if not (bundle / f).is_file()]
    if missing:
        return {"status": "FAIL", "reason": "MISSING_FILES", "missing": missing}
    manifest = _parse_sha_manifest(bundle / "manifest.sha256")
    checks = {}
    for name in ("payload.bin", "challenge.txt"):
        computed = sha256_file(bundle / name)
        expected = manifest.get(name)
        checks[name] = {
            "expected": expected,
            "computed": computed,
            "match": computed == expected,
        }
    return {
        "status": "PASS" if all(v["match"] for v in checks.values()) else "FAIL",
        "checks": checks,
        "payload_size_bytes": (bundle / "payload.bin").stat().st_size,
        "challenge_id": _challenge_id(bundle),
    }

def make_capability_receipt(
    bundle: Path,
    agent_id: str,
    substrate_profile: str,
    issuer: str,
    method: str = "python-hashlib-sha256",
) -> dict:
    v = verify_capability_bundle(bundle)
    ok = v["status"] == "PASS"
    return {
        "receipt_type": "NEXUS_CAPABILITY_CHALLENGE_V1.1",
        "challenge_id": _challenge_id(bundle),
        "agent_id": agent_id,
        "payload_size_bytes": (bundle / "payload.bin").stat().st_size,
        "payload_sha256": sha256_file(bundle / "payload.bin"),
        "manifest_match": ok,
        "method": method,
        "test_vector_status": "PASS" if ok else "FAIL",
        "C1_byte_access": "YES",
        "C2_sha256_computation": "YES",
        "C3_verification": "YES" if ok else "NO",
        "C4_response_format": "YES",
        "C5_integrity": "YES" if ok else "NO",
        "substrate_profile": substrate_profile,
        "timestamp_utc": utc_now(),
        "issuer": issuer,
    }

def verify_capability_receipt(bundle: Path, receipt: dict) -> dict:
    b = verify_capability_bundle(bundle)
    if b["status"] != "PASS":
        return {"status": "FAIL", "reason": "BUNDLE_INVALID", "bundle": b}
    required = {
        "receipt_type", "challenge_id", "agent_id", "payload_size_bytes",
        "payload_sha256", "manifest_match", "method", "test_vector_status",
        "C1_byte_access", "C2_sha256_computation", "C3_verification",
        "C4_response_format", "C5_integrity", "substrate_profile",
        "timestamp_utc", "issuer",
    }
    missing = sorted(required - receipt.keys())
    checks = {
        "required_fields": not missing,
        "receipt_type": receipt.get("receipt_type") == "NEXUS_CAPABILITY_CHALLENGE_V1.1",
        "challenge_id": receipt.get("challenge_id") == _challenge_id(bundle),
        "payload_size": receipt.get("payload_size_bytes") == (bundle / "payload.bin").stat().st_size,
        "payload_sha256": receipt.get("payload_sha256") == sha256_file(bundle / "payload.bin"),
        "manifest_match": receipt.get("manifest_match") is True,
        "test_vector_status": receipt.get("test_vector_status") == "PASS",
        "capabilities_yes": all(
            receipt.get(k) == "YES"
            for k in (
                "C1_byte_access", "C2_sha256_computation", "C3_verification",
                "C4_response_format", "C5_integrity"
            )
        ),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
    }

def _manifest_digest(core: dict) -> str:
    return hashlib.sha256(canonical_bytes(core)).hexdigest()

def build_handshake_manifest(
    artifact: Path,
    object_id: str,
    issuer: str,
    media_type: str | None = None,
    challenge_id: str | None = None,
) -> dict:
    core = {
        "schema_version": "1.0.0",
        "object_id": object_id,
        "size_bytes": artifact.stat().st_size,
        "sha256": sha256_file(artifact),
        "media_type": media_type
        or mimetypes.guess_type(str(artifact))[0]
        or "application/octet-stream",
        "issuer": issuer,
        "created_at_utc": utc_now(),
        "challenge_id": challenge_id or f"NEXUS-HS-{secrets.token_hex(12)}",
    }
    return {**core, "manifest_digest": _manifest_digest(core)}

def validate_handshake_manifest(manifest: dict) -> bool:
    digest = manifest.get("manifest_digest")
    core = {k: v for k, v in manifest.items() if k != "manifest_digest"}
    return isinstance(digest, str) and digest == _manifest_digest(core)

def receive_artifact(
    artifact: Path,
    manifest: dict,
    receiver_id: str,
    method: str = "python-hashlib-sha256",
) -> dict:
    computed = sha256_file(artifact)
    size = artifact.stat().st_size
    matches = (
        validate_handshake_manifest(manifest)
        and size == manifest.get("size_bytes")
        and computed == manifest.get("sha256")
    )
    return {
        "receipt_type": "NEXUS_REAL_HANDSHAKE_V1_RECEIPT",
        "object_id": manifest.get("object_id"),
        "challenge_id": manifest.get("challenge_id"),
        "manifest_digest": manifest.get("manifest_digest"),
        "received_size": size,
        "computed_sha256": computed,
        "manifest_match": matches,
        "method": method,
        "receiver_id": receiver_id,
        "timestamp_utc": utc_now(),
        "status": "PASS" if matches else "FAIL",
    }

def verify_handshake_receipt(manifest: dict, receipt: dict) -> dict:
    checks = {
        "manifest_self_consistent": validate_handshake_manifest(manifest),
        "object_id": receipt.get("object_id") == manifest.get("object_id"),
        "challenge_id": receipt.get("challenge_id") == manifest.get("challenge_id"),
        "manifest_digest": receipt.get("manifest_digest") == manifest.get("manifest_digest"),
        "size": receipt.get("received_size") == manifest.get("size_bytes"),
        "sha256": receipt.get("computed_sha256") == manifest.get("sha256"),
        "manifest_match": receipt.get("manifest_match") is True,
        "status": receipt.get("status") == "PASS",
        "receiver_present": bool(receipt.get("receiver_id")),
    }
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}

class Transport(Protocol):
    def put(self, source: Path, object_name: str) -> str: ...
    def get(self, ref: str, destination: Path) -> Path: ...

class LocalDirectoryTransport:
    """Deterministic test double for the transport boundary; not an online backend."""
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, source: Path, object_name: str) -> str:
        target = self.root / object_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return object_name

    def get(self, ref: str, destination: Path) -> Path:
        source = self.root / ref
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        return destination

def local_handshake(
    source: Path,
    transport: Transport,
    workdir: Path,
    object_id: str,
    sender_id: str,
    receiver_id: str,
) -> dict:
    workdir.mkdir(parents=True, exist_ok=True)
    manifest = build_handshake_manifest(source, object_id, sender_id)
    ref = transport.put(source, f"{manifest['sha256']}.bin")
    received = transport.get(ref, workdir / "received.bin")
    receipt = receive_artifact(received, manifest, receiver_id)
    sender_verification = verify_handshake_receipt(manifest, receipt)
    return {
        "manifest": manifest,
        "transport_ref": ref,
        "receipt": receipt,
        "sender_verification": sender_verification,
        "real_online_handshake": False,
        "scope": "LOCAL_TRANSPORT_TEST_DOUBLE_ONLY",
    }

def _print(obj: dict) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("issue-capability")
    a.add_argument("out")
    a.add_argument("--issuer", required=True)
    a.add_argument("--seed")
    a.add_argument("--size", type=int, default=1024)
    b = sub.add_parser("verify-capability")
    b.add_argument("bundle")
    c = sub.add_parser("manifest")
    c.add_argument("artifact")
    c.add_argument("--object-id", required=True)
    c.add_argument("--issuer", required=True)

    args = parser.parse_args()
    if args.cmd == "issue-capability":
        _print(issue_capability_challenge(Path(args.out), args.issuer, args.size, seed=args.seed))
    elif args.cmd == "verify-capability":
        _print(verify_capability_bundle(Path(args.bundle)))
    elif args.cmd == "manifest":
        _print(build_handshake_manifest(Path(args.artifact), args.object_id, args.issuer))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
