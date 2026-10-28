# AXIOM Alpha-Node · Steward output clobber falsification · 2026-10-28 R0

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_OUTPUT_CLOBBER_C1_20261028_R0
DECISION = PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = a8ce88c1b6073597cceadcd083af94be56bf33a3
PREDECESSOR_RECEIPT = ISSUE_93_COMMENT_6460107290
SOURCE = scripts/nexus_repository_steward.py
SOURCE_GIT_BLOB = 296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_BYTES = 8023
SOURCE_SHA256 = 94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998

## Observed contradiction and falsifier

The original full Steward CLI advertises a read-only inventory and emits
"source_mutation": false, yet --output uses Path.write_text() without an
exclusive-create guard. In a synthetic Git repository, passing the path of a
tracked README.md as --output overwrote its original bytes, exited 0, and
reported source_mutation=false. This is a *capability/contract contradiction*
and a reproducible synthetic source-clobber risk, NOT evidence that a real
NEXUS tracked file has been overwritten.

Negative hypothesis: a caller-supplied output destination can overwrite a
previously bound source while a successful CLI result obscures the mutation.
Falsifier: demonstrate the original CLI rejects an existing tracked destination
without changing it, or that the isolated guard accepts such a destination.
The first was contradicted by the frozen evaluator; the second was not observed.

## Isolated candidate

- Frozen evaluator first commit: 3430b93163f2bb5637ca43ec8be48d5a3a4d3f44
- Evaluator: frozen_steward_output_guard_evaluator_v1_20261028.py
  (5790 bytes, SHA-256 cb2a6b3d8324d6e11690e7d0a03a97d7f15b65c718520c2b1199a12244bf542b)
- Candidate: steward_output_guard_candidate_v1_20261028.py
  (3856 bytes, SHA-256 0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74)
- Candidate reads the original source, requires its exact pinned SHA-256,
  reuses its inventory audit, and creates a *new* output file only outside the
  checkout using POSIX directory-fd O_NOFOLLOW and O_EXCL. No directory
  creation, overwrite, runtime integration, or productive Steward modification.
- Platform lacking required POSIX flags fails closed.

## Executed independent evaluation (synthetic Git fixture)

Command from repository root:

python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_steward_output_guard_evaluator_v1_20261028.py --steward scripts/nexus_repository_steward.py --candidate research/r16/axiom-alpha-node-c1-adaptation-20261012/steward_output_guard_candidate_v1_20261028.py

Local result: 14/14 PASS. Baseline-only run: 3/3 PASS.
Original CLI: tracked README clobbered 1/1; returned success with
source_mutation=false 1/1. Candidate: tracked README clobbered 0/1;
new in-checkout output refused 1/1; existing external file refused 1/1;
symlink-parent and symlink-leaf paths refused 2/2; relative and parent
traversal paths refused 2/2; new external output accepted 1/1 and bytes
matched original positive output 1/1; source remained intact 1/1;
mutated pinned source refused 1/1.

Two separate negative mutants were evaluated against the frozen oracle:
- Remove O_EXCL: 13/14 PASS; expected existing-external-file test failed.
- Remove checkout-boundary check: 13/14 PASS; expected new-in-checkout
  output test failed.

All execution occurred on temporary synthetic Git repositories under
Linux; the test oracle was committed before the candidate. The same
producer environment ran the evaluator: no external third-party
scientific validation is claimed. No actual NEXUS source was overwritten.

## Scope, authority and unresolved risks

Research-only existing R16 Alpha-Node lane; additive versioned files.
Original production Steward remains byteidentical. This is NOT a production
security patch. POSIX-only; Windows, macOS, bind mounts, mount namespace
aliases, privileged races, durability failure cleanup and concurrent
adversarial directory replacement are not independently validated.
A safe production integration would require a separately scoped review,
additional platform/race tests, and real CI integration.

PUBLIC_SAFE = synthetic fixture and source-only code, no secrets/private data
EXTERNAL_AGENT_REGISTRY = unchanged, no external actor registration
CLAIM_PROMOTION = NO
HOSTINGER_WWW_RUNTIME = NO_CHANGE
GITHUB_WWW_PARITY = NOT_ESTABLISHED
PROJECT_HANDOFF_AUTOMATION_RATE = NOT_COMPUTABLE_NO_AUTHENTICATED_FULL_DENOMINATOR
