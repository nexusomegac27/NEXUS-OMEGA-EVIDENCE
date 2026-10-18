# R15/R2 · Reproduction / GitHub publication guide

**No real GPS, user position, network request, 3D renderer, private device or Hostinger output is contained.** Code is standard-library Python only. All metrics in this stack are *synthetic*; neither test success nor a hash match is a scientific truth claim or publication permission.

## Reproduce

```bash
python frozen_byte_ledger_evaluator.py synthetic_byte_ledger_guard.py
# Expect FINAL 22 / 22, exit 0.
python frozen_byte_ledger_evaluator.py mutant_missing_pairwise_context_guard.py
# Expect FINAL 20 / 22 with explicit wrong_dataset/wrong_view failures, exit 1.
```

Verify archive/manifest SHA-256 with any independent implementation. The previous R15 R1 original archive is not redistributed: original 110,827 bytes, SHA-256 `a725dbc35fcc6d8a5524460bd6217e3355a7517cf269a00a2f71160553eb7229`. Query original sources; do not interpret the 6,917-byte Cursor FOUNDATION_MD claim as the 25,683-byte original markdown.

## Scope

- Frozen evaluator was authored and SHA256-finalized before candidate implementation.
- Comparison only computes **invented response-body bytes** in paired, explicitly synthetic traces. It does not authenticate the source hashes nor capture completeness flags.
- No real network instrumentation, no consent-driven GNSS, no 3D frustum, no browser replay, no field experiments, no external peer review.
- No new external-agent write privileges. Candidate must not be integrated into R15 mobile runtime without separate operator-granted authority and independent scientific review.

## GitHub owner-gated placement

Suggested lane: `research/r15/soft-geography-gps-fov-20261018/`. This is a **new research directory** absent from pinned main and cannot be created by any external actor. An authorized owner mutation needs to register it in root `README.md` and `docs/architecture/REPOSITORY_STRUCTURE.json` as one reviewed PR, run existing structural validation, and read back the resulting commit. A branch report alone is not main publication. Issue #93 receives an append-only receipt **only after** a real observed GitHub write. Never assume 2026-10-17 main and current main are the same without checking again.
