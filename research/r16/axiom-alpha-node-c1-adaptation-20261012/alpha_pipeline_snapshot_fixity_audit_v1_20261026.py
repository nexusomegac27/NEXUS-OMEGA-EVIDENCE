#!/usr/bin/env python3
"""Read-only C1 research adapter: verify one flat, sealed pipeline snapshot.

Does not modify the existing archive continuity guard, indexes, workflows,
repository, runtime, or any claimed scientific result. The snapshot path and
its SHA256SUMS.txt must be independently bound to an immutable Git commit for
an externally auditable result; local PASS alone is not provenance.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SUM_LINE = re.compile(r'^([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9._-]{0,199})$')


def audit(snapshot):
    root = Path(snapshot)
    if not root.is_dir() or root.is_symlink():
        raise ValueError('SNAPSHOT_NOT_DIRECTORY')
    sums = root / 'SHA256SUMS.txt'
    if not sums.is_file() or sums.is_symlink():
        raise ValueError('SUMS_NOT_REGULAR_FILE')
    if sums.stat().st_size > 131072:
        raise ValueError('SUMS_TOO_LARGE')
    text = sums.read_bytes().decode('ascii', errors='strict')
    if not text.endswith('\n') or '\r' in text:
        raise ValueError('SUMS_NONCANONICAL_LINES')
    expected = {}
    lower_names = set()
    for line in text.splitlines():
        match = SUM_LINE.fullmatch(line)
        if not match:
            raise ValueError('SUMS_MALFORMED_ENTRY')
        digest, name = match.groups()
        if name in ('.', '..', 'SHA256SUMS.txt') or name.startswith('.'):
            raise ValueError('SUMS_UNSAFE_NAME')
        if name in expected or name.casefold() in lower_names:
            raise ValueError('SUMS_DUPLICATE_NAME')
        expected[name] = digest
        lower_names.add(name.casefold())
    if not expected:
        raise ValueError('SUMS_EMPTY')
    observed = set()
    for item in root.iterdir():
        if item.is_symlink() or not item.is_file():
            raise ValueError('SNAPSHOT_NONREGULAR_ENTRY')
        if item.name != 'SHA256SUMS.txt':
            observed.add(item.name)
    if observed != set(expected):
        raise ValueError('SNAPSHOT_INVENTORY_MISMATCH')
    total = 0
    for name, digest in sorted(expected.items()):
        h = hashlib.sha256()
        with (root / name).open('rb') as stream:
            for block in iter(lambda: stream.read(65536), b''):
                total += len(block)
                h.update(block)
        if h.hexdigest() != digest:
            raise ValueError('SNAPSHOT_SHA256_MISMATCH:' + name)
    return {'state':'PASS_FIXITY_C1', 'verified_files':len(expected),
            'verified_bytes':total, 'evidence_class':'LOCAL_SNAPSHOT_ONLY',
            'external_source_binding':'NOT_ESTABLISHED_BY_THIS_TOOL',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print('FAIL_CLOSED: EXPECTED_SINGLE_SNAPSHOT_PATH', file=sys.stderr)
        return 2
    try:
        print(json.dumps(audit(argv[0]), sort_keys=True))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
