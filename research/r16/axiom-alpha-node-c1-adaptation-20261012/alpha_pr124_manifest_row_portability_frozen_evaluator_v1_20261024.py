"""Frozen Run122 evaluator: path portability, research-only.

Oracle is fixed before the candidate schema commit. Python jsonschema Draft202012
4.26.0; no network, GitHub write, production or scientific adjudication.
"""
import copy
import json
import sys
from jsonschema import Draft202012Validator

PREFIX = "research/r16/axiom-alpha-node-c1-adaptation-20261012/"
BASE = {
    "path": PREFIX + "ALPHA_PR124_PINNED_DISCOVERY_INDEX_20261024_R0.json",
    "bytes": 8561,
    "sha256": "45308605c40df5b868b28ba2befb7c50351eacbfc0497b02e4577e89b46c90e7",
    "git_blob_sha1": "ef56ed01ad34a8ee44fd97ccb4a3ab0ad3589b38",
}
# Immutable expected decisions, not generated from the proposed schema.
CASES = [
    ("historical_valid", "ALPHA_PR124_PINNED_DISCOVERY_INDEX_20261024_R0.json", True),
    ("ordinary_valid", "alpha-file_v3.json", True),
    ("device_lookalike_valid", "CONTEXT.py", True),
    ("com10_valid", "COM10.txt", True),
    ("basename_255_valid", "a" * 255, True),
    ("device_con", "CON", False),
    ("device_con_extension", "con.txt", False),
    ("device_prn", "PRN", False),
    ("device_aux_extension", "AuX.json", False),
    ("device_nul_extension", "nul.md", False),
    ("device_com1", "COM1", False),
    ("device_com9_extension", "cOm9.py", False),
    ("device_lpt1", "LPT1", False),
    ("device_lpt9_extension", "lPt9.txt", False),
    ("device_con_double_extension", "CON..md", False),
    ("trailing_dot", "valid.", False),
    ("trailing_double_dot", "valid..", False),
    ("basename_256_invalid", "a" * 256, False),
    ("traversal_invalid", "../escape.py", False),
    ("nested_invalid", "sub/file.py", False),
    ("unicode_invalid", "alpha\u00e9.py", False),
]

def evaluate(schema):
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    out = []
    for name, filename, expected in CASES:
        row = copy.deepcopy(BASE)
        row["path"] = PREFIX + filename
        observed = validator.is_valid(row)
        out.append({"id": name, "expected": expected, "observed": observed,
                    "pass": observed == expected})
    for name, field, value in [
        ("unsafe_integer", "bytes", 9007199254740992),
        ("invalid_sha", "sha256", "z" * 64),
        ("invalid_blob", "git_blob_sha1", "z" * 40),
    ]:
        row = copy.deepcopy(BASE)
        row[field] = value
        observed = validator.is_valid(row)
        out.append({"id": name, "expected": False, "observed": observed,
                    "pass": not observed})
    return {"correct": sum(r["pass"] for r in out), "total": len(out),
            "negative_total": sum(not r["expected"] for r in out), "cases": out}

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: frozen_portability_evaluator.py baseline.json candidate.json")
    with open(sys.argv[1], encoding="utf-8") as stream:
        baseline = json.load(stream)
    with open(sys.argv[2], encoding="utf-8") as stream:
        candidate = json.load(stream)
    old, new = evaluate(baseline), evaluate(candidate)
    print(json.dumps({"baseline": old, "candidate": new,
                      "falsifier": "A reserved Windows device name, trailing dot or >255-byte basename is accepted, or a valid control is rejected",
                      "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}, sort_keys=True))
    return 0 if new["correct"] == new["total"] and old["correct"] < old["total"] else 2

if __name__ == "__main__":
    sys.exit(main())
