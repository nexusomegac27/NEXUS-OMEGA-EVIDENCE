# NEXUS OMEGA — AXIOM Deep Research and Native Android Repair Contract
## AlarmManager / Kotlin IMU Foreground Service / Atomic Local Seal — 12 causal research rounds
### Canonical successor to OPPO R0-S5 source repair · 2026-11-01 · C1_DESCRIPTIVE_ONLY

OBJECT = NEXUS_OMEGA_AXIOM_ANDROID_ALARMMANAGER_NATIVE_SEAL_12_ROUND_DEEP_RESEARCH_AND_CURSOR_IMPLEMENTATION_20261101_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
PARENT = NEXUS_OMEGA_CURSOR_OPPO_NATIVE_STOP_SEAL_SOURCE_REPAIR_PROOF_BEFORE_RETEST_20261101_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_SECOND_OPPO_FAIL_ADJUDICATION_SOURCE_FIRST_FIX_NO_THIRD_RUN_20261101_R0
PREDECESSOR_COMMIT = ee6f27f58e74e4ab8f5be54cac5f00c9e30074a6
SOURCE_LINK = github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TEST_EXECUTION_CLASS = PURE_JVM_REFERENCE_ONLY_FOR_AXIOM_NEW_CODE
ORIGINAL_NATIVE_KOTLIN_SOURCE_AUDITED = NO
RAW_OPPO_APK_SEAL_GZIP_BYTES_REHASHED_BY_AXIOM = NO
DEVICE_FULL_7MIN_AFTER_DISCONNECT = NOT_ESTABLISHED
SOURCE_SAFETY_PRIVACY = NO_RAW_SENSOR_NO_DEBUG_IP_NO_SIGNING_KEY
PUBLIC_WRITE_API = OFF
EXTERNAL_AGENT_ACK = NOT_ESTABLISHED
GLOBAL_CUTOVER = NO
PIXEL9A = NOT_ADMITTED

## A. New Cursor S5 result — bound on operator-report level

A truthful SUCCESS_S5_SHORT_AND_ONLY is reported:
- Session short-alarm-stop-seal-20261101-s5-r2
- seenStart = true, seenSeal = true
- Native event sequence AlarmManager DEADLINE_FIRE -> STOPPING -> SEAL_OK
- 27/27 local S4 negative cases PASS, source and logs NOT independently fetched by AXIOM
- Seal JSON 864 B, claimed SHA256 bfca06560052a84bbef09b1c53d6abb12c26eb4119ee6486f229651125112a9f
- ZIP 28,990 B, claimed SHA256 3e40be1050932833128259eebd8bfee63a405b158617ab75b3be46204ef19960
- Gzip 28,272 B, claimed SHA256 718666c947ceca77f181bc4cfcfaf063b6c20b2358e654695b267b5bfd44ac6d
- FULL_UNATTENDED_NO_ADB = NOT_CLAIMED; third full trial remains HOLD
- Earlier two full unattended tests = FAIL_CLOSED preserved.

Those are real technical lead evidence *reported by Cursor*, NOT original binary rehash or confirmed independent published Android Kotlin code. S5 reduces the problem to stability of the now functional Alarm→Stop→Seal path under longer/no-ADB and process/battery conditions.

AXIOM has independently authored a PURE JVM Kotlin reference FSM and matching tests. Exact original GitHub source:
  reference/NativeStopSealReference.kt 7038 B SHA256 f9acb219aa9e8f7f922e7df39a35245f50dd1acb23a90b7336ae7e3c53037ba1
  reference/NativeStopSealReferenceTests.kt 5584 B SHA256 522ac02b2fe6ef8e45d8bb5414a950d5b9519a6f56ce61fefc85743c7d240fd0
Executed locally with actual Kotlin JVM compiler / Java: PASS 45 independent assertions. Scope: in-memory mock store and fake GZIP sealer, *no Android device, no real AlarmManager, no original Android code, no disk atomicity*. This reference is a concrete, compiled logic starting point, NOT an approved drop-in production implementation. The original production source and tested patched APK are still necessary.

## B. Twelve primary-source research rounds, falsifiers and required fixes

R01 — Trigger type/lifetime. Android AlarmManager listener-based alarms may be canceled when calling process has no components; PendingIntent alarms are retained while process sleeps but cleared on reboot. HYPOTHESIS: S5 uses a listener/in-process callback which survived short test but not prior long attempt. TEST: print actual overload, receiver class, notification and requestCode; kill app process in a non-destructive isolated fixture and compare alarm delivery to persisted record. FIX: for process-surviving expiration use explicit PendingIntent + manifest-declared non-exported receiver, never only OnAlarmListener. Source: https://developer.android.com/reference/android/app/AlarmManager.

