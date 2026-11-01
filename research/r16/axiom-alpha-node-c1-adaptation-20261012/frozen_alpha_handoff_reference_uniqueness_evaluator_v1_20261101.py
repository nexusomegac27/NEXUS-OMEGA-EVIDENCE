"""Frozen independent oracle for unique attempt-level evidence references.
Expected outputs are specified here, separate from the guard under test.
Synthetic fixtures only; not a GitHub authenticity or census-completeness test.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

BASE = {
    "coverage_complete": True,
    "coverage_source": "SYNTHETIC_ONLY",
    "pinned_commit": "a" * 40,
    "attempts": [
        {"attempt_id": f"a{i}", "evidence_ref": f"gh:receipt:{i}",
         "routine": True, "public": True, "authorized": True,
         "accessible": True, "completed": True,
         "operator_nudge": False, "receipt_verified": True}
        for i in range(3)
    ],
}

def cases():
    yield "unique_positive", copy.deepcopy(BASE), ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = obj["attempts"][0]["evidence_ref"]
    yield "duplicate_success_reference", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = " " + obj["attempts"][0]["evidence_ref"] + " "
    yield "whitespace_alias_reference", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = obj["attempts"][0]["evidence_ref"]
    obj["attempts"][1]["completed"] = False
    yield "success_failure_same_reference", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = obj["attempts"][0]["evidence_ref"]
    obj["attempts"][1]["public"] = False
    yield "ineligible_duplicate_reference", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = "gh:receipt:0#attempt:1"
    yield "distinct_fragment_reference", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["attempt_id"] = obj["attempts"][0]["attempt_id"]
    yield "duplicate_attempt_id", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = "   "
    yield "blank_evidence_ref", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["completed"] = False
    yield "eligible_failure_counted", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 2)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["operator_nudge"] = True
    yield "manual_nudge_excluded_from_numerator", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 2)
    obj = copy.deepcopy(BASE)
    del obj["attempts"][1]["accessible"]
    yield "missing_accessibility", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["coverage_complete"] = False
    yield "incomplete_coverage", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    for row in obj["attempts"]:
        row["public"] = False
    yield "zero_eligible", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["public"] = False
    yield "private_excluded", obj, ("METRIC_READY_STRUCTURAL_ONLY", 2, 2)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = "\t" + obj["attempts"][0]["evidence_ref"] + "\n"
    yield "unicode_whitespace_alias", obj, ("NOT_COMPUTABLE", None, None)

def main(path):
    passed = 0
    for name, obj, expected in cases():
        proc = subprocess.run([sys.executable, str(path)], input=json.dumps(obj).encode(),
                              capture_output=True, timeout=10, check=False)
        try:
            data = json.loads(proc.stdout) if proc.returncode == 0 else {}
        except ValueError:
            data = {}
        observed = (data.get("status"), data.get("eligible_denominator"),
                    data.get("automated_numerator"))
        ok = observed == expected
        passed += int(ok)
        print(json.dumps({"case": name, "expected": expected,
                          "observed": observed, "pass": ok}, sort_keys=True))
    print(json.dumps({"passed": passed, "total": 15, "scope": "SYNTHETIC_ONLY"}, sort_keys=True))
    return 0 if passed == 15 else 1

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1
                  else Path(__file__).with_name("alpha_handoff_reference_uniqueness_guard_v2_20261101.py")))
