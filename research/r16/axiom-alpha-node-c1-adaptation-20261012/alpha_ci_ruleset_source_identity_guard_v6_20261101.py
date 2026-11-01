"""C1 isolated V6: bind REST-shaped ruleset source identity to the owner repo.

Reject wrong/missing repository source, source_type or canonical endpoint.
Imports V5 unchanged; does not authenticate HTTP, prove ruleset enforcement,
or mutate repository settings or external actor registration.
"""
import json
import sys

import alpha_ci_ruleset_effective_scope_guard_v5_20261101 as prior

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
RULESET_URL = f'https://api.github.com/repos/{REPO}/rulesets/21252293'


def source_ok(data):
    if not isinstance(data, dict):
        return False
    ruleset = data.get('ruleset_response')
    return (isinstance(ruleset, dict) and
            type(ruleset.get('source')) is str and ruleset['source'] == REPO and
            type(ruleset.get('source_type')) is str and ruleset['source_type'] == 'Repository' and
            type(ruleset.get('url')) is str and ruleset['url'] == RULESET_URL)


def fail():
    result = prior.fail()
    result['ruleset_source_identity_structural'] = False
    result['snapshot_scope'] = 'REST_SHAPED_UNAUTHENTICATED_SOURCE_BOUND'
    return result


def evaluate(data):
    if not source_ok(data):
        return fail()
    result = prior.evaluate(data)
    result['ruleset_source_identity_structural'] = result['status'] != 'NOT_COMPUTABLE'
    result['snapshot_scope'] = 'REST_SHAPED_UNAUTHENTICATED_SOURCE_BOUND'
    return result


def main():
    try:
        parser = prior.prior.prior.prior
        raw = sys.stdin.buffer.read(parser.MAX_BYTES + 1)
        if len(raw) > parser.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=parser.unique_pairs,
                          parse_constant=parser.reject_nonfinite, parse_float=parser.reject_nonfinite)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError, KeyError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
