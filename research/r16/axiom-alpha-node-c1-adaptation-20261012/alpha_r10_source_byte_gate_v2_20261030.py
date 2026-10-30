#!/usr/bin/env python3
"""Offline R10 C1 source-byte and registry gate; never authenticates GitHub actors."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"[0-9a-f]{40}\\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\\Z")
LOGIN = re.compile(r"[A-Za-z0-9-]{1,39}\\Z")
CLAIM_FIELDS = {
    "source_commit", "source_sha256", "source_bytes", "source_git_blob",
    "owner_login", "actor_login", "actor_origin", "receipt_origin",
    "claims_independent_receiver_ack", "claims_expert_research_executed",
}


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def read_json(path):
    raw = Path(path).read_bytes()
    if len(raw) > 65536:
        raise ValueError("JSON_TOO_LARGE")
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                     parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE")))
    if type(obj) is not dict:
        raise ValueError("INVALID_JSON_OBJECT")
    return raw, obj


def hex_pin(value, pattern):
    if type(value) is not str or not pattern.fullmatch(value):
        raise ValueError("INVALID_PIN")


def check(registry_raw, registry, claim, source_raw, pins):
    for value, pattern in ((pins.registry_sha256, HEX64), (pins.source_commit, HEX40),
                           (pins.source_sha256, HEX64), (pins.source_git_blob, HEX40)):
        hex_pin(value, pattern)
    if type(pins.source_bytes) is not int or pins.source_bytes <= 0:
        raise ValueError("INVALID_SOURCE_BYTES_PIN")
    if hashlib.sha256(registry_raw).hexdigest() != pins.registry_sha256:
        raise ValueError("REGISTRY_SHA256_MISMATCH")
    if registry.get("default") != "DENY" or registry.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY":
        raise ValueError("INVALID_REGISTRY_POLICY")
    if registry.get("anchor_repo") != "nexusomegac27/NEXUS-OMEGA-EVIDENCE":
        raise ValueError("INVALID_REGISTRY_REPO")
    owner = registry.get("owner_github_login")
    allow = registry.get("external_actor_allowlist")
    if type(owner) is not str or not LOGIN.fullmatch(owner):
        raise ValueError("INVALID_REGISTRY_OWNER")
    if type(allow) is not list or any(type(x) is not str or not LOGIN.fullmatch(x) for x in allow):
        raise ValueError("INVALID_REGISTRY_ALLOWLIST")
    if len({x.lower() for x in allow}) != len(allow):
        raise ValueError("DUPLICATE_REGISTRY_ACTOR")
    if set(claim) != CLAIM_FIELDS:
        raise ValueError("INVALID_CLAIM_FIELDS")
    for key, pattern in (("source_commit", HEX40), ("source_sha256", HEX64), ("source_git_blob", HEX40)):
        hex_pin(claim[key], pattern)
    if type(claim["source_bytes"]) is not int or claim["source_bytes"] <= 0:
        raise ValueError("INVALID_CLAIM_SOURCE_BYTES")
    for key in ("claims_independent_receiver_ack", "claims_expert_research_executed"):
        if type(claim[key]) is not bool:
            raise ValueError("INVALID_CLAIM_BOOL")
    for key in ("owner_login", "actor_login"):
        if type(claim[key]) is not str or not LOGIN.fullmatch(claim[key]):
            raise ValueError("INVALID_CLAIM_LOGIN")
    if claim["actor_origin"] not in ("GITHUB_API", "SELF_DECLARED", "UNKNOWN"):
        raise ValueError("INVALID_ACTOR_ORIGIN")
    if claim["receipt_origin"] not in ("EXTERNAL_GITHUB_ASSET", "OWNER_MEDIATED_FILE", "OWNER_ISSUE_COMMENT"):
        raise ValueError("INVALID_RECEIPT_ORIGIN")
    if claim["owner_login"].lower() != owner.lower():
        raise ValueError("OWNER_MISMATCH")
    if len(source_raw) > 1048576 or not source_raw:
        raise ValueError("SOURCE_SIZE_LIMIT")
    actual_sha = hashlib.sha256(source_raw).hexdigest()
    actual_blob = hashlib.sha1(b"blob " + str(len(source_raw)).encode("ascii") + b"\\0" + source_raw).hexdigest()
    if (len(source_raw), actual_sha, actual_blob) != (pins.source_bytes, pins.source_sha256, pins.source_git_blob):
        raise ValueError("SOURCE_BYTES_HASH_BLOB_MISMATCH")
    if any(claim[key] != getattr(pins, key) for key in
           ("source_commit", "source_sha256", "source_bytes", "source_git_blob")):
        raise ValueError("CLAIM_SOURCE_PIN_MISMATCH")
    actor = claim["actor_login"].lower()
    eligible = (claim["claims_independent_receiver_ack"]
                and claim["actor_origin"] == "GITHUB_API"
                and claim["receipt_origin"] == "EXTERNAL_GITHUB_ASSET"
                and actor != owner.lower() and actor in {x.lower() for x in allow})
    return {
        "source_bytes_sha256_git_blob": "MATCH",
        "registry_sha256": "MATCH",
        "policy_review_eligibility": "ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY" if eligible else "NOT_ESTABLISHED",
        "independent_receiver_ack": "NOT_ESTABLISHED",
        "authenticated_github_actor": "NOT_ESTABLISHED",
        "expert_research_execution": "SOURCE_ASSERTED_ONLY" if claim["claims_expert_research_executed"] else "NOT_ESTABLISHED",
        "scientific_adjudication": "NOT_PERFORMED",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main():
    ap = argparse.ArgumentParser()
    for flag in ("registry", "claim", "source", "registry-sha256", "source-commit",
                 "source-sha256", "source-bytes", "source-git-blob"):
        ap.add_argument("--" + flag, required=True, type=int if flag == "source-bytes" else str)
    args = ap.parse_args()
    try:
        rb, registry = read_json(args.registry)
        _, claim = read_json(args.claim)
        result = check(rb, registry, claim, Path(args.source).read_bytes(), args)
        print(json.dumps({"ok": True, "result": result}, sort_keys=True))
        return 0
    except (ValueError, OSError, UnicodeDecodeError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
