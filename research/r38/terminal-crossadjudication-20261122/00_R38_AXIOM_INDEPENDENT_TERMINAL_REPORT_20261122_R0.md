# NEXUS OMEGA — R38 terminal scientific cross-adjudication and Cursor handoff (C1)
OBJECT = NEXUS_OMEGA_AXIOM_R38_TERMINAL_INDEPENDENT_CROSS_ADJUDICATION_AND_CURSOR_HANDOFF_20261122_R0
DATE = 2026-11-22
STATE = CLOSED_AS_RESEARCH_AND_FIRST_PARTY_PROTOTYPE_PHASE_WITH_MATERIAL_CAVEATS_C1
R38_PHASE = OPERATOR_DECLARED_COMPLETE_FOR_HANDOFF
R38_SCIENTIFIC_COMPLETION = PARTIAL_CONDITIONAL
R38_EXECUTABLE_CANDIDATE = PRESENT_FIRST_PARTY_OFFLINE_SYNTHETIC
R38_SOURCE_SEAL = FAIL_2_OF_27
R38_ORIGINAL_RECEIPT_79 = 3_UNEXPECTED_FAILURES
R38_AXTUAL_DELIVERED_SOURCE_LOCAL_REPLAY_79 = EXPECTED_VERDICTS_79_OF_79_WITH_CAVEAT_SOURCE_NOT_SEALED
CURSOR_R38_IMPLEMENTATION_RECEIVER_ACK = NOT_OBSERVED_AS_OF_THIS_AUDIT
R39 = NOT_STARTED_AWAITING_CURSOR_RETURN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED = NO
REAL_OPPO_ORIGINAL_BODYTWIN_ABC = NOT_PERFORMED
ACTUAL_EXISTING_BODYTWIN_CONSUMER = NOT_CONNECTED
OPPO_OWNER_APPROVAL_WITNESS = OPEN
OPPO_SOURCE_BUILD_AUTH = OPEN
PRIVATE_ORIGINAL_GITHUB_RECEIVER = OPEN
INDEPENDENT_BODY_REFERENCE = ABSENT
PR_MERGE = NO
HOSTINGER_WRITE = NO
WWW_WRITE = NO
NEW_DEVICE_CAPTURE = NO
RECORD_SUPERSESSION = APPEND_ONLY_NO_SOURCE_REPLACEMENT

## 1. R37 to R38 frozen primary lineage
Public NEXUS-OMEGA-EVIDENCE R37 terminal commit e1c70329e33eefae09e9b2cddcf1966e00d80f4d (CLOSED_WITH_MATERIAL_CAVEATS_C1 research phase).
Public R38 G0-G10 implementation-spec Draft PR #382 SOURCE HEAD 90debcc169fdac1448500c253a0164c2f4f972a9, its original 10/10 SHA256SUMS own hash 12aded2d28b3311171b1b95e6f4bb5b04f574aff10063ab161f6d1adb6bbab99. Original source unchanged. Current GitHub state at 2026-11-22 verified OPEN DRAFT NOT MERGED, 11 changed files, no new Cursor code committed to #382.
Private R38 receiver in DIFFERENT repo nexusomegac27/NEXUS-OMEGA-PRIVATE-SCIENCE-CUSTODY PR #37 @ac2f88d82f27df50008ab7e30296a49613a67b0e, OPEN DRAFT NOT MERGED (verified via connected authorized GitHub API); it holds 2/2 restricted source/receipt TEMPLATE files and no actual OPPO original bytes. External anonymous 404 not a proof of inexistence.
Cursor implementation mission Issue #383 originally OPEN, requires actual receiver source/codes G0-G10 and independent repeatable tests. A user-provided external/Qwen/AutoClaw workspace is NOT Cursor's authenticated own source return or GitHub receipt.

## 2. Source scope — nine user uploads
Exact 9 mounted operator originals inspected: AUTO_C~1.ZIP, R38_IN~1.TXT, R38_RE~1.JSO, R38_IN~1.MD, CANONI~1.TXT, NEXUSO~1(2).PDF, NEXUS-~1(20261122-125505).MD, R38_RE~1.MD, workspace.tar(6).gz. Individual byte-level hashes for each and any restricted evidence roots are recorded only in the separated authorized private R38 intake manifest; do NOT duplicate private/workspace original content digests into public CAS or GitHub.
The 10-page Nov 22 PDF is a visually structured retrospective of R37 CLOSEOUT and R38 G0–G10 planned implementation. It is not an R38 execution receipt. Qwen/Mistral/Vibe/Grok/independent receiver reports converge publicly on R38 frozen source readback 10/10; distinct actor labels are self-declared unless separately authenticated.
Grok/reporting and deterministic Triade-B identify a NEW readback error type: an LLM-mediated reading claimed older PR #378 and Issue #379 OPEN although deterministic API/embedded HTML showed CLOSED. Make R38-T21 mandatory: READBACK_CHANNEL_MISMATCH, FAIL_EXPECTED, schema source kind RAW_API_JSON vs HTML_EMBEDDED_STATE vs LLM_REPORTED.
The Qwen full workspace includes R37 10/10 public contract snapshots, public R38 10/10 source snapshots and first-party SVK. Exact original OPPO sensor gzip and original R37 Stage0 M01/M02 source ZIP were NOT in this workspace. Do not infer actual private access from old notes.

