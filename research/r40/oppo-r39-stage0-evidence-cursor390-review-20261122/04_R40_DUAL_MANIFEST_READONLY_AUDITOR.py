#!/usr/bin/env python3
"""Read-only GitHub-native-vs-original Windows CRLF manifest auditor (stdlib).
C1: exact byte match != transformed text equivalence. No source file writes.
Usage: python -I -B 04_R40_DUAL_MANIFEST_READONLY_AUDITOR.py CHECKOUT_SOURCE_DIR
Exit 0: every file original exact; 2: only LF->CRLF transport-equivalent;
3: missing / unexpected source mutation; 4: bad original manifest.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

RE = re.compile(r"^([a-f0-9]{64})  ([A-Za-z0-9_./-]+)$")


def h(b):
    return hashlib.sha256(b).hexdigest()


def compare_file(root, path, original_sha):
    if path.startswith("/") or any(x in (".", "..", "") for x in path.split("/")):
        return {"path": path, "status": "INVALID_MANIFEST_PATH"}
    p = root / path
    if not p.is_file() or p.is_symlink():
        return {"path": path, "status": "MISSING_OR_SYMLINK"}
    data = p.read_bytes()
    native = h(data)
    if native == original_sha:
        state = "EXACT_ORIGINAL_BYTES"
    else:
        # A deterministic and explicit transform, never silently written to disk.
        rebuilt = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        state = ("LF_TO_CRLF_COMPATIBLE_NOT_BYTE_EXACT"
                 if rebuilt != data and h(rebuilt) == original_sha
                 else "CONTENT_ORIGINAL_HASH_MISMATCH")
    return {"path": path, "native_bytes": len(data), "native_sha256": native,
            "original_expected_sha256": original_sha, "status": state}


def audit(root):
    manifest_path = root / "SHA256SUMS.txt"
    manifest = manifest_path.read_bytes()
    rows = []
    seen = set()
    for line in manifest.decode("ascii").splitlines():
        m = RE.fullmatch(line)
        if not m or m.group(2) in seen:
            raise ValueError("MALFORMED_OR_DUPLICATE_SOURCE_MANIFEST")
        seen.add(m.group(2))
        rows.append(compare_file(root, m.group(2), m.group(1)))
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    if len(rows) == counts.get("EXACT_ORIGINAL_BYTES", 0):
        status, code = "ORIGINAL_BYTES_EXACT", 0
    elif counts.get("LF_TO_CRLF_COMPATIBLE_NOT_BYTE_EXACT", 0) + counts.get("EXACT_ORIGINAL_BYTES", 0) == len(rows):
        status, code = "CONTENT_EQUIVALENT_TRANSPORT_NORMALIZED_NOT_SOURCE_EXACT", 2
    else:
        status, code = "SOURCE_INTEGRITY_MISSING_OR_CONFLICTED", 3
    return {"status": status, "source_file_count": len(rows), "counts": counts,
            "manifest_native_bytes": len(manifest), "manifest_native_sha256": h(manifest),
            "claim_ceiling": "C1_DESCRIPTIVE_ONLY", "bodytwin_validated": False,
            "device_capture": False, "file_results": rows}, code


def main():
    if len(sys.argv) != 2:
        print("Usage: script.py CHECKOUT_SOURCE_DIR", file=sys.stderr)
        return 4
    try:
        outcome, code = audit(Path(sys.argv[1]))
    except (ValueError, UnicodeError, OSError) as e:
        print(json.dumps({"status": "MANIFEST_INVALID", "error": str(e)}))
        return 4
    print(json.dumps(outcome, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
