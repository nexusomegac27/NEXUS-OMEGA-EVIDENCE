#!/usr/bin/env python3
"""Frozen black-box oracle for source-byte gate V2. Synthetic fixtures, separate subprocess."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REG = {"default": "DENY", "owner_github_login": "nexusomegac27",
       "external_actor_allowlist": [], "anchor_repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
       "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}
SOURCE = b"R10-C1\r\nimmutable-test-source\x00end\n"
SHA = hashlib.sha256(SOURCE).hexdigest()
BLOB = hashlib.sha1(b"blob " + str(len(SOURCE)).encode() + b"\0" + SOURCE).hexdigest()
CLAIM = {"source_commit": "d" * 40, "source_sha256": SHA,
         "source_bytes": len(SOURCE), "source_git_blob": BLOB,
         "owner_login": "nexusomegac27", "actor_login": "nexusomegac27",
         "actor_origin": "GITHUB_API", "receipt_origin": "OWNER_MEDIATED_FILE",
         "claims_independent_receiver_ack": True, "claims_expert_research_executed": True}


def case(candidate, name, reg_change=None, claim_change=None, source=None,
         reg_raw=None, claim_raw=None, pins_change=None, repin=False,
         outcome="NOT_ESTABLISHED", error=None):
    registry = copy.deepcopy(REG)
    registry.update(reg_change or {})
    claim = copy.deepcopy(CLAIM)
    claim.update(claim_change or {})
    canonical = (json.dumps(REG, sort_keys=True) + "\n").encode()
    rb = reg_raw if reg_raw is not None else (json.dumps(registry, sort_keys=True) + "\n").encode()
    cb = claim_raw if claim_raw is not None else (json.dumps(claim, sort_keys=True) + "\n").encode()
    sb = SOURCE if source is None else source
    pins = {"registry-sha256": hashlib.sha256(rb if repin else canonical).hexdigest(),
            "source-commit": CLAIM["source_commit"], "source-sha256": SHA,
            "source-bytes": str(len(SOURCE)), "source-git-blob": BLOB}
    pins.update(pins_change or {})
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for fname, content in (("registry", rb), ("claim", cb), ("source", sb)):
            (root / fname).write_bytes(content)
        command = [sys.executable, candidate]
        for key in ("registry", "claim", "source"):
            command += ["--" + key, str(root / key)]
        for key, value in pins.items():
            command += ["--" + key, value]
        p = subprocess.run(command, text=True, capture_output=True, timeout=5)
        try:
            obj = json.loads(p.stdout)
        except ValueError as exc:
            raise AssertionError(f"{name}: invalid output {p.stdout[:200]}") from exc
        if error is not None:
            good = p.returncode == 2 and obj.get("ok") is False and obj.get("error") == error
        else:
            result = obj.get("result", {})
            good = (p.returncode == 0 and obj.get("ok") is True
                    and result.get("source_bytes_sha256_git_blob") == "MATCH"
                    and result.get("registry_sha256") == "MATCH"
                    and result.get("policy_review_eligibility") == outcome
                    and result.get("independent_receiver_ack") == "NOT_ESTABLISHED"
                    and result.get("authenticated_github_actor") == "NOT_ESTABLISHED"
                    and result.get("scientific_adjudication") == "NOT_PERFORMED"
                    and result.get("claim_ceiling") == "C1_DESCRIPTIVE_ONLY")
        if not good:
            raise AssertionError(f"FAIL {name}: rc={p.returncode} {obj}")
        print("PASS " + name)


def main(candidate):
    bad = "SOURCE_BYTES_HASH_BLOB_MISMATCH"
    tests = [
        ("owner_ack_not_independent", {}),
        ("same_length_source_mutation", {"source": SOURCE.replace(b"test", b"tEst"), "error": bad}),
        ("source_append_mutation", {"source": SOURCE + b"!", "error": bad}),
        ("source_truncated", {"source": SOURCE[:-1], "error": bad}),
        ("source_empty", {"source": b"", "error": "SOURCE_SIZE_LIMIT"}),
        ("source_false_hash_pin", {"pins_change": {"source-sha256": "0"*64}, "error": bad}),
        ("source_false_blob_pin", {"pins_change": {"source-git-blob": "0"*40}, "error": bad}),
        ("source_false_byte_pin", {"pins_change": {"source-bytes": str(len(SOURCE)+1)}, "error": bad}),
        ("claim_source_hash_mutation", {"claim_change": {"source_sha256": "0"*64}, "error": "CLAIM_SOURCE_PIN_MISMATCH"}),
        ("claim_source_commit_mutation", {"claim_change": {"source_commit": "a"*40}, "error": "CLAIM_SOURCE_PIN_MISMATCH"}),
        ("claim_injects_rehashed_flag", {"claim_change": {"source_bytes_rehashed": True}, "error": "INVALID_CLAIM_FIELDS"}),
        ("claim_injects_allowlist", {"claim_change": {"external_actor_allowlist": ["reviewer"]}, "error": "INVALID_CLAIM_FIELDS"}),
        ("registry_unpinned_allowlist_mutation", {"reg_change": {"external_actor_allowlist": ["reviewer"]}, "error": "REGISTRY_SHA256_MISMATCH"}),
        ("registry_repin_wrong_default", {"reg_change": {"default": "ALLOW"}, "repin": True, "error": "INVALID_REGISTRY_POLICY"}),
        ("registry_repin_wrong_repo", {"reg_change": {"anchor_repo": "other/repo"}, "repin": True, "error": "INVALID_REGISTRY_REPO"}),
        ("duplicate_claim_json_key", {"claim_raw": (json.dumps(CLAIM)[:-1]+',"source_bytes":32}').encode(), "error": "DUPLICATE_JSON_KEY"}),
        ("duplicate_registry_json_key", {"reg_raw": b'{"default":"DENY","default":"DENY"}', "error": "DUPLICATE_JSON_KEY"}),
        ("nonfinite_claim", {"claim_raw": (json.dumps(CLAIM)[:-1]+',"source_bytes":NaN}').encode(), "error": "NONFINITE"}),
        ("bool_source_bytes", {"claim_change": {"source_bytes": True}, "error": "INVALID_CLAIM_SOURCE_BYTES"}),
        ("external_unregistered", {"claim_change": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}}),
        ("future_allowlisted_review_only", {"reg_change": {"external_actor_allowlist": ["reviewer"]}, "claim_change": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}, "repin": True, "outcome": "ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY"}),
        ("owner_never_external", {"reg_change": {"external_actor_allowlist": ["nexusomegac27"]}, "claim_change": {"receipt_origin": "EXTERNAL_GITHUB_ASSET"}, "repin": True}),
        ("external_self_declared", {"reg_change": {"external_actor_allowlist": ["reviewer"]}, "claim_change": {"actor_login": "reviewer", "actor_origin": "SELF_DECLARED", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}, "repin": True}),
        ("external_without_ack_claim", {"reg_change": {"external_actor_allowlist": ["reviewer"]}, "claim_change": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET", "claims_independent_receiver_ack": False}, "repin": True}),
    ]
    for name, kw in tests:
        case(candidate, name, **kw)
    print(f"RESULT {len(tests)}/{len(tests)} PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: frozen_oracle.py candidate.py")
    main(sys.argv[1])
