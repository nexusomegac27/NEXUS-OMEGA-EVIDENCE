# NEXUS OMEGA — AXIOM · Independent Trusted-Witness P0 Readback · 2026-11-01 R0

OBJECT = NEXUS_OMEGA_AXIOM_INDEPENDENT_TRUSTED_WITNESS_P0_READBACK_AND_CI_REPAIR_20261101_R0
PARENT = NEXUS_OMEGA_CURSOR_AGENT_COMMUNICATION_TRUSTED_WITNESS_P0_LAST_MILE_RETURN_20261031_R0
SOURCE_CODE_COMMIT = 986b9af8f4bcfb341a188cbb6ed7d8da3d500e98
AXIOM_CI_REPAIR_COMMIT = d76af91d121b93d1b456120fc54f67e412c27ed1
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_LOCAL_TEST_CI_VALIDATED_EXTERNAL_TRUST_NOT_ESTABLISHED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
V1_PUBLIC_READ_MILESTONE = CLOSED_LIVING
CUTOVER_ACTIVE = NO
EXTERNAL_AUTHENTICATED_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
PR185_MERGE = NO
ORIGINAL_WINDOWS_TRANSFER_REHASH = NOT_PERFORMED

## Exact GitHub-source verification

AXIOM independently fetched the original GitHub files at commit 986b9af8f4bcfb341a188cbb6ed7d8da3d500e98 and rehashed UTF-8 bytes with SHA-256 (known ABC test vector verified).

| Path (research paths share research/communication/github-only-exchange-enforcement-20261029/) | Actual bytes | Actual SHA-256 |
| --- | ---: | --- |
| RESULT_AXIOM_CURSOR_AGENT_COMMUNICATION_TRUSTED_WITNESS_P0_LAST_MILE_20261031_R0.md | 5048 | 6b9ac2cf68c22ba3fb6aab0c61bb891baa10175959ce8f2cdd92040c4afb8baa |
| TASK_ANCHOR_AXIOM_CURSOR_AGENT_COMMUNICATION_TRUSTED_WITNESS_P0_LAST_MILE_20261031_R0.json | 7935 | ed8be89d541c21ac47a6f14f229f295847a67af1e32836ec9d576e895c8b5098 |
| scripts/nexus_document_router.py | 50522 | 31a30eaae3bad5f52225947206a3ee7f3c22ae337400dca01519be0a596351ec |
| tests/test_nexus_document_router.py | 28280 | 934cfafb1539105c0a2b8dbc5cf5714b9d46308478fcb800ca6927aba44f8bd6 |

The Cursor RESULT includes older peel-tip test hash 29061 B / 7447da... but the operator separately supplied the correct final-tip 28280 B / 934c... value. That is a source-version distinction, not evidence of tampering. Windows EXEC/HANDSHAKE/WALLS/SUMS blobs are not available via the fetched GitHub sources and were not independently byte-rehashed here.

Prior foundation: 120eace7fb807552148cdecd52eeb07cc4fc9c3c, 8469 B, SHA-256 c6c941991f870d8497427824b6b9afefe10f2ec945524be350d57810cbe438ef. Original P0 order: 12d79983f44e8ea6bd0361a43c66242be42439a0, 8385 B, SHA-256 1aeacbecb80ecef7846bd5b4d696d848b3240b76f847c01e094c6a222c5286b6. Their earlier chain had already been independently checked.

## Exact CI and governance

At Cursor original tip 986b9af: PR185 OPEN DRAFT 82 changed files; R27E structural firewall PASS, preentry PASS, Semgrep PASS; 10/12 CI checks SUCCESS, two router-p0 check-runs FAILURE. The failures were not failing security negatives. The Github Actions runner could not import nexus_document_router from scripts/ in its Python path. Both job logs prove ModuleNotFoundError and no 29-case execution.

