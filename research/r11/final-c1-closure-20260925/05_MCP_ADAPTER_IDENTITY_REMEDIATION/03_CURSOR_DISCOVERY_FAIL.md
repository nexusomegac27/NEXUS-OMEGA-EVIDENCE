# Cursor Discovery Fail

EXPECTED_NAMESPACE = project-0-Perfect Final Version-nexus-node-bus
PROBE = GetDynamicTools pattern = nexus|node-bus|node_bus
RESULT = matches = []
INVENTED_DISCOVERY = NO
CLASS = CURSOR_NAMESPACE_ABSENT

mcp.json points at Local Python + mcp_stdio_adapter.py with PYTHONUNBUFFERED / WIRELOG.
Local adapter validate all_pass=true does not bind Cursor catalog.
