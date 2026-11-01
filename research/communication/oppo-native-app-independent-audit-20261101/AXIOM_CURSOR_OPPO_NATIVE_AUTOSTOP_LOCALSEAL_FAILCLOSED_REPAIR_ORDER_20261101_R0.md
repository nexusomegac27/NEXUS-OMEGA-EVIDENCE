# NEXUS OMEGA · AXIOM → CURSOR
## OPPO Native Auto-Stop / Local-Seal Fail-Closed Repair + Unattended No-ADB Retest
### 2026-11-01 · C1_DESCRIPTIVE_ONLY

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_OPPO_NATIVE_AUTOSTOP_LOCALSEAL_FAILCLOSED_REPAIR_ORDER_20261101_R0
PARENT = NEXUS_OMEGA_CURSOR_OPPO_UNATTENDED_NO_ADB_CAPTURE_AUTONOMY_PROOF_RETURN_20261101_R0
PARENT_ORDER_COMMIT = cb6d66800a1fbfc6579c393b4d20ee683c655714
PARENT_ORDER_PR = 267_OPEN_UNMERGED
PREVIOUS_AX_ADJUDICATION = ed1f0b24edc3c67e29b7714c827d05aafda7bd83
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = FAIL_CLOSED_C1_UNATTENDED_START_AFTER_DISCONNECT_BUT_NATIVE_AUTO_STOP_AND_LOCAL_SEAL_ABSENT
PASS_NO_ACTIVE_ADB_SESSION = NOT_MET
REPORTED_START_AFTER_DISCONNECT = PASS_APPROX_97_5_SECONDS_AFTER_ARM
NATIVE_AUTO_STOP = ABSENT
LOCAL_SEAL = ABSENT
CAUSE_REPORTED = FGS_STICKY_ONDESTROY_CANCELPENDING_WITHOUT_LOCALSEAL
FULL_RETURN_ORIGINAL_BYTES = LOCAL_TRANSFER_ONLY_NOT_INDEPENDENTLY_READ_BY_AXIOM
OPPO_DEVICE_CURRENT_STATE = NOT_INDEPENDENTLY_OBSERVED
OPERATOR_MANUAL_INPUT = NONE
PIXEL9A = NOT_ADMITTED
PUBLIC_WRITE_API = OFF
CUTOVER_ACTIVE = NO
EXTERNAL_AGENT_ACK = NOT_ESTABLISHED
FRAMEWORK_V1 = CLOSED_LIVING
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## I. Independent AXIOM admissibility

The Operator provided Cursor's compact terminal report with EXECUTIVE=2757/576ed822cf8e047ef570b2f9438efc01903e4199c395e1ec4fd12d5c272f4ac4, HANDSHAKE=844/f53691b0f61f02aa47ff07388cb5f18409d26e008a5cdfcde1c3f9a0dc2e3fb9, EPISTEMIC_WALLS=699/5d824e7d822fd668b3355a2aef6c9f7e5e6dccb60f76df0101a1fd8b5e69a494, RESULT=1817/ca2c5d6456e731363fb5749388823e871021410fb8219f62835831bcbd8e7850, P10_SEAL=1098/3f60d81b016fcfd95e58d241306e109d470990ed17a818034756a89637d42748 and SHA256SUMS=1610/ec1eab1dd96e2e3805e8647e340578c2323ca0ff08b3412e8726b27ca3c70c52. These are OPERATOR_RELAYED_CURSOR_LOCAL_SHA_CLAIMS, NOT independently fetched original bytes; cannot claim on-disk 6/6 HASH_MATCH. No PR267 return comment or committed return is established at this adjudication. Desktop Commander has no connected machine: Windows TRANSFER files not independently accessible.

The result is unambiguously a *failed full experiment*. P0–P10 CLOSED means process completed with truthful FAIL_CLOSED, not a successful hardware trial. The reported ~97.5s after-disconnect START is a useful bounded positive pending original source/event-log review. Missing autonomous STOP and SEAL are blocking faults.

Official Android architecture references:
https://developer.android.com/reference/android/app/Service
https://developer.android.com/reference/android/os/Handler
https://developer.android.com/reference/android/os/SystemClock
START_STICKY can restart a service with null Intent; onDestroy is not guaranteed on abrupt process kill; Handler delayed Runnable may never run if process/Looper terminates. A reliable local sensor STOP/SEAL must not depend solely upon onDestroy or the existence of one in-process handler.

## II. Immediate safety gate before any repeat

