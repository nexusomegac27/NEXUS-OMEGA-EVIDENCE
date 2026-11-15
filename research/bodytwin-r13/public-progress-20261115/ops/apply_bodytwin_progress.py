#!/usr/bin/env python3
"""NEXUS BodyTwin C1 progress publisher: bounded preview/apply; no network or sensors.

Designed for Cursor on an explicitly authorized Hostinger-mounted webroot.
--apply requires an exact operator release acknowledgement; default is NO WRITE.
Updates /bodytwin/index.html by two isolated textual insertions.
Original HTML is backed up byte-for-byte before the atomic HTML swap.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

RELEASE = "BODYTWIN_PUBLIC_C1_RELEASE_20261115"
OPEN = "<!-- NEXUS_BODYTWIN_C1_PROGRESS_20261115_START"
CLOSE = "<!-- NEXUS_BODYTWIN_C1_PROGRESS_20261115_END -->"
STYLE = '<link rel="stylesheet" href="/bodytwin/updates/progress.css">'
FILES = {"progress.css": "progress.css", "index.html": "updates/index.html", "events.json": "updates/events.json"}

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def utf8(raw: bytes) -> str:
    return raw.decode("utf-8", "strict")

def plan(old: bytes, fragment: bytes) -> tuple[bytes, str]:
    current, piece = utf8(old), utf8(fragment)
    has_start = OPEN in current
    has_end = CLOSE in current
    if has_start or has_end:
        if has_start and has_end and STYLE in current and current.count(OPEN) == 1 and current.count(CLOSE) == 1:
            return old, "ALREADY_PRESENT"
        raise ValueError("PARTIAL_OR_DUPLICATE_UPDATE")
    if STYLE in current:
        raise ValueError("STYLESHEET_COLLISION_WITHOUT_MARKERS")
    lo = current.lower()
    if lo.count("</head>") != 1 or lo.count("</main>") != 1:
        raise ValueError("NO_UNIQUE_HEAD_MAIN_INSERTION_ANCHORS")
    if not piece.startswith(OPEN) or not piece.rstrip().endswith(CLOSE):
        raise ValueError("UNBOUND_FRAGMENT_MARKERS")
    h = lo.index("</head>")
    with_style = current[:h] + STYLE + "\n" + current[h:]
    m = with_style.lower().index("</main>") + len("</main>")
    new = with_style[:m] + "\n" + piece + "\n" + with_style[m:]
    clean = new.replace(STYLE + "\n", "", 1).replace("\n" + piece + "\n", "", 1)
    if clean.encode("utf-8") != old:
        raise ValueError("NONREVERSIBLE_OR_UNINTENDED_HTML_CHANGE")
    return new.encode("utf-8"), "READY"

def run(web_root: Path, site_source: Path, apply: bool, acknowledgement: str, backup_root: Path | None) -> dict:
    web_root = web_root.resolve(strict=True)
    site_source = site_source.resolve(strict=True)
    html = web_root / "bodytwin" / "index.html"
    fragment = site_source / "progress-fragment.html"
    css = site_source / "progress.css"
    standalone = site_source / "updates" / "index.html"
    ledger = site_source / "updates" / "events.json"
    for path in (html, fragment, css, standalone, ledger):
        if not path.is_file() or path.is_symlink():
            raise ValueError("REQUIRED_SOURCE_MISSING_OR_SYMLINK:" + path.name)
    original = html.read_bytes()
    update, state = plan(original, fragment.read_bytes())
    j = json.loads(utf8(ledger.read_bytes()))
    if j.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY" or j.get("bodytwin", {}).get("validated") != "NO":
        raise ValueError("LEDGER_C1_CEILING_OR_VALIDATION_VIOLATION")
    if j.get("published_live") is not False:
        raise ValueError("LEDGER_MUST_REMAIN_PREDEPLOY_CANDIDATE")
    assets = {"progress.css": css.read_bytes(), "index.html": standalone.read_bytes(), "events.json": ledger.read_bytes()}
    new_dir = web_root / "bodytwin" / "updates"
    for name, raw in assets.items():
        target = new_dir / name
        if target.exists() and (target.is_symlink() or target.read_bytes() != raw):
            raise ValueError("EXISTING_ASSET_COLLISION:" + name)
    receipt = {
        "object": "NEXUS_BODYTWIN_C1_PROGRESS_SCOPED_RELEASE_20261115_R0",
        "mode": "DRY_RUN" if not apply else "LOCAL_FILES_WRITTEN_HOST_HTTP_NOT_VERIFIED",
        "state": state, "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "original_html_bytes": len(original), "original_html_sha256": digest(original),
        "candidate_html_bytes": len(update), "candidate_html_sha256": digest(update),
        "assets_sha256": {name: digest(raw) for name, raw in assets.items()},
        "existing_viewer_mutation": "TWO_ADDITIVE_INSERTIONS_ONLY",
        "live_verification": "NOT_PERFORMED_IN_THIS_SCRIPT",
        "bodytwin_validated": "NO", "oppo_capture": False, "hostinger_http_observed": False,
    }
    if not apply:
        return receipt
    if acknowledgement != RELEASE:
        raise ValueError("EXPLICIT_OPERATOR_PUBLICATION_ACK_REQUIRED")
    if backup_root is None:
        raise ValueError("EXPLICIT_NONPUBLIC_BACKUP_DIRECTORY_REQUIRED")
    backup_root = backup_root.resolve(strict=True)
    if web_root == backup_root or web_root in backup_root.parents or backup_root in web_root.parents:
        raise ValueError("BACKUP_LOCATION_NOT_ISOLATED_FROM_PUBLIC_WEBROOT")
    backup_path = backup_root / ("bodytwin-index-before-progress-20261115-" + digest(original)[:12] + ".html")
    if backup_path.exists() and backup_path.read_bytes() != original:
        raise ValueError("BACKUP_COLLISION")
    if not backup_path.exists():
        with backup_path.open("xb") as fh:
            fh.write(original); fh.flush(); os.fsync(fh.fileno())
    new_dir.mkdir(exist_ok=True)
    if html.read_bytes() != original:
        raise ValueError("WEBROOT_HTML_CHANGED_DURING_STAGING")
    for name, raw in assets.items():
        target = new_dir / name
        if target.exists():
            continue
        tmp = target.with_name("." + name + ".stage")
        try:
            with tmp.open("xb") as fh:
                fh.write(raw); fh.flush(); os.fsync(fh.fileno())
            os.replace(tmp, target)
        finally:
            if tmp.exists(): tmp.unlink()
    if update != original:
        temp = html.with_name(".index.html.bodytwin-progress-stage")
        try:
            with temp.open("xb") as fh:
                fh.write(update); fh.flush(); os.fsync(fh.fileno())
            os.replace(temp, html)
        finally:
            if temp.exists(): temp.unlink()
    receipt["backup_sha256"] = digest(backup_path.read_bytes())
    receipt["asset_files_deployed"] = 3
    receipt["html_on_disk_matches"] = html.read_bytes() == update
    receipt["rollback_rule"] = "Restore EXACT backup HTML and remove only 3 matching versioned new assets"
    return receipt

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--web-root", required=True)
    ap.add_argument("--site-source", required=True)
    ap.add_argument("--apply", action="store_true", help="Writes only after explicit operator ACK")
    ap.add_argument("--operator-ack", default="")
    ap.add_argument("--backup-dir")
    args = ap.parse_args()
    try:
        result = run(Path(args.web_root), Path(args.site_source), args.apply, args.operator_ack, Path(args.backup_dir) if args.backup_dir else None)
        print(json.dumps(result, indent=2, sort_keys=True))
    except Exception as e:
        print(json.dumps({"state":"FAIL_CLOSED","error":str(e),"claim_ceiling":"C1_DESCRIPTIVE_ONLY"}))
        sys.exit(2)
