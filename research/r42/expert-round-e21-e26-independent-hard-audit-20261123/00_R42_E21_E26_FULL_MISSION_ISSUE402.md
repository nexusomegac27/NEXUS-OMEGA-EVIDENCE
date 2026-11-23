# NEXUS OMEGA · R42-E expert mission · source-exact Issue #402 copy

Canonical invitation URL: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/402
This file is a byte-level archival copy of the Issue #402 instruction body (not evidence that any external provider has acknowledged it).

# NEXUS OMEGA · R42-E · Externe Expertenrunde E21–E26 · source-exact hard audit

OBJECT = NEXUS_OMEGA_AXIOM_R42_E21_E26_EXTERNAL_HARD_AUDIT_AND_PUBLIC_WITNESS_20261123_R0
DATE = 2026-11-23 (Europe/Berlin)
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = EXPERT_MISSION_ISSUED_NOT_PROVIDER_ACKNOWLEDGED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R41 = ADMINISTRATIVELY_CLOSED_WITH_MATERIAL_GAPS
R42 = OFFLINE_IMPLEMENTATION_BOUND_CURSOR_REPORTED
EXPERT_QUORUM = NOT_ESTABLISHED
ALT_D_DO_NOT_RUN = ACTIVE; 14_PHYSICAL_GATES = HOLD
BODYTWIN_VALIDATED = NO; CONSENT_BIND = OPEN
NO_DEVICE_CAPTURE; NO_ADB_SENSOR_START; NO_APK_INSTALL; NO_MERGE; NO_HOSTINGER_WRITE; NO_WWW_WRITE; NO_CLAIM_PROMOTION
EXTERNAL_DIRECT_WRITE = DENY_PENDING_REGISTERED_ACTOR_AND_OPERATOR_AUTHORIZATION

## 0. Causal source anchor — do NOT substitute an issue or summary for raw source
- Parent Cursor handoff ZIP: `NEXUS_OMEGA_CURSOR_R41_TO_R42_CUSTODY_HANDOFF_20261123_R0.zip` 243264 B SHA256 `a606c459dfcb973307a6deae4928997918348d8ce8ef161ca0b755fc0ea6fd23`; Cursor now confirms `CURSOR_RECEIVER_ACK=YES`, prior handoff match.
- Current uploaded Cursor R42 return original ZIP `NEXUS_OMEGA_CURSOR_R41_TO_R42_CUSTODY_HANDOFF_RETURN_20261123_R0.zip` **4686 B** SHA256 `7082d8ed3192a9d99d157654b51b0ca2af4548b9f329d8ac24903f962a30f6bb`; independently rehashed by AXIOM, external sidecar MATCH, ZIP CRC PASS, internal 5/5 SHA256 MATCH. Stamp `2026-11-22T23:44:42Z`. This 4686 B ZIP contains FIVE report files + manifest, NOT the eight original source/witness files described below.
- Existing Cursor order: Issue #400; R42 source **foundation/order-only** Draft PR #401 HEAD `21db4552d91f39cb42ab54523537fd0aa4f8f136`; its four files are the research order/contract/W1 protocol, **not the Kotlin/FC2/W1 original runtime evidence**. Earlier R41 implementation PR #396 HEAD `ba3f187daa1949c712bba9b822ab6005d0ae6363`; R41 expert stage2 PR #399 HEAD `cc79821533b0344ae9d91181f59445749c8e2e5d`; W1 Issue #397. Do not treat a URL as an ACK or commit/PR as deployment.
- Claimed current Cursor R42 state: STOP_DEADLINE_GATE_EVENT_TIME_PLUS_DRAIN `PASS_OFFLINE_C1`, Python twin self-test `PASS`, FC2 `PASS_12_NEG_6_POS`, W1 raw HTTP `OBSERVED_8_OF_8_C1_REPORT_LEVEL`. `GRADLE_RUNTIME=NOT_ESTABLISHED`, `X15_PER_SAMPLE_RECONCILIATION=OPEN`, `STAGE2_FULL_REPLAY=NOT_EXECUTED`, `EXPERT_QUORUM=NOT_ESTABLISHED`. **These are producer reports, not independent source-exact replays.** Separate public BodyTwin GET from AXIOM was blocked with cache miss/not accessible: `AXIOM_CURRENT_RAW_HTTP_WITNESS=NOT_VERIFIED`, NOT `SITE_DOWN`.

