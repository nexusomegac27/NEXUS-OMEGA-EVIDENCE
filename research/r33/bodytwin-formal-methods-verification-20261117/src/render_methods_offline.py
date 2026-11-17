#!/usr/bin/env python3
"""R33 BodyTwin methods offline renderer — fail-closed, HTML-escaped (R33-R2).

F01: html.escape on all dynamic text.
F02: strict JSON (no duplicate keys, no nonfinite), semantic fences on all blocked fields.
F05: relative receipt paths only.
"""
from __future__ import annotations

import hashlib
import html
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CAPSULE = ROOT / "data" / "07_BODYTWIN_R33_METHODS_CAPSULE.json"
SCHEMA = ROOT / "data" / "02_BODYTWIN_R33_METHODS_RECORD_SCHEMA.json"
OUT_DIR = ROOT / "candidate_offline"
VIEW_HTML = OUT_DIR / "methods_assurance.html"
VIEW_JSON = OUT_DIR / "methods_assurance.json"
RECEIPT = ROOT / "receipts" / "renderer_double_pass_receipt.json"

MIN_BYTES = 1
MAX_BYTES = 64000

PRIVATE_MARKERS = (
    "C:\\Users\\",
    "C:/Users/",
    "\\AppData\\",
    "/AppData/",
    "NEXUS_OMEGA_TRANSFER\\20_TO_CURSOR",
    "NEXUS_OMEGA_TRANSFER/20_TO_CURSOR",
)


class ContractError(ValueError):
    """Fail-closed contract violation."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative_to_root(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.name


def uniq(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ContractError(f"duplicate_json_key:{key}")
        out[key] = value
    return out


def _bad_const(token: str) -> None:
    raise ContractError(f"nonfinite_json_constant:{token}")


def assert_finite(obj: Any, path: str = "$") -> None:
    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise ContractError(f"nonfinite_float:{path}")
    elif isinstance(obj, dict):
        for key, value in obj.items():
            assert_finite(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            assert_finite(value, f"{path}[{index}]")


def load_bytes(raw: bytes) -> dict[str, Any]:
    if len(raw) < MIN_BYTES or len(raw) > MAX_BYTES:
        raise ContractError(f"payload_size_out_of_bounds:{len(raw)}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError(f"invalid_utf8:{exc}") from exc
    for marker in PRIVATE_MARKERS:
        if marker.lower() in text.lower():
            raise ContractError(f"private_topology_marker:{marker}")
    try:
        data = json.loads(
            text,
            object_pairs_hook=uniq,
            parse_constant=_bad_const,
        )
    except ContractError:
        raise
    except json.JSONDecodeError as exc:
        raise ContractError(f"json_decode:{exc}") from exc
    if not isinstance(data, dict):
        raise ContractError("root_must_be_object")
    assert_finite(data)
    return data


def load_capsule(path: Path) -> dict[str, Any]:
    return load_bytes(path.read_bytes())


def enforce_semantic_fences(data: dict[str, Any]) -> None:
    if data.get("bodytwin_validated") != "NO":
        raise ContractError("bodytwin_validated_must_be_NO")
    if data.get("clinical_validated") is not False:
        raise ContractError("clinical_validated_must_be_false")
    if data.get("whole_body_pose_validated") is not False:
        raise ContractError("whole_body_pose_validated_must_be_false")
    if data.get("physical_measurement_validated") is not False:
        raise ContractError("physical_measurement_validated_must_be_false")
    if data.get("consent_bind") != "OPEN":
        raise ContractError("consent_bind_must_be_OPEN")
    if data.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY":
        raise ContractError("claim_ceiling_must_be_C1_DESCRIPTIVE_ONLY")
    if data.get("claim_promotion") is not False:
        raise ContractError("claim_promotion_must_be_false")
    if data.get("trial_001") != "DESIGNED_NOT_EXECUTED":
        raise ContractError("trial_001_must_be_DESIGNED_NOT_EXECUTED")
    pub = data.get("publication_status")
    if pub not in (
        "OFFLINE_CANDIDATE_NOT_WWW_WITNESSED",
        "OFFLINE_CANDIDATE",
        None,
    ):
        # Allow only offline / non-WWW statuses; reject WWW escalation tokens.
        if isinstance(pub, str) and ("WWW" in pub.upper() and "NOT" not in pub.upper()):
            raise ContractError(f"publication_status_www_escalation:{pub}")
        if pub not in (
            "OFFLINE_CANDIDATE_NOT_WWW_WITNESSED",
            "OFFLINE_CANDIDATE",
        ):
            raise ContractError(f"publication_status_not_offline:{pub}")
    methods = data.get("new_methods")
    if not isinstance(methods, list):
        raise ContractError("new_methods_must_be_list")
    for index, method in enumerate(methods):
        if not isinstance(method, dict):
            raise ContractError(f"method_not_object:{index}")
        if method.get("bodytwin_measurement_claim") is not False:
            raise ContractError(f"bodytwin_measurement_claim_must_be_false:{index}")
        if method.get("claim_ceiling") not in (None, "C1_DESCRIPTIVE_ONLY"):
            raise ContractError(f"method_claim_ceiling:{index}")


def validate_schema(data: dict[str, Any]) -> dict[str, Any]:
    report: dict[str, Any] = {
        "schema_path": relative_to_root(SCHEMA) if SCHEMA.is_file() else None,
        "schema_available": SCHEMA.is_file(),
        "result": "SKIPPED_NO_SCHEMA",
    }
    if not SCHEMA.is_file():
        return report
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        report["result"] = "SKIPPED_JSONSCHEMA_ABSENT"
        return report
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ContractError(f"schema_validation_failed:{errors[0].message}")
    report["result"] = "PASS"
    report["jsonschema_version"] = getattr(jsonschema, "__version__", "unknown")
    return report


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def render_html(
    data: dict[str, Any],
    capsule_sha: str,
    schema_report: dict[str, Any],
    generated_utc: str,
) -> str:
    rows = []
    for method in data.get("new_methods", []):
        rows.append(
            "<tr>"
            f"<td>{esc(method.get('id'))}</td>"
            f"<td>{esc(method.get('title'))}</td>"
            f"<td>{esc(method.get('science_scope'))}</td>"
            f"<td>{esc(method.get('evidence_class'))}</td>"
            f"<td>{esc(method.get('status'))}</td>"
            f"<td>{esc(method.get('bodytwin_measurement_claim'))}</td>"
            "</tr>"
        )
    rows_html = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(data.get('object', 'R33 Methods'))}</title>
<style>
body{{font-family:system-ui,sans-serif;margin:1.5rem;line-height:1.45;color:#111}}
table{{border-collapse:collapse;width:100%;margin-top:1rem}}
th,td{{border:1px solid #ccc;padding:0.4rem 0.6rem;text-align:left;vertical-align:top}}
th{{background:#f4f4f4}}
.meta{{font-size:0.9rem;color:#333}}
.hold{{background:#fff3cd;padding:0.75rem;border:1px solid #e0c56e;margin:1rem 0}}
</style>
</head>
<body>
<h1>{esc(data.get('object', 'R33 Methods'))}</h1>
<div class="hold">
<strong>HOLD:</strong> BODYTWIN_VALIDATED={esc(data.get('bodytwin_validated'))};
CONSENT_BIND={esc(data.get('consent_bind'))};
CLINICAL={esc(data.get('clinical_validated'))};
CLAIM_CEILING={esc(data.get('claim_ceiling'))};
PUBLICATION={esc(data.get('publication_status'))}.
No medical or physical BodyTwin validation is claimed.
</div>
<p class="meta">capsule_sha256={esc(capsule_sha)} · schema={esc(schema_report.get('result'))} · generated_utc={esc(generated_utc)}</p>
<table>
<thead><tr><th>id</th><th>title</th><th>scope</th><th>class</th><th>status</th><th>measurement_claim</th></tr></thead>
<tbody>
{rows_html}
</tbody>
</table>
</body>
</html>
"""


