#!/usr/bin/env python3
"""C1 isolated, independent PR124 content-binding evaluator (no network/writes).

The evaluator consumes a separate pinned Git tree and actual source bytes;
manifest producer metadata alone is never treated as an oracle.
"""
import copy
import hashlib
import json

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'

def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def validate(manifest, index, tree, source_bytes):
    errors = []
    entries = manifest.get('files', [])
    index_names = [PREFIX + x['name'] for x in index.get('files', [])]
    names = [x.get('path') for x in entries]
    expected_head = index.get('source', {}).get('pinned_pre_index_head')
    expected_base = index.get('source', {}).get('base_commit')
    for field, expected in [('pinned_source_head', expected_head), ('pinned_main', expected_base),
                            ('parent_index_blob', index.get('_blob_sha'))]:
        if manifest.get(field) != expected:
            errors.append('PIN_MISMATCH:' + field)
    if len(names) != len(set(names)):
        errors.append('DUPLICATE_PATH')
    if names != sorted(names):
        errors.append('NOT_LEXICOGRAPHIC')
    if set(names) != set(index_names):
        errors.append('INVENTORY_MISMATCH')
    if len(entries) != len(index_names) or manifest.get('count') != len(index_names):
        errors.append('COUNT_MISMATCH')
    tree_map = {x['path']: x for x in tree if x.get('type') == 'blob'}
    for entry in entries:
        path = entry.get('path')
        if not isinstance(path, str) or not path.startswith(PREFIX) or '/..' in path:
            errors.append('OUT_OF_SCOPE')
            continue
        item = tree_map.get(path)
        raw = source_bytes.get(path)
        if item is None or raw is None:
            errors.append('SOURCE_NOT_PRESENT:' + path)
            continue
        if entry.get('bytes') != len(raw) or item.get('size') != len(raw):
            errors.append('BYTE_COUNT_MISMATCH:' + path)
        if entry.get('sha256') != hashlib.sha256(raw).hexdigest():
            errors.append('SHA256_MISMATCH:' + path)
        computed_blob = blob_sha(raw)
        if entry.get('git_blob_sha1') != computed_blob or item.get('sha') != computed_blob:
            errors.append('GIT_BLOB_MISMATCH:' + path)
    return sorted(set(errors))

def fixture():
    paths = [PREFIX+'a.py', PREFIX+'b.json']
    data = {paths[0]: b'abc\n', paths[1]: b'{"v":1}\n'}
    tree = [{'path': p, 'type':'blob', 'sha':blob_sha(data[p]), 'size':len(data[p])} for p in paths]
    index = {'source': {'pinned_pre_index_head':'a'*40, 'base_commit':'b'*40},
             '_blob_sha':'c'*40, 'files':[{'name':p[len(PREFIX):]} for p in paths]}
    manifest = {'pinned_source_head':'a'*40, 'pinned_main':'b'*40,
                'parent_index_blob':'c'*40, 'count':2,
                'files':[{'path':p, 'bytes':len(data[p]), 'sha256':hashlib.sha256(data[p]).hexdigest(),
                          'git_blob_sha1':blob_sha(data[p])} for p in paths]}
    return manifest,index,tree,data

def selftest():
    m,i,t,d = fixture()
    cases = [('valid',lambda m,i,t,d:None,False),
      ('missing_path',lambda m,i,t,d:m['files'].pop(),True),
      ('extra_path',lambda m,i,t,d:m['files'].append(dict(m['files'][0],path=PREFIX+'extra.py')),True),
      ('duplicate_path',lambda m,i,t,d:m['files'].append(copy.deepcopy(m['files'][0])),True),
      ('wrong_sha256',lambda m,i,t,d:m['files'][0].update(sha256='0'*64),True),
      ('wrong_blob',lambda m,i,t,d:m['files'][0].update(git_blob_sha1='0'*40),True),
      ('wrong_size',lambda m,i,t,d:m['files'][0].update(bytes=999),True),
      ('changed_source',lambda m,i,t,d:d.update({PREFIX+'a.py':b'evil\n'}),True),
      ('wrong_head',lambda m,i,t,d:m.update(pinned_source_head='0'*40),True),
      ('wrong_parent_index',lambda m,i,t,d:m.update(parent_index_blob='0'*40),True),
      ('out_of_scope',lambda m,i,t,d:m['files'][0].update(path='outside/a.py'),True),
      ('reverse_order',lambda m,i,t,d:m['files'].reverse(),True),
      ('wrong_tree',lambda m,i,t,d:t[0].update(sha='0'*40),True),
      ('wrong_count',lambda m,i,t,d:m.update(count=1),True)]
    passed=0
    for name,mutation,should_fail in cases:
        mm,ii,tt,dd=copy.deepcopy((m,i,t,d))
        mutation(mm,ii,tt,dd)
        errors=validate(mm,ii,tt,dd)
        if bool(errors)!=should_fail:
            raise AssertionError((name,errors,should_fail))
        passed+=1
    return {'passed':passed,'total':len(cases),'negative_fixtures':len(cases)-1}

if __name__=='__main__':
    print(json.dumps(selftest(),sort_keys=True))
