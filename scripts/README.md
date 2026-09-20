# Scripts and validators

Executable repository tooling lives under `scripts/`.

Historical validators remain at their stable paths. New R5 reference implementations and validators belong under `scripts/r5/`. Repository-wide structural enforcement is implemented by `validate_repository_structure.py`.

`artifact_handoff.py` validates and processes the GitHub artifact handoff inbox.
It emits bind, relay and ack receipts only after fail-closed byte and protocol
validation.
