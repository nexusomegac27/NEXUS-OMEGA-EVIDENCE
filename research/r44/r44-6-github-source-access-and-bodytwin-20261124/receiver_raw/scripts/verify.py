#!/usr/bin/env python3
"""R44-6 SOURCE_RECEIVER_PREFLIGHT — ZIP verification + registry public-source rehash.

Verification scope (receiver lane only, no experiment start):
  1. Sidecar content vs claimed ZIP SHA-256
  2. ZIP size + SHA-256 vs claims (Issue #441 / sidecar / attachment)
  3. Safe-archive inspection before unpack (traversal, absolute, symlink, dup, expansion)
  4. ZIP CRC + per-member SHA-256
  5. ZIP members vs repo bytes (fetched at pinned commit) byte equality
  6. Internal manifest 99_SHA256SUMS.txt coverage (7 content files)
  7. 13 public_exact registry sources rehash from their pinned refs
Output: machine receipt JSON + compact stdout summary.
"""
import hashlib, io, json, os, urllib.request, urllib.error, zipfile, datetime

BASE   = "/home/z/my-project/scripts/r44_6_preflight/fetched"
ORDER  = os.path.join(BASE, "order")
OUTJSON = "/home/z/my-project/scripts/r44_6_preflight/r44_6_preflight_machine_receipt_raw.json"
COMMIT = "89ccff827d564309cba3274bff94a6d577e6853a"
OWNER, REPO = "nexusomegac27", "NEXUS-OMEGA-EVIDENCE"
SUBDIR = "research/r44/r44-6-github-source-access-and-bodytwin-20261124"

CLAIM = {
    "zip_bytes": 43449,
    "zip_sha256": "cf10b2bc1a3284eb1858b36724b444603b526b8ba4878063dc60820f427f660a",
    "manifest_sha256": "97410f2598c93837c94b11b5bc83638dee81a732360447a8b4c8f751f77710f1",
}

def sha_b(b): return hashlib.sha256(b).hexdigest()

def read_b(p):
    with open(p, "rb") as f: return f.read()

rec = {
    "schema": "nexus/r44-6/receiver-preflight/v1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "actor": {
        "github_login": OWNER,
        "role": "OFF_CHAIN_UNREGISTERED_ADVISORY_RECEIVER",
        "registration_state": "UNREGISTERED_ADVISORY_C1",
        "n_eff": 1,
        "same_writer_caveat": "GitHub writes and readbacks run under the operator-owned account nexusomegac27; this receiver round is advisory off-chain, NOT an independent external receiver ACK, NOT EXPERT_ACK, no quorum credit.",
        "expert_ack": False,
        "quorum_credit": False,
    },
    "lane": "receiver_preflight_only_no_lane_start",
    "order_commit": COMMIT,
    "tool_capability": {"terminal": True, "curl": True, "python3": True, "sha256": True,
                        "network_egress": "raw.githubusercontent.com reachable, HTTP 200"},
    "results": {},
}

# --- 1 sidecar ---
side = read_b(os.path.join(ORDER, "R44_6_EXPERT_ORDER_R0.zip.sha256"))
side_sha = side.split()[0].decode()
side_name = side.split()[1].decode()
rec["results"]["sidecar"] = {
    "bytes": len(side), "sha256_of_sidecar_file": sha_b(side),
    "declared_zip_sha256": side_sha, "declared_zip_name": side_name,
    "matches_claim": side_sha == CLAIM["zip_sha256"] and side_name == "R44_6_EXPERT_ORDER_R0.zip",
}

# --- 2 zip size/sha ---
zpath = os.path.join(ORDER, "R44_6_EXPERT_ORDER_R0.zip")
zb = read_b(zpath)
rec["results"]["zip"] = {
    "bytes": len(zb), "bytes_match": len(zb) == CLAIM["zip_bytes"],
    "sha256": sha_b(zb), "sha256_match": sha_b(zb) == CLAIM["zip_sha256"],
}

# --- 3/4 safe inspection, CRC, members ---
zf = zipfile.ZipFile(io.BytesIO(zb))
infos = zf.infolist()
names = [i.filename for i in infos]
safety = {
    "member_count": len(names),
    "duplicates": sorted({n for n in names if names.count(n) > 1}),
    "absolute_paths": [n for n in names if n.startswith("/")],
    "traversal": [n for n in names if ".." in n.split("/")],
    "backslash": [n for n in names if "\\" in n],
    "symlinks": [i.filename for i in infos if ((i.external_attr >> 16) & 0o170000) == 0o120000],
    "total_uncompressed_bytes": sum(i.file_size for i in infos),
}
safety["safe"] = not (safety["duplicates"] or safety["absolute_paths"] or safety["traversal"] or safety["backslash"] or safety["symlinks"])
bad = zf.testzip()
members = {i.filename: {"bytes": i.file_size, "sha256": sha_b(zf.read(i.filename))} for i in infos}
rec["results"]["zip_safety"] = safety
rec["results"]["zip_crc"] = {"testzip": bad, "all_crc_pass": bad is None}
rec["results"]["zip_members"] = members

