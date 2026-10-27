#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 witness for Windows reserved device-name path components.

Not integrated into scripts/nexus_repository_steward.py. No filesystem I/O.
Microsoft's Win32 naming reference explicitly reserves COM¹..COM³ and LPT¹..LPT³.
"""
from __future__ import annotations
import re

DEVICE = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?$", re.I)


def reserved_device_component(component: str) -> bool:
    if not isinstance(component, str):
        raise TypeError("component must be str")
    return bool(DEVICE.fullmatch(component))


def flagged_components(relative_path: str) -> list[str]:
    if not isinstance(relative_path, str):
        raise TypeError("relative_path must be str")
    parts = relative_path.split("/")
    if not relative_path or any(p in ("", ".", "..") for p in parts):
        raise ValueError("invalid relative Git path")
    return [p for p in parts if reserved_device_component(p)]
