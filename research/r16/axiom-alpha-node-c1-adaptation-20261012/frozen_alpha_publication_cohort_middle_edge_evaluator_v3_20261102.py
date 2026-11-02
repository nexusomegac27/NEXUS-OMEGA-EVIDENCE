"""Frozen independent V3 cohort-middle-edge oracle, authored before candidate.

The expected chain was obtained by ten separate GitHub compare API reads
(parent -> merge, ahead=1, behind=0), pinned at main ccfd6c4168...
This is a structural C1 evaluator, NOT actor or source authenticity proof.
Do not edit this oracle as part of candidate repair.
"""
import copy
import importlib
import json
import sys
import frozen_alpha_publication_cohort_evaluator_v1_20261102 as v1
import alpha_publication_cohort_boundary_anchor_guard_v2_20261102 as v2

FIRST_PARENT = "964fe47c4bdbad599e0689b132ff73c0822f3518"
MERGES = (
    "3cc35487e8cae54aeac95377b6a8c376f412dc4f",
    "3fef33f230f5cfbec75167811d0a12787f1847db",
    "71feb351c3e2436344a10b22b53ba19c946d73df",
    "b23cf96871608a18d21350f9c3df0fb075d9cec1",
    "265d760ce6a1e0e0bf4e526e48881d9ef55e3144",
    "9e5110ce84f2bd63bad1882d80a7ee6a219b448d",
    "c1aee5da5015e1108ceab049c7031180978c109d",
    "4e22d346006b67de332bfeb1f0ea68db8412fd70",
    "b7f966a886c88e015ac49f32efdf4bf7e31f1fea",
    "7961026bf0f630aee160e083122c2900744d2da1",
)

def positive():
    d = v1.fixture()
    for i, p in enumerate(d["prs"]):
        p["parent_commit"] = FIRST_PARENT if i == 0 else MERGES[i - 1]
        p["merge_commit"] = MERGES[i]
    return d

def cases():
    yield "positive", positive(), True, True
    for i in range(1, 9):
        d = positive()
        fake = format(i, "x") * 40
        d["prs"][i]["merge_commit"] = fake
        d["prs"][i + 1]["parent_commit"] = fake
        yield "coforged_middle_%d" % i, d, True, False
    d = positive()
    d["prs"].pop()
    yield "missing_pr", d, False, False
    d = positive()
    d["prs"][0]["files"].pop()
    yield "missing_file", d, False, False
    d = positive()
    d["claim_ceiling"] = "C2"
    yield "claim_promotion", d, False, False
    d = positive()
    d["prs"][-1]["merge_commit"] = "0" * 40
    yield "last_main_swap", d, False, False
    d = positive()
    f = d["prs"][0]["files"][0]
    f["sha256"] = "f" * 64
    f["git_blob_sha1"] = "e" * 40
    f["github_blob_sha1"] = "e" * 40
    yield "residual_coforged_file_hashes", d, True, True

def run(mode):
    checker = v2 if mode == "baseline" else importlib.import_module(
        "alpha_publication_cohort_middle_edge_guard_v3_20261102")
    total = passed = 0
    for name, d, old, new in cases():
        total += 1
        observed, reason = checker.evaluate(copy.deepcopy(d))
        expected = old if mode == "baseline" else new
        ok = type(observed) is bool and observed is expected
        passed += ok
        print(json.dumps({"fixture": name, "expected": expected,
                          "observed": observed, "reason": reason,
                          "pass": ok}, sort_keys=True))
    print(json.dumps({"mode": mode, "passed": passed, "total": total,
                      "result": "PASS" if passed == total else "FAIL"},
                     sort_keys=True))
    return 0 if passed == total else 1

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("baseline", "candidate"):
        sys.exit("USAGE: frozen...py baseline|candidate")
    sys.exit(run(sys.argv[1]))
