#!/usr/bin/env python3
"""Independent subprocess oracle: immutable before candidate publication."""
import copy
import json
import os
import subprocess
import sys
import tempfile

PIN = 'b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9'


def run(candidate, payload):
    with tempfile.TemporaryDirectory() as root:
        path = os.path.join(root, 'input.json')
        with open(path, 'w', encoding='utf-8') as out:
            json.dump(payload, out)
        result = subprocess.run([sys.executable, '-S', candidate, path], capture_output=True, text=True, timeout=8)
        return result.returncode, json.loads(result.stdout)


def main(candidate, snapshot):
    with open(snapshot, encoding='utf-8') as handle:
        data = json.load(handle)
    checks = []

    def check(name, payload, expected_status, expected_count=None):
        code, result = run(candidate, payload)
        ok = (code == 0 if expected_status != 'FAIL_CLOSED' else code == 2) and result.get('status') == expected_status
        if expected_count is not None:
            ok = ok and result.get('matching_workflows') == expected_count
        checks.append((name, ok))

    check('real-pinned-inventory', data, 'STATIC_REQUIRED_CONTEXT_COLLISION', 12)
    one = copy.deepcopy(data)
    for i, item in enumerate(one['workflows']):
        item['jobs'] = ['unique_' + str(i)] if 'validate' in item['jobs'] else item['jobs']
    one['workflows'][0]['jobs'] = ['validate']
    check('unique-positive-control', one, 'UNIQUE_OR_ABSENT', 1)
    none = copy.deepcopy(one)
    none['workflows'][0]['jobs'] = ['not_validate']
    check('absent-positive-control', none, 'UNIQUE_OR_ABSENT', 0)
    mutations = {}
    x = copy.deepcopy(data); x['repo'] = 'another/repo'; mutations['foreign-repo'] = x
    x = copy.deepcopy(data); x['pinned_commit'] = 'main'; mutations['mutable-pin'] = x
    x = copy.deepcopy(data); x['workflows'].append(copy.deepcopy(x['workflows'][0])); mutations['duplicate-path'] = x
    x = copy.deepcopy(data); x['workflows'][0]['blob_sha'] = 'z'*40; mutations['invalid-blob'] = x
    x = copy.deepcopy(data); x['workflows'][0]['jobs'] = []; mutations['missing-jobs'] = x
    x = copy.deepcopy(data); x['workflows'][0]['jobs'] = ['validate','validate']; mutations['duplicate-job'] = x
    x = copy.deepcopy(data); x['workflows'][0]['path'] = '../evil.yml'; mutations['path-escape'] = x
    x = copy.deepcopy(data); x['workflows'] = []; mutations['empty-inventory'] = x
    x = copy.deepcopy(data); x['required_context'] = ['validate']; mutations['invalid-context'] = x
    x = copy.deepcopy(data); x['workflows'][0]['unexpected'] = 'value'; mutations['extra-field'] = x
    x = copy.deepcopy(data); x['workflows'][0]['jobs'] = [1]; mutations['nonstring-job'] = x
    for name, payload in mutations.items():
        check(name, payload, 'FAIL_CLOSED')
    with tempfile.TemporaryDirectory() as root:
        path = os.path.join(root, 'duplicate.json')
        with open(path, 'w') as f:
            f.write('{"repo":"x","repo":"y"}')
        p = subprocess.run([sys.executable, '-S', candidate, path], capture_output=True, text=True, timeout=8)
        checks.append(('duplicate-json-keys', p.returncode == 2 and json.loads(p.stdout).get('status') == 'FAIL_CLOSED'))
    print(json.dumps({'pass': sum(ok for _, ok in checks), 'total': len(checks), 'checks': checks}, sort_keys=True))
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
