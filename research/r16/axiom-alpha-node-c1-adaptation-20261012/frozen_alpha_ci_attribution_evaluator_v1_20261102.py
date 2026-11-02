"""Frozen, independent C1 oracle for check-run commit attribution and CI/science separation.

Synthetic offline fixtures only. Freeze before authoring the candidate. No GitHub
calls, model/runtime changes, or evaluator self-approval.
"""
import copy
import importlib.util
import json
import sys

HEAD = "a" * 40
OTHER = "b" * 40
TARGET = "frozen_alpha_cohort_decode_budget_evaluator_v6_20261102.py"


def load(path):
    spec = importlib.util.spec_from_file_location("candidate", path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def run(path):
    subject = load(path)
    good = [{"name": "validate" if i % 2 else "other", "head_sha": HEAD,
             "status": "completed", "conclusion": "success"} for i in range(8)]
    ref = ["jobs:\n  test:\n    steps:\n      - run: python " + TARGET + "\n"]
    no_ref = ["jobs:\n  test:\n    steps:\n      - run: python -m unittest tests.test_repository_structure\n"]
    cases = [
        ("green_no_science", good, no_ref, HEAD, TARGET, "CI_GREEN_NO_EXPLICIT_TEST_REFERENCE"),
        ("green_reference_only", good, ref, HEAD, TARGET, "CI_GREEN_REFERENCE_ONLY_NOT_EXECUTION"),
        ("comment_reference_not_proof", good, ["# " + TARGET], HEAD, TARGET, "CI_GREEN_REFERENCE_ONLY_NOT_EXECUTION"),
        ("wrong_head_one", [{**good[0], "head_sha": OTHER}] + good[1:], no_ref, HEAD, TARGET, "CHECK_HEAD_MISMATCH"),
        ("wrong_head_all", [{**c, "head_sha": OTHER} for c in good], no_ref, HEAD, TARGET, "CHECK_HEAD_MISMATCH"),
        ("failed_check", [{**good[0], "conclusion": "failure"}] + good[1:], no_ref, HEAD, TARGET, "CI_NOT_ALL_SUCCESS"),
        ("neutral_check", [{**good[0], "conclusion": "neutral"}] + good[1:], no_ref, HEAD, TARGET, "CI_NOT_ALL_SUCCESS"),
        ("empty_checks", [], no_ref, HEAD, TARGET, "INVALID_INPUT"),
        ("nontext_workflow", good, [123], HEAD, TARGET, "INVALID_INPUT"),
        ("bad_target", good, no_ref, HEAD, "", "INVALID_INPUT"),
        ("missing_name", [{"head_sha": HEAD, "status": "completed", "conclusion": "success"}], no_ref, HEAD, TARGET, "INVALID_INPUT"),
        ("self_asserted_pass_ignored", [{**c, "alpha_science_pass": True} for c in good], no_ref, HEAD, TARGET, "CI_GREEN_NO_EXPLICIT_TEST_REFERENCE"),
    ]
    out = []
    for name, checks, workflows, head, target, expected in cases:
        try:
            got = subject.assess(copy.deepcopy(checks), copy.deepcopy(workflows), head, target)["status"]
        except Exception as exc:
            got = "EXCEPTION_" + type(exc).__name__
        out.append({"case": name, "expected": expected, "actual": got, "ok": got == expected})
    return out


if __name__ == "__main__":
    results = run(sys.argv[1])
    print(json.dumps({"passed": sum(x["ok"] for x in results), "total": len(results), "results": results}, sort_keys=True))
    sys.exit(0 if all(x["ok"] for x in results) else 1)

