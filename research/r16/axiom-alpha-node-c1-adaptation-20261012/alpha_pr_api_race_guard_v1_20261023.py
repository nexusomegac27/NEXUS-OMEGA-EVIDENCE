#!/usr/bin/env python3
"""C1-only guard for a GitHub PR metadata / file-list read window.

The caller must independently fetch/authenticate before + after PR metadata,
and the complete paginated filename list between them. Count equality and
stable metadata do NOT prove GitHub authentication or full page retrieval.
This guard does not grant write, merge, CI, or scientific authority.
"""
import re

_SHA40=re.compile(r'[0-9a-f]{40}\Z')
_MAX_FILES=3000

def _incomplete(reason):
    return {'status':'INCOMPLETE','reasons':[reason],
            'source_authentication':'NOT_ESTABLISHED',
            'pagination_completeness':'COUNT_MATCH_ONLY_NOT_PROOF'}

def _valid_path(path):
    return (isinstance(path,str) and 0<len(path)<=4096 and
            not path.startswith('/') and '\\' not in path and
            all(part not in ('','.','..') for part in path.split('/')) and
            not any(ord(c)<32 or ord(c)==127 for c in path))

def check(snapshot):
    if not isinstance(snapshot,dict):return _incomplete('snapshot_type')
    before,after=snapshot.get('before'),snapshot.get('after')
    files=snapshot.get('filenames')
    if not isinstance(before,dict) or not isinstance(after,dict):
        return _incomplete('two_metadata_reads_required')
    if not isinstance(files,list) or len(files)>_MAX_FILES:
        return _incomplete('inventory_type_or_size')
    repo,number,base,head=(snapshot.get(k) for k in
        ('expected_repo','expected_pr','expected_base','expected_head'))
    if (not isinstance(repo,str) or not repo or type(number) is not int or number<1
        or not isinstance(base,str) or not _SHA40.fullmatch(base)
        or not isinstance(head,str) or not _SHA40.fullmatch(head)):
        return _incomplete('expected_identity_unbound')
    for label,meta in (('before',before),('after',after)):
        if (meta.get('repository')!=repo or type(meta.get('number')) is not int
            or meta['number']!=number or meta.get('base_sha')!=base
            or meta.get('head_sha')!=head):
            return _incomplete(label+'_identity_or_commit_drift')
        count=meta.get('changed_files')
        if type(count) is not int or not (0<=count<=_MAX_FILES):
            return _incomplete(label+'_count_invalid')
    if before['changed_files']!=after['changed_files']:
        return _incomplete('count_changed_between_reads')
    if len(files)!=before['changed_files']:
        return _incomplete('file_inventory_count_mismatch')
    if any(not _valid_path(name) for name in files):
        return _incomplete('invalid_filename')
    if len(set(files))!=len(files):
        return _incomplete('duplicate_filename')
    return {'status':'STABLE_COUNT_MATCH','reasons':[],
            'observed_files':len(files),'pinned_head':head,
            'source_authentication':'NOT_ESTABLISHED',
            'pagination_completeness':'COUNT_MATCH_ONLY_NOT_PROOF'}
