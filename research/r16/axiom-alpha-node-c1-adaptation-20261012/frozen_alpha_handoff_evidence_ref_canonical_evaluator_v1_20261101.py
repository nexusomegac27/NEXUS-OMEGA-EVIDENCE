"""Frozen independent C1 subprocess oracle for evidence_ref canonicalization.
Synthetic inputs only; expected results are defined independently of the V4 implementation.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

BASE = {
    "coverage_complete": True,
    "coverage_source": "SYNTHETIC_NOT_AUTHENTICATED",
    "pinned_commit": "a" * 40,
    "attempts": [
        {"attempt_id": f"attempt-{i}", "evidence_ref": f"gh:receipt:{i}",
         "routine": True, "public": True, "authorized": True,
         "accessible": True, "completed": True, "operator_nudge": False,
         "receipt_verified": True}
        for i in range(3)
    ],
}
READY = ("METRIC_READY_STRUCTURAL_ONLY", 3, 3)
CLOSED = ("NOT_COMPUTABLE", None, None)


def cases():
    def ref(value, i=1):
        obj = copy.deepcopy(BASE)
        obj["attempts"][i]["evidence_ref"] = value
        return obj

    yield "positive_baseline", copy.deepcopy(BASE), READY
    yield "positive_distinct_composed_unicode", ref("gh:café:2"), READY
    yield "positive_case_sensitive", ref("GH:receipt:1"), READY
    yield "positive_internal_punctuation", ref("gh:receipt/2026-11_01"), READY
    obj = copy.deepcopy(BASE)
    obj["attempts"][1]["completed"] = False
    yield "regression_failed_attempt_in_denominator", obj, ("METRIC_READY_STRUCTURAL_ONLY", 3, 2)
    yield "regression_exact_duplicate", ref("gh:receipt:0"), CLOSED
    obj = copy.deepcopy(BASE)
    obj["coverage_complete"] = False
    yield "regression_incomplete_coverage", obj, CLOSED

    # These ten negative fixtures are accepted by the immutable V3 baseline.
    yield "negative_single_padded", ref(" gh:receipt:1 "), CLOSED
    yield "negative_single_nfd", ref("gh:cafe\u0301:1"), CLOSED
    yield "negative_zero_width_joiner", ref("gh:re\u200dceipt:1"), CLOSED
    yield "negative_embedded_nul", ref("gh:\u0000receipt:1"), CLOSED
    yield "negative_embedded_newline", ref("gh:receipt:\n1"), CLOSED
    yield "negative_single_nbsp_padding", ref("\u00a0gh:receipt:1\u00a0"), CLOSED
    yield "negative_single_tab_suffix", ref("gh:receipt:1\t"), CLOSED
    yield "negative_bom_format", ref("gh:\ufeffreceipt:1"), CLOSED
    obj = copy.deepcopy(BASE)
    obj["attempts"][0]["evidence_ref"] = "gh:café:1"
    obj["attempts"][1]["evidence_ref"] = "gh:cafe\u0301:1"
    yield "negative_nfc_nfd_alias", obj, CLOSED
    obj = copy.deepcopy(BASE)
    obj["attempts"][0]["evidence_ref"] = "gh:receipt:1"
    obj["attempts"][1]["evidence_ref"] = "gh:receipt:\u200d1"
    yield "negative_invisible_alias", obj, CLOSED


def main(path):
    passed = total = 0
    for name, obj, expected in cases():
        total += 1
        run = subprocess.run([sys.executable, str(path)],
                             input=json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                             capture_output=True, timeout=10, check=False)
        try:
            actual = json.loads(run.stdout) if run.returncode == 0 else {}
        except ValueError:
            actual = {}
        observed = (actual.get("status"), actual.get("eligible_denominator"),
                    actual.get("automated_numerator"))
        ok = observed == expected
        passed += ok
        print(json.dumps({"case": name, "expected": expected,
                          "observed": observed, "pass": ok}, ensure_ascii=False,
                         sort_keys=True))
    print(json.dumps({"passed": passed, "total": total,
                      "scope": "SYNTHETIC_ONLY"}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
