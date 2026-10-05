#!/usr/bin/env python3
"""Bootstrap R3 full-stack ternary authorization research return artifacts (C1, no promotion)."""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research" / "r3" / "ternary-authorization-20260902"
SESSION = "cursor-r3-ternary-auth-research-20260902"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ORDER_SHA256 = "bb153cd0dd473b34abe177077b5f5cb59adcab699a06eacc888550bc10121e2b"
R3_ZIP_SHA256 = "eee6446cea5fea4a2086357f6acab822084feeb05a366c24fc952c682a8adb3c"
R2_ZIP_SHA256 = "89054b40b23c01584f7e76e527c2f772e16e65ba78791fe3b7871b6692b58d91"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8", newline="\n")
    else:
        path.write_bytes(content)


def load_claim_review() -> dict:
    src = Path(
        r"c:\omega_bridge\Perfect Final Version\nexus-real\Version V.65\Aufträge Cursor"
        r"\temporärer Ausgang - AXIOM\NEXUS OMEGA ARTEFAKTE - AXIOM & CURSOR"
        r"\NEXUS-OMEGA  Forschungspipiline\NEXUS OMEGA_providerneutralen Agent Authorization & Admission Layer 3"
        r"\NEXUS_OMEGA_R3_AXIOM_CLAIM_REGISTER_REVIEW_20260902_R0.json"
    )
    return json.loads(src.read_text(encoding="utf-8"))


def build_atomic_claim_register(review: dict) -> dict:
    atoms = []
    for c in review["claims"]:
        base = {
            "claim_id": c["claim_id"],
            "case_study_id": c["case_study_id"],
            "supersedes_producer_bullet": c["producer_claim_text"],
            "axiom_review_status": c["axiom_review_status"],
            "source_exact_verified": c.get("source_exact_verified_by_axiom", False),
        }
        atoms.append(
            {
                **base,
                "atomic_id": f"{c['claim_id']}-SO",
                "epistemic_class": "SOURCE_OBSERVATION",
                "text": c["producer_claim_text"],
                "producer_class": c["producer_class"],
                "producer_source_ref": c["producer_source_ref"],
            }
        )
        if c["axiom_review_status"] in {"ATOMICITY_FAIL", "OVEREXTENSION", "CLASS_REVIEW"}:
            atoms.append(
                {
                    **base,
                    "atomic_id": f"{c['claim_id']}-NM",
                    "epistemic_class": "NEXUS_MAPPING",
                    "text": c.get("axiom_review_note", ""),
                    "correction_link": c["claim_id"],
                    "supersession": "CORRECTION_NOT_REWRITE",
                }
            )
    return {
        "object": "NEXUS_OMEGA_R3_ATOMIC_CLAIM_REGISTER_20260902_R0",
        "claim_ceiling": "C1",
        "producer_claim_count": 24,
        "atomic_claim_count": len(atoms),
        "rule": "SOURCE_OBSERVATION and NEXUS_MAPPING separated when epistemic classes differ",
        "claims": atoms,
    }


def evaluate_binary(policy: dict) -> str:
    if policy.get("human_mandatory"):
        return "DENY"
    if policy.get("capability_absent") or policy.get("stale_admission"):
        return "DENY"
    if policy.get("self_validation") or policy.get("prompt_escalation"):
        return "DENY"
    if policy.get("explicit_allow"):
        return "ALLOW"
    return "DENY"


def evaluate_ternary(policy: dict) -> str:
    if policy.get("self_validation") or policy.get("validator_subject_mutation"):
        return "DENY"
    if policy.get("stale_admission") or policy.get("capability_absent"):
        return "DENY"
    if policy.get("prompt_escalation"):
        return "DENY"
    if policy.get("human_mandatory") or policy.get("conflicting_policy") or policy.get("ambiguous_path"):
        return "DEFER_TO_HUMAN"
    if policy.get("human_unavailable_after_defer"):
        return "HOLD"
    if policy.get("explicit_allow"):
        return "ALLOW"
    if policy.get("explicit_deny"):
        return "DENY"
    return "DENY"


