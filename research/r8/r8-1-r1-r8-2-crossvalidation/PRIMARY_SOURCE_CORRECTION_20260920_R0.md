# Primary-source correction — Sentinel-2 Processing Baselines / REANA

Checked against current official sources on 2026-09-20.

## Sentinel-2 Processing Baseline

The R8 handover material contains a stale statement that PB 05.11 remained operational until the planned PB 05.13 transition.

Official ESA Sentinel Online states:

- PB 05.12 was deployed on **4 February 2026** and implements PSD 15.1.
- PB 05.13 is scheduled for deployment on **21 September 2026** and implements PSD 15.2.
- ESA's 15 September 2026 activation notice publishes the first A/B/C datatakes that will produce PB 05.13 products.

Therefore, on 2026-09-20:

```text
CURRENT_CONFIRMED_BASELINE = PB 05.12
PB 05.13 = SCHEDULED_FOR_2026-09-21, NOT YET THE CURRENT BASELINE
```

R8 Gate D remains unchanged: the exact processing baseline used in any scientific calculation must be read from the physical product metadata, not inferred from today's operational baseline.

## REANA

REANA is an open-source reproducible-analysis platform made at CERN. The project documents containerised analyses, multiple workflow engines and remote compute backends. A valid YAML file or REANA specification is **not** evidence that the supplied workflow executed.

For this NEXUS lane:

```text
WORKFLOW_PARSE != WORKFLOW_EXECUTION
CONTAINER_TAG != IMMUTABLE_CONTAINER_DIGEST
DECLARED_OUTPUT != RUN_RECEIPT
```

R3 therefore requires actual bound dependencies, run receipts and fresh-run output hashes before any REANA reproducibility claim.
