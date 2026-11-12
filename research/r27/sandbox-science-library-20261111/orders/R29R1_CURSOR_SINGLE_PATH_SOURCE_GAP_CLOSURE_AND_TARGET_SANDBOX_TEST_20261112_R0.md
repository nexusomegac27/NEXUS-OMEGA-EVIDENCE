# NEXUS OMEGA — R29R1 decision: CURSOR one-path runtime test, no research loop

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R29R1_SOURCE_GAP_RESOLVED_TARGET_EXECUTION_SINGLE_PATH_20261112_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
DATE = 2026-11-12
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
PURPOSE = CLOSE_EXACT_REFERENCE_SOURCE_GAP_AND_EXECUTE_FIRST_TRUE_TARGET_SANDBOX_FALSIFICATION
ROUTE = CURSOR_FIRST; EXTERNAL_EXPERTS_ONLY_AFTER_INDEPENDENT_RUNTIME_EVIDENCE
AUTOMATED_NEW_RESEARCH_LOOP = NO
OPPO_CAPTURE = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
HOSTINGER = NOT_AUTHORIZED
EXTERNAL_GITHUB_WRITE = DENY

## A. Canonical chain and source gap closure

Previous Cursor return:
NEXUS_OMEGA_CURSOR_R29R1_OFFLINE_REFERENCE_AND_EXECUTABLE_SANDBOX_BIND_RETURN_20261112_R0
with state PASS_WITH_MATERIAL_CAVEATS_C1_ORDER_MATCH_WORKER_REHASH_MATCH_PACKAGE_SOURCE_GAP_REFERENCE_AND_SANDBOX_NOT_EXECUTED_DEVICE_PREFLIGHT_FAIL_CLOSED.

AXIOM independently read the five operator-uploaded original Cursor return documents, checking all 5/5 SHA256 members against attached SHA256SUMS.txt, and independently SHA256 hashed SUMS file itself:
- EXECUTIVE.md 5091 bytes SHA256 d2bf2ae5e9809e9cd6c589921e86edbe42956cd446504b870ef078412edfee8a
- HANDSHAKE.md 837 bytes SHA256 991ac2f2c41599aeaa2bfd73ffdb2c205f8ba49e26af3592bb301ccd714788bd
- EPISTEMIC_WALLS.md 636 bytes SHA256 a8b5294c2f51aa710bc61dd1ccfa2774ca5e3f4003b671629cef06c774b38670
- RESULT.md 1239 bytes SHA256 12f142b6b2a476c646b8f2f3c224e86ffe2feabdeda25fa895bbbb8f3bb83eb4
- MACHINE_RECEIPT.json 3840 bytes SHA256 3d52c2ad060552bb7abd7d4aa6a65bf4c09ccd8ab01d5b645184f1a69382bac1
- SHA256SUMS.txt 406 bytes SHA256 b91e5ccb6bca8cf107132f0d9faec14710dba95d2cec1e3820fddf98042a7f43
AXIOM did NOT receive/recompute original Cursor outer ZIP 6469 B; leave ZIP SHA 7a4e2b30a2dc2d4146b46ebe09655d7038d9b6c0a9a20f9cf17c469d80168cd3 as CURSOR_REPORTED, not AXIOM independent.

The previously absent AXIOM original R29R1 ZIP is physically present in AXIOM container, 16800 bytes, SHA256 bd5435b30476b6b52e7aca7f33854d7e837b51edcd7778402e383c094d6aed2a, ZIP CRC PASS, 8/8 entries readable and internal MANIFEST child hashes MATCH. Cursor's prior local PACKAGE_SOURCE_GAP was real for Cursor's local disk, but is no longer a barrier to obtaining the exact PUBLIC-SAFE REFERENCE SOURCE. DO NOT say Cursor received full ZIP via GitHub: the GitHub transfer transports only the exact necessary code and source-binding metadata, not original ZIP binary.

