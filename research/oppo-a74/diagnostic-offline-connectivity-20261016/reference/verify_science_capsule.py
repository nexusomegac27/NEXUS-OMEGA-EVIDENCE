#!/usr/bin/env python3
"""NEXUS OMEGA C1 scientific capsule LOCAL byte verifier.

A successful local SHA-256 comparison is NOT remote delivery,
privacy certification, scientific validity, or an AXIOM receiver ACK.
No network access or device actions.
"""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_PRIVACY = frozenset({"PRIVATE_ORIGINAL", "PRIVATE_ANALYSIS", "ENCRYPTED_PRIVATE", "PUBLIC_SAFE"})
_ROLES = frozenset({
    "SENSOR_ORIGINAL", "SESSION_CONFIG", "CAPTURE_METADATA", "ANALYSIS_SCRIPT",
    "TEST_LOG", "NEGATIVE_CONTROL", "STATISTICS", "ESTIMATOR_STATE",
    "NULL_MODEL", "ENVIRONMENT_LOCK", "SHELL_STDOUT", "SHELL_STDERR",
    "CHAIN_RECEIPT", "SCIENTIFIC_REPORT", "SOURCE_REGISTER", "OTHER_SCIENCE",
})

class CapsuleError(Exception):
    pass

def _strict_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise CapsuleError(f"DUPLICATE_JSON_KEY:{k}")
        d[k] = v
    return d

def _manifest(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"),
            object_pairs_hook=_strict_pairs,
            parse_constant=lambda x: (_ for _ in ()).throw(CapsuleError("NONFINITE_JSON")))
    except (OSError, UnicodeError, json.JSONDecodeError) as e:
        raise CapsuleError(f"MANIFEST_PARSE:{e}") from e

def _path(raw):
    if not isinstance(raw, str) or not raw or "\\" in raw or "\x00" in raw:
        raise CapsuleError("INVALID_RELATIVE_PATH")
    p = PurePosixPath(raw)
    if p.is_absolute() or any(s in (".", "..", "") for s in raw.split("/")) or ":" in p.parts[0]:
        raise CapsuleError("PATH_TRAVERSAL_OR_NONCANONICAL")
    return p

def _regular(root, rel):
    cur = root
    for part in rel.parts:
        cur = cur / part
        if cur.is_symlink():
            raise CapsuleError(f"SYMLINK_FORBIDDEN:{rel}")
    if not cur.is_file() or not cur.resolve().is_relative_to(root.resolve()):
        raise CapsuleError(f"ORIGINAL_BYTES_MISSING_OR_ESCAPE:{rel}")
    if not stat.S_ISREG(cur.stat().st_mode):
        raise CapsuleError(f"NOT_REGULAR_FILE:{rel}")
    return cur

def _digest(file):
    h = hashlib.sha256()
    n = 0
    with file.open("rb") as f:
        first = f.read(128)
        if first.startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise CapsuleError("LFS_POINTER_NOT_ORIGINAL_BYTES")
        h.update(first)
        n += len(first)
        while True:
            block = f.read(1024 * 1024)
            if not block: break
            h.update(block)
            n += len(block)
    return n, h.hexdigest()

def verify(root, manifest_path, public=False):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise CapsuleError("ROOT_NOT_DIRECTORY")
    m = _manifest(manifest_path)
    if not isinstance(m, dict) or m.get("schema") != "nexus-science-capsule/v1":
        raise CapsuleError("UNSUPPORTED_SCHEMA")
    if not isinstance(m.get("capsule_id"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]{8,120}", m["capsule_id"]):
        raise CapsuleError("CAPSULE_ID_INVALID")
    entries = m.get("files")
    if not isinstance(entries, list) or not entries or len(entries) > 10000:
        raise CapsuleError("FILES_UNBOUNDED_OR_EMPTY")
    mp = Path(manifest_path).resolve()
    mr = mp.relative_to(root).as_posix() if mp.is_relative_to(root) else None
    visited, out = set(), []
    for e in entries:
        if not isinstance(e, dict):
            raise CapsuleError("FILE_ENTRY_NOT_OBJECT")
        rel = _path(e.get("relative_path"))
        name = rel.as_posix()
        if name == mr:
            raise CapsuleError("MANIFEST_SELF_HASH_FORBIDDEN")
        if name in visited:
            raise CapsuleError("DUPLICATE_FILE_PATH")
        visited.add(name)
        if e.get("role") not in _ROLES or e.get("privacy_class") not in _PRIVACY:
            raise CapsuleError(f"ROLE_OR_PRIVACY_INVALID:{name}")
        if public and e["privacy_class"] != "PUBLIC_SAFE":
            raise CapsuleError(f"PRIVATE_FILE_IN_PUBLIC_CAPSULE:{name}")
        size, sha = e.get("bytes"), e.get("sha256")
        if type(size) is not int or size < 0 or not isinstance(sha, str) or not _SHA256.fullmatch(sha):
            raise CapsuleError("INVALID_EXPECTED_HASH_OR_SIZE")
        file = _regular(root, rel)
        actual_size, actual_hash = _digest(file)
        if (actual_size, actual_hash) != (size, sha):
            raise CapsuleError(f"SOURCE_BYTE_MISMATCH:{name}")
        out.append({"path": name, "bytes": size, "sha256": sha, "role": e["role"]})
    return {"capsule_id": m["capsule_id"], "count": len(out),
            "verdict": "LOCAL_ORIGINAL_BYTES_MATCH_ONLY",
            "receiver_ack": "NOT_ESTABLISHED",
            "remote_readback": "NOT_ESTABLISHED",
            "scientific_validation": "NOT_ESTABLISHED",
            "files": out}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--public", action="store_true")
    a = p.parse_args()
    try:
        print(json.dumps(verify(a.root, a.manifest, a.public), sort_keys=True))
    except (CapsuleError, OSError, ValueError) as e:
        print("HOLD_C1_CAPSULE_VERIFY:" + str(e), file=sys.stderr)
        sys.exit(1)
