#!/usr/bin/env python3
"""Isolated standard-library C1 evidence intake reducer.

This validates source bytes and emits a deterministic scoped disposition.
It does not push, deploy, access GitHub, or rewrite a model/runtime.
"""
import argparse
import hashlib
import json
from pathlib import Path

HEX64 = set("0123456789abcdef")
CLAIM = "C1_DESCRIPTIVE_ONLY"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def valid_digest(value):
    return isinstance(value, str) and len(value) == 64 and all(ch in HEX64 for ch in value)


def decide(data, source: bytes | None, existing_hashes=()):
    """Return a verdict without modifying any external state."""
    reported_hash = data.get("sha256")
    result = {"material_id": reported_hash if valid_digest(reported_hash) else "UNBOUND",
              "decision": "HOLD_SCOPED", "reason": None,
              "source_verified": False, "research_push_eligible": False,
              "model_weights_changed": False, "runtime_modified": False,
              "claim_ceiling": CLAIM}
    if data.get("claim_ceiling") != CLAIM:
        result["reason"] = "CLAIM_CEILING_OR_SCOPE_INVALID"
        return result
    if not valid_digest(reported_hash) or type(data.get("bytes")) is not int or data["bytes"] < 0:
        result["reason"] = "INVALID_EXPECTED_BYTES_OR_SHA256"
        return result
    if source is None:
        result["reason"] = "SOURCE_GAP"
        return result
    if len(source) != data["bytes"] or sha256(source) != reported_hash:
        result["reason"] = "SOURCE_MISMATCH"
        return result
    result["source_verified"] = True
    if reported_hash in set(existing_hashes):
        result.update(decision="NO_CHANGE", reason="NOOP_DUPLICATE")
        return result
    if data.get("public_safe") is not True or data.get("publication_rights") is not True:
        result["reason"] = "PRIVACY_OR_PUBLICATION_RIGHTS_UNPROVEN"
        return result
    if data.get("kind") == "code_change":
        result.update(decision="PATCH_CANDIDATE", reason="SANDBOX_INDEPENDENT_EVAL_REQUIRED")
        return result
    if data.get("kind") == "contradiction":
        result.update(decision="CONTRADICTION_APPEND", reason="COUNTEREVIDENCE_PRESERVED",
                      research_push_eligible=True)
        return result
    if data.get("kind") in ("research", "test_result", "source"):
        result.update(decision="KNOWLEDGE_APPEND", reason="C1_EVIDENCE_ELIGIBLE_FOR_OPERATOR_RESEARCH_PUSH",
                      research_push_eligible=True)
        return result
    result["reason"] = "UNKNOWN_MATERIAL_KIND"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path, help="JSON metadata about the material")
    parser.add_argument("source", type=Path, help="actual source file bytes")
    parser.add_argument("--existing", type=Path, help="JSON list of SHA256 values already indexed")
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    existing = json.loads(args.existing.read_text(encoding="utf-8")) if args.existing else []
    result = decide(metadata, args.source.read_bytes() if args.source.exists() else None, existing)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["decision"] not in ("HOLD_SCOPED",) else 2


if __name__ == "__main__":
    raise SystemExit(main())
