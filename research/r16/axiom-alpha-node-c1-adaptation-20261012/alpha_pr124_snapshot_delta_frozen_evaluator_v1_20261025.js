/** Frozen independent C1 PR124 snapshot coverage evaluator.
 * Usage: node evaluator.js BASE.json DELTA.json PR_FILES.json EXPECTED_HEAD
 * This checks snapshot row/path/blob coverage, NOT file-byte authenticity.
 * Producer must separately rehash bytes and read Git blobs. No network/write.
 */
"use strict";
function audit(base, delta, prFiles, expectedHead) {
  const errors = [];
  const validHex = (s, n) => typeof s === "string" && new RegExp("^[0-9a-f]{" + n + "}$").test(s);
  if (!base || !Array.isArray(base.files) || base.count !== base.files.length) errors.push("BASE_SHAPE");
  if (!delta || !Array.isArray(delta.files) || delta.count !== delta.files.length) errors.push("DELTA_SHAPE");
  if (!Array.isArray(prFiles)) errors.push("PR_FILE_LIST_SHAPE");
  if (!validHex(expectedHead, 40) || delta?.pinned_pr_head !== expectedHead) errors.push("HEAD_MISMATCH");
  if (errors.length) return {status:"FAIL_CLOSED", errors};
  const rows = [...base.files, ...delta.files];
  const actual = new Map(), bound = new Set();
  for (const f of prFiles) {
    if (typeof f.filename !== "string" || !validHex(f.sha, 40) || actual.has(f.filename)) errors.push("PR_FILE_INVALID_OR_DUPLICATE");
    else actual.set(f.filename, f.sha);
  }
  for (const row of rows) {
    if (typeof row.path !== "string" || bound.has(row.path)) errors.push("BINDING_PATH_DUPLICATE_OR_INVALID");
    else bound.add(row.path);
    if (!Number.isSafeInteger(row.bytes) || row.bytes < 0 || !validHex(row.sha256, 64) || !validHex(row.git_blob_sha1, 40)) errors.push("BINDING_METADATA_INVALID");
    if (!actual.has(row.path)) errors.push("BOUND_PATH_NOT_IN_PR");
    else if (actual.get(row.path) !== row.git_blob_sha1) errors.push("GIT_BLOB_MISMATCH");
  }
  for (const path of actual.keys()) if (!bound.has(path)) errors.push("UNBOUND_PR_PATH");
  return {status:errors.length?"FAIL_CLOSED":"PASS_C1_SNAPSHOT", errors:[...new Set(errors)].sort(),
    base_count:base.files.length, delta_count:delta.files.length, pr_count:prFiles.length,
    covered_count:rows.filter(x=>actual.get(x.path)===x.git_blob_sha1).length};
}
if (typeof module !== "undefined") {
  module.exports = {audit};
  if (require.main === module) {
    const fs = require("fs");
    if (process.argv.length !== 6) {console.error("Usage: evaluator BASE DELTA PR_FILES EXPECTED_HEAD");process.exit(2);}
    const [base,delta,prFiles] = process.argv.slice(2,5).map(p=>JSON.parse(fs.readFileSync(p,"utf8")));
    const result=audit(base,delta,prFiles,process.argv[5]);
    process.stdout.write(JSON.stringify(result)+"\n");
    process.exit(result.status==="PASS_C1_SNAPSHOT"?0:1);
  }
}