## 1. Required exact byte sources — independent intake gate G0, one per artifact
Cursor reports:
| Object | Bytes | SHA256 (expected) |
|---|---:|---|
| ScientificImuStopDeadlineGate.kt | 4842 | d07e86c897d9897e6270a77a190ee856ca87c90ff77e48dcc89f5fdf1df695ac |
| ScientificImuCaptureEngine.kt | 14540 | 7c9457f972b5cb5e60ef468f6f7b9e5332f20b4176fd65d9495a392868108d17 |
| ScientificImuForegroundService.kt | 36049 | 65c57f547e6f322860ecdb5b39c3c0bfb23409d7e43379e8fb6344b07d4d9b63 |
| ScientificImuStopDeadlineGateTest.kt | 7529 | 0564b43ca59bed7d570b322be19b3f5c37eef10fe3fbee389db68380e9a4eb8b |
| stop_deadline_gate.py | 4450 | a48a2f10f98fef02490f8c4c9b5fe5fc7392c91883713d1241807b1548bc560e |
| fc2_gate_engine.py | 14348 | 3983e9f166a6c3cbeb29d76c2ee5ab8a9b64d44783e4ebf63f23cc452f12da3f |
| FC2_GATE_ENGINE_RECEIPT.json | 8082 | 83b587f320a07851f777f50736f145ec72364c317009df04b926f60e6e1da074 |
| W1_RAW_HTTP_WITNESS_RECEIPT.json | 12499 | d2e1a313b83fc6e03ca241d9e27076698664a0376eb6d36cf979a4ebe2fb9a29 |

**G0 rule:** Actual original source bytes must be fetched from a pinned immutable Git commit on a registered authorized branch, or independently received as original exact ZIP+manifest (private if necessary); hash ALL eight exactly by bytes, fail closed on any gap. Require repo path, object git blob SHA, base/head commit, actual diff to prior R41, approved branch, compiler targets and declared execution environment. No original private OPPO/capture records, keys, secrets or CAS may be pushed public. Public repo path only after public-safe review; otherwise private custody and redacted metadata. Report state `SOURCE_GAP` if unreceived, do not invent. Original `stage2` nine previously absent scripts arrived as additive 9/9 HASH_MATCH supplement but full independent replay remains `NOT_EXECUTED`.

## 2. E21 · independent Android/Kotlin Runtime & Temporal Semantics (PRIORITY 1)
Design adversarial `SensorEvent.timestamp` vs `SystemClock.elapsedRealtimeNanos()` vs receipt/delivery timestamp; events created before stop but batch-delivered after; stopwatch boundary [start,deadline); invalid zero/negative/overflow deadline; stop state-machine idempotency under race/Service lifecycle; flush, FIFO reorder/dedupe, UTC discontinuity, reboot/boot-id or incompatible clock domains; foreground notification/service stop. Explicitly audit whether implementation in actual CaptureEngine/ForegroundService routes through gate or is only a research twin. **At least 16 named negative tests plus 4 positive controls**, baseline red→repaired green on SAME code path, truth table for accepted/dropped/quarantined/stranded with sample IDs; terminal assertions `accepted + rejected + quarantined + pending == observed`. Never infer unknown generated events from requested Hz, prove losslessness only under stated assumptions. Distinguish original X15 6001/6000 per-ID source `OPEN` from X16 synthetic boundary exact; if original unavailable, do not claim causality. Independent clean Gradle/JVM build of actual app if authorized and environment suitable, otherwise `GRADLE_NOT_RUN` (no device/APK).

## 3. E22 · FC2 Evidence Engine / adversarial auth & software assurance (PRIORITY 1)
On **actual 14348-byte** FC2 source and corresponding 8082-byte receipt, independently attempt 12 reported attacks AND >=8 newly devised attacks with >=6 legitimate positives. Trust anchor: expected hashes/attestations signed or preauthorized by an independently controlled identity; content hashes alone do NOT prove authorship/authority; verified subject digest must bind exact source+test+runner+scope+version+nonce and reviewer; deny on TOCTOU, path traversal/symlink, duplicate JSON keys, numeric ambiguity, misleading canon, replay, revoked signer, mixed trusted/untrusted receipts, reused hash for multiple gates, fake second-party and mismatched build. Positives must pass or "deny everything" is not a PASS. Show actual `fail_before / pass_after` with R41 legacy source and R42 new source, never only a mock. Two separate evidence dimensions SOFTWARE vs PHYSICAL; each of 14 original physical gates remain HOLD. Align with in-toto Statement subject digest and OWASP logging controls, but do not pretend installed attestation/PKI if absent.

## 4. E23 · W1 public BodyTwin independent raw-byte/browser witness (PRIORITY 1, PARALLEL)
Read-only four allowlisted endpoints ONLY:
- https://www.nexus-mobile.de/bodytwin/
- https://www.nexus-mobile.de/bodytwin/live/current.json
- https://www.nexus-mobile.de/research/bodytwin/state.json
- https://www.nexus-mobile.de/bodytwin/updates/
Cross-check the claimed W1 receipt (12499 B) with genuine independently collected dual snapshots, preferably at least one feed interval apart; store HTTP code, response body byte length & SHA256, Date/Age/ETag/Cache-Control/Last-Modified/Vary, redirects, MIME, client clock separately. Compare `source_updated_at` or equivalent immutable source hash, `generated_at`/run_utc, reducer seq, embedded STATUS/LIVE/MEMORY canonical hashes and browser-rendered values. Conditional 304 must bind an independently stored cached 200 body; no body is not a 0-byte source. Same-host public feed is NOT independent ground truth. Historical `STATUS != EMBEDDED` remains OPEN until differential can distinguish legitimate projection/version, stale HTML/cache/service-worker and genuine semantic drift. Distinguish producer tick vs source change; never silently claim "site down" from timeout. **>=14 negative tests + 4 positive controls** including age/stale, 304 missing body, partial payload, misleading redirect, stale HTML vs fresh JSON, seq rollback, clock skew, forged valid claim, PII in public bytes. No Hostinger write/deploy.

