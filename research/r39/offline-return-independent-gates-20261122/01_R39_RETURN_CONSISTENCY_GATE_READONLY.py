#!/usr/bin/env python3
"""Read-only, strict R39 Cursor return validator. No device actions, no extraction.

Used on original uploaded R39 4,800-byte Cursor return. A PASS here is
archive/manifest integrity ONLY: X13-R1 source and per-test logs are absent.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_GITHUB_COMMENT_ID = "7081290152"
MAX_TOTAL = 1_000_000


def digest(b):
    return hashlib.sha256(b).hexdigest()


def parse_json_strict(b):
    def pairs_unique(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError("duplicate_json_key:" + k)
            d[k] = v
        return d
    return json.loads(b.decode("utf-8"), object_pairs_hook=pairs_unique,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError("nonfinite:" + s)))


def check(path):
    outcome = {"object": "R39_CURSOR_OFFLINE_SOURCE_CONSISTENCY_VALIDATOR_V1",
               "input_zip_bytes": path.stat().st_size,
               "input_sha256": digest(path.read_bytes()),
               "archive_integrity": "NOT_CHECKED",
               "manifest_integrity": "NOT_CHECKED", "machine_total": None,
               "errors": [], "warnings": [], "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
               "source_replay": "NOT_ESTABLISHED", "physical_run": False,
               "bodytwin_validated": False}
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        if len(names) > 20 or len(names) != len(set(names)) or any(i.file_size > MAX_TOTAL for i in infos):
            raise ValueError("unsafe_zip_metadata")
        if any(n.startswith("/") or ".." in n.split("/") for n in names):
            raise ValueError("unsafe_zip_path")
        if z.testzip() is not None:
            raise ValueError("zip_crc_failure")
        outcome["archive_integrity"] = "PASS_CRC"
        required = {"00_EXECUTIVE.txt", "01_HANDSHAKE.txt", "02_EPISTEMIC_WALLS.txt",
                    "03_RESULT.txt", "04_MACHINE.json", "SHA256SUMS.txt"}
        if set(names) != required:
            outcome["errors"].append("ZIP_SOURCE_SET_MISMATCH")
        m = z.read("SHA256SUMS.txt").decode("utf-8")
        matches = 0
        for line in m.splitlines():
            parts = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
            if parts is None:
                outcome["errors"].append("MALFORMED_SHA256SUMS")
                continue
            want, name = parts.groups()
            if name not in required - {"SHA256SUMS.txt"} or name not in names:
                outcome["errors"].append("INVALID_MANIFEST_FILE:" + name)
                continue
            if digest(z.read(name)) == want:
                matches += 1
            else:
                outcome["errors"].append("HASH_MISMATCH:" + name)
        outcome["manifest_integrity"] = f"MATCH_{matches}_OF_5"
        if matches != 5:
            outcome["errors"].append("MANIFEST_INTEGRITY_FAILURE")
        machine = parse_json_strict(z.read("04_MACHINE.json"))
        ex = z.read("00_EXECUTIVE.txt").decode("utf-8")
        res = z.read("03_RESULT.txt").decode("utf-8")
        by = machine.get("offline_suite", {}).get("by_status", {})
        passed, gap = by.get("PASSED_EXPECTED"), by.get("SOURCE_GAP")
        total = machine.get("offline_suite", {}).get("total")
        outcome["machine_total"] = total
        outcome["machine_status_counts"] = by
        if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in [passed, gap, total]):
            outcome["errors"].append("INVALID_MACHINE_COUNT")
        elif passed + gap != total:
            outcome["errors"].append("INVALID_MACHINE_DENOMINATOR")
        if not re.search(r"PASSED_EXPECTED\s*=\s*" + str(passed) + r"(?:\s|$)", ex):
            outcome["errors"].append("EXECUTIVE_VS_MACHINE_COUNT_CONFLICT")
        if not re.search(r"PASSED_EXPECTED_N\s*=\s*" + str(passed) + r"(?:\s|$)", res):
            outcome["errors"].append("RESULT_VS_MACHINE_COUNT_CONFLICT")
        if gap:
            outcome["warnings"].append("OPEN_SOURCE_GAPS:" + str(gap))
        if ("COMMENT_ID=" + EXPECTED_GITHUB_COMMENT_ID) not in ex:
            outcome["errors"].append("AUTHORITY_COMMENT_ID_NOT_GITHUB_SOURCE_EXACT")
        if "7081290152" in machine.get("thaw_comment_file", {}).get("name", ""):
            outcome["warnings"].append("ONDISK_COMMENT_NAME_ALIGNS_WITH_GITHUB_API")
        outcome["warnings"].append("X13_R1_SOURCE_AND_65_CASE_RESULTS_NOT_INCLUDED")
        outcome["warnings"].append("CURSOR_EXIT_ZERO_REPORTED_SEPARATELY_NOT_BYTE_BOUND")
    outcome["aggregate_status"] = ("PASS_ARCHIVE_ONLY" if not outcome["errors"] else
                                   "PASS_ARCHIVE_WITH_MATERIAL_INTERNAL_CONTRADICTIONS")
    return outcome


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source_zip", type=Path)
    a = p.parse_args()
    print(json.dumps(check(a.source_zip), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
