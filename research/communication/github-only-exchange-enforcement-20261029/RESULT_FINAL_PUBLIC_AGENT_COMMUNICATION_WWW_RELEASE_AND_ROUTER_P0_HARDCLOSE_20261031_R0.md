# NEXUS OMEGA · CURSOR RETURN
## FINAL PUBLIC AGENT COMMUNICATION WWW RELEASE + ROUTER P0 HARD CLOSE · 2026-10-31

OBJECT = NEXUS_OMEGA_CURSOR_FINAL_PUBLIC_AGENT_COMMUNICATION_WWW_RELEASE_AND_ROUTER_P0_HARDCLOSE_RETURN_20261031_R0
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
ORDER_PIN = 7587f26b88f48a49b6a1b0db9f1c07ae63ca715c
ORDER_BYTES = 9597
ORDER_SHA256 = 54649b6863ca9085d2ae02f620efa3312b2e4b473f19858aa6c307f51b7638a3
ORDER_REHASH = MATCH

## WWW publication (independent HTTP body SHA-256)

| Route | HTTP | Bytes | SHA-256 | Match |
| --- | --- | --- | --- | --- |
| /ai/agent-border/communication/ | 200 | 13521 | 1b9a7902b64bf8fd1059821d33bb7dab604194212ee14e2378090bd0ed1f6987 | MATCH source HTML |
| /ai/agent-border/communication/status.json (candidate then LIVE) | 200 | 3230 | 3e6d6d46297a46fa11e1b7de08ec8ab66af0eddc8aac48e8d58389da6fe62707 | LIVE_READ_ONLY_CONFIRMED |
| /ai/agent-border/communication/protocol.json | 200 | 2417 | 8c5f45076e4b21607903c39a8b46b2d7bd1d923e70a7e775dec53802dfc26b51 | MATCH source PROTOCOL |

HOSTINGER = u310432914@82.198.228.32:65002 SCP scoped to public_html/ai/agent-border/communication/ + nav link in border index.html
ROLLBACK_REHEARSAL = PASS (pre index restored then re-applied; remote backup under .nexus-releases/agent-comm-20261031/)
BROWSER_DESKTOP = PASS (title Agent Communication Framework; status.json reachable; no script/form)
ORIGINAL_BORDER_REGRESSION = PASS (manifest/canonical-head/well-known/dissent/L07/L10/L12 HTTP 200 unchanged routes)
PUBLIC_EXTERNAL_WRITE_API = OFF
CUTOVER_ACTIVE = NO

## DocumentRouter P0 hard-close

P0_ROUTER_CODE = scripts/nexus_document_router.py
P0_ROUTER_BYTES = 45479
P0_ROUTER_SHA256 = 98508e051ff78092e13615fec84f6faf36d857baddd31c8199d6b07872e10eb7
FORGED_ACK_NEGATIVE = PASS (authenticated/return_source_verified self-assert ignored; ACK remains NOT_ESTABLISHED without github_api_witness)
DISPATCH_TRANSPORT_WITNESS = PASS (local journal -> OUTBOUND_QUEUED; DISPATCHED only with TRANSPORT_API_VERIFIED + connected adapter)
ACTIVE_GATE_NEGATIVE = PASS (--activate-cutover / cutover_force_active alone leaves STAGED; requires activation manifest gates PASS)
PRIVACY_PRIVATE_NEGATIVE = PASS (allow_private_dispatch alone insufficient; OWNER_PRIVATE_LANE_V1 proof required)
LOCAL_TESTS = 22_OF_22_PASS
PUBLIC_INTERFACE_STATIC_TESTS = 11_OF_11_PASS_AT_SOURCE_CANDIDATE
EXTERNAL_AUTHENTICATED_RECEIVER = NOT_ESTABLISHED
PR185 = OPEN_DRAFT_NO_AUTO_MERGE
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STRUCTURE = 1.7.24
NEXT = AXIOM_INDEPENDENT_WWW_BYTES_AND_ROUTER_P0_ADJUDICATION

STATE = PASS_WITH_MATERIAL_CAVEATS_C1_WWW_LIVE_READ_ONLY_ROUTER_P0_HARD_CLOSED_CUTOVER_NOT_ACTIVE
