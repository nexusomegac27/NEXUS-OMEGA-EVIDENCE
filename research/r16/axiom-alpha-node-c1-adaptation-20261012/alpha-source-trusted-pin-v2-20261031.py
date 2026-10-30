#!/usr/bin/env python3
"""Offline C1 source-byte gate V2: bind producer bytes to a separate pinned witness.

Caller MUST obtain expected_pin_sha256 independently of the producer. A hash supplied
by the same untrusted producer is not an authority. No remote API/authentication here.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HEX40=re.compile(r'[0-9a-f]{40}\Z')
HEX64=re.compile(r'[0-9a-f]{64}\Z')
REPO='nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PIN_KEYS={'schema','repository','source_commit','root_tree_sha1','path','bytes',
          'sha256','git_blob_sha1','api_tree_entry_sha1','api_tree_entry_mode',
          'api_tree_entry_type','api_tree_truncated','predecessor_sha256',
          'claim_ceiling','provenance'}
MATCH_KEYS={'repository','source_commit','path','bytes','sha256','git_blob_sha1','claim_ceiling'}


def unique_pairs(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError('DUPLICATE_JSON_KEY')
        out[key]=value
    return out


def reject_constant(_):
    raise ValueError('NONFINITE_JSON')


def parse(raw):
    return json.loads(raw.decode('utf-8','strict'),object_pairs_hook=unique_pairs,
                      parse_constant=reject_constant)


def check(manifest_raw, root, pin_path, expected_pin_sha, predecessor_path):
    if not HEX64.fullmatch(expected_pin_sha):raise ValueError('EXPECTED_PIN_SHA256')
    pin_bytes=Path(pin_path).read_bytes()
    if len(pin_bytes)>8192:raise ValueError('OVERSIZE_PIN')
    if hashlib.sha256(pin_bytes).hexdigest()!=expected_pin_sha:
        raise ValueError('TRUSTED_PIN_DIGEST_MISMATCH')
    pin=parse(pin_bytes)
    if type(pin) is not dict or set(pin)!=PIN_KEYS or pin['schema']!='NEXUS_ALPHA_SOURCE_TRUSTED_PIN_V2':
        raise ValueError('TRUSTED_PIN_SCHEMA')
    if pin['repository']!=REPO or pin['claim_ceiling']!='C1_DESCRIPTIVE_ONLY':
        raise ValueError('TRUSTED_PIN_SCOPE')
    for field in ('source_commit','root_tree_sha1','git_blob_sha1','api_tree_entry_sha1','predecessor_sha256'):
        pattern=HEX64 if field=='predecessor_sha256' else HEX40
        if type(pin[field]) is not str or not pattern.fullmatch(pin[field]):
            raise ValueError('TRUSTED_PIN_HASH_FORMAT')
    if type(pin['bytes']) is not int or not 0<=pin['bytes']<=1048576:
        raise ValueError('TRUSTED_PIN_BYTES')
    if type(pin['sha256']) is not str or not HEX64.fullmatch(pin['sha256']):
        raise ValueError('TRUSTED_PIN_SHA256')
    if type(pin['path']) is not str or not pin['path'] or len(pin['path'])>512:
        raise ValueError('TRUSTED_PIN_PATH')
    if pin['api_tree_entry_sha1']!=pin['git_blob_sha1'] or pin['api_tree_entry_mode']!='100644' or pin['api_tree_entry_type']!='blob' or pin['api_tree_truncated'] is not False:
        raise ValueError('TRUSTED_PIN_TREE_PROJECTION')
    if pin['provenance']!='GITHUB_API_COMMIT_AND_RECURSIVE_TREE_READ_ONLY_NOT_AUTHENTICATED':
        raise ValueError('TRUSTED_PIN_PROVENANCE')
    if len(manifest_raw)>16384:raise ValueError('OVERSIZE_MANIFEST')
    manifest=parse(manifest_raw)
    if type(manifest) is not dict or any(manifest.get(k)!=pin[k] or type(manifest.get(k)) is not type(pin[k]) for k in MATCH_KEYS):
        raise ValueError('TRUSTED_PIN_MANIFEST_MISMATCH')
    expected_url='https://github.com/'+REPO+'/blob/'+pin['source_commit']+'/'+pin['path']
    if manifest.get('source_ref')!=expected_url:
        raise ValueError('TRUSTED_PIN_SOURCE_REF_MISMATCH')
    predecessor_bytes=Path(predecessor_path).read_bytes()
    if len(predecessor_bytes)>65536 or hashlib.sha256(predecessor_bytes).hexdigest()!=pin['predecessor_sha256']:
        raise ValueError('PREDECESSOR_DIGEST_MISMATCH')
    proc=subprocess.run([sys.executable,'-S',str(predecessor_path),str(root)],
                        input=manifest_raw,capture_output=True,timeout=8)
    if proc.returncode!=0 or len(proc.stdout)>16384:
        raise ValueError('LOCAL_SOURCE_GATE_REJECTED')
    old=parse(proc.stdout)
    if type(old) is not dict or old.get('state')!='LOCAL_SOURCE_BYTES_MATCH' or any(old.get(k)!=pin[k] for k in ('bytes','sha256','git_blob_sha1','source_commit','path')):
        raise ValueError('LOCAL_SOURCE_GATE_MISMATCH')
    return {'state':'TRUSTED_PIN_SOURCE_BYTES_MATCH',
            'bytes':pin['bytes'],'sha256':pin['sha256'],'git_blob_sha1':pin['git_blob_sha1'],
            'source_commit':pin['source_commit'],'root_tree_sha1':pin['root_tree_sha1'],
            'path':pin['path'],'trusted_pin_sha256':expected_pin_sha,
            'commit_tree_membership':'API_PROJECTION_MATCH_NOT_CRYPTOGRAPHICALLY_RECONSTRUCTED',
            'transport_authentication':'NOT_VERIFIED',
            'external_pin_authority':'CALLER_MUST_VERIFY_INDEPENDENTLY',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        if len(sys.argv)!=5:raise ValueError('USAGE_ROOT_PIN_EXPECTED_SHA_PREDECESSOR')
        raw=sys.stdin.buffer.read(16385)
        out=check(raw,*sys.argv[1:])
        print(json.dumps(out,sort_keys=True,separators=(',',':')))
        return 0
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,json.JSONDecodeError,
            subprocess.TimeoutExpired) as e:
        print(json.dumps({'state':'FAIL_CLOSED','reason':str(e)},sort_keys=True))
        return 2


if __name__=='__main__':sys.exit(main())
