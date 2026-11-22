package com.nexusomega.maps.sensor

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * R41 P2 offline unit tests for [ScientificImuStopDeadlineGate].
 *
 * Defect class (pre-repair expected): samples at/after absolute elapsedRealtime
 * deadline must be rejected. Ungated CaptureEngine historically accepted a
 * ~3.6s tail (~363 events/channel @ ~100 Hz).
 *
 * Object: NEXUS_OMEGA_AXIOM_CURSOR_R41_OFFLINE_IMPLEMENTATION_SOURCE_STOP_METROLOGY_GATES_ORDER_20261122_R0
 * Claim ceiling: C1_DESCRIPTIVE_ONLY
 * PHYSICAL / DEVICE_CAPTURE: NOT authorized by this type.
 */
class ScientificImuStopDeadlineGateTest {

    private val G = ScientificImuStopDeadlineGate

    @Test
    fun accept_when_no_deadline_bound() {
        assertTrue(G.shouldAcceptSample(0L, 1_000_000_000L))
        assertTrue(G.shouldAcceptSample(-1L, 99L))
    }

    @Test
    fun accept_strictly_before_deadline() {
        val deadline = 60_000_000_000L // 60s in ns
        assertTrue(G.shouldAcceptSample(deadline, deadline - 1L))
        assertTrue(G.shouldAcceptSample(deadline, 0L))
    }

    @Test
    fun reject_at_exact_deadline() {
        val deadline = 60_000_000_000L
        assertFalse(G.shouldAcceptSample(deadline, deadline))
    }

    @Test
    fun reject_after_deadline() {
        val deadline = 60_000_000_000L
        assertFalse(G.shouldAcceptSample(deadline, deadline + 1L))
        assertFalse(G.shouldAcceptSample(deadline, deadline + 3_622_217_000L))
    }

    @Test
    fun r37_tail_class_363_post_deadline_samples_all_rejected() {
        // Synthetic 100 Hz stream: deadline at t=0; 363 samples spanning ~3.622s.
        val deadline = 1_000_000_000_000L
        val periodNs = 10_000_000L // 100 Hz
        var accepted = 0
        var rejected = 0
        for (i in 0 until 363) {
            val now = deadline + i * periodNs
            if (G.shouldAcceptSample(deadline, now)) accepted++ else rejected++
        }
        assertEquals(0, accepted)
        assertEquals(363, rejected)
    }

    @Test
    fun pre_deadline_stream_all_accepted() {
        val deadline = 60_000_000_000L
        val periodNs = 10_000_000L
        var accepted = 0
        // 5990 samples = 59.90s of 100 Hz (within <60s gate)
        for (i in 0 until 5990) {
            val now = i * periodNs
            if (G.shouldAcceptSample(deadline, now)) accepted++
        }
        assertEquals(5990, accepted)
    }

    @Test
    fun deadlineReached_aligns_with_session_machine() {
        val d = 5_000L
        assertFalse(G.deadlineReached(0L, 9_999L))
        assertFalse(G.deadlineReached(d, d - 1L))
        assertTrue(G.deadlineReached(d, d))
        assertTrue(G.deadlineReached(d, d + 1L))
        assertEquals(
            ScientificImuSessionMachine.deadlineReached(d, d),
            G.deadlineReached(d, d),
        )
    }

    @Test
    fun negative_mutation_force_accept_past_deadline_is_detectable() {
        // Adversarial mutant: invert the gate. Offline harness must fail-closed.
        fun mutantAccept(deadline: Long, now: Long): Boolean {
            if (deadline <= 0L) return true
            return now >= deadline // WRONG — accepts after deadline
        }
        val deadline = 60_000_000_000L
        assertTrue(mutantAccept(deadline, deadline + 1L))
        assertFalse(G.shouldAcceptSample(deadline, deadline + 1L))
        assertTrue(
            "negative fixture: mutant must diverge from repaired gate",
            mutantAccept(deadline, deadline) != G.shouldAcceptSample(deadline, deadline),
        )
    }
}