R02 — Permission/routing. Android 12+ exact alarms typically require SCHEDULE_EXACT_ALARM or a narrow approved exception. Android 13/14 new installs may not have grant; canScheduleExactAlarms must be observed and SecurityException fail-closed. USE_EXACT_ALARM is restricted to designated user-facing use cases; never claim an IMU study automatically qualifies. TEST: actual Android/target SDK, manifest permission, canScheduleExactAlarms at ARM and exact SDK call, USER_ALLOW state, grant/revocation. FIX: use allowed policy-compliant exact clock only if already authorized; else measured inexact setAndAllowWhileIdle with disclosed latency or HOLD_TIMED_PRECISION. Never auto-bypass permission UI. Source: https://developer.android.com/develop/background-work/services/alarms and https://developer.android.com/about/versions/14/changes/schedule-exact-alarms.

R03 — PendingIntent identity and accidental substitution. Intent.filterEquals does NOT compare extras; FLAG_UPDATE_CURRENT can silently replace them. HYPOTHESIS: later generation overwrites prior STOP nonce/slot or callback points at stale Activity. TEST: schedule 2 distinct session IDs, request codes and immutable Uri.data; compare scheduled/received session, generation, sourceId, deadline. FIX: explicit receiver component, exported=false, immutable PendingIntent, unique per-session URI+persisted stable requestCode, session+generation+deadline verified against durable store; old alarms no-op, not START. No implicit LaunchActivity STOP fallback. Source: https://developer.android.com/reference/android/content/Intent and https://developer.android.com/reference/android/app/PendingIntent.

R04 — Doze and OPPO power management. Standard exact alarms are deferred by Doze; while-idle APIs can be rate-limited and not precisely on time. ColorOS background restrictions may materially alter execution; reports alone do not prove this caused our failure. TEST: actual dumpsys alarm/deviceidle/power/FGS and screen+charging state, without silently changing system power settings; time of SCHEDULED, DELIVERED, CALLBACK_ENTER. FIX: observed deadline slack budget, policy-compliant alarm selection, visible FGS when recording, no unauthorized battery-exemption grant or hidden wake lock. Sources: https://source.android.com/docs/core/power/platform_mgmt ; https://developer.android.com/develop/background-work/services/alarms ; https://support.oppo.com/en/answer/?aid=2171043.

R05 — BroadcastReceiver work budget. An alarm firing a receiver is not completed local ZIP/GZIP sealing: BroadcastReceiver.onReceive executes on main thread and has a short ANR window, goAsync does not grant unlimited runtime. TEST: log RECEIVER_ENTER/EXIT, owner service state, STOP_CONTROLLER_ENTER, GZIP_CLOSE, MANIFEST_COMMIT. FIX: receiver validates session/generation and dispatches minimal signal to already running legitimate service/writer executor, not full ZIP work in receiver or Activity. If service/process absent, no false native completion; go into recovery, review Android background FGS start restrictions and exact-alarm exception only if user-requested. Sources: https://developer.android.com/reference/android/content/BroadcastReceiver ; https://developer.android.com/develop/background-work/background-tasks/broadcasts ; https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start.

R06 — Clock and deadline basis. Handler.postDelayed uses uptimeMillis (does not advance in deep sleep) whereas elapsedRealtime includes deep sleep. SensorEvent.timestamp shares elapsedRealtimeNanos timebase. TEST: all scheduled/actual/stop times in device monotonic domain plus bounded host clock uncertainty, no assumed NTP exactness. FIX: persist stopDeadlineElapsedRealtimeMs and boot epoch, use AlarmManager.ELAPSED_REALTIME_WAKEUP if allowed; re-evaluate on receipt; a callback not executed cannot be PASS. Sources: https://developer.android.com/reference/android/os/SystemClock and https://developer.android.com/reference/android/hardware/SensorEvent.

R07 — Service restart semantics. START_STICKY may deliver null Intent; onDestroy is not guaranteed after abrupt kill; force-stop can suppress scheduled alarms. TEST: restart/null Intent, crash at RECORDING and STOPPING, unrelated process death, no default START. FIX: load actual durable source, mark RECOVERY_PENDING on interrupted capture, evaluate verified files and boot ID, never automatically mark uninterrupted SEALED. Source: https://developer.android.com/reference/android/app/Service.

