"""Frozen independent synthetic oracle for C1 tree-correction resolution.

This test file is to be committed BEFORE the candidate implementation.
The fixtures and expected outcomes are independent of candidate internals.
"""
import copy
import hashlib
import importlib.util
import json
import sys

COMMIT = "1" * 40
TREE = "2" * 40
OLD = "1" * 40
MCOMMIT = "3" * 40
PATH = "research/r16/alpha/manifest.json"
MAIN = "4" * 40


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def fixture():
    manifest = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY", "pinned_main": MAIN,
                "pinned_source_head": COMMIT, "pinned_source_tree": OLD,
                "count": 2, "files": [{"path": "research/r16/alpha/a.py"},
                                      {"path": "research/r16/alpha/b.py"}]}
    raw = encoded(manifest)
    correction = {"correction_type": "APPEND_ONLY_SINGLE_FIELD_TREE_IDENTITY",
                  "field": "pinned_source_tree", "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
                  "pinned_main": MAIN,
                  "supersedes": {"commit": MCOMMIT, "path": PATH, "bytes": len(raw),
                                 "sha256": hashlib.sha256(raw).hexdigest(),
                                 "git_blob_sha1": blob(raw)},
                  "old_value": OLD, "new_value": TREE, "source_commit": COMMIT}
    return manifest, correction


def bind_raw(mr, c):
    c = copy.deepcopy(c)
    c["supersedes"]["bytes"] = len(mr)
    c["supersedes"]["sha256"] = hashlib.sha256(mr).hexdigest()
    c["supersedes"]["git_blob_sha1"] = blob(mr)
    return mr, encoded(c)


def check(module):
    failures = []
    labels = []
    def run(name, mutate=None, accepted=False, reason=None):
        m, c = fixture()
        kw = dict(manifest_commit=MCOMMIT, manifest_path=PATH,
                  observed_commit=COMMIT, observed_tree=TREE)
        mr, cr = encoded(m), encoded(c)
        if mutate:
            mr, cr, kw = mutate(m, c, mr, cr, kw)
        mr_before = mr
        cr_before = cr
        try:
            result = module.resolve_tree_identity(mr, cr, **kw)
            ok = (result.get("status") == ("RESOLVED_C1" if accepted else "INCOMPLETE"))
            if accepted:
                ok &= result.get("effective", {}).get("pinned_source_tree") == TREE
                ok &= result.get("effective", {}).get("count") == 2
                ok &= result.get("source_sha256") == hashlib.sha256(mr).hexdigest()
            if reason is not None and not accepted:
                ok &= result.get("reason") == reason
            ok &= mr == mr_before and cr == cr_before
        except Exception:
            ok = False
        labels.append(name)
        if not ok:
            failures.append(name)
    run("positive_valid_correction", accepted=True)
    run("tampered_manifest", lambda m,c,mr,cr,k: (mr.replace(b'"count":2',b'"count":3'),cr,k), reason="SOURCE_SHA256_MISMATCH")
    run("wrong_supersedes_size", lambda m,c,mr,cr,k: (mr,encoded({**c,"supersedes":{**c["supersedes"],"bytes":1}}),k))
    run("wrong_supersedes_sha256", lambda m,c,mr,cr,k: (mr,encoded({**c,"supersedes":{**c["supersedes"],"sha256":"0"*64}}),k))
    run("wrong_supersedes_blob", lambda m,c,mr,cr,k: (mr,encoded({**c,"supersedes":{**c["supersedes"],"git_blob_sha1":"0"*40}}),k))
    run("wrong_manifest_commit", lambda m,c,mr,cr,k: (mr,cr,{**k,"manifest_commit":"5"*40}))
    run("wrong_manifest_path", lambda m,c,mr,cr,k: (mr,cr,{**k,"manifest_path":"research/r16/alpha/other.json"}))
    run("changed_git_commit", lambda m,c,mr,cr,k: (mr,cr,{**k,"observed_commit":"5"*40}))
    run("changed_git_tree", lambda m,c,mr,cr,k: (mr,cr,{**k,"observed_tree":"5"*40}))
    run("wrong_old_tree", lambda m,c,mr,cr,k: (mr,encoded({**c,"old_value":"5"*40}),k))
    run("wrong_field", lambda m,c,mr,cr,k: (mr,encoded({**c,"field":"count"}),k))
    run("claim_promotion", lambda m,c,mr,cr,k: (mr,encoded({**c,"claim_ceiling":"C2"}),k))
    run("wrong_main", lambda m,c,mr,cr,k: (mr,encoded({**c,"pinned_main":"5"*40}),k))
    run("duplicate_manifest_key", lambda m,c,mr,cr,k: (*bind_raw(mr.replace(b'{',b'{"count":2,',1),c),k))
    run("duplicate_correction_key", lambda m,c,mr,cr,k: (mr,cr.replace(b'{',b'{"field":"count",',1),k))
    run("nonfinite_json", lambda m,c,mr,cr,k: (*bind_raw(mr.replace(b'"count":2',b'"count":NaN'),c),k))
    run("invalid_unicode_surrogate", lambda m,c,mr,cr,k: (*bind_raw(mr.replace(b'"count":2',b'"bad":"\\ud800","count":2'),c),k))
    run("duplicate_file_path", lambda m,c,mr,cr,k: (*bind_raw(encoded({**m,"files":[m["files"][0],m["files"][0]]}),c),k), reason="SOURCE_INVENTORY_DUPLICATE")
    run("missing_file", lambda m,c,mr,cr,k: (*bind_raw(encoded({**m,"files":[m["files"][0]]}),c),k), reason="SOURCE_INVENTORY_INCOMPLETE")
    run("malformed_json", lambda m,c,mr,cr,k: (b'{',cr,k))
    run("nonbytes_source", lambda m,c,mr,cr,k: ("not bytes",cr,k), reason="SOURCE_BYTES_REQUIRED")
    return {"total":len(labels),"passed":len(labels)-len(failures),"failed":failures,"labels":labels}


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = check(module)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if not result["failed"] else 1)
