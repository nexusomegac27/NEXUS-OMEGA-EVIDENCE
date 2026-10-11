#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""NEXUS R27-E: read-only, deny-by-default PR path and external-return validator.
Run from the TRUSTED BASE branch in a pull_request_target workflow.
Never check out, import or execute code from the untrusted PR head.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CONTRACT = "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json"
HEX = re.compile(r"^[a-f0-9]{64}$")
GH_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")


def strict_json(raw: bytes):
    def unique(pairs):
        d = {}
        for key, val in pairs:
            if key in d:
                raise ValueError("DUPLICATE_JSON_KEY:" + key)
            d[key] = val
        return d
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def api_json(api_url: str, token: str):
    if not api_url.startswith("https://api.github.com/"):
        raise ValueError("NON_GITHUB_API_URL")
    req = urllib.request.Request(api_url, headers={
        "Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "NEXUS-R27E-structural-firewall",
    })
    with urllib.request.urlopen(req, timeout=20) as res:
        return strict_json(res.read(2_500_000))


def get_changed_files(repo: str, number: int, token: str):
    out = []
    for page in range(1, 5):
        url = f"https://api.github.com/repos/{repo}/pulls/{number}/files?per_page=100&page={page}"
        batch = api_json(url, token)
        if not isinstance(batch, list):
            raise ValueError("INVALID_PR_FILE_RESPONSE")
        out.extend(batch)
        if len(out) > 100:
            raise ValueError("TOO_MANY_PR_CHANGES")
        if len(batch) < 100:
            break
    return out


def get_file_bytes(repo: str, head_sha: str, path: str, token: str, max_bytes: int):
    if not GH_NAME.fullmatch(repo) or not SHA.fullmatch(head_sha):
        raise ValueError("UNSAFE_SOURCE_REF")
    escaped = urllib.parse.quote(path, safe="/")
    url = f"https://api.github.com/repos/{repo}/contents/{escaped}?ref={head_sha}"
    o = api_json(url, token)
    if not isinstance(o, dict) or o.get("encoding") != "base64" or o.get("type") != "file":
        raise ValueError("UNREADABLE_SOURCE_FILE:" + path)
    if int(o.get("size", max_bytes + 1)) > max_bytes:
        raise ValueError("OVERSIZED_FILE:" + path)
    raw = base64.b64decode(o["content"], validate=False)
    if len(raw) > max_bytes or git_blob_sha1(raw) != o.get("sha"):
        raise ValueError("BYTE_OR_BLOB_MISMATCH:" + path)
    raw.decode("utf-8")
    return raw


def slot_map(registry: dict) -> dict:
    allowed = {}
    for assignment in registry["assignments"]:
        base = assignment["returns_path"]
        if not base.startswith("research/") or not base.endswith("/returns/"):
            raise ValueError("INVALID_NEXUS_SLOT")
        if assignment["root"] + "/returns/" != base:
            raise ValueError("SLOT_ROOT_DIVERGENCE")
        for filename in assignment["filenames"]:
            if "/" in filename or "\\" in filename or filename in (".", ".."):
                raise ValueError("INVALID_FILENAME")
            path = base + filename
            if path in allowed:
                raise ValueError("DUPLICATE_SLOT")
            allowed[path] = assignment
    return allowed


def manifest_path_for_assignment(assignment: dict) -> str:
    """Select exactly one NEXUS-owned manifest name; never trust a PR-supplied path.

    Allows future owner-preallocated assignments to share an existing returns/
    directory without weakening R27-E's immutable original manifest contract.
    """
    filenames = assignment["filenames"]
    manifests = [n for n in filenames if n.endswith("_RETURN_MANIFEST_R0.json")]
    if len(manifests) != 1:
        raise ValueError("ASSIGNMENT_MUST_HAVE_ONE_MANIFEST")
    named = assignment.get("manifest_filename", manifests[0])
    if named != manifests[0]:
        raise ValueError("ASSIGNMENT_MANIFEST_CONFLICT")
    return assignment["returns_path"] + named


