# PR #356 — canonical base-target CI repair receipt
OBJECT = NEXUS_OMEGA_R28_TESSERACT_PR356_NON_CANONICAL_BASE_DIAGNOSTIC_20261112_R0
STATE = APPEND_ONLY_DIAGNOSTIC_NOT_MERGE_PERMISSION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SOURCE_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/356
HEAD_BEFORE_REPAIR = 52ba35b09b2bdc03060cf083de7eac15ea61ee9c

The initial owner-authored draft PR #356 targeted the predecessor research feature branch. The trusted-base structural firewall correctly emitted FAIL_CLOSED / ValueError: NON_CANONICAL_TARGET_BRANCH; the dependent pre-entry check correctly emitted DENY because upstream firewall failed. The standard repository structure checks succeeded. This was not a science or privacy failure, but it is a real GitHub admission failure, not to be relabeled PASS.

Repair: retarget the draft PR to the canonical main branch, without merging and without modifying historical source files or the R27-E actor registry. This receipt appends the cause and the retry intention. Actual fresh CI must be checked after this commit; no success preclaimed.

Dependency: PR #356 currently contains the still-unmerged #355 source order files as ancestors. This is a stacked lineage; any future merge requires independent owner review, no duplicate content drift and the GitHub mandated checks. No auto-merge, no new permissions, no device execution.

RECEIVER_ACK = PENDING_AXIOM_INDEPENDENT_REHASH
