#!/usr/bin/env python3
"""C1 research-only V4: fail closed on altered V1/V2/V3 dependency bytes.

This append-only wrapper pins the three historical PR preflight sources and
executes ONLY the verified in-memory bytes, in dependency order. It does not
authenticate a GitHub API snapshot, prove its path-absence assertion, grant
publication authority, modify CI, or merge. It is not a defense against a
compromised Python interpreter, stdlib, or concurrent privileged attacker.
"""
import hashlib
from pathlib import Path
import sys
import types

PINNED = (
    ('alpha_pr_publication_preflight_guard_v1_20261023',
     '920fc924070f92d835429613a85e1ffbd15061ba78f2a31d2749cf68ca5549c0'),
    ('alpha_pr_publication_preflight_guard_v2_20261023',
     '192664502c89ce1a9a2776a66e4ee472c735915345647f653710239c8226b6f0'),
    ('alpha_pr_publication_preflight_guard_v3_20261023',
     '41993a0f087f36c9e8c8dbcc9195b1e75da2228b5a25594c87fe34d94295ef8e'),
)


def check_pr_publication_preflight(snapshot, now_utc):
    """Preserve V3's result only when all three exact dependency bytes match."""
    root = Path(__file__).resolve().parent
    sources = []
    try:
        for name, expected in PINNED:
            path = root / (name + '.py')
            if path.is_symlink() or not path.is_file():
                return {'status': 'INCOMPLETE'}
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != expected:
                return {'status': 'INCOMPLETE'}
            sources.append((name, path, raw))
    except (OSError, ValueError):
        return {'status': 'INCOMPLETE'}

    old = {name: sys.modules.get(name) for name, _, _ in sources}
    try:
        for name, path, raw in sources:
            module = types.ModuleType(name)
            module.__file__ = str(path)
            sys.modules[name] = module
            exec(compile(raw, str(path), 'exec'), module.__dict__)
        fn = sys.modules[sources[-1][0]].check_pr_publication_preflight
        result = fn(snapshot, now_utc)
        return result if isinstance(result, dict) and isinstance(result.get('status'), str) else {'status': 'INCOMPLETE'}
    except (Exception,):
        return {'status': 'INCOMPLETE'}
    finally:
        for name, previous in old.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous
