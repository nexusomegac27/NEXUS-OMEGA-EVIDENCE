#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Predeclared synthetic oracle for a GitHub release asset metadata locator.

Independent of candidate implementation; a located release asset is NOT
original-byte verification, successful download, authenticated receiver, or
handoff completion. This evaluator performs no network or filesystem writes.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

OWNER, REPO, TAG, NAME = 'nexusomegac27', 'kammflug', 'v1', 'kammflug-paket.zip'
API = f'https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}'
ASSET = f'https://github.com/{OWNER}/{REPO}/releases/download/{TAG}/{NAME}'
ASSET_API = f'https://api.github.com/repos/{OWNER}/{REPO}/releases/assets/675456328'
DIGEST = 'sha256:6372e9c1081bae50c4b3f14b32c50ab4f5d3128bb76a3708381d223d3006c9fa'
FOUND = 'ASSET_LOCATED_METADATA_ONLY_C1'
BAD = 'INCOMPLETE_FAIL_CLOSED'
ABSENT = 'SOURCE_NOT_PRESENT_IN_RELEASE_METADATA'

def base():
    return {'id': 423503294, 'tag_name': TAG, 'draft': False, 'prerelease': False,
            'assets': [{'id': 675456328, 'name': NAME, 'size': 301238,
                        'state': 'uploaded', 'content_type': 'application/zip',
                        'browser_download_url': ASSET, 'url': ASSET_API,
                        'digest': DIGEST}]}

# The expected statuses are literals, never computed from the candidate.
def fixtures():
    yield 'observed_metadata_positive', base(), API, FOUND
    x=base();x['assets'][0]['digest']=None;yield 'missing_digest_metadata_only',x,API,FOUND
    x=base();x['assets']=[];yield 'asset_absent',x,API,ABSENT
    x=base();x['assets'][0]['name']='other.zip';yield 'wrong_name',x,API,ABSENT
    x=base();x['assets'].append(copy.deepcopy(x['assets'][0]));yield 'duplicate_name',x,API,BAD
    x=base();x['assets'].append({**x['assets'][0], 'name':'KAMMFLUG-PAKET.ZIP'});yield 'casefold_collision',x,API,BAD
    x=base();x['draft']=True;yield 'draft',x,API,BAD
    x=base();x['prerelease']=True;yield 'prerelease',x,API,BAD
    x=base();x['tag_name']='v2';yield 'tag_drift',x,API,BAD
    x=base();yield 'source_url_spoof',x,'https://api.github.com/repos/attacker/kammflug/releases/tags/v1',BAD
    x=base();yield 'source_url_query',x,API+'?per_page=100',BAD
    x=base();x['assets'][0]['browser_download_url']='https://evil.example/payload.zip';yield 'download_url_spoof',x,API,BAD
    x=base();x['assets'][0]['url']='https://api.github.com/repos/attacker/kammflug/releases/assets/675456328';yield 'asset_api_url_spoof',x,API,BAD
    x=base();x['assets'][0]['size']=True;yield 'boolean_size',x,API,BAD
    x=base();x['assets'][0]['size']=0;yield 'zero_size',x,API,BAD
    x=base();x['assets'][0]['size']=-1;yield 'negative_size',x,API,BAD
    x=base();x['assets'][0]['size']=2**53;yield 'unsafe_integer_size',x,API,BAD
    x=base();x['assets'][0]['id']=True;yield 'boolean_asset_id',x,API,BAD
    x=base();x['id']=True;yield 'boolean_release_id',x,API,BAD
    x=base();x['assets'][0]['state']='new';yield 'not_uploaded',x,API,BAD
    x=base();x['assets'][0]['content_type']='text/html';yield 'html_asset',x,API,BAD
    x=base();x['assets'][0]['digest']='sha256:'+'z'*64;yield 'malformed_digest',x,API,BAD
    x=base();x['assets'][0]['digest']='sha512:'+'a'*128;yield 'wrong_digest_algorithm',x,API,BAD
    x=base();x['assets']='oops';yield 'invalid_asset_collection',x,API,BAD
    yield 'nonobject_snapshot',None,API,BAD
    x=base();x['assets'][0]['name']='KAMMFLUG-PAKET.ZIP';yield 'case_sensitive_absence',x,API,ABSENT


def evaluate(candidate_path):
    spec=importlib.util.spec_from_file_location('candidate_under_test',str(candidate_path))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    outcomes=[]
    for name,snapshot,source,expected in fixtures():
        try:
            result=mod.locate_release_asset(copy.deepcopy(snapshot),source,OWNER,REPO,TAG,NAME)
            actual=result.get('status')
            correct=(actual==expected and result.get('original_bytes_verified') is False
                     and result.get('sha256_verified') is False
                     and result.get('claim_ceiling')=='C1_DESCRIPTIVE_ONLY')
            if expected==FOUND:
                correct=correct and result.get('asset_id')==675456328 and result.get('asset_size_reported')==301238
                correct=correct and result.get('asset_url')==ASSET
            if expected!=FOUND:
                correct=correct and 'asset_url' not in result
        except Exception:
            actual='EXCEPTION';correct=False
        outcomes.append({'case':name,'expected':expected,'actual':actual,'pass':correct})
    print(json.dumps({'correct':sum(x['pass'] for x in outcomes),'total':len(outcomes),'outcomes':outcomes},indent=2))
    return all(x['pass'] for x in outcomes)

if __name__=='__main__':
    raise SystemExit(0 if evaluate(Path(sys.argv[1])) else 1)
