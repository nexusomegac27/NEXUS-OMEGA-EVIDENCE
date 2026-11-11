# NEXUS OMEGA · AXIOM — OPPO native app independent adjudication — 2026-11-01 R0

OBJECT = NEXUS_OMEGA_AXIOM_OPPO_NATIVE_APP_AND_COMMUNICATION_GATE_INDEPENDENT_ADJUDICATION_20261101_R0
PARENT = NEXUS_OMEGA_CURSOR_OPPO_NATIVE_APP_COMMUNICATION_GATE_IMPLEMENTATION_RETURN_20261101_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
GITHUB_SOURCE_TIP = 77f26c0d1cfaf18b9c1addfac2e47444c614478a
PR263 = OPEN_NOT_MERGED_29_FILES
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_REAL_OWNER_GITHUB_CANARIES_ANDROID_DEVICE_REPORT_LEVEL_SHA_MANIFEST_PARTIAL
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SOURCE_SHA256SUMS = 13_OF_26_MATCH_13_MISMATCH
CI_EVIDENCE_PR263 = 8_OF_8_SUCCESS
GITHUB_OWNER_CANARY_HANDOFF = 3_OF_3_REAL_COMMENTS
OPPO_NO_ADB_DEVICE_TEST = CURSOR_REPORTED_C1_NOT_INDEPENDENTLY_REEXECUTED
ANDROID_NATIVE_SOURCE_IN_GITHUB = ABSENT_AT_REVIEWED_TIP
APK_ACTUAL_BYTES_ACCESSIBLE_TO_AXIOM = NO
EXTERNAL_INDEPENDENT_AGENT_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
GLOBAL_CUTOVER = NO
PIXEL9A = NOT_ADMITTED_NO_ACTION

## 1. Independent scope and positive evidence

Using connected GitHub REST, AXIOM retrieved actual commit 77f26c0d1cfaf18b9c1addfac2e47444c614478a, PR263 metadata (open/unmerged, 29 changed files), all eight successful checks including Semgrep and R27E, and GitHub issue comments 6557237199, 6557237474, 6557237772 and terminal return comment 6557308840. Independent GET of all three Canary comments confirms the commenter is repository OWNER account, not a distinct external receiver. The three immutable text Canary files in the Return match their stated byte sizes and SHA256, respectively:
CANARY_01 = 576 bytes, f239f445c3d20aad60880df8cab6dcdd24e429d1d6f43a25fd42264c812dc175
CANARY_02 = 624 bytes, e907bc87079f2a9fd3d745680fac3aec3f8a25d3a6b087de61d0e7eb8c59fedb
CANARY_03 = 694 bytes, df4a8b0f7b1bc7ac69fbb5f73c182796bbddeeacf5c0b29d0abc5b5f2d955d9e
The current GitHub API comment bodies match the published source payloads. This proves owner-origin public-safe document publishing and retrieval; not an authentic independent agent runtime, private telemetry delivery, or Android app server transfer.

## 2. Independent raw GitHub blob SHA256 audit

AXIOM fetched all 26 file blobs named in the Return SHA256SUMS, with encoding=base64 to preserve actual binary bytes. A separately self-tested SHA256 implementation computed raw file digests and compared with the signed-off SUMS manifest. 13/26 match and 13/26 DO NOT match. No file was missing in the census.

The actual EXECUTIVE.md original content is 1957 bytes SHA256 d5ff6fa1f2170f02044ae92c31624d94cfba01d9bea1543ff3a1fe2fb71142eb = MATCH. HANDSHAKE.md, P7_APK_INSTALL_IMU, P10_SCOPED_DIFFERENTIAL, the three CANARY text sources and other entries MATCH. It is incorrect to promote the published SUMS bundle to 26/26 verified or to assume its previously reported local 17/17 proves GitHub-pushed file integrity.

Below, all paths are relative to the Return folder; EXPECTED is the original SHA256SUMS entry, ACTUAL is the SHA256 of the immutable GitHub blob at the reviewed commit:

