#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated composition of pinned strict intake and outcome/rate guard.

Caller-asserted synthetic sample only; not an independently censused project rate.
No source mutation, network, runtime activation, claim promotion or auto-merge.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

PARENTS = (
    ('alpha_handoff_strict_json_intake_v2_20261025.py',
     'b3307f6d5c069533a3196d68d5c6ada718b09bb394e8e154cbc6e0e1715d34da', 'strict_intake'),
    ('alpha_handoff_outcome_identity_guard_v2_20261025.py',
     '31a39afa384dad3974bf32aa089aaaecdd4a6e13983e33b099b1c88c79f54fa9', 'outcome_guard'),
)


def _pinned(name, expected_sha256, module_name):
    path = Path(__file__).resolve().with_name(name)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError('PINNED_COMPOSITION_SOURCE_DRIFT_FAIL_CLOSED')
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError('PINNED_COMPOSITION_MODULE_UNAVAILABLE')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduce_json_text(text):
    # Both source identities are checked before the first caller record is classified.
    strict = _pinned(*PARENTS[0])
    guard = _pinned(*PARENTS[1])
    reduced = strict.reduce_json_text(text)
    return guard.guard_reducer_result(reduced)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', help='UTF-8 JSON array of caller-asserted handoffs')
    args = parser.parse_args()
    text = Path(args.json_file).read_text(encoding='utf-8')
    result = reduce_json_text(text)
    print(json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False))


if __name__ == '__main__':
    main()
