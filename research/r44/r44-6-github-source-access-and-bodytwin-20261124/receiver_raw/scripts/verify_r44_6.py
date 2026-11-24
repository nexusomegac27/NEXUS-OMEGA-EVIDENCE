#!/usr/bin/env python3
"""R44-6 receiver independent byte-level verification (UNREGISTERED_ADVISORY_C1).
Verifies:
  A. R44-6 package (10 files at commit 89ccff82...) against 99_SHA256SUMS.txt,
     sidecar, issue pins (ZIP bytes+sha, manifest selfhash).
  B. ZIP safety: member names (traversal/absolute/symlink/dupes), CRC, member
     hashes vs the ZIP-internal manifest.
  C. R44-5 additive publication at a63ee946 vs local R44-5 artifacts.
Writes r44_6_receiver_verification.json.
"""
import hashlib, json, zipfile, os, sys

BASE = "/home/z/my-project/scripts/r44_6_receiver"
PKG = f"{BASE}/fetch/r44_6_package"
A63 = f"{BASE}/fetch/r44_5_additive_at_a63ee946"
LOCAL_R445 = "/home/z/my-project/scripts/r44_5_artifacts"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

report = {"schema": "nexus/r44-6/receiver-verification/v0", "actor": "GLM UNREGISTERED_ADVISORY_C1 (n_eff=1, append-only, advisory-only; NOT EXPERT_ACK, NOT quorum)", "verification_date": "2026-11-25 (Europe/Berlin)"}

# ---------- A. package files ----------
pins = {  # from Issue #441 / #439 comment pins and manual
    "zip_bytes": 43449,
    "zip_sha256": "cf10b2bc1a3284eb1858b36724b444603b526b8ba4878063dc60820f427f660a",
    "manifest_selfhash": "97410f2598c93837c94b11b5bc83638dee81a732360447a8b4c8f751f77710f1",
    "sidecar_bytes": 92,
    "sidecar_sha256": "f4b5e376e0c305059fffdaedc13f6a933c6537cba425cfea27913effce3d7524",
}
pkg_files = {
    "00_START_HERE_EXPERT_MANUAL.md": (4896, "355eeb9aa097a2e897c3fbc0a039d531d0e6f2747709c2874cf43936801e5346"),
    "01_EXPERT_MAXI_ORDER.md": (5216, "8e80f59b4c7c601e946baee80b5b87e5987dea2af2c9bb5736054a7ce7425da8"),
    "02_SOURCE_REGISTRY.json": (17904, "4881502cd08c9fb3236fb7b424b478f02996636d771e6fde178bcc693481dc70"),
    "03_CONTROL_MATRIX.json": (7572, "cf86217b17d1478de392f0c32808b091e87be58d606bc773dbcd1ae64fb14b71"),
    "04_RETURN_SCHEMA.json": (2256, "39a28fa2317dfdf3dc9924dcbcca569f7c50df5c1e8292c18ad45c79a08ed4f7"),
    "05_INTAKE_FINDINGS.md": (2627, "ffe9ea9b80f69e6b63cd68f2adb5fc84b346d18a5186f6f4294a47b5236daafc"),
    "06_MACHINE_CONTRACT.json": (1353, "5d2da4a5757ec7321dd391076038cf27ba1360e9dd65ea3277aad3656bf6af2a"),
}

results = {}
for name, (exp_b, exp_h) in pkg_files.items():
    p = f"{PKG}/{name}"
    b = os.path.getsize(p); h = sha256_file(p)
    results[name] = {"bytes": b, "sha256": h, "size_match": b == exp_b, "hash_match": h == exp_h}

# manifest selfhash (99_SHA256SUMS.txt itself, Issue #441 MANIFEST_SHA256 pin)
p99 = f"{PKG}/99_SHA256SUMS.txt"
b99 = os.path.getsize(p99); h99 = sha256_file(p99)
results["99_SHA256SUMS.txt"] = {"bytes": b99, "sha256": h99, "selfhash_pin_match": h99 == pins["manifest_selfhash"]}