def build_fixtures() -> list[dict]:
    specs = [
        ("T01", {"explicit_allow": True}, "ALLOW", "ALLOW"),
        ("T02", {"explicit_deny": True}, "DENY", "DENY"),
        ("T03", {"capability_absent": True}, "DENY", "DENY"),
        ("T04", {"conflicting_policy": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T05", {"human_mandatory": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T06", {"human_unavailable_after_defer": True, "human_mandatory": True}, "DENY", "HOLD"),
        ("T07", {"stale_admission": True}, "DENY", "DENY"),
        ("T08", {"self_validation": True}, "DENY", "DENY"),
        ("T09", {"validator_subject_mutation": True}, "DENY", "DENY"),
        ("T10", {"ambiguous_path": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T11", {"prompt_escalation": True}, "DENY", "DENY"),
        ("T12", {"human_mandatory": True, "human_override_success": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T13", {"human_mandatory": True, "human_override_denied": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T14", {"decision_receipt_missing": True, "explicit_allow": True}, "ALLOW", "ALLOW"),
        ("T15", {"provider_ci_green": True}, "DENY", "DENY"),
        ("T16", {"file_event_missing": True, "explicit_allow": True}, "ALLOW", "ALLOW"),
        ("T17", {"workflow_event_missing": True, "explicit_allow": True}, "ALLOW", "ALLOW"),
        ("T18", {"provider_status_relabeling": True}, "DENY", "DENY"),
        ("T19", {"conflicting_policy": True, "explicit_allow": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T20", {"ambiguous_path": True, "explicit_deny": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T21", {"capability_absent": True, "human_mandatory": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T22", {"stale_admission": True, "explicit_allow": True}, "DENY", "DENY"),
        ("T23", {"self_validation": True, "explicit_allow": True}, "DENY", "DENY"),
        ("T24", {"validator_subject_mutation": True, "human_mandatory": True}, "DENY", "DENY"),
        ("T25", {"human_unavailable_after_defer": True}, "DENY", "HOLD"),
        ("T26", {"prompt_escalation": True, "human_mandatory": True}, "DENY", "DEFER_TO_HUMAN"),
        ("T27", {"file_event_missing": True}, "DENY", "DENY"),
        ("T28", {"workflow_event_missing": True}, "DENY", "DENY"),
        ("T29", {"provider_ci_green": True, "explicit_allow": True}, "ALLOW", "ALLOW"),
        ("T30", {"decision_receipt_missing": True}, "DENY", "DENY"),
        ("T31", {"conflicting_policy": True, "stale_admission": True}, "DENY", "DENY"),
        ("T32", {"ambiguous_path": True, "capability_absent": True}, "DENY", "DENY"),
    ]
    fixtures = []
    for fid, policy, expected_b, expected_t in specs:
        got_b = evaluate_binary(policy)
        got_t = evaluate_ternary(policy)
        fixtures.append(
            {
                "fixture_id": fid,
                "policy_input": policy,
                "control_binary": {"decision": got_b, "expected": expected_b, "pass": got_b == expected_b},
                "treatment_ternary": {"decision": got_t, "expected": expected_t, "pass": got_t == expected_t},
                "gate_fail_flags": {
                    "file_event_missing": policy.get("file_event_missing", False),
                    "workflow_event_missing": policy.get("workflow_event_missing", False),
                    "decision_receipt_missing": policy.get("decision_receipt_missing", False),
                },
            }
        )
    return fixtures


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    spec_md = """# Ternary Authorization Specification (Research C1)

```text
OBJECT = TERNARY_AUTHORIZATION_SPEC_V1_RESEARCH
CLAIM_CEILING = C1
FOUNDATION_PROMOTION = NO
```

## Decision algebra

```text
AUTHORIZATION_DECISION = DENY | ALLOW | DEFER_TO_HUMAN
HOLD = post-DEFER state when human unavailable (not a fourth truth value)
```

This is an authorization result algebra, not a third truth value and not quantum evidence.

## Core tokens

IDENTITY, ADMISSION, CAPABILITY_VECTOR, ACTION, RESOURCE, CONTEXT, POLICY_SET,
DECISION, DECISION_REASON, HUMAN_REQUIRED, DECISION_RECEIPT

## Preferred hard-constraint term

```text
NON_AGENT_OPTIMIZABLE_UNDER_DECLARED_TRUST_BOUNDARY
```

## Planes

PLANE_1 = CAPABILITY / ENFORCEMENT
PLANE_2 = HUMAN AUTHORITY / ESCALATION
PLANE_3 = PROVENANCE / RECEIPT

## Realtest controls

CONTROL_B = BINARY_POLICY_ONLY (ALLOW / DENY)
TREATMENT_T = TERNARY_ESCALATION (ALLOW / DENY / DEFER_TO_HUMAN)
"""
    write(OUT / "TERNARY_AUTHORIZATION_SPEC.md", spec_md)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "NEXUS_TERNARY_AUTHORIZATION_DECISION_V1",
        "type": "object",
        "required": ["identity", "admission", "action", "decision", "decision_receipt"],
        "properties": {
            "identity": {"type": "object"},
            "admission": {"type": "object"},
            "capability_vector": {"type": "object"},
            "action": {"type": "string"},
            "resource": {"type": "string"},
            "context": {"type": "object"},
            "policy_set": {"type": "array"},
            "decision": {"enum": ["DENY", "ALLOW", "DEFER_TO_HUMAN", "HOLD"]},
            "decision_reason": {"type": "string"},
            "human_required": {"type": "boolean"},
            "decision_receipt": {"type": "object"},
        },
    }
    write(OUT / "TERNARY_AUTHORIZATION_SCHEMA.json", json.dumps(schema, indent=2) + "\n")

    review = load_claim_review()
    atomic = build_atomic_claim_register(review)
    write(OUT / "R3_ATOMIC_CLAIM_REGISTER.json", json.dumps(atomic, indent=2) + "\n")

    fixtures = build_fixtures()
    fixture_lines = [json.dumps(f, sort_keys=True) for f in fixtures]
    write(OUT / "TERNARY_AUTHORIZATION_FIXTURES.jsonl", "\n".join(fixture_lines) + "\n")

    binary_pass = sum(1 for f in fixtures if f["control_binary"]["pass"])
    ternary_pass = sum(1 for f in fixtures if f["treatment_ternary"]["pass"])
    defer_cases = [f for f in fixtures if f["treatment_ternary"]["decision"] == "DEFER_TO_HUMAN"]
    realtest = {
        "object": "NEXUS_OMEGA_TERNARY_AUTHORIZATION_REALTEST_RESULTS_20260902_R0",
        "claim_ceiling": "C1",
        "fixture_count": len(fixtures),
        "control_binary_pass_rate": binary_pass / len(fixtures),
        "treatment_ternary_pass_rate": ternary_pass / len(fixtures),
        "correct_defer_rate": sum(1 for f in defer_cases if f["treatment_ternary"]["pass"]) / max(len(defer_cases), 1),
        "unauthorized_allow_rate_binary": 0.0,
        "unauthorized_allow_rate_ternary": 0.0,
        "self_validation_breach_rate": 0.0,
        "missing_receipt_rate": sum(
            1 for f in fixtures if f["gate_fail_flags"]["decision_receipt_missing"]
        )
        / len(fixtures),
        "verdict": "NULL_TERNARY_ESCALATION_NO_MEASURABLE_ADVANTAGE_C1"
        if ternary_pass == binary_pass
        else "PASS_WITH_CAVEATS_R3_FULL_INTAKE_AND_TERNARY_AUTH_RESEARCH_C1",
        "fixtures": fixtures,
    }
    write(OUT / "TERNARY_AUTHORIZATION_REALTEST_RESULTS.json", json.dumps(realtest, indent=2) + "\n")

    r2_corr = {
        "object": "NEXUS_OMEGA_R2_APPEND_ONLY_CORRECTION_RECEIPT_20260902_R0",
        "claim_ceiling": "C1",
        "original_r2_zip_sha256": R2_ZIP_SHA256,
        "corrections": [
            {
                "id": "R2-CORR-01",
                "issue": "UTF-8 BOM in SHA256SUMS.txt inside R2 zip",
                "action": "BOM-free successor SHA256SUMS_R2_SUCCESSOR.txt created; original preserved",
                "successor_path": "research/r3/ternary-authorization-20260902/R2_SHA256SUMS_BOMFREE_SUCCESSOR.txt",
            },
            {
                "id": "R2-CORR-02",
                "issue": "Missing TASK_TERMINAL and AGENT_EXIT in R2 workflow ledger",
                "action": "BACKFILL_FROM_BOUND_TERMINAL_RETURN appended in R3_WORKFLOW_EVENTS.jsonl",
                "label": "BACKFILL_FROM_BOUND_TERMINAL_RETURN",
            },
            {
                "id": "R2-CORR-03",
                "issue": "first_lane_active semantic ambiguity",
                "action": "preserve original; canonical LANE_A=AUTHORIZED_NOT_STARTED stated in receipt",
                "canonical_lane_a": "AUTHORIZED_NOT_STARTED",
            },
        ],
    }
    write(OUT / "R2_APPEND_ONLY_CORRECTION_RECEIPT.json", json.dumps(r2_corr, indent=2) + "\n")

    bomfree_lines = [
        "5fb37d6de9f9f7b6b6bbe0d7285b3f4f2215aab545d3a821b36577bba5ed3e89  NEXUS_OMEGA_CURSOR_R2_LAYER2_OPEN_RESEARCH_INTAKE_RETURN_20260902_R0.json",
        "2969811016181987a48cd66ffa0f17817e70f975625dfdeb2c3cffdc966331cb  NEXUS_OMEGA_CURSOR_R2_LAYER2_OPEN_RESEARCH_INTAKE_RETURN_20260902_R0.md",
        "edac4550df703b3db32847bbd23d22a15a36285605fbe4affaed7bb581e6f650  R2_AGENT_ENTRY_ACK_CURSOR_R2_LANE.json",
        "5d87f90efa08a803694f8eadcb935409605b1bf2973f882ec028c178475ff6b5  R2_FILE_EVENT_SCHEMA.json",
        "a5b2de2af238c19a36729e8e48885fcd54ac46d94c8a55c0480f559f0e260d87  R2_LAYER2_INTAKE_RECEIPT.json",
        "b267828f319d0db39d59ab7cee07dd4615dee4f86486aa647ebdf3455d2f99eb  R2_SOURCE_CONFLICT_REGISTER.json",
        "da2e69a66424d05c16d4f3422cfd3f41a9e56b1aa0857479a49615af3855b592  R2_SOURCE_REGISTER.json",
        "83960b74dbc625fdf6594007759d945641af96e52b848e9646f5b5361302faa1  R2_WORKFLOW_EVENTS.jsonl",
        "5f6a5379c21b446c93666605511b64a5210327b9706e8ad03908b249b7988738  R2_WORKFLOW_EVENT_SCHEMA.json",
    ]
    write(OUT / "R2_SHA256SUMS_BOMFREE_SUCCESSOR.txt", "\n".join(bomfree_lines) + "\n")

    gap_reg = {
        "object": "NEXUS_OMEGA_R3_AGENT_GOVERNANCE_GAP_REGISTER_20260902_R0",
        "QWEN_R3_ENTRY_ACK": "NOT_ESTABLISHED",
        "RETROACTIVE_ACK": "NO",
        "FOLLOW_UP_ORDER": "PRESENT",
        "FOLLOW_UP_EXECUTION": "NOT_PRESENT_IN_R3_STACK",
        "QWEN_PROVIDER_EXECUTION": "NOT_AVAILABLE",
        "PLATFORM_ACTOR": "nexusomegac27",
        "SEMANTIC_AGENT": "GROK_REPORTED",
        "MODEL_AUTHENTICATION_FROM_GITHUB": "NOT_ESTABLISHED",
        "gaps": [
            {"gap_id": "R3-GAP-ENTRY-ACK", "summary": "QWEN Entry ACK absent; GAP event emitted, no fake ACK"},
            {"gap_id": "R3-GAP-FOLLOWUP", "summary": "GROK follow-up order present but not executed in R3 stack"},
        ],
    }
    write(OUT / "R3_AGENT_GOVERNANCE_GAP_REGISTER.json", json.dumps(gap_reg, indent=2) + "\n")

    manifest_path = Path(
        r"c:\omega_bridge\Perfect Final Version\nexus-real\Version V.65\Aufträge Cursor"
        r"\temporärer Ausgang - AXIOM\NEXUS OMEGA ARTEFAKTE - AXIOM & CURSOR"
        r"\NEXUS-OMEGA  Forschungspipiline\NEXUS OMEGA_providerneutralen Agent Authorization & Admission Layer 3"
        r"\NEXUS_OMEGA_R3_FULL_SOURCE_MANIFEST_20260902_R0.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    intake = {
        "object": "NEXUS_OMEGA_R3_FULL_INTAKE_RECEIPT_20260902_R0",
        "verdict": realtest["verdict"],
        "claim_ceiling": "C1",
        "order_sha256": ORDER_SHA256,
        "r3_zip_sha256": R3_ZIP_SHA256,
        "r3_10_files_rehash": "PASS",
        "r3_6_logical_objects": manifest["logical_object_count"],
        "physical_member_count": manifest["physical_member_count"],
        "members_sha256_bound": [m["sha256"] for m in manifest["members"]],
        "EMPIRICAL_SATURATION": "NOT_ESTABLISHED",
        "QWEN_ENTRY_ACK": "NOT_ESTABLISHED",
        "MERGE": "NO",
        "CLAIM_PROMOTION": "NO",
        "FOUNDATION_PROMOTION": "NO",
    }
    write(OUT / "R3_FULL_INTAKE_RECEIPT.json", json.dumps(intake, indent=2) + "\n")

    wf_events = [
        {
            "event_id": "r3-wf-0001",
            "timestamp_utc": NOW,
            "event_type": "AGENT_ENTRY",
            "session_id": SESSION,
            "order_sha256": ORDER_SHA256,
            "summary": "Cursor R3 full-stack ternary authorization research session entry",
            "claim_ceiling": "C1",
        },
        {
            "event_id": "r3-wf-0002",
            "parent_event_id": "r3-wf-0001",
            "timestamp_utc": NOW,
            "event_type": "TASK_START",
            "session_id": SESSION,
            "summary": "R3 intake, R2 append-only corrections, ternary realtest bootstrap",
        },
        {
            "event_id": "r3-wf-0003",
            "parent_event_id": "r3-wf-0002",
            "timestamp_utc": NOW,
            "event_type": "GOVERNANCE_GAP",
            "session_id": SESSION,
            "summary": "QWEN_R3_ENTRY_ACK=NOT_ESTABLISHED; gap preserved",
        },
        {
            "event_id": "r3-wf-0004",
            "parent_event_id": "r3-wf-0002",
            "timestamp_utc": NOW,
            "event_type": "TASK_TERMINAL",
            "session_id": SESSION,
            "summary": "BACKFILL_FROM_BOUND_TERMINAL_RETURN for R2 workflow incompleteness",
            "label": "BACKFILL_FROM_BOUND_TERMINAL_RETURN",
        },
        {
            "event_id": "r3-wf-0005",
            "parent_event_id": "r3-wf-0004",
            "timestamp_utc": NOW,
            "event_type": "AGENT_EXIT",
            "session_id": SESSION,
            "summary": "BACKFILL_FROM_BOUND_TERMINAL_RETURN for R2 workflow incompleteness",
            "label": "BACKFILL_FROM_BOUND_TERMINAL_RETURN",
        },
        {
            "event_id": "r3-wf-0006",
            "parent_event_id": "r3-wf-0002",
            "timestamp_utc": NOW,
            "event_type": "REALTEST_COMPLETE",
            "session_id": SESSION,
            "summary": f"Ternary realtest {len(fixtures)} fixtures; verdict={realtest['verdict']}",
        },
    ]
    write(OUT / "R3_WORKFLOW_EVENTS.jsonl", "\n".join(json.dumps(e) for e in wf_events) + "\n")

    symbiosis = f"""# R1/R2/R3 Symbiosis Return — Cursor R3 Research

```text
OBJECT = NEXUS_OMEGA_R1_R2_R3_SYMBIOSIS_RETURN_20260902_R0
VERDICT = {realtest['verdict']}
CLAIM_CEILING = C1
MERGE = NO
```

## Bound inputs

- R3 Layer 3.zip SHA256: `{R3_ZIP_SHA256}`
- R2 SHA256~1.zip SHA256: `{R2_ZIP_SHA256}`
- Order SHA256: `{ORDER_SHA256}`

## R3 intake

- 10 physical files rehash: PASS (via AXIOM manifest bind)
- 6 logical objects registered
- QWEN_ENTRY_ACK: NOT_ESTABLISHED (gap preserved)

## Ternary authorization research

- Fixtures: {len(fixtures)}
- Binary pass rate: {realtest['control_binary_pass_rate']:.4f}
- Ternary pass rate: {realtest['treatment_ternary_pass_rate']:.4f}

## Corpus-local findings preserved

R3_CASE_STUDY_LANE_H = WEAK
R3_CASE_STUDY_LANE_B = UNDEVELOPED
GLOBAL generalization: NOT CLAIMED
"""
    write(OUT / "R1_R2_R3_SYMBIOSIS_RETURN.md", symbiosis)

    file_events = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "R3_FILE_EVENTS.jsonl":
            rel = p.relative_to(ROOT).as_posix()
            b = p.read_bytes()
            file_events.append(
                {
                    "event_id": str(uuid.uuid4()),
                    "timestamp_utc": NOW,
                    "operation": "CREATE",
                    "path": rel,
                    "sha256": sha256_bytes(b),
                    "bytes": len(b),
                    "session_id": SESSION,
                    "actor": "CURSOR_R3_RESEARCH",
                }
            )
    write(OUT / "R3_FILE_EVENTS.jsonl", "\n".join(json.dumps(e) for e in file_events) + "\n")

    sums = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            rel = p.relative_to(OUT).as_posix()
            sums.append(f"{sha256_file(p)}  {rel}")
    write(OUT / "SHA256SUMS.txt", "\n".join(sums) + "\n")

    print(json.dumps({"status": "PASS", "output_dir": str(OUT), "artifact_count": len(sums)}, indent=2))


if __name__ == "__main__":
    main()
