#!/usr/bin/env python3
"""Research-only fail-closed JSON and binary64 numeric-domain gate for GitHub captures.

Read-only; no network or file mutations. ACCEPT_STRICT_JSON means ONLY that
supplied input is an unambiguous UTF-8 JSON object with representable
binary64 floating numbers within the size limit. It does NOT authenticate its content, GitHub actor, CI or main.

A caller must run the independently pinned downstream semantic/byte guard
AFTER this gate; this gate never replaces or approves that evaluator.
"""
import json
import math
from pathlib import Path
import sys

MAX_CAPTURE_BYTES = 1_048_576


class DuplicateJSONKey(ValueError):
    pass


class NumericDomainError(ValueError):
    pass


def _bounded_float(token):
    """Reject numeric overflow and nonzero-to-zero underflow, without mutation.

    This is a deliberately conservative evidence-capture policy, not a claim
    that RFC 8259 forbids arbitrarily large numeric exponents.
    """
    value = float(token)
    if not math.isfinite(value):
        raise NumericDomainError('NUMERIC_DOMAIN_UNREPRESENTABLE')
    if value == 0.0:
        mantissa = token.lower().split('e', 1)[0]
        if any(ch in '123456789' for ch in mantissa):
            raise NumericDomainError('NUMERIC_DOMAIN_UNREPRESENTABLE')
    return value


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError('NONFINITE_JSON_CONSTANT')


def validate_capture(raw):
    if not isinstance(raw, bytes):
        return {'status': 'REJECT', 'reason': 'NOT_RAW_BYTES'}
    if not raw or len(raw) > MAX_CAPTURE_BYTES:
        return {'status': 'REJECT', 'reason': 'EMPTY_OR_OVERSIZE'}
    try:
        decoded = raw.decode('utf-8', errors='strict')
        value = json.loads(decoded, object_pairs_hook=_unique_pairs,
                           parse_constant=_reject_constant,
                           parse_float=_bounded_float)
    except NumericDomainError:
        return {'status': 'REJECT', 'reason': 'NUMERIC_DOMAIN_UNREPRESENTABLE'}
    except DuplicateJSONKey:
        return {'status': 'REJECT', 'reason': 'DUPLICATE_JSON_KEY'}
    except UnicodeDecodeError:
        return {'status': 'REJECT', 'reason': 'INVALID_UTF8'}
    except (ValueError, RecursionError):
        return {'status': 'REJECT', 'reason': 'INVALID_OR_AMBIGUOUS_JSON'}
    if not isinstance(value, dict):
        return {'status': 'REJECT', 'reason': 'ROOT_NOT_OBJECT'}
    return {'status': 'ACCEPT_STRICT_JSON', 'reason': 'SYNTAX_AND_NUMERIC_DOMAIN_ONLY',
            'authentication': 'NOT_ESTABLISHED',
            'downstream_evaluator': 'REQUIRED_SEPARATELY',
            'main_verified': False,
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main(argv):
    if len(argv) != 2:
        result = {'status': 'REJECT', 'reason': 'INPUT_PATH_REQUIRED'}
    else:
        try:
            path = Path(argv[1])
            if path.stat().st_size > MAX_CAPTURE_BYTES:
                result = {'status': 'REJECT', 'reason': 'EMPTY_OR_OVERSIZE'}
            else:
                result = validate_capture(path.read_bytes())
        except OSError:
            result = {'status': 'REJECT', 'reason': 'INPUT_UNAVAILABLE'}
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status'] == 'ACCEPT_STRICT_JSON' else 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