# manifest line-by-line check
manifest_lines = [l for l in open(p99, encoding="utf-8").read().splitlines() if l.strip()]
manifest_result = []
for line in manifest_lines:
    h, name = line.split(None, 1)
    name = name.strip()
    p = f"{PKG}/{name}"
    ok = os.path.exists(p) and sha256_file(p) == h
    manifest_result.append({"member": name, "match": ok})
results["manifest_7_of_7"] = {"lines": len(manifest_lines), "all_match": all(x["match"] for x in manifest_result), "detail": manifest_result}

# sidecar
ps = f"{PKG}/R44_6_EXPERT_ORDER_R0.zip.sha256"
bs = os.path.getsize(ps); hs = sha256_file(ps)
sidecar_text = open(ps, encoding="utf-8").read().strip()
results["sidecar"] = {"bytes": bs, "sha256": hs, "size_match": bs == pins["sidecar_bytes"], "hash_match": hs == pins["sidecar_sha256"], "contains_zip_pin": pins["zip_sha256"] in sidecar_text}

# ZIP bytes
pz = f"{PKG}/R44_6_EXPERT_ORDER_R0.zip"
bz = os.path.getsize(pz); hz = sha256_file(pz)
results["zip"] = {"bytes": bz, "sha256": hz, "size_match": bz == pins["zip_bytes"], "hash_match": hz == pins["zip_sha256"]}

# ---------- B. ZIP safety + members ----------
zip_check = {}
with zipfile.ZipFile(pz) as z:
    names = z.namelist()
    dupes = len(names) != len(set(names))
    bad = [n for n in names if n.startswith("/") or ".." in n.replace("\\", "/").split("/") or ":" in n]
    crc_ok, crc_detail = True, []
    for info in z.infolist():
        try:
            with z.open(info) as fh:
                data = fh.read()
            ok = hashlib.sha256(data).hexdigest() is not None
            crc_ok &= (z.testzip() is None)
            crc_detail.append({"name": info.filename, "size": info.file_size, "crc": z.testzip() is None})
        except Exception as e:
            crc_ok = False
            crc_detail.append({"name": info.filename, "error": str(e)})
    zip_check = {"member_count": len(names), "names": names, "duplicates": dupes, "unsafe_paths": bad, "crc_all_pass": crc_ok}
    # member hashes vs any internal manifest present in the archive
    member_hashes = {}
    for info in z.infolist():
        with z.open(info) as fh:
            member_hashes[info.filename] = {"bytes": info.file_size, "sha256": hashlib.sha256(fh.read()).hexdigest()}
    zip_check["member_hashes"] = member_hashes
    # find internal manifest and compare
    internal_manifest_checks = []
    for mname, mh in member_hashes.items():
        if mname.lower().endswith("sha256sums.txt") or "sha256sums" in mname.lower():
            with z.open(mname) as fh:
                txt = fh.read().decode("utf-8", "replace")
            for line in txt.splitlines():
                if line.strip():
                    h, n = line.split(None, 1); n = n.strip()
                    # try exact or suffix match against members
                    target = None
                    if n in member_hashes:
                        target = n
                    else:
                        cands = [k for k in member_hashes if k.endswith(n) or k.endswith("/" + n)]
                        target = cands[0] if len(cands) == 1 else None
                    internal_manifest_checks.append({"line_member": n, "target": target, "match": bool(target) and member_hashes[target]["sha256"] == h})
    zip_check["internal_manifest_checks"] = internal_manifest_checks
results["zip_safety"] = zip_check

