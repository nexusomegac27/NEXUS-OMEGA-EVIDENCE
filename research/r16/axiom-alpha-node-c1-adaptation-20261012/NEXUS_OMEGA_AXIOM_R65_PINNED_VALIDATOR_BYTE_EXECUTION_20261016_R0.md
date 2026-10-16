# AXIOM Alpha-Node R65 — pinned validator byte execution (C1)

OBJECT: NEXUS_OMEGA_AXIOM_R65_PINNED_VALIDATOR_BYTE_EXECUTION_20261016_R0
CLASS: ISOLATED_SCAFFOLD_PATCH_CANDIDATE
PREDECESSOR: NEXUS_OMEGA_AXIOM_R64_PYTHON_CHILD_ENVIRONMENT_ISOLATION_20261016_R0
PREDECESSOR_ZIP_SHA256: 0caea7c796c1eebdd284d7bca825c86d349fc818cb7fa0abd2161f00a85eaf85
BASE_MAIN: d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING: C1_DESCRIPTIVE_ONLY

## Falsifiable negative finding

The R64 local gate SHA-256-checks the source of its child validator, then executes the original mutable path. In a deterministic atomic replacement fixture, an attacker-controlled Python file replaces that path between the digest check and subprocess execution. The replacement prints plausible FULL_SCOPE_VERIFIED JSON and exits zero. R64 falsely accepts both a partial and a corrupt manifest handoff in this local test. This does not imply a remote compromise.

## Isolated repair candidate

R65 captures the original validator bytes once, validates their SHA-256, copies exactly those bytes into a newly created private temporary directory, rehashes that snapshot and runs the snapshot using CPython -I -S. The mutable original path is never executed. No fallback to it is permitted.

Frozen R65 evaluator SHA256: 7cb603d1b939fd4f60c9a76b24e8fa332635e045a7e594d2a6e193687cd14f30
R65 candidate SHA256: 745131b17bc5a2ae3a72d1cd8c1e425df07ee61f5a354ff7a1d4f2147823f289
Frozen evaluator result: R64 6/10 PASS; R65 10/10 PASS.
Partial handoff false accepts: 1/1 -> 0/1.
Corrupt handoff false accepts: 1/1 -> 0/1.
Historical R64 frozen regression: 10/10 PASS.
Deliberately regressed candidate: 4/10 failures detected.
Physical R64 package manifest: 13/13 SHA-256 and byte-length matches.

Falsifier: any atomic replacement after the successful hash that causes unpinned bytes to execute or a partial/corrupt handoff to be accepted refutes the repair in this threat model.

## Explicit limits

Separate frozen evaluator is not an external peer review or an independent authorization oracle. Only synthetic local Git repositories were tested. No proof against malicious already-pinned code, same-UID temporary-directory tampering, hostile OS/interpreter, or runtime deployment. No private OPPO or KIMI original is republished. No production CI integration or achieved Handoff automation improvement is claimed.

At the observed GitHub snapshot, main d355400dabed3c280e1fce5030cab69ea099428b, PR #114 open at 078dc08aea659a99959542fbe5637e635b08e612, Issue #93 latest comment 6202997859. External writer registry remains default deny; this owner research note does not allocate any write slot.

Handoff target >=90% remains a TARGET, not an achieved metric: independently eligible 30-day denominator UNKNOWN, autonomous success numerator UNKNOWN. Historical 10 reported handoffs are not counted as verified successes. Main publication/readback and GitHub-WWW parity require separate actual receipts.

No model-weight change, no new worker, no new pipeline root, no Node reset, no Hostinger write, no claim promotion. Research candidate only.
