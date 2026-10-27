#!/usr/bin/env python3
"""Run142 C1-only, pure cross-snapshot manifest inventory gate.

Validates internal set coverage and cross-snapshot disjointness; supplied metadata
remains UNAUTHENTICATED. No network, publication, runtime or merge capability.
"""
import re

ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
HEX64 = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)
HEX40 = re.compile(r'[0-9a-f]{40}\Z', re.ASCII)

def fail(reason):
    return {'status':'FAIL_CLOSED', 'reason':reason,
            'source_authentication':'NOT_ESTABLISHED',
            'project_automation_rate':'NOT_COMPUTABLE',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def valid_path(path):
    if not isinstance(path,str) or not path.startswith(ROOT) or len(path)>1024:
        return False
    suffix=path[len(ROOT):]
    if not suffix or suffix.startswith('/') or '\\' in suffix or '\x00' in suffix:
        return False
    return all(part not in ('','.','..') for part in suffix.split('/'))

def audit_inventory(groups,current_paths):
    if not isinstance(groups,list) or not (1<=len(groups)<=32):
        return fail('groups_invalid')
    if not isinstance(current_paths,list) or len(current_paths)>3000:
        return fail('current_invalid')
    names=set()
    observed=set()
    per_group={}
    for group in groups:
        if not isinstance(group,dict) or set(group)!={'name','files'}:
            return fail('group_shape')
        name=group['name']
        if not isinstance(name,str) or not re.fullmatch(r'[a-z][a-z0-9_]{0,63}',name) or name in names:
            return fail('group_name_duplicate_or_invalid')
        names.add(name)
        rows=group['files']
        if not isinstance(rows,list) or len(rows)>3000:
            return fail('group_rows_invalid')
        per_group[name]=len(rows)
        for row in rows:
            if not isinstance(row,dict) or set(row)!={'path','bytes','sha256','git_blob_sha1'}:
                return fail('row_shape')
            path=row['path']
            if not valid_path(path):
                return fail('row_path_invalid')
            if type(row['bytes']) is not int or not (0<=row['bytes']<=2**53-1):
                return fail('row_byte_count_invalid')
            if not isinstance(row['sha256'],str) or HEX64.fullmatch(row['sha256']) is None:
                return fail('row_sha256_invalid')
            if not isinstance(row['git_blob_sha1'],str) or HEX40.fullmatch(row['git_blob_sha1']) is None:
                return fail('row_blob_invalid')
            if path in observed:
                return fail('cross_snapshot_or_intragroup_duplicate_path')
            observed.add(path)
            if len(observed)>3000:
                return fail('manifest_too_large')
    if any(not valid_path(p) for p in current_paths):
        return fail('current_path_invalid')
    if len(set(current_paths))!=len(current_paths):
        return fail('current_path_duplicate')
    if observed!=set(current_paths):
        return fail('current_manifest_set_mismatch')
    return {'status':'COMPLETE_C1', 'historical_count':len(groups[0]['files']),
            'current_count':len(current_paths), 'group_counts':per_group,
            'source_authentication':'NOT_ESTABLISHED',
            'project_automation_rate':'NOT_COMPUTABLE',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}
