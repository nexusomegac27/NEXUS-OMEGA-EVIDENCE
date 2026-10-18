# AXIOM Alpha-Node R3 — Event-record object fail-closed successor · 2026-10-18

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_EVENT_RECORD_OBJECT_GUARD_SUCCESSOR_20261018_R3
PREDECESSOR = NEXUS_OMEGA_AXIOM_ALPHA_EVENT_PARTITION_FRESH_INDEPENDENT_RETEST_20261018_R2
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = TESTED_IMPROVEMENT_ISOLATED_C1_BRANCH_READBACK_ONLY
ORIGINAL_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
SOURCE_PATH = scripts/archive_continuity_guard.py
SOURCE_BLOB = fe51de53a905a6c6ac5f8b999cbb34bed327a59d
SOURCE_BYTES = 8726
PARENT_RESEARCH_HEAD = 5982772fd8d340b3121747d085a72be81701a2a5
NEW_PATCH_BLOB = d48ad5bb3c0fa5aad4567e0424fa28c571d318cf
NEW_PATCH_SHA256 = b6802e013492e0e376721671a622d1a5e7e4a404022e2734f5a474d951264b39
NEW_PATCH_BYTES = 2370
FROZEN_EVALUATOR_BLOB = 7fb662b7a4f639a9cf44ec0e6a3c5c7f60d9b1d3
FROZEN_EVALUATOR_SHA256 = 0b2e880de710a7fb9d3e212702adcbb7069fe441b4c70f37f49886a85590ff3b
FROZEN_EVALUATOR_BYTES = 6247
```

## One candidate and negative hypothesis

The existing R0 event-partition research patch catches filename/time/partition and duplicate-ID mismatches but may crash on syntactically valid JSON whose top-level value is not an object. The new R3 append-only successor adds a single explicit `isinstance(data, dict)` guard before accessing event fields; it records malformed records as `INVALID_EVENT_RECORDS` rather than aborting the read-only audit.

The independent frozen 16-case evaluator was prepared and run **before** the successor patch was implemented. It extends the previous 12 tests with JSON top-level array/null/string and invalid UTF-8. The fourth case is an already correctly rejected regression, not a newly discovered failure.

| Same evaluator, local isolated execution | Passed | Failed/errors |
| --- | ---: | ---: |
| Original main | 9/16 | 4 assertion failures + 3 unhandled errors |
| Prior R0 event-partition patch | 13/16 | 3 unhandled errors |
| R3 successor | **16/16** | 0 |

The seven targeted malformed/path-integrity cases change from 0/7 (main), to 4/7 (R0), to 7/7 (R3). Valid historical, timezone, read-only and existing negative controls remain accepted/rejected as expected. The successor patch applies cleanly to an isolated copy of the original main source and reproduces byte-for-byte identical patched output. No repository runtime script was modified.

## Falsifiers and limitations

Falsifiers: an authoritative event-store contract permits non-object top-level event records; a valid historical event fails the guard; the patch does not apply to the pinned source; an external independent rerun disagrees. No third-party validation, production integration, race-condition safety or full security certification is claimed.

## Transport, review and target metrics

Both new research artifacts were created append-only on the existing owner research branch and their Git blobs read back against independently calculated local identities. The draft PR attempt was blocked by platform safety controls; the Issue #93 receipt write was also blocked. Neither was bypassed. This branch receipt is **not** an Issue #93 receiver acknowledgment.

Main merge = NO; CI on the new branch = NO_CHECKS_OBSERVED; runtime = unchanged; WWW parity = NOT_ESTABLISHED; R10 independent expert ACK = NOT_ESTABLISHED. No claim promotion.

Project-wide eligible public handoff numerator/denominator = UNKNOWN/UNKNOWN, so the 90% target is not computable. This iteration's intended complete public review handoff = 0/1 (draft PR + Issue receipt absent). Branch artifact fixity = 2/2 verified, not equivalent to main publication.

`EVIDENCE > AGREEMENT · BLOCKED_LANE != BLOCKED_SYSTEM · C1_DESCRIPTIVE_ONLY`
