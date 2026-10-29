#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only, isolated C1 preflight for the V1..V7 Issue #93 parser chain (V3).

This preflight never imports or executes a checked module, accesses GitHub,
changes files, authenticates a receipt, or claims runtime integration.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

PINNED_MAIN = '959cfe7e13db98735e4b3d7ec26d2d0ce7d5cbe7'
EXPECTED = {
    'alpha_issue93_exact_key_receipt_census_v1_20261029.py': (5622, '4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c'),
    'alpha_issue93_fenced_receipt_guard_v2_20261029.py': (1769, '05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91'),
    'alpha_issue93_html_comment_guard_v3_20261029.py': (2407, 'dd5875d92cd674c1b4f4428afea05aefcac769023f95e360960b627864ce5f96'),
    'alpha_issue93_raw_html_block_guard_v4_20261029.py': (2772, '582bc71f0607664ad299a18058b1403c305fe265b5089ce136c4926bcbdcc21a'),
    'alpha_issue93_quoted_attribute_guard_v5_20261029.py': (3939, 'acd0777f1ba8500ae3e4b0205bee3cc2d5807425dceb85c45319caed8f76a5c7'),
    'alpha_issue93_multiline_raw_guard_v6_20261029.py': (3940, '73311462e79da1bb940e8c23f8b34fb8c17d84941051f5f17883264aca384dfd'),
    'alpha_issue93_strict_raw_close_guard_v7_20261029.py': (4079, '6c680b8cd487e52492c7cca35174947c85a0e79a98081371d29048d5e0d48d33'),
}
MAX_FILE_BYTES = 100_000


class FixityError(ValueError):
    pass


def verify_inventory(root, expected):
    """Verify pinned bytes without executing code; expected is an explicit oracle."""
    # Path.absolute() normalizes spelling without following symlinks.
    # Reject a symlinked root or ancestor before accessing any expected file.
    # This is a best-effort preflight, not a race-free directory capability.
    root = Path(root).absolute()
    if any(part.is_symlink() for part in (root, *root.parents)):
        raise FixityError('SYMLINK_ROOT_REJECTED')
    if not root.is_dir() or not isinstance(expected, dict) or not expected:
        raise FixityError('INVALID_ROOT_OR_MANIFEST')
    if len(expected) > 100:
        raise FixityError('TOO_MANY_FILES')
    total = 0
    for name, spec in sorted(expected.items()):
        if (not isinstance(name, str) or name in ('.', '..')
                or Path(name).name != name or '/' in name or '\\' in name):
            raise FixityError('UNSAFE_NAME')
        if (not isinstance(spec, tuple) or len(spec) != 2
                or type(spec[0]) is not int or not 0 <= spec[0] <= MAX_FILE_BYTES
                or not isinstance(spec[1], str) or len(spec[1]) != 64
                or any(c not in '0123456789abcdef' for c in spec[1])):
            raise FixityError('INVALID_EXPECTATION')
        path = root / name
        if path.is_symlink():
            raise FixityError('SYMLINK_REJECTED:' + name)
        try:
            # O_NONBLOCK prevents indefinite open() waits on POSIX FIFOs.
            # fstat still rejects nonregular files before any read.
            fd = os.open(path, os.O_RDONLY | getattr(os, 'O_BINARY', 0)
                         | getattr(os, 'O_NOFOLLOW', 0)
                         | getattr(os, 'O_NONBLOCK', 0))
        except OSError:
            raise FixityError('SOURCE_NOT_PRESENT:' + name) from None
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise FixityError('NONREGULAR_FILE:' + name)
            with os.fdopen(fd, 'rb') as stream:
                fd = -1
                raw = stream.read(MAX_FILE_BYTES + 1)
        finally:
            if fd >= 0:
                os.close(fd)
        if len(raw) != spec[0]:
            raise FixityError('BYTE_COUNT_MISMATCH:' + name)
        if hashlib.sha256(raw).hexdigest() != spec[1]:
            raise FixityError('SHA256_MISMATCH:' + name)
        total += len(raw)
    return {'status': 'MATCH', 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'scope': 'LOCAL_PINNED_BYTES_ONLY_NOT_AUTHENTICATED',
            'source_files': len(expected), 'source_bytes': total,
            'runtime_integration': False, 'parser_executed': False}


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (0, 2) or (len(args) == 2 and args[0] != '--root'):
        print('FAIL_CLOSED: USAGE', file=sys.stderr)
        return 2
    root = Path(args[1]) if args else Path(__file__).parent
    try:
        result = verify_inventory(root, EXPECTED)
    except (FixityError, OSError, TypeError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2
    result['pinned_main'] = PINNED_MAIN
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
