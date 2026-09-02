#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate and package NEXUS OMEGA artifact rollout preparation plans."""

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

PROTOCOL = "PR15_ARTIFACT_HANDOFF_ROLLOUT_PREP_V1"
ROLLOUT_ROOT = Path("research/pipeline/rollout")
PLANS = ROLLOUT_ROOT / "plans"
RECEIPTS = ROLLOUT_ROOT / "receipts"
SEED_ROLLOUT_ID = "NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0"
SEED_HANDOFF_ID = "NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0"
PR15_HEAD = "ab4081133ad9d37d6a3ae3fce2c838ef1d6eea9a"
PR15_PARENT = "5c1dc9df32fd8d96277e98ef754602d9726e52d7"
PR15_BRANCH = "axiom/agent-authorization-admission-r3-open-research-20260902"
ROLLOUT_RE = re.compile(r"^NEXUS_RO_\d{8}T\d{6}Z_[a-z0-9][a-z0-9_-]{0,79}_R\d+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CLAIM_CEILINGS = {"C0_EXPLORATORY", "C1_DESCRIPTIVE", "C0_EXPLORATORY_C1_DESCRIPTIVE", "C1"}
TOKEN_CLASSES = {"T16", "T32", "T64", "T128", "T256", "UNSPECIFIED"}
AUTHORITY_GATES = {
    "MERGE",
    "MAIN_WRITE",
    "FORCE_PUSH",
    "PUBLIC_RELEASE",
    "DEPLOYMENT",
    "CLAIM_PROMOTION",
    "FOUNDATION_PROMOTION",
    "INTEGRATION_AUTHORITY",
    "SECRET_ACCESS",
}
PLAN_KEYS = {
    "schema_version",
    "protocol",
    "rollout_id",
    "stage",
    "object_id",
    "state",
    "created_at_utc",
    "claim_ceiling",
    "source",
    "github_observations",
    "source_refs",
    "rollout_policy",
    "rollout_phases",
    "authority_gates",
    "token_continuation",
    "relay",
    "caveats",
}
REF_KEYS = {"role", "path", "bytes", "sha256"}
POLICY_FORBIDS = {
    "execution_enabled": "ROLLOUT_EXECUTION_ENABLED",
    "auto_merge": "ROLLOUT_AUTO_MERGE",
    "auto_main_write": "ROLLOUT_AUTO_MAIN_WRITE",
    "auto_force_push": "ROLLOUT_AUTO_FORCE_PUSH",
    "auto_claim_promotion": "ROLLOUT_AUTO_CLAIM_PROMOTION",
    "auto_foundation_promotion": "ROLLOUT_AUTO_FOUNDATION_PROMOTION",
    "auto_public_release": "ROLLOUT_AUTO_PUBLIC_RELEASE",
    "auto_deployment": "ROLLOUT_AUTO_DEPLOYMENT",
    "self_validation": "ROLLOUT_SELF_VALIDATION",
}
REQUIRED_CAVEATS = {
    "C0_C1_ONLY",
    "PREPARE_ONLY",
    "NO_MERGE_AUTOMATION",
    "NO_CLAIM_PROMOTION",
    "NO_FOUNDATION_PROMOTION",
    "NO_FORCE_PUSH",
    "NO_MAIN_WRITE",
    "NO_SELF_VALIDATION",
    "R2_PR13_SEPARATION_PRESERVED",
}


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


def validate_source(source: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(source, dict):
        return ["ROLLOUT_SOURCE_OBJECT"]
    if source.get("object") != "NEXUS_OMEGA_PR15_ARTIFACT_HANDOFF_ACK_CHAIN":
        errors.append("ROLLOUT_SOURCE_OBJECT_ID")
    if source.get("state") != "PR15_ARTIFACT_HANDOFF_ACK_CHAIN_OBSERVED_C1":
        errors.append("ROLLOUT_SOURCE_STATE")
    if source.get("repository") != "nexusomegac27/NEXUS-OMEGA-EVIDENCE":
        errors.append("ROLLOUT_SOURCE_REPOSITORY")
    if source.get("source_pr") != 15:
        errors.append("ROLLOUT_SOURCE_PR")
    if source.get("source_branch") != PR15_BRANCH:
        errors.append("ROLLOUT_SOURCE_BRANCH")
    if source.get("source_head") != PR15_HEAD or not COMMIT_RE.fullmatch(str(source.get("source_head", ""))):
        errors.append("ROLLOUT_SOURCE_HEAD")
    if source.get("parent") != PR15_PARENT:
        errors.append("ROLLOUT_SOURCE_PARENT")
    if source.get("seed_handoff") != SEED_HANDOFF_ID:
        errors.append("ROLLOUT_SOURCE_SEED_HANDOFF")
    if source.get("repository_structure_version_observed") != "1.3.0":
        errors.append("ROLLOUT_SOURCE_STRUCTURE_VERSION")
    return errors


def validate_github_observations(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["GITHUB_OBSERVATIONS_OBJECT"]
    if value.get("checks") != "ALL_OBSERVED_PASS":
        errors.append("GITHUB_CHECKS_NOT_ALL_PASS")
    if value.get("actions_artifact") != "artifact-handoff-bind-relay-ack":
        errors.append("GITHUB_ACTIONS_ARTIFACT")
    if value.get("actions_artifact_bytes") != 4869:
        errors.append("GITHUB_ACTIONS_ARTIFACT_BYTES")
    if value.get("cursor_action") != "NONE":
        errors.append("GITHUB_CURSOR_ACTION")
    for key in ("actions_run_url", "axiom_comment_url", "cursor_comment_url"):
        if not isinstance(value.get(key), str) or not value[key].startswith("https://github.com/"):
            errors.append(f"GITHUB_{key.upper()}")
    return errors


def validate_source_refs(root: Path, refs: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(refs, list) or not refs:
        return ["SOURCE_REFS"]
    seen_paths: set[str] = set()
    roles: set[str] = set()
    for ref in refs:
        if isinstance(ref, dict):
            path = ref.get("path")
            role = ref.get("role")
            if path in seen_paths:
                errors.append(f"SOURCE_REF_DUPLICATE_PATH:{path}")
            if isinstance(path, str):
                seen_paths.add(path)
            if isinstance(role, str):
                roles.add(role)
        errors.extend(validate_ref(root, ref, "SOURCE"))
        if isinstance(ref, dict) and str(ref.get("role", "")).endswith("LEDGER"):
            ledger_path, path_error = repo_path(root, ref.get("path"))
            if path_error:
                errors.append(f"SOURCE_LEDGER_{path_error}")
            elif ledger_path:
                rows, row_errors = load_jsonl_path(ledger_path)
                errors.extend(f"SOURCE_LEDGER_{err}" for err in row_errors)
                if not rows:
                    errors.append("SOURCE_LEDGER_EMPTY")
    required_roles = {"HANDOFF_ENVELOPE", "BIND_RECEIPT", "RELAY_PACKET", "ACK_RECEIPT", "HANDOFF_WORKFLOW_EVENT_LEDGER"}
    missing = required_roles - roles
    for role in sorted(missing):
        errors.append(f"SOURCE_REF_ROLE_MISSING:{role}")
    return errors


def validate_policy(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["ROLLOUT_POLICY_OBJECT"]
    for key, code in POLICY_FORBIDS.items():
        if value.get(key) is not False:
            errors.append(code)
    if value.get("r2_pr13_separation") != "PRESERVED":
        errors.append("ROLLOUT_R2_PR13_SEPARATION")
    return errors


def validate_phases(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return ["ROLLOUT_PHASES"]
    for phase in value:
        if not isinstance(phase, dict):
            errors.append("ROLLOUT_PHASE_OBJECT")
            continue
        name = phase.get("phase")
        status = phase.get("status")
        if not isinstance(name, str) or not name:
            errors.append("ROLLOUT_PHASE_NAME")
        if phase.get("auto_execute") is not False:
            errors.append(f"ROLLOUT_PHASE_AUTO_EXECUTE:{name}")
        if status not in {"PREPARED", "PENDING_OPERATOR", "BLOCKED_UNTIL_OPERATOR"}:
            errors.append(f"ROLLOUT_PHASE_STATUS:{name}")
        if name == "POST_GATE_EXECUTION" and status != "BLOCKED_UNTIL_OPERATOR":
            errors.append("ROLLOUT_POST_GATE_EXECUTION_NOT_BLOCKED")
        if phase.get("authority_required") is True and status == "PREPARED":
            errors.append(f"ROLLOUT_PHASE_AUTHORITY_BYPASS:{name}")
    return errors


def validate_gates(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return ["AUTHORITY_GATES"]
    for gate in value:
        if not isinstance(gate, dict):
            errors.append("AUTHORITY_GATE_OBJECT")
            continue
        gate_name = gate.get("gate")
        if gate_name not in AUTHORITY_GATES:
            errors.append(f"AUTHORITY_GATE_UNKNOWN:{gate_name}")
        if gate.get("auto_execute") is not False:
            errors.append(f"AUTHORITY_GATE_AUTO_EXECUTE:{gate_name}")
        status = gate.get("status")
        if status not in {"PENDING_OPERATOR", "NOT_REQUESTED"}:
            errors.append(f"AUTHORITY_GATE_STATUS:{gate_name}")
        if status == "CLOSED":
            errors.append(f"AUTHORITY_GATE_CLOSED_WITHOUT_OPERATOR_RECORD:{gate_name}")
        if gate.get("operator_confirmation_required") is True and status != "PENDING_OPERATOR":
            errors.append(f"AUTHORITY_GATE_OPERATOR_STATUS:{gate_name}")
    return errors


def validate_tokens(value: Any, root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["TOKEN_CONTINUATION_OBJECT"]
    if value.get("requested_token_class") not in TOKEN_CLASSES:
        errors.append("TOKEN_REQUESTED_CLASS")
    if not isinstance(value.get("token_class_used"), str) or not value["token_class_used"]:
        errors.append("TOKEN_CLASS_USED")
    if not isinstance(value.get("token_telemetry"), str) or not value["token_telemetry"]:
        errors.append("TOKEN_TELEMETRY")
    if value.get("continuation_required_on_token_pressure") is not True:
        errors.append("TOKEN_PRESSURE_POLICY")
    if not isinstance(value.get("continuation_required"), bool):
        errors.append("CONTINUATION_REQUIRED_BOOL")
    if value.get("continuation_required") is True:
        capsule = value.get("continuation_capsule_path")
        if not isinstance(capsule, str):
            errors.append("CONTINUATION_CAPSULE_MISSING")
        else:
            capsule_path, capsule_error = repo_path(root, capsule)
            if capsule_error or capsule_path is None or not capsule_path.is_file():
                errors.append("CONTINUATION_CAPSULE_MISSING")
    return errors


def validate_relay(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["ROLLOUT_RELAY_OBJECT"]
    if value.get("next_actor") != "OPERATOR_AT_AUTHORITY_GATE":
        errors.append("ROLLOUT_RELAY_NEXT_ACTOR")
    if value.get("cursor_action") != "NONE":
        errors.append("ROLLOUT_RELAY_CURSOR_ACTION")
    if value.get("prepared_artifact") != "artifact-rollout-prep-receipts":
        errors.append("ROLLOUT_RELAY_ARTIFACT")
    return errors


def validate_plan_obj(root: Path, plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(plan) != PLAN_KEYS:
        errors.append("ROLLOUT_KEYSET")
    if plan.get("schema_version") != "1.0.0":
        errors.append("ROLLOUT_SCHEMA_VERSION")
    if plan.get("protocol") != PROTOCOL:
        errors.append("ROLLOUT_PROTOCOL")
    if not isinstance(plan.get("rollout_id"), str) or not ROLLOUT_RE.fullmatch(plan["rollout_id"]):
        errors.append("ROLLOUT_ID")
    if plan.get("stage") != "PREPARE_ONLY":
        errors.append("ROLLOUT_STAGE")
    if plan.get("state") != "PREPARED_SEPARATE_C1":
        errors.append("ROLLOUT_STATE")
    if plan.get("claim_ceiling") not in CLAIM_CEILINGS:
        errors.append("ROLLOUT_CLAIM_CEILING")
    errors.extend(validate_source(plan.get("source")))
    errors.extend(validate_github_observations(plan.get("github_observations")))
    errors.extend(validate_source_refs(root, plan.get("source_refs")))
    errors.extend(validate_policy(plan.get("rollout_policy")))
    errors.extend(validate_phases(plan.get("rollout_phases")))
    errors.extend(validate_gates(plan.get("authority_gates")))
    errors.extend(validate_tokens(plan.get("token_continuation"), root))
    errors.extend(validate_relay(plan.get("relay")))

    caveats = plan.get("caveats")
    if not isinstance(caveats, list) or not all(isinstance(c, str) and c for c in caveats):
        errors.append("ROLLOUT_CAVEATS")
    else:
        missing = REQUIRED_CAVEATS - set(caveats)
        for caveat in sorted(missing):
            errors.append(f"ROLLOUT_CAVEAT_MISSING:{caveat}")

    return sorted(set(errors))


def rollout_paths(root: Path) -> list[Path]:
    plans = root.resolve() / PLANS
    if not plans.exists():
        return []
    return sorted(plans.glob("*/rollout.json"))


def validate_rollout_path(root: Path, path: Path) -> list[str]:
    try:
        plan = load_json_path(path)
    except Exception as exc:
        return [f"ROLLOUT_JSON_INVALID:{path.relative_to(root).as_posix()}:{exc}"]
    errors = validate_plan_obj(root, plan)
    if path.parent.name != plan.get("rollout_id"):
        errors.append("ROLLOUT_ID_PATH_MISMATCH")
    return errors


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    paths = rollout_paths(root)
    if not (root / ROLLOUT_ROOT / "README.md").is_file():
        errors.append("ROLLOUT_ROOT_README_MISSING")
    if not (root / PLANS / SEED_ROLLOUT_ID / "rollout.json").is_file():
        errors.append("ROLLOUT_SEED_MISSING")
    if not paths:
        errors.append("ROLLOUT_PLANS_EMPTY")
    seen_ids: set[str] = set()
    for path in paths:
        try:
            plan = load_json_path(path)
            rollout_id = str(plan.get("rollout_id", path.parent.name))
        except Exception:
            rollout_id = path.parent.name
        if rollout_id in seen_ids:
            errors.append(f"ROLLOUT_DUPLICATE_ID:{rollout_id}")
        seen_ids.add(rollout_id)
        for err in validate_rollout_path(root, path):
            errors.append(f"{rollout_id}:{err}")
    return {
        "object": "NEXUS_OMEGA_ARTIFACT_ROLLOUT_VALIDATION_V1",
        "protocol": PROTOCOL,
        "status": "PASS" if not errors else "FAIL_CLOSED",
        "rollouts": len(paths),
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


def load_plan(root: Path, path: Path) -> dict[str, Any]:
    plan = load_json_path(path)
    errors = validate_plan_obj(root, plan)
    if errors:
        raise ValueError(f"{plan.get('rollout_id', path)} validation errors: {errors}")
    return plan


def generated_receipts(plan: dict[str, Any], plan_sha256: str, generated_at: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    gh = github_context()
    common = {
        "schema_version": "1.0.0",
        "protocol": PROTOCOL,
        "rollout_id": plan["rollout_id"],
        "generated_at_utc": generated_at,
        "claim_ceiling": plan["claim_ceiling"],
        "claim_promotion": False,
        "foundation_promotion": False,
        "integration_authority": "NONE",
        "generation_context": "GITHUB_ACTIONS_WORKFLOW_RECEIPT" if gh else "LOCAL_REPOSITORY_RECEIPT",
        "github_context": gh,
        "source_plan_sha256": plan_sha256,
        "source_pr": plan["source"]["source_pr"],
        "source_head": plan["source"]["source_head"],
        "seed_handoff": plan["source"]["seed_handoff"],
    }
    readiness = {
        **common,
        "receipt_type": "READINESS",
        "decision": "ROLLOUT_PREPARED_C1_NO_EXECUTION",
        "operator_required": True,
        "source_refs": plan["source_refs"],
        "rollout_policy": plan["rollout_policy"],
        "rollout_phases": plan["rollout_phases"],
        "caveats": plan["caveats"],
    }
    gate_packet = {
        **common,
        "receipt_type": "AUTHORITY_GATE_PACKET",
        "decision": "BLOCKED_ON_OPERATOR_AUTHORITY_GATES",
        "operator_required": True,
        "authority_gates": plan["authority_gates"],
        "instruction": "Only the Operator can close pending Authority-Gates. Automated agents may not execute gated actions from this packet.",
    }
    ack = {
        **common,
        "receipt_type": "ACK",
        "decision": "ROLL_OUT_PREP_ACK_ONLY",
        "operator_required": False,
        "ack_state": "SEPARATE_ROLLOUT_PREPARATION_COMPLETE_C1",
        "relay": plan["relay"],
        "token_continuation": plan["token_continuation"],
    }
    events = [
        {"event": "VALIDATE_PASS", "rollout_id": plan["rollout_id"], "ts": generated_at},
        {"event": "READINESS_RECEIPT_CREATED", "rollout_id": plan["rollout_id"], "ts": generated_at},
        {"event": "AUTHORITY_GATE_PACKET_CREATED", "rollout_id": plan["rollout_id"], "ts": generated_at},
        {"event": "ROLL_OUT_ACK_CREATED", "rollout_id": plan["rollout_id"], "ts": generated_at},
    ]
    return readiness, gate_packet, ack, events


def process(root: Path, output: Path, write_repo: bool = False) -> dict[str, Any]:
    root = root.resolve()
    result = validate(root)
    if result["errors"]:
        return result
    base = root / RECEIPTS if write_repo else output.resolve()
    generated_at = now_iso()
    processed = []
    for plan_path in rollout_paths(root):
        plan = load_plan(root, plan_path)
        rollout_id = plan["rollout_id"]
        plan_sha = sha256_file(plan_path)
        readiness, gate_packet, ack, events = generated_receipts(plan, plan_sha, generated_at)
        dump_json(base / rollout_id / "READINESS_RECEIPT.json", readiness)
        dump_json(base / rollout_id / "AUTHORITY_GATE_PACKET.json", gate_packet)
        dump_json(base / rollout_id / "ROLL_OUT_ACK.json", ack)
        dump_jsonl(base / rollout_id / "ROLLOUT_WORKFLOW_EVENTS.jsonl", events)
        processed.append(rollout_id)
    summary = [
        "# Artifact rollout preparation summary",
        "",
        f"Protocol: `{PROTOCOL}`",
        f"Status: `{result['status']}`",
        f"Rollouts processed: `{len(processed)}`",
        "",
    ]
    for rollout_id in processed:
        summary.append(f"- `{rollout_id}`: readiness, authority gate and ack receipts generated")
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
    proc.add_argument("--output", type=Path, default=Path("_artifact_rollout_out"))
    proc.add_argument("--write-repo", action="store_true")
    proc.set_defaults(func=cmd_process)
    return p


def main() -> None:
    ns = parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
