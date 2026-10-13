#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""NEXUS OMEGA: offline, read-only research continuity and freshness auditor.

No external dependencies, models, egress, GitHub/Hostinger writes, or new registry.
Structured output is a derived observation, never a new canonical truth store.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

OPEN_STATES = frozenset({"INTAKE", "ACTIVE", "READY_FOR_CURSOR", "CURSOR_PROCESSING", "REOPENED"})
TERMINAL_STATES = frozenset({"PROCESSED", "SUPERSEDED"})
ISO_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")


def read_json(path: Path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"DUPLICATE_KEY: {path.name}:{key}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def timestamp(text):
    if not isinstance(text, str) or not ISO_UTC.fullmatch(text):
        raise ValueError("INVALID_TIMESTAMP")
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc)


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def severity(state, age, max_age_days):
    if state in OPEN_STATES and age >= max_age_days:
        return "AGING_OPEN_REVIEW"
    return "NO_TIME_ESCALATION"


def audit(root: Path, as_of: datetime, max_age_days: int = 30) -> dict:
    root = root.resolve()
    contract_path = root / "docs/architecture/REPOSITORY_STRUCTURE.json"
    structure = read_json(contract_path)
    lanes = structure.get("active_research_lanes")
    if not isinstance(lanes, dict) or not lanes:
        raise ValueError("STRUCTURE_LANES_MISSING")
    seen_paths, rows, findings = set(), [], []
    for lane_id, meta in sorted(lanes.items()):
        if not isinstance(meta, dict):
            raise ValueError("INVALID_LANE_METADATA")
        path = meta.get("path")
        if not isinstance(path, str) or not path.startswith("research/") or ".." in Path(path).parts or Path(path).is_absolute():
            raise ValueError("INVALID_LANE_PATH")
        if path in seen_paths:
            findings.append({"code": "DUPLICATE_REGISTERED_PATH", "scope": lane_id, "severity": "INTEGRITY"})
        seen_paths.add(path)
        on_disk = root / path
        present = on_disk.is_dir()
        has_readme = (on_disk / "README.md").is_file()
        if not present:
            findings.append({"code": "REGISTERED_LANE_DIRECTORY_MISSING", "scope": lane_id, "severity": "INTEGRITY"})
        elif not has_readme:
            findings.append({"code": "REGISTERED_LANE_README_MISSING", "scope": lane_id, "severity": "INTEGRITY"})
        rows.append({"id": lane_id, "path": path, "registered_state": meta.get("state", "UNSPECIFIED"),
                     "directory_present": present, "readme_present": has_readme,
                     "independent_runtime_validation": "NOT_MEASURED_BY_THIS_TOOL"})
    pipeline = root / "research/pipeline"
    package_rows = []
    for p in sorted(pipeline.glob("packages/*/*/NEXUS_RP_*/manifest.json")):
        doc = read_json(p)
        package_id = doc.get("package_id")
        if not isinstance(package_id, str) or p.parent.name != package_id:
            findings.append({"code": "PACKAGE_ID_PATH_MISMATCH", "scope": p.parent.name, "severity": "INTEGRITY"})
            continue
        try:
            modified = timestamp(doc.get("updated_at_utc", doc.get("created_at_utc")))
        except (TypeError, ValueError):
            findings.append({"code": "PACKAGE_TIMESTAMP_INVALID", "scope": package_id, "severity": "INTEGRITY"})
            continue
        age_days = max(0, (as_of - modified).days)
        state = doc.get("state", "UNKNOWN")
        # Package manifests are contextual; events are considered separately.
        age_code = severity(state, age_days, max_age_days)
        if age_code != "NO_TIME_ESCALATION":
            findings.append({"code": age_code, "scope": package_id, "severity": "REVIEW_ONLY",
                             "age_days": age_days, "declared_state": state,
                             "basis": "PACKAGE_MANIFEST_NOT_EVENT_RECONCILED"})
        package_rows.append({"id": package_id, "declared_state": state, "manifest_date": iso(modified),
                             "age_days": age_days, "needs_review": age_code != "NO_TIME_ESCALATION"})
    idx_path = pipeline / "index/latest.json"
    index_obs = {"state": "NOT_PRESENT", "age_days": None, "last_generated": None, "authority": "DERIVED_ONLY"}
    if idx_path.is_file():
        doc = read_json(idx_path)
        try:
            generated = timestamp(doc["generated_at_utc"])
            days = max(0, (as_of-generated).days)
            index_obs = {"state": "PRESENT", "age_days": days, "last_generated": iso(generated), "authority": "DERIVED_ONLY"}
            if days >= max_age_days:
                findings.append({"code": "DERIVED_INDEX_AGE_EXCEEDS_BUDGET", "scope": "research/pipeline/index/latest.json",
                                 "severity": "REVIEW_ONLY", "age_days": days,
                                 "basis": "STALE_NAVIGATION_POSSIBLE_NOT_PIPELINE_FAILURE"})
        except (KeyError, ValueError):
            findings.append({"code": "DERIVED_INDEX_TIMESTAMP_INVALID", "scope": "research/pipeline/index/latest.json",
                             "severity": "INTEGRITY"})
    # The event store is authoritative for changes, but this audit does not infer
    # scientific completion from its latest timestamp or mutate event-derived indexes.
    event_paths = sorted(pipeline.glob("events/*/*/*/*.json"))
    event_count = 0
    event_errors = []
    for event in event_paths:
        try:
            data = read_json(event)
            if not isinstance(data.get("event_id"), str) or not isinstance(data.get("package_id"), str):
                raise ValueError("EVENT_IDENTITY_MISSING")
            timestamp(data.get("recorded_at_utc"))
            event_count += 1
        except (ValueError, KeyError, OSError, json.JSONDecodeError):
            event_errors.append(event.relative_to(root).as_posix())
    if event_errors:
        findings.append({"code": "INVALID_EVENT_RECORDS", "scope": "research/pipeline/events",
                         "severity": "INTEGRITY", "count": len(event_errors)})
    # The GitHub branch/working directory alone cannot reveal archived private roots.
    # We explicitly surface this rather than pretending to have inventoried Windows.
    return {
        "object": "NEXUS_OMEGA_RESEARCH_CONTINUITY_GUARD_V1",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "observation_type": "READ_ONLY_DERIVED_NON_CANONICAL",
        "observed_at_utc": iso(as_of),
        "registered_lane_count": len(rows),
        "lane_registry_version": structure.get("version", "UNKNOWN"),
        "lanes": rows,
        "observed_packages": package_rows,
        "observed_event_count": event_count,
        "event_error_count": len(event_errors),
        "derived_index": index_obs,
        "findings": findings,
        "findings_by_severity": {code:sum(f["severity"] == code for f in findings) for code in ("INTEGRITY", "REVIEW_ONLY")},
        "runtime_mcp_node_bus": "NOT_ASSESSED",
        "local_windows_archive_roots": "NOT_ACCESSED",
        "website_publication_parity": "NOT_ASSESSED",
        "source_completeness": "GITHUB_CHECKOUT_ONLY",
        "auto_resolution": "NONE_NO_MUTATION",
        "tokenneutral_external_llm_calls_in_audit": 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--as-of", help="UTC ISO8601, deterministic replay")
    ap.add_argument("--max-age-days", type=int, default=30)
    ap.add_argument("--fail-on-integrity", action="store_true")
    args = ap.parse_args(argv)
    if args.max_age_days < 1:
        ap.error("--max-age-days must be >= 1")
    try:
        as_of = timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
        result = audit(args.root, as_of, args.max_age_days)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"state": "HOLD_SOURCE", "reason": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if args.fail_on_integrity and result["findings_by_severity"]["INTEGRITY"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
