"""Independent C1 subprocess oracle; frozen before candidate GitHub commit."""
import json
import subprocess
import sys
P = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
R = {'path': P+'Alpha.py', 'bytes': 42, 'sha256': 'a'*64, 'git_blob_sha1': 'b'*40}
def pack(rows):
    return json.dumps({'count': len(rows), 'files': rows})
def change(**kw):
    return dict(R, **kw)
CASES = [
    ('valid', pack([R]), True),
    ('valid_pair', pack([R, change(path=P+'Beta.py')]), True),
    ('missing_sha', pack([{k:v for k,v in R.items() if k!='sha256'}]), False),
    ('missing_blob', pack([{k:v for k,v in R.items() if k!='git_blob_sha1'}]), False),
    ('bad_sha', pack([change(sha256='z'*64)]), False),
    ('bad_blob', pack([change(git_blob_sha1='g'*40)]), False),
    ('zero_bytes', pack([change(bytes=0)]), False),
    ('boolean_bytes', pack([change(bytes=True)]), False),
    ('extra_field', pack([change(extra='x')]), False),
    ('casefold', pack([R, change(path=P+'alpha.py')]), False),
    ('unsafe_int', pack([change(bytes=9007199254740992)]), False),
    ('reserved_path', pack([change(path=P+'CON.txt')]), False),
]
def evaluate(script):
    failed = []
    for name, raw, expected in CASES:
        p = subprocess.run([sys.executable, script], input=raw, text=True,
                           capture_output=True, timeout=5)
        try:
            status = json.loads(p.stdout)['status']
            actual = p.returncode == 0 and status == 'PASS_C1'
            coherent = (p.returncode == 0) == (status == 'PASS_C1')
        except (ValueError, KeyError, TypeError):
            actual, coherent = False, False
        if not coherent or actual != expected:
            failed.append(name)
    return {'correct': len(CASES)-len(failed), 'total': len(CASES), 'failures': failed}
if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
