# Auth Preflight — NOT REACHED (gate)

IF_NODE_BUS_READY = false → PERMIT_AUTH_PREFLIGHT = NO

## Observe-only (no mcp_auth, no token write)

### GITHUB_MCP
- namespace: plugin-github-github
- CURRENT_CONNECTOR_STATE: error / live tool discovery failed
- tools visible: mcp_auth only
- AUTH_FAILURE_CLASS: CONNECTOR_DISCOVERY_FAIL_OR_AUTH_REQUIRED (undifferentiated without auth probe)
- REQUIRED_SCOPE: NOT_ESTABLISHED_THIS_TURN
- SAFE_REMEDIATION_PATH: WAIT_NODE_BUS_READY → THEN separate AUTH_RESOLUTION order; DO_NOT_EXECUTE mcp_auth this return

### GITLAB_MCP
- namespace: plugin-gitlab-GitLab
- CURRENT_CONNECTOR_STATE: error / live tool discovery failed
- tools visible: mcp_auth only
- AUTH_FAILURE_CLASS: CONNECTOR_DISCOVERY_FAIL_OR_AUTH_REQUIRED (undifferentiated without auth probe)
- REQUIRED_SCOPE: NOT_ESTABLISHED_THIS_TURN
- SAFE_REMEDIATION_PATH: WAIT_NODE_BUS_READY → THEN separate AUTH_RESOLUTION order; DO_NOT_EXECUTE mcp_auth this return

DO_NOT_EXECUTE preserved:
MCP_AUTH_WRITE · TOKEN_ROTATION · NEW_CREDENTIAL_CREATION · PUSH · COMMIT · MERGE · DEPLOY
