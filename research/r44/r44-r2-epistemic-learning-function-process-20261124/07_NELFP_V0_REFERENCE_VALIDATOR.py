"""NELFP-v0 research-only static evidence gate.
Synthetic unit tests only; no network, agent execution, model training or deployment.
This reference validator is NOT a PROV-O/RO-Crate conformance implementation.
"""
import hashlib
import json
import re
import sys

Q_LEVELS = {"Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "QX"}
STATUSES = {"RESEARCH_DESIGN_C1", "SOURCE_RECEIVED_C1", "LOCAL_REPLAY_VERIFIED_C1", "HOLD"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def adjudicate(r):
    findings = []
    if r.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY":
        findings.append("CLAIM_CEILING_INVALID")
    if r.get("status") not in STATUSES:
        findings.append("STATUS_INVALID")
    if r.get("source_q") not in Q_LEVELS:
        findings.append("SOURCE_Q_INVALID")
    if r.get("source_q") in {"Q4", "Q5"}:
        if not r.get("original_bytes_received") or not HEX64.fullmatch(str(r.get("original_sha256", ""))):
            findings.append("Q4_WITHOUT_ORIGINAL_BYTES")
    if r.get("source_q") == "Q5" and not r.get("external_independent_replay"):
        findings.append("Q5_WITHOUT_INDEPENDENT_REPLAY")
    if r.get("status") == "LOCAL_REPLAY_VERIFIED_C1":
        run = r.get("run") or {}
        if not (isinstance(run.get("passed"), int) and isinstance(run.get("total"), int)
                and run["total"] > 0 and run["passed"] == run["total"] and run.get("exit_code") == 0):
            findings.append("LOCAL_PASS_WITH_FAILED_TEST_OR_EXIT")
    w = r.get("window_counts")
    if isinstance(w, dict) and all(k in w for k in ("total", "train", "test")):
        if min(w.values()) < 0 or w["train"] + w["test"] > w["total"]:
            findings.append("WINDOW_COUNTS_INCONSISTENT")
    if isinstance(r.get("elapsed_seconds"), (int, float)) and r["elapsed_seconds"] < 0:
        findings.append("NEGATIVE_ELAPSED_DURATION")
    if r.get("canonical_credit") and r.get("external_role") != r.get("canonical_role"):
        findings.append("ROLE_NAMESPACE_SUBSTITUTION")
    if r.get("claims_two_smartphones") and r.get("sensor_topology") != "TWO_SIMULTANEOUS_SMARTPHONES":
        findings.append("SOURCE_TOPOLOGY_SUBSTITUTION")
    if r.get("claims_full_cohort") and r.get("sample_subjects", 0) <= 1:
        findings.append("SAMPLE_CLAIMED_AS_COHORT")
    if r.get("claimed_authenticated_quorum", 0) > r.get("operator_registered_distinct_actors", 0):
        findings.append("UNAUTHENTICATED_ACTOR_QUORUM")
    if r.get("claims_final_archive") and r.get("embedded_receipt_bytes") != r.get("actual_zip_bytes"):
        findings.append("STALE_EMBEDDED_RECEIPT")
    if r.get("claims_adaptive_gain") and r.get("frozen_adaptive_metric") == r.get("frozen_baseline_metric"):
        findings.append("NO_GAIN_PRIMARY_NOT_PRESERVED")
    if r.get("claims_blind_holdout") and r.get("test_label_overlap"):
        findings.append("HOLDOUT_CONTAMINATED")
    if r.get("claims_physical_authorization"):
        findings.append("RESEARCH_CLAIM_CANNOT_AUTHORIZE_PHYSICAL")
    if findings:
        return {"verdict": "REJECTED_SCOPED_CLAIM", "codes": sorted(set(findings))}
    if r.get("status") == "HOLD":
        return {"verdict": "HOLD_WITH_NEGATIVE_EVIDENCE_PRESERVED", "codes": []}
    return {"verdict": "ACCEPTED_ONLY_WITHIN_DECLARED_C1_SCOPE", "codes": []}


def selftest():
    base = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY", "status": "LOCAL_REPLAY_VERIFIED_C1",
            "source_q": "Q4", "original_bytes_received": True,
            "original_sha256": "1" * 64, "run": {"passed": 51, "total": 51, "exit_code": 0}}
    tests = [
        ("local_toy_green", {}, "ACCEPTED_ONLY_WITHIN_DECLARED_C1_SCOPE"),
        ("original_math_33_of_51", {"run": {"passed": 33, "total": 51, "exit_code": 1}}, "LOCAL_PASS_WITH_FAILED_TEST_OR_EXIT"),
        ("q4_missing_bytes", {"original_bytes_received": False}, "Q4_WITHOUT_ORIGINAL_BYTES"),
        ("impossible_mhealth_windows", {"window_counts": {"total": 3356, "train": 3921633, "test": 1708057}}, "WINDOW_COUNTS_INCONSISTENT"),
        ("negative_duration", {"elapsed_seconds": -15759.254}, "NEGATIVE_ELAPSED_DURATION"),
        ("external_E27_alias", {"canonical_credit": True, "canonical_role": "E27_ANDROID", "external_role": "E27_AGENT_INDEPENDENCE"}, "ROLE_NAMESPACE_SUBSTITUTION"),
        ("wearable_vs_phone", {"claims_two_smartphones": True, "sensor_topology": "SHIMMER_WEARABLES"}, "SOURCE_TOPOLOGY_SUBSTITUTION"),
        ("fda_one_subject_full_cohort", {"claims_full_cohort": True, "sample_subjects": 1}, "SAMPLE_CLAIMED_AS_COHORT"),
        ("self_reported_quorum", {"claimed_authenticated_quorum": 3, "operator_registered_distinct_actors": 0}, "UNAUTHENTICATED_ACTOR_QUORUM"),
        ("b05_receipt", {"claims_final_archive": True, "embedded_receipt_bytes": 10336, "actual_zip_bytes": 11447}, "STALE_EMBEDDED_RECEIPT"),
        ("r43_primary_no_gain", {"claims_adaptive_gain": True, "frozen_adaptive_metric": 18.303982903117085, "frozen_baseline_metric": 18.303982903117085}, "NO_GAIN_PRIMARY_NOT_PRESERVED"),
        ("holdout_overlap", {"claims_blind_holdout": True, "test_label_overlap": True}, "HOLDOUT_CONTAMINATED"),
        ("source_only_q5", {"source_q": "Q5", "external_independent_replay": False}, "Q5_WITHOUT_INDEPENDENT_REPLAY"),
        ("physical_claim", {"claims_physical_authorization": True}, "RESEARCH_CLAIM_CANNOT_AUTHORIZE_PHYSICAL"),
        ("honest_hold", {"status": "HOLD", "source_q": "QX"}, "HOLD_WITH_NEGATIVE_EVIDENCE_PRESERVED"),
    ]
    rows = []
    for name, changes, expected in tests:
        r = dict(base, **changes)
        result = adjudicate(r)
        actual = result["verdict"] if expected in {"ACCEPTED_ONLY_WITHIN_DECLARED_C1_SCOPE", "HOLD_WITH_NEGATIVE_EVIDENCE_PRESERVED"} else (expected if expected in result["codes"] else "NOT_DETECTED")
        rows.append({"fixture": name, "expected": expected, "actual": actual, "match": actual == expected})
    out = {"object": "R44_R2_NELFP_V0_SYNTHETIC_REFERENCE_TEST", "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
           "actual_source_data_executed": False, "actor_authentication": False,
           "passed": sum(x["match"] for x in rows), "total": len(rows), "checks": rows}
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        result = selftest()
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["passed"] == result["total"] else 1)
    print("Usage: python r44_r2_reference_gate.py --selftest", file=sys.stderr)
    sys.exit(2)
