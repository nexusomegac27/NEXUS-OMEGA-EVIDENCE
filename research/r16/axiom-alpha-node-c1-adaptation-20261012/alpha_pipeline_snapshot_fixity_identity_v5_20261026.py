#!/usr/bin/env python3
"""POSIX-only C1 snapshot fixity V5: V4 plus post-hash identity continuity.

Detect deterministic same-name inode replacement, in-place metadata drift and
manifest mutation after read. Not an atomic snapshot, cryptographic signature,
or guarantee against adversarial changes after the final stat. V4 is immutable.
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


def fingerprint(st):
    """Exclude atime: reads themselves may update it."""
    return (st.st_mode, st.st_dev, st.st_ino, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns)


def check_identity(directory, name, original, error):
    try:
        now = os.stat(name, dir_fd=directory, follow_symlinks=False)
    except OSError as exc:
        raise ValueError(error + ':' + name) from exc
    if not stat.S_ISREG(now.st_mode) or fingerprint(now) != original:
        raise ValueError(error + ':' + name)


def safe_open(parent_fd, name):
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(name, flags, dir_fd=parent_fd)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise ValueError('SNAPSHOT_NONREGULAR_ENTRY')
    return fd


def inventory(directory):
    """Enumerate a pinned directory descriptor; reject nonregular entries."""
    observed = set()
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
                raise ValueError('SNAPSHOT_NONREGULAR_ENTRY')
            if entry.name != 'SHA256SUMS.txt':
                observed.add(entry.name)
                if len(observed) > MAX_FILES:
                    raise ValueError('SNAPSHOT_TOO_MANY_FILES')
    return observed


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
            manifest_identity = fingerprint(os.fstat(stream.fileno()))
            raw = stream.read(131073)
            if fingerprint(os.fstat(stream.fileno())) != manifest_identity:
                raise ValueError('SNAPSHOT_MANIFEST_IDENTITY_CHANGED_DURING_READ')
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
        if inventory(directory) != set(expected):
            raise ValueError('SNAPSHOT_INVENTORY_MISMATCH')
        total = 0
        hashed_identities = {}
        for name, digest in sorted(expected.items()):
            h = hashlib.sha256()
            with os.fdopen(safe_open(directory, name), 'rb') as stream:
                original_identity = fingerprint(os.fstat(stream.fileno()))
                file_size = original_identity[3]
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
                if fingerprint(os.fstat(stream.fileno())) != original_identity:
                    raise ValueError('SNAPSHOT_FILE_IDENTITY_CHANGED_DURING_HASH:' + name)
            hashed_identities[name] = original_identity
            if h.hexdigest() != digest:
                raise ValueError('SNAPSHOT_SHA256_MISMATCH:' + name)
        # Detect a deterministic post-inventory addition/deletion after hashing.
        # This does not claim an atomic view under continuous concurrent writes.
        if inventory(directory) != set(expected):
            raise ValueError('SNAPSHOT_INVENTORY_CHANGED_AFTER_HASH')
        for name, original in sorted(hashed_identities.items()):
            check_identity(directory, name, original,
                           'SNAPSHOT_FILE_IDENTITY_CHANGED_AFTER_HASH')
        check_identity(directory, 'SHA256SUMS.txt', manifest_identity,
                       'SNAPSHOT_MANIFEST_IDENTITY_CHANGED_AFTER_READ')
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
