#!/usr/bin/env python3
"""Independent, frozen V3 source-gap status oracle. Does not modify candidate.

Expected statuses are defined before V3 is implemented. Test only in isolated
temporary directories. V1/V2 must match immutable GitHub blobs in receipt.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
V1 = ROOT / 'alpha_manifest_pin_guard_v1_20261023.py'
V2 = ROOT / 'alpha_manifest_pin_guard_v2_20261023.py'
V3 = ROOT / 'alpha_manifest_pin_guard_v3_20261023.py'
PINS = {
    V1.name: '06a8d4e589390a67187fd14194d7e32cbb56f824e5bf694b8b20b16b404eeadb',
    V2.name: 'b8d3e1089a1f972408e51e7795074e8157a49b2ecbef372908f1fec07c0d72f1',
}


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def fixture(kind):
    src = b'public-safe sample\n'
    commit = '1' * 40
    path = 'research/r16/sample.txt'
    item = {'path': path, 'bytes': len(src), 'sha256': hashlib.sha256(src).hexdigest(), 'git_blob_sha1': blob(src)}
    manifest = {'immutable_assets_parent_commit': commit, 'files': [item]}
    if kind == 'duplicate_paths':
        manifest['files'].append(dict(item))
    if kind == 'invalid_size':
        manifest['files'][0]['bytes'] = -1
    raw = json.dumps(manifest, separators=(',', ':')).encode()
    if kind == 'overflow':
        raw = raw[:-1] + b',"nonfinite":1e999}'
    if kind == 'bad_json':
        raw = b'{not valid json'
    if kind == 'duplicate_keys':
        raw = raw[:-1] + b',"files":[]}'
    digest = hashlib.sha256(raw).hexdigest()
    if kind == 'wrong_pin':
        digest = '0' * 64
    if kind == 'source_mismatch':
        src += b'x'
    observed_blob = blob(src)
    if kind == 'blob_mismatch':
        observed_blob = '0' * 40
    if kind == 'bad_argument':
        raw = None
    return (raw, digest, commit, path, src, observed_blob)


def load(path, key):
    spec = importlib.util.spec_from_file_location(key, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate():
    for path in (V1, V2):
        b = path.read_bytes()
        assert hashlib.sha256(b).hexdigest() == PINS[path.name], f'original bytes mismatch: {path.name}'
    cases = [
        ('positive_match', 'positive', 'MATCH', 'MATCH'),
        ('missing_v1', 'positive', 'MANIFEST_INVALID', 'INCOMPLETE'),
        ('tampered_v1', 'positive', 'INCOMPLETE', 'INCOMPLETE'),
        ('missing_v2', 'positive', None, 'INCOMPLETE'),
        ('tampered_v2', 'positive', None, 'INCOMPLETE'),
        ('wrong_pin', 'wrong_pin', 'MANIFEST_MISMATCH', 'MANIFEST_MISMATCH'),
        ('overflow', 'overflow', 'MANIFEST_INVALID', 'MANIFEST_INVALID'),
        ('bad_json', 'bad_json', 'MANIFEST_INVALID', 'MANIFEST_INVALID'),
        ('duplicate_keys', 'duplicate_keys', 'MANIFEST_INVALID', 'MANIFEST_INVALID'),
        ('duplicate_paths', 'duplicate_paths', 'MANIFEST_AMBIGUOUS', 'MANIFEST_AMBIGUOUS'),
        ('invalid_size', 'invalid_size', 'MANIFEST_INVALID', 'MANIFEST_INVALID'),
        ('source_mismatch', 'source_mismatch', 'SOURCE_MISMATCH', 'SOURCE_MISMATCH'),
        ('blob_mismatch', 'blob_mismatch', 'BLOB_MISMATCH', 'BLOB_MISMATCH'),
        ('bad_argument', 'bad_argument', 'INCOMPLETE', 'INCOMPLETE'),
    ]
    results = []
    for i, (label, kind, expected_v2, expected_v3) in enumerate(cases):
        with tempfile.TemporaryDirectory(prefix='nexus_alpha_sourcegap_') as d:
            tmp = Path(d)
            for src in (V1, V2):
                shutil.copyfile(src, tmp / src.name)
            if V3.exists():
                shutil.copyfile(V3, tmp / V3.name)
            if label == 'missing_v1':
                (tmp / V1.name).unlink()
            elif label == 'tampered_v1':
                (tmp / V1.name).write_bytes((tmp / V1.name).read_bytes() + b'#')
            elif label == 'missing_v2':
                (tmp / V2.name).unlink()
            elif label == 'tampered_v2':
                (tmp / V2.name).write_bytes((tmp / V2.name).read_bytes() + b'#')
            args = fixture(kind)
            v2_status = None
            if expected_v2 is not None:
                try:
                    v2_status = load(tmp / V2.name, 'oracle_v2_' + str(i)).check_pinned_manifest_exactness(*args)['status']
                except Exception as e:
                    v2_status = type(e).__name__
            v3_status = None
            if V3.exists():
                try:
                    v3_status = load(tmp / V3.name, 'oracle_v3_' + str(i)).check_pinned_manifest_exactness(*args)['status']
                except Exception as e:
                    v3_status = type(e).__name__
            results.append({'case': label, 'v2': v2_status, 'v2_expected': expected_v2,
                            'v3': v3_status, 'v3_expected': expected_v3,
                            'v2_pass': v2_status == expected_v2 if expected_v2 is not None else None,
                            'v3_pass': v3_status == expected_v3 if V3.exists() else None})
    return results


if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
