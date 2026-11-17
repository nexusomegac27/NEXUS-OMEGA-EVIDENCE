# R33 — Strict R32 Archive Census, Content-Addressed Pointers and Zero-Duplication Handoff

OBJECT = NEXUS_OMEGA_AXIOM_R33_READ_ONLY_R32_ARCHIVE_ZERO_DUPLICATION_PROTOCOL_20261117_R0
STATE = DESIGN_ONLY_NOT_HOST_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R32_SOURCE_ROOT = UNOBSERVED_BY_AXIOM
R32_ARCHIVE_SOURCE_FREEZE = PENDING_OPERATOR_HOST_SOURCE_CENSUS
R33 = FRESH_SMALL_DELTA_ROOT_ONLY
PRIVATE_RAW_SOURCE = PRESERVE_ONLY_ORIGINAL_PRIVATE_CUSTODY
NO_CROSS_SCOPE_COPY = TRUE

## Rationale

Operator says the R32 project folder is heavily filled with files. Current AXIOM uploads do not constitute a full census of that Windows host directory. No size, total count, freeze SHA or exact Windows root is inferred. A new round should not duplicate an archive or scatter another 40 evidence snapshots through chat transfers.

## Requested Cursor RO census before R33 working execution

R0: Resolve actual canonical R32 directory path on authorized operator Windows machine. Report path type and provenance, without guessing. Keep FOLDER_X and all originals read-only. Determine whether current path contains private sensor material; don't print raw personal/secret data.
R1: Recursively enumerate stable relative paths, bytes, mtime as *metadata*, file type, SHA256, source category; record source roots separately from derivative/transient/temporary files. Never read/execute untrusted scripts or ZIP instructions as commands. If hidden protected file cannot be read, state ACCESS_DENIED.
R2: Identify exact byte duplicate classes by SHA256 and length (not basename, not shared prefix). Mark canonical original per hash and duplicate references. No deletion or de-duplication-on-disk until separately authorized; construct a virtual content-addressed index first.
R3: Check exact freeze consistency: two read-only censuses at two times; if changing files occur, flag NONQUIESCENT and do not claim frozen snapshot. The source directory is not to be overwritten, restructured or cleaned up during this pass.
R4: Preserve all previous R31 A-prime source and Qwen Lean source original hashes. Do not move them into a different path to imply a new author.
R5: Prepare a *small* R32→R33 delta manifest: source_object, original byte digest, archive root and locator, semantic category, governance/privacy status, confidence/provenance, explicit R33 dependency, and whether the new round actually needs a byte copy.
R6: Mark only indispensable NEW R33 sources for copy: source-exact Qwen 7230B Lean file and 379B external log when not accessible via existing verified source path, plus new source contracts and clean replay logs. Everything else via URI/repo path/hash pointer; 0 unnecessary bulk archive transfers.
R7: Versioned handoff: R32 snapshot remains READ_ONLY; create R33 new source tree and append-only source manifest with parent snapshot root/hash once ACTUALLY measured. Branch/pr proposed, no merge. Return one terminal RO census, not 20 tiny Chat receipts.

## Fail closed rules

- If R32 source path is unknown, not mounted, changing or unable to rehash, mark SOURCE_GAP; do not invent an R32 archive hash or finish a closure ceremony.
- SHA256 equality is binary byte identity, not scientific equality; dedupe pointers do not grant any new access rights.
- No semantic deduplication from similar filenames or truncated hashes.
- No empty implementation ZIP may pass: in uploaded R31_OP~1.ZIP its inner design-implementation placeholder is zero bytes, state DESIGN_ONLY_NO_CODE, despite the two valid docs.
- Do not ingest a file from a different trust zone into public GitHub without classification and explicit authorization; private source hash existence can be referenced without publishing private bytes.
- GitHub Merge != Hostinger Deploy != Public WWW Witness; a new R33 repo branch alone is research record only.
- R30 CLOSED preserved and actual older R31 R32=NO historical source flags remain immutable.

## Proposed short R33 return schema

{
 "object": "NEXUS_OMEGA_CURSOR_R33_READ_ONLY_SOURCE_CENSUS_RETURN",
 "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
 "r32_root_observed": false,
 "r32_file_count": null,
 "r32_total_bytes": null,
 "r32_inventory_sha256": null,
 "r32_nonquiescent_files": [],
 "source_exact_qwen_lean_sha256": "70820997285f1bb83d211afbc3cb18f3663790f399d4bce1c506dbd910e5be16",
 "r33_delta_only": true,
 "private_sources_copied_publicly": false,
 "r30": "CLOSED_C1_PRESERVED",
 "pr_merge": false,
 "hostinger_write": false,
 "bodytwin_validated": false
}

This JSON is a TEMPLATE with null/false placeholders, not a completed Windows census. Replace only with actually witnessed values in authorized run.

NEXT = ONE_OPERATORKNOWN_R32_READ_ONLY_CENSUS_THEN_DELTA_ARCHIVE_INDEX
