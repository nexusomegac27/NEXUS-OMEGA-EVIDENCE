"""C1 research-only CI check attribution guard; offline and read-only.

A green GitHub check is not an executed scientific evaluator. Workflow source
references are discoverability hints, not proof of test execution. The caller
must independently obtain source bytes and check-run records at immutable refs.
"""
import re

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
TARGET = re.compile(r"[A-Za-z0-9_]+\.py\Z")


def assess(checks, workflows, expected_head_sha, target):
    """Classify GitHub check attribution without promoting science claims.

    The result never attests to live test execution or independent GitHub actor
    identity; those require separate authenticated source and job-log readback.
    """
    result = {"status": "INVALID_INPUT", "check_count": 0,
              "explicit_workflow_references": 0,
              "scientific_test_execution": "NOT_ESTABLISHED"}
    if not isinstance(expected_head_sha, str) or not HEX40.fullmatch(expected_head_sha):
        return result
    if not isinstance(target, str) or not TARGET.fullmatch(target):
        return result
    if not isinstance(checks, list) or not 1 <= len(checks) <= 100:
        return result
    if not isinstance(workflows, list) or not 1 <= len(workflows) <= 50:
        return result
    if any(not isinstance(w, str) or len(w) > 131072 for w in workflows):
        return result
    for c in checks:
        if (not isinstance(c, dict) or not isinstance(c.get("name"), str)
                or not c["name"] or not isinstance(c.get("head_sha"), str)
                or not HEX40.fullmatch(c["head_sha"])
                or not isinstance(c.get("status"), str)
                or not isinstance(c.get("conclusion"), str)):
            return result
    result["check_count"] = len(checks)
    result["explicit_workflow_references"] = sum(target in w for w in workflows)
    if any(c["head_sha"] != expected_head_sha for c in checks):
        result["status"] = "CHECK_HEAD_MISMATCH"
    elif any(c["status"] != "completed" or c["conclusion"] != "success" for c in checks):
        result["status"] = "CI_NOT_ALL_SUCCESS"
    elif result["explicit_workflow_references"]:
        result["status"] = "CI_GREEN_REFERENCE_ONLY_NOT_EXECUTION"
    else:
        result["status"] = "CI_GREEN_NO_EXPLICIT_TEST_REFERENCE"
    return result
