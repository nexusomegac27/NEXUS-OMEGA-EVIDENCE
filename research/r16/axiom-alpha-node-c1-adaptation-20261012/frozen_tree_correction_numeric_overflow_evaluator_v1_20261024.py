"""Independent frozen oracle: reject JSON numeric overflow in a tree correction.

Fix the oracle before writing the candidate. Test only the public API, not
private helpers. A hash match does not authenticate a source or prove science.
"""
import hashlib
import importlib.util
import json
import sys

C = "1" * 40
T = "2" * 40
M = "3" * 40
B = "4" * 40
P = "research/r16/alpha/manifest.json"


def encode(obj):
    return (json.dumps(obj, separators=(",", ":"), sort_keys=True) + "\n").encode()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def baseline():
    manifest = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY", "pinned_main": B,
                "pinned_source_head": C, "pinned_source_tree": C,
                "count": 2, "files": [{"path": "research/r16/a"}, {"path": "research/r16/b"}]}
    mr = encode(manifest)
    correction = {"claim_ceiling": "C1_DESCRIPTIVE_ONLY",
                  "correction_type": "APPEND_ONLY_SINGLE_FIELD_TREE_IDENTITY",
                  "field": "pinned_source_tree", "pinned_main": B,
                  "source_commit": C, "old_value": C, "new_value": T,
                  "supersedes": {"commit": M, "path": P, "bytes": len(mr),
                                 "sha256": hashlib.sha256(mr).hexdigest(),
                                 "git_blob_sha1": blob(mr)}}
    return mr, correction


def rebind(mr, correction):
    correction = json.loads(json.dumps(correction))
    correction["supersedes"].update(bytes=len(mr),
        sha256=hashlib.sha256(mr).hexdigest(), git_blob_sha1=blob(mr))
    return mr, encode(correction)


def check(module):
    cases = []
    kw = dict(manifest_commit=M, manifest_path=P, observed_commit=C, observed_tree=T)

    def run(label, manifest_insert=b"", correction_insert=b"", accepted=False):
        mr, correction = baseline()
        if manifest_insert:
            mr = mr.replace(b'"count":2', b'"count":2,' + manifest_insert, 1)
        mr, cr = rebind(mr, correction)
        if correction_insert:
            cr = cr.replace(b'"field":', correction_insert + b',"field":', 1)
        before = (mr, cr)
        try:
            outcome = module.resolve_tree_identity(mr, cr, **kw)
            status = outcome.get("status")
            correct = status == ("RESOLVED_C1" if accepted else "INCOMPLETE")
            if accepted:
                correct &= outcome.get("effective", {}).get("pinned_source_tree") == T
            correct &= before == (mr, cr)
        except Exception:
            status, correct = "UNHANDLED_EXCEPTION", False
        cases.append({"fixture": label, "expected": "RESOLVED_C1" if accepted else "INCOMPLETE",
                      "observed": status, "pass": bool(correct)})

    run("valid_original", accepted=True)
    run("valid_finite_large", manifest_insert=b'"probe":1e308', accepted=True)
    run("valid_finite_small", correction_insert=b'"probe":1e-308', accepted=True)
    run("valid_large_exponent_string", manifest_insert=b'"probe":"1e999"', accepted=True)
    run("valid_negative_finite", correction_insert=b'"probe":-1.5e2', accepted=True)
    run("invalid_manifest_positive_overflow", manifest_insert=b'"probe":1e999')
    run("invalid_manifest_negative_overflow", manifest_insert=b'"probe":-1e999')
    run("invalid_manifest_nested_overflow", manifest_insert=b'"probe":{"n":1e999}')
    run("invalid_manifest_list_overflow", manifest_insert=b'"probe":[0,1e999]')
    run("invalid_correction_positive_overflow", correction_insert=b'"probe":1e999')
    run("invalid_correction_negative_overflow", correction_insert=b'"probe":-1e999')
    run("invalid_correction_nested_overflow", correction_insert=b'"probe":{"n":1e999}')
    run("invalid_correction_list_overflow", correction_insert=b'"probe":[0,1e999]')
    run("invalid_manifest_NaN", manifest_insert=b'"probe":NaN')
    run("invalid_correction_Infinity", correction_insert=b'"probe":Infinity')
    run("invalid_manifest_boundary_overflow", manifest_insert=b'"probe":1e309')
    return {"total": len(cases), "passed": sum(x["pass"] for x in cases),
            "failed": [x["fixture"] for x in cases if not x["pass"]], "cases": cases}


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = check(module)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if not result["failed"] else 1)