| File | EXPECTED | ACTUAL |
| --- | --- | --- |
| RECEIPTS/NO_ADB_OPERATIONAL_TEST.txt | 88b885db4cbf054b242ae74f57373c56595c3b8a18a53139203ee932169e78ad | ea013ac79e1d7eebd3f31b7d7510a2dbcf6b3e169f8c2b5613e551dad199fae4 |
| RECEIPTS/P0_INVENTORY.txt | dd1071972fab260bcbb46f0d7aa2964ffb424047a8b268a9c6d6626a04a360c9 | bdb130ebd63f5a39ef4b387f6966f2034c75e7826341c940b8366b623f4902e3 |
| RECEIPTS/P1_DEVICE_CENSUS.txt | 84828e4fa09dadbf4117d6517b0018a54bdd286c20c4d86821c87eb91714cdc3 | 57dcf7990f99b76616775f0afe13e7d95229201e6ab540ac9c7b47ec110577be |
| RECEIPTS/P8_FALSIFICATION.txt | f871df6dd4b7d77de83d53823a2f84307433ce65aff7b031c62da1dfa18b8f9d | a5d672b3471b5958888532655f20c37e473cabdb3270f2a7362dc80cf9d83895 |
| RECEIPTS/P9_CANARIES/HASHES.txt | 407e044474bf7de38b81bf2bc0f2e2e947e323889b132545bc16c17050b5a543 | fc67171409bcb93b2afe9f9baaf0235dd43c72fcd3ea3f71b3e7ec4b08adc2cd |
| RECEIPTS/P9_CANARIES/NOADB_HOST_PULL_HASHES.tsv | ba0b0b033b0eca2151d138d9f12cdd39fbce12bdfedbeaa891f4cbb29b2d6382 | fad95d0c6ec2393b493d5bbfc30c372cfa88b8d38374c37d17838a15a4f9ae2e |
| RECEIPTS/P9_CANARIES/POST_01.json | 58d093cf46405e8631bfa4ae23d3e27444de4cca3c9001ff029c8432105ce6f1 | 46f74bf68161509f791b228cc3d84e09c8590856a0f737dbe5ab1b6a730eec5c |
| RECEIPTS/P9_CANARIES/POST_02.json | f30eb628633f45837588673656ce5f0f00bbb30cb4e5674c6f3fa25b0498c26b | 851d2161e9a2d966bb26bd619c46fc9c68bbf35afd03b69f63bf68340bf11604 |
| RECEIPTS/P9_CANARIES/POST_03.json | d27cb4190c84b37b34a821d69c1f454c0870c9bbae499ab0edefe33e3e94cb8f | 0314587d2498a368cc3e9beda6a99218fa528f8ec5e205009aadcce964ad6091 |
| RECEIPTS/P9_CANARIES/READBACK_01.json | 278988ef1a2e55255c0ab4494406d9247b204019b4babc18615d81a906b3b8fe | 8a3495c3763a6286d9737df437b58036a2cbe681f525c95d7cef826351c696d9 |
| RECEIPTS/P9_CANARIES/READBACK_02.json | 16c7639265276e0a5014cf147680cddff7ad09dfdeb7679130130e11c24a0ebd | bc7b97137901efe2be05922c7f088cc93343f7164ddee95085110b45f42729fe |
| RECEIPTS/P9_CANARIES/READBACK_03.json | 57d1f816c55e0aa724a2405cf348f0df4d9686cd85e978fe0e207fc0ba034ca6 | b1f9a2cecf4f93775ece5bad28ff3bf96239e9a7145e6ba34bfbaccf19a821f0 |
| RECEIPTS/P9_CANARIES/READBACK_LIST.json | 46caff0a7c73d03919ce4342d32cceae032cbb9d348d8cdd7494e6ed894e17aa | 288157dcb4bcb52dfb9174989e6425c558a53784575188beffb09559766e88e5 |

Raw base64 content includes UTF-8 BOM for certain files, but naive CRLF substitution of NO_ADB/P8 actual blobs does not reproduce declared hashes. Cause not established. Do NOT replace original Git historical evidence, mark SOURCE_INTEGRITY_PARTIAL_C1 and require an append-only erratum preserving both digests and exact transformation/reason if established.

## 3. OPPO reported device evidence, no invented independent binary audit

Cursor public P7 receipt reports OPPO A74 CPH2219 Android 13 SDK33, app id com.nexusomega.maps, versionCode 10 -> 11, versionName 1.3.7-communication-gate-vc11, successful non-destructive adb install -r, 22,897,281-byte debug APK with declared SHA256 BCD5A7C1158EB5BA481E769A676D047EFD25E80F12CFE3FED3E9B75D653A90CA, retained older scientific segment/navigation SHA, and short IMU capture with acc_count=1311, gyro_count=1291.

The published NO_ADB receipt reports another approximately 414.7s two-segment session with 41,534 accelerometer and 36,307 gyroscope samples, two sealed gzip payload SHA and one package ZIP SHA. ADB disconnected during capture and host rehash on reconnect are Cursor-reported in the receipt, but actual private binary gzip/zip and APK bytes were not available for AXIOM independent rehash, and NO_ADB receipt GitHub hash mismatches its SUMS entry. Thus REAL_DEVICE_FUNCTIONALITY = CURSOR_REPORTED_WITH_GITHUB_SOURCE, not independently device-reexecuted or binary-reproducibly built. The local 28/28 JVM test suite is likewise a Cursor report, not one of the PR263 GitHub Actions source-tested Android jobs. GH CI 8/8 checks the EVIDENCE PR only.