## 3. AUTO_C~1.ZIP expert source verification and independent replay
AUTOCLAW ZIP 10 entries, CRC PASS, 8/8 structured MANIFEST.json file hashes and byte sizes MATCH; 7/7 SHA256SUMS listed content entries MATCH (manifest also binds the SHA256SUMS itself). Contains executable research x11_observability_rank.py, x12_kernel_gates.py and archived JSON results, independently reviewed and safely rerun offline from original code.
- X11 independently executed isolated Python with Numpy, numerical rank verdicts reproduced across SIX toy configurations: 3 sensors on same segment -> 0 modeled joint DOF, 2 sensors on adjacent segments -> 1 DOF, three properly placed sensors with calibrated mounting / rich excitation can span 3 DOF in that specific model. Recomputed rank labels match archived; raw JSON differs due floating-point/evironment. These are LOCAL JACOBIAN MODEL EXAMPLES, NOT general proof of human pose observability, and static-pose sensitivity is not absolute identifiability.
- X12 20 negative gate cases plus positive control independently rerun: 21/21 per-ID semantic match archived output. Exact output JSON bytes differ due formatting/environment. The script is a reference checker, NOT a tested NEXUS runtime. Logical gate labels vary from R38 canonical machine JSON; implement explicit exact enum normalization, not fuzzy green comparison.
- Owner/user permission or physical body reference not established by this toy replay.

## 4. New workspace SVK candidate — two distinct generations, one stale seal (MATERIAL)
User workspace.tar contains 164 entries with a self-described `QWEN_WORKSPACE` first-party SVK candidate (source under `nexus-omega/r38/svk_candidate/`) and a frozen manifest with 27 source entries.
CRITICAL: independently rehashing the EXACT TAR-ARCHIVED CANDIDATE BYTES against its included `MANIFEST.sha256` gives 25/27 MATCH, 2 MATERIAL SOURCE MISMATCH:
- `svk/models/ws01_phone_twin_synth.py`: manifest EXPECTED sha256 `2635c598eb353ac5c9a62588bbb344c2b724e0fae38ec93ee9fb2f0b42b3e881`; actual TAR sha256 `0b100e9510154fe14f41d6766edc4bfb60cbb1d6e01fe6a919c8cca57a449f49`.
- `tests/defs_q.py`: manifest EXPECTED sha256 `7a6b227ac0b4e71897a3a0a9a94ca253d81c4f063d4b2eb42b3e49ae8b1a5`; actual TAR sha256 `be42cf11d7493eea8e3eb9f419163dde0e5337349e49f60a28206f9754c994fa`.
The original candidate MANIFEST file itself hashes to `e632779395a345660197bd20fd6405279a17da5b8d71237320f7736873aed293`; this intact hash authenticates only the contents of THAT STALE FILE, not agreement with the actual delivered source bytes. No authorized post-hoc mutation of this original historical manifest. Exact patch provenance from expected source to actual code NOT PROVIDED; do not call it proven malicious modification.

Original TAR-ARCHIVED RESULT `results/RECEIPT.json` claims 79 executed, 40 PASSED_EXPECTED, 36 FAIL_EXPECTED, 3 FAILED_UNEXPECTED [Q14,Q19,SF-WS01-4], zero GAPS, aggregate_conforming=false, `FAIL_MACHINE_GATES` (semantic_ok, model_ok, independent_ok), existing consumer NOT_CONNECTED, real ABC source NOT_EXECUTED. Q14 lacks expected mounting-slip uncertainty/abstention reason, Q19 fails correlated-noise disclosure, SF-WS01-4 detects ignored slip. These negatives are valid discoveries, preserved verbatim as historical evidence. Original archived results are not a PASS and not superseded by a silent rewrite.

