# R11 Step1 — Node Bus Proof Matrix (C1)

| PROVE | LOCAL_JSONL | CURSOR_MCP | VERDICT |
|---|---|---|---|
| NODE_BUS_PRESENT | PASS (server + mcp.json) | PRESENT_NS | PARTIAL |
| NODE_BUS_RESPONDS | PASS | FAIL discovery | BLOCKED |
| TOOL_REGISTRY_RESOLVES | PASS 11 tools | UNRESOLVED | BLOCKED |
| NODE_IDENTITY_BOUND | FAIL absent | N/A | BLOCKED |
| JOB_ID_PROPAGATES | PASS 864b28d0… | NOT_TESTED_MCP | LOCAL_PASS |
| RECEIPT_RETURN_PATH_WORKS | PASS c5f86fa6… | NOT_TESTED_MCP | LOCAL_PASS |
| FAIL_CLOSED_ON_INVALID_JOB | PASS | NOT_TESTED_MCP | LOCAL_PASS |
| DUPLICATE_EVENT_NOOP | PASS idempotent | NOT_TESTED_MCP | LOCAL_PASS |

Authority boundary local: PROHIBITED list present; claim promotion hard-fail; llm_hot_path false.

REQUIRED_TERMINAL for READY not met: Cursor registry unresolved + identity unbound.
