# R11 MCP Adapter + Identity Remediation Matrix

Claim ceiling: C1_DESCRIPTIVE_ONLY

| Blocker | Parent state | Remediation | Local result | Cursor plane |
|---------|--------------|-------------|--------------|--------------|
| B1 CUSTOM_JSONL_STDIO_NOT_MCP | OPEN | Thin MCP stdio adapter over handle_tool | PASS dual protocol + tools + health | FAIL discovery |
| B2 NODE_IDENTITY_NOT_BOUND | OPEN | node_identity.py + receipt bind + nexus://node/identity | PASS fields + receipt match | NOT_REACHED |

## Architecture (locked)

```text
EXISTING_JSONL_WORKER = EXECUTION_CORE
MCP_ADAPTER = TRANSPORT_SKIN
REBUILD_NODE_BUS = NO
```

## Preserved paths

| Path | Status |
|------|--------|
| JOB_ID_PROPAGATION | PASS (eb3d9cca…) |
| RECEIPT_PATH | PASS (4f889fe7…) |
| REPLAY | PASS MATCH (merkle 2c5d39a2…) |
| FAIL_CLOSED_INVALID_JOB | PRESERVED (not re-broken) |
| DUPLICATE_EVENT_NOOP | PRESERVED (not re-broken) |

## Hard gate

```text
IF NODE_BUS_READY THEN AUTH_PREFLIGHT
ELSE STOP_WITH_EXACT_PROTOCOL_ERROR = CURSOR_NAMESPACE_ABSENT
```

NODE_BUS_READY = FALSE → Auth not executed.