def validate_paths(files: list, actor: str, registry: dict) -> list[str]:
    errors = []
    owner = registry["owner_github_login"]
    slots = slot_map(registry)
    external = actor != owner
    if external and actor not in registry["external_actor_allowlist"]:
        errors.append("UNREGISTERED_EXTERNAL_GITHUB_ACTOR")
    changed = set()
    for file in files:
        p, status = file.get("filename", ""), file.get("status", "")
        if p in changed:
            errors.append("DUPLICATE_CHANGE_PATH:" + p)
        changed.add(p)
        if not p or p.startswith("/") or "\\" in p or "//" in p or ".." in p.split("/"):
            errors.append("INVALID_PATH:" + p)
            continue
        if external:
            if p not in slots:
                errors.append("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT:" + p)
            if status != "added":
                errors.append("EXTERNAL_NOT_CREATE_ONLY:" + p + ":" + status)
        elif "/returns/" in p and p not in slots:
            if not (p.endswith("/returns/README.md") and status == "added"):
                errors.append("UNREGISTERED_RETURN_PATH:" + p)
        if status in ("removed", "renamed", "copied") and (external or "/returns/" in p):
            errors.append("FORBIDDEN_RETURN_PATH_OPERATION:" + p)
    if external:
        matched = {p for p in changed if p in slots}
        involved = {id(slots[p]) for p in matched}
        if len(involved) != 1:
            errors.append("RETURN_MUST_USE_ONE_ASSIGNED_SLOT")
        else:
            slot = slots[next(iter(matched))]
            if slot["status"] != "ACTIVE_AUTHORIZED":
                errors.append("SLOT_NOT_ACTIVATED")
            expected = {slot["returns_path"] + n for n in slot["filenames"]}
            if changed != expected:
                errors.append("INCOMPLETE_OR_EXTRA_RETURN_FILE_SET")
        if len(files) > registry["max_files_per_external_return"]:
            errors.append("FILE_COUNT_CAP_EXCEEDED")
    return errors


