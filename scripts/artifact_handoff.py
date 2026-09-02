#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate and process NEXUS OMEGA artifact handoff inbox entries."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

PROTOCOL = "INBOX_VALIDATE_BIND_RELAY_ACK_V1"
HANDOFF_ROOT = Path("research/pipeline/handoff")
INBOX = HANDOFF_ROOT / "inbox"
SEED_HANDOFF_ID = "NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0"
HANDOFF_RE = re.compile(r"^NEXUS_AH_\d{8}T\d{6}Z_[a-z0-9][a-z0-9_-]{0,79}_R\d+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CLAIM_CEILINGS = {"C0_EXPLORATORY", "C1_DESCRIPTIVE", "C0_EXPLORATORY_C1_DESCRIPTIVE", "C1"}
TOKEN_CLASSES = {"T16", "T32", "T64", "T128", "T256", "UNSPECIFIED"}
AUTHORITY_GATES = {
    "MERGE",
    "CLAIM_PROMOTION",
    "FOUNDATION_PROMOTION",
    "MAIN_WRITE",
    "FORCE_PUSH",
    "SECRET_ACCESS",
    "PUBLIC_RELEASE",
    "DEPLOYMENT",
    "INTEGRATION_AUTHORITY",
}
ENVELOPE_KEYS = {
    "schema_version",
    "protocol",
    "handoff_id",
    "stage",
    "object_id",
    "source_return_id",
    "source_return_path",
    "created_at_utc",
    "received_at_utc",
    "producer",
    "validator",
    "claim_ceiling",
    "claim_promotion",
    "foundation_promotion",
    "integration_authority",
    "merge_authority",
    "force_push",
    "main_write",
    "self_validation",
    "branch_policy",
    "lane_separation",
    "payload_refs",
    "ledger_refs",
    "receipt_refs",
    "token_continuation",
    "authority_gates",
    "relay_targets",
    "caveats",
}
AGENT_KEYS = {"agent_id", "role", "provider", "model", "session_id"}
REF_KEYS = {"role", "path", "bytes", "sha256"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json_path(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM prohibited")
    if b"\r" in data:
        raise ValueError("CR bytes prohibited")
    obj = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    if not isinstance(obj, dict):
        raise ValueError("top-level JSON object required")
    return obj


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) for row in rows)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_path(root: Path, rel: str) -> tuple[Path | None, str | None]:
    if not isinstance(rel, str) or not rel:
        return None, "REF_PATH"
    if "\\" in rel or ":" in rel:
        return None, f"REF_PATH_INVALID:{rel}"
    pure = PurePosixPath(rel)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None, f"REF_PATH_INVALID:{rel}"
    root = root.resolve()
    path = (root / Path(*pure.parts)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None, f"REF_PATH_ESCAPE:{rel}"
    return path, None


def validate_ref(root: Path, ref: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(ref, dict):
        return [f"{prefix}_REF_OBJECT"]
    if set(ref) != REF_KEYS:
        errors.append(f"{prefix}_REF_KEYSET")
    path_value = ref.get("path")
    path, path_error = repo_path(root, path_value)
    if path_error:
        errors.append(f"{prefix}_{path_error}")
        return errors
    assert path is not None
    if not path.is_file():
        errors.append(f"{prefix}_MISSING:{path_value}")
        return errors
    if not isinstance(ref.get("bytes"), int) or ref["bytes"] < 0:
        errors.append(f"{prefix}_BYTES")
    elif path.stat().st_size != ref["bytes"]:
        errors.append(f"{prefix}_BYTES_MISMATCH:{path_value}")
    if not isinstance(ref.get("sha256"), str) or not SHA256_RE.fullmatch(ref["sha256"]):
        errors.append(f"{prefix}_SHA256")
    elif sha256_file(path) != ref["sha256"]:
        errors.append(f"{prefix}_SHA256_MISMATCH:{path_value}")
    return errors


def load_jsonl_path(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append("JSONL_BOM")
    if b"\r" in data:
        errors.append("JSONL_CR")
    rows: list[dict[str, Any]] = []
    for number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line.strip():
            errors.append(f"JSONL_BLANK_LINE:{number}")
            continue
        try:
            row = json.loads(raw_line.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
        except Exception as exc:
            errors.append(f"JSONL_INVALID:{number}:{exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"JSONL_OBJECT_REQUIRED:{number}")
            continue
        if "event" not in row:
            errors.append(f"JSONL_EVENT_MISSING:{number}")
        rows.append(row)
    return rows, errors


def validate_agent(value: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return [f"{prefix}_OBJECT"]
    if set(value) != AGENT_KEYS:
        errors.append(f"{prefix}_KEYSET")
    for key in AGENT_KEYS:
        if not isinstance(value.get(key), str) or not value[key]:
            errors.append(f"{prefix}_{key.upper()}")
    if value.get("role") not in {"PRODUCER", "VALIDATOR", "OPERATOR", "RELAY"}:
        errors.append(f"{prefix}_ROLE")
    return errors


def validate_file_event_targets(root: Path, env: dict[str, Any], rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ledgers = env.get("ledger_refs", {})
    policy = ledgers.get("file_event_target_hash_policy")
    caveats = set(env.get("caveats", []))
    if policy == "PRESERVE_ONLY_DECLARED_CAVEAT":
        if "FILE_EVENT_TARGET_HASHES_PRESERVED_NOT_REASSERTED" not in caveats:
            errors.append("LEDGER_PRESERVE_CAVEAT_MISSING")
        return errors
    if policy != "REQUIRE_MATCH":
        return ["LEDGER_POLICY_INVALID"]
    base_rel = ledgers.get("file_event_base_path")
    base_dir, base_error = repo_path(root, base_rel) if isinstance(base_rel, str) else (None, "REF_PATH")
    if base_error:
        return [f"LEDGER_BASE_{base_error}"]
    assert base_dir is not None
    if not base_dir.is_dir():
        return [f"LEDGER_BASE_MISSING:{base_rel}"]
    for number, row in enumerate(rows, start=1):
        if not all(key in row for key in ("path", "bytes", "sha256")):
            continue
        target_rel = row["path"]
        if not isinstance(target_rel, str) or "\\" in target_rel or "/" in target_rel or target_rel in {"", ".", ".."}:
            errors.append(f"FILE_EVENT_{number}_TARGET_PATH")
            continue
        target = base_dir / target_rel
        if not target.is_file():
            errors.append(f"FILE_EVENT_{number}_TARGET_MISSING:{target_rel}")
            continue
        if target.stat().st_size != row.get("bytes"):
            errors.append(f"FILE_EVENT_{number}_TARGET_BYTES:{target_rel}")
        if sha256_file(target) != row.get("sha256"):
            errors.append(f"FILE_EVENT_{number}_TARGET_SHA256:{target_rel}")
    return errors


def validate_envelope_obj(root: Path, env: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(env) != ENVELOPE_KEYS:
        errors.append("HANDOFF_KEYSET")
    if env.get("schema_version") != "1.0.0":
        errors.append("HANDOFF_SCHEMA_VERSION")
    if env.get("protocol") != PROTOCOL:
        errors.append("HANDOFF_PROTOCOL")
    if env.get("stage") != "INBOX":
        errors.append("HANDOFF_STAGE")
    if not isinstance(env.get("handoff_id"), str) or not HANDOFF_RE.fullmatch(env["handoff_id"]):
        errors.append("HANDOFF_ID")
    if env.get("claim_ceiling") not in CLAIM_CEILINGS:
        errors.append("HANDOFF_CLAIM_CEILING")
    if env.get("claim_promotion") is not False:
        errors.append("HANDOFF_CLAIM_PROMOTION")
    if env.get("foundation_promotion") is not False:
        errors.append("HANDOFF_FOUNDATION_PROMOTION")
    if env.get("integration_authority") != "NONE":
        errors.append("HANDOFF_INTEGRATION_AUTHORITY")
    if env.get("merge_authority") != "NONE":
        errors.append("HANDOFF_MERGE_AUTHORITY")
    if env.get("force_push") is not False:
        errors.append("HANDOFF_FORCE_PUSH")
    if env.get("main_write") is not False:
        errors.append("HANDOFF_MAIN_WRITE")
    if env.get("self_validation") is not False:
        errors.append("HANDOFF_SELF_VALIDATION")

    errors.extend(validate_agent(env.get("producer"), "PRODUCER"))
    errors.extend(validate_agent(env.get("validator"), "VALIDATOR"))
    producer = env.get("producer") if isinstance(env.get("producer"), dict) else {}
    validator = env.get("validator") if isinstance(env.get("validator"), dict) else {}
    if producer.get("agent_id") == validator.get("agent_id"):
        errors.append("HANDOFF_SELF_VALIDATION")
    if producer.get("role") == "VALIDATOR" or validator.get("role") != "VALIDATOR":
        errors.append("HANDOFF_VALIDATOR_ROLE")

    branch_policy = env.get("branch_policy")
    if not isinstance(branch_policy, dict):
        errors.append("BRANCH_POLICY_OBJECT")
    else:
        if not COMMIT_RE.fullmatch(str(branch_policy.get("source_commit", ""))):
            errors.append("BRANCH_POLICY_SOURCE_COMMIT")
        for key, code in (
            ("normal_push_only", "BRANCH_POLICY_NORMAL_PUSH"),
            ("no_force_push", "BRANCH_POLICY_NO_FORCE_PUSH"),
            ("no_merge_automation", "BRANCH_POLICY_NO_MERGE_AUTOMATION"),
            ("no_claim_promotion_automation", "BRANCH_POLICY_NO_CLAIM_PROMOTION_AUTOMATION"),
            ("no_foundation_promotion_automation", "BRANCH_POLICY_NO_FOUNDATION_PROMOTION_AUTOMATION"),
        ):
            if branch_policy.get(key) is not True:
                errors.append(code)

    lane = env.get("lane_separation")
    if not isinstance(lane, dict):
        errors.append("LANE_SEPARATION_OBJECT")
    else:
        if lane.get("keep_r2_pr13_separate") is not True:
            errors.append("LANE_SEPARATION_R2_PR13")
        if lane.get("r2_branch") == lane.get("pr13_branch"):
            errors.append("LANE_SEPARATION_BRANCH_FUSION")

    payload_refs = env.get("payload_refs")
    if not isinstance(payload_refs, list) or not payload_refs:
        errors.append("PAYLOAD_REFS")
    else:
        seen_paths: set[str] = set()
        for ref in payload_refs:
            if isinstance(ref, dict):
                path = ref.get("path")
                if path in seen_paths:
                    errors.append(f"PAYLOAD_DUPLICATE_PATH:{path}")
                if isinstance(path, str):
                    seen_paths.add(path)
            errors.extend(validate_ref(root, ref, "PAYLOAD"))

    ledgers = env.get("ledger_refs")
    if not isinstance(ledgers, dict):
        errors.append("LEDGER_REFS_OBJECT")
    else:
        file_ref = ledgers.get("file_event_ledger")
        workflow_ref = ledgers.get("workflow_event_ledger")
        errors.extend(validate_ref(root, file_ref, "FILE_EVENT_LEDGER"))
        errors.extend(validate_ref(root, workflow_ref, "WORKFLOW_EVENT_LEDGER"))
        if isinstance(file_ref, dict):
            file_path, file_path_error = repo_path(root, file_ref.get("path"))
            if file_path_error:
                errors.append(f"FILE_EVENT_LEDGER_{file_path_error}")
            elif file_path:
                rows, row_errors = load_jsonl_path(file_path)
                errors.extend(f"FILE_EVENT_LEDGER_{err}" for err in row_errors)
                if not rows:
                    errors.append("FILE_EVENT_LEDGER_EMPTY")
                errors.extend(validate_file_event_targets(root, env, rows))
        if isinstance(workflow_ref, dict):
            workflow_path, workflow_path_error = repo_path(root, workflow_ref.get("path"))
            if workflow_path_error:
                errors.append(f"WORKFLOW_EVENT_LEDGER_{workflow_path_error}")
            elif workflow_path:
                rows, row_errors = load_jsonl_path(workflow_path)
                errors.extend(f"WORKFLOW_EVENT_LEDGER_{err}" for err in row_errors)
                if not rows:
                    errors.append("WORKFLOW_EVENT_LEDGER_EMPTY")
                for number, row in enumerate(rows, start=1):
                    if row.get("event") == "UNEXPECTED_FAIL" and not (row.get("id") or row.get("detail")):
                        errors.append(f"WORKFLOW_EVENT_{number}_UNEXPECTED_FAIL_UNDESCRIBED")

    receipts = env.get("receipt_refs")
    if not isinstance(receipts, dict):
        errors.append("RECEIPT_REFS_OBJECT")
    else:
        errors.extend(validate_ref(root, receipts.get("entry_receipt"), "ENTRY_RECEIPT"))
        errors.extend(validate_ref(root, receipts.get("exit_receipt"), "EXIT_RECEIPT"))

    tokens = env.get("token_continuation")
    if not isinstance(tokens, dict):
        errors.append("TOKEN_CONTINUATION_OBJECT")
    else:
        if tokens.get("requested_token_class") not in TOKEN_CLASSES:
            errors.append("TOKEN_REQUESTED_CLASS")
        if not isinstance(tokens.get("token_class_used"), str) or not tokens["token_class_used"]:
            errors.append("TOKEN_CLASS_USED")
        if not isinstance(tokens.get("token_telemetry"), str) or not tokens["token_telemetry"]:
            errors.append("TOKEN_TELEMETRY")
        if tokens.get("continuation_required_on_token_pressure") is not True:
            errors.append("TOKEN_PRESSURE_POLICY")
        if not isinstance(tokens.get("continuation_required"), bool):
            errors.append("CONTINUATION_REQUIRED_BOOL")
        if tokens.get("continuation_required") is True:
            capsule = tokens.get("continuation_capsule_path")
            if not isinstance(capsule, str):
                errors.append("CONTINUATION_CAPSULE_MISSING")
            else:
                capsule_path, capsule_error = repo_path(root, capsule)
                if capsule_error or capsule_path is None or not capsule_path.is_file():
                    errors.append("CONTINUATION_CAPSULE_MISSING")

    gates = env.get("authority_gates")
    if not isinstance(gates, list):
        errors.append("AUTHORITY_GATES")
    else:
        for gate in gates:
            if not isinstance(gate, dict):
                errors.append("AUTHORITY_GATE_OBJECT")
                continue
            gate_name = gate.get("gate")
            if gate_name not in AUTHORITY_GATES:
                errors.append(f"AUTHORITY_GATE_UNKNOWN:{gate_name}")
            if gate.get("status") == "OPEN":
                errors.append(f"HANDOFF_AUTHORITY_GATE_OPEN:{gate_name}")
            if gate.get("operator_confirmation_required") is True and gate.get("status") != "CLOSED":
                errors.append(f"HANDOFF_AUTHORITY_GATE_OPEN:{gate_name}")
            if gate.get("operator_confirmation_required") is False and gate.get("status") == "CLOSED":
                errors.append(f"AUTHORITY_GATE_AUTO_CLOSED:{gate_name}")

    relay_targets = env.get("relay_targets")
    if not isinstance(relay_targets, list) or not relay_targets:
        errors.append("RELAY_TARGETS")
    else:
        for target in relay_targets:
            if not isinstance(target, dict):
                errors.append("RELAY_TARGET_OBJECT")
                continue
            if target.get("authority_required") is not False:
                errors.append(f"RELAY_TARGET_AUTHORITY_REQUIRED:{target.get('target')}")

    source_path = env.get("source_return_path")
    if isinstance(source_path, str):
        path, path_error = repo_path(root, source_path)
        if path_error:
            errors.append(f"SOURCE_RETURN_{path_error}")
        elif path is not None and not path.is_file():
            errors.append(f"SOURCE_RETURN_MISSING:{source_path}")

    return sorted(set(errors))


def handoff_paths(root: Path) -> list[Path]:
    inbox = root.resolve() / INBOX
    if not inbox.exists():
        return []
    return sorted(inbox.glob("*/handoff.json"))


def validate_handoff_path(root: Path, path: Path) -> list[str]:
    try:
        env = load_json_path(path)
    except Exception as exc:
        return [f"HANDOFF_JSON_INVALID:{path.relative_to(root).as_posix()}:{exc}"]
    errors = validate_envelope_obj(root, env)
    if path.parent.name != env.get("handoff_id"):
        errors.append("HANDOFF_ID_PATH_MISMATCH")
    return errors


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    paths = handoff_paths(root)
    if not (root / HANDOFF_ROOT / "README.md").is_file():
        errors.append("HANDOFF_ROOT_README_MISSING")
    if not (root / INBOX / SEED_HANDOFF_ID / "handoff.json").is_file():
        errors.append("HANDOFF_SEED_MISSING")
    if not paths:
        errors.append("HANDOFF_INBOX_EMPTY")
    seen_ids: set[str] = set()
    for path in paths:
        try:
            env = load_json_path(path)
            handoff_id = str(env.get("handoff_id", path.parent.name))
        except Exception:
            handoff_id = path.parent.name
        if handoff_id in seen_ids:
            errors.append(f"HANDOFF_DUPLICATE_ID:{handoff_id}")
        seen_ids.add(handoff_id)
        for err in validate_handoff_path(root, path):
            errors.append(f"{handoff_id}:{err}")
    return {
        "object": "NEXUS_OMEGA_ARTIFACT_HANDOFF_VALIDATION_V1",
        "protocol": PROTOCOL,
        "status": "PASS" if not errors else "FAIL_CLOSED",
        "handoffs": len(paths),
        "errors": sorted(set(errors)),
    }


def github_context() -> dict[str, Any]:
    keys = [
        "GITHUB_REPOSITORY",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_ATTEMPT",
        "GITHUB_JOB",
        "GITHUB_WORKFLOW",
        "GITHUB_SHA",
        "GITHUB_REF_NAME",
        "GITHUB_ACTOR",
        "GITHUB_EVENT_NAME",
    ]
    return {key.lower(): os.environ.get(key) for key in keys if os.environ.get(key)}


def load_env(root: Path, path: Path) -> dict[str, Any]:
    env = load_json_path(path)
    errors = validate_envelope_obj(root, env)
    if errors:
        raise ValueError(f"{env.get('handoff_id', path)} validation errors: {errors}")
    return env


def generated_receipts(env: dict[str, Any], envelope_sha256: str, generated_at: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    gh = github_context()
    common = {
        "schema_version": "1.0.0",
        "protocol": PROTOCOL,
        "handoff_id": env["handoff_id"],
        "generated_at_utc": generated_at,
        "claim_ceiling": env["claim_ceiling"],
        "claim_promotion": False,
        "foundation_promotion": False,
        "integration_authority": "NONE",
        "generation_context": "GITHUB_ACTIONS_WORKFLOW_RECEIPT" if gh else "LOCAL_REPOSITORY_RECEIPT",
        "github_context": gh,
        "source_envelope_sha256": envelope_sha256,
        "source_return_id": env["source_return_id"],
        "source_return_path": env["source_return_path"],
    }
    bind = {
        **common,
        "receipt_type": "BIND",
        "decision": "BOUND_STRUCTURE_ONLY_C1",
        "payload_refs": env["payload_refs"],
        "ledger_refs": env["ledger_refs"],
        "receipt_refs": env["receipt_refs"],
        "caveats": env["caveats"],
    }
    relay = {
        **common,
        "receipt_type": "RELAY",
        "decision": "AUTO_RELAY_ALLOWED_STRUCTURE_ONLY",
        "relay_targets": env["relay_targets"],
        "operator_required": False,
        "authority_gates": env["authority_gates"],
        "relay_instruction": "Consume the bound bytes and receipts only; do not infer semantic validation, merge, claim promotion or foundation promotion.",
    }
    ack = {
        **common,
        "receipt_type": "ACK",
        "decision": "AUTO_ACK_VALIDATED_STRUCTURE_ONLY",
        "token_continuation": env["token_continuation"],
        "self_validation": False,
        "operator_required": False,
        "ack_state": "HANDOFF_ACCEPTED_FOR_RELAY_STRUCTURE_ONLY",
    }
    events = [
        {"event": "VALIDATE_PASS", "handoff_id": env["handoff_id"], "ts": generated_at},
        {"event": "BIND_RECEIPT_CREATED", "handoff_id": env["handoff_id"], "ts": generated_at},
        {"event": "RELAY_PACKET_CREATED", "handoff_id": env["handoff_id"], "ts": generated_at},
        {"event": "ACK_RECEIPT_CREATED", "handoff_id": env["handoff_id"], "ts": generated_at},
    ]
    return bind, relay, ack, events


def process(root: Path, output: Path, write_repo: bool = False) -> dict[str, Any]:
    root = root.resolve()
    result = validate(root)
    if result["errors"]:
        return result
    base = root / HANDOFF_ROOT if write_repo else output.resolve()
    generated_at = now_iso()
    processed = []
    for envelope_path in handoff_paths(root):
        env = load_env(root, envelope_path)
        handoff_id = env["handoff_id"]
        envelope_sha = sha256_file(envelope_path)
        bind, relay, ack, events = generated_receipts(env, envelope_sha, generated_at)
        dump_json(base / "bound" / handoff_id / "BIND_RECEIPT.json", bind)
        dump_json(base / "relay" / handoff_id / "RELAY_PACKET.json", relay)
        dump_json(base / "ack" / handoff_id / "ACK_RECEIPT.json", ack)
        dump_jsonl(base / "ack" / handoff_id / "HANDOFF_WORKFLOW_EVENTS.jsonl", events)
        processed.append(handoff_id)
    summary = [
        "# Artifact handoff summary",
        "",
        f"Protocol: `{PROTOCOL}`",
        f"Status: `{result['status']}`",
        f"Handoffs processed: `{len(processed)}`",
        "",
    ]
    for handoff_id in processed:
        summary.append(f"- `{handoff_id}`: bind, relay and ack receipts generated")
    if not write_repo:
        with (base / "SUMMARY.md").open("w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(summary) + "\n")
    return {**result, "processed": processed, "output": base.as_posix()}


def cmd_validate(ns: argparse.Namespace) -> None:
    result = validate(ns.root)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not result["errors"] else 1)


def cmd_process(ns: argparse.Namespace) -> None:
    result = process(ns.root, ns.output, ns.write_repo)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not result["errors"] else 1)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path.cwd())
    sp = p.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("validate")
    v.set_defaults(func=cmd_validate)
    proc = sp.add_parser("process")
    proc.add_argument("--output", type=Path, default=Path("_artifact_handoff_out"))
    proc.add_argument("--write-repo", action="store_true")
    proc.set_defaults(func=cmd_process)
    return p


def main() -> None:
    ns = parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
