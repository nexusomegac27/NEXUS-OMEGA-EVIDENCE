# AXIOM → CURSOR / NEXUS MOBILE · OPPO A74 self-diagnostic offline-first evidence & Wi-Fi debugging research — 2026-10-16 R0

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_OPPO_NEXUS_APP_SELF_DIAGNOSTIC_OFFLINE_FIRST_CONNECTIVITY_MAXI_ORDER_20261016_R0
AUTHORITY = OPERATOR_DIRECT_NEXUS_APP_DEBUG_DIAGNOSTICS_CONNECTIVITY_AND_DETAILED_LOGS
RECIPIENT = CURSOR_PRAXIS
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PREDECESSOR = NEXUS_OMEGA_AXIOM_OPPO_A74_DELAYED_SHELL_LOG_DELTA_ADJUDICATION_20261016_R0
REPO = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PR117_PREDECESSOR = OPEN
R3 = SEALED_PRESERVED
R9 = OPEN_CONTINUITY
R10 = CLOSED
R11 = OPEN_NONINTERFERENCE
CURRENT_SOURCE_STATE = DESIGN_PLUS_TESTED_PURE_EVENT_REDUCER
NEXUS_APP_RUNTIME_CHANGED = NO
PIXEL_APP_INSTALL = NO
NEW_SENSOR_CAPTURE_OR_WORKER = NO
HOSTINGER_403_404_BYPASS = NO
RAW_LOGS_PUBLICATION = NO
CLAIM_PROMOTION = NO

## 0. Operator situation — exact causal sequence

Operator states OPPO wireless debugging repeatedly switches itself off, disrupting recent live access. This is **operator observation, not a root-cause measurement**. Preceding one-shot OPPO audit returned DEVICE_NOT_ACCESSIBLE, ADB EMPTY, private Hostinger 403/404; Column A fresh device metadata ABSENT, Column B 2026-10-15 historical soak BOUND. Device/server original ZIP 8/8 identity NOT_ESTABLISHED, 0002/3/4 device originals gap.

Delayed shell forensic delta: 5563-byte SOAK EXEC SHA256 f33a5772f7b30b73da797a88445ffc4b43e90a333fd67b454b6e35c21fb894f1, CURSOR_LOCAL_MATCH, but enclosing shell exit FAILED and cause NOT_ESTABLISHED, raw stderr/stdout not available to AXIOM. Return EXEC/HS/WALLS/RESULT/SUMS hashes from Cursor are RECEIPT_REPORTED_ONLY, not an independent AXIOM rehash. No new scientific validation claimed.

OPERATOR GOAL: Make NEXUS App capable of operating as its own transparent, on-device *research diagnostics application* and of automatically sending exact, source-bound, detailed diagnostic files to AXIOM via **an actual authorized private evidence channel**; prevent disruption from transient ADB/Wi-Fi disconnection. This does NOT grant a normal Android app the privileged power to toggle Secure System Wireless Debugging or make debuggable APKs safe for broad production use.

## 1. External primary research — scientific papers and immutable public implementation pins

Platform FIRST PARTY:
1. Android adb: https://developer.android.com/tools/adb . Android 11+ legacy wireless pairing, Android 17+ ADB Wi-Fi 2.0 with adb 37.0.0+ host, trusted network and mDNS. Check actual OPPO OS and host tool versions before applicability; newer adb host tools alone do not upgrade older Android's adbd to Wi-Fi 2.0. No undocumented hidden settings hacks. https://developer.android.com/studio/debug/dev-options .
2. Offline First: https://developer.android.com/topic/architecture/data-layer/offline-first ; WorkManager: https://developer.android.com/develop/background-work/background-tasks/persistent . Use persistent local source of truth, network-constrained UNIQUE upload work, bounded exponential retries, resume and idempotence. WorkManager is NOT a real-time 100 Hz sensor loop or guarantee of exact scheduling.
3. FGS and OS restrictions: https://developer.android.com/develop/background-work/services/fgs/changes , https://developer.android.com/develop/background-work/services/fgs/service-types ; OEM-specific battery restrictions must be observed, not assumed away.
4. Android SensorEvent timestamp docs https://developer.android.com/reference/android/hardware/SensorEvent and ConnectivityManager callbacks; never confuse WALL UTC / sensor monotonic / server time.

