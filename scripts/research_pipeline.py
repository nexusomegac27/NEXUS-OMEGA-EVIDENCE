#!/usr/bin/env python3
"""NEXUS OMEGA shared AXIOM/Cursor research-pipeline tool.

Stdlib-only. Package/event metadata are orchestration/provenance records; they do
not promote scientific claims or integration authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

STATES = {
    "INTAKE", "ACTIVE", "READY_FOR_CURSOR", "CURSOR_PROCESSING",
    "PROCESSED", "BLOCKED", "SUPERSEDED", "REOPENED",
}
PACKAGE_RE = re.compile(r"^NEXUS_RP_\d{8}T\d{6}Z_[a-z0-9][a-z0-9_-]{0,63}_[0-9a-f]{8}$")


def now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-_")
    return (value or "research")[:64]


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pipeline_root(repo: Path) -> Path:
    return repo.resolve() / "research" / "pipeline"


def package_dirs(repo: Path):
    base = pipeline_root(repo) / "packages"
    if not base.exists():
        return []
    return sorted(p for p in base.glob("*/*/NEXUS_RP_*") if p.is_dir())


def find_package(repo: Path, package_id: str) -> Path:
    matches = [p for p in package_dirs(repo) if p.name == package_id]
    if len(matches) != 1:
        raise SystemExit(f"package {package_id!r}: expected exactly one match, found {len(matches)}")
    return matches[0]


def write_event(repo: Path, package_id: str, event_type: str, actor: str,
                prior_state, new_state, activity: str, subject_refs=None,
                evidence_refs=None, notes=None) -> Path:
    dt = now()
    event_id = f"NEXUS_RPE_{stamp(dt)}_{secrets.token_hex(4)}"
    rel = Path("events") / dt.strftime("%Y/%m/%d") / f"{stamp(dt)}_{event_id}.json"
    event = {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "package_id": package_id,
        "event_type": event_type,
        "recorded_at_utc": iso(dt),
        "actor": actor,
        "prior_state": prior_state,
        "new_state": new_state,
        "activity": activity,
        "subject_refs": subject_refs or [],
        "evidence_refs": evidence_refs or [],
        "claim_ceiling": "C1",
        "notes": notes or [],
    }
    path = pipeline_root(repo) / rel
    dump_json(path, event)
    return path


def events_for(repo: Path, package_id: str):
    base = pipeline_root(repo) / "events"
    out = []
    if base.exists():
        for path in sorted(base.glob("*/*/*/*.json")):
            try:
                event = load_json(path)
            except Exception:
                continue
            if event.get("package_id") == package_id:
                out.append(event)
    return sorted(out, key=lambda e: (e.get("recorded_at_utc", ""), e.get("event_id", "")))


def build_index(repo: Path) -> None:
    records = []
    for pkg in package_dirs(repo):
        manifest = load_json(pkg / "manifest.json")
        records.append({
            "package_id": manifest["package_id"],
            "phase": manifest["phase"],
            "strand": manifest["strand"],
            "title": manifest["title"],
            "state": manifest["state"],
            "created_at_utc": manifest["created_at_utc"],
            "updated_at_utc": manifest["updated_at_utc"],
            "latest_snapshot": manifest["latest_snapshot"],
            "path": pkg.relative_to(repo).as_posix(),
        })
    records.sort(key=lambda r: (r["created_at_utc"], r["package_id"]))
    generated = iso(now())
    dump_json(pipeline_root(repo) / "index" / "packages.json", {
        "object": "NEXUS_OMEGA_RESEARCH_PIPELINE_PACKAGE_CATALOG_V1",
        "generated_from": "EVENT_STORE_AND_PACKAGE_MANIFESTS",
        "generated_at_utc": generated,
        "packages": records,
        "note": "Derived catalog; package/event/snapshot objects remain the evidentiary sources.",
    })
    def latest(state):
        xs = [r for r in records if r["state"] == state]
        return xs[-1]["package_id"] if xs else None
    dump_json(pipeline_root(repo) / "index" / "latest.json", {
        "object": "NEXUS_OMEGA_RESEARCH_PIPELINE_LATEST_V1",
        "generated_from": "EVENT_STORE",
        "generated_at_utc": generated,
        "latest_active_package": latest("ACTIVE"),
        "latest_ready_for_cursor": latest("READY_FOR_CURSOR"),
        "latest_processed_package": latest("PROCESSED"),
        "note": "Derived navigation view; authoritative lifecycle history is package/event/snapshot state.",
    })


def cmd_new(ns) -> None:
    repo = ns.root.resolve()
    dt = now()
    slug = slugify(ns.slug or ns.title)
    package_id = f"NEXUS_RP_{stamp(dt)}_{slug}_{secrets.token_hex(4)}"
    pkg = pipeline_root(repo) / "packages" / dt.strftime("%Y/%m") / package_id
    pkg.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema_version": "1.0.0", "package_id": package_id,
        "created_at_utc": iso(dt), "updated_at_utc": iso(dt),
        "phase": ns.phase, "strand": ns.strand, "title": ns.title,
        "objective": ns.objective, "state": "INTAKE",
        "owners": ["AXIOM", "CURSOR_PRAXIS"], "producer": ns.producer,
        "intended_processor": ns.processor, "claim_ceiling": "C1",
        "claim_promotion": False, "integration_authority": "NONE",
        "predecessor_packages": ns.predecessor or [],
        "research_questions": ns.question or [], "item_count": 0,
        "snapshot_count": 0, "latest_snapshot": None,
        "uncertainty": [], "notes": [],
    }
    dump_json(pkg / "manifest.json", manifest)
    dump_json(pkg / "items.json", {"package_id": package_id, "items": []})
    dump_json(pkg / "provenance.json", {
        "package_id": package_id,
        "model": "NEXUS_PROV_INSPIRED_V1",
        "entities": [], "activities": [],
        "agents": [ns.producer, ns.processor],
    })
    dump_json(pkg / "timeline.json", {"package_id": package_id, "events": []})
    write_event(repo, package_id, "PACKAGE_CREATED", ns.producer, None, "INTAKE", "package-create")
    build_index(repo)
    print(package_id)


def cmd_add(ns) -> None:
    repo = ns.root.resolve(); pkg = find_package(repo, ns.package)
    manifest = load_json(pkg / "manifest.json"); items_doc = load_json(pkg / "items.json")
    item = {
        "item_id": f"ITEM_{secrets.token_hex(8)}", "object_role": ns.role,
        "repository": ns.repository, "commit": ns.commit, "path": ns.path_ref,
        "git_blob": ns.git_blob, "bytes": ns.bytes, "sha256": ns.sha256,
        "source_status": ns.source_status, "producer": ns.producer,
        "observed_at_utc": iso(now()), "research_relevance": ns.relevance,
        "uncertainty": ns.uncertainty or [],
    }
    items_doc["items"].append(item); dump_json(pkg / "items.json", items_doc)
    manifest["item_count"] = len(items_doc["items"]); manifest["updated_at_utc"] = iso(now())
    if manifest["state"] == "INTAKE": manifest["state"] = "ACTIVE"
    dump_json(pkg / "manifest.json", manifest)
    write_event(repo, manifest["package_id"], "ITEM_ADDED", ns.producer, None, manifest["state"],
                "research-item-add", [item["item_id"]], [ns.path_ref] if ns.path_ref else [])
    build_index(repo)


def cmd_state(ns) -> None:
    repo = ns.root.resolve(); pkg = find_package(repo, ns.package)
    manifest = load_json(pkg / "manifest.json"); prior = manifest["state"]
    if ns.state not in STATES: raise SystemExit(f"invalid state: {ns.state}")
    manifest["state"] = ns.state; manifest["updated_at_utc"] = iso(now())
    dump_json(pkg / "manifest.json", manifest)
    write_event(repo, manifest["package_id"], "STATE_CHANGED", ns.actor, prior, ns.state,
                ns.activity, notes=ns.note or [])
    build_index(repo)


def cmd_seal(ns) -> None:
    repo = ns.root.resolve(); pkg = find_package(repo, ns.package)
    manifest = load_json(pkg / "manifest.json")
    prior = manifest["state"]; manifest["state"] = "READY_FOR_CURSOR"
    manifest["updated_at_utc"] = iso(now())
    version = manifest.get("snapshot_count", 0) + 1
    snapshot_name = f"v{version}"; snapshot = pkg / "snapshots" / snapshot_name
    snapshot.mkdir(parents=True, exist_ok=False)
    manifest["snapshot_count"] = version; manifest["latest_snapshot"] = snapshot_name
    dump_json(pkg / "manifest.json", manifest)
    write_event(repo, manifest["package_id"], "STATE_CHANGED", ns.actor, prior,
                "READY_FOR_CURSOR", "seal-for-cursor")
    timeline = {"package_id": manifest["package_id"], "events": events_for(repo, manifest["package_id"])}
    dump_json(pkg / "timeline.json", timeline)
    for name in ("manifest.json", "items.json", "provenance.json", "timeline.json"):
        shutil.copy2(pkg / name, snapshot / name)
    (snapshot / "CURSOR_HANDOFF.md").write_text(
        f"# Cursor handoff\n\nPACKAGE_ID = `{manifest['package_id']}`\n\nSNAPSHOT = `{snapshot_name}`\n\n"
        f"STATE = `READY_FOR_CURSOR`\n\nCLAIM_CEILING = `C1`\n\n"
        "Cursor must bind this exact snapshot before processing and return the package ID + snapshot version.\n",
        encoding="utf-8")
    files = sorted(p for p in snapshot.iterdir() if p.is_file() and p.name != "SHA256SUMS.txt")
    lines = [f"{sha256_file(p)}  {p.name}" for p in files]
    (snapshot / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_event(repo, manifest["package_id"], "SNAPSHOT_SEALED", ns.actor,
                "READY_FOR_CURSOR", "READY_FOR_CURSOR", "snapshot-seal",
                [f"{manifest['package_id']}:{snapshot_name}"],
                [snapshot.relative_to(repo).as_posix()])
    build_index(repo)
    print(snapshot.relative_to(repo).as_posix())


def validate(repo: Path) -> list[str]:
    errors = []
    for pkg in package_dirs(repo):
        try: manifest = load_json(pkg / "manifest.json")
        except Exception as exc:
            errors.append(f"PACKAGE_MANIFEST_UNREADABLE:{pkg}:{exc}"); continue
        if manifest.get("package_id") != pkg.name: errors.append(f"PACKAGE_ID_PATH_MISMATCH:{pkg}")
        if not PACKAGE_RE.match(pkg.name): errors.append(f"PACKAGE_ID_INVALID:{pkg.name}")
        if manifest.get("claim_ceiling") != "C1": errors.append(f"PACKAGE_CLAIM_CEILING:{pkg.name}")
        if manifest.get("claim_promotion") is not False: errors.append(f"PACKAGE_CLAIM_PROMOTION:{pkg.name}")
        if manifest.get("integration_authority") != "NONE": errors.append(f"PACKAGE_INTEGRATION_AUTHORITY:{pkg.name}")
        if manifest.get("state") not in STATES: errors.append(f"PACKAGE_STATE_INVALID:{pkg.name}")
        items = load_json(pkg / "items.json")
        if manifest.get("item_count") != len(items.get("items", [])): errors.append(f"PACKAGE_ITEM_COUNT:{pkg.name}")
        snaps = sorted((pkg / "snapshots").glob("v*")) if (pkg / "snapshots").exists() else []
        if manifest.get("snapshot_count") != len(snaps): errors.append(f"PACKAGE_SNAPSHOT_COUNT:{pkg.name}")
        for snap in snaps:
            sums = snap / "SHA256SUMS.txt"
            if not sums.is_file(): errors.append(f"SNAPSHOT_SUMS_MISSING:{snap}"); continue
            for line in sums.read_text(encoding="utf-8").splitlines():
                digest, name = line.split("  ", 1); target = snap / name
                if not target.is_file() or sha256_file(target) != digest:
                    errors.append(f"SNAPSHOT_DIGEST_MISMATCH:{snap}:{name}")
    event_base = pipeline_root(repo) / "events"
    if event_base.exists():
        for path in event_base.glob("*/*/*/*.json"):
            try: event = load_json(path)
            except Exception as exc: errors.append(f"EVENT_UNREADABLE:{path}:{exc}"); continue
            if event.get("claim_ceiling") != "C1": errors.append(f"EVENT_CLAIM_CEILING:{path}")
            if not event.get("package_id"): errors.append(f"EVENT_PACKAGE_MISSING:{path}")
    return sorted(errors)


def cmd_validate(ns) -> None:
    errors = validate(ns.root.resolve())
    print(json.dumps({"object": "NEXUS_OMEGA_RESEARCH_PIPELINE_VALIDATION_V1",
                      "status": "PASS" if not errors else "FAIL", "errors": errors}, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--root", type=Path, default=Path.cwd())
    sp = p.add_subparsers(dest="cmd", required=True)
    n = sp.add_parser("new"); n.add_argument("--phase", required=True); n.add_argument("--strand", required=True)
    n.add_argument("--title", required=True); n.add_argument("--objective", required=True); n.add_argument("--slug")
    n.add_argument("--producer", default="AXIOM"); n.add_argument("--processor", default="CURSOR_PRAXIS")
    n.add_argument("--predecessor", action="append"); n.add_argument("--question", action="append"); n.set_defaults(func=cmd_new)
    a = sp.add_parser("add"); a.add_argument("--package", required=True); a.add_argument("--role", required=True)
    a.add_argument("--path-ref"); a.add_argument("--repository", default="nexusomegac27/NEXUS-OMEGA-EVIDENCE")
    a.add_argument("--commit"); a.add_argument("--git-blob"); a.add_argument("--bytes", type=int); a.add_argument("--sha256")
    a.add_argument("--source-status", default="PRESENT"); a.add_argument("--producer", default="AXIOM")
    a.add_argument("--relevance", required=True); a.add_argument("--uncertainty", action="append"); a.set_defaults(func=cmd_add)
    s = sp.add_parser("state"); s.add_argument("--package", required=True); s.add_argument("--state", required=True)
    s.add_argument("--actor", required=True); s.add_argument("--activity", required=True); s.add_argument("--note", action="append"); s.set_defaults(func=cmd_state)
    z = sp.add_parser("seal"); z.add_argument("--package", required=True); z.add_argument("--actor", default="AXIOM"); z.set_defaults(func=cmd_seal)
    v = sp.add_parser("validate"); v.set_defaults(func=cmd_validate)
    b = sp.add_parser("build-index"); b.set_defaults(func=lambda ns: build_index(ns.root.resolve()))
    return p


def main():
    ns = parser().parse_args(); ns.func(ns)

if __name__ == "__main__":
    main()
