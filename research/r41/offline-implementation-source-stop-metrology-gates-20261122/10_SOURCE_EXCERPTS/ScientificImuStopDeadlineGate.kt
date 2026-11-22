package com.nexusomega.maps.sensor

/**
 * Pure JVM stop-deadline gate for per-sample acceptance (R41 P2).
 *
 * Aligns with [ScientificImuSessionMachine.deadlineReached]:
 * when a positive deadline is set, samples at or past the deadline must be rejected.
 *
 * Object: NEXUS_OMEGA_AXIOM_CURSOR_R41_OFFLINE_IMPLEMENTATION_SOURCE_STOP_METROLOGY_GATES_ORDER_20261122_R0
 * Claim ceiling: C1_DESCRIPTIVE_ONLY
 * PHYSICAL / DEVICE_CAPTURE: NOT authorized by this type.
 */
object ScientificImuStopDeadlineGate {
    /**
     * @param stopDeadlineElapsedNs elapsedRealtimeNanos absolute deadline; <=0 means no gate (accept)
     * @param nowElapsedNs current SystemClock.elapsedRealtimeNanos()
     * @return true iff the sample may be written into the capture stream
     */
    fun shouldAcceptSample(stopDeadlineElapsedNs: Long, nowElapsedNs: Long): Boolean {
        if (stopDeadlineElapsedNs <= 0L) return true
        return nowElapsedNs < stopDeadlineElapsedNs
    }

    /** Inverse of [shouldAcceptSample] when a positive deadline is bound. */
    fun deadlineReached(stopDeadlineElapsedNs: Long, nowElapsedNs: Long): Boolean {
        return ScientificImuSessionMachine.deadlineReached(stopDeadlineElapsedNs, nowElapsedNs)
    }
}
