#!/usr/bin/env python3
"""Independent subprocess black-box test for C1 policy-pin gate; synthetic fixtures."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REGISTRY = {
    "object": "NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1",
    "default": "DENY",
    "owner_github_login": "nexusomegac27",
    "external_actor_allowlist": [],
    "anchor_repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
    "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
}
CLAIM = {
    "source_commit": "dab7c59070d67e7e2a244bd6d05db9a4d37460e3",
    "source_sha256": "60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5",
    "source_bytes": 4380,
    "source_git_blob": "4e31f92be1f673f49a2c27e570b5849e754cca78",
    "source_bytes_rehashed": True,
    "source_blob_rehashed": True,
    "owner_login": "nexusomegac27",
    "actor_login": "nexusomegac27",
    "actor_origin": "GITHUB_API",
    "receipt_origin": "OWNER_MEDIATED_FILE",
    "claims_independent_receiver_ack": True,
    "claims_expert_research_executed": True,
}


def check_case(path, name, registry_delta=None, claim_delta=None, expected="NOT_ESTABLISHED",
               repin=False, registry_raw=None, claim_raw=None, pins_delta=None):
    registry = copy.deepcopy(REGISTRY)
    registry.update(registry_delta or {})
    claim = copy.deepcopy(CLAIM)
    claim.update(claim_delta or {})
    baseline = (json.dumps(REGISTRY, sort_keys=True) + "\n").encode()
    rb = registry_raw if registry_raw is not None else (json.dumps(registry, sort_keys=True) + "\n").encode()
    cb = claim_raw if claim_raw is not None else (json.dumps(claim, sort_keys=True) + "\n").encode()
    with tempfile.TemporaryDirectory() as d:
        rp, cp = Path(d)/"registry.json", Path(d)/"claim.json"
        rp.write_bytes(rb)
        cp.write_bytes(cb)
        pins = {
            "--registry-sha256": hashlib.sha256(rb if repin else baseline).hexdigest(),
            "--source-commit": CLAIM["source_commit"],
            "--source-sha256": CLAIM["source_sha256"],
            "--source-bytes": str(CLAIM["source_bytes"]),
            "--source-git-blob": CLAIM["source_git_blob"],
        }
        pins.update(pins_delta or {})
        cmd = [sys.executable, path, "--registry", str(rp), "--claim", str(cp)]
        for k, v in pins.items():
            cmd += [k, v]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        try:
            output = json.loads(p.stdout)
        except Exception as exc:
            raise AssertionError(f"{name}: non-JSON {p.stdout[:150]}") from exc
        if expected == "ERROR":
            good = p.returncode == 2 and output.get("ok") is False
        else:
            result = output.get("result", {})
            good = (p.returncode == 0 and output.get("ok") is True
                    and result.get("policy_review_eligibility") == expected
                    and result.get("independent_receiver_ack") == "NOT_ESTABLISHED"
                    and result.get("authenticated_github_actor") == "NOT_ESTABLISHED"
                    and result.get("scientific_adjudication") == "NOT_PERFORMED"
                    and result.get("claim_ceiling") == "C1_DESCRIPTIVE_ONLY")
        print(("PASS " if good else "FAIL ") + name)
        if not good:
            raise AssertionError(f"{name}: {p.returncode} {output}")


def main(path):
    cases = [
        ("owner_ack_rejected", {}),
        ("claim_forged_allowlist_field_rejected", {"claim_delta": {"external_actor_allowlist": ["reviewer"]}, "expected": "ERROR"}),
        ("external_actor_unregistered_rejected", {"claim_delta": {"actor_login": "reviewer", "actor_origin": "GITHUB_API", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}}),
        ("external_actor_self_declared_rejected", {"claim_delta": {"actor_login": "reviewer", "actor_origin": "SELF_DECLARED", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}}),
        ("registry_allowlist_mutation_unpinned", {"registry_delta": {"external_actor_allowlist": ["reviewer"]}, "expected": "ERROR"}),
        ("registry_default_allow_rejected", {"registry_delta": {"default": "ALLOW"}, "repin": True, "expected": "ERROR"}),
        ("registry_wrong_repo_rejected", {"registry_delta": {"anchor_repo": "other/repo"}, "repin": True, "expected": "ERROR"}),
        ("claim_owner_mismatch_rejected", {"claim_delta": {"owner_login": "imposter"}, "expected": "ERROR"}),
        ("source_sha_mutation_rejected", {"claim_delta": {"source_sha256": "0"*64}, "expected": "ERROR"}),
        ("source_byte_mutation_rejected", {"claim_delta": {"source_bytes": 4381}, "expected": "ERROR"}),
        ("source_byte_bool_rejected", {"claim_delta": {"source_bytes": True}, "expected": "ERROR"}),
        ("duplicate_registry_key_rejected", {"registry_raw": b'{"default":"DENY","default":"DENY"}', "expected": "ERROR"}),
        ("duplicate_claim_key_rejected", {"claim_raw": (json.dumps(CLAIM)[:-1]+',"source_bytes":4380}').encode(), "expected": "ERROR"}),
        ("nonfinite_claim_rejected", {"claim_raw": (json.dumps(CLAIM)[:-1]+',"source_bytes":NaN}').encode(), "expected": "ERROR"}),
        ("future_registered_only_review_eligible", {"registry_delta": {"external_actor_allowlist": ["reviewer"]}, "claim_delta": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET"}, "repin": True, "expected": "ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY"}),
        ("source_not_rehashed_rejected", {"registry_delta": {"external_actor_allowlist": ["reviewer"]}, "claim_delta": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET", "source_bytes_rehashed": False}, "repin": True}),
        ("owner_bridge_rejected", {"registry_delta": {"external_actor_allowlist": ["reviewer"]}, "claim_delta": {"actor_login": "reviewer"}, "repin": True}),
        ("no_ack_claim_rejected", {"registry_delta": {"external_actor_allowlist": ["reviewer"]}, "claim_delta": {"actor_login": "reviewer", "receipt_origin": "EXTERNAL_GITHUB_ASSET", "claims_independent_receiver_ack": False}, "repin": True}),
        ("bad_registry_pin_rejected", {"pins_delta": {"--registry-sha256": "a"*64}, "expected": "ERROR"}),
        ("zero_source_pin_rejected", {"pins_delta": {"--source-bytes": "0"}, "expected": "ERROR"}),
    ]
    for name, kw in cases:
        check_case(path, name, **kw)
    print(f"RESULT {len(cases)}/{len(cases)} PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py candidate.py")
    main(sys.argv[1])
