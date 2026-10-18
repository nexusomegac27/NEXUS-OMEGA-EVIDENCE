# R18-R2 — Local C1 research reproduction

This bundle is **research-only**. It does not deploy, run SAC, create a NEXUS agent, authenticate a real Judge, check a real network, or claim scientific/production acceptance. Source links are content-reviewed only: K7 HTTP raw-body audit remains incomplete.

## Reproduce synthetic protocol gate

Requires Python >=3.10, standard library only. Extract ZIP, enter its folder, run:

```bash
python -m unittest -v test_r18_r2_frozen_contract.py
```

Expected `Ran 14 tests; OK`. Test method #2 contains 23 parametrized negative/boundary subcases — do not report them as 23 additional independent tests.

To intentionally break the `integrity FAIL` veto (negative control), run in `mutation/`:

```bash
cd mutation
python -m unittest -v test_r18_r2_frozen_contract.py
```

Expected **nonzero** exit; `Ran 14 tests; FAILED (failures=2)`. The test suite was authored before the candidate, but both are from the same AXIOM session, not an independent accepted oracle.

## Integrity and scope

`R18_R2_MANIFEST.json` lists SHA-256 and byte size for every payload file. Verify all before replay. `R18_R2_SOURCE_SCOPE_AND_CORRECTION_LEDGER_20261018_R0.json` marks external raw HTTP provenance null because neither direct HTTP response bodies nor full K7 header receipts were captured. GitHub commit pins and content-scoped links are distinguishable from HTTP-body fixity.

The R18-R1 parent ZIP is not duplicated in this bundle: 98,547 bytes, SHA-256 `08b51af99c973c2fb86b49ccea989be587ca52844674b925438b681e338f527d`. Prior R18 C01–C47 draft is **not ratified**, and no Shadow-Loop is permitted.
