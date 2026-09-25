# Capability ≠ Authority Matrix — 20260925_R0

## Laws (normative)

```text
MCP_READY != AUTHORITY
TOOL_COUNT != CAPABILITY_QUALITY
CAPABILITY != WRITE_PERMISSION
OBSERVABILITY != CANONICAL_EVIDENCE
SHADOW_FABRIC != LIVE_DEPLOY
TRIGGER != AUTHORITY
```

## Namespace disposition (C1 descriptive)

| Namespace / plane | Capability class | Authority class | Disposition |
|-------------------|------------------|-----------------|-------------|
| READY ×12 (generic MCP) | TOOL_SURFACE_PRESENT | NONE by default | USE_ONLY_UNDER_GATE |
| GITHUB_MCP | ERROR_AUTH | NONE | RESOLVE before use |
| GITLAB_MCP | ERROR_AUTH | NONE | RESOLVE_OR_QUARANTINE |
| NEXUS_NODE_BUS | LOADING | NONE | WAIT_READY (R11 step 1) |
| CURSOR_NATIVE ×16 | SESSION_TOOLS | NONE as write/deploy | CLASSIFIED |
| HOSTINGER | CAPABILITY_ONLY | NO_WRITE_AUTHORITY this bind | NO Hostinger write |
| POSTHOG | DERIVED_OBSERVABILITY | NOT_CANONICAL_EVIDENCE | Observe only |
| PARENT_FABRIC | SHADOW_BUILT | LIVE_DEPLOY=NO | PRESERVED |

## Write / push authority

```text
LIVE_WRITE = NO
LIVE_PUSH = NO
AUTO_PUSH = NO
HOSTINGER_WRITE = NO
REPO_COMMIT_PUSH = NO_WITHOUT_EXPLICIT_OPERATOR_ORDER
MCP_AUTH_INVOKE = NO_THIS_BIND
```

## Desktop Commander Remote (bridge note)

```text
CLASS = CONTROLLED_CLOUD_RELAY_BRIDGE_CANDIDATE
FUNDAMENT = NO
LOCAL_STDIO_OSS = SEPARATE_PLANE
START_THIS_BIND = NO
PAIRING = CONFIRM_ONLY_IF_BROWSER_CODE_EQ_TERMINAL_CODE
```

## WENN-DANN

```text
WENN Agent READY-Status als Write-/Push-Autorität liest,
DANN FAIL — MCP_READY != AUTHORITY.

WENN Agent TOOL_COUNT als Qualitäts- oder Capability-Beweis setzt,
DANN FAIL — TOOL_COUNT != CAPABILITY_QUALITY.

WENN Agent PostHog als kanonische Evidenz nutzt,
DANN FAIL — OBSERVABILITY != CANONICAL_EVIDENCE.

WENN Agent Shadow-Fabric als Live-Deploy liest,
DANN FAIL — SHADOW_FABRIC != LIVE_DEPLOY.
```
