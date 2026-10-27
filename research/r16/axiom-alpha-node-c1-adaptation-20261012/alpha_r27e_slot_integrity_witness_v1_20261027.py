#!/usr/bin/env python3
"""Read-only C1 witness for the pinned R27-E external return slot registry.

Inspects caller-supplied JSON, NOT an authenticated GitHub API response.
Does not grant GitHub actor rights, enforce branch protection or alter runtime.
Historical registry source: main 6a6f2690f27615971791d88e11acc8c49f8f300e,
Git blob 1fabcab7f556e83621a3676ddfb3d11cdd964b55.
"""
import json
import sys

MAX_INPUT_BYTES = 65536
PARENT = "NEXUS_OMEGA_AXIOM_TO_EXISTING_CURSOR_R27_WWW_WAKE_AND_AUTHN_HARD_REMEDIATION_MAXI_ORDER_20261011_R0"
ROOT = "research/r27/www-extern-wake-isolation-20261011"
FILENAMES = (
    "R27-00_CAPABILITY_AND_TRUST_INVENTORY_R0.md",
    "R27-01_AUTHN_HARD_REMEDIATION_R0.md",
    "R27-02_NEGATIVE_TEST_RESULTS_R0.md",
    "R27-03_E0_E1_E2_CONTRACTS_R0.json",
    "R27-04_PROVIDER_FAILOVER_ASSESSMENT_R0.json",
    "R27-05_RETURN_MANIFEST_R0.json",
    "R27-06_SEND_RECEIPT_R0.md",
)
PROHIBITIONS = frozenset((
    "EXTERNAL_ROOT_OR_NAMESPACE_CREATION", "EXTERNAL_EDIT_EXISTING_FILES",
    "EXTERNAL_RENAME_DELETE_MOVE", "EXTERNAL_CREATE_SUBDIRECTORY",
    "EXTERNAL_PATCH_GOVERNANCE_CODE_CI", "EXTERNAL_CREATE_OWN_TEMPLATE",
    "AUTO_MERGE", "AUTO_RUNTIME", "NEW_WORKER",
))


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("NONFINITE_JSON")


def matches(actual, expected):
    return type(actual) is type(expected) and actual == expected


def audit(registry):
    if type(registry) is not dict:
        raise ValueError("INVALID_REGISTRY_SHAPE")
    expected = {
        "object": "NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1",
        "schema_version": "1.0.0",
        "status": "C1_OPERATOR_PREALLOCATED_SLOTS_EXTERNAL_ACTORS_NOT_AUTHORIZED",
        "authority": "NEXUS_OPERATOR_GOVERNED_ONLY",
        "default": "DENY",
        "owner_github_login": "nexusomegac27",
        "external_actor_allowlist": [],
        "identity_policy": "GITHUB_LOGIN_NOT_MODEL_IDENTITY; EXTERNAL_WRITE_NEEDS_OPERATOR_ACTOR_REGISTRATION_AND_BRANCH_RULE",
        "anchor_repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "max_files_per_external_return": 7,
        "max_file_bytes": 262144,
        "max_total_bytes": 1048576,
        "existing_frozen_return_paths": [],
        "structure_change": "OPERATOR_OWNED_PR_ONLY_UPDATE_ROOT_README_MACHINE_CONTRACT_AND_VALIDATOR",
        "manifest_self_hash": "EXCLUDED; MANIFEST_SHA256_POSTED_BY_RECEIVER_IN_PR_COMMENT",
        "legacy_rule": "HISTORICAL_PATH_BOUND_ASSETS_UNCHANGED",
    }
    drift = [key for key, value in expected.items()
             if not matches(registry.get(key), value)]
    assignments = registry.get("assignments")
    if type(assignments) is not list or len(assignments) != 1 or type(assignments[0]) is not dict:
        drift.append("assignments")
    else:
        expected_assignment = {
            "assignment_id": "R27-E-20261011",
            "scope": "ADVERSARIAL_EXTERNAL_RESEARCH_NOT_RUNTIME",
            "root": ROOT,
            "returns_path": ROOT + "/returns/",
            "parent_order_object": PARENT,
            "parent_order_sha256": "619f4463a865b801d652cd38dbecfeaa4178d8a559cb73d314893ef34f3310f1",
            "status": "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED",
            "filenames": list(FILENAMES),
            "required_complete_return": True,
        }
        drift.extend("assignments[0]." + key for key, value in expected_assignment.items()
                     if not matches(assignments[0].get(key), value))
    prohibited = registry.get("prohibited")
    if (type(prohibited) is not list or any(type(x) is not str for x in prohibited)
            or len(prohibited) != len(set(prohibited)) or set(prohibited) != PROHIBITIONS):
        drift.append("prohibited")
    return {
        "state": "HOLD_SCOPED_REGISTRY_CONTRACT_DRIFT" if drift else "PASS_PINNED_REGISTRY_SNAPSHOT_C1",
        "drift_fields": sorted(set(drift)),
        "api_origin_authenticated": False,
        "external_actor_authorized": False,
        "github_ruleset_enforcement_verified": False,
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("INPUT_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant)
        print(json.dumps(audit(data), sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
