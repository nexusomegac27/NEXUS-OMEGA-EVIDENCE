# NEXUS OMEGA - AXIOM R71 - Detached manifest local preflight

OBJECT = NEXUS_OMEGA_AXIOM_R71_DETACHED_MANIFEST_LOCAL_PREFLIGHT_20261016_R0
STATE = TESTED_ISOLATED_C1_CANDIDATE_NOT_INTEGRATED
PREDECESSOR = NEXUS_OMEGA_AXIOM_R70_ELIGIBILITY_DENOMINATOR_PROVENANCE_GUARD_20261016_R0
PREDECESSOR_PACKAGE_SHA256 = 3113c68e358f34b65b2c2a1389c501ec112e37b8d3ebe7473874e8feb5cf951e
PREDECESSOR_MANIFEST = 17/17_MATCH
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Gap and falsifier

R67 recorded an append-only correction of an incorrect report SHA256 in its first published detached manifest. R70's detached manifest remains local-only after a platform-blocked write. This iteration tests one narrower quality gate: a detached manifest must not pass local preflight if its referenced report bytes, SHA256 or Git blob identity disagree. Local checks cannot authenticate remote GitHub state.

FALSIFIER: an altered same-length report, a wrong declared SHA256, a wrong Git blob SHA1, a missing report or a duplicate JSON key must fail closed. A clean, original R70 report and detached manifest must pass. The evaluator is frozen before candidate implementation.

## Isolated candidate and results

TOOL = r71_detached_manifest_local_preflight.py
TOOL_SHA256 = 553aad734333aa219244e2e47a5843f32004ea4117e54863ef48c0d714e8ef73
FROZEN_EVALUATOR_SHA256 = e1f462ced3ee898b2c6655c78a47c1ede5107dd4e131659827b823735103b4d6
BASELINE = deliberately weak JSON-and-path-exists preflight, 6/18 tests PASS (not R70 production behavior)
CANDIDATE = 18/18 PASS
MUTANT_SKIP_DIGEST = 3/18 failures detected
R70_HISTORICAL_EVALUATOR = 14/14 PASS on unchanged R70 source
SOURCE = actual local R70 ZIP 51652 bytes, SHA256 3113c68e358f34b65b2c2a1389c501ec112e37b8d3ebe7473874e8feb5cf951e
SOURCE_REPORT = 3324 bytes, Git blob 0cbdc15c7c69fa872ca194911aeb9297f11ec457

The local checker rejects duplicate keys, path traversal, symlinks, malformed identities, self-hash claims and byte/hash/blob mismatches. It returns LOCAL_PREFLIGHT_PASS only for local source identity, never remote validation, scientific correctness, CI success or main merge. The frozen evaluator is separately executed but not an external scientific reviewer. This is a research-only scaffold; no productive validator, oracle, Windows node, Hostinger, rights, secrets or repository governance was changed.

## Publication and goal limits

Any GitHub branch, PR, CI, main merge, Issue 93 receipt and WWW parity require separate actual readback. No publication claim follows from a local PASS. The 30-day eligible handoff denominator and verified autonomous numerator remain unknown; 90 percent attainment is not computable. R10 PR 115 is public SEND, not an authenticated independent expert return. External actor allowlist is empty on pinned main.
