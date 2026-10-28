# AXIOM Alpha-Node · Atomic output integrity research · 2026-10-28 R0

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_ATOMIC_OUTPUT_C1_20261028_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = b8be4e59f52d8d3739a5d0521e7d7bd80c9d7611
PREDECESSOR_ISSUE93_RECEIPT = 6460634584
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/164
ROOT = research/r16/axiom-alpha-node-c1-adaptation-20261012/
PRODUCTION_STEWARD = scripts/nexus_repository_steward.py
PRODUCTION_STEWARD_BLOB = 296c7dc67b40f28270c92512ca6f67f8ad25fc50
PRODUCTION_STEWARD_SHA256 = 94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
PRODUCTION_STEWARD_MODIFIED = NO

## Observation and negative hypothesis

The previous isolated POSIX output guard (PR #164) uses O_EXCL and O_NOFOLLOW but opens the *final* inventory destination before writing its bytes. Its source is `steward_output_guard_candidate_v1_20261028.py`, 3856 bytes, Git blob `b697ebb2f0908cd09956bce880c78695f083a4c0`, SHA-256 `0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74`.

Negative hypothesis: an I/O failure after a successful exclusive open leaves a partially written final output path, which a downstream reader could mistake for a completed inventory. The falsifier would be absence of any partial final file after an injected write failure on the original pinned guard.

A synthetic Linux process with RLIMIT_FSIZE=4096, SIGXFSZ ignored and a 122880-byte payload produced a nonzero exit and an existing incomplete final output file with the pinned v1 guard. This contradicts a possible interpretation that O_EXCL alone ensures atomic publication. No real NEXUS inventory was corrupted.

## Single isolated candidate and independent test oracle

The v2 candidate writes to an exclusive, unpredictable temporary file in a directory-fd-verified external directory, flushes and fsyncs, then uses same-directory `os.link` (fails if the final path exists) to publish the complete file. It removes the temporary name and fsyncs the directory. It retains the v1 guard's source hash pin and checkout/symlink/traversal restrictions. This is not a productive integration.

Evaluator FIRST commit = `20766f15f5e9a9578d83b02fd9635bc1646ba143`
Evaluator path = `frozen_steward_atomic_output_evaluator_v2_20261028.py`
Evaluator bytes = 4611
Evaluator Git blob = `85bf666208f98048960151b40bd62afa62b2b6e6`
Evaluator SHA-256 = `f173dbce994b66d9c9cd3f65b2df881ee9fbdbd589da304e76478a352db7e692`

Candidate SECOND commit = `7601b9a2acdad475dbd3594be9bd8616817e18c8`
Candidate path = `steward_output_atomic_guard_candidate_v2_20261028.py`
Candidate bytes = 3187
Candidate Git blob = `e7fbad4dd0cd24f6f03c80b9ebbb709c2e14384c`
Candidate SHA-256 = `441bffe0285183605b8d76d9f4d542ebf06f8e63e4f8cc92112550bc4df93841`

The evaluator invokes original and candidate guarded_write functions in separate Python subprocesses; it does not import candidate code or share its implementation. It was committed before the candidate. Both evaluator and candidate were authored and executed in the same AXIOM environment: independent **test implementation**, not an independent third-party validation.

## Actual executed results

Platform: Linux 6.18.55 x86_64, Python 3.13.5, Git 2.47.3. No secrets or personal data. Synthetic temporary directories only.

- Baseline-only frozen evaluator: 3/3 PASS, including partial-final negative witness 1/1.
- Candidate frozen evaluator: 14/14 PASS. Write-failure final-file exposure 1/1 baseline versus 0/1 candidate; failure cleanup and positive byte-identical output PASS.
- Existing-file no-overwrite, checkout exclusion, symlink parent/leaf, relative path and traversal checks PASS.
- Negative mutant replacing atomic hard-link publication with overwrite-capable `os.rename`: 12/14 PASS, with expected failures for existing-file overwrite and symlink-leaf protection. The mutant was local only, not published.
- Test command: `python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_steward_atomic_output_evaluator_v2_20261028.py --baseline research/r16/axiom-alpha-node-c1-adaptation-20261012/steward_output_guard_candidate_v1_20261028.py --candidate research/r16/axiom-alpha-node-c1-adaptation-20261012/steward_output_atomic_guard_candidate_v2_20261028.py`

## Claim boundaries and disposition

This establishes a synthetic POSIX function-level partial-write counterexample and an isolated mitigation under the stated fixture. It does NOT establish complete original Steward CLI end-to-end integration, safe production use, Windows/macOS portability, robustness against privileged mount replacement, kill/crash orphan-temp cleanup, directory-fsync failure semantics, concurrency stress or independent external scientific validation. In particular, errors *after* link publication may leave a visible complete final file while the caller reports failure. The candidate's atomicity claim is strictly **prepublication write failure does not expose a partial final file**.

Repository structure is unchanged: three additive research files in the existing registered R16 lane; no source replacement, runtime/Hostinger/WWW write, actor registration, node reset, evaluator auto-approval or claim promotion.

PROJECT_AUTOMATION_RATE = NOT_COMPUTABLE_NO_FULL_AUTHENTICATED_ELIGIBLE_DENOMINATOR
PROJECT_100_PERCENT_READBACK = NOT_ESTABLISHED
R10_INDEPENDENT_EXPERT_RETURN = SOURCE_NOT_PRESENT
PUBLICATION = PENDING_PR_CI_AND_MAIN_READBACK
WWW_PARITY = NOT_ESTABLISHED
