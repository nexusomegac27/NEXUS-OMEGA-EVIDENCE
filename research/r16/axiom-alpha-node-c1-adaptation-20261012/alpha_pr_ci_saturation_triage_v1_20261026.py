#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated read-only decision adapter for a saturated owner PR.

Input is independently retrieved, pinned GitHub PR metadata, workflow-run
results and the separately retrieved trusted-base job-log error. This code
never fetches, writes, changes CI, merges, or treats CI as scientific truth.
It only recommends stopping additional files on an already failing PR.
"""
import re

SHA40 = re.compile(r'^[0-9a-f]{40}$', re.ASCII)
REQUIRED = frozenset((
    'validate-anchor', 'validate-scientific-communication',
    'validate-scientific-ledger', 'validate-a83-framework-hardening',
    'Validate repository structure', 'R27-E External Agent Structural Firewall'))
MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'

def _result(status, count=None):
    return {'status': status, 'changed_files': count,
            'merge_authorized': False, 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def triage(snapshot):
    """Return conservative triage, never a publication or merge authorization."""
    if not isinstance(snapshot, dict):
        return _result('HOLD_INVALID_METADATA')
    if snapshot.get('repository') != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE' or snapshot.get('pr_number') != 124:
        return _result('HOLD_ACTOR_SCOPE')
    if snapshot.get('owner_login') != 'nexusomegac27':
        return _result('HOLD_ACTOR_SCOPE')
    count = snapshot.get('changed_files')
    if type(count) is not int or count < 0:
        return _result('HOLD_INVALID_METADATA')
    head = snapshot.get('head_sha')
    if (not isinstance(head, str) or not SHA40.fullmatch(head)
            or snapshot.get('main_sha') != MAIN or snapshot.get('base_sha') != MAIN):
        return _result('HOLD_SOURCE_DRIFT', count)
    runs = snapshot.get('runs')
    if not isinstance(runs, list) or not runs:
        return _result('HOLD_INCOMPLETE_CI', count)
    names = set()
    for run in runs:
        if not isinstance(run, dict) or not isinstance(run.get('name'), str) or not run['name'] or run['name'] in names:
            return _result('HOLD_INCOMPLETE_CI', count)
        names.add(run['name'])
        if run.get('head_sha') != head:
            return _result('HOLD_SOURCE_DRIFT', count)
        if run.get('status') not in ('completed','queued','in_progress'):
            return _result('HOLD_INCOMPLETE_CI', count)
        if run['status'] != 'completed' and run.get('conclusion') is not None:
            return _result('HOLD_INCOMPLETE_CI', count)
        if run['status'] == 'completed' and run.get('conclusion') not in (
                'success','failure','cancelled','timed_out','action_required','neutral','skipped','stale'):
            return _result('HOLD_INCOMPLETE_CI', count)
    if not REQUIRED.issubset(names):
        return _result('HOLD_INCOMPLETE_CI', count)
    if any(r['status'] != 'completed' for r in runs):
        return _result('HOLD_PENDING_CI', count)
    failed = [r for r in runs if r['conclusion'] != 'success']
    if failed:
        firewall_failed = any(r['name'] == 'R27-E External Agent Structural Firewall' for r in failed)
        if (count > 100 and firewall_failed and len(failed) == 1
                and snapshot.get('r27e_failure_reason') == 'TOO_MANY_PR_CHANGES'):
            return _result('HOLD_ACCUMULATION_C1', count)
        return _result('HOLD_FAILED_CI', count)
    return _result('CI_CLEAR_NOT_MERGE_AUTHORITY', count)
