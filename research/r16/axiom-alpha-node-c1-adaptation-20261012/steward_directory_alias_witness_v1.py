#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 witness for portable directory-prefix alias collisions.

This is not integrated into the production repository steward. The result
is a conservative portability warning, not proof of actual OS aliasing.
"""
from __future__ import annotations
import unicodedata


def _portable_key(component: str) -> str:
    return unicodedata.normalize("NFC", unicodedata.normalize("NFC", component).casefold())


def directory_alias_collisions(paths: list[str]) -> list[tuple[str, str]]:
    """Detect distinct Git directory prefixes with the same NFC/casefold key."""
    seen: dict[tuple[str, ...], tuple[str, ...]] = {}
    collisions: set[tuple[str, str]] = set()
    for path in sorted(paths):
        if not isinstance(path, str) or not path or path.startswith("/"):
            raise ValueError("INVALID_RELATIVE_GIT_PATH")
        parts = path.split("/")
        if any(not p or p in (".", "..") for p in parts):
            raise ValueError("INVALID_RELATIVE_GIT_PATH")
        for depth in range(1, len(parts)):
            prefix = tuple(parts[:depth])
            key = tuple(_portable_key(part) for part in prefix)
            prior = seen.setdefault(key, prefix)
            if prior != prefix:
                collisions.add(("/".join(prior), "/".join(prefix)))
    return sorted(collisions)
