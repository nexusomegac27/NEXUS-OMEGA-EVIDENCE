"""Read-only byte verification; no imported research code or network calls."""
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def verify(root):
    manifest = read_json(root / 'SHA256_MANIFEST.json')
    paths = set()
    for item in manifest['files']:
        rel = item['path']
        if rel in paths:
            raise ValueError('Duplicate manifest path: ' + rel)
        paths.add(rel)
        path = (root / rel).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Out-of-package path: ' + rel)
        data = path.read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('Manifest mismatch: ' + rel)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != paths | {'SHA256_MANIFEST.json', 'SHA256SUMS.txt'}:
        raise ValueError('Unlisted or missing file: ' + str(actual ^ (paths | {'SHA256_MANIFEST.json', 'SHA256SUMS.txt'})))
    sums = {}
    for line in (root / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        expected, rel = line.split('  ', 1)
        if rel in sums or rel not in actual or rel == 'SHA256SUMS.txt':
            raise ValueError('Invalid checksum path: ' + rel)
        sums[rel] = expected
        if digest((root / rel).read_bytes()) != expected:
            raise ValueError('Checksum mismatch: ' + rel)
    if set(sums) != actual - {'SHA256SUMS.txt'}:
        raise ValueError('Checksum coverage mismatch')
    for path in root.rglob('*.json'):
        read_json(path)
    bindings = read_json(root / 'INPUT_BINDINGS.json')
    for item in bindings['files']:
        data = (root / item['path']).read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('Input binding mismatch: ' + item['path'])
    with zipfile.ZipFile(root / 'inputs/R10R9_GROK_RETURN_20261005.zip') as archive:
        members = archive.infolist()
        if len(members) != 29 or archive.testzip() is not None:
            raise ValueError('ZIP integrity/count failure')
        for member in members:
            rel = Path(member.filename)
            if len(rel.parts) != 2 or rel.parts[0] != 'out' or member.is_dir():
                raise ValueError('Unexpected archive member')
            if archive.read(member) != (root / 'inputs/GROK_BOT_RETURN' / rel.name).read_bytes():
                raise ValueError('Extracted file differs: ' + rel.name)
    inner = read_json(root / 'inputs/GROK_BOT_RETURN/G24_MANIFEST_SHA256.json')
    if len(inner['files']) != 28:
        raise ValueError('G24 count mismatch')
    for item in inner['files']:
        data = (root / 'inputs/GROK_BOT_RETURN' / item['file']).read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('G24 mismatch: ' + item['file'])
    rows = list(csv.DictReader(io.StringIO((root / 'inputs/GROK_BOT_RETURN/G01_SOURCE_EXACT_LEDGER.csv').read_text(encoding='utf-8'))))
    if len(rows) != 193 or len(rows[0]) != 15:
        raise ValueError('G01 ledger shape mismatch')
    hs = read_json(root / 'HANDSHAKE.json')
    for filename, field in [('ORDER.md','order_sha256'),('INPUT_BINDINGS.json','input_bindings_sha256')]:
        if digest((root / filename).read_bytes()) != hs[field]:
            raise ValueError('Handshake binding mismatch: ' + field)
    if hs['reviewer_acknowledged'] or hs['reviewer_execution_established'] or hs['execution_authorized'] or hs['promotion'] or hs['merge']:
        raise ValueError('Unauthorized state in outgoing handshake')
    return {'status':'PASS_BYTE_INTEGRITY_ONLY','manifest_files':len(paths),'checksum_files':len(sums),'input_bindings':len(bindings['files']),'zip_files':29,'g24_matches':28,'ledger_rows':193,'ledger_columns':15,'research_code_executed':False,'scientific_validation':False}


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2))
