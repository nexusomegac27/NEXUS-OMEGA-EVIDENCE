#!/usr/bin/env python3
"""POSIX-only, read-only C1 snapshot fixity V3 with bounded resource budget.

Research limits: 128 regular data files, 1 MiB per file, 4 MiB aggregate.
These are test-profile limits, not empirically calibrated production policy.
No external source authentication, scientific validation, or runtime promotion.
"""
import hashlib
import json
import os
import re
import stat
import sys

SUM_LINE = re.compile(r'^([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9._-]{0,199})$')
MAX_FILES = 128
MAX_FILE_BYTES = 1048576
MAX_TOTAL_BYTES = 4194304


def safe_open(parent_fd, name):
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(name, flags, dir_fd=parent_fd)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise ValueError('SNAPSHOT_NONREGULAR_ENTRY')
    return fd


def audit(snapshot):
    if not all(hasattr(os, key) for key in ('O_DIRECTORY', 'O_NOFOLLOW', 'O_NONBLOCK')):
        raise ValueError('POSIX_NOFOLLOW_UNAVAILABLE')
    directory = os.open(snapshot, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISDIR(os.fstat(directory).st_mode):
            raise ValueError('SNAPSHOT_NOT_DIRECTORY')
        try:
            sums_fd = safe_open(directory, 'SHA256SUMS.txt')
        except FileNotFoundError:
            raise ValueError('SUMS_NOT_REGULAR_FILE') from None
        with os.fdopen(sums_fd, 'rb') as stream:
            raw = stream.read(131073)
        if len(raw) > 131072:
            raise ValueError('SUMS_TOO_LARGE')
        text = raw.decode('ascii', errors='strict')
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
            if len(expected) > MAX_FILES:
                raise ValueError('SNAPSHOT_TOO_MANY_FILES')
        if not expected:
            raise ValueError('SUMS_EMPTY')
        observed = set()
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
                    raise ValueError('SNAPSHOT_NONREGULAR_ENTRY')
                if entry.name != 'SHA256SUMS.txt':
                    observed.add(entry.name)
                    if len(observed) > MAX_FILES:
                        raise ValueError('SNAPSHOT_TOO_MANY_FILES')
        if observed != set(expected):
            raise ValueError('SNAPSHOT_INVENTORY_MISMATCH')
        total = 0
        for name, digest in sorted(expected.items()):
            h = hashlib.sha256()
            with os.fdopen(safe_open(directory, name), 'rb') as stream:
                file_size = os.fstat(stream.fileno()).st_size
                if file_size > MAX_FILE_BYTES:
                    raise ValueError('SNAPSHOT_FILE_TOO_LARGE')
                if total + file_size > MAX_TOTAL_BYTES:
                    raise ValueError('SNAPSHOT_TOTAL_TOO_LARGE')
                read_bytes = 0
                while True:
                    read_limit = min(65536, MAX_FILE_BYTES - read_bytes + 1,
                                     MAX_TOTAL_BYTES - total + 1)
                    block = stream.read(read_limit)
                    if not block:
                        break
                    read_bytes += len(block)
                    total += len(block)
                    if read_bytes > MAX_FILE_BYTES:
                        raise ValueError('SNAPSHOT_FILE_TOO_LARGE')
                    if total > MAX_TOTAL_BYTES:
                        raise ValueError('SNAPSHOT_TOTAL_TOO_LARGE')
                    h.update(block)
            if h.hexdigest() != digest:
                raise ValueError('SNAPSHOT_SHA256_MISMATCH:' + name)
        return {'state':'PASS_FIXITY_C1', 'verified_files':len(expected),
                'verified_bytes':total, 'evidence_class':'LOCAL_SNAPSHOT_ONLY',
                'external_source_binding':'NOT_ESTABLISHED_BY_THIS_TOOL',
                'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}
    finally:
        os.close(directory)


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
