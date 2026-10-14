#!/usr/bin/env python3
"""NEXUS read-only artifact TRIAGE. Not REA, not an executor, not an authorization gate.

Python standard library, no network, no subprocess, no writes. User-supplied root
must already have been authorized by an independent host policy. This tool merely
produces source-bound metadata for a disposable sandbox artifact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import zipfile

SCHEMA = "NEXUS_REA_STATIC_TRIAGE_V0"
MAX_FILE = 32 * 1024 * 1024
MAX_ENTRIES = 512
MAX_UNCOMPRESSED = 128 * 1024 * 1024
MAX_RATIO = 200

class Denied(ValueError):
    pass


def _kind(prefix: bytes, filename: str) -> str:
    if prefix.startswith(b"\x7fELF"): return "ELF"
    if prefix.startswith(b"MZ"): return "PE_CANDIDATE_MZ_ONLY"
    if prefix[:4] in (b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe"): return "MACHO_CANDIDATE"
    if prefix.startswith(b"\0asm"): return "WASM"
    if prefix.startswith(b"PK\x03\x04"): return "ZIP"
    return "UNCLASSIFIED_STATIC_BYTES"


def _validate_zip(path: Path) -> dict:
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            if len(infos) > MAX_ENTRIES: raise Denied("ZIP_ENTRY_COUNT_LIMIT")
            total = 0
            names = set()
            for i in infos:
                name = i.filename
                if (not name or name in names or "\\" in name or name.startswith("/") or
                    re.match(r"^[A-Za-z]:", name) or "\x00" in name or
                    any(part in ("", ".", "..") for part in name.rstrip("/").split("/"))):
                    raise Denied("ZIP_PATH_OR_DUPLICATE_INVALID")
                names.add(name)
                if i.flag_bits & 1: raise Denied("ZIP_ENCRYPTED_ENTRY_UNSUPPORTED")
                mode = (i.external_attr >> 16) & 0xffff
                if stat.S_IFMT(mode) in (stat.S_IFLNK, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK):
                    raise Denied("ZIP_UNSAFE_FILE_TYPE")
                total += i.file_size
                if total > MAX_UNCOMPRESSED: raise Denied("ZIP_UNCOMPRESSED_SIZE_LIMIT")
                if i.file_size > MAX_RATIO * max(1, i.compress_size):
                    raise Denied("ZIP_COMPRESSION_RATIO_LIMIT")
            return {"entries":len(infos),"declared_uncompressed_bytes":total,"entries_extracted":False}
    except (zipfile.BadZipFile, EOFError, OSError) as ex:
        raise Denied("ZIP_MALFORMED") from ex


def triage(root: Path, path: Path, case_id: str) -> dict:
    if not re.fullmatch(r"NEXUS_[A-Z0-9_]{4,120}", case_id):
        raise Denied("CASE_ID_INVALID")
    root = Path(os.path.abspath(root))
    target = Path(os.path.abspath(path))
    if not root.is_dir() or root.is_symlink(): raise Denied("ROOT_UNAVAILABLE_OR_SYMLINK")
    try: relative = target.relative_to(root)
    except ValueError as ex: raise Denied("ARTIFACT_OUTSIDE_APPROVED_ROOT") from ex
    if not relative.parts: raise Denied("ARTIFACT_IS_ROOT")
    for segment in (root.joinpath(*relative.parts[:k]) for k in range(1,len(relative.parts)+1)):
        if segment.is_symlink(): raise Denied("SYMLINK_COMPONENT")
    if not target.is_file(): raise Denied("NOT_REGULAR_FILE")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode): raise Denied("NOT_REGULAR_FILE")
        if before.st_size == 0 or before.st_size > MAX_FILE: raise Denied("FILE_SIZE_LIMIT")
        digest = hashlib.sha256()
        sample = b""
        with os.fdopen(fd, "rb", closefd=False) as stream:
            for block in iter(lambda: stream.read(1 << 18), b""):
                if len(sample) < 16: sample += block[:16-len(sample)]
                digest.update(block)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise Denied("FILE_CHANGED_DURING_READ")
        detected = _kind(sample, target.name)
    finally:
        os.close(fd)
    zip_summary = _validate_zip(target) if detected == "ZIP" else None
    record = {
        "schema":SCHEMA,"case_id":case_id,"source_sha256":digest.hexdigest(),
        "source_bytes":before.st_size,"artifact_type":detected,
        "evidence_mode":"STATIC_MAGIC_AND_ZIP_CENTRAL_DIRECTORY_ONLY",
        "zip_summary":zip_summary,"claim_ceiling":"C1_DESCRIPTIVE_ONLY",
        "execution_performed":False,"decompilation_performed":False,
        "mcp_called":False,"network_called":False,
        "claim":"ARTIFACT_BYTES_OBSERVED_NOT_BEHAVIOR_VERIFIED",
        "authority":"NONE_NOT_AN_AUTHORIZATION_GATE",
        "unresolved":["NO_BEHAVIORAL_EXECUTION", "NO_SOURCE_CODE_RECOVERY", "NO_PROVIDER_ANALYSIS"]
    }
    return record


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only offline NEXUS artifact triage (research-only).")
    ap.add_argument("--root",required=True,type=Path)
    ap.add_argument("--artifact",required=True,type=Path)
    ap.add_argument("--case-id",required=True)
    args = ap.parse_args(argv)
    try:
        print(json.dumps(triage(args.root,args.artifact,args.case_id),ensure_ascii=False,sort_keys=True,separators=(",",":")))
        return 0
    except (Denied,OSError,ValueError) as e:
        print("DENIED_C1: "+str(e),file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main())