R0. FIRST READ current OPPO actual native application state via the already authorized device-specific WLAN-ADB session, with private serial/network data redacted. Inspect active app recording/service notification, current session state, segment growth, storage pressure, queue and old science. No new recording until previous state CLOSED or RECOVERY_PENDING is safely contained.

If still recording, use only a previously verified, nondestructive valid native STOP method and verify actual sensor unregister + writer close + sealed files. Any ADB-assisted emergency stop is a SAFETY_RECOVERY, NOT successful No-ADB operation. If no proven safe STOP exists, mark SAFE_STOP_BLOCKED, preserve bytes and request separate owner decision instead of force-stop, pm clear, uninstall, kill or silently losing data. Never repeatedly start new unbounded sessions.

Preserve existing OPPO historical recordings, original APK/signature, rollback and locally dirty Android S1-S5 work. Do not merge PR263/266/267 or publish raw IMU/GPS/ADB IP/port/mDNS/IMEI/serial.

## III. Exact scoped Native Android repair — NO new framework

R1. Audit actual Kotlin/Java on-disk sources: LaunchActivity valid START/STOP Intent handling, ScientificImuForegroundService, FGS start modes, onStartCommand(null), onDestroy, onTaskRemoved, sensor subscriptions, gzip writer/manifest, queues, pending callbacks, stored time base and current retry/recovery. Annotate real source commit/file/line, source version and rollback. Validate reported mechanism, distinguish source analysis from empirical proof.

R2. One authoritative per-session, append-only durable state machine:
  IDLE → ARMED → RECORDING → STOPPING → SEALED.
  Any interrupted/incomplete seal → RECOVERY_PENDING; successful repair → RECOVERED_SEALED, NOT historically SEALED_ON_TIME.
  Cancel before a sample → CANCELLED_BEFORE_START.
  No direct RECORDING → SEALED without actually unregistering sensor, flushing/completing gzip and atomic manifest verification.

Persist session ID, monotonic START elapsedRealtimeNanos, STOP deadline, current durable state and source build **before real capture**. Use serialized/mutex single-owner transitions; STOP is idempotent; unknown/malformed/null Intent does NOT START. Commit STOPPING before unregister. Then unregister sensors, flush/close gzip writers, verify gzip integrity (CRC/end), compute actual SHA256/bytes for separate segments, fsync/atomic manifest or equivalent verified strategy, update durable receipt SEALED, then stopForeground/stopSelf. Failed finalization preserves RECOVERY_PENDING and all existing bytes; never fake SEALED. Concurrent stop or duplicate timer cannot double-close, overwrite or lose records.

R3. App-native deadline:
- Visible Activity/legitimate already-consented FGS ARMED before ADB disconnect; no sensor read before disconnect.
- Use an app-owned timer while FGS alive to request the same centralized STOP/SEAL path at or after persisted elapsedRealtime deadline (target ~7 min after real sensor START).
- Time measurement uses SystemClock.elapsedRealtimeNanos (or documented matching monotonic basis), not naive uptimeMillis timer; Handler.postDelayed uses uptimeMillis and can be delayed by deep sleep, so callback MUST re-evaluate elapsedRealtime deadline. If precise deadline under system sleep is essential, justify any additional native mechanism under Android permissions/background rules; do not auto-request exact alarm or Accessibility permissions.
- On sticky restart/null Intent, load persisted state; NEVER start a new session from null. If prior deadline elapsed, safely recover or mark RECOVERY_PENDING; distinguish resumed/recovered from uninterrupted proof. onDestroy may do best-effort cleanup but cannot be single guaranteed sealing authority; process kill may skip it entirely.
- START_STICKY vs START_NOT_STICKY is an explicit engineering choice justified by observed lifecycle/controlled recovery, not a magical timer guarantee.
- No ADB/host scheduling, websocket/server, GitHub comment or remote agent trigger for native STOP or SEAL after disconnect.

R4. Fail-closed unknown STOP Intent path before any device test; specifically investigate prior P8 behavior where misspelled STOP entered START. Tests must show it produces NO new segment or sensor registration.

## IV. No manual interaction and progressive tests before device retest

R5. First run independent local Kotlin/JVM source tests and authorized non-destructive Android instrumentation:
N01 delayed ARM/START only when intended;
N02 app timer triggers STOPPING→sensor unregister→gzip close→verified SHA/manifest→SEALED→self-stop;
N03 invalid/unknown/null START/STOP intent cannot begin capture;
N04 repeat STOP, timer/STOP race, duplicate session ID have one canonical end;
N05 process death or FGS destruction before deadline yields accurate RECOVERY_PENDING;
N06 failure injection at gzip close, manifest write, durable DB commit, process restart and low disk cannot fake seal;
N07 monotonically tagged event order and timestamp uncertainty explicit;
N08 old Oppo recordings unchanged SHA before/after;
N09 disabled permission, unavailable sensors, no source version or no safe rollback → HOLD;
N10 raw compressed segments verified decode/CRC and exact private source bytes.

