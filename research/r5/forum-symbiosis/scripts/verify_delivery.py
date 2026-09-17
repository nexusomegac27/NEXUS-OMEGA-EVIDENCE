# SPDX-License-Identifier: Apache-2.0
"""Verify an acyclic, complete candidate manifest and C1 handshake. No network."""
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

EXCLUDED = {'OUTPUT_MANIFEST.json', 'RETURN.json', 'DELIVERY_HANDSHAKE.json'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root):
    root = root.resolve()
    errors = []
    manifest = json.loads((root / 'OUTPUT_MANIFEST.json').read_text(encoding='utf-8'))
    result = json.loads((root / 'RETURN.json').read_text(encoding='utf-8'))
    hand = json.loads((root / 'DELIVERY_HANDSHAKE.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'} - EXCLUDED
    seen = set()
    for row in manifest['files']:
        name = row['path']
        if (name in seen or name in EXCLUDED or '\\' in name or ':' in name
                or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts):
            errors.append('INVALID_PATH:' + name)
            continue
        seen.add(name)
        p = root / name
        if p.is_symlink() or not p.resolve().is_relative_to(root) or not p.is_file():
            errors.append('MISSING_OR_UNSAFE:' + name)
        elif digest(p) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append('BYTE_MISMATCH:' + name)
    if actual != seen:
        errors.append('INVENTORY_MISMATCH')
    if set(manifest['excludes']) != EXCLUDED:
        errors.append('EXCLUSION_MISMATCH')
    mh = digest(root / 'OUTPUT_MANIFEST.json')
    rh = digest(root / 'RETURN.json')
    if result['output_manifest_sha256'] != mh or hand['output_manifest_sha256'] != mh or hand['return_sha256'] != rh:
        errors.append('HANDSHAKE_MISMATCH')
    for obj in (manifest, result, hand):
        if obj.get('claim_ceiling') != 'C1_DESCRIPTIVE_ONLY':
            errors.append('CEILING_MISMATCH')
    for key in ('live_publication', 'merge', 'claim_promotion', 'foundation_promotion', 'scientific_validation_established'):
        if result[key] is not False:
            errors.append('AUTHORITY_OR_CLAIM_DRIFT:' + key)
    if not result['remaining_gaps']:
        errors.append('GAPS_MUST_REMAIN_EXPLICIT')
    return {'status': 'FAIL' if errors else 'PASS', 'payload_files':len(seen), 'errors':errors,
            'manifest_sha256':mh,'return_sha256':rh,'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

if __name__ == '__main__':
    try:
        report = verify(Path(sys.argv[1]))
    except (ValueError, KeyError, OSError, IndexError) as error:
        report = {'status':'FAIL','error_type':type(error).__name__}
    print(json.dumps(report, sort_keys=True))
    sys.exit(0 if report['status'] == 'PASS' else 1)
