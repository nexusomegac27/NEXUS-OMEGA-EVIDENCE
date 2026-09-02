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
├── handoff/     GitHub agent-return inbox and transport receipts
├── rollout/     separate rollout preparation and Authority-Gate packets
├── packages/    stable package roots + immutable sealed snapshots
├── index/       rebuildable navigation projections
└── templates/   package/event templates
```

Research publication is not live implementation. Promotion into stable `docs/schema/scripts/tests/validation/examples` requires a separately governed integration path.