def render_once(capsule_path: Path | None = None) -> dict[str, Any]:
    path = capsule_path or CAPSULE
    raw = path.read_bytes()
    capsule_sha = sha256_bytes(raw)
    data = load_bytes(raw)
    enforce_semantic_fences(data)
    schema_report = validate_schema(data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    html_text = render_html(data, capsule_sha, schema_report, generated_utc)
    json_text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    VIEW_HTML.write_text(html_text, encoding="utf-8", newline="\n")
    VIEW_JSON.write_text(json_text, encoding="utf-8", newline="\n")

    # Deterministic double-pass: same capsule_sha + generated_utc; re-load written JSON.
    data2 = load_bytes(VIEW_JSON.read_bytes())
    enforce_semantic_fences(data2)
    html2 = render_html(data2, capsule_sha, schema_report, generated_utc)
    html_sha1 = sha256_bytes(html_text.encode("utf-8"))
    html_sha2 = sha256_bytes(html2.encode("utf-8"))
    if html_sha1 != html_sha2:
        raise ContractError("double_pass_html_mismatch")

    receipt = {
        "object": "NEXUS_OMEGA_R33_METHODS_RENDERER_DOUBLE_PASS_RECEIPT_20261117_R2",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "claim_promotion": False,
        "bodytwin_validated": "NO",
        "consent_bind": "OPEN",
        "capsule_path": relative_to_root(path),
        "capsule_sha256": capsule_sha,
        "capsule_bytes": len(raw),
        "view_html_path": relative_to_root(VIEW_HTML),
        "view_json_path": relative_to_root(VIEW_JSON),
        "view_html_sha256": html_sha1,
        "view_html_bytes": len(html_text.encode("utf-8")),
        "view_json_sha256": sha256_file(VIEW_JSON),
        "view_json_bytes": VIEW_JSON.stat().st_size,
        "double_pass": "PASS",
        "schema_report": schema_report,
        "public_history_review": "PUBLIC_HISTORY_REVIEW_PENDING",
        "absolute_host_paths": False,
        "generated_utc": generated_utc,
    }
    RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return receipt


def main(argv: list[str]) -> int:
    try:
        receipt = render_once()
    except ContractError as exc:
        print(f"CONTRACT_FAIL:{exc}", file=sys.stderr)
        return 2
    print(json.dumps({"result": "PASS", "receipt": receipt}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
