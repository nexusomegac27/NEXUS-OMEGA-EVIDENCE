#!/usr/bin/env python3
"""Validate the append-only NEXUS scientific communication ledger."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from validate_scientific_communication import errors as semantic_errors

INDEX_REL = Path("communication/index/v1/records.jsonl")
LATEST_REL = Path("communication/index/v1/latest.json")
OBJECT_ROOT = Path("communication/objects/sha256")
INDEX_KEYS = {
    "schema_version", "sequence", "record_id", "record_type", "record_path",
    "record_bytes", "record_sha256", "previous_index_line_sha256",
    "recorded_at_utc", "index_serialization", "claim_ceiling", "claim_promotion"
}
INDEX_SERIALIZATION = "NEXUS_SORTED_JSON_V1"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def no_duplicate_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out

def load_json_bytes(data: bytes) -> dict[str, Any]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM prohibited")
    text = data.decode("utf-8")
    obj = json.loads(text, object_pairs_hook=no_duplicate_object)
    if not isinstance(obj, dict):
        raise ValueError("top-level JSON object required")
    return obj

def canonical_index_line(entry: dict[str, Any]) -> bytes:
    return json.dumps(
        entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

def expected_object_path(record_sha256: str) -> Path:
    return OBJECT_ROOT / record_sha256[:2] / record_sha256[2:4] / record_sha256 / "record.json"

def validate_ledger(root: Path) -> list[str]:
    errs: list[str] = []
    index_path = root / INDEX_REL
    latest_path = root / LATEST_REL
    if not index_path.exists():
        return ["INDEX_NOT_PRESENT"]
    if not latest_path.exists():
        return ["LATEST_NOT_PRESENT"]

    raw_index = index_path.read_bytes()
    if b"\r" in raw_index:
        errs.append("INDEX_MUST_USE_LF")
    raw_lines = raw_index.splitlines()
    if not raw_lines:
        return sorted(set(errs + ["INDEX_EMPTY"]))

    seen_ids: set[str] = set()
    referenced_paths: set[Path] = set()
    previous_hash = None
    last_entry = None
    last_line_hash = None

    for offset, raw_line in enumerate(raw_lines, 1):
        try:
            entry = load_json_bytes(raw_line)
        except Exception as exc:
            errs.append(f"INDEX_LINE_{offset}_JSON_INVALID:{exc}")
            continue

        if set(entry) != INDEX_KEYS:
            errs.append(f"INDEX_LINE_{offset}_KEYSET_INVALID")
        if entry.get("schema_version") != "1.0.0":
            errs.append(f"INDEX_LINE_{offset}_SCHEMA_VERSION")
        if entry.get("sequence") != offset:
            errs.append(f"INDEX_LINE_{offset}_SEQUENCE")
        if entry.get("index_serialization") != INDEX_SERIALIZATION:
            errs.append(f"INDEX_LINE_{offset}_SERIALIZATION")
        if entry.get("claim_ceiling") != "C1":
            errs.append(f"INDEX_LINE_{offset}_CLAIM_CEILING")
        if entry.get("claim_promotion") is not False:
            errs.append(f"INDEX_LINE_{offset}_CLAIM_PROMOTION")

        record_id = entry.get("record_id")
        if record_id in seen_ids:
            errs.append(f"INDEX_LINE_{offset}_DUPLICATE_RECORD_ID")
        if isinstance(record_id, str):
            seen_ids.add(record_id)

        if entry.get("previous_index_line_sha256") != previous_hash:
            errs.append(f"INDEX_LINE_{offset}_PREVIOUS_HASH")

        if canonical_index_line(entry) != raw_line:
            errs.append(f"INDEX_LINE_{offset}_NONCANONICAL_SERIALIZATION")

        digest = entry.get("record_sha256")
        rel = Path(entry.get("record_path", ""))
        if not isinstance(digest, str) or len(digest) != 64:
            errs.append(f"INDEX_LINE_{offset}_RECORD_SHA256")
        elif rel != expected_object_path(digest):
            errs.append(f"INDEX_LINE_{offset}_CONTENT_ADDRESS_PATH")

        path = root / rel
        referenced_paths.add(rel)
        if not path.exists():
            errs.append(f"INDEX_LINE_{offset}_OBJECT_NOT_PRESENT")
        else:
            data = path.read_bytes()
            if len(data) != entry.get("record_bytes"):
                errs.append(f"INDEX_LINE_{offset}_OBJECT_BYTES")
            if sha256_bytes(data) != digest:
                errs.append(f"INDEX_LINE_{offset}_OBJECT_SHA256")
            try:
                record = load_json_bytes(data)
                if record.get("record_id") != record_id:
                    errs.append(f"INDEX_LINE_{offset}_RECORD_ID_BIND")
                if record.get("record_type") != entry.get("record_type"):
                    errs.append(f"INDEX_LINE_{offset}_RECORD_TYPE_BIND")
                for sem in semantic_errors(record):
                    errs.append(f"INDEX_LINE_{offset}_SEMANTIC:{sem}")
            except Exception as exc:
                errs.append(f"INDEX_LINE_{offset}_OBJECT_JSON_INVALID:{exc}")

        last_entry = entry
        last_line_hash = sha256_bytes(raw_line)
        previous_hash = last_line_hash

    object_root = root / OBJECT_ROOT
    if object_root.exists():
        for obj in object_root.rglob("record.json"):
            rel = obj.relative_to(root)
            if rel not in referenced_paths:
                errs.append(f"ORPHAN_OBJECT:{rel.as_posix()}")

    try:
        latest = load_json_bytes(latest_path.read_bytes())
    except Exception as exc:
        errs.append(f"LATEST_JSON_INVALID:{exc}")
        return sorted(set(errs))

    expected_latest_keys = {
        "schema_version", "sequence", "record_id", "record_type", "record_path",
        "record_bytes", "record_sha256", "head_index_line_sha256", "index_path",
        "index_serialization", "claim_ceiling", "claim_promotion"
    }
    if set(latest) != expected_latest_keys:
        errs.append("LATEST_KEYSET_INVALID")
    if last_entry:
        comparisons = {
            "sequence": last_entry.get("sequence"),
            "record_id": last_entry.get("record_id"),
            "record_type": last_entry.get("record_type"),
            "record_path": last_entry.get("record_path"),
            "record_bytes": last_entry.get("record_bytes"),
            "record_sha256": last_entry.get("record_sha256"),
        }
        for key, value in comparisons.items():
            if latest.get(key) != value:
                errs.append(f"LATEST_{key.upper()}_MISMATCH")
    if latest.get("head_index_line_sha256") != last_line_hash:
        errs.append("LATEST_HEAD_HASH_MISMATCH")
    if latest.get("index_path") != INDEX_REL.as_posix():
        errs.append("LATEST_INDEX_PATH")
    if latest.get("index_serialization") != INDEX_SERIALIZATION:
        errs.append("LATEST_SERIALIZATION")
    if latest.get("claim_ceiling") != "C1":
        errs.append("LATEST_CLAIM_CEILING")
    if latest.get("claim_promotion") is not False:
        errs.append("LATEST_CLAIM_PROMOTION")

    return sorted(set(errs))

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ns = ap.parse_args()
    errs = validate_ledger(ns.root)
    if errs:
        print(json.dumps({"valid": False, "errors": errs}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"valid": True, "errors": []}, indent=2))

if __name__ == "__main__":
    main()
