"""C1 isolated V5: conservative GitHub ruleset applicability/bypass precheck.

Fail closed when an unauthenticated REST-shaped ruleset has unmodeled ref
exclusions, bypass principals, or type-ambiguous include lists. Does not prove
live ruleset enforcement, authenticate HTTP, or modify GitHub settings.
V4 and its predecessors remain byte-identical and are imported unchanged.
"""
import json
import sys

import alpha_ci_github_rest_native_adapter_v4_20261101 as prior

MAIN = 'refs/heads/main'


def scope_ok(data):
    if not isinstance(data, dict):
        return False
    ruleset = data.get('ruleset_response')
    if not isinstance(ruleset, dict):
        return False
    conditions = ruleset.get('conditions')
    if not isinstance(conditions, dict):
        return False
    ref_name = conditions.get('ref_name')
    if not isinstance(ref_name, dict):
        return False
    include, exclude, bypass = (ref_name.get('include'), ref_name.get('exclude'),
                                ruleset.get('bypass_actors'))
    if (not isinstance(include, list) or not include or
            any(not isinstance(ref, str) or not ref for ref in include) or
            len(set(include)) != len(include) or MAIN not in include):
        return False
    # Deliberately narrow profile: any exclusion requires a separately tested
    # GitHub pattern matcher. Reject rather than claim enforcement on main.
    if not isinstance(exclude, list) or exclude:
        return False
    # Any bypass actor means the required-check rule is not universal. No
    # implicit trust in actor labels, model names or unverified permissions.
    if not isinstance(bypass, list) or bypass:
        return False
    return True


def fail():
    result = prior.fail()
    result['ruleset_scope_structural'] = False
    result['snapshot_scope'] = 'REST_SHAPED_UNAUTHENTICATED_NO_EXCLUSIONS_NO_BYPASS'
    return result


def evaluate(data):
    if not scope_ok(data):
        return fail()
    result = prior.evaluate(data)
    result['ruleset_scope_structural'] = result['status'] != 'NOT_COMPUTABLE'
    result['snapshot_scope'] = 'REST_SHAPED_UNAUTHENTICATED_NO_EXCLUSIONS_NO_BYPASS'
    return result


def main():
    try:
        parser = prior.prior.prior
        raw = sys.stdin.buffer.read(parser.MAX_BYTES + 1)
        if len(raw) > parser.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=parser.unique_pairs,
                          parse_constant=parser.reject_nonfinite,
                          parse_float=parser.reject_nonfinite)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError, KeyError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
