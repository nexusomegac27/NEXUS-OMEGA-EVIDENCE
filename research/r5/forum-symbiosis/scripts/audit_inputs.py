# SPDX-License-Identifier: Apache-2.0
"""Read-only ZIP custody check. Prints a sanitized report, never extracts/executes inputs."""
import argparse
import hashlib
import io
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

NAMES = [
    '78OJZ7ibkodxSykV-grok-workspace.zip',
    'NEXUS_FORUM_GROK_MODEL_PROPOSAL_ORDER_20260917_R0.zip',
    'nexus-omega_MANUS-trust-dashboard.zip',
    'NEXUS_- MODEL-C-R10-EVIDENTIAL.txt',
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect_archive(z):
    seen, issues = set(), []
    total = 0
    for entry in z.infolist():
        name = entry.filename
        parts = PurePosixPath(name.replace('\\', '/')).parts
        normalized = '/'.join(p.rstrip(' .').casefold() for p in parts)
        if (name.startswith(('/', '\\')) or ':' in name or '\\' in name
                or '..' in parts or any(p.rstrip(' .') != p for p in parts)
                or any(re.fullmatch(r'(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?', p, re.I) for p in parts)):
            issues.append({'entry': name, 'issue': 'UNSAFE_PATH'})
        if normalized in seen:
            issues.append({'entry': name, 'issue': 'DUPLICATE_PATH'})
        seen.add(normalized)
        if stat.S_ISLNK(entry.external_attr >> 16):
            issues.append({'entry': name, 'issue': 'SYMLINK'})
        if entry.flag_bits & 1:
            issues.append({'entry': name, 'issue': 'ENCRYPTED'})
        total += entry.file_size
        if entry.file_size > 32 * 1024 * 1024:
            issues.append({'entry': name, 'issue': 'ENTRY_TOO_LARGE'})
    if total > 128 * 1024 * 1024:
        issues.append({'issue': 'TOTAL_TOO_LARGE'})
    # Only bounded archives are decompressed for CRC verification.
    crc = z.testzip() if not issues else 'NOT_RUN'
    return {'entries': len(z.infolist()), 'uncompressed_bytes': total,
            'issues': issues, 'crc_error': crc, 'extracted': False, 'executed': False}

def check_files(z, manifest, prefix=''):
    checks = []
    for row in manifest['files']:
        path = row['path']
        data = z.read(prefix + path) if prefix + path in z.namelist() else None
        digest = sha(data) if data is not None else None
        checks.append({'path': path, 'expected_sha256': row['sha256'],
                       'actual_sha256': digest, 'expected_bytes': row.get('bytes'),
                       'actual_bytes': len(data) if data is not None else None,
                       'match': digest == row['sha256'] and (row.get('bytes') is None or len(data) == row['bytes'])})
    return checks

def audit(root, current=None):
    report = {'schema_version': 'forum-input-audit/1', 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
              'scope': 'Provided archives and optional bounded current-file comparison; not full corpus audit', 'inputs': []}
    for name in NAMES:
        data = (root / name).read_bytes()
        item = {'name': name, 'bytes': len(data), 'sha256': sha(data)}
        if name.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                item['archive'] = inspect_archive(z)
        report['inputs'].append(item)
    with zipfile.ZipFile(root / NAMES[0]) as g, zipfile.ZipFile(root / NAMES[1]) as o:
        report['nested_order_match'] = sha(g.read('attachments/' + NAMES[1])) == sha((root / NAMES[1]).read_bytes())
        manifest = json.loads(o.read('DELIVERY_MANIFEST.json'))
        report['order_manifest'] = check_files(o, manifest)
        report['grok_manifest'] = check_files(g, json.loads(g.read('public/return/OUTPUT_MANIFEST.json')), 'public/return/')
        ret = json.loads(g.read('public/return/GROK_RETURN.json'))
        hand = json.loads(g.read('public/return/DELIVERY_HANDSHAKE.json'))
        report['grok_bindings'] = {
            'order_sha256': sha(o.read('01_GROK_ORDER.md')),
            'order_matches': ret['order_sha256'] == sha(o.read('01_GROK_ORDER.md')),
            'return_sha256': sha(g.read('public/return/GROK_RETURN.json')),
            'manifest_sha256': sha(g.read('public/return/OUTPUT_MANIFEST.json')),
            'handshake_sha256': sha(g.read('public/return/DELIVERY_HANDSHAKE.json')),
            'manifest_matches_return': ret['output_manifest_sha256'] == sha(g.read('public/return/OUTPUT_MANIFEST.json')),
            'manifest_matches_handshake': hand['output_manifest_sha256'] == sha(g.read('public/return/OUTPUT_MANIFEST.json')),
            'return_matches_handshake': hand['grok_return_sha256'] == sha(g.read('public/return/GROK_RETURN.json')),
        }
        prefix = 'artifacts/forum-v0-supplement/'
        binding = json.loads(g.read(prefix + '07_SOURCE_BINDING.json'))
        report['supplement_bindings'] = check_files(g, {'files': [
            {'path': name, 'sha256': row['sha256'], 'bytes': row['bytes']}
            for name, row in binding['files'].items()
        ]}, prefix)
        report['public_return_duplicates'] = []
        for name in g.namelist():
            if name.startswith('public/return/') and not name.endswith('/'):
                duplicate = '.vercel/output/static/' + name[len('public/'):]
                if duplicate in g.namelist():
                    report['public_return_duplicates'].append({'path': name, 'match': g.read(name) == g.read(duplicate)})
        if current:
            rows = []
            for name in o.namelist():
                prefix = 'inputs/current_manifest_files/'
                if name.startswith(prefix) and not name.endswith('/'):
                    rel = name[len(prefix):]
                    p = (current / rel).resolve()
                    p.relative_to(current.resolve())
                    digest = sha(p.read_bytes()) if p.is_file() else None
                    rows.append({'path': rel, 'snapshot_sha256': sha(o.read(name)), 'current_sha256': digest,
                                 'match': digest == sha(o.read(name))})
            report['current_cursor_files'] = rows
        report['r9_return_sha256'] = sha(o.read('inputs/receipts/R9_RETURN.md'))
        report['review_summary_predecessor_return'] = 'c73e4dab2ddafd0c4fb4a8872ab4081e2a86c09c0ce2b5cf6e812fe1339e670d'
        report['review_summary_matches_supplied_grok'] = report['review_summary_predecessor_return'] == report['grok_bindings']['return_sha256']
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_directory', type=Path)
    parser.add_argument('--current-root', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.input_directory, args.current_root), ensure_ascii=False, indent=2))
