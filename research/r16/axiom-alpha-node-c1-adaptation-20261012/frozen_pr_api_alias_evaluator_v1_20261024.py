#!/usr/bin/env python3
"""Frozen independent test oracle: PR metadata snapshot alias reuse (C1).

Prepared before candidate implementation. Structural identity checks are not
proof of independent HTTP requests, API authentication, or pagination.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
BASE = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '71f114900936a3bcdc59a6aebb4d1a7b9f5b76c8'
FILES = ['research/r16/axiom-alpha-node-c1-adaptation-20261012/a.py',
         'research/r16/axiom-alpha-node-c1-adaptation-20261012/b.py']

def snapshot():
    before = {'repository':REPO,'number':124,'base_sha':BASE,'head_sha':HEAD,'changed_files':2}
    return {'before':before,'after':copy.deepcopy(before),'filenames':FILES.copy(),
            'expected_repo':REPO,'expected_pr':124,'expected_base':BASE,'expected_head':HEAD}

def cases():
    a=[]
    def add(name,change,expected):
        s=snapshot(); change(s); a.append((name,s,expected))
    add('distinct_two_read_objects',lambda s:None,'STABLE_COUNT_MATCH')
    add('same_dict_alias',lambda s:s.__setitem__('after',s['before']),'INCOMPLETE')
    add('same_dict_alias_with_mutation',lambda s:(s.__setitem__('after',s['before']),s['after'].__setitem__('changed_files',2)),'INCOMPLETE')
    add('distinct_equal_copy',lambda s:s.__setitem__('after',copy.deepcopy(s['before'])),'STABLE_COUNT_MATCH')
    add('head_changed',lambda s:s['after'].__setitem__('head_sha','a'*40),'INCOMPLETE')
    add('base_changed',lambda s:s['after'].__setitem__('base_sha','a'*40),'INCOMPLETE')
    add('file_count_changed',lambda s:s['after'].__setitem__('changed_files',3),'INCOMPLETE')
    add('partial_list',lambda s:s['filenames'].pop(),'INCOMPLETE')
    add('duplicate_path',lambda s:s['filenames'].__setitem__(1,s['filenames'][0]),'INCOMPLETE')
    add('path_traversal',lambda s:s['filenames'].__setitem__(1,'../x.py'),'INCOMPLETE')
    add('repo_changed',lambda s:s['after'].__setitem__('repository','other/repo'),'INCOMPLETE')
    add('pr_changed',lambda s:s['after'].__setitem__('number',125),'INCOMPLETE')
    add('missing_after',lambda s:s.__setitem__('after',None),'INCOMPLETE')
    add('empty_list_valid',lambda s:(s['before'].__setitem__('changed_files',0),s['after'].__setitem__('changed_files',0),s.__setitem__('filenames',[])),'STABLE_COUNT_MATCH')
    add('invalid_unicode_surrogate_path',lambda s:s['filenames'].__setitem__(0,'x\ud800.py'),'INCOMPLETE')
    add('invalid_unicode_low_surrogate_path',lambda s:s['filenames'].__setitem__(0,'x\udfff.py'),'INCOMPLETE')
    add('valid_unicode_path',lambda s:s['filenames'].__setitem__(0,'research/r16/é-😀.py'),'STABLE_COUNT_MATCH')
    return a

def evaluate(path):
    spec=importlib.util.spec_from_file_location('isolated_candidate',str(path))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    out=[]
    for name,s,expected in cases():
        try: observed=mod.check(s)['status']
        except Exception as exc: observed='EXCEPTION:'+type(exc).__name__
        out.append({'name':name,'expected':expected,'observed':observed,'pass':observed==expected})
    return {'total':len(out),'passed':sum(x['pass'] for x in out),'records':out}

if __name__=='__main__':
    report=evaluate(Path(sys.argv[1]));print(json.dumps(report,indent=2))
    sys.exit(0 if report['passed']==report['total'] else 1)
