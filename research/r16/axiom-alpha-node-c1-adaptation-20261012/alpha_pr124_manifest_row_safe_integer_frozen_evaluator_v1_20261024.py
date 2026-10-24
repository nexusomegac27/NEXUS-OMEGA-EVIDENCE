"""Frozen independent JSON Schema evaluator for Alpha Run121.

Research-only; no network, GitHub writes, runtime authority or scientific claim.
Inputs are local schema files. This evaluator must precede the candidate commit.
"""
import copy
import json
import sys
from jsonschema import Draft202012Validator

BASE = {
    "path": "research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_PR124_PINNED_DISCOVERY_INDEX_20261024_R0.json",
    "bytes": 8561,
    "sha256": "45308605c40df5b868b28ba2befb7c50351eacbfc0497b02e4577e89b46c90e7",
    "git_blob_sha1": "ef56ed01ad34a8ee44fd97ccb4a3ab0ad3589b38",
}
# This fixed test matrix is independent of the proposed candidate schema.
CASES = (
    ("valid_historical", None, True),
    ("valid_minimum", 1, True),
    ("valid_safe_maximum", 9007199254740991, True),
    ("invalid_zero", 0, False),
    ("invalid_negative", -1, False),
    ("invalid_boolean", True, False),
    ("unsafe_first_integer", 9007199254740992, False),
    ("unsafe_next_integer", 9007199254740993, False),
    ("unsafe_very_large_integer", 10**30, False),
    ("invalid_fractional", 1.5, False),
)


def evaluate(schema):
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    results = []
    for name, size, expected in CASES:
        row = copy.deepcopy(BASE)
        if size is not None:
            row["bytes"] = size
        observed = validator.is_valid(row)
        results.append({"id": name, "expected": expected,
                        "observed": observed, "pass": observed == expected})
    return {"correct": sum(x["pass"] for x in results),
            "total": len(results), "cases": results}


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: evaluator.py baseline.json candidate.json")
    with open(sys.argv[1], encoding="utf-8") as stream:
        baseline = json.load(stream)
    with open(sys.argv[2], encoding="utf-8") as stream:
        candidate = json.load(stream)
    old, new = evaluate(baseline), evaluate(candidate)
    result = {"baseline": old, "candidate": new,
              "baseline_expected_correct": 7,
              "candidate_expected_correct": 10,
              "falsifier": "A numeric byte length outside +/-2^53-1 is accepted by candidate schema",
              "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}
    print(json.dumps(result, sort_keys=True))
    return 0 if old["correct"] == 7 and new["correct"] == 10 else 2


if __name__ == "__main__":
    sys.exit(main())