P8 has a material functional concern: a wrongly formed stop ACTION on the exported LaunchActivity reportedly reaches the START branch (undesired acquisition). Describing NEG_02 as PASS_DOCUMENTED does not make it a correct fail-closed negative. Fix unrecognized actions so they NEVER start capture, then test against actual device/service state and segment increments. A missing runtime_status.json after stop is insufficient proof alone.

## 4. Privacy, traceability and local Android source gap

The public return, including CANARY01 and other receipts, contains an internal Wi-Fi ADB endpoint and a device-specific mDNS debugging identifier. These are NOT credentials, but are unnecessary network/device debugging identifiers. No such values are repeated in this new document. Future public receipts MUST redact them; Operator should review disabling WLAN debugging after testing and re-pairing/rotating debug credentials if warranted. Historical public GitHub records remain and a follow-up commit alone cannot undo their previous exposure. Do not claim attack/exfiltration from presence alone.

The P10 report identifies a locally hosted PFV Android worktree, local-path Git origin and 24 differential rows. The native Android implementation source and APK actual bytes are NOT published in PR263; this is an honest source-quarantine/capability gap, but the file SHA inventory is not an independently auditable app source. A separate scoped source-only, privacy-reviewed GitHub branch/repository with actual original Kotlin/Gradle/Manifest bytes and independent Android CI is required for a reproducible release. Avoid unreviewed private sensors/APK/signing keys/GPS/credentials.

## 5. Release-by-gate decision

G0 Source inventory: CURSOR_REPORTED_PASS, original Android source unavailable.
G1 OPPO census: CURSOR_REPORTED_PASS, P1 raw GitHub hash mismatch.
G2 App install/IMU: CURSOR_REPORTED_PASS_C1, binary no independent rehash.
G3 Local outbox/retention: CURSOR_REPORTED_WITH_CAVEATS, raw binary/restart rehash absent.
G4 Owner GitHub document lane: 3/3 REAL_API_COMMENT + direct body readback, OWNER_ONLY, NO independent external actor.
G5 Security/privacy: HOLD_SCOPED_FOR_PUBLIC_DEBUG_META_AND_UNKNOWN_STOP_ACTION.
G6 Capture when ADB disconnected: CURSOR_REPORTED_PASS_C1 with GitHub receipt mismatch, not independently reexecuted.
G7 Real Android negative/JVM tests: 28/28 LOCAL_REPORTED, GH CI not native Android build.
G8 Actual Android source push/reproducible binary: HOLD_LOCAL_SOURCE_ONLY.
G9 GH evidence CI: 8/8 PASS; SHA manifest: 13/26 MATCH, 13 MISMATCH.
G10 Pixel 9a: NOT_ADMITTED_NO_ACTION.

TERMINAL_VERDICT = PASS_WITH_MATERIAL_CAVEATS_C1_OWNER_GITHUB_HANDOFF_REAL_OPPO_DEVICE_REPORTED_SOURCE_INTEGRITY_PARTIAL
PUBLIC_READ_ONLY = PRESERVE
EXTERNAL_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
CUTOVER_ACTIVE = NO
PIXEL9A = NOT_ADMITTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## 6. Narrow mandatory Cursor follow-on

R0 Preserve originals, old science, local source/dirty S1-S5, APK and source-safe private device artifacts; no destructive changes.
R1 Append-only hash erratum for the 13 mismatches with actual Git blob bytes and exact pre-push local bytes; independently verify root cause (Git newline/encoding transformation possible, NOT established). Do not rewrite original manifest as if originally correct. Re-run 26-file source-bound verification on an explicitly versioned successor.
R2 Correct unknown STOP/START Intent handling to FAIL_CLOSED on all unexpected actions; execute and capture device negative test, service state and new-segment-count check.
R3 Public security minimization: future evidence strips debug network/IP/mDNS/serial. Operator review of wireless debugging when finished; no historical rewriting without separate authorization.
R4 Source-only privacy-reviewed native Android repository/PR, no secrets/raw sessions or debug binaries; real Gradle build/test CI, original APK hash witness from authorized private route, no source substitution.
R5 Re-run authorized non-destructive OPPO E2E after fix, ADB-disconnected local capture and offline queue recovery; independently attest preserved prior sessions. On missing device or operator rights keep precise HOLD.
R6 Preserve real 3/3 owner GitHub comment proof; no external-agent independent ACK until actually demonstrated and independently reviewed.
R7 Keep PR263 open without merge until integrity erratum and scope-specific independent acceptance; Pixel A36a/A36b remain NOT_STARTED.

NEXT_RETURN_OBJECT = NEXUS_OMEGA_CURSOR_OPPO_NATIVE_APP_EVIDENCE_INTEGRITY_AND_SOURCE_REPAIR_RETURN_20261101_R0
