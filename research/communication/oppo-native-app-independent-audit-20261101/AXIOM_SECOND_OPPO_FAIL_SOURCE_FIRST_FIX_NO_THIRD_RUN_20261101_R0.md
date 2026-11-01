# NEXUS OMEGA · AXIOM
## Second OPPO unattended No-ADB failure: independent admissibility and source-first remediation
### 2026-11-01 · Append-only PR270 · C1_DESCRIPTIVE_ONLY

OBJECT = NEXUS_OMEGA_AXIOM_SECOND_OPPO_FAIL_ADJUDICATION_SOURCE_FIRST_FIX_NO_THIRD_RUN_20261101_R0
PARENT_RETURN = NEXUS_OMEGA_CURSOR_OPPO_NATIVE_AUTOSTOP_LOCALSEAL_REPAIR_AND_UNATTENDED_RETEST_RETURN_20261101_R0
PREDECESSOR_ORDER = NEXUS_OMEGA_AXIOM_CURSOR_OPPO_NATIVE_AUTOSTOP_LOCALSEAL_FAILCLOSED_REPAIR_ORDER_20261101_R0
PREDECESSOR_COMMIT = e0c3b608bc524b488d4b33d6c3ff8ccaf7371816
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = FAIL_CLOSED_C1_NATIVE_AUTOSTOP_LOCALSEAL_UNATTENDED_NOT_MET
SOURCE_AUTHORITY = OPERATOR_RELAYED_CURSOR_LOCAL_RETURN
ORIGINAL_LOCAL_BYTES_READ_BY_AXIOM = NO
REAL_NATIVE_KOTLIN_SOURCE_INSPECTED_BY_AXIOM = NO
THIRD_SEVEN_MINUTE_TEST = HOLD_PENDING_SOURCE_AND_QUALIFIED_STOP_SEAL_FIX
PIXEL9A = NOT_ADMITTED
EXTERNAL_AGENT_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
CUTOVER_ACTIVE = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## I. Observation and evidence ceiling

The Operator relays a second honest FAIL_CLOSED:
G5 start after ADB disconnect = PASS_PARTIAL; two gzip segments after disconnect.
G6 native AUTO_STOP = FAIL.
G7 native unattended LOCAL_SEAL = FAIL.
G8 complete unassisted ADB-off recording = NOT_MET.
The seal occurred ONLY after ADB-assisted LaunchActivity STOP around 16:06, so it is an assisted recovery finalization and cannot be promoted to unassisted autonomy.
ZIP reported 985511 bytes SHA256 c5261f3ea32cb1c388de10a554d5bdb368142f4f3c4f44c138d614ca66843c83; actual ZIP bytes inaccessible to AXIOM, therefore not independently rehashed.
Cursor's locally held EXECUTIVE 2275/3e0ae38fa83b20b14bed8248ac47111dd87ce18d4aef911985155b591ef39d28, HANDSHAKE 706/e123026907b24b73b1a04da96d5b5aaf80e664ce52a389908eac46ed650edafc, EPISTEMIC_WALLS 525/3150ed7adc9c7a69b4ab143108f7024540ba5f44108dd54a5d92fe865976ce01, RESULT 882/8ad21ba19804f977a2820819689b3674916cb2cb7e9d9d01b01c69a642b26d3f, SHA256SUMS 849/388f00ec40fdeeae579bd0f0f0b28953104031a9aae22c41b5145487d48f1121 are OPERATOR_RELAYED_SHA_ASSERTIONS_ONLY. They are not source-inventoried here.

GitHub REST at adjudication: PR270 OPEN, unmerged, head 176a371a07b3327e97333e24b7678fd510e24caf, zero return comments. No independently inspectable Android source/return was found at this official review slot; a local Windows TRANSFER path alone is not a GitHub source witness. The prior PR263 original 13-of-26 GitHub blob SHA mismatches remain open; do not rewrite historical sources.

Two consecutive full experiments with similar failure are NOT two successful independent replications. They isolate a critical closure defect. Stop automatically reissuing full seven-minute trials.

## II. What technical Android sources actually establish

Android Service official docs: START_STICKY may recreate a service with null onStartCommand Intent; it is not a persisted timer and MUST NOT implicitly restart recording.
https://developer.android.com/reference/android/app/Service

Android Handler docs: postDelayed uses uptimeMillis; deep sleep postpones callback, and callbacks can be lost if Looper exits. Queued callback is NOT proof that it ran.
https://developer.android.com/reference/android/os/Handler

SystemClock docs: elapsedRealtimeNanos includes deep sleep and is a monotonic interval timebase; the event callback still needs actual execution and verification.
https://developer.android.com/reference/android/os/SystemClock

SensorManager: unregisterListener explicitly unregisters sensor event delivery; successful onDestroy or guessed STOP is not equal to verified unregister/flush/close.
https://developer.android.com/reference/android/hardware/SensorManager

Those facts support a hypothesis of lifecycle/scheduler/single-writer logic failure. Actual Kotlin source and device event chronology must independently establish the specific causal path; do not assert a line-level root cause from a chat summary.

## III. Cursor directive: preserve device, show ACTUAL Kotlin, execute patch BEFORE another long measurement