## 5. E24 · Metrology, identifiability and measurement uncertainty
Independently compare M0 diagonal RSS (known inadequate under covariance) vs M1 full covariance/GUM Jacobian PSD checks vs M2 Monte-Carlo from sensor observations under mounting/common-mode/time-base uncertainties vs M3 genuinely independent calibrated angle reference (DESIGN ONLY, without device capture). Include yaw observability/gauge null model (accelerometer+gyro alone no absolute yaw without external cue), mismatched units/coordinate frame, noise vs accuracy, coverage with sample size/binomial interval, correlated scenarios, nonlinear near gimbal/singular geometry. Use BIPM JCGM 100:2008/Amd.1:2026 and JCGM 101:2008 as methodological source, NOT as automatic physical validity. >=10 negative + 4 positive controls. No claim "OPPO calibrated".

## 6. E25 · independent reproduction, source provenance and supply-chain gates
Design genuinely independent clean-room runner and track source receipts: git tree/blob SHA, unmodified raw bytes, SHA256, runner version/JDK/Gradle/Python/OS, deterministic seeds, actual exit/stdout/stderr redacted, artifacts checksums; verify old vs new code and that production Android path imports it. Defend fake build logs, stale runner, code-generation shadows, CRLF/LF, dependency substitution, non-hermetic network/side effects, missing 9 scripts replay status. Source class `ORIGINAL_EXECUTED`, `SYNTHETIC_EXECUTED`, `REPORTED_ONLY`, `DESK`, `NOT_RUN`. If full source absent, produce a bounded SOURCE_GAP matrix and independent test plan; no false app validated.

## 7. E26 · open architecture competition / nonredundant innovation
Solicit at least 3 fundamentally different alternatives to R42 components (event-time watermark ledger, independently pinned attestation, differential model-based testing, minimal offline evidence protocol, etc.) with explicit rejection criteria, attack/negative suite, deployment cost, offline fallback, no external compulsory runtime cloud, threat model and possible **REMOVE** recommendation. Primary hypothesis and counterhypothesis must be presented. No author may count as second party of own work.

## 8. Actor / research governance
Each external researcher is an invitation recipient, not a confirmed worker. `ACK` only upon author-distinct, verifiable, timestamped receipt; no self-asserted peer-review. For later expert quorum need >=3 authenticated, non-colluding, independently authored protocol families with declared pre-exposure; multiple models orchestrated through one shared actor/context without independence evidence count as one line at most. Operator-relayed unregistered reports accepted as advisory C1 design input only. All actual external GitHub write permissions remain DENY until explicit registration and operator grant. Researchers may return via operator relay into quarantine as not-authenticated. Source data must remain public-safe and privacy reviewed. No private secrets, raw capture or identifier release.

## 9. Return format, acceptance and no-go
Separate machine return for E21..E26 with `actor_id`, `auth_method`, `registration`, `preexposed`, `source_commit`, `expected_sha`, `observed_sha`, `code_execution`, `test_count`, `positive_control`, `negative_fixtures`, `original_vs_synthetic`, `red_before_green_after`, `uncertainty`, `C1`, `physical_gate_status`, `bodytwin_publication_status`, `independent_second_party`. For each claim quote exact source path + line span (when accessible) and checksum, include SHA256SUMS + zipped return in an approved GitHub private/preregistered path or operator-relayed exact ZIP; no fabricated address or source. PR remains Draft/Unmerged; output no real source if not authorized. 
Classification: `R42_EXPERT_DESK_SOURCE_VERIFIED`, `R42_EXPERT_SYNTHETIC_REPLAY_VERIFIED`, `R42_APP_JVM_INTEGRATION_VERIFIED`, `R42_PUBLIC_WITNESS_VERIFIED` are orthogonal and **do not** clear any physical/BodyTwin gate. Publish a negative conclusion when hypotheses fail. 
**Intake GO only for independent research**, not capture. `G0_SOURCE_EXACT` required before code-based runtime PASS.

## 10. Official reference anchors (research methods, not R42 results)
Android SensorEvent: https://developer.android.com/reference/android/hardware/SensorEvent
AOSP Sensors Batching: https://source.android.com/docs/core/interaction/sensors/batching
Android SystemClock: https://developer.android.com/reference/android/os/SystemClock
BIPM GUM/JCGM: https://www.bipm.org/en/committees/jc/jcgm/publications/
in-toto Attestation v1: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
RFC 9110: https://www.rfc-editor.org/rfc/rfc9110.html
RFC 9111: https://www.rfc-editor.org/rfc/rfc9111.html
OWASP ASVS 5: https://github.com/OWASP/ASVS

NEXT = CURSOR_8_SOURCE_OBJECT_CUSTODY_IF_PERMITTED + REGISTERED_AUTHOR_ACK + E21_E22_E23_REPLAY_FIRST + E24_E25_E26_PARALLEL → AXIOM_INDEPENDENT_RETURN_ADJUDICATION.