AXIOM INDEPENDENT CODE REPLAY:
- Isolated temporary OS filesystem (not original user uploads), Python `-I -B`, source-only; memory/CPU/time/file-output limits, no untrusted binary `.pyc` or remote model executed. First replay of candidate folder alone returned 79 test invocations, 76 expected labels, 3 SOURCE_GAP [U09,U10,U14] because GitHub readback source subdirectories were absent. Its aggregate code reported `aggregate_conforming=true` DESPITE SOURCE_GAP, a MATERIAL false-green risk for overall adequacy.
- Second replay with ALL relevant uploaded `nexus-omega/r38/` workspace source directories restored: 79 test invocations, 43 PASSED_EXPECTED + 36 FAIL_EXPECTED, 0 unexpected, 0 source gaps, aggregate_conforming=true; `FAIL_MACHINE_GATES` persists because independent_ok=false, existing consumer NOT_CONNECTED, actual original A/B/C not run, input source class SYNTHETIC. This is a real independently executed numerical REPLAY OF THE CURRENT UNSEALED DELIVERED SOURCE and proves only that specific synthetic run in a complete workspace; NOT reproducibility of the archived ORIGINAL FAILED run, not a signed/source-exact final executable integration, not an external registered reviewer and not a physical BodyTwin validation.
- The source `run_svk.py` rewrites its own candidate `MANIFEST.sha256` during runtime. New generated selfhash `591e4ce271932e0cfc5375db6c14e84de090d1bcf8823542abe060308b38d0a3` reflects a new run's output, NOT the original uploaded frozen manifest. Mandatory fix: freeze source before run, output execution witness to a distinct result directory, never modify the accepted source manifest, and bind explicit before/after source tree hashes.
- For repeatability, a green test must require unexpected_failures=0 AND source_gaps=0 AND missing_source=0 AND original_source_manifest_complete AND independent actor gate for whichever science grade requires it. Harness must not mark SOURCE_GAP as conformance.
- The candidate's Python `run_svk.py` has a HUMAN approval object `approved=True` sourced to a self-described workspace-chat response; this remains REPORTED_ONLY, NOT an independently verifiable operator signature or hardware capture consent. Purely synthetic tests require NO_DEVICE_ACTION and not forged physical owner authorizations.
- Synthetic A/B/C input replicas intentionally emulate the archived phone counts 6374/6366 and 6011/6003; are SYNTHETIC not private real OPPO replays. A NEW phone-twin candidate is a different artifact than the existing consumer. The candidate itself truthfully says NOT_CONNECTED and no original B/C.
- Source `test_source_commit=WORKSPACE_CANDIDATE_UNCOMMITTED`, not an authenticated GitHub commit. Its archived receipt `classification=IMPLEMENTED_OFFLINE_C1_WITH_CAVEATS_FIRST_PARTY` is a creator report; executing it independently here still does not prove Cursor's implementation ACK or commissioned external return.

## 5. Original R37 persistent limitations
- 6374 ACC + 6366 GYRO in the previously handled physical phone source; stationary-compatible magnitude (~9.81855 m/s² accel, ~0.002037 rad/s gyro), approximate 100Hz event-clock; original first/last sensor span ~63.6s with 363 postdeadline events per channel vs requested 60s, 50Hz prereg versus actual 100Hz.
- Android actual installed app `source_build` empty, owner approval original missing, full raw original transfer through authorized private GitHub receiver still open.
- M01 original 8/8 unit +10/10 synthetic independently executed in R37, but this workspace does NOT include the original Stage0 127368B ZIP; R38 Qwen code is a NEW research candidate, not original signed producer or current NEXUS runtime.
- M02 original 14/16 manifest failure preserved, wrong physical IMU counter (ACC+GYRO one co-located phone assembly) and no universal min3-IMU physics theorem. X11 constructive rank toy is evidence against blind minimum count, not a validated anatomical model.
- No independent on-body calibration/reference, real existing BodyTwin consumer real-source A/B/C, clinical/physical human body claim or production release in current upload.

## 6. R38 terminal & R39 readiness
Scientific output: substantial C1 progress—an offline modular, typed, testable candidate, independent current-source synthetic reproduction, adversarial failure discovery, and independent X11/X12 benchmark replays. But R38 cannot be called fully source-sealed, physically integrated or independently accepted.
TERMINAL = OPERATOR_REQUESTED_PHASE_CLOSED_WITH_MATERIAL_CAVEATS_C1_FIRST_PARTY_SYNTHETIC_IMPLEMENTATION.
CURSOR_BIND = REQUIRED_NEXT; no Cursor-authenticated actual original source and offline commit receipt was included in these 9 files, and no GitHub Cursor implementation commit was observed in PR382 at this review.
R39_READY = ONLY_AFTER_CURSOR_RETURN_AND_AXIOM_ADJUDICATION. Do NOT create a R39 implementation/foundation PR in advance or claim an already finished independent consumer.
Required Cursor next: exact private source intake; new, separately frozen R38 corrected source manifest (original 25/27 untouched); independently test 79 current source under full workspace, re-run 3 historical failing control fixtures against original failing source IF archived original code exists, independently reproduce R38-T21 plus source-manifest TOCTOU and source gap aggregate-negative tests; isolate/determine actual NEXUS BodyTwin consumer, private authorized A/B/C if source approved, no capture; source-exact GitHub Draft PR+run receipts+independent reviewer with truthful gate statuses. Then return explicit R38 terminal bind for AXIOM R39 stage selection.
