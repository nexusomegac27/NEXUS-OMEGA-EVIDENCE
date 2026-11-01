"""Independent frozen 16-case oracle for canonical attempt IDs (C1).
Expected outputs are fixed before the V3 candidate is authored or committed.
Synthetic inputs only; this does not authenticate receipts or census coverage.
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
    def change_id(value, index=1):
        obj = copy.deepcopy(BASE)
        obj["attempts"][index]["attempt_id"] = value
        return obj

    yield "positive_baseline", copy.deepcopy(BASE), ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    obj = copy.deepcopy(BASE)
    obj["attempts"][0]["attempt_id"] = "é-1"
    obj["attempts"][1]["attempt_id"] = "é-2"
    yield "positive_distinct_nfc_unicode", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    obj = copy.deepcopy(BASE)
    obj["attempts"][0]["attempt_id"] = "Case"
    obj["attempts"][1]["attempt_id"] = "case"
    yield "positive_case_sensitive", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    yield "positive_internal_punctuation", change_id("attempt:2026/11-01"), ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["completed"] = False
    yield "regression_failed_attempt_denominator", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 2)
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["evidence_ref"] = obj["attempts"][0]["evidence_ref"]
    yield "regression_duplicate_evidence_ref", obj, ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["coverage_complete"] = False
    yield "regression_incomplete_coverage", obj, ("NOT_COMPUTABLE", None, None)

    # Nine held-out negatives: V2 uses raw string identity and accepts all nine.
    yield "negative_leading_space_alias", change_id(" a0"), ("NOT_COMPUTABLE", None, None)
    yield "negative_trailing_space_alias", change_id("a0 "), ("NOT_COMPUTABLE", None, None)
    yield "negative_tab_alias", change_id("\ta0\n"), ("NOT_COMPUTABLE", None, None)
    yield "negative_nbsp_alias", change_id("\u00a0a0\u00a0"), ("NOT_COMPUTABLE", None, None)
    obj = copy.deepcopy(BASE)
    obj["attempts"][0]["attempt_id"] = "é"
    obj["attempts"][1]["attempt_id"] = "e\u0301"
    yield "negative_unicode_nfd_nfc_alias", obj, ("NOT_COMPUTABLE", None, None)
    yield "negative_zero_width_format", change_id("a\u200db"), ("NOT_COMPUTABLE", None, None)
    yield "negative_embedded_nul", change_id("a\u0000b"), ("NOT_COMPUTABLE", None, None)
    yield "negative_single_padded_id", change_id(" a1 "), ("NOT_COMPUTABLE", None, None)
    yield "negative_single_nfd_id", change_id("e\u0301"), ("NOT_COMPUTABLE", None, None)


def main(path):
    total = passed = 0
    for name, obj, expected in cases():
        total += 1
        proc = subprocess.run([sys.executable, str(path)], input=json.dumps(obj).encode("utf-8"),
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
    print(json.dumps({"passed": passed, "total": total, "scope": "SYNTHETIC_ONLY"}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
