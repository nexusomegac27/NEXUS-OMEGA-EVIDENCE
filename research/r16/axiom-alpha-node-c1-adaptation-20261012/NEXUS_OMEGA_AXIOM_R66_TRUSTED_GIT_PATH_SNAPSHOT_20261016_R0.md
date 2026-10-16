# AXIOM Alpha-Node R66 - trusted Git executable PATH snapshot (C1)

OBJECT = NEXUS_OMEGA_AXIOM_R66_TRUSTED_GIT_PATH_SNAPSHOT_20261016_R0
CLASS = TESTED_IMPROVEMENT_CANDIDATE_ISOLATED_SCAFFOLD
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR_R65_ZIP_SHA256 = 1fac311e537fb98dc6c01f074d41c23cf4bf5ee1a443ae9d44c33196946d8791
PREDECESSOR_R65_MANIFEST = 16/16 BYTE_AND_SHA256_MATCH
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Falsifiable local negative

R65 pins its Python validator source but inherits PATH for the child process. That validator invokes git by name. A synthetic adversarial PATH-prepended Git shim suppresses research/r16/unlisted.md from git diff --name-only -z while leaving the actual commit objects and manifest unchanged. R65 falsely accepts the partial handoff with exit 0. This is a local fixture, NOT evidence of a remote compromise.

## Isolated candidate

R66 copies trusted POSIX /usr/bin/git into a fresh private temporary bin/git, rehashes that snapshot, sets child PATH exclusively to that bin directory, and removes inherited LD_*/DYLD_* variables. Existing pinned Python source execution with -I -S is preserved. Missing trusted Git causes a scoped hold, not a fallback to attacker PATH. The system binary and host remain explicit trust assumptions.

## Independent black-box evidence

FROZEN_R66_EVALUATOR_SHA256 = 21a5a442bcc0f30280f3a1e939c132dab069c6b3334b2823e9a8ae8ccc1dcb2d
R66_CANDIDATE_SHA256 = 10538c67dda261ae5f9d721e071fa3a6ae98c74d205a2eb46dafd1a5df1e0f5d
BASELINE_R65 = 7/8 PASS; hostile PATH false accept 1/1
CANDIDATE_R66 = 8/8 PASS; hostile PATH false accept 0/1
HISTORICAL_R65_REGRESSION = 10/10 PASS
DELIBERATE_MUTANT_INHERITED_PATH = 7/8 PASS; 1 hostile-PATH failure detected
FALSIFIER = Any attacker-controlled PATH shim that hides an unmanifested changed path yet yields LOCAL_SCOPE_ACCEPTED_C1 from R66.

## Limits and publication

Only synthetic local POSIX Git tests. No Windows, hostile kernel, compromised /usr/bin/git, malicious already-pinned validator, remote actor authentication, productive CI integration, actual handoff improvement, or scientific validation established. The executable and evaluator remain in the local reproducible R66 research package, NOT integrated into main or deployed. No model/system-instruction modification, no worker, no new pipeline, no node reset.

R10 PR #115 at 539d4bb33d2ba2c4895713c1bc437ece0743eeea remains PUBLIC_SEND, not independent receiver ACK. No new external expert return or expert research execution was observed in the PR conversation or AXIOM Inbox #93 at this check. R10 Task Anchor JSON remains unpublished; SOURCE_NOT_PRESENT for independent expert returns. No R10 courier, Cursor dispatch, Hostinger change or merge.

METRIC_90_PERCENT = NOT_COMPUTABLE; eligible 30-day denominator UNKNOWN; verified autonomous numerator UNKNOWN. Historical 10 reported handoffs are not verified numerator entries. Main publications this run 0 until actual merge and readback; WWW parity NOT_ESTABLISHED.

BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET = NON_DESTRUCTIVE.
