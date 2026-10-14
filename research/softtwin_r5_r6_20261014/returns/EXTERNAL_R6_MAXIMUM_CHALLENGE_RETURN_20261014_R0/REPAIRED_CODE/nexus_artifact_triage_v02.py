#!/usr/bin/env python3
"""NEXUS REA offline static triage V0.2 research candidate (R6 distinct revision).

Delta vs V0.1 (source-exact; static proofs in the return bundle; runtime here NOT_EXECUTED):
 (1) ROOT ANCHORING CLOSED FOR INTERMEDIATE SYMLINKS: every component of the
     approved root path is opened with O_NOFOLLOW|O_DIRECTORY anchored to the
     previous component FD. A symlink anywhere in the root path (intermediate
     or final) is denied. V0.1 followed intermediate components.
 (2) ZIP LOCAL DATA REGION BOUND: the declared compressed data region must lie
     inside the captured buffer; without data-descriptor flag the local header
     crc/compressed/uncompressed sizes must match the central directory.
 (3) HARDLINK WITNESS: st_nlink > 1 is recorded in unresolved (documented
     behavior for S09) instead of silent acceptance.

POSIX-only research candidate, C1. No network, subprocess, extraction,
execution or auth decisions. Not a sandbox. No atomic snapshot guarantee
against hostile in-place writers (order S5). No Windows native claim.
Environments whose temp paths contain symlink components (e.g. macOS /tmp)
are denied BY DESIGN; run tests from a symlink-free base directory.
"""
from __future__ import annotations
import argparse
import hashlib
import errno
import io
import json
import os
from pathlib import Path
import re
import stat
import struct
import sys
import unicodedata
import zipfile

SCHEMA = "NEXUS_REA_STATIC_TRIAGE_V0_2_C1"
MAX_FILE = 32 * 1024 * 1024
MAX_ENTRIES = 512
MAX_UNCOMPRESSED = 128 * 1024 * 1024
MAX_RATIO = 200
CASE_RE = re.compile(r"NEXUS_[A-Z0-9_]{4,120}\Z")
_OPEN_SUPPORTS_DIR_FD = os.open in os.supports_dir_fd
WIN_RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$", re.I)

class Denied(ValueError):
    pass

