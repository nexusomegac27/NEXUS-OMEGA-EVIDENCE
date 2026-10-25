#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 research successor: reject nonfinite JSON before pinned V1 intake.

Python accepts NaN/Infinity tokens and can parse 1e400 as float infinity.
Keep the predecessor and reducer byte-identical; no live census or deployment.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

PINNED_INTAKE_V1_NAME = 'alpha_handoff_strict_json_intake_v1_20261025.py'
PINNED_INTAKE_V1_SHA256 = '1836fbc766b710718ab93ebb01bd69d05bdc277dbcc48d010fc7701caa77da3d'


def _reject_nonfinite_constant(_token):
    raise ValueError('NONFINITE_JSON_NUMBER')


def _parse_finite_float(token):
    value = float(token)
    if not math.isfinite(value):
        raise ValueError('NONFINITE_JSON_NUMBER')
    return value


def _pinned_intake():
    path = Path(__file__).resolve().with_name(PINNED_INTAKE_V1_NAME)
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINNED_INTAKE_V1_SHA256:
        raise ValueError('PINNED_INTAKE_V1_SOURCE_DRIFT_FAIL_CLOSED')
    spec = importlib.util.spec_from_file_location('pinned_handoff_strict_v1', path)
    if spec is None or spec.loader is None:
        raise ValueError('PINNED_INTAKE_V1_LOADER_UNAVAILABLE')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduce_json_text(text):
    if type(text) is not str:
        raise ValueError('INPUT_MUST_BE_JSON_TEXT')
    intake = _pinned_intake()
    rows = json.loads(text, object_pairs_hook=intake._reject_duplicate_keys,
                      parse_constant=_reject_nonfinite_constant,
                      parse_float=_parse_finite_float)
    return intake._pinned_reducer().reduce_sample(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json_file', help='UTF-8 JSON array of caller-asserted handoffs')
    args = parser.parse_args()
    data = Path(args.json_file).read_text(encoding='utf-8')
    print(json.dumps(reduce_json_text(data), sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