PEER-REVIEWED:
AWARE (Ferreira et al. 2015), DOI 10.3389/fict.2015.00006: native context instrumentation, local/remote recording and battery limits. Source https://www.frontiersin.org/journals/ict/articles/10.3389/fict.2015.00006/full .
RADAR-Base (Ranjan et al. 2019), DOI 10.2196/11734: high-resolution mobile sensor stream, modular ingestion, privacy and backend separation. https://mhealth.jmir.org/2019/8/e11734/ .
Missingness and quality: https://pmc.ncbi.nlm.nih.gov/articles/PMC10231441/ (data completeness changes feature validity); 2026 systematic scoping review https://pmc.ncbi.nlm.nih.gov/articles/PMC13013828/ (stream missingness/duty cycles frequently unreported).

SOURCE-EXACT GITHUB FOOTPRINTS (commit pinned from connector, COPYING NOT AUTHORIZED BY CITATION):
- OpenTelemetry Android, Apache-2.0: https://github.com/open-telemetry/opentelemetry-android/tree/b4b9c307a35bd721304360589e59941351b7165c . Features include offline-disk buffer, network change, crashes/ANR, redaction; evaluate compatibility and data budget.
- Harvard Beiwe Android, BSD-3-Clause: https://github.com/onnela-lab/beiwe-android/tree/5eb833ce413fc3b7c52e1e2790b01c8d584df028 . Research-grade native Android sensor configuration and data provenance; do not import broad clinical/privacy collection.
- AWARE Android, Apache-2.0: https://github.com/awareframework/aware-client/tree/f77e873baaedfc649fd39ca8f3547f914c3e6b32 . Plugin-style sensors and local storage; scrutinize old SDK/Android permissions.
- RADAR passive app, Apache-2.0: https://github.com/RADAR-base/radar-prmt-android/tree/4e17dc986f877576a79316eab97086293f3bab96 . Data sources and report schema; do not import Kafka/Firebase dependency by default.
- Google Now in Android, Apache-2.0: https://github.com/android/nowinandroid/tree/a49ed253d75e61a2b6ab80a8da677b57437b08eb . Reference for unique WorkManager offline-first, not mandatory dependency.

Each GitHub pin is REAL repo/commit existence read via the connected GitHub API on 2026-10-16. Scientific primary source ≠ code license ≠ evidence our installed OPPO app uses that code. Decide by source/target SDK/API compatibility and verified upstream behavior, not star count.

## 2. Code location and strongest operational blocker

Connected GitHub owner account has NEXUS-OMEGA-EVIDENCE, NEXUS_GROK-QWEN, NEXUS-OMEGA-QWEN-INDEPENDENT-VALIDATION, nexus-omega-r5-validation-20260904, NEXUS-OMEGA-AGENT-REGISTRY, rapid-wind-sand-finch, NEXUS-OMEGA-GROK-SOFT-LINEAGE. Main recursive trees were inspected and NO complete installable Android NEXUS App source structure (AndroidManifest.xml + Gradle + app/src/main) was located; only an isolated R21 example Kotlin companion. Therefore AXIOM cannot truthfully rebuild or install NEXUS App. Cursor MUST locate the TRUE existing authorized local Android app source + build identity (package ID, signer SHA256, versionCode/Name, Gradle/AGP, min/target/compile SDK, branches) through the established local authorized workspace. NEVER invent a remote repository, guess path or create an unrelated Android app pretending to be NEXUS.

First preflight read-only: map installed package/build to source, backups, capture process, battery profile, ADB version and device OS; verify whether adb is actually OFF, merely paired/disconnected, not discovered via mDNS, server unreachable, or offline. Do not conflate Wi-Fi IP change with loss of sensor events. If device unreachable, start offline app source research/build only on real available source; no system-level intervention.

## 3. Implement an **in-app diagnostics lab**, NOT privileged system ADB

D0 BOUNDARY: A normal unprivileged Android app cannot programmatically force Developer Options wireless debugging ON on stock Android, cannot silently perform privileged adb pairing, cannot bypass user trust, root, or enterprise policy. In-app research diagnostics must not set android:debuggable=true in release and must not expose sensitive diagnostic data to external debuggers. Provide honest on-device UX "SENSOR CAPTURE", "APP HEALTH", "WIFI", "ADB: ONLY IF EXTERNALLY VERIFIED", "PENDING UPLOAD", "LAST PRIVATE RECEIPT" as separate independently observed statuses. No synthetic green badges.

D1 APP OBSERVABILITY: Minimal Kotlin/Android library module with lifecycle/FGS/process state, sensor requested vs observed intervals from actual SensorEvent timestamps, monotonic sequence, duplicate/out-of-order/gap, wall-UTC separately, network type/connectivity callbacks, upload queue and source API outcomes. Android manifest permissions must be minimal; no GPS, contacts, SMS, accessibility, nearby device scanning or root. Privacy and purpose statement C1. ADB presence cannot be inferred from Android Wifi connectivity or an app's own network; host-side adb metadata is a separate source class.