Source-exact GitHub files in THIS PR:
- scripts/r29_reference_f01_f26.py = original R29R1 ZIP bytes 12864, SHA256 662a6e4d626e67b6f7fcdc14ecc211421c4b8ef762e6e25a0105592b03b39f2e, expected Git blob SHA1 cab0ab2ba78fb662c2081c88f3fe6c71fc3a1f52.
- scripts/r29_reference_mutations.py = original R29R1 ZIP bytes 1224, SHA256 aaeac633f3d9a5f41ab51114aa18cce88b1e3bb251f2a4171d25b4a294e01917, expected Git blob SHA1 c0187e88560fcf6288588e063b87917b282372c4.
- .github/workflows/validate-r29r1-reference.yml = owner-added CI reference job, executes only these synthetic scripts in GitHub Actions with scoped read-only token and NumPy 2.3.5; never a target sandbox, phone session or independently isolated-node qualification.
The two published source files were read back from GitHub and both blob SHA1 values match independently computed local Git-blob SHA1 for original ZIP source bytes. Their full SHA256 and lengths must also be independently checked by Cursor upon intake, including the full exact commit pin.

AXIOM independently re-executed ORIGINAL ZIP code with Python 3.13.5 and numpy 2.3.5: 26/26 primary expected synthetic controls, 25/25 positive twins, always-deny and always-accept mutations detected. New output SHA256 8a23b25cfce172b2af704bc0dfb66ff110cbb77f7cf86294c84cc67f809f8ed9 matches ORIGINAL ZIP's REFERENCE_F01_F26_RECEIPT.json byte-for-byte. This is repeatability of the REFERENCE implementation, not a target run.

## B. One decisive Cursor execution mandate — not another paperwork round

1. FETCH pinned source files from this PR and independent rehash; run original source/anti-mutation code in an isolated **local reference** workdir with Python+numpy and preserved exit/stdout/clock/tooling receipts. No second operator ZIP handoff needed.
2. Next discover the **actual NEXUS Sandbox target** source, executor, isolation boundary and policy/validator at pinned commit. Existing real GitHub modules scripts/nexus_preentry_lab.py and scripts/validate_external_agent_pr.py and their tests are real SOURCE candidates; they are NOT automatically a whole isolated external-agent sandbox. If the purported target is only a static catalogue or PR, state TARGET_RUNTIME_ABSENT and implement the minimal, read-only, testable validator adapter on the private/authorized implementation branch instead of inventing a runtime.
3. Execute real target integration checks against the true implementation. Count an Fxx PASS only when the target system under test, not scripts/r29_reference_f01_f26.py, actually processes corresponding test input and yields an observed bounded result. Unsupported controls are NOT_RUN with precise reason and source gap, not included in 26/26. Compare positive and negative controls under predeclared oracles. Publish measured counts, real stderr/stdout hashes, test/target binary hashes, interpreter/OS/clock and isolation proofs.
4. If existing target lacks any tested enforcement or safe runtime, produce a minimal working unit test plus actual receipt on the highest-value supported scope (e.g., structural actor/path rejection) and separately report absent isolation. NEVER loop back to another abstract F01–F26 order or arbitrary new rounds.
5. Only after target execution, independently evaluated improvements and source custody: one **bounded independent external expert falsification review** of that runtime receipt. Research will ask whether actual target measurements support increased correctness and whether TESSERACT-8 outperforms simpler provenance/core designs; no extra rounds solely to affirm design.
6. Keep R28_STATIONARY_CAPTURE:G0–G3 distinct from PRIVATE_OPPO_BRIDGE:G0–G12. No device, host or consent receipt from this public work; no OPPO capture, APK deployment, signed release, CAS upload or WWW publish. Private PR33 remains separate and open.

## C. Acceptance and no-loop stop condition

A successful Cursor return has real source rehash and either:
- FIRST_TARGET_EXECUTION: identifiable pinned *actual* policy implementation, at least one observed negative+positive target pair, source/test/runtime hashes, exit/stdout, fixed denominator, fail-safe privacy and authority scope; OR
- TARGET_ABSENT_MATERIAL: reproducible source audit proving there is no real target runtime yet, with an implemented offline narrow policy adapter/test harness and exact output, plus explicit absent isolation claims.
A paper-only retelling or synthetic reference 26/26 without actual target tests is NOT closure.

Preserve prior R27/R28/R29 originals, PR357/358 and private PR33 statuses, don't auto-merge any PR or register external GitHub agents. Post source/CI GitHub draft pointer under existing research path; actual raw private host/device content stays private. Return one source-exact cursor package through existing transport; independent AXIOM receiver ACK pending. No endless instruction reissuance. The next scientific transition is an empirical target receipt, not another opinion poll.

C1_DESCRIPTIVE_ONLY = HARD_CEILING
CLAIM_PROMOTION = NO
NEXT = PINNED_REFERENCE_EXECUTION_THEN_ACTUAL_TARGET_BOUNDED_TEST_THEN_EXTERNAL_FALSIFICATION
