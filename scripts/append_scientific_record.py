#!/usr/bin/env python3
"""Append one validated record to the local content-addressed communication ledger.

This tool performs no network writes. Commit/push/release remain separate governed steps.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from validate_scientific_communication import errors as semantic_errors
from validate_scientific_ledger import (
    INDEX_REL, LATEST_REL, INDEX_SERIALIZATION, canonical_index_line,
    expected_object_path, load_json_bytes, sha256_bytes, validate_ledger
)

def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def append_record(root: Path, source: Path, recorded_at_utc: str | None = None) -> dict:
    raw = source.read_bytes()
    record = load_json_bytes(raw)
    sem = semantic_errors(record)
    if sem:
        raise ValueError("semantic validation failed: " + ",".join(sem))

    index_path = root / INDEX_REL
    latest_path = root / LATEST_REL
    index_path.parent.mkdir(parents=True, exist_ok=True)

    existing_lines: list[bytes] = []
    previous_line_hash = None
    existing_ids: set[str] = set()

    if index_path.exists() or latest_path.exists():
        if not (index_path.exists() and latest_path.exists()):
            raise ValueError("ledger partially initialized")
        current_errors = validate_ledger(root)
        if current_errors:
            raise ValueError("existing ledger invalid: " + ";".join(current_errors))
        existing_lines = index_path.read_bytes().splitlines()
        for line in existing_lines:
            entry = load_json_bytes(line)
            existing_ids.add(entry["record_id"])
        if existing_lines:
            previous_line_hash = sha256_bytes(existing_lines[-1])

    record_id = record["record_id"]
    if record_id in existing_ids:
        raise ValueError(f"duplicate record_id: {record_id}")

    digest = sha256_bytes(raw)
    rel_obj = expected_object_path(digest)
    obj_path = root / rel_obj
    if obj_path.exists() and obj_path.read_bytes() != raw:
        raise ValueError("content-address collision/path conflict")

    sequence = len(existing_lines) + 1
    entry = {
        "schema_version": "1.0.0",
        "sequence": sequence,
        "record_id": record_id,
        "record_type": record["record_type"],
        "record_path": rel_obj.as_posix(),
        "record_bytes": len(raw),
        "record_sha256": digest,
        "previous_index_line_sha256": previous_line_hash,
        "recorded_at_utc": recorded_at_utc or utc_now(),
        "index_serialization": INDEX_SERIALIZATION,
        "claim_ceiling": "C1",
        "claim_promotion": False,
    }
    line = canonical_index_line(entry)
    line_hash = sha256_bytes(line)

    new_index = b"\n".join(existing_lines + [line]) + b"\n"
    latest = {
        "schema_version": "1.0.0",
        "sequence": sequence,
        "record_id": record_id,
        "record_type": record["record_type"],
        "record_path": rel_obj.as_posix(),
        "record_bytes": len(raw),
        "record_sha256": digest,
        "head_index_line_sha256": line_hash,
        "index_path": INDEX_REL.as_posix(),
        "index_serialization": INDEX_SERIALIZATION,
        "claim_ceiling": "C1",
        "claim_promotion": False,
    }
    latest_bytes = (
        json.dumps(latest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")

    atomic_write(obj_path, raw)
    atomic_write(index_path, new_index)
    atomic_write(latest_path, latest_bytes)

    post = validate_ledger(root)
    if post:
        raise RuntimeError("post-append ledger validation failed: " + ";".join(post))

    return {
        "sequence": sequence,
        "record_id": record_id,
        "record_path": rel_obj.as_posix(),
        "record_bytes": len(raw),
        "record_sha256": digest,
        "head_index_line_sha256": line_hash,
        "claim_ceiling": "C1",
        "claim_promotion": False,
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("record", type=Path)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--recorded-at-utc")
    ns = ap.parse_args()
    receipt = append_record(ns.root, ns.record, ns.recorded_at_utc)
    print(json.dumps(receipt, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
