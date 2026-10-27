#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 Unicode-normalization collision witness for Git-tree paths.

Not a production Steward change, filesystem identity oracle, or path migration.
NFC + casefold is a conservative portability review key, not proof of a collision
on every filesystem. It deliberately does not apply NFKC compatibility folding.
"""
import json
import sys
import unicodedata


def witness(payload):
    paths = payload.get("paths") if isinstance(payload, dict) else None
    if not isinstance(paths, list) or any(
        not isinstance(p, str) or not p or p.startswith("/") or "\\" in p
        or any(x in ("", ".", "..") for x in p.split("/"))
        or any(ord(c) < 32 for c in p)
        for p in paths
    ):
        return {"state": "HOLD_INVALID_INPUT", "collision_pairs": []}
    seen = {}
    collisions = set()
    for path in paths:
        key = unicodedata.normalize("NFC", path).casefold()
        # normalize again after casefold, which can expand Unicode scalars
        key = unicodedata.normalize("NFC", key)
        for previous in seen.get(key, set()):
            if previous != path:
                collisions.add(tuple(sorted((previous, path))))
        seen.setdefault(key, set()).add(path)
    pairs = [list(p) for p in sorted(collisions)]
    return {"state": "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION" if pairs else "PASS",
            "collision_pairs": pairs}


def main():
    try:
        payload = json.load(sys.stdin)
        result = witness(payload)
    except (ValueError, UnicodeError):
        result = {"state": "HOLD_INVALID_INPUT", "collision_pairs": []}
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))


if __name__ == "__main__":
    main()
