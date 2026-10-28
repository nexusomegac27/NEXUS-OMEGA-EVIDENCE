# NEXUS OMEGA · AXIOM Alpha-Node · Handoff denominator witness · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_DENOMINATOR_WITNESS_20261028_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PREDECESSOR_ISSUE93_RECEIPT=6464324854
PINNED_MAIN_BEFORE=2d9bebb5788bdcc47d95a2e68fb955d5cd230356
FROZEN_EVALUATOR_FIRST_COMMIT=f181a0e98d082366785b82b63dad8746043aa521
CANDIDATE_SECOND_COMMIT=dc0db9abf123a2d28fc880fea3b9a1a6cffb632b
PRODUCTION_STEWARD_CHANGED=NO
```

## One bounded candidate: observable numerator and denominator

The preceding receipt-file digest witness verifies caller-provided file bytes but explicitly cannot authenticate GitHub origin or completeness. Prior Alpha receipts report project-wide `AUTOMATION_RATE=NOT_COMPUTABLE`: there is no complete, authenticated enumeration of all eligible public routine authorized accessible handoffs. The 90% goal is a target, **not** a measured current result. This candidate isolates the **denominator classification** and four-part readback arithmetic without claiming source completeness.

**Negative hypothesis:** a naive handoff counter inflates the automation numerator by including private/local or inaccessible events and inflates the readback numerator when one required readback is absent. **Falsifier:** if a frozen subprocess oracle finds that the candidate counts either excluded class, accepts missing readback as complete, computes a rate with unknown eligibility, or claims a project-wide rate, the candidate fails.

The only new artifacts are three additive research files in the existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` owner lane. No new pipeline root, governance, CI, source overwrites, runtime, Hostinger, WWW, actor registration, or task-anchor rewrite.

## Independent frozen oracle and isolated tests

- Frozen subprocess evaluator `frozen_handoff_metric_evaluator_v1_20261028.py`: 5,266 bytes; SHA-256 `67b2ff73c2f1cfc6ef36738ea1fd1951c4526084054ef587b342db2c6449ab8e`; Git blob `6419917ab52b1f13c9fed8bcb54649f72b569b1f`. Committed **before** the candidate on `f181a0e98d082366785b82b63dad8746043aa521`.
- Candidate `alpha_handoff_metric_witness_v1_20261028.py`: 6,431 bytes; SHA-256 `df569e5ff841157d72379c344c8e1997e820911479efe2faa05c708fdf1b16b0`; Git blob `c98b8e9334255ad82c04788450ef1b17360f66ed`. Committed on `dc0db9abf123a2d28fc880fea3b9a1a6cffb632b`.
- Local Python subprocess oracle: **15/15 PASS** on synthetic data. No candidate imports by evaluator; no external third-party review claimed.
- Negative mutant removing private-channel exclusion: **10/15 PASS**, 5 expected failures. Negative mutant bypassing the four readback flags: **14/15 PASS**, 1 expected failure. Neither mutant was published.

Synthetic declared-complete 12-event fixture: 10 eligible public/routine/authorized/accessible events, 9 published without manual nudge, 2 excluded (one private, one inaccessible public). **Sample-only arithmetic: 9/10 = 90%**. Eleven public publications in the fixture have all four readbacks: **11/11**. These are **not real NEXUS project rates**. A missing source readback yields 10/11, a public unknown eligibility yields `NOT_COMPUTABLE`, and partial declared coverage prevents a scope rate. Duplicate IDs, duplicate JSON keys, nonfinite JSON, malformed flags, and oversized input fail closed.

## Trust and publication boundary

The tool only processes **caller-supplied** event records. `DECLARED_COMPLETE` is not externally authenticated completeness; `source_commit_sha` and `source_manifest_sha256` are syntactically checked but not independently retrieved or hashed. The output deliberately sets `api_origin_authenticated=false`, `source_completeness_authenticated=false`, `project_automation_rate=NOT_COMPUTABLE`, and `global_zero_violations_established=false`. A reported zero in a synthetic sample is not evidence of zero unauthorized writes project-wide. No actual NEXUS handoff numerator or eligible denominator is established by this test.

A future real metric requires an independently complete, source-exact inventory of public GitHub handoff opportunities, including failures, with actor/authorization, accessibility, publication, manual-nudge and four separate readback receipts verified at immutable refs. Locally private or inaccessible material must not enter the success numerator. This is a research scaffold, **not** an automatic CI oracle, self-approval, runtime integration, or new recurring task.

R10 PR #115 and Issue #93 readback: no new independently authenticated R10 expert return observed in the checked channels. Owner-public SEND is distinct from independent receiver ACK, authenticated actor, scientific adjudication and actual expert execution. R10 manifest was physically read from pinned commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` (Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, 4,588 UTF-8 bytes). Expert return remains `SOURCE_NOT_PRESENT` for this check. No R10 dispatch, ZIP, Cursor, experiment or merge authorization.

PR CI, merge, actual-main byte readback, and Issue #93 receipt are **not** asserted by this pre-merge report; they are separate downstream gates. `BLOCKED_LANE != BLOCKED_SYSTEM`, `DRIFT_RESET=NON_DESTRUCTIVE`, `C1_DESCRIPTIVE_ONLY`.