R08 — Single writer and STOP transaction. HYPOTHESIS: Timer/Alarm enters STOP but concurrently active sensor writer or onDestroy cancels a pending close. TEST: concurrent alarm + user stop + duplicate broadcast, failure between STOPPING commit and unregister, gzip close, SHA, manifest. FIX: one serialized writer actor, idempotent per session; durable STOPPING before side effects; stop sensor event acquisition, drain writer, exact file seal and committed receipt, THEN stopSelf. The in-memory reference models gate ordering but actual Android Room/SQLite atomic implementation is still required.

R09 — Gzip/ZIP stream integrity. A filename and SHA alone do not prove gzip trailer or ZIP central directory were finished. TEST: GZIPInputStream full decode to EOF (CRC/trailer), ZipFile validate every entry, SHA/bytes of original closed segments, sealed manifest cross-bind. FIX: finish+close GzipOutputStream and ZipOutputStream, flush/sync underlying file where applicable; write sidecar with Android AtomicFile; commit SEALED only after verification, otherwise RECOVERY_PENDING. Sources: https://developer.android.com/reference/java/util/zip/GZIPOutputStream ; https://developer.android.com/reference/java/util/zip/ZipOutputStream ; https://developer.android.com/reference/android/util/AtomicFile.

R10 — Exact evidence and source reproducibility. The prior PR263 independent readback found 13/26 SHA256SUMS GitHub raw-byte mismatches. Those remain unresolved historical source conflicts. S5 local SHA is a claim until bytes accessible. TEST: device original→host private copy rehash; source/return distinct immutable byte digests; GitHub postpush raw files 100% rehash. FIX: save appended immutable erratum, do not retro-edit prior evidence; publish only synthetic/sanitized receipts to public GitHub, original private sensor data isolated.

R11 — Negative controls and honest C1. The S4 27/27 reported PASS does not include every real Android failure by default. TEST: nonce collision, wrong PendingIntent generation, duplicate deadline, ACTION_STOP typo, alarm grant revoked, process death, clock boot epoch change, gzip CRC truncation, low disk, Doze screen off, stop/service restart race, ADB safety rescue. FIX: each negative must lead to actual FAIL_CLOSED or RECOVERY_PENDING with native logs and event count. Real unit/model, real Android source CI, OPPO connected, OPPO disconnected and AXIOM independent private bytes are separate proof classes.

R12 — Progressive release, not another blind 7-minute attempt.
  L0: exact original Kotlin/AndroidManifest/Gradle code census, sources+hash, current service state and safe backup, no secrets.
  L1: confirm AlarmManager PendingIntent-based routing, permission and method; real Kotlin source/Android build and S4 negatives re-run against exact build.
  L2: real OPPO 30–45 sec visible/ADB-connected native stop+seal (S5 reported PASS; source review needed).
  L3: real OPPO short screen-off background (90–120 sec if safe), native unattended stop+seal; no host ADB stop; if fail => no L4.
  L4: exactly ONE authorized 7-min no-ADB full test with host connection audit; app native START/CAPTURE/STOP/SEAL before reconnect and no human input; independent SHA/CRC/manifest readback and safe original-retention.
  L5: independent AXIOM adjudication of exact source/timeline and GitHub immutable file blobs; only evidence-scoped PASS_NO_ACTIVE_ADB.
All stages require no destructive reinstall/permission bypass, no Pixel action, public POST OFF, C1 only.

## C. Critical implementation wiring for Cursor (illustrative contract, not original Android app code)

Use existing source; avoid duplicating the service:
  1. On valid visible App ARM: create persisted session id and generation, source build, device boot epoch, T_start, scheduled native deadline.
  2. On actual App-native START: establish recording, persist stopDeadlineElapsedRealtime; use exact user-authorized AlarmManager API or permissible inexact while-idle fallback and explicit immutable PendingIntent.getBroadcast targeting private StopDeadlineReceiver.
  3. Alarm Receiver: verify known action and session generation; log native DEADLINE_FIRE and queue signal to the SAME already running ScientificImuForegroundService/serial writer; do not run long Gzip/ZIP operations in broadcast main thread; if writer no longer exists, record RECOVERY_PENDING.
  4. The native service/controller checks deadline and session boot epoch again; stops SensorManager, drains and closes writer, verifies Gzip CRC, writes atomic manifest, emits seal hash and SEALED; finally stops service and cancels alarm for same session.
  5. All fallback calls from Activity, notification or ADB safety recovery invoke same close path but MUST label stopOrigin=APP_UI or ADB_ASSISTED_RECOVERY, not APP_DEADLINE.
  6. On sticky restart/null Intent or reboot, do not default START; reconcile actual original gzip and mark interrupted capture RECOVERY_PENDING if necessary. Do not mark on-time/no-ADB from later repair.