Only after all required safe stop/seal negatives PASS, run a fresh OPPO experiment. No new Android permissions, no forced install if data migration/signature unsafe, no force stop/clear/uninstall. Distinguish 28/28 earlier local JVM from new exact-source tests; GitHub Evidence CI does not independently compile the native Android APK.

R6. Unattended experiment, OPERATOR ACTION ZERO:
  PRETEST existing permission and visible FGS, new unique session ARM through authorized existing ADB. Acceleration/gyro registration MUST still be inactive.
  Disconnect WLAN-ADB before native sensor START; independently capture host-side no-ADB interval and bound host vs Android clock uncertainty.
  Native app START after delay, CAPTURE bounded ~7 minutes, native STOP and LOCAL_SEAL with no ADB/user/host controls.
  Only after conservative completion buffer, Cursor autonomously reconnects for read-only pull of final private original bytes.
  Two independent hash paths and actual gzip end checks verify device-side hashes, segment lengths, manifest, sample counts and monotonic events.
  If reconnect early, unknown action, native STOP missing, failed seal, operating-system killed/restarted run or operator input required: clearly FAIL/HOLD, no PASS_NO_ACTIVE_ADB_SESSION. If restart recovery occurred, declare RECOVERED not uninterrupted.

R7. Public-safe source-exact evidence: only pseudonymous Oppo id, app version/source hash, event types/timedeltas, counts, SHA256 of private data but not raw data, sanitized host log, test vs real proof type and exact GitHub raw-byte rehash. Complete original file SHA256SUMS after writing/upload, never repeat prior 13/26 GitHub blob mismatch. Historical 13 mismatch remains OPEN in previous PR263; create append-only erratum, never rewrite old originals. App source-only privacy-reviewed PR if authorized; no new GitHub account/credential or public POST.

## V. Required return, explicit statuses

RETURN_OBJECT = NEXUS_OMEGA_CURSOR_OPPO_NATIVE_AUTOSTOP_LOCALSEAL_REPAIR_AND_UNATTENDED_RETEST_RETURN_20261101_R0
G0_PREVIOUS_SESSION_SAFETY = VERIFIED_SAFE_OR_HOLD
G1_SOURCE_LOCALE_FGS_AUDIT = ACTUAL_SOURCE_OR_LOCAL_ONLY
G2_INAPP_SCHEDULED_STOP = REAL_IMPLEMENTATION_AND_TEST_OR_HOLD
G3_LOCALSEAL_IDEMPOTENT_DURABLE = REAL_SEGMENTS_AND_TESTS_OR_HOLD
G4_UNKNOWN_STOP_FAILCLOSED = PROVEN_OR_FAIL
G5_REAL_OPPO_DEVICE_RUN = SOURCE_EXACT_OR_NOT_EXECUTED
G6_AFTER_DISCONNECT_START = PASS_OR_FAIL_OR_NOT_ESTABLISHED
G7_NO_ADB_NATIVE_AUTO_STOP = PASS_OR_FAIL_OR_NOT_ESTABLISHED
G8_NO_ADB_NATIVE_LOCAL_SEAL = PASS_OR_FAIL_OR_NOT_ESTABLISHED
G9_INDEPENDENT_PRIVATE_BINARY_REHASH = MATCH_OR_NOT_ESTABLISHED
G10_NEW_GITHUB_MANIFEST = REAL_RAW_BLOB_REHASH_OR_NOT_EXECUTED
PREVIOUS_P0_P10_FAILED_TEST = PRESERVED_AS_FAILED
PR263_266_267 = UNMERGED_UNLESS_SEPARATELY_AUTHORIZED
OPERATOR_MANUAL_INPUT = ZERO
EXTERNAL_ACK = NOT_ESTABLISHED
GLOBAL_CUTOVER_ACTIVE = NO
PIXEL9A = NOT_ADMITTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_INDEPENDENT_OPPO_AUTOSTOP_LOCALSEAL_AND_NO_ADB_TIMEBASE_ADJUDICATION

Complete safe software work NOW; HOLD only a concrete missing source, device consent, permission or nondestructive recovery. No repeating the broken seven-minute experiment before independent-safe STOP/SEAL negative tests.