def _kind(prefix: bytes, filename: str = "") -> str:
    if prefix.startswith(b"\x7fELF"): return "ELF"
    if prefix.startswith(b"MZ"): return "PE_CANDIDATE_MZ_ONLY"
    if prefix[:4] in (b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe"): return "MACHO_CANDIDATE"
    if prefix.startswith(b"\0asm"): return "WASM"
    if prefix.startswith(b"PK\x03\x04"): return "ZIP"
    return "UNCLASSIFIED_STATIC_BYTES"

def _absolute_components(path: str) -> list:
    if not os.path.isabs(path):
        raise Denied("PATH_MUST_BE_ABSOLUTE")
    parts = [p for p in path.split(os.sep) if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise Denied("PATH_COMPONENT_INVALID")
    return parts

def _open_root_fd(root: Path) -> int:
    """Open the approved root directory with every component NOFOLLOW-checked (V0.2)."""
    dflags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    parts = _absolute_components(str(root))
    opened = []
    try:
        parent = os.open(os.sep, dflags)
        opened.append(parent)
        for p in parts:
            parent = os.open(p, dflags, dir_fd=parent)
            opened.append(parent)
        root_fd = parent
    except OSError as e:
        for f in reversed(opened):
            try: os.close(f)
            except OSError: pass
        if e.errno == errno.ELOOP:
            raise Denied("ROOT_UNAVAILABLE_OR_SYMLINK") from e
        raise Denied("SECURE_OPEN_FAILED_" + str(e.errno)) from e
    for f in opened:
        if f != root_fd:
            try: os.close(f)
            except OSError: pass
    return root_fd

def _fd_read_snapshot(root: Path, target: Path):
    if os.name != "posix" or not _OPEN_SUPPORTS_DIR_FD or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise Denied("SECURE_OPENAT_UNAVAILABLE_THIS_PLATFORM")
    root = Path(os.path.abspath(root))
    target = Path(os.path.abspath(target))
    try: rel = target.relative_to(root)
    except ValueError as ex: raise Denied("ARTIFACT_OUTSIDE_APPROVED_ROOT") from ex
    if not rel.parts: raise Denied("ARTIFACT_IS_ROOT")
    root_fd = _open_root_fd(root)
    dflags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    fflags = os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    opened = [root_fd]
    try:
        parent = root_fd
        for item in rel.parts[:-1]:
            if item in (".", ".."):
                raise Denied("ARTIFACT_PATH_INVALID")
            parent = os.open(item, dflags, dir_fd=parent)
            opened.append(parent)
        f = os.open(rel.parts[-1], fflags, dir_fd=parent)
        opened.append(f)
        before = os.fstat(f)
        if not stat.S_ISREG(before.st_mode): raise Denied("NOT_REGULAR_FILE")
        if before.st_size == 0 or before.st_size > MAX_FILE: raise Denied("FILE_SIZE_LIMIT")
        with os.fdopen(os.dup(f), "rb") as stream:
            data = stream.read(MAX_FILE + 1)
        if len(data) != before.st_size or len(data) > MAX_FILE: raise Denied("FILE_CHANGED_DURING_READ")
        after = os.fstat(f)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise Denied("FILE_CHANGED_DURING_READ")
        return data, before.st_nlink
    except OSError as e:
        if e.errno == errno.ELOOP: raise Denied("SYMLINK_COMPONENT") from e
        raise Denied("SECURE_OPEN_FAILED_" + str(e.errno)) from e
    finally:
        for f in reversed(opened):
            try: os.close(f)
            except OSError: pass

def _safe_member_name(name: str):
    if not name or name.startswith("/") or "\\" in name or "\0" in name or re.match(r"^[A-Za-z]:", name):
        raise Denied("ZIP_PATH_INVALID")
    parts = name.rstrip("/").split("/")
    if any(not p or p in (".", "..") or ":" in p or p.rstrip(" .") != p or WIN_RESERVED.fullmatch(p) for p in parts):
        raise Denied("ZIP_PATH_INVALID")
    if any(any(ord(c) < 32 for c in p) for p in parts):
        raise Denied("ZIP_PATH_INVALID")
    return "/".join(unicodedata.normalize("NFC", p).casefold() for p in parts)

def _validate_zip_bytes(data: bytes) -> dict:
    try:
        with zipfile.ZipFile(io.BytesIO(data), "r") as z:
            infos = z.infolist()
            if len(infos) > MAX_ENTRIES: raise Denied("ZIP_ENTRY_COUNT_LIMIT")
            total = 0
            seen = set()
            normalized_paths = []
            for i in infos:
                name = i.filename
                norm = _safe_member_name(name)
                if norm in seen: raise Denied("ZIP_PATH_OR_DUPLICATE_INVALID")
                seen.add(norm); normalized_paths.append((norm, i.is_dir()))
                if i.flag_bits & 1: raise Denied("ZIP_ENCRYPTED_UNSUPPORTED")
                mode = (i.external_attr >> 16) & 65535
                typ = stat.S_IFMT(mode)
                if typ not in (0, stat.S_IFREG, stat.S_IFDIR): raise Denied("ZIP_UNSAFE_FILE_TYPE")
                total += i.file_size
                if total > MAX_UNCOMPRESSED: raise Denied("ZIP_UNCOMPRESSED_SIZE_LIMIT")
                if i.file_size > MAX_RATIO * max(1, i.compress_size): raise Denied("ZIP_COMPRESSION_RATIO_LIMIT")
                o = i.header_offset
                if o < 0 or o + 30 > len(data) or data[o:o+4] != b"PK\x03\x04": raise Denied("ZIP_LOCAL_HEADER_INVALID")
                hdr = struct.unpack_from("<HHHHHIIIHH", data, o + 4)
                flags, method, fnlen, extralen = hdr[1], hdr[2], hdr[-2], hdr[-1]
                if o + 30 + fnlen + extralen > len(data): raise Denied("ZIP_LOCAL_HEADER_INVALID")
                rawname = data[o+30:o+30+fnlen]
                if b"\0" in rawname: raise Denied("ZIP_LOCAL_NAME_INVALID")
                enc = "utf-8" if i.flag_bits & 0x800 else "cp437"
                try: local_name = rawname.decode(enc, "strict")
                except UnicodeError as ex: raise Denied("ZIP_LOCAL_NAME_INVALID") from ex
                if local_name != name or flags != i.flag_bits or method != i.compress_type:
                    raise Denied("ZIP_LOCAL_CENTRAL_MISMATCH")
                data_end = o + 30 + fnlen + extralen + i.compress_size
                if data_end > len(data): raise Denied("ZIP_LOCAL_DATA_REGION_OUT_OF_BOUNDS")
                if not (flags & 0x08):
                    l_crc, l_csize, l_usize = hdr[5], hdr[6], hdr[7]
                    if l_crc != i.CRC or l_csize != i.compress_size or l_usize != i.file_size:
                        raise Denied("ZIP_LOCAL_CENTRAL_MISMATCH")
            for p, isdir in normalized_paths:
                for other, otherdir in normalized_paths:
                    if other != p and other.startswith(p + "/") and not isdir:
                        raise Denied("ZIP_FILE_DIRECTORY_PREFIX_COLLISION")
            return {"entries": len(infos), "declared_uncompressed_bytes": total, "entries_extracted": False, "zip_metadata_bound_to_source_bytes": True, "local_data_regions_bounded": True}
    except (zipfile.BadZipFile, EOFError, OSError, UnicodeError, struct.error) as ex:
        raise Denied("ZIP_MALFORMED") from ex

def triage(root: Path, path: Path, case_id: str) -> dict:
    if not isinstance(case_id, str) or not CASE_RE.fullmatch(case_id): raise Denied("CASE_ID_INVALID")
    raw, nlink = _fd_read_snapshot(root, path)
    kind = _kind(raw[:16])
    zip_summary = _validate_zip_bytes(raw) if kind == "ZIP" else None
    unresolved = ["NOT_A_SANDBOX", "NO_HOSTILE_INPLACE_WRITER_ATOMICITY", "ZIP_DECLARED_UNCOMPRESSED_ONLY", "NO_EXECUTION", "NO_SOURCE_CODE_RECOVERY", "NO_WINDOWS_NATIVE_HANDLE_VALIDATION"]
    if nlink > 1:
        unresolved.append("HARDLINK_WITNESS_NLINK_" + str(int(nlink)))
    return {
      "schema": SCHEMA, "case_id": case_id, "source_sha256": hashlib.sha256(raw).hexdigest(),
      "source_bytes": len(raw), "artifact_type": kind,
      "evidence_mode": "FD_CAPTURED_BYTES_STATIC_MAGIC_ZIP_CENTRAL_AND_LOCAL_HEADERS_ONLY",
      "zip_summary": zip_summary, "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
      "execution_performed": False, "decompilation_performed": False, "mcp_called": False, "network_called": False,
      "claim": "CAPTURED_BYTES_AND_METADATA_OBSERVED_NOT_BEHAVIOR_VERIFIED",
      "authority": "NONE_NOT_AN_AUTHORIZATION_GATE",
      "unresolved": unresolved
    }

def main(argv=None):
    p = argparse.ArgumentParser(description="NEXUS REA C1 offline bound-byte triage V0.2 POSIX-only research candidate")
    p.add_argument("--root", required=True, type=Path); p.add_argument("--artifact", required=True, type=Path); p.add_argument("--case-id", required=True)
    args = p.parse_args(argv)
    try:
        print(json.dumps(triage(args.root, args.artifact, args.case_id), sort_keys=True, separators=(",", ":")))
        return 0
    except (Denied, OSError, ValueError) as e:
        print("DENIED_C1: " + str(e), file=sys.stderr)
        return 2
if __name__ == "__main__": raise SystemExit(main())
