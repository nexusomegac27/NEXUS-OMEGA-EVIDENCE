"""Read-only C1 V2 witness: both required->observed and observed->required coverage.
Does not authenticate API payloads, define required policy, or modify rulesets.
"""
import json
import sys
from collections import Counter

MAX_BYTES = 1048576


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def reject_nonfinite(_value):
    raise ValueError('NONFINITE_NUMBER')


def fail():
    return {'status': 'NOT_COMPUTABLE', 'missing_required_names': None, 'absent_required_contexts': None,
            'duplicate_contexts': None, 'observed_checks': None,
            'required_contexts': None, 'scope': 'STRUCTURAL_ONLY_NOT_POLICY_OR_AUTHENTICATION'}


def evaluate(data):
    if not isinstance(data, dict):
        return fail()
    rule, runs, head = data.get('ruleset'), data.get('check_runs'), data.get('head_sha')
    if not isinstance(rule, dict) or not isinstance(runs, list) or not runs:
        return fail()
    if not isinstance(head, str) or len(head) != 40 or any(c not in '0123456789abcdef' for c in head):
        return fail()
    if (rule.get('enforcement') != 'active' or rule.get('target') != 'branch' or
            'refs/heads/main' not in rule.get('include_refs', [])):
        return fail()
    required = rule.get('required_status_checks')
    if not isinstance(required, list) or not required:
        return fail()
    required_pairs = []
    for row in required:
        if not isinstance(row, dict) or not isinstance(row.get('context'), str) or not row['context']:
            return fail()
        if type(row.get('integration_id')) is not int or row['integration_id'] <= 0:
            return fail()
        required_pairs.append((row['context'], row['integration_id']))
    if len(set(required_pairs)) != len(required_pairs):
        return fail()
    seen_ids, observed_pairs = set(), []
    for run in runs:
        if not isinstance(run, dict) or not isinstance(run.get('name'), str) or not run['name']:
            return fail()
        if (type(run.get('app_id')) is not int or run['app_id'] <= 0 or
                type(run.get('id')) is not int or run['id'] <= 0 or run['id'] in seen_ids):
            return fail()
        if (run.get('head_sha') != head or run.get('status') != 'completed' or
                run.get('conclusion') != 'success'):
            return fail()
        seen_ids.add(run['id'])
        observed_pairs.append((run['name'], run['app_id']))
    counts = Counter(observed_pairs)
    missing = sorted(set(observed_pairs) - set(required_pairs))
    absent = sorted(set(required_pairs) - set(observed_pairs))
    duplicate = sorted((name, app_id, count) for (name, app_id), count in counts.items() if count > 1)
    return {'status': 'GAP_OBSERVED' if missing or absent or duplicate else 'OBSERVED_CONTEXTS_COVERED',
            'missing_required_names': [name for name, _ in missing],
            'absent_required_contexts': [{'name': name, 'app_id': app_id} for name, app_id in absent],
            'duplicate_contexts': [{'name': name, 'app_id': app_id, 'count': count}
                                   for name, app_id, count in duplicate],
            'observed_checks': len(runs), 'required_contexts': len(required_pairs),
            'scope': 'STRUCTURAL_ONLY_NOT_POLICY_OR_AUTHENTICATION'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                          parse_constant=reject_nonfinite, parse_float=reject_nonfinite)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
