#!/usr/bin/env python3
"""Deterministic offline renderer for R33 BodyTwin methods capsule (C1).

SOURCE_EXACT capsule bytes -> sorted JSON view + static HTML.
Double-render must yield identical SHA-256.
BODYTWIN_VALIDATED remains NO. No WWW write.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "receipts"
CAPSULE_NAME = "07_BODYTWIN_R33_METHODS_CAPSULE.json"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_capsule(path: Path) -> tuple[dict, bytes, str]:
    raw = path.read_bytes()
    obj = json.loads(raw.decode("utf-8"))
    return obj, raw, sha256_bytes(raw)


def canonical_json(obj: dict) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def render_html(obj: dict, capsule_sha: str) -> bytes:
    methods = obj.get("new_methods") or []
    rows = []
    for m in methods:
        mid = m.get("id", "")
        status = m.get("status", "")
        title = m.get("title", "")
        rows.append(
            f"<tr><td>{mid}</td><td>{status}</td><td>{title}</td></tr>"
        )
    body = "\n".join(rows)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>R33 BodyTwin Methods Offline Candidate C1</title>
<meta name="nexus-claim-ceiling" content="C1_DESCRIPTIVE_ONLY"/>
<meta name="nexus-bodytwin-validated" content="NO"/>
</head>
<body>
<h1>R33 BodyTwin Methods — Offline Candidate</h1>
<p>claim_ceiling=C1_DESCRIPTIVE_ONLY · bodytwin_validated=NO · consent_bind=OPEN</p>
<p>capsule_sha256={capsule_sha}</p>
<p>object={obj.get("object","")}</p>
<table>
<thead><tr><th>id</th><th>status</th><th>title</th></tr></thead>
<tbody>
{body}
</tbody>
</table>
<p>publication_status=OFFLINE_CANDIDATE_NOT_WWW_WITNESSED</p>
</body>
</html>
"""
    return html.encode("utf-8")


def render_once(capsule_path: Path, tag: str) -> dict:
    obj, raw, capsule_sha = load_capsule(capsule_path)
    if obj.get("bodytwin_validated") is not False and obj.get("bodytwin_validated") != "NO":
        # schema uses boolean false
        if obj.get("bodytwin_validated") is not False:
            raise SystemExit("FAIL: bodytwin_validated must be false/NO")
    view = canonical_json(obj)
    html = render_html(obj, capsule_sha)
    view_path = OUT / f"methods_view_{tag}.json"
    html_path = OUT / f"methods_view_{tag}.html"
    view_path.write_bytes(view)
    html_path.write_bytes(html)
    return {
        "tag": tag,
        "capsule_sha256": capsule_sha,
        "view_sha256": sha256_bytes(view),
        "html_sha256": sha256_bytes(html),
        "view_bytes": len(view),
        "html_bytes": len(html),
        "view_path": str(view_path),
        "html_path": str(html_path),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    capsule = DATA / CAPSULE_NAME
    if not capsule.is_file():
        raise SystemExit(f"missing capsule: {capsule}")
    r1 = render_once(capsule, "pass1")
    r2 = render_once(capsule, "pass2")
    match = (
        r1["view_sha256"] == r2["view_sha256"]
        and r1["html_sha256"] == r2["html_sha256"]
        and r1["capsule_sha256"] == r2["capsule_sha256"]
    )
    receipt = {
        "object": "NEXUS_OMEGA_CURSOR_R33_RESIDUAL_C_RENDERER_RECEIPT_20261117_R1",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "bodytwin_validated": False,
        "consent_bind": "OPEN",
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "double_render_match": match,
        "pass1": r1,
        "pass2": r2,
        "verdict": "PASS" if match else "FAIL",
    }
    out = OUT / "renderer_double_pass_receipt.json"
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": receipt["verdict"], "match": match, "view": r1["view_sha256"]}, indent=2))
    return 0 if match else 1


if __name__ == "__main__":
    raise SystemExit(main())
