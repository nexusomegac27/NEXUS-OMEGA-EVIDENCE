# Exact Blockers (preserve)

## BLOCKER_1
CLASS = PROTOCOL_CUSTOM_JSONL_NOT_MCP_STDIO_HANDSHAKE
SURFACE = Cursor MCP namespace project-0-Perfect Final Version-nexus-node-bus
PARENT_STATE = LOADING
THIS_TURN_STATE = error (discovery failed)
SERVER = .nexus/node-bus/server/nexus_node_bus.py
CODE_FACT = main() implements Minimal JSON-lines stdio (tool/arguments), not MCP initialize + tools/list JSON-RPC
REPAIR_PATH_IF_AVAILABLE = Adapter or server rewrite to MCP stdio handshake under NEW Operator/AXIOM order only (NOT this return)
SAFE_NEXT = PRESERVE · NO_RESEARCH_REPEAT · NO_SILENT_PROTOCOL_MUTATION

## BLOCKER_2
CLASS = NODE_IDENTITY_NOT_BOUND
EVIDENCE = LOCAL_JSONL_PROOFS.json proofs.NODE_IDENTITY_BOUND=false · capabilities omit node identity field
REPAIR_PATH_IF_AVAILABLE = Bind NODE_IDENTITY in capabilities/schema under NEW order
SAFE_NEXT = PRESERVE · do not invent URN

CRITIQUE_REQUIRES_REPAIR_PATH_V1
1. WHY_WRONG = Cursor MCP plane cannot list/call Node Bus tools; identity field absent
2. VIOLATED_RULE_OR_EVIDENCE_GAP = REQUIRED_TERMINAL READY unmet; TOOL_REGISTRY / NODE_IDENTITY proofs incomplete on Cursor plane
3. REPAIR_PATH_IF_AVAILABLE = MCP handshake adapter + identity bind (separate order)
4. SAFE_NEXT_ACTION = Seal INCOMPLETE · wait remediation order
5. WAIT_OR_HARDSTOP_REASON_IF_NO_REPAIR_EXISTS = N/A repair exists but NOT authorized this gate
