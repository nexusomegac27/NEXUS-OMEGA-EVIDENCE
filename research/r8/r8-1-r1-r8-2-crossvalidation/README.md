# NEXUS OMEGA R8.1-R1 + R8.2 — Independent AXIOM Cross-Validation

```text
OBJECT = NEXUS_OMEGA_AXIOM_R8_1_R1_AND_R8_2_FULL_CROSSVALIDATION_20260920_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_R1_CUSTODY_VALIDATED_R2_SIMULATION_PARTIALLY_REPRODUCED_R3_REQUIRED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
```

This lane validates the late R8.1-R1 remediation package and the R8.2 simulation package contained in the supplied Grok→AXIOM closure drop. It is append-only and does not overwrite the earlier R8.0/R8.1 custody adjudications.

## Source drop

Outer closure ZIP:

- bytes: `6702429`
- SHA-256: `78e0471c67cc7d283e3d922f3cc1f8758e3f35d831f9fd93167d2403d5a9eec3`
- entries: `10`
- ZIP CRC: `PASS`

### R8.1-R1 package

`[STRIPPED-83-bytes].zip`

- bytes: `9074`
- SHA-256: `feb93ac28ec960b43df873b01d62c0b6f226274e97aea8ab02d6d122ed3e6c3a`
- entries: `16`
- ZIP CRC: `PASS`
- checksum manifest: `15/15 MATCH`, covering every non-self file
- JSON parse: `PASS`
- Python stub compile: `PASS`

The package is byte-identical `16/16` to the `artifacts/r8_1_r1_package/` subtree in the supplied workspace snapshot `cosU82vZIanmzdeA-grok-workspace.zip`.

Scientific state:

```text
PHYSICAL_RASTER_BYTES = ABSENT
SOURCE_IDENTITY = NOT_ESTABLISHED
NDVI = NOT_COMPUTED
NDVI_UNCERTAINTY = NOT_ESTABLISHED
```

The source-control guard objects, explicit SCL mask policy, provenance erratum and rejection of hard-coded NDVI/uncertainty values are accepted as C1 method/custody results.

Claims that an executable REANA successor, SNAP implementation, real container digests or complete dual implementation already exist are **not physically established by this R8.1-R1 ZIP**. No REANA YAML or SNAP graph is present; Implementation A is a guard stub and Implementation B contains configuration only.

### R8.2 simulation package

`R8_2_SIMULATION_CATEGORY_MISTRAL_VIBE_GROK_R1.zip`

- bytes: `6484`
- SHA-256: `4f6a0f9059edc33aacb8db41a25e0b3a9c636f2b071f3892dc80d6cc2e214a76`
- entries: `8`
- ZIP CRC: `PASS`
- listed checksum objects: `6/6 MATCH`
- non-self objects in ZIP: `7`
- full non-self manifest coverage: `6/7`
- uncovered object: `26_PUBLICATION_ELIGIBILITY_SIMULATION.json`

The package is byte-identical `8/8` to the `artifacts/r8_2_sim/` subtree in the supplied workspace snapshot.

## R8.2 reproduced results

### SIM-01

The first-order analytic calculations are independently reproduced:

```text
Red = 0.08
NIR = 0.25
NDVI = 0.515151515151515

sigma_abs = 0.02 per band
analytic_sigma_abs = 0.09641435995156428

sigma_rel = 0.15% per band
analytic_sigma_rel = 0.0007791810261008788
```

The packaged script SHA-256 is:

`0b3a51eabf91c1c617f43d034608f382176ed1ba0a50c60c5dfa82aab72ac010`

The JSON declares Monte Carlo `N=100000`, while the script's main entry point executes only `N=10000` for the absolute case and does not emit the relative Monte Carlo result.

Independent execution of the packaged function at `N=100000, seed=42` gives:

```text
MC_sigma_abs = 0.0978928157035729
difference_from_first_order_Taylor = +1.5334393681%

MC_sigma_rel = 0.0007795006983539178
difference_from_first_order_Taylor = +0.0410266988%
```

Therefore the package's negative fixture “>1% deviation from analytic means implementation bug” is rejected as an invalid universal criterion for the nonlinear ratio under the stated absolute-noise model. First-order Taylor and Monte Carlo are different estimators/models here; disagreement above 1% is not by itself evidence of a coding defect.

### SIM-02

The synthetic class-distribution arithmetic is reproduced:

```text
POLICY_A = 0.25 + 0.30 + 0.10 + 0.15 + 0.035 = 0.835
POLICY_B_CORE = 0.25 + 0.30 = 0.55
```

This is a synthetic sensitivity example only. It is not a measured Lübeck valid-pixel fraction and does not validate `0.87`.

### SIM-03

The coordinate transform is independently reproduced with pyproj 3.7.2 / PROJ 9.5.1:

```text
EPSG:4326  lon=10.6890 lat=53.8694
→ EPSG:25832
E = 611054.5344123215
N = 5970313.421324412
```

Accepted claim: deterministic CRS transformation result.

Not accepted from the package:

- a demonstrated ITRF2020→ETRS89 epoch-dependent Helmert step;
- generic `CE90 8 m` as current product truth;
- the listed ECEF triple as independently reproduced.

Direct WGS84 geodetic→ECEF reproduction for h=0 gives approximately `3703567.929, 699060.032, 5128186.228`, about 8.12 m vector distance from the package's listed ECEF example.

## REANA simulation workflow

`17_REANA_R8_2_SIMULATION.yaml` parses as YAML, but parseability is not execution proof.

Execution eligibility is not established because:

- `inputs.files` lists only SIM-01 files while later steps consume SIM-02/SIM-03 files;
- the coordinate step imports `pyproj`, while no dependency installation or pinned image containing pyproj is bound;
- `python:3.11-slim` is tag-pinned, not digest-pinned;
- no REANA run receipt, output hash or fresh-run pair is supplied.

## Workspace snapshots

The two supplied workspace ZIPs are physically non-identical:

```text
A = 3298421 bytes
SHA256 = 2a9c2dcd642d2de1b7528034cab3271029b094e6df8848503437810522c6a751
entries = 364

B = 3306107 bytes
SHA256 = 6647ec76db1b217bd58c68185fac036d21014ccf9a405e1d2f1b9da6f8c5eb79
entries = 376
```

At file level: A has 284 files, B 296, 284 common, 12 only in B, and 5 common files differ. No `.git` content was found.

The package closure's claimed temporal/causal ordering is **not established from ZIP timestamps alone**. The snapshot containing the extra R8.2 artifacts carries an earlier uniform ZIP timestamp than the smaller snapshot. Accepted claim: structural non-identity and explicit delta only.

## Current publication boundary

Publication-eligible now:

- R8.1-R1 physical hash/manifest facts;
- empirical HOLD state;
- provenance and mask-policy corrections;
- reproduced SIM-01 analytic values with Monte Carlo caveat;
- reproduced SIM-02 synthetic arithmetic;
- reproduced SIM-03 EPSG transform;
- negative evidence and package deficiencies.

Not publication-eligible as validated results:

- empirical NDVI;
- empirical valid-pixel fraction;
- empirical NDVI uncertainty;
- executable REANA claim;
- full R8.2 atomic simulation promotion under the package's own hash criteria;
- workspace chronology/causality.

R3 must close these simulation-specific reproducibility and atomic-binding gaps before the simulation atoms are handed to Cursor.