D2 LOCAL EVIDENCE: App-private, append-only immutable bounded segmented diagnostic journal; defined file encoding + schema + source class; use durable SQLite/WAL or fsynced segments, atomic segment close, per-segment SHA256 and previous-segment hash chain, crash consistent recovery, actual byte rehash. Distinguish metadata-log hash chain from actual raw sensor ZIP chain. Preserve source-time and observed-time, monotonic timebase and order. Define storage cap and never silently overwrite old segments; report DATA_DROP_EXPLICIT if resource exhaustion, preserve last valid bound snapshot. Only required data. Encrypt at rest where justified and handle key rotation; no hardcoded secret.

D3 OFFLINE-FIRST EGRESS: Existing WorkManager unique upload scheduling with explicit NetworkType.CONNECTED, exponential backoff + Retry-After/JITTER/rate-limits, nonduplicating idempotency key = session+segment seq+SHA, byte-exact HTTPS request on **previously authorized and verified PRIVATE Hostinger evidence endpoint**. Do NOT assume that endpoint exists or reuse public_html/WWW URLs. Reject plaintext/insecure connections and server hash mismatch, never discard local data on HTTP 204 or sender-self-ACK alone. Remote receiver must independently read ORIGINAL committed bytes, hash, return authenticated receipt; client deletion/retention according to operator policy. HTTP 403/404 = AUTH_SCOPE_GAP, not reconnect loop or bypass. ADB is never a data transport dependency for normal app operations.

D4 HOST ADB DIAGNOSTICS: On an *authorized workstation*, without device write and only if already connected, record adb version, server-status, devices -l, mdns listing, network changes/time to reconnect and whether the Android device is genuinely supporting ADB Wi-Fi 2.0. For Android <17: do not claim the 2026 2.0 fix works; older paths require legitimate user trust pairing, Wi-Fi and mDNS. DO NOT run unauthorized adb tcpip 5555 or adb kill-server under active capture, force Android settings, obtain root or disable OEM security. If none accessible, return ADB_SOURCE_GAP and focus on D1–D3.

D5 PRIVATE LOGS TO AXIOM: Cursor must send **actual detailed original log files**, not only hashes or summaries, via a real private registered Hostinger custody channel or another actually available authorized private connector; provide nonpublic object pointer/read permission to AXIOM if capability exists. Fields: raw shell command (redacted), exact numerical exit, PID, start/end UTC and monotonic, stdout original-bytes size/hash, stderr original-bytes size/hash, adb/FGS/Wi-Fi/HTTP event metadata, package/source commit, private device-upload manifests, original upstream ack, receiver readback. Segregate credentials/PII, sealed private original bytes, redacted public manifest. At no point publicly post /10_TO_AXIOM path with source secrets, private SSIDs, IPs, token, sensor raw recordings. Hostinger has previously returned HTTP403/404 for the private API and connected Hostinger AI Builder does not control this existing VPS. Until a genuine authorized private reader can retrieve actual bytes independently, AXIOM_INDEPENDENT_RAW_LOG_REHASH = NOT_ESTABLISHED. Avoid user download/manual courier.

D6 NON-INTERFERENCE: Do not unseal R3, stop capture, reset current OPPO app, perform new capture work, change Android OEM battery settings, reboot, change ADB pairing or install/debug APK during current data acquisition. Build/test offline separately or on emulator; for later OPPO patch install require exact original APK signer/source, backup, verified safe capture boundary and operator-authorized read-only preflight; if installation would replace a still-running capture process, HOLD_CAPTURE_NONINTERFERENCE. Pixel 9a remains HOLD_EVIDENCE and needs explicit later install approval.

## 4. Falsification and quality metrics (actual executed counts, not merely proposed)

Minimum independent negative suite N01–N16:
N01 Wi-Fi internet loss preserves local sensor source event and journal.
N02 ADB vanishes while app network works; source classification remains separate.
N03 app process crash during segment flush; recover through WAL/atomic manifest.
N04 at-least-once duplicate upload leads to exactly one accepted receipt, no silent local wipe.
N05 malicious/wrong hash or body size from server -> quarantine and retry policy.
N06 sustained HTTP403/404 -> scoped AUTH HOLD, no unauthorized bypass or credential requests.
N07 HTTP429 Retry-After, jitter and permanent backoff.
N08 out-of-order/duplicate monotonic event.
N09 reboot/monotonic reset different session -> no false regression or cross-session chain.
N10 low storage/high watermark -> bounded backpressure and visible data drop warning.
N11 private log includes SSID, serial, auth token or private path -> public redaction enforced.
N12 public GitHub/raw log leak attempt blocked.
N13 foreground service/OS permission deny -> visible SOURCE_GAP, never hidden background guarantee.
N14 Android OEM power saving and process eviction -> source recorded, no impossible uptime claim.
N15 mistaken OPPO scientific success triggers Pixel installation -> fail closed.
N16 mismatched device zip/Hostinger zip despite identical JSON receipt -> NOT_ESTABLISHED.

