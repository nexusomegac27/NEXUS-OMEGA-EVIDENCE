#!/usr/bin/env python3
"""Isolated C1 diagnostic of GitHub ruleset/check-run name collisions; no GitHub writes."""
import json
import re
import sys
from collections import Counter

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
SCHEMA = 'NEXUS_ALPHA_CI_RULESET_CHECK_SNAPSHOT_V1'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError('NONFINITE_JSON')


def audit(doc):
    if type(doc) is not dict or set(doc) != {'schema','repository','pinned_main','pr_head','ruleset','check_runs'}:
        raise ValueError('INVALID_ENVELOPE')
    if doc['schema'] != SCHEMA or doc['repository'] != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE':
        raise ValueError('INVALID_SOURCE_SCOPE')
    for key in ('pinned_main','pr_head'):
        if type(doc[key]) is not str or not HEX40.fullmatch(doc[key]):
            raise ValueError('INVALID_COMMIT_PIN')
    rule = doc['ruleset']
    if type(rule) is not dict or set(rule) != {'id','enforcement','ref_include','required_status_checks'}:
        raise ValueError('INVALID_RULESET')
    if type(rule['id']) is not int or rule['id'] <= 0 or rule['enforcement'] != 'active':
        raise ValueError('RULESET_NOT_ACTIVE')
    if rule['ref_include'] != ['refs/heads/main']:
        raise ValueError('UNBOUND_BRANCH_RULE')
    required = rule['required_status_checks']
    if type(required) is not list or not required:
        raise ValueError('MISSING_REQUIRED_CHECKS')
    required_pairs = set()
    for item in required:
        if type(item) is not dict or set(item) != {'context','integration_id'}:
            raise ValueError('INVALID_REQUIRED_CHECK')
        name, app = item['context'], item['integration_id']
        if type(name) is not str or not name.strip() or type(app) is not int or app <= 0:
            raise ValueError('INVALID_REQUIRED_CHECK')
        if (name,app) in required_pairs:
            raise ValueError('DUPLICATE_REQUIRED_CHECK')
        required_pairs.add((name,app))
    runs = doc['check_runs']
    if type(runs) is not list or not 1 <= len(runs) <= 1000:
        raise ValueError('INVALID_CHECK_RUNS')
    seen = set()
    counts = Counter()
    successful = 0
    for item in runs:
        if type(item) is not dict or set(item) != {'id','name','app_id','status','conclusion'}:
            raise ValueError('INVALID_CHECK_RUN')
        ident, name, app = item['id'], item['name'], item['app_id']
        if type(ident) is not int or ident <= 0 or ident in seen:
            raise ValueError('DUPLICATE_OR_INVALID_RUN_ID')
        seen.add(ident)
        if type(name) is not str or not name.strip() or type(app) is not int or app <= 0:
            raise ValueError('INVALID_CHECK_IDENTITY')
        if item['status'] not in ('completed','queued','in_progress') or item['conclusion'] not in ('success','failure','cancelled','skipped','neutral','timed_out',None):
            raise ValueError('INVALID_CHECK_STATE')
        if item['status'] != 'completed' and item['conclusion'] is not None:
            raise ValueError('CONTRADICTORY_CHECK_STATE')
        successful += item['status'] == 'completed' and item['conclusion'] == 'success'
        counts[(name,app)] += 1
    matched = {name:counts[(name,app)] for name,app in sorted(required_pairs)}
    collisions = {name:count for name,count in matched.items() if count > 1}
    missing = sorted(name for name,count in matched.items() if count == 0)
    nonrequired = sum(count for pair,count in counts.items() if pair not in required_pairs)
    return {'state':'REQUIRED_CHECK_NAME_COLLISION_OBSERVED' if collisions else ('REQUIRED_CHECK_MISSING' if missing else 'NO_REQUIRED_NAME_COLLISION_IN_SNAPSHOT'),
            'observed_checks':len(runs),'successful_checks':successful,
            'required_contexts':len(required_pairs),'required_name_matches':matched,
            'collisions':collisions,'missing_required':missing,
            'not_named_as_required_runs':nonrequired,
            'hard_gate_coverage':'NOT_PROVEN_BY_API_SNAPSHOT',
            'independent_transport_authentication':'NOT_ESTABLISHED',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        doc = json.load(sys.stdin, object_pairs_hook=unique, parse_constant=reject_constant)
        result = audit(doc)
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError) as exc:
        result = {'state':'FAIL_CLOSED','reason':type(exc).__name__ if isinstance(exc,RecursionError) else str(exc)}
        print(json.dumps(result,sort_keys=True))
        return 2
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
