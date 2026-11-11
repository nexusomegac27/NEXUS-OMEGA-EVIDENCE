#!/usr/bin/env python3
"""C1-only PRE-ENTRY POLICY check for the existing Agent Communication Framework.

No network, owner credentials, system/device writes or trust promotion. Passing this
validator DOES NOT authorize live transport, a public writable API, private transfer,
an autonomous receiver, or Pixel 9a activation. It prevents contradictory release
claims from entering the versioned governance pipeline, pending real independent
witness connectors and protected GitHub branch / owner review.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

POLICY = Path(__file__).resolve().parents[1] / (
    "research/communication/github-only-exchange-enforcement-20261029/"
    "NEXUS_COMMUNICATION_GATE_ADMISSION_STATE_V1_20261101.json"
)

class GatePolicyError(ValueError):
    pass

def require_equal(obj: dict[str, Any], key: str, value: Any, scope: str) -> None:
    actual = obj.get(key)
    if type(actual) is not type(value) or actual != value:
        raise GatePolicyError(f"{scope}.{key}: expected {value!r}; observed {actual!r}")

def require_sha(value: Any, kind: str) -> None:
    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise GatePolicyError(f"{kind}: must be immutable 40-hex commit")

def validate(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise GatePolicyError("root must be JSON object")
    for key, val in [
        ("schema", "nexus-omega-communication-gate-admission-v1"),
        ("claim_ceiling", "C1_DESCRIPTIVE_ONLY"),
        ("release_class", "C1_LOCAL_POLICY_PREENTRY_ONLY"),
        ("v1_architecture", "CLOSED_LIVING"),
    ]:
        require_equal(state, key, val, "root")
    lanes: dict[str, dict[str, Any]] = {}
    for lane in (
        "public_www", "github_document_router", "real_receiver",
        "owner_cutover", "private_source", "pixel9a_second_twin",
        "symbiosis",
    ):
        item = state.get(lane)
        if not isinstance(item, dict):
            raise GatePolicyError(f"{lane}: required object")
        lanes[lane] = item

    pub, doc, rx = lanes["public_www"], lanes["github_document_router"], lanes["real_receiver"]
    owner, private, pixel, sy = lanes["owner_cutover"], lanes["private_source"], lanes["pixel9a_second_twin"], lanes["symbiosis"]
    require_equal(pub, "state", "LIVE_READ_ONLY_CONFIRMED_AT_RECORDED_CHECK", "public_www")
    require_equal(pub, "write_api", "OFF", "public_www")
    require_equal(pub, "no_account_required_for_public_read", True, "public_www")
    if not str(pub.get("last_proof") or "").startswith(
        "https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/actions/runs/"
    ):
        raise GatePolicyError("public_www.last_proof: expected prior immutable CI witness link; status does not establish continuous uptime")
    require_equal(doc, "state", "STAGED", "github_document_router")
    require_equal(doc, "ci_at_tested_commit", "16_OF_16_SUCCESS", "github_document_router")
    require_equal(doc, "unit_suite", "29_OF_29_SUCCESS", "github_document_router")
    require_equal(doc, "repaired_negatives", "15_OF_15_PASS", "github_document_router")
    require_equal(doc, "baseline_defects", "12_OF_12_FAIL_EXPECTED", "github_document_router")
    require_sha(doc.get("tested_commit"), "github_document_router.tested_commit")
    # The CI summary is an already externally checked historical fact in this
    # report, NOT an input proof authorizing an execution.
    for k in (
        "state", "source_fetch_by_receiver", "github_distinct_principal",
        "return_source_independently_verified",
    ):
        require_equal(rx, k, "NOT_ESTABLISHED", "real_receiver")
    for k, v in [
        ("state", "NO"), ("authorization", "NOT_INDEPENDENTLY_PROVEN"),
        ("rollback", "NOT_INDEPENDENTLY_PROVEN"), ("platform_delivery", "NOT_ESTABLISHED"),
    ]:
        require_equal(owner, k, v, "owner_cutover")
    for k, v in [
        ("state", "HOLD"), ("transport", "NOT_ESTABLISHED"),
        ("permission", "NOT_ESTABLISHED"), ("raw_to_public_github", "PROHIBITED"),
    ]:
        require_equal(private, k, v, "private_source")
    for k, v in [
        ("state", "NOT_ADMITTED"), ("phase", "READ_ONLY_OFFLINE_PREFLIGHT_ONLY"),
        ("dual_device_sync", "NOT_AUTHORIZED"), ("live_sensor_relay", "NOT_AUTHORIZED"),
        ("raw_sensor_cloud_upload", "NOT_AUTHORIZED"), ("opt_in", "REQUIRED_EXPLICIT"),
        ("previous_oppo_evidence_reverification", "REQUIRED_BEFORE_NEW_PIXEL_ACTION"),
    ]:
        require_equal(pixel, k, v, "pixel9a_second_twin")
    for k, v in [
        ("state", "C1_FEEDBACK_LOOP_RESEARCH_ONLY"),
        ("human_authority", "OPERATOR"),
        ("agent_identity", "NOT_ATTESTED_BY_MODEL_LABEL"),
        ("claim_of_consciousness", "NOT_ESTABLISHED"),
    ]:
        require_equal(sy, k, v, "symbiosis")
    violations=state.get("violations_always_fail")
    if not isinstance(violations, list) or len(violations) < 8 or len(set(violations)) != len(violations):
        raise GatePolicyError("violations_always_fail must hold >=8 distinct security regression classes")
    if not all(isinstance(i,str) and i.strip() for i in violations):
        raise GatePolicyError("violations_always_fail contains invalid marker")
    if state.get("next_release_requirement") != "EXACT_SOURCE_BOUND_VERIFIER_API_AND_RETURN_BLOB_FETCH_PLUS_OWNER_RIGHTS_AND_ROLLBACK_BEFORE_CUTOVER":
        raise GatePolicyError("missing real trusted source/cutover requirement")
    if state.get("publication_policy") != "DO_NOT_DEPLOY_THIS_LOCAL_POLICY_FILE_AS_LIVE_WEB_STATUS_WITHOUT_SEPARATE_RELEASE_AND_REMOTE_BYTES_CHECK":
        raise GatePolicyError("missing separate WWW release guard")
    return {
        "object": state["object"],
        "policy_preentry": "PASS_STAGED_CONTRACT",
        "document_transport": "HOLD_NOT_LIVE_ATTESTED",
        "external_receiver": "NOT_ESTABLISHED",
        "private_material": "HOLD",
        "pixel9a_second_twin": "NOT_ADMITTED",
        "public_www": "HISTORIC_READ_ONLY_PROOF_ONLY",
        "cutover_authorization": "NOT_GRANTED_BY_POLICY_VALIDATION",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=POLICY)
    args=parser.parse_args(argv)
    try:
        state=json.loads(args.state.read_text(encoding="utf-8"))
        verdict=validate(state)
    except (OSError, ValueError, KeyError, TypeError, GatePolicyError) as e:
        print(json.dumps({"policy_preentry":"FAIL_CLOSED","reason":str(e),"claim_ceiling":"C1_DESCRIPTIVE_ONLY"},sort_keys=True))
        return 2
    print(json.dumps(verdict,sort_keys=True))
    return 0

if __name__=="__main__":
    sys.exit(main())