Suggested manifest receiver scope (ADAPT to actual package; do not add new permissions silently):
    <receiver android:name=".StopDeadlineReceiver" android:exported="false"/>
Recommended native alarm identity: explicit component + ACTION_DEADLINE_STOP + Uri containing unique session and generation (not extras-only) + FLAG_IMMUTABLE + appropriately scoped requestCode. Extras are untrusted context, all authoritative data must be loaded from private durable source.

Security: do not attach cleartext WAN/LAN debug endpoint, raw original IMU, ADB serial/mDNS, signing keys or personal device identifiers to GitHub. Never force stop or delete existing science as workaround. Android 13 OPPO A74 is the scope, no Pixel9a.

## D. AXIOM executed new code — cleanly bounded

Reference code paths in this same PR270:
  research/communication/oppo-native-app-independent-audit-20261101/reference/NativeStopSealReference.kt
  research/communication/oppo-native-app-independent-audit-20261101/reference/NativeStopSealReferenceTests.kt
Verified GitHub raw SHA source 7038 / f9acb219aa9e8f7f922e7df39a35245f50dd1acb23a90b7336ae7e3c53037ba1;
Tests 5584 / 522ac02b2fe6ef8e45d8bb5414a950d5b9519a6f56ce61fefc85743c7d240fd0.
Local Kotlin compiler compiled exact same bytes and Java executed: PASS 45 independent assertions.
Reference models: session ID/boot discriminator, monotonic deadline, stopOrigin partition, duplicate/stale/invalid event rejection, STOPPING before finalization, false-seal -> RECOVERY_PENDING and failed/restarted state. It does NOT implement:
  Android AlarmManager, exact alarm permission, manifest receiver, foreground service permission,
  actual Gzip/CRC, filesystem synchronization, atomic Room transaction, device lifecycle, battery behavior,
  host ADB-disconnected proof, private Android source deployment, or real OPPO test.
Cursor must replace in-memory store with audited durable commit and no mutable single in-memory-only authority; the reference methods must run on serialized background executor. Do not ship pure reference files as a real Android fix without integration and field tests.

## E. Terminal decision and next Cursor order

OBJECT = NEXUS_OMEGA_AXIOM_ANDROID_ALARMMANAGER_NATIVE_SEAL_12_ROUND_DEEP_RESEARCH_AND_CURSOR_IMPLEMENTATION_20261101_R0
S5_NATIVE_SHORT_STOP_SEAL = CURSOR_REPORTED_PASS_WITH_CAVEATS_C1
S4_NEGATIVES = CURSOR_REPORTED_27_OF_27_PASS
AXIOM_REFERENCE_KOTLIN = COMPILED_45_OF_45_ASSERTIONS_PASS
REAL_KOTLIN_PRODUCT_SOURCE_AND_APK = NOT_INDEPENDENTLY_AVAILABLE
FULL_UNATTENDED_NO_ADB = HOLD_UNTIL_L0_L3_PROVEN
PREVIOUS_TWO_FAILED_LONG_RUNS = IMMUTABLE_FAIL_CLOSED
PRIVATE_ORIGINAL_HASHES = NOT_INDEPENDENTLY_REHASHED_BY_AXIOM
WWW_PUBLIC_READ_ONLY = PRESERVE
PUBLIC_WRITE_API = OFF
GITHUB_OWNER_HANDOFFS = REAL_3_OF_3_PAST
EXTERNAL_AGENT_ACK = NOT_ESTABLISHED
CUTOVER_ACTIVE = NO
PIXEL9A = NOT_ADMITTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

NEXT_RETURN = NEXUS_OMEGA_CURSOR_OPPO_ALARMMANAGER_LONG_RUNTIME_GATES_AND_NATIVE_CODE_INTEGRATION_RETURN_20261101_R0

THE NEXT ACTION IS IMPLEMENT AND ATTEST SOURCE-BOUND LONG-RUNTIME GATES L0-L3, THEN IF PASSED RUN ONE REAL L4. No further generic architecture review, no third blind 7-minute attempt, no manual operator interaction, no deceptive PASS.
