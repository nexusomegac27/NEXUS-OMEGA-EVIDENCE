#!/usr/bin/env python3
"""C1 research-only PR publication target preflight.

Consumes separately fetched GitHub metadata; never fetches, writes, merges,
changes evaluator, or authenticates the caller. READY_FOR_CONTENT_CHECK is
NOT permission to publish. Caller must still verify source bytes, license,
privacy, scope, fresh path absence, platform policy, CI and post-write readback.
"""
from datetime import datetime, timezone
import re

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
OWNER = 'nexusomegac27'
LANE = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
SHA40 = re.compile(r'^[0-9a-f]{40}$')


def _iso(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(timezone.utc)


def check_pr_publication_preflight(snapshot, now_utc):
    """Return a scoped, deterministic status; do not mutate snapshot."""
    if not isinstance(snapshot, dict):
        return {'status': 'INCOMPLETE'}
    repo, pr, main, branch, target = (snapshot.get(k) for k in ('repo','pr','main','branch','target'))
    if not all(isinstance(x, dict) for x in (repo,pr,main,branch,target)):
        return {'status': 'INCOMPLETE'}
    try:
        sha_fields = (target['pinned_main'], target['pinned_head'],
                      main['sha'], branch['sha'], pr['base_sha'], pr['head_sha'])
        if not all(isinstance(s,str) and SHA40.fullmatch(s) for s in sha_fields):
            return {'status': 'INCOMPLETE'}
        if (repo['repository_full_name'] != REPO or target['repository_full_name'] != REPO
                or pr['head_repo_full_name'] != REPO or repo['owner']['login'] != OWNER):
            return {'status': 'REPO_SCOPE_MISMATCH'}
        if (not repo['permissions']['push'] or pr['user']['login'] != OWNER):
            return {'status': 'ACTOR_SCOPE_HOLD'}
        if (pr['number'] != target['pr_number'] or pr['state'] != 'open'
                or pr['merged'] is not False or pr['draft'] is not True
                or pr['base'] != 'main' or repo['default_branch'] != 'main'
                or main['name'] != 'main'):
            return {'status': 'PR_STATE_HOLD'}
        if (main['sha'] != target['pinned_main'] or pr['base_sha'] != target['pinned_main']):
            return {'status': 'MAIN_DRIFT'}
        if target['branch'] != pr['head'] or branch['name'] != pr['head']:
            return {'status': 'WRONG_BRANCH'}
        if pr['head_sha'] != target['pinned_head']:
            return {'status': 'HEAD_DRIFT'}
        if branch['sha'] != target['pinned_head']:
            return {'status': 'BRANCH_DRIFT'}
        path = target['path']
        if (not isinstance(path,str) or not path.startswith(LANE)
                or path == LANE or '\\' in path or '..' in path.split('/')
                or any(not seg or seg=='.' for seg in path.split('/'))
                or not path.endswith(('.py','.json','.md'))):
            return {'status': 'PATH_SCOPE_HOLD'}
        if target.get('path_absent_confirmed') is not True:
            return {'status': 'PATH_EXISTS_OR_UNVERIFIED'}
        now = _iso(now_utc)
        observed = _iso(target['observed_at'])
        age = (now-observed).total_seconds()
        if age < 0 or age > 120:
            return {'status': 'STALE_SNAPSHOT'}
        return {'status': 'READY_FOR_CONTENT_CHECK'}
    except (KeyError, TypeError, ValueError, OverflowError, AttributeError):
        return {'status': 'INCOMPLETE'}
