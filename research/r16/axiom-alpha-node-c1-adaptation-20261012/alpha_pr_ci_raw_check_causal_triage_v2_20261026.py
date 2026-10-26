#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 PR #124 raw check-run and causal-failure triage.

Pure, offline decision adapter. The caller must independently fetch/pin PR,
main, check-run and job-log bytes; supplied metadata is not authenticated here.
No CI changes, writes, merge permission, or scientific claim promotion.
"""
from collections import Counter
import re

SHA40 = re.compile(r'^[0-9a-f]{40}$', re.ASCII)
EXPECTED = Counter({'nexus-preentry-lab': 1,
                    'validate-repository-structure': 1,
                    'validate': 4,
                    'r27e-external-structural-firewall': 1,
                    'semgrep-cloud-platform/scan': 1})
APPS = {name: ('semgrep-code-nexusomegac27' if name.startswith('semgrep-')
               else 'github-actions') for name in EXPECTED}
VALID_CONCLUSIONS = frozenset(('success', 'failure', 'cancelled', 'timed_out',
                               'action_required', 'neutral', 'skipped', 'stale'))

def _out(status, count=None):
    return {'status': status, 'changed_files': count,
            'merge_authorized': False, 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'check_name_identity_complete': False}

def triage(snapshot, pin):
    """Classify exactly one independently pinned PR #124 check-run snapshot."""
    if not isinstance(snapshot, dict) or not isinstance(pin, dict):
        return _out('HOLD_INVALID_METADATA')
    if (snapshot.get('repository') != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
            or snapshot.get('pr_number') != 124
            or snapshot.get('owner_login') != 'nexusomegac27'):
        return _out('HOLD_ACTOR_SCOPE')
    count = snapshot.get('changed_files')
    if type(count) is not int or count < 0:
        return _out('HOLD_INVALID_METADATA')
    for key in ('head_sha', 'base_sha', 'main_sha'):
        expected = pin.get(key)
        if not isinstance(expected, str) or not SHA40.fullmatch(expected):
            return _out('HOLD_INVALID_METADATA', count)
        if snapshot.get(key) != expected:
            return _out('HOLD_SOURCE_DRIFT', count)
    ids = pin.get('check_ids')
    if (not isinstance(ids, list) or len(ids) != 8
            or any(type(i) is not int or i <= 0 for i in ids)
            or len(set(ids)) != 8 or ids != sorted(ids)):
        return _out('HOLD_INVALID_METADATA', count)
    checks = snapshot.get('checks')
    if not isinstance(checks, list) or len(checks) != 8:
        return _out('HOLD_INCOMPLETE_CI', count)
    seen_ids, names = set(), Counter()
    pending = False
    failures = set()
    for check in checks:
        if not isinstance(check, dict):
            return _out('HOLD_INCOMPLETE_CI', count)
        cid, name = check.get('id'), check.get('name')
        if type(cid) is not int or cid <= 0 or cid in seen_ids:
            return _out('HOLD_INCOMPLETE_CI', count)
        seen_ids.add(cid)
        if name not in EXPECTED or check.get('app_slug') != APPS[name]:
            return _out('HOLD_INCOMPLETE_CI', count)
        names[name] += 1
        if check.get('head_sha') != pin['head_sha']:
            return _out('HOLD_SOURCE_DRIFT', count)
        status, conclusion = check.get('status'), check.get('conclusion')
        if status in ('queued', 'in_progress') and conclusion is None:
            pending = True
        elif status == 'completed' and conclusion in VALID_CONCLUSIONS:
            if conclusion != 'success':
                failures.add(name)
        else:
            return _out('HOLD_INCOMPLETE_CI', count)
    if sorted(seen_ids) != ids or names != EXPECTED:
        return _out('HOLD_INCOMPLETE_CI', count)
    if pending:
        return _out('HOLD_PENDING_CI', count)
    if not failures:
        # Four GitHub Actions jobs share the display name 'validate'.
        # A green set of names cannot prove which four workflows were run.
        return _out('HOLD_UNATTRIBUTED_CI', count)
    if failures == {'r27e-external-structural-firewall', 'nexus-preentry-lab'}:
        r27e = snapshot.get('r27e_log_excerpt')
        preentry = snapshot.get('preentry_log_excerpt')
        if (count > 100 and isinstance(r27e, str)
                and 'ValueError: TOO_MANY_PR_CHANGES' in r27e
                and isinstance(preentry, str)
                and 'UPSTREAM_RESULT: failure' in preentry
                and 'DENY: R27-E structural intake did not pass' in preentry):
            return _out('HOLD_ACCUMULATION_C1', count)
    return _out('HOLD_FAILED_CI', count)
