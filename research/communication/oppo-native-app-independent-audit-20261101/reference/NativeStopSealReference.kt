/*
 * NEXUS OMEGA -- OPPO native stop/seal PURE JVM REFERENCE MODEL (C1).
 * NOT PRODUCT CODE. NO Android bridge, no real disk fsync, no device permissions.
 * Cursor must bind this to actual source with a durable transactional store,
 * serialized SensorManager/writer executor, native AlarmManager receiver,
 * AtomicFile/Room and original-file CRC/hash witnesses before production use.
 */
package nexus.omega.research

/** This model deliberately treats a process restart as loss of uninterrupted continuity. */
enum class CapturePhase {
    ARMED, RECORDING, STOPPING, SEALED, RECOVERY_PENDING, CANCELLED_BEFORE_START
}
enum class StopOrigin { APP_DEADLINE, APP_UI, ADB_ASSISTED_RECOVERY }
enum class GateOutcome {
    ARMED, RECORDING, SEALED, RECOVERY_PENDING, CANCELLED_BEFORE_START,
    TOO_EARLY, STALE_EVENT, IGNORED_INVALID_ACTION, NO_ACTIVE_SESSION
}

data class SealReceipt(val byteLength: Long, val sha256: String, val streamCrcValid: Boolean)

data class CaptureState(
    val sessionId: String,
    val bootEpochId: String,
    val phase: CapturePhase,
    val startNotBeforeElapsedMs: Long,
    val durationMs: Long,
    val startedElapsedMs: Long? = null,
    val stopDeadlineElapsedMs: Long? = null,
    val stopOrigin: StopOrigin? = null,
    val sealed: SealReceipt? = null
)

/** Contract: commit() must be atomic and durable BEFORE the next side effect. */
interface DurableCaptureStore {
    fun read(): CaptureState?
    fun commit(value: CaptureState)
}

/** Contract: ONLY serialized writer owner may implement finishAndVerify. */
fun interface GzipSealer {
    fun finishAndVerify(sessionId: String): SealReceipt
}

/**
 * Pure reference coordinator. Call only on a dedicated serialized executor, never
 * the Android main thread. Real store must preserve prior sessions separately.
 */
class NativeStopSealReference(private val store: DurableCaptureStore) {
    private val shaRegex = Regex("^[0-9a-f]{64}$")

    @Synchronized
    fun arm(sessionId: String, bootId: String, nowElapsedMs: Long,
            delayMs: Long, durationMs: Long): GateOutcome {
        require(sessionId.isNotBlank() && bootId.isNotBlank())
        require(nowElapsedMs >= 0 && delayMs >= 0 && durationMs in 1..3_600_000L)
        val old = store.read()
        if (old != null && old.phase !in setOf(CapturePhase.SEALED, CapturePhase.CANCELLED_BEFORE_START))
            return GateOutcome.STALE_EVENT
        if (old != null && old.sessionId == sessionId) return GateOutcome.STALE_EVENT
        val allowedAt = Math.addExact(nowElapsedMs, delayMs)
        store.commit(CaptureState(sessionId, bootId, CapturePhase.ARMED,
            allowedAt, durationMs))
        return GateOutcome.ARMED
    }

    /** Called ONLY by an internal app-owned scheduler; not a public Intent handler. */
    @Synchronized
    fun internalStart(sessionId: String, bootId: String, nowElapsedMs: Long): GateOutcome {
        val old = store.read() ?: return GateOutcome.NO_ACTIVE_SESSION
        if (old.sessionId != sessionId || old.bootEpochId != bootId || old.phase != CapturePhase.ARMED)
            return GateOutcome.STALE_EVENT
        if (nowElapsedMs < old.startNotBeforeElapsedMs) return GateOutcome.TOO_EARLY
        val deadline = Math.addExact(nowElapsedMs, old.durationMs)
        store.commit(old.copy(phase = CapturePhase.RECORDING,
            startedElapsedMs = nowElapsedMs, stopDeadlineElapsedMs = deadline))
        return GateOutcome.RECORDING
    }