AXIOM repaired ONLY its own earlier workflow at commit d76af91d121b93d1b456120fc54f67e412c27ed1, path .github/workflows/validate-agent-communication-router-p0.yml: added PYTHONPATH=$GITHUB_WORKSPACE/scripts to the unittest command, no router-code or fixture changes. Two subsequent independent GitHub Actions checkouts executed all 29 tests successfully: run 41266859896, job 124731355966, and run 41266857146, job 124731348652; 29 tests / OK in each log. Last observed CI on repaired head: 11/12 successful, Semgrep pending, zero failures; do not promote to 12/12 until observed.

PR185 remains 82 changed files, below R27E limit 100. PR246 living foundation OPEN, 2 files, 8/8 SUCCESS. PR253 open-neutral successor OPEN DRAFT, 22 files, 9/9 SUCCESS. None were merged by AXIOM.

## Accepted P0 local improvements

Source code now requires a separately injected GithubClient for the issue-comment API fetch before accepting an external author; plain caller api_attestation strings cannot independently promote. receive_receipt and verify_receiver both require principal_verified, return_source_verified and bytes_match for the final report-level ACK. Local journal without actual transport adapter remains OUTBOUND_QUEUED. Cutover requires a separate configured trusted_cutover_evidence object. Private material demands an owner_lane_registry entry as well as explicit scope. These are real incremental source changes; 29 unit tests successfully exercise their mock/negative logic.

## Remaining material source-level limits

1. Actual GitHub REST integration NOT PROVEN: RouterConfig.github_client defaults to None; the tests use FakeGitHubClient and no actual authorized GitHub comment/return from a separate principal was demonstrated. Real provider actor verification thus remains NOT_ESTABLISHED.
2. SHA256 and bytes fallback from caller data remains: verify_github_receiver_witness uses fetched.observed_sha256 OR witness.observed_sha256 and fetched.observed_bytes OR witness.observed_bytes; return source commit/hash likewise use fetched values OR witness fields. A GitHub comment author metadata cannot attest that the recipient actually fetched and byte-hashed the specified original document. Need verifier-fetched raw content bytes/return bytes with exact source refs, authorized slot and nonce; never treat the untrusted witness fallback as proof.
3. Intermediate state may overclaim: receive_receipt sets ack.independent=true unconditionally and can advance FETCH_OBSERVED and RECEIVED_BYTES_VERIFIED solely from caller source hash and length, even if github_client=None. Final ESTABLISHED_REPORT_LEVEL now requires more fields, but intermediate receipts are not evidence of independent byte receipt. Only trusted backend actual fetch should advance them.
4. Cutover and private trust still use injected dictionaries: trusted_cutover_evidence and owner_lane_registry have syntactic signer/status/bytes checks, not observed GitHub owner approvals, cryptographic signer verification, true configured private connection, or pinned final CI/rollback source. This is useful separation, but not a production authorization seal.
5. transport_adapter.prove() is injected and the test uses FakeTransportAdapter. The router does not itself prove an API delivery from an actual provider; no live delivery, distinct external authenticated ACK or bidirectional success established.

These are source-code and evidence-status findings, not a claim of a public remote exploit. Public read-only Agent Communication V1 stays live and closed as a living foundation. No new public POST, new agent account, unreviewed merge, or framework fork is authorized.

## Terminal

STATE = PASS_WITH_MATERIAL_CAVEATS_C1_TESTED_LOCAL_TRUSTED_WITNESS_DESIGN
SOURCE_HASHES = 4_OF_4_MATCH_AT_CURSOR_COMMIT
CI_WORKFLOW_IMPORT_ERROR = REPAIRED_BY_AXIOM
ROUTER_CI = 29_OF_29_PASS_IN_TWO_GITHUB_ACTIONS_JOBS
GOVERNANCE_PR185 = R27E_PASS_82_FILES
PR246 = OPEN_2_FILES_CI_8_OF_8_PASS
PR253 = OPEN_DRAFT_22_FILES_CI_9_OF_9_PASS
FULL_EXTERNAL_VERIFIER = NOT_ESTABLISHED
CUTOVER_ACTIVE = NO
PUBLIC_WRITE_API = OFF
WWW_READ_ONLY = LIVE_PREVIOUSLY_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = NARROW_REAL_BYTE_WITNESS_AND_OWNER_EVIDENCE_SUCCESSOR_ONLY
