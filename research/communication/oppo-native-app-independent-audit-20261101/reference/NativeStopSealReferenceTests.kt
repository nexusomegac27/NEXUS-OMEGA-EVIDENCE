/* JVM-only falsification runner for the OPPO reference FSM. NOT real Android E2E. */
package nexus.omega.research

class InMemoryStore : DurableCaptureStore {
    var snapshot: CaptureState? = null
    val commits = mutableListOf<CapturePhase>()
    override fun read(): CaptureState? = snapshot
    override fun commit(value: CaptureState) { snapshot = value; commits.add(value.phase) }
}

private const val HASH = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
private fun validSeal() = SealReceipt(512, HASH, true)
private class Tests {
    var assertions = 0
    fun eq(actual: Any?, expected: Any?) {
        assertions++
        check(actual == expected) { "EXPECTED " + expected + ", GOT " + actual }
    }
    fun yes(actual: Boolean) { assertions++; check(actual) }
}

fun main() {
    val t = Tests()
    run {
        val db = InMemoryStore(); val c = NativeStopSealReference(db)
        t.eq(c.arm("A", "BOOT1", 1000, 1500, 7000), GateOutcome.ARMED)
        t.eq(c.internalStart("A", "BOOT1", 2499), GateOutcome.TOO_EARLY)
        t.eq(c.internalStart("A", "BOOT1", 2500), GateOutcome.RECORDING)
        t.eq(c.getState()!!.stopDeadlineElapsedMs, 9500L)
        t.eq(c.onAppDeadline("A", "BOOT1", 9499, GzipSealer { validSeal() }), GateOutcome.TOO_EARLY)
        var seals = 0
        val sealer = GzipSealer { seals++; validSeal() }
        t.eq(c.onAppDeadline("A", "BOOT1", 9500, sealer), GateOutcome.SEALED)
        t.eq(c.getState()!!.stopOrigin, StopOrigin.APP_DEADLINE)
        t.eq(c.getState()!!.sealed!!.sha256, HASH)
        t.eq(seals, 1)
        t.eq(c.onAppDeadline("A", "BOOT1", 10000, sealer), GateOutcome.STALE_EVENT)
        t.eq(c.authorizedStop("A", "BOOT1", StopOrigin.ADB_ASSISTED_RECOVERY, sealer), GateOutcome.STALE_EVENT)
        t.eq(seals, 1)
        t.yes(db.commits.takeLast(2) == listOf(CapturePhase.STOPPING, CapturePhase.SEALED))
        t.eq(c.invalidOrNullIntentIgnored(null), GateOutcome.IGNORED_INVALID_ACTION)
        t.eq(c.invalidOrNullIntentIgnored("com.nexusomega.maps.ACTOIN_STOP"), GateOutcome.IGNORED_INVALID_ACTION)
        t.eq(c.arm("A", "BOOT1", 10000, 500, 5000), GateOutcome.STALE_EVENT)
        t.eq(c.arm("B", "BOOT1", 10000, 500, 5000), GateOutcome.ARMED)
        t.eq(c.internalStart("B", "BOOT1", 10500), GateOutcome.RECORDING)
        t.eq(c.onAppDeadline("A", "BOOT1", 20000, sealer), GateOutcome.STALE_EVENT)
        t.eq(c.onAppDeadline("B", "BOOT_DIFFERENT", 20000, sealer), GateOutcome.STALE_EVENT)
        t.eq(c.getState()!!.phase, CapturePhase.RECORDING)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        t.eq(c.arm("X", "BOOT", 0, 0, 10), GateOutcome.ARMED)
        t.eq(c.internalStart("X", "BOOT", 0), GateOutcome.RECORDING)
        t.eq(c.onAppDeadline("X", "BOOT", 10, GzipSealer { throw java.io.IOException("disk full") }), GateOutcome.RECOVERY_PENDING)
        t.eq(c.getState()!!.phase, CapturePhase.RECOVERY_PENDING)
        t.eq(c.getState()!!.sealed, null)
        t.yes(db.commits.takeLast(2) == listOf(CapturePhase.STOPPING, CapturePhase.RECOVERY_PENDING))
        t.eq(c.onAppDeadline("X", "BOOT", 10, GzipSealer { validSeal() }), GateOutcome.STALE_EVENT)
        t.eq(c.onServiceRestart("BOOT"), GateOutcome.RECOVERY_PENDING)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        c.arm("Y", "BOOT1", 0, 0, 40)
        c.internalStart("Y", "BOOT1", 0)
        t.eq(c.onAppDeadline("Y", "BOOT1", 40, GzipSealer { SealReceipt(22, "notSha", true) }), GateOutcome.RECOVERY_PENDING)
        t.eq(c.getState()!!.phase, CapturePhase.RECOVERY_PENDING)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        c.arm("U", "BOOT1", 0, 0, 40)
        c.internalStart("U", "BOOT1", 0)
        t.eq(c.onAppDeadline("U", "BOOT1", 40, GzipSealer { SealReceipt(22, HASH, false) }), GateOutcome.RECOVERY_PENDING)
        t.eq(c.getState()!!.sealed, null)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        c.arm("BOOT", "A", 0, 10, 50)
        t.eq(c.onServiceRestart("B"), GateOutcome.CANCELLED_BEFORE_START)
        t.eq(c.getState()!!.phase, CapturePhase.CANCELLED_BEFORE_START)
        t.eq(c.internalStart("BOOT", "A", 10), GateOutcome.STALE_EVENT)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        c.arm("Z", "BOOT1", 0, 0, 50)
        c.internalStart("Z", "BOOT1", 0)
        t.eq(c.onServiceRestart("BOOT2"), GateOutcome.RECOVERY_PENDING)
        t.eq(c.getState()!!.phase, CapturePhase.RECOVERY_PENDING)
        t.eq(c.getState()!!.sealed, null)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        c.arm("R", "BOOT", 0, 0, 100)
        c.internalStart("R", "BOOT", 0)
        t.eq(c.authorizedStop("R", "BOOT", StopOrigin.ADB_ASSISTED_RECOVERY,
            GzipSealer { validSeal() }), GateOutcome.SEALED)
        t.eq(c.getState()!!.stopOrigin, StopOrigin.ADB_ASSISTED_RECOVERY)
        t.eq(c.onAppDeadline("R", "BOOT", 100, GzipSealer { throw Error("MUST NOT RUN") }), GateOutcome.STALE_EVENT)
    }
    run {
        val db = InMemoryStore();val c = NativeStopSealReference(db)
        t.eq(c.onAppDeadline("N", "X", 20, GzipSealer { validSeal() }), GateOutcome.NO_ACTIVE_SESSION)
        t.eq(c.invalidOrNullIntentIgnored("ACTION_STOPP"), GateOutcome.IGNORED_INVALID_ACTION)
        t.eq(c.invalidOrNullIntentIgnored(null), GateOutcome.IGNORED_INVALID_ACTION)
    }
    println("PASS: " + t.assertions + " independent assertions")
}