def validate_return_contents(files: list, event: dict, registry: dict, token: str) -> list[str]:
    errors = []
    path_to_data = {}
    limit = registry["max_file_bytes"]
    head = event["pull_request"]["head"]
    repo, sha = head["repo"]["full_name"], head["sha"]
    total = 0
    for f in files:
        path = f["filename"]
        data = get_file_bytes(repo, sha, path, token, limit)
        total += len(data)
        path_to_data[path] = data
        if path.endswith(".md"):
            text = data.decode("utf-8")
            for field in ("OBJECT", "PARENT", "CLAIM_CEILING", "RUNTIME", "NEW_WORKER"):
                if not re.search(r"(?m)^\s*" + field + r"\s*=", text[:2500]):
                    errors.append("MISSING_HEADER:" + field + ":" + path)
            if not re.search(r"(?m)^\s*CLAIM_CEILING\s*=\s*C1_DESCRIPTIVE_ONLY", text[:2500]):
                errors.append("CLAIM_CEILING_INVALID:" + path)
            if not re.search(r"(?m)^\s*RUNTIME\s*=\s*NOT_AUTHORIZED", text[:2500]):
                errors.append("RUNTIME_UNAUTHORIZED:" + path)
            if not re.search(r"(?m)^\s*NEW_WORKER\s*=\s*NO", text[:2500]):
                errors.append("WORKER_UNAUTHORIZED:" + path)
        elif path.endswith(".json"):
            strict_json(data)
        else:
            errors.append("DISALLOWED_FILE_TYPE:" + path)
    if total > registry["max_total_bytes"]:
        errors.append("TOTAL_RETURN_BYTES_EXCEEDED")
    assignment = slot_map(registry)[files[0]["filename"]]
    prefix = assignment["returns_path"]
    manifest_path = manifest_path_for_assignment(assignment)
    manifest = strict_json(path_to_data[manifest_path])
    required = {"schema_version", "agent_id", "github_actor", "parent_order_sha256",
                "claim_ceiling", "runtime", "new_worker", "axiom_ack", "children"}
    if set(manifest) != required:
        errors.append("MANIFEST_KEY_SET_MISMATCH")
        return errors
    for field, expected in [("schema_version", "1.0.0"), ("claim_ceiling", "C1_DESCRIPTIVE_ONLY"),
                            ("runtime", "NOT_AUTHORIZED"), ("new_worker", "NO"),
                            ("axiom_ack", "PENDING"), ("parent_order_sha256", assignment["parent_order_sha256"]),
                            ("github_actor", event["pull_request"]["user"]["login"])]:
        if manifest.get(field) != expected:
            errors.append("MANIFEST_FIELD_MISMATCH:" + field)
    if not isinstance(manifest.get("agent_id"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]{2,64}", manifest["agent_id"]):
        errors.append("INVALID_AGENT_ID")
    children = manifest.get("children")
    if not isinstance(children, list):
        return errors + ["MANIFEST_CHILDREN_MISSING"]
    declared = {}
    for child in children:
        if not isinstance(child, dict) or set(child) != {"filename", "bytes", "sha256", "git_blob_sha1"}:
            errors.append("INVALID_CHILD_RECORD")
            continue
        name = child["filename"]
        if not isinstance(name, str) or "/" in name or name in declared:
            errors.append("INVALID_OR_DUPLICATE_CHILD_NAME")
            continue
        declared[name] = child
    expected = {p[len(prefix):] for p in path_to_data if p != manifest_path}
    if set(declared) != expected:
        errors.append("MANIFEST_CHILD_SET_MISMATCH")
    for name in expected & set(declared):
        raw = path_to_data[prefix + name]
        c = declared[name]
        if c.get("bytes") != len(raw) or c.get("sha256") != hashlib.sha256(raw).hexdigest() or c.get("git_blob_sha1") != git_blob_sha1(raw):
            errors.append("CHILD_CONTENT_HASH_MISMATCH:" + name)
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--event", type=Path, required=True)
    p.add_argument("--registry", type=Path, default=Path(CONTRACT))
    args = p.parse_args()
    event = strict_json(args.event.read_bytes())
    registry = strict_json(args.registry.read_bytes())
    pr = event["pull_request"]
    actor = pr["user"]["login"]
    if not GH_NAME.fullmatch(event["repository"]["full_name"]):
        raise ValueError("INVALID_REPO_METADATA")
    if pr["base"]["ref"] != "main":
        raise ValueError("NON_CANONICAL_TARGET_BRANCH")
    token = os.environ["GITHUB_TOKEN"]
    files = get_changed_files(event["repository"]["full_name"], int(pr["number"]), token)
    errors = validate_paths(files, actor, registry)
    # Even an owner-side AXIOM bridge cannot use an incomplete/tampered return.
    # An owner policy/README PR has no registered return-asset modifications.
    known = slot_map(registry)
    return_files = [f for f in files if f.get("filename") in known]
    if return_files:
        slot = known[return_files[0]["filename"]]
        expected = {slot["returns_path"] + n for n in slot["filenames"]}
        received = {f.get("filename") for f in files}
        if received != expected or any(f.get("status") != "added" for f in files):
            errors.append("INCOMPLETE_OR_MIXED_RETURN_PR")
        if not errors:
            errors.extend(validate_return_contents(files, event, registry, token))
    print(json.dumps({"object": "NEXUS_R27E_EXTERNAL_PR_FIREWALL_V1",
        "status": "PASS" if not errors else "FAIL", "actor": actor,
        "changed_files": len(files), "errors": errors}, sort_keys=True))
    return int(bool(errors))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as err:
        print(json.dumps({"object": "NEXUS_R27E_EXTERNAL_PR_FIREWALL_V1",
                          "status": "FAIL_CLOSED", "error": type(err).__name__ + ": " + str(err)}))
        sys.exit(1)