S0 SAFETY FIRST: read-only inspect authorized OPPO current foreground-service recording state, session IDs, storage/file growth, recent timer event logs, old science. If still recording, use ONLY already verified native nondestructive STOP and check actual finalization. ADB-assisted safety stop is NOT native auto-stop proof. No force-stop/pm clear/uninstall/factory reset. If safe stop cannot be established: HOLD_DEVICE_RECORDING, no further test.
S1 SOURCE INVENTORY: preserve dirty local S1–S5 and science. List exact Kotlin/Gradle/Manifest modules with bytes/SHA, installed build SHA, source branch and current timer/seal method. No auto-reset or source overwrite. Provide source-only reviewed immutable GitHub branch or an actually authorized private code channel; lacking it is a material independent review gap, never covered by Evidence PR CI.
S2 TRACE ROOT CAUSE: exact onStartCommand/START_STICKY/null Intent, LaunchActivity action mapping, arm delay, sensor registration, native auto-stop scheduling, callback invocation/cancellation, onDestroy cancelPending, single-writer close and localSeal source. Correlate native monotonic logs T_ARM/T_START/T_DEADLINE/T_STOP_EXPECTED with missing STOP_CALLBACK_ENTER, STOPPING, SENSOR_UNREGISTERED, WRITER_CLOSED, SEGMENT_SEALED and recovery. Scheduled is NOT executed. Do not attribute to Android Doze without actual device evidence.
S3 PATCH ONE STOP/SEAL ENTRY: implement durable per-session IDLE→ARMED→RECORDING→STOPPING→SEALED, RECOVERY_PENDING for incomplete finalization. STOP must be serialized/idempotent, persist STOPPING, block further samples, unregister SensorManager listener, drain/finish compressed stream, verify CRC and size/hash, atomically commit sidecar and manifest, only then claim SEALED and stop service. STOP retries, duplicate timers and unknown Intent cannot restart acquisition. Process death before close is RECOVERY_PENDING and must never be SEALED_ON_TIME falsely. onDestroy is best effort, NEVER sole seal authority.
S4 TIMING: persist start and stop deadline using elapsedRealtimeNanos and source commit. While already legally running visible FGS is active, arrange service-owned deadline callback and secondary safe deadline recheck in the active sensor-event path where suitable; log both schedule and actual callback-enter. Handler postDelayed is NOT a guarantee under deep sleep or process death. On sticky restart, read durable state, inspect files and deadline, recover or HOLD, NEVER start new capture from null Intent. No uncontrolled exact alarm permission, Accessibility, LLM dynamic code, host ADB STOP, network watchdog or new external rights.
S5 NEGATIVE TESTS BEFORE OPPO LONG RUN: compile exact source; unit/instrumented tests for timer deadline → actual shared STOP → CRC-valid file and atomic manifest; unknown STOP and null Intent cannot START; double callback/STOP idempotency; process death before and after each STOP/SEAL boundary; low disk and denied sensor; monotonic timebase deep-sleep disparity; old science bytes unchanged; source SHA and APK identity. Test both NORMAL and injected broken callback that never fires: the latter must show FAILED, not PASS.
S6 A SHORT BOUNDED OPPO CORRECTNESS TEST MAY OCCUR only after safe device state, code patch, backup, old data preserved and stop/closure negative tests pass. Limit to <=45 seconds, ADB connected for diagnostics, no ADB STOP except documented emergency safety rescue. It proves NATIVE_AUTO_STOP_AND_SEAL in source and device, NOT the ADB-disconnected claim. If this short proof fails, no long retest. If no safe build/install route, return HOLD, never delete/replace old app data.
S7 SOURCE FIRST: return exact changed source, diff, real compiled tests and where lawful/authorized privacy-reviewed source-only GitHub PR and real code CI. Public evidence redacts Wi-Fi debug endpoint, mDNS, raw sensor data. Local raw ZIP remains private; independent original bytes and GitHub raw hashes must match after push. Historical 13 SHA mismatches retained append-only.
S8 ONLY AFTER PASS OF S0–S7: the prior already-scoped unattended 7-min ADB-disconnected experiment may be repeated once under operator's zero-manual-action constraint. If source/checklist still incomplete, do not schedule it or present a third failure as new evidence.

## IV. Test conditions and terminal acceptance

Required before another full disconnected run:
- CURRENT_OPPO_RECORDING = SAFE_STOPPED_AND_SEALED_OR_NAMED_HOLD
- NATIVE_KOTLIN_SOURCE = ACTUAL_SOURCE_REVIEWABLE_AND_HASHED
- NATIVE_AUTO_STOP_SHORT_TEST = REAL_HARDWARE_PASS_AND_REAL_CALLBACK_INVOCATION
- NATIVE_LOCAL_SEAL_SHORT_TEST = REAL_PRIVATE_GZIP_CRC_MANIFEST_SHA_PASS
- UNKNOWN_STOP_AND_NULL_STICKY = FAIL_CLOSED_TEST_PASS
- INTERRUPTED_FINALIZATION = RECOVERY_PENDING_TEST_PASS
- OLD_OPPO_DATA = REHASH_AND_PRESERVED
- DEVICE_APK_BUILD = ACTUAL_NATIVE_BUILD_CI_OR_LOCAL_CI_EXPLICITLY_DISCLOSED
- THIRD_NO_ADB_FULL_TEST = NOT_EXECUTED_UNTIL_ALL_ABOVE_PASS

Return object:
NEXUS_OMEGA_CURSOR_OPPO_NATIVE_STOP_SEAL_SOURCE_REPAIR_PROOF_BEFORE_RETEST_20261101_R0

Return source and actual logs, not architecture-only research. Owner action during autonomous test remains NONE. No GitHub merge, public write, external ACK, global cutover or Pixel9a action.

TERMINAL = SOURCE_FIRST_IMPLEMENTATION_AND_FALSIFICATION_REQUIRED_NO_THIRD_PREMATURE_UNATTENDED_RUN