Evidence metrics: capture duty-cycle and source event timestamp percentile gaps, packet missingness, uptime observation vs last successfully observed, WIFI connectivity percent, ADB separately monitored only by an authenticated host observer, private upload lag and queue depth, number of hash-vs-readback matches, retries by class, crash and ANR counts, CPU/battery/performance overhead. Preregister denominator and timebase, missingness, synthetic baselines and OOS holdout before conclusions. A live viewer status ≠ actual sensor event receipt ≠ science validation.

A small public-safe research reference with 10 synthetic negative cases is already written under this order's research folder. It is NOT installed Android code and not proof of future production logging; verified standalone deterministic reducer 10/10 isolated in the AXIOM source runtime. Future native Kotlin implementation should preserve the tested semantics (idempotency, predecessor hash, monotonic per-session, source class).

## 5. Cursor steps — full implementation conditional on real sources

G0 receive this pinned operator-governed order; independently read original R9 PR113/114/117 and delayed shell return, respect R3.
G1 discover exact installed OPPO app source/Android API/toolchain and actual already authorized workstation/device/host accesses; record path redacted in GitHub. If absent, return SOURCE_GAP explicitly; no fake build.
G2 perform empirical differential diagnosis of Wi-Fi vs ADB vs FGS vs app upload as available, preserving logs and exact shell exits; no reboot/ADB restart.
G3 implement the modular Android research diagnostics D1/D2/D3 behind runtime-off configuration, compile and run all offline tests in isolated environment. Reuse minimal dependencies, document fallback/migration/rollback, battery and privacy limits.
G4 test target on emulator/synthetic lab before any OPPO deployment; run N01–N16 and record which truly executed with commands, version, seed, stdout/stderr, data hashes and failure witness.
G5 if AND ONLY IF safe authorized OPPO deploy pathway and existing capture idle/safe boundary are proven, prepare minimal same-signer patch upgrade and separate installation permission check. Otherwise no live app change; preserving 485-minute historical soak matters more than guessed autonomy.
G6 enable private byte-exact log egress only when authenticated server archive ingress and independent readback are actually verified; credentials in private vault not GitHub, never direct-to-ChatGPT phantom pipe.
G7 receiver should send source-exact RETURN: 01_EXECUTIVE, 02_APP_SOURCE_MAP_AND_SIGNER, 03_ADB_WIFI_DIAGNOSTIC, 04_OFFLINE_LOG_STORAGE_AND_QUEUE, 05_PRIVATE_HOST_CUSTODY_READBACK, 06_TEST_LOGS_AND_NEGATIVE_CASES, 07_SECURITY_PRIVACY, 08_PIXEL_GATE, 09_SHA256SUMS_DETACHED, 10_HANDSHAKE, plus original private safe redacted stdout/stderr where authorized; all exact bytes and hashes. Owner public-safe GitHub receipt only; no unregistered expert slot, protected main merge or claiming first-party APP production deploy from GitHub alone.

DONE means: NEXUS APP diagnostics tested with real app source and exact instrumentation; offline persistence tested with forced network failure; private server truly accepts and independently rehashes original payloads; OPPO noninterference established; original shell stdout/stderr returned with verifiable bytes. Missing any item -> PASS_WITH_CAVEATS or HOLD_SCOPED, not success-by-design.

## 6. Governance and final

CURSOR_PUBLIC_GITHUB_ORDER = SEND_ONLY
CURSOR_ACTUAL_RECEIVE = PENDING
CURRENT_CONNECTED_APP_SOURCE = NOT_ESTABLISHED
CURRENT_OPPO_DEVICE_ACCESS = NOT_ESTABLISHED
CURRENT_PRIVATE_LOG_INGRESS = NOT_ESTABLISHED
NEXUS_APP_SELF_DIAGNOSTIC_APK_INSTALLED = NO
PIXEL_APP_INSTALL = HOLD_EVIDENCE
R3_SEALED = YES
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = CURSOR_DISCOVER_EXISTING_AUTHORIZED_ANDROID_APP_SOURCE_AND_IMPLEMENT_OFFLINE_RESEARCH_DIAGNOSTICS_THEN_PRIVATE_SOURCE_EXACT_RETURN

Design goal: the scientific instrument must keep its observations when communication is lost; communication may recover later without retroactively erasing any epistemic gap.