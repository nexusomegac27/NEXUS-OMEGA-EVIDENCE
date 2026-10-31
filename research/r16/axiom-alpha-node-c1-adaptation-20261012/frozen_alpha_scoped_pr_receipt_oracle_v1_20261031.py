#!/usr/bin/env python3
"""Frozen, offline structural oracle for a *bounded* GitHub PR/receipt projection.
No network, authentication, API completeness or operational-metric claims.
"""
import copy
import json
import re
import sys

H40 = re.compile(r"[0-9a-f]{40}\Z")
OWNER = "nexusomegac27"
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"


def no_duplicate_keys(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError("duplicate_json_key")
        d[key] = value
    return d


def valid_sha(value):
    return isinstance(value, str) and H40.fullmatch(value) is not None


def evaluate(data):
    faults = []
    if not isinstance(data, dict) or data.get("schema_version") != "alpha_pr_receipt_v1":
        return {"status": "FAIL_CLOSED", "faults": ["ENVELOPE"]}
    scope = data.get("scope")
    records = data.get("records")
    if (not isinstance(scope, dict) or scope.get("repository") != REPO
            or type(scope.get("first_pr")) is not int or type(scope.get("last_pr")) is not int
            or not valid_sha(scope.get("initial_parent")) or not valid_sha(scope.get("pinned_main"))
            or not isinstance(records, list) or len(records) != scope["last_pr"] - scope["first_pr"] + 1
            or scope["first_pr"] != 228 or scope["last_pr"] != 237):
        return {"status": "FAIL_CLOSED", "faults": ["SCOPE_OR_CARDINALITY"]}
    parent = scope["initial_parent"]
    receipt_parents = 0
    for offset, record in enumerate(records):
        number = scope["first_pr"] + offset
        if not isinstance(record, dict):
            faults.append(f"{number}:NOT_OBJECT")
            continue
        fields = ("pr_head", "pr_base", "merge_commit", "git_commit", "git_parent",
                  "receipt_main", "receipt_head")
        if any(not valid_sha(record.get(k)) for k in fields):
            faults.append(f"{number}:INVALID_SHA_FIELD")
            continue
        tests = (
            (type(record.get("pr")) is int and record["pr"] == number, "PR_NUMBER"),
            (record.get("pr_merged") is True, "MERGE_NOT_PROVEN"),
            (record.get("git_parent_count") == 1 and type(record.get("git_parent_count")) is int, "PARENT_COUNT"),
            (record["pr_base"] == parent, "BASE_CHAIN"),
            (record["git_parent"] == parent, "GIT_PARENT_CHAIN"),
            (record["git_commit"] == record["merge_commit"], "MERGE_COMMIT"),
            (type(record.get("receipt_pr")) is int and record["receipt_pr"] == number, "RECEIPT_PR"),
            (type(record.get("receipt_id")) is int and record["receipt_id"] > 0, "RECEIPT_ID"),
            (record.get("receipt_actor") == OWNER, "RECEIPT_ACTOR"),
            (record["receipt_main"] == record["merge_commit"], "RECEIPT_MAIN"),
            (record["receipt_head"] == record["pr_head"], "RECEIPT_HEAD"),
            (record.get("claim_ceiling") == "C1_DESCRIPTIVE_ONLY", "CLAIM_CEILING"),
        )
        faults.extend(f"{number}:{tag}" for ok, tag in tests if not ok)
        rp = record.get("receipt_parent")
        if rp is not None:
            receipt_parents += 1
            if not valid_sha(rp) or rp != parent:
                faults.append(f"{number}:RECEIPT_PARENT")
        parent = record["merge_commit"]
    if parent != scope["pinned_main"]:
        faults.append("PINNED_MAIN_MISMATCH")
    if len({x.get("receipt_id") for x in records if isinstance(x, dict)}) != len(records):
        faults.append("DUPLICATE_RECEIPT_ID")
    return {"status": "SCOPED_API_PROJECTION_CONSISTENT" if not faults else "FAIL_CLOSED",
            "scope_prs": len(records), "matched": len(records) if not faults else None,
            "receipt_parents_explicit": receipt_parents, "faults": faults,
            "full_source_byte_readback_rate": "NOT_COMPUTABLE",
            "project_automation_rate": "NOT_COMPUTABLE",
            "project_full_readback_rate": "NOT_COMPUTABLE"}


def selftest(data):
    assert evaluate(data)["status"] == "SCOPED_API_PROJECTION_CONSISTENT", "POSITIVE"
    mutants = [
        ("receipt_main", lambda x: x["records"][2].update(receipt_main="f"*40)),
        ("receipt_id", lambda x: x["records"][3].update(receipt_id=x["records"][2]["receipt_id"])),
        ("git_parent", lambda x: x["records"][4].update(git_parent="0"*40)),
        ("pr_base", lambda x: x["records"][5].update(pr_base="0"*40)),
        ("receipt_actor", lambda x: x["records"][6].update(receipt_actor="expert")),
        ("pr_merged", lambda x: x["records"][7].update(pr_merged=False)),
        ("receipt_head", lambda x: x["records"][8].update(receipt_head="e"*40)),
        ("dropped_record", lambda x: x["records"].pop()),
        ("missing_sha", lambda x: x["records"][1].pop("git_commit")),
        ("claim_promotion", lambda x: x["records"][0].update(claim_ceiling="C2")),
    ]
    for name, mutate in mutants:
        bad = copy.deepcopy(data)
        mutate(bad)
        assert evaluate(bad)["status"] == "FAIL_CLOSED", name
    return {"oracle": "FROZEN_SCOPED_PR_RECEIPT_ORACLE_V1", "positive": 1,
            "negative": len(mutants), "negative_detected": len(mutants)}


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw, object_pairs_hook=no_duplicate_keys,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite_json")))
        result = evaluate(data)
        if "--selftest" in sys.argv and result["status"] != "FAIL_CLOSED":
            result["selftest"] = selftest(data)
    except (ValueError, TypeError, KeyError, RecursionError, AssertionError) as exc:
        result = {"status": "FAIL_CLOSED", "faults": [type(exc).__name__ + ":" + str(exc)]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "SCOPED_API_PROJECTION_CONSISTENT" else 2


if __name__ == "__main__":
    sys.exit(main())
