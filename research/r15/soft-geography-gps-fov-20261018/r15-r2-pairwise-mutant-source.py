"""NEXUS R15 R2. Standalone synthetic-only response-body byte ledger comparison.

Not a browser network monitor, real bandwidth estimate, telemetry authenticator,
privacy guarantee, permission gate, source validator or runtime integration.
Only compares pre-supplied synthetic ledgers with identical declared dataset,
LOD, cold-cache and coverage-oracle profiles. No network or device access.
"""
import json
import math
import re
import sys
from pathlib import Path

HEX64 = re.compile(r'^[0-9a-f]{64}$')
LOCAL_RESOURCE = re.compile(r'^local://tile/[0-9]{3}$')


def reject_duplicates(items):
    out = {}
    for k, v in items:
        if k in out:
            raise ValueError('duplicate_json_key')
        out[k] = v
    return out


def reject_constant(value):
    raise ValueError('nonfinite_json_constant')


def reject_float(value):
    f = float(value)
    if not math.isfinite(f):
        raise ValueError('floating_overflow')
    return f


def hold(reason):
    return {
        'state': 'HOLD_SCOPED',
        'reason': reason,
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
        'real_network_bytes_verified': False,
        'baseline_response_body_bytes': None,
        'candidate_response_body_bytes': None,
        'synthetic_body_byte_reduction_percent': None,
        'real_savings_claim': False,
    }


def guarded_comparison(p):
    if type(p) is not dict:
        return hold('not_an_object')
    if p.get('profile') != 'R15_R2_SYNTHETIC_NO_REAL_GPS':
        return hold('non_synthetic_input_forbidden')
    if p.get('claim_ceiling') != 'C1_DESCRIPTIVE_ONLY':
        return hold('claim_promotion_forbidden')
    if p.get('personal_location_included') is not False:
        return hold('personal_location_not_allowed')
    if set(p) != {'profile', 'claim_ceiling', 'personal_location_included', 'baseline', 'candidate'}:
        return hold('unexpected_top_level_fields')
    values = []
    captures = []
    for label in ('baseline', 'candidate'):
        c = p.get(label)
        if type(c) is not dict or set(c) != {
            'capture_id', 'dataset_sha256', 'view_snapshot_sha256',
            'lod_profile', 'cache_state', 'coverage_oracle',
            'coverage_passed', 'capture_complete', 'requests'
        }:
            return hold('bad_capture_schema_' + label)
        if type(c.get('capture_id')) is not str or c['capture_id'] != ('circle' if label == 'baseline' else 'fov'):
            return hold('invalid_capture_id_' + label)
        if any(type(c.get(k)) is not str or not HEX64.fullmatch(c[k]) for k in ('dataset_sha256', 'view_snapshot_sha256')):
            return hold('invalid_source_or_view_hash_' + label)
        if c.get('lod_profile') != 'SYNTHETIC_IDENTICAL_LOD':
            return hold('lod_comparability_unproven_' + label)
        if c.get('cache_state') != 'COLD_CLEAN':
            return hold('different_or_unknown_cache_state_' + label)
        if c.get('coverage_oracle') != 'SYNTHETIC_FIXED_VIEW_V1' or c.get('coverage_passed') is not True:
            return hold('coverage_not_pinned_or_failed_' + label)
        if c.get('capture_complete') is not True:
            return hold('incomplete_trace_' + label)
        reqs = c['requests']
        if type(reqs) is not list or not 1 <= len(reqs) <= 500:
            return hold('request_count_bad_' + label)
        ids = set()
        total = 0
        for r in reqs:
            if type(r) is not dict or set(r) != {'id', 'resource', 'response_body_bytes'}:
                return hold('unknown_or_missing_request_attributes_' + label)
            if type(r['id']) is not str or not (1 <= len(r['id']) <= 60) or r['id'] in ids:
                return hold('duplicate_or_invalid_request_id_' + label)
            ids.add(r['id'])
            if type(r['resource']) is not str or not LOCAL_RESOURCE.fullmatch(r['resource']):
                return hold('nonlocal_or_unknown_resource_' + label)
            n = r['response_body_bytes']
            if type(n) is not int or not 0 <= n <= 100_000_000:
                return hold('invalid_byte_count_' + label)
            total += n
        if total > 10_000_000_000:
            return hold('synthetic_budget_exceeded_' + label)
        captures.append(c)
        values.append(total)
    # DELIBERATE MUTANT: removed same-dataset and same-view comparison.
    b, c = values
    reduction = 100.0 * (b - c) / b if b > 0 else None
    return {
        'state': 'SYNTHETIC_ACCOUNTED_C1',
        'reason': 'only_invented_response_body_sizes_compared_not_network_telemetry',
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
        'real_network_bytes_verified': False,
        'baseline_response_body_bytes': b,
        'candidate_response_body_bytes': c,
        'synthetic_body_byte_reduction_percent': reduction,
        'synthetic_request_counts': {'baseline': len(captures[0]['requests']), 'candidate': len(captures[1]['requests'])},
        'real_savings_claim': False,
    }


def main():
    if len(sys.argv) != 2:
        out = hold('expected_one_input_path')
    else:
        try:
            text = Path(sys.argv[1]).read_text(encoding='utf-8')
            p = json.loads(text, object_pairs_hook=reject_duplicates,
                           parse_constant=reject_constant, parse_float=reject_float)
            out = guarded_comparison(p)
        except (OSError, UnicodeError, ValueError, TypeError, OverflowError) as exc:
            out = hold('invalid_json_or_io_' + type(exc).__name__)
    print(json.dumps(out, ensure_ascii=True, sort_keys=True, separators=(',', ':')))
    return 0 if out['state'] == 'SYNTHETIC_ACCOUNTED_C1' else 2

if __name__ == '__main__':
    sys.exit(main())
