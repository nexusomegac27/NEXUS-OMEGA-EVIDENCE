#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated raw-input SHA-256 pin for the existing V3 census adapter.

The expected digest MUST be supplied from a separately checked source.
The CLI argument alone is not GitHub authentication or proof of completeness.
"""
import hashlib
import hmac
import json
import re
import sys
import alpha_handoff_readback_scope_adapter_v3_20261028 as v3

PIN = re.compile(r'[0-9a-f]{64}\Z')


def main():
    try:
        if len(sys.argv) != 3 or sys.argv[1] != '--expected-sha256' or not PIN.fullmatch(sys.argv[2]):
            raise ValueError('EXPECTED_EXTERNAL_SHA256_PIN_REQUIRED')
        raw = sys.stdin.buffer.read(v3.base.MAX_INPUT + 1)
        if len(raw) > v3.base.MAX_INPUT:
            raise ValueError('INPUT_TOO_LARGE')
        actual = hashlib.sha256(raw).hexdigest()
        if not hmac.compare_digest(actual, sys.argv[2]):
            raise ValueError('PINNED_INPUT_SHA256_MISMATCH')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=v3.base.unique_pairs,
                         parse_constant=v3.base.nonfinite)
        result = v3.audit(obj)
        result['input_bytes'] = len(raw)
        result['input_sha256'] = actual
        result['input_pinned_match'] = True
        result['input_pin_source_authenticated'] = False
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