# --- 5/6 repo bytes vs members vs manifest ---
repo_files = {}
for n in sorted(os.listdir(ORDER)):
    b = read_b(os.path.join(ORDER, n))
    repo_files[n] = {"bytes": len(b), "sha256": sha_b(b)}

manifest_b = read_b(os.path.join(ORDER, "99_SHA256SUMS.txt"))
manifest = {}
for line in manifest_b.decode().strip().splitlines():
    h, _, fn = line.partition("  ")
    manifest[fn.strip()] = h.strip()

file_readback = []
for fn, mh in sorted(manifest.items()):
    repo = repo_files.get(fn)
    mem = members.get(fn)
    ok_repo = bool(repo) and repo["sha256"] == mh
    ok_mem = bool(mem) and mem["sha256"] == mh
    ok_eq  = bool(repo) and bool(mem) and repo["sha256"] == mem["sha256"]
    file_readback.append({"file": fn, "manifest_sha": mh, "repo_match": ok_repo,
                          "zip_member_match": ok_mem, "repo_vs_zip_byte_equal": ok_eq})
manifest_in_zip = members.get("99_SHA256SUMS.txt")
rec["results"]["manifest"] = {
    "manifest_bytes": len(manifest_b),
    "manifest_sha256": sha_b(manifest_b),
    "manifest_sha256_matches_claim": sha_b(manifest_b) == CLAIM["manifest_sha256"],
    "entries": len(manifest),
    "file_readback_7": file_readback,
    "manifest_in_zip_present": manifest_in_zip is not None,
    "manifest_repo_vs_zip_byte_equal": bool(manifest_in_zip) and manifest_in_zip["sha256"] == sha_b(manifest_b),
}
rec["results"]["repo_files"] = repo_files

# --- 7 registry public_exact rehash ---
reg = json.loads(read_b(os.path.join(ORDER, "02_SOURCE_REGISTRY.json")))
src_receipts = []
n_match = 0
for s in reg.get("public_exact", []):
    entry = {"source_id": s["id"], "ref": s["ref"], "path": s["path"],
             "route": "raw.githubusercontent pinned commit", "url": s["raw_url"],
             "expected_bytes": s["bytes"], "expected_sha256": s["sha256"],
             "access_class": "public_exact", "license": "UNKNOWN", "privacy": "PUBLIC_REPO_FILE"}
    try:
        req = urllib.request.Request(s["raw_url"], headers={"User-Agent": "nexus-omega-receiver-preflight/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read(); status = r.status
        entry.update({"http_status": status, "actual_bytes": len(b), "computed_sha256": sha_b(b),
                      "bytes_match": len(b) == s["bytes"], "sha256_match": sha_b(b) == s["sha256"]})
        entry["result"] = "MATCH" if (entry["bytes_match"] and entry["sha256_match"]) else "MISMATCH"
    except urllib.error.HTTPError as e:
        entry.update({"http_status": e.code, "error": str(e), "result": f"HTTP_{e.code}"})
    except Exception as e:
        entry.update({"error": repr(e), "result": "FETCH_ERROR"})
    if entry.get("result") == "MATCH": n_match += 1
    src_receipts.append(entry)

pending = reg.get("pending_or_restricted", [])
rec["results"]["registry_public_rehash"] = {
    "public_exact_total": len(reg.get("public_exact", [])),
    "match": n_match,
    "receipts": src_receipts,
    "pending_or_restricted_ids": [p["id"] for p in pending],
    "pending_count": len(pending),
}

# --- verdict summary ---
r = rec["results"]
rec["verdict"] = {
    "zip_bytes_sha256_sidecar": "MATCH" if (r["zip"]["bytes_match"] and r["zip"]["sha256_match"] and r["sidecar"]["matches_claim"]) else "MISMATCH",
    "manifest_sha256": "MATCH" if r["manifest"]["manifest_sha256_matches_claim"] else "MISMATCH",
    "manifest_file_readback": f"{sum(1 for x in file_readback if x['repo_match'] and x['zip_member_match'] and x['repo_vs_zip_byte_equal'])}/{len(file_readback)}_MATCH",
    "zip_crc": "PASS" if r["zip_crc"]["all_crc_pass"] else "FAIL",
    "zip_members": f"{len(names)}_MEMBERS_SAFE" if safety["safe"] else "UNSAFE_REJECT",
    "registry_public_rehash": f"{n_match}/{len(reg.get('public_exact', []))}_MATCH",
}
with open(OUTJSON, "w", encoding="utf-8") as f:
    json.dump(rec, f, indent=2, ensure_ascii=False)

print(json.dumps(rec["verdict"], indent=2))
print("\nmember list:")
for n, m in members.items():
    print(f"  {m['bytes']:>7} B  {m['sha256'][:16]}…  {n}")
print("\nreadback:")
for x in file_readback:
    print(f"  repo={x['repo_match']} zip={x['zip_member_match']} eq={x['repo_vs_zip_byte_equal']}  {x['file']}")
print("\nregistry sources:")
for s in src_receipts:
    print(f"  {s['result']:<10} {s.get('actual_bytes', '-')!s:>9} B  {s['source_id']}")
print(f"\nmachine receipt -> {OUTJSON}")