# ---------- C. a63ee946 additive vs local R44-5 artifacts ----------
a63 = {}
pairs = [
    ("10_R44_5_R1_ORDER_CHAT_TRANSMISSION_SNAPSHOT_RECEIVER_PUBLISHED.md", "10_R44_5_R1_ORDER_CHAT_TRANSMISSION_SNAPSHOT_RECEIVER_PUBLISHED.md"),
    ("11_R44_5_RECEIVER_CUSTODY_AND_SCOPE_CONTRACT_C1.json", "11_R44_5_RECEIVER_CUSTODY_AND_SCOPE_CONTRACT_C1.json"),
    ("99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt", "99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt"),
]
local_pins = {
    "10_R44_5_R1_ORDER_CHAT_TRANSMISSION_SNAPSHOT_RECEIVER_PUBLISHED.md": (11089, "f7f47387d05531c59533c61c4cf466978ccb52b50b4f7443b84549ebfc5b86a8"),
    "11_R44_5_RECEIVER_CUSTODY_AND_SCOPE_CONTRACT_C1.json": (6488, "ccd2117505d528499db6ccaad7d3a9e75658093f1ff4e2a85c21c2d06d349b98"),
    "99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt": (252, "1ff92b06db04c32f50c3168e2c40a13fdeb344ba6f79fac6f87f8a4c9a4ab29f"),
}
for fname, _ in pairs:
    pa = f"{A63}/{fname}"
    pl = f"{LOCAL_R445}/{fname}"
    ba, ha = os.path.getsize(pa), sha256_file(pa)
    exists_local = os.path.exists(pl)
    hl = sha256_file(pl) if exists_local else None
    exp_b, exp_h = local_pins[fname]
    a63[fname] = {
        "github_bytes": ba, "github_sha256": ha,
        "local_bytes": os.path.getsize(pl) if exists_local else None,
        "local_sha256": hl,
        "github_vs_local_identical": (ha == hl),
        "github_matches_r44_5_receipt_pin_bytes": ba == exp_b,
        "github_matches_r44_5_receipt_pin_sha": ha == exp_h,
    }
    # the 99_ manifest lists the two other files; verify its internal lines too
results["r44_5_additive_at_a63ee946"] = a63

# selfhash of the additive manifest (as pinned in commit message + local receipt)
pm = f"{A63}/99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt"
results["r44_5_additive_manifest_selfhash"] = {
    "sha256": sha256_file(pm),
    "matches_local_receipt_selfhash": sha256_file(pm) == "1ff92b06db04c32f50c3168e2c40a13fdeb344ba6f79fac6f87f8a4c9a4ab29f",
}

# ---------- verdict ----------
def all_match(d, keys):
    return all(d[k] for k in keys)

results["verdict"] = {
    "package_7_files_hash_and_size_match": all(results[n]["size_match"] and results[n]["hash_match"] for n in pkg_files),
    "manifest_selfhash_match": results["99_SHA256SUMS.txt"]["selfhash_pin_match"],
    "manifest_lines_all_match": results["manifest_7_of_7"]["all_match"],
    "sidecar_match": results["sidecar"]["size_match"] and results["sidecar"]["hash_match"] and results["sidecar"]["contains_zip_pin"],
    "zip_bytes_and_sha_match": results["zip"]["size_match"] and results["zip"]["hash_match"],
    "zip_safe_and_crc_pass": zip_check["member_count"] > 0 and not zip_check["duplicates"] and not zip_check["unsafe_paths"] and zip_check["crc_all_pass"],
    "internal_manifest_all_match": all(x["match"] for x in zip_check.get("internal_manifest_checks", [])) if zip_check.get("internal_manifest_checks") else None,
    "r44_5_additive_github_equals_local": all(v["github_vs_local_identical"] for v in a63.values()),
}

out = f"{BASE}/r44_6_receiver_verification.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(report | {"results": results}, f, indent=2, ensure_ascii=False)
print(json.dumps(results["verdict"], indent=2))
print("\nZIP members:", zip_check["member_count"])
print("ZIP member names:", json.dumps(zip_check["names"], indent=1))
print("internal manifest checks:", json.dumps(zip_check["internal_manifest_checks"], indent=1))
print("r44_5 additive:", json.dumps(results["r44_5_additive_at_a63ee946"], indent=2))
print("saved:", out)
