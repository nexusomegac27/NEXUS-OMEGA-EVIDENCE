#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated successor: reject forged outcome identities before sample-rate display.

The parent uncertainty guard and its independent evaluator remain untouched.
Caller-provided outcomes are NOT proof of real handoffs or a complete census.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re

PARENT_NAME = 'alpha_handoff_uncertainty_rate_guard_v1_20261025.py'
PARENT_SHA256 = 'b49e5193de2cbf86289ec309b969d1ec46ec767fe9ec38416e6f7b958b2e0571'
ID = re.compile(r'[A-Za-z0-9._:-]{1,128}\Z')


def _parent():
    path = Path(__file__).resolve().with_name(PARENT_NAME)
    if hashlib.sha256(path.read_bytes()).hexdigest() != PARENT_SHA256:
        raise ValueError('PINNED_PARENT_SOURCE_DRIFT_FAIL_CLOSED')
    spec = importlib.util.spec_from_file_location('pinned_uncertainty_guard_v1', path)
    if spec is None or spec.loader is None:
        raise ValueError('PINNED_PARENT_LOADER_UNAVAILABLE')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def guard_reducer_result(result):
    parent = _parent()
    guarded = parent.guard_reducer_result(result)
    outcomes = guarded['outcomes']
    counts = Counter(row.get('id') for row in outcomes if type(row.get('id')) is str)
    for row in outcomes:
        state = row['status']
        identifier = row.get('id')
        if state != 'UNKNOWN':
            if type(identifier) is not str or ID.fullmatch(identifier) is None:
                raise ValueError('NON_UNKNOWN_OUTCOME_ID_INVALID')
        if type(identifier) is str and counts[identifier] > 1 and state != 'UNKNOWN':
            raise ValueError('DUPLICATE_ID_NON_UNKNOWN_OUTCOME')
    return guarded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', help='JSON result from the pinned caller-asserted sample reducer')
    args = parser.parse_args()
    parent = _parent()
    raw = Path(args.json_file).read_text(encoding='utf-8')
    result = json.loads(raw, object_pairs_hook=parent._no_duplicate_keys,
                        parse_constant=parent._reject_constant,
                        parse_float=parent._finite_float)
    print(json.dumps(guard_reducer_result(result), sort_keys=True,
                     separators=(',', ':'), allow_nan=False))


if __name__ == '__main__':
    main()
