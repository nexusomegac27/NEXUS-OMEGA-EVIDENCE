# CURSOR HANDOFF — Snapshot v2

```text
PACKAGE_ID = NEXUS_RP_20260901T035600Z_retroactive-symbiotic-backfill_6f1a9c27
SNAPSHOT = v2
STATE = READY_FOR_CURSOR
PREDECESSOR = snapshots/v1
CURSOR_ACTION = START
CLAIM_CEILING = C1
```

Read in this order:

1. `CURSOR_FULL_BUNDLED_ORDER.md`
2. `GITHUB_BRIDGE_PROTOCOL.md`
3. `CURSOR_ACK_INPUT.txt`
4. `A90_AXIOM_COMPLETION_STATE.json`
5. `A90_PLAN_BINDING.md`
6. `items.json`
7. `provenance.json`
8. `manifest.json`
9. `SHA256SUMS.txt`

First mandatory action: verify `SHA256SUMS.txt`, observe current live `main`, then post the execution ACK in the GitHub PR conversation.

Do not mark `PROCESSED` until a terminal Cursor return exists.
