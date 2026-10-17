# NEXUS OMEGA · AXIOM Alpha-Node R93 · Pinned README reference integrity

OBJECT = NEXUS_OMEGA_AXIOM_R93_PINNED_README_REFERENCE_GUARD_20261017_R0
CLASS = C1_ISOLATED_RESEARCH_CANDIDATE
PREDECESSOR = NEXUS_OMEGA_AXIOM_R92_ACTOR_ORIGIN_RECEIPT_GUARD_20261017
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
R10_SOURCE_PIN = 539d4bb33d2ba2c4895713c1bc437ece0743eeea
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Source-exact observation

The R10 README at the immutable pinned commit contains eight numbered research-file references. The GitHub Git-tree API at the same commit exposes six of those exact paths; two are not present under the declared names:

- `TASK_ORDER_ANCHOR_V1.json` — absent; independently disclosed as a blocked publication in the R10 PR description.
- `R10_GITHUB_EXPERT_HANDSHAKE_DETACHED_MANIFEST_R1.json` — absent; the physically present manifest is `R10_GITHUB_NATIVE_DETACHED_SOURCE_MANIFEST_20261016_R1.json`.

The README original was read from GitHub and reproduced locally as 2,276 bytes, Git-blob SHA-1 `080923c713e9fe6b36490c0973d5f626f5408176`, SHA-256 `22e22221a286b3c94a8342689bed86474a8ed8b41a572c7e180cc24af7be966a`. The Git tree was nontruncated. This is an already documented documentation inconsistency, not a newly discovered concealed source gap.

## Negative hypothesis and candidate

Hypothesis: a list of referenced files is not evidence that the named files exist on the immutable commit. A naive parser that counts eight entries can falsely report 8/8 complete. The isolated `candidate.py` checks an independently supplied immutable commit pin, complete Git-tree inventory, safe relative paths and exact case-sensitive membership. It does not rewrite source, infer equivalent names, authenticate actors or approve scientific claims.

Independent frozen evaluator SHA-256: `ef43702dada17305e218f25e9df18226263354deda8883eb2dd9c45dd807bd96` (created before candidate implementation).

- Naive baseline: 2/14 contract fixtures PASS.
- R93 candidate: 14/14 contract fixtures PASS.
- Real R10 case: 6/8 referenced files physically present by exact path; two references correctly flagged.
- Negative fixtures include missing source, wrong commit pin, truncated/absent tree, missing README, traversal, external URL, case drift, duplicate numbering and empty inventory.
- Falsifier: if a complete Git tree at the pinned commit contains all eight exact referenced paths, the guard must return PASS. If it returns PASS for the observed six-of-eight tree, the candidate is falsified.

## Boundaries and decision

The candidate is an isolated offline scaffold, not integrated tooling, CI, a runtime worker or a change to an independent evaluator. The real Git-tree snapshot came from a connected GitHub API; the local fixture is a preserved API observation, not a cryptographically signed external witness. No R10 scientific result or expert receipt is promoted. The R10 manifest itself remains byte-identical between the pinned commit and current PR head as observed via the GitHub connector; the mutable PR head is NOT the immutable source pin.

DECISION = TESTED_IMPROVEMENT_CANDIDATE_C1
R10_PUBLIC_SEND = ESTABLISHED
R10_INDEPENDENT_RECEIVER_ACK = SOURCE_NOT_PRESENT
R10_EXPERT_RESEARCH_EXECUTED = NOT_ESTABLISHED
R9 = OPEN_NONINTERFERENCE
PR115 = OPEN_NOT_MERGED
NO_R10_SOURCE_MUTATION = YES
NO_MERGE_AUTHORIZATION = YES
NO_HOSTINGER_OR_DEVICE_WRITE = YES

Reproduction: `python frozen_evaluator.py naive_baseline.py` and `python frozen_evaluator.py candidate.py`. Full local fixture, source inventory, evaluator, candidate, baseline and results are retained in the isolated R93 package. Publication/merge status requires a separate actual GitHub readback; a branch commit is not a main merge.
