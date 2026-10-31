#!/usr/bin/env python3
"""Read-only, fail-closed audit of pinned workflow/job inventory (C1)."""
import json
import re
import sys

HEX40 = re.compile(r'^[0-9a-f]{40}$')
PATH = re.compile(r'^\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml$')
JOB = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def audit(document):
    if not isinstance(document, dict) or set(document) != {'repo', 'pinned_commit', 'required_context', 'workflows'}:
        raise ValueError('SCHEMA')
    if document['repo'] != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE' or not isinstance(document['pinned_commit'], str) or not HEX40.fullmatch(document['pinned_commit']):
        raise ValueError('PIN')
    required = document['required_context']
    if not isinstance(required, str) or not JOB.fullmatch(required):
        raise ValueError('REQUIRED_CONTEXT')
    workflows = document['workflows']
    if not isinstance(workflows, list) or not workflows or len(workflows) > 100:
        raise ValueError('WORKFLOW_LIST')
    paths, matched, total_jobs = set(), [], 0
    for item in workflows:
        if not isinstance(item, dict) or set(item) != {'path', 'blob_sha', 'jobs'}:
            raise ValueError('WORKFLOW_SCHEMA')
        path, sha, jobs = item['path'], item['blob_sha'], item['jobs']
        if not isinstance(path, str) or not PATH.fullmatch(path) or path in paths:
            raise ValueError('WORKFLOW_PATH')
        paths.add(path)
        if not isinstance(sha, str) or not HEX40.fullmatch(sha):
            raise ValueError('WORKFLOW_BLOB')
        if not isinstance(jobs, list) or not jobs or len(jobs) > 100 or any(not isinstance(j, str) or not JOB.fullmatch(j) for j in jobs) or len(jobs) != len(set(jobs)):
            raise ValueError('JOB_SCHEMA')
        total_jobs += len(jobs)
        if required in jobs:
            matched.append(path)
    return {'status': 'STATIC_REQUIRED_CONTEXT_COLLISION' if len(matched) > 1 else 'UNIQUE_OR_ABSENT', 'workflow_count': len(workflows), 'job_count': total_jobs, 'matching_workflows': len(matched), 'matching_paths': sorted(matched), 'hard_gate_enforcement': 'NOT_PROVEN'}


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('ARGUMENTS')
        with open(sys.argv[1], 'rb') as handle:
            raw = handle.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError('INPUT_TOO_LARGE')
        payload = json.loads(raw.decode('utf-8'), object_pairs_hook=reject_duplicates, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE')))
        result = audit(payload)
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, UnicodeError, OSError, TypeError, RecursionError) as error:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(error)[:100]}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