    /** The only normal unattended stop path. A delivered alarm MUST verify deadline. */
    @Synchronized
    fun onAppDeadline(sessionId: String, bootId: String, nowElapsedMs: Long,
                      sealer: GzipSealer): GateOutcome {
        val old = store.read() ?: return GateOutcome.NO_ACTIVE_SESSION
        if (old.sessionId != sessionId || old.bootEpochId != bootId || old.phase != CapturePhase.RECORDING)
            return GateOutcome.STALE_EVENT
        val deadline = old.stopDeadlineElapsedMs ?: return GateOutcome.STALE_EVENT
        if (nowElapsedMs < deadline) return GateOutcome.TOO_EARLY
        return stopAndSeal(old, StopOrigin.APP_DEADLINE, sealer)
    }

    /** Explicit authenticated UI/recovery only. This must NOT count as unattended. */
    @Synchronized
    fun authorizedStop(sessionId: String, bootId: String, origin: StopOrigin,
                       sealer: GzipSealer): GateOutcome {
        require(origin != StopOrigin.APP_DEADLINE) { "deadline only via onAppDeadline" }
        val old = store.read() ?: return GateOutcome.NO_ACTIVE_SESSION
        if (old.sessionId != sessionId || old.bootEpochId != bootId || old.phase != CapturePhase.RECORDING)
            return GateOutcome.STALE_EVENT
        return stopAndSeal(old, origin, sealer)
    }

    /** Invalid/null Android Intents can NEVER be mapped to a default START. */
    @Synchronized
    fun invalidOrNullIntentIgnored(@Suppress("UNUSED_PARAMETER") action: String?): GateOutcome =
        GateOutcome.IGNORED_INVALID_ACTION

    /** Native service restart cannot claim the previous in-flight session sealed. */
    @Synchronized
    fun onServiceRestart(bootId: String): GateOutcome {
        require(bootId.isNotBlank())
        val old = store.read() ?: return GateOutcome.NO_ACTIVE_SESSION
        if (old.phase == CapturePhase.SEALED || old.phase == CapturePhase.CANCELLED_BEFORE_START)
            return GateOutcome.STALE_EVENT
        val next = if (old.phase == CapturePhase.ARMED) CapturePhase.CANCELLED_BEFORE_START
                   else CapturePhase.RECOVERY_PENDING
        // Changing bootId is not a way to resume a measurement in a different clock epoch.
        store.commit(old.copy(phase = next))
        return if (next == CapturePhase.RECOVERY_PENDING) GateOutcome.RECOVERY_PENDING
               else GateOutcome.CANCELLED_BEFORE_START
    }

    @Synchronized
    fun getState(): CaptureState? = store.read()

    private fun stopAndSeal(old: CaptureState, origin: StopOrigin,
                            sealer: GzipSealer): GateOutcome {
        // IMPORTANT: STOPPING commit must be durable before writer side effects.
        store.commit(old.copy(phase = CapturePhase.STOPPING, stopOrigin = origin))
        return try {
            // Production: unregister sensor, drain writer, finish gzip/CRC, fsync,
            // hash exact sealed binary bytes, atomically publish a private manifest.
            val receipt = sealer.finishAndVerify(old.sessionId)
            require(receipt.byteLength > 0 && receipt.streamCrcValid &&
                    shaRegex.matches(receipt.sha256)) { "Invalid seal receipt" }
            store.commit(old.copy(phase = CapturePhase.SEALED,
                stopOrigin = origin, sealed = receipt))
            GateOutcome.SEALED
        } catch (failure: Exception) {
            // Never mark a partially written gzip as SEALED.
            store.commit(old.copy(phase = CapturePhase.RECOVERY_PENDING,
                stopOrigin = origin, sealed = null))
            GateOutcome.RECOVERY_PENDING
        }
    }
}
