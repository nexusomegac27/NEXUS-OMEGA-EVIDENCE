"""C1 isolated V3: pin all eight middle merge identities for PR 274-283.

References were read from ten independent GitHub compare calls on pinned main.
Structural-only; does not authenticate GitHub actors, API responses or file bytes.
"""
import json
import sys
import alpha_publication_cohort_boundary_anchor_guard_v2_20261102 as prior

MIDDLE_MERGES = (
    "3fef33f230f5cfbec75167811d0a12787f1847db",
    "71feb351c3e2436344a10b22b53ba19c946d73df",
    "b23cf96871608a18d21350f9c3df0fb075d9cec1",
    "265d760ce6a1e0e0bf4e526e48881d9ef55e3144",
    "9e5110ce84f2bd63bad1882d80a7ee6a219b448d",
    "c1aee5da5015e1108ceab049c7031180978c109d",
    "4e22d346006b67de332bfeb1f0ea68db8412fd70",
    "b7f966a886c88e015ac49f32efdf4bf7e31f1fea",
)

def evaluate(d):
    ok, reason = prior.evaluate(d)
    if not ok:
        return False, reason
    for i, expected in enumerate(MIDDLE_MERGES, start=1):
        if d["prs"][i]["merge_commit"] != expected:
            return False, "MIDDLE_MERGE_%d" % (i + 274)
    return True, "PASS_PINNED_COHORT_STRUCTURAL_ONLY"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("USAGE: guard manifest.json")
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            d = json.load(f)
        ok, reason = evaluate(d)
    except (OSError, ValueError, TypeError, RecursionError) as e:
        ok, reason = False, type(e).__name__
    print(json.dumps({"pass_test": ok, "reason": reason,
                      "scope": "STRUCTURAL_ONLY"}, sort_keys=True))
    sys.exit(0 if ok else 1)
