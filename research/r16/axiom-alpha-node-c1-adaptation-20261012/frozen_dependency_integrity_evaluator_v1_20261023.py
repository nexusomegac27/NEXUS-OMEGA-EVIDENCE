#!/usr/bin/env python3
"""Frozen independent evaluator for source-exact dependency pinning.

The candidate is supplied by CLI argument; this evaluator neither imports nor
modifies candidate code. All fixtures are synthetic and local. Failures do not
establish platform, GitHub actor, runtime, or scientific authentication.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
NAMES = [f'alpha_pr_publication_preflight_guard_v{i}_20261023.py' for i in (1, 2, 3)]
MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '3edc1dd69b2906f4812f1ad24db0e9e5fd2718d7'
BRANCH = 'axiom/alpha-export-surface-closure-c1-20261021'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PATH = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_pr_publication_preflight_guard_v4_20261023.py'
BASE = {
    'repo': {'repository_full_name': REPO, 'owner': {'login': 'nexusomegac27'},
             'permissions': {'push': True}, 'default_branch': 'main'},
    'pr': {'number': 124, 'state': 'open', 'merged': False, 'draft': True,
           'base': 'main', 'base_sha': MAIN, 'head': BRANCH, 'head_sha': HEAD,
           'head_repo_full_name': REPO, 'user': {'login': 'nexusomegac27'}},
    'main': {'name': 'main', 'sha': MAIN},
    'branch': {'name': BRANCH, 'sha': HEAD},
    'target': {'pinned_main': MAIN, 'pinned_head': HEAD,
               'repository_full_name': REPO, 'pr_number': 124,
               'branch': BRANCH, 'path': PATH, 'path_absent_confirmed': True,
               'observed_at': '2026-10-23T11:38:00Z'}
}
NOW = '2026-10-23T11:38:30Z'


def cases():
    return [
        ('valid_clean', None, None, 'READY_FOR_CONTENT_CHECK'),
        ('wrong_branch_clean', 'wrong_branch', None, 'WRONG_BRANCH'),
        ('no_push_clean', 'no_push', None, 'ACTOR_SCOPE_HOLD'),
        ('naive_timestamp_clean', 'naive_time', None, 'TIMEZONE_REQUIRED'),
        ('missing_target_clean', 'missing_target', None, 'INCOMPLETE'),
        ('benign_v1_byte_append', None, 'append_v1', 'INCOMPLETE'),
        ('benign_v2_byte_append', None, 'append_v2', 'INCOMPLETE'),
        ('benign_v3_byte_append', None, 'append_v3', 'INCOMPLETE'),
        ('v2_wrong_branch_bypass', 'wrong_branch', 'bypass_v2', 'INCOMPLETE'),
        ('v1_wrong_branch_bypass', 'wrong_branch', 'bypass_v1', 'INCOMPLETE'),
        ('missing_v2_dependency', None, 'missing_v2', 'INCOMPLETE'),
        ('symlink_v2_dependency', None, 'symlink_v2', 'INCOMPLETE'),
    ]


def mutate_files(root, mutation):
    if mutation is None:
        return
    n1, n2, n3 = (root / n for n in NAMES)
    if mutation.startswith('append_v'):
        n = {'append_v1': n1, 'append_v2': n2, 'append_v3': n3}[mutation]
        n.write_bytes(n.read_bytes() + b'\n')
    elif mutation == 'bypass_v2':
        src = n2.read_text()
        old = '    return _v1(snapshot, now_utc)\n'
        assert src.count(old) == 2
        src = src[:-len(old)] + "    return {'status': 'READY_FOR_CONTENT_CHECK'}\n"
        n2.write_text(src)
    elif mutation == 'bypass_v1':
        src = n1.read_text()
        old = "return {'status': 'WRONG_BRANCH'}"
        assert src.count(old) == 1
        n1.write_text(src.replace(old, "return {'status': 'READY_FOR_CONTENT_CHECK'}"))
    elif mutation == 'missing_v2':
        n2.unlink()
    elif mutation == 'symlink_v2':
        src = root / 'shadow_v2.py'
        src.write_bytes(n2.read_bytes())
        n2.unlink()
        n2.symlink_to(src)
    else:
        raise ValueError(mutation)


def run_case(module, case):
    name, snapshot_change, file_change, expected = case
    with tempfile.TemporaryDirectory(prefix='alpha_dep_eval_') as d:
        root = Path(d)
        for n in NAMES:
            shutil.copyfile(ROOT / n, root / n)
        if module.endswith('v4_20261023'):
            shutil.copyfile(ROOT / (module + '.py'), root / (module + '.py'))
        mutate_files(root, file_change)
        snapshot = copy.deepcopy(BASE)
        if snapshot_change == 'wrong_branch':
            snapshot['target']['branch'] = 'codex/wrong-branch'
        elif snapshot_change == 'no_push':
            snapshot['repo']['permissions']['push'] = False
        elif snapshot_change == 'naive_time':
            snapshot['target']['observed_at'] = '2026-10-23T11:38:00'
        elif snapshot_change == 'missing_target':
            snapshot['target'] = None
        code = ("import importlib,json,sys; s=json.load(sys.stdin); "
                "m=importlib.import_module(sys.argv[1]); "
                "x=m.check_pr_publication_preflight(s['snapshot'],s['now']); "
                "print(json.dumps({'status':x.get('status'),'unchanged':s['snapshot']==s['before']}))")
        inp = {'snapshot': snapshot, 'before': copy.deepcopy(snapshot), 'now': NOW}
        p = subprocess.run([sys.executable, '-I', '-c', code, module],
                           input=json.dumps(inp), capture_output=True, text=True,
                           timeout=8, cwd=root, env={**os.environ, 'PYTHONPATH': str(root)})
        # -I ignores PYTHONPATH, so prepend an explicit module directory in -c.
        if p.returncode != 0 and 'ModuleNotFoundError' in p.stderr:
            code = "import sys;sys.path.insert(0,sys.argv[2]);" + code
            p = subprocess.run([sys.executable, '-I', '-c', code, module, str(root)],
                               input=json.dumps(inp), capture_output=True, text=True,
                               timeout=8, cwd=root)
        try:
            out = json.loads(p.stdout)
            actual = out['status'] if out.get('unchanged') is True else 'MUTATED_INPUT'
        except (ValueError, KeyError, TypeError):
            actual = 'EXCEPTION' if p.returncode else 'BAD_OUTPUT'
        return {'case': name, 'expected': expected, 'actual': actual,
                'pass': actual == expected, 'negative': bool(file_change),
                'stderr_type': p.stderr.split(':')[0][-100:] if p.returncode else None}


def main():
    module = sys.argv[1] if len(sys.argv) > 1 else 'alpha_pr_publication_preflight_guard_v3_20261023'
    rows = [run_case(module, c) for c in cases()]
    result = {'module': module, 'passed': sum(x['pass'] for x in rows),
              'total': len(rows), 'rows': rows,
              'scope': 'ISOLATED_SYNTHETIC_DEPENDENCY_BYTE_INTEGRITY_ONLY'}
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result['passed'] == result['total'] else 1


if __name__ == '__main__':
    sys.exit(main())
