# Active research domain

`research/` is the canonical intake and working surface for public research that has **not** been integrated into the stable framework.

Normal research lanes use:

```text
research/<phase>/<agent-or-topic>/
```

Recommended agent subtree:

```text
README.md
orders/
returns/
receipts/
sources/
experiments/
patches/
```

## Shared AXIOM↔Cursor pipeline infrastructure

`research/pipeline/` is the one cross-phase exception to the normal phase/agent hierarchy. It is infrastructure for grouping many research deltas into stable, timestamped packages for later Cursor processing.

It does **not** replace the canonical source lane of any research artifact. Pipeline packages normally reference existing source/return/receipt objects by exact repository path, commit/blob identity and SHA-256 where available.

```text
research/pipeline/
├── events/      append-only lifecycle events
├── packages/    stable package roots + immutable sealed snapshots
├── index/       rebuildable navigation projections
└── templates/   package/event templates
```

Research publication is not live implementation. Promotion into stable `docs/schema/scripts/tests/validation/examples` requires a separately governed integration path.

## Current phase-IX foundation

- `research/ix/open-agent-foundation-r1/` — provider-neutral Open-Agent research foundation.
- `research/ix/open-agent-foundation-r2/` — integrity/boundary/provenance research foundation.
- `research/ix/open-agent-foundation-r3/` — controlled-falsification validation and R4 carry-forward.
- `research/ix/open-agent-foundation-r4/` — canonical R4 external-research order; agent activation remains off.
- IX remains `IX_EXECUTION=NOT_STARTED`.
- `research/fundus/` — cross-session C1 reference index; not a truth authority.

These paths are research/checkpoint surfaces only. They do not imply production integration or activation.

## R27-E · Operator-owned external return slot

`research/r27/www-extern-wake-isolation-20261011/returns/` is the first **preallocated** external-agent return slot. Its seven exact allowed filenames are registered in `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json`. Neither external agents nor website visitors may create a new phase, agent namespace, return subdirectory or internal control-plane path. External GitHub principals require explicit operator registration and a real required-check / review ruleset. Preintegration research remains descriptive C1, not an implementation.

- [`r15/soft-geography-gps-fov-20261018/`](r15/soft-geography-gps-fov-20261018/) — read-only owner R15-R2 adversarial GIS research and external expert MAXI preparation; no new external writer, source appendix not execution authorization.
