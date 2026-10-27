#!/usr/bin/env python3
"""Isolated C1 research: read-only R27-E main ruleset enforcement audit.

Input is caller-supplied JSON snapshots, not authenticated live GitHub data.
No repository setting is changed. Actor registry and branch enforcement are
independent gates; neither implies expert research or claim promotion.
"""
import json
import sys

MAX_BYTES = 1024 * 1024
EXPECTED = {"validate", "r27e-external-structural-firewall", "nexus-preentry-lab"}


def fail(reason):
    raise ValueError(reason)


def unique_pairs(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            fail("DUPLICATE_JSON_KEY")
        d[key] = value
    return d


def nonfinite(_):
    fail("NONFINITE_JSON")


def audit(data):
    if type(data) is not dict or set(data) != {"ruleset", "registry"}:
        fail("INVALID_ENVELOPE")
    ruleset, registry = data["ruleset"], data["registry"]
    if type(ruleset) is not dict or type(registry) is not dict:
        fail("INVALID_SOURCE_SHAPE")
    if (ruleset.get("id") != 21252293 or ruleset.get("target") != "branch" or
            ruleset.get("source") != "nexusomegac27/NEXUS-OMEGA-EVIDENCE"):
        fail("UNEXPECTED_RULESET_IDENTITY")
    if (registry.get("object") != "NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1" or
            registry.get("anchor_repo") != ruleset["source"] or
            registry.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY"):
        fail("UNEXPECTED_REGISTRY_IDENTITY")
    if type(registry.get("external_actor_allowlist")) is not list or any(
            type(actor) is not str or not actor for actor in registry["external_actor_allowlist"]):
        fail("INVALID_ACTOR_ALLOWLIST")
    if type(ruleset.get("rules")) is not list:
        fail("INVALID_RULES")
    conditions = ruleset.get("conditions")
    if type(conditions) is not dict or type(conditions.get("ref_name")) is not dict:
        fail("INVALID_REF_CONDITIONS")
    refs = conditions["ref_name"]
    if type(refs.get("include")) is not list or type(refs.get("exclude")) is not list:
        fail("INVALID_REF_LISTS")
    if any(type(x) is not str for x in refs["include"] + refs["exclude"]):
        fail("INVALID_REF_ENTRY")
    # This audit deliberately does not infer wildcard semantics or GitHub ruleset precedence.
    main_applies = (ruleset.get("enforcement") == "active" and
                    "refs/heads/main" in refs["include"] and
                    "refs/heads/main" not in refs["exclude"])
    check_rules = [r for r in ruleset["rules"] if type(r) is dict and
                   r.get("type") == "required_status_checks"]
    pr_rules = [r for r in ruleset["rules"] if type(r) is dict and
                r.get("type") == "pull_request"]
    if len(check_rules) > 1 or len(pr_rules) > 1:
        fail("AMBIGUOUS_DUPLICATE_RULE_TYPE")
    contexts = set()
    if check_rules:
        params = check_rules[0].get("parameters")
        if type(params) is not dict or type(params.get("required_status_checks")) is not list:
            fail("INVALID_CHECK_PARAMETERS")
        for item in params["required_status_checks"]:
            if type(item) is not dict or type(item.get("context")) is not str or not item["context"]:
                fail("INVALID_CHECK_ENTRY")
            if item["context"] in contexts:
                fail("DUPLICATE_CHECK_CONTEXT")
            contexts.add(item["context"])
    params = pr_rules[0].get("parameters") if pr_rules else None
    if params is not None and type(params) is not dict:
        fail("INVALID_REVIEW_PARAMETERS")
    approval_count = params.get("required_approving_review_count") if params else None
    if approval_count is not None and (type(approval_count) is not int or approval_count < 0):
        fail("INVALID_APPROVAL_COUNT")
    codeowners = bool(params and params.get("require_code_owner_review") is True)
    approvals = bool(approval_count is not None and approval_count >= 1)
    bypass = ruleset.get("bypass_actors")
    if type(bypass) is not list:
        fail("INVALID_BYPASS_ACTORS")
    registry_default_deny = (registry.get("default") == "DENY" and
                             not registry["external_actor_allowlist"])
    missing = sorted(EXPECTED - contexts)
    return {
        "state": "HOLD_SCOPED_ENFORCEMENT_GAP" if (
            not main_applies or missing or not codeowners or not approvals or bypass
        ) else "PASS_REQUIRED_CONFIG_WITNESSES_C1",
        "main_exact_ref_active": main_applies,
        "missing_required_status_contexts": missing,
        "required_status_contexts": sorted(contexts),
        "codeowner_review_required": codeowners,
        "one_approval_required": approvals,
        "bypass_actor_count": len(bypass),
        "external_registry_default_deny_empty": registry_default_deny,
        "api_origin_authenticated": False,
        "github_ruleset_precedence_verified": False,
        "external_actor_authorized": False,
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail("INPUT_TOO_LARGE")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=nonfinite)
        print(json.dumps(audit(data), sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
