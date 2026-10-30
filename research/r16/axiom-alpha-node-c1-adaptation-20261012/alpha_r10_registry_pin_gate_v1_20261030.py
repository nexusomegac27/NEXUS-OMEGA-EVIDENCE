#!/usr/bin/env python3
"""Offline C1 R10 policy-pin preflight; never authenticates actors or promotes ACKs."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
LOGIN = re.compile(r"[A-Za-z0-9-]{1,39}\Z")
CLAIM_FIELDS = {
    "source_commit", "source_sha256", "source_bytes", "source_git_blob",
    "source_bytes_rehashed", "source_blob_rehashed", "owner_login",
    "actor_login", "actor_origin", "receipt_origin",
    "claims_independent_receiver_ack", "claims_expert_research_executed",
}


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("DUPLICATE_JSON_KEY")
        out[k] = v
    return out


def parse_file(path):
    raw = Path(path).read_bytes()
    if len(raw) > 65536:
        raise ValueError("INPUT_TOO_LARGE")
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                     parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE")))
    if type(obj) is not dict:
        raise ValueError("INVALID_JSON_OBJECT")
    return raw, obj


def require_hex(s, regex):
    if type(s) is not str or not regex.fullmatch(s):
        raise ValueError("INVALID_PIN")


def check(registry_bytes, registry, claim, pins):
    require_hex(pins.registry_sha256, HEX64)
    require_hex(pins.source_commit, HEX40)
    require_hex(pins.source_sha256, HEX64)
    require_hex(pins.source_git_blob, HEX40)
    if type(pins.source_bytes) is not int or pins.source_bytes <= 0:
        raise ValueError("INVALID_SOURCE_BYTES_PIN")
    if hashlib.sha256(registry_bytes).hexdigest() != pins.registry_sha256:
        raise ValueError("REGISTRY_SHA256_MISMATCH")
    if registry.get("default") != "DENY" or registry.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY":
        raise ValueError("INVALID_REGISTRY_POLICY")
    if registry.get("anchor_repo") != "nexusomegac27/NEXUS-OMEGA-EVIDENCE":
        raise ValueError("INVALID_REGISTRY_REPOSITORY")
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
    for k, pattern in (("source_commit", HEX40), ("source_sha256", HEX64), ("source_git_blob", HEX40)):
        require_hex(claim[k], pattern)
    if type(claim["source_bytes"]) is not int or claim["source_bytes"] <= 0:
        raise ValueError("INVALID_CLAIM_BYTES")
    for k in ("source_bytes_rehashed", "source_blob_rehashed", "claims_independent_receiver_ack",
              "claims_expert_research_executed"):
        if type(claim[k]) is not bool:
            raise ValueError("INVALID_CLAIM_BOOLEAN")
    for k in ("owner_login", "actor_login"):
        if type(claim[k]) is not str or not LOGIN.fullmatch(claim[k]):
            raise ValueError("INVALID_CLAIM_ACTOR")
    if claim["actor_origin"] not in ("GITHUB_API", "SELF_DECLARED", "UNKNOWN"):
        raise ValueError("INVALID_ACTOR_ORIGIN")
    if claim["receipt_origin"] not in ("EXTERNAL_GITHUB_ASSET", "OWNER_MEDIATED_FILE", "OWNER_ISSUE_COMMENT"):
        raise ValueError("INVALID_RECEIPT_ORIGIN")
    if claim["owner_login"].lower() != owner.lower():
        raise ValueError("OWNER_MISMATCH")
    source_match = all((claim[k] == getattr(pins, k)) for k in
                       ("source_commit", "source_sha256", "source_bytes", "source_git_blob"))
    if not source_match:
        raise ValueError("SOURCE_PIN_MISMATCH")
    actor = claim["actor_login"].lower()
    policy_eligible = bool(
        claim["source_bytes_rehashed"] and claim["source_blob_rehashed"]
        and claim["claims_independent_receiver_ack"]
        and claim["actor_origin"] == "GITHUB_API"
        and claim["receipt_origin"] == "EXTERNAL_GITHUB_ASSET"
        and actor != owner.lower() and actor in {x.lower() for x in allow}
    )
    return {
        "policy_review_eligibility": "ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY" if policy_eligible else "NOT_ESTABLISHED",
        "independent_receiver_ack": "NOT_ESTABLISHED",
        "authenticated_github_actor": "NOT_ESTABLISHED",
        "expert_research_execution": "SOURCE_ASSERTED_ONLY" if claim["claims_expert_research_executed"] else "NOT_ESTABLISHED",
        "scientific_adjudication": "NOT_PERFORMED",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--registry-sha256", required=True)
    ap.add_argument("--source-commit", required=True)
    ap.add_argument("--source-sha256", required=True)
    ap.add_argument("--source-bytes", type=int, required=True)
    ap.add_argument("--source-git-blob", required=True)
    args = ap.parse_args()
    try:
        reg_raw, registry = parse_file(args.registry)
        _, claim = parse_file(args.claim)
        result = check(reg_raw, registry, claim, args)
        print(json.dumps({"ok": True, "result": result}, sort_keys=True))
    except (ValueError, OSError, UnicodeDecodeError, TypeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}, sort_keys=True))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
