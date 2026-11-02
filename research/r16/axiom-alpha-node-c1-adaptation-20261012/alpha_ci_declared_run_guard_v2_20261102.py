"""Research-only C1 check-head and declared workflow run guard.

Conservative textual YAML scan: only a direct Python command under a `run:`
key counts as a declared step. It is NOT evidence that the command executed.
No YAML dependencies, network calls, runtime integration or claim promotion.
"""
import re

HEX40 = re.compile(r"[0-9a-f]{40}\\Z")
TARGET = re.compile(r"[A-Za-z0-9_]+\\.py\\Z")
RUN = re.compile(r"^(\\s*)(?:-\\s*)?run:\\s*(.*?)\\s*$")


def declared_runs(workflow, target):
    """Count narrowly recognizable direct Python run commands, not mentions."""
    command = re.compile(r"^\\s*python(?:3(?:\\.\\d+)?)?\\s+(?:-B\\s+)?(?:\\./)?"
                         + re.escape(target) + r"(?=\\s|$)")
    lines = workflow.splitlines()
    found = 0
    block_indent = None
    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(stripped)
        if block_indent is not None:
            if indent > block_indent:
                if command.match(stripped):
                    found += 1
                continue
            block_indent = None
        m = RUN.match(line)
        if not m:
            continue
        inline = m.group(2).strip()
        if inline in ("|", "|-", "|+", ">", ">-", ">+"):
            block_indent = len(m.group(1))
        elif command.match(inline):
            found += 1
    return found


def assess(checks, workflows, expected_head_sha, target):
    """Classify declared source commands, not actual scientific execution."""
    result = {"status": "INVALID_INPUT", "check_count": 0,
              "declared_run_steps": 0, "text_mentions": 0,
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
    result["text_mentions"] = sum(w.count(target) for w in workflows)
    result["declared_run_steps"] = sum(declared_runs(w, target) for w in workflows)
    if any(c["head_sha"] != expected_head_sha for c in checks):
        result["status"] = "CHECK_HEAD_MISMATCH"
    elif any(c["status"] != "completed" or c["conclusion"] != "success" for c in checks):
        result["status"] = "CI_NOT_ALL_SUCCESS"
    elif result["declared_run_steps"]:
        result["status"] = "CI_GREEN_DECLARED_RUN_NOT_EXECUTION"
    else:
        result["status"] = "CI_GREEN_NO_DECLARED_RUN"
    return result
