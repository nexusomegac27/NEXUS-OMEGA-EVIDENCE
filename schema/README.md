# Schema domain

Machine-readable contracts live under `schema/`.

Historical v1/A83 schemas remain at their bound paths. New R5 contracts belong under `schema/r5/` and should have matching implementation/tests/validation material under the same phase slug.

Repository-wide artifact handoff automation is defined by:

- `artifact-handoff-envelope-v1.schema.json`
- `artifact-handoff-receipt-v1.schema.json`
- `artifact-handoff-ledger-event-v1.schema.json`

Repository-wide artifact rollout preparation is defined by:

- `artifact-rollout-plan-v1.schema.json`
- `artifact-rollout-receipt-v1.schema.json`
