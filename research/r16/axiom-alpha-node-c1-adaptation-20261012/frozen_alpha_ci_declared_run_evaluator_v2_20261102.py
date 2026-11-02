"""Independent frozen evaluator for C1 declared-run classification; synthetic only.

This oracle is intentionally separate from the subject and is frozen before
candidate authoring. It never claims a workflow command actually executed.
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
    good = [{"name": "check", "head_sha": HEAD, "status": "completed",
             "conclusion": "success"} for _ in range(3)]
    cases = [
        ("inline", ["steps:\n  - run: python " + TARGET], good, "CI_GREEN_DECLARED_RUN_NOT_EXECUTION", 1),
        ("python3", ["steps:\n  - run: python3 ./" + TARGET + " --verbose"], good, "CI_GREEN_DECLARED_RUN_NOT_EXECUTION", 1),
        ("multiline", ["steps:\n  - run: |\n      echo preparing\n      python " + TARGET], good, "CI_GREEN_DECLARED_RUN_NOT_EXECUTION", 1),
        ("comment_only", ["# - run: python " + TARGET], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("comment_in_block", ["steps:\n  - run: |\n      # python " + TARGET], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("echo_only", ["steps:\n  - run: echo python " + TARGET], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("env_only", ["env:\n  TARGET: " + TARGET], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("yaml_comment", ["# target " + TARGET + "\nsteps:\n  - run: python other.py"], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("module_other", ["steps:\n  - run: python -m unittest tests.test_alpha\n# " + TARGET], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("shell_string", ["steps:\n  - run: printf 'python " + TARGET + "'"], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("wrong_head", ["steps:\n  - run: python " + TARGET], [{**good[0], "head_sha": OTHER}] + good[1:], "CHECK_HEAD_MISMATCH", 1),
        ("failed", ["steps:\n  - run: python " + TARGET], [{**good[0], "conclusion": "failure"}] + good[1:], "CI_NOT_ALL_SUCCESS", 1),
        ("empty_checks", ["steps:\n  - run: python " + TARGET], [], "INVALID_INPUT", 0),
        ("bad_target", ["steps:\n  - run: python " + TARGET], good, "INVALID_INPUT", 0, "../other.py"),
        ("bad_workflow", [42], good, "INVALID_INPUT", 0),
        ("no_reference", ["steps:\n  - run: python other.py"], good, "CI_GREEN_NO_DECLARED_RUN", 0),
        ("self_asserted_science", ["steps:\n  - run: python " + TARGET], [{**c, "science_pass": True} for c in good], "CI_GREEN_DECLARED_RUN_NOT_EXECUTION", 1),
    ]
    out = []
    for case in cases:
        name, workflows, checks, status, count, *target_override = case
        try:
            got = subject.assess(copy.deepcopy(checks), copy.deepcopy(workflows),
                                 HEAD, target_override[0] if target_override else TARGET)
            ok = (got["status"] == status and got["declared_run_steps"] == count
                  and got["scientific_test_execution"] == "NOT_ESTABLISHED")
            observed = {k: got.get(k) for k in ("status", "declared_run_steps", "scientific_test_execution")}
        except Exception as exc:
            ok = False
            observed = "EXCEPTION_" + type(exc).__name__
        out.append({"case": name, "expected_status": status, "expected_count": count,
                    "observed": observed, "ok": ok})
    return out


if __name__ == "__main__":
    results = run(sys.argv[1])
    print(json.dumps({"passed": sum(x["ok"] for x in results), "total": len(results),
                      "results": results}, sort_keys=True))
    sys.exit(0 if all(x["ok"] for x in results) else 1)
