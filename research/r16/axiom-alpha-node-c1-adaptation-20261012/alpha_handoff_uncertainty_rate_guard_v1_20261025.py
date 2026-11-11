#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated post-reducer guard: do not present a complete sample rate with UNKNOWN rows.

Consumes the output of the existing pinned handoff reducer; does not authenticate
source records, claim a project census, or modify predecessor code/oracles.
"""
from __future__ import annotations
import argparse
import copy
import json
import math
from pathlib import Path

STATES = frozenset({'ELIGIBLE_AUTOMATED', 'ELIGIBLE_FAILED', 'UNKNOWN', 'EXCLUDED'})
COUNTS = ('sample_eligible_denominator', 'sample_automated_numerator',
          'unknown_or_unverified', 'excluded_out_of_scope')


def guard_reducer_result(result):
    if type(result) is not dict:
        raise ValueError('INVALID_REDUCER_RESULT')
    if result.get('claim_ceiling') != 'C1_DESCRIPTIVE_ONLY':
        raise ValueError('CLAIM_CEILING_MISMATCH')
    if result.get('measurement_scope') != 'CALLER_ASSERTED_SAMPLE_ONLY_NOT_INDEPENDENTLY_AUDITED':
        raise ValueError('MEASUREMENT_SCOPE_MISMATCH')
    if result.get('project_handoff_automation_rate') != 'NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS':
        raise ValueError('UNAUTHORIZED_PROJECT_RATE')
    for key in COUNTS:
        if type(result.get(key)) is not int or result[key] < 0:
            raise ValueError('INVALID_REDUCER_COUNT')
    outcomes = result.get('outcomes')
    if type(outcomes) is not list:
        raise ValueError('INVALID_REDUCER_OUTCOMES')
    states = []
    for index, row in enumerate(outcomes):
        if (type(row) is not dict or type(row.get('index')) is not int
                or row['index'] != index or row.get('status') not in STATES):
            raise ValueError('INVALID_REDUCER_OUTCOME')
        states.append(row['status'])
    expected = (sum(x.startswith('ELIGIBLE_') for x in states),
                states.count('ELIGIBLE_AUTOMATED'), states.count('UNKNOWN'),
                states.count('EXCLUDED'))
    if tuple(result[key] for key in COUNTS) != expected:
        raise ValueError('REDUCER_COUNT_MISMATCH')
    den, num, unknown, _excluded = expected
    old_rate = result.get('sample_rate_percent')
    expected_rate = round(100 * num / den, 2) if den else None
    if type(old_rate) not in (int, float, type(None)) or old_rate != expected_rate:
        raise ValueError('REPORTED_RATE_MISMATCH')
    guarded = copy.deepcopy(result)
    if unknown:
        guarded['sample_rate_percent'] = None
        guarded['sample_rate_status'] = 'WITHHELD_UNRESOLVED_ROWS'
    elif den == 0:
        guarded['sample_rate_percent'] = None
        guarded['sample_rate_status'] = 'NO_ELIGIBLE_ROWS'
    else:
        guarded['sample_rate_status'] = 'COMPLETE_CALLER_ASSERTED_SAMPLE'
    return guarded


def _no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('DUPLICATE_JSON_KEY')
        obj[key] = value
    return obj


def _finite_float(token):
    number = float(token)
    if not math.isfinite(number):
        raise ValueError('NONFINITE_JSON_NUMBER')
    return number


def _reject_constant(_token):
    raise ValueError('NONFINITE_JSON_NUMBER')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', help='JSON result of the pinned handoff sample reducer')
    args = parser.parse_args()
    text = Path(args.json_file).read_text(encoding='utf-8')
    result = json.loads(text, object_pairs_hook=_no_duplicate_keys,
                        parse_constant=_reject_constant, parse_float=_finite_float)
    print(json.dumps(guard_reducer_result(result), sort_keys=True,
                     separators=(',', ':'), allow_nan=False))


if __name__ == '__main__':
    main()
