# NEXUS OMEGA / Bodytwin 4D · R16/R1 Node-vm Source Exact Replay Repair

OBJECT = NEXUS_OMEGA_AXIOM_R16_Q0_R1_REFERENCE_NODE_VM_HARNESS_PORTABILITY_20261108_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RECONSTRUCTED_REFERENCE_NODE_REPLAY_20_OF_20
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PRODUCTION_VIEWER_REPLACEMENT = NO
CURSOR_VISUAL_DESIGN = EXCLUDED

- `q0-reference-r1/viewer.js` is the **original uploaded reconstructed** R1 implementation, 9116 bytes SHA256 `e03e6664c312f2f50081e6dc0fb8d03210e847ef5bf67d895688b20a10d8ebea`, unchanged. This is NOT the source of the live `/bodytwin/` production viewer.
- `tests/audit-q0-reference-r1.as-received.mjs` is the **original uploaded 7756-byte** R1 Node test, SHA256 `1bb562bc87506ebed82708930d11ee36b97843e55f33cb47aa0bafe738cddbf6`, which AXIOM independently reproduced at 17/20 under Node v22.16.0.
- `tests/audit-q0-reference-r1.mjs` is an **append-only test-harness correction**, not a change to mathematical logic: (1) P05 converts cross-vm Array to host Array with `Array.from` before deep equality; (2) the injected `globalThis.__x.errorState` is a **live getter** rather than a stale copied scalar, making N07/N08 capture the actual update from `draw()`.
- `evidence/AXIOM_NODE_R16_Q0_R1_TEST_RECEIPT.json` is the actual Node v22.16.0 test output: **20/20 PASS, exit 0**.

**Remaining material gaps:** the stereographic projection is correctly FAIL_CLOSED on default pose when w=1, which is not a user-friendly production design. E1 must explicitly adjudicate changing camera/pole geometry before E3 visual UX work; the original E2 32883-byte full report is not in hand, and original production viewer source is not bytebound here. This PR authorizes **research-only use of the reference**, not a Hostinger release, production HTML rewrite, physical IMU, A72 closure or claim promotion.

Related P0 bodytwin panel overlap fix lives separately in PR #333; unrelated website hotfix and this research test shall never be conflated.
