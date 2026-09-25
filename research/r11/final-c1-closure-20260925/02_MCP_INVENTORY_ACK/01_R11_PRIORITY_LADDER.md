# R11 Priority Ladder — MCP Inventory ACK Bind 20260925_R0

## Bound ladder (AXIOM ACK preserved)

```text
1. NEXUS_NODE_BUS → READY
2. GITHUB_MCP_AUTH → RESOLVE
3. GITLAB_MCP_AUTH → RESOLVE_OR_QUARANTINE
4. CURSOR_NATIVE_16_TOOLS → CLASSIFY
5. CAPABILITY_MATRIX → AUTHORITY_MATRIX
6. ONLY_THEN → LIVE_TRIGGER / AUTO_PUSH
```

## Status this bind

| Step | Target | Status |
|------|--------|--------|
| 1 | NEXUS_NODE_BUS READY | PENDING — live probe = LOADING |
| 2 | GITHUB_MCP_AUTH | PENDING — live probe = ERROR_AUTH |
| 3 | GITLAB_MCP_AUTH | PENDING — RESOLVE_OR_QUARANTINE |
| 4 | CURSOR_NATIVE 16 tools | DONE — CLASSIFIED |
| 5 | Cap → Authority matrix | BOUND_DESIGN (see 02) |
| 6 | LIVE_TRIGGER / AUTO_PUSH | BLOCKED until 1–5 |

## Cursor native tools (classified names)

```text
AwaitShell
ConnectScm
CreateGoal
Delete
EditNotebook
FetchMcpResource
GenerateImage
ReadLints
SearchConversations
SetActiveBranch
SwitchMode
Task
TodoWrite
UpdateGoal
WebFetch
WebSearch
```

CLASS = CURSOR_NATIVE_SESSION_TOOLS
COUNT = 16
AUTHORITY_FROM_PRESENCE = NONE

## Gate law

```text
WENN Step 6 before Steps 1–5 PASS,
DANN FAIL — ONLY_THEN LIVE_TRIGGER/AUTO_PUSH.

WENN NODE_BUS LOADING as READY treated,
DANN FAIL — LOADING != READY.

WENN ERROR_AUTH as capability PASS treated,
DANN FAIL — ERROR_AUTH requires RESOLVE or QUARANTINE.
```
