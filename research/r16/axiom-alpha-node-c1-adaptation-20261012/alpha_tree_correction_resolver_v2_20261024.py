"""Isolated C1 research guard for an append-only Git tree-identity correction.

Inputs must come from independently retrieved, immutable GitHub objects. This
module rejects nonfinite numeric overflow and checks internal consistency; it does not authenticate
HTTP actors, grant writes, verify scientific claims, or change source files.
"""
import copy
import hashlib
import json
import re

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
EXPECTED_FIELD = "pinned_source_tree"
EXPECTED_KIND = "APPEND_ONLY_SINGLE_FIELD_TREE_IDENTITY"


class IntegrityError(ValueError):
    pass


def _unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise IntegrityError("DUPLICATE_JSON_KEY")
        obj[key] = value
    return obj


def _no_nonfinite(value):
    raise IntegrityError("NONFINITE_JSON_NUMBER")


def _load(raw):
    if not isinstance(raw, bytes):
        raise IntegrityError("SOURCE_BYTES_REQUIRED")
    try:
        doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                         parse_constant=_no_nonfinite)
        json.dumps(doc, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise IntegrityError("INVALID_JSON_OR_UNICODE") from exc
    if not isinstance(doc, dict):
        raise IntegrityError("ROOT_NOT_OBJECT")
    return doc


def _sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _require(condition, reason):
    if not condition:
        raise IntegrityError(reason)


def resolve_tree_identity(manifest_bytes, correction_bytes, *,
                          manifest_commit, manifest_path,
                          observed_commit, observed_tree):
    """Return a fail-closed status and an ephemeral effective manifest.

    observed_commit/tree MUST originate from a separate GitHub Git-commit
    readback by the caller; passing invented values does not authenticate them.
    """
    try:
        original = _load(manifest_bytes)
        correction = _load(correction_bytes)
        supersedes = correction.get("supersedes")
        _require(isinstance(supersedes, dict), "SUPERSEDES_MISSING")
        for value in (manifest_commit, observed_commit, observed_tree):
            _require(isinstance(value, str) and HEX40.fullmatch(value), "INVALID_GIT_ID")
        _require(isinstance(manifest_path, str) and manifest_path.startswith("research/r16/")
                 and ".." not in manifest_path.split("/"), "INVALID_MANIFEST_PATH")
        _require(correction.get("correction_type") == EXPECTED_KIND
                 and correction.get("field") == EXPECTED_FIELD, "CORRECTION_SCOPE_MISMATCH")
        _require(original.get("claim_ceiling") == correction.get("claim_ceiling")
                 == "C1_DESCRIPTIVE_ONLY", "CLAIM_CEILING_MISMATCH")
        _require(correction.get("pinned_main") == original.get("pinned_main"),
                 "MAIN_BINDING_MISMATCH")
        _require(supersedes.get("commit") == manifest_commit
                 and supersedes.get("path") == manifest_path, "SOURCE_LOCATION_MISMATCH")
        _require(supersedes.get("bytes") == len(manifest_bytes), "SOURCE_SIZE_MISMATCH")
        _require(supersedes.get("sha256") == _sha256(manifest_bytes),
                 "SOURCE_SHA256_MISMATCH")
        _require(supersedes.get("git_blob_sha1") == _blob(manifest_bytes),
                 "SOURCE_GIT_BLOB_MISMATCH")
        _require(original.get("pinned_source_head") == correction.get("source_commit")
                 == observed_commit, "SOURCE_COMMIT_MISMATCH")
        _require(original.get(EXPECTED_FIELD) == correction.get("old_value"),
                 "OLD_TREE_MISMATCH")
        _require(isinstance(correction.get("new_value"), str)
                 and HEX40.fullmatch(correction["new_value"]), "INVALID_NEW_TREE")
        _require(correction["new_value"] == observed_tree, "GIT_TREE_READBACK_MISMATCH")
        _require(correction["old_value"] != correction["new_value"],
                 "NO_ACTUAL_CORRECTION")
        _require(isinstance(original.get("count"), int)
                 and type(original["count"]) is int and original["count"] >= 1
                 and isinstance(original.get("files"), list)
                 and len(original["files"]) == original["count"],
                 "SOURCE_INVENTORY_INCOMPLETE")
        paths = [row.get("path") if isinstance(row, dict) else None
                 for row in original["files"]]
        _require(all(isinstance(p, str) and p for p in paths)
                 and len(set(paths)) == len(paths), "SOURCE_INVENTORY_DUPLICATE")
        effective = copy.deepcopy(original)
        effective[EXPECTED_FIELD] = correction["new_value"]
        return {"status": "RESOLVED_C1", "effective": effective,
                "source_sha256": _sha256(manifest_bytes),
                "correction_sha256": _sha256(correction_bytes),
                "source_git_blob": _blob(manifest_bytes)}
    except (IntegrityError, KeyError, TypeError, ValueError) as exc:
        reason = str(exc) if isinstance(exc, IntegrityError) else "MALFORMED_BINDING"
        return {"status": "INCOMPLETE", "reason": reason}
