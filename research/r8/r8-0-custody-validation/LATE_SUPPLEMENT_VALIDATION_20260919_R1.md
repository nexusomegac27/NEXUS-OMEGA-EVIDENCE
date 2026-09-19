# R8 late supplement validation — Mistral/Vibe custody package

```text
OBJECT = NEXUS_OMEGA_AXIOM_R8_LATE_SUPPLEMENT_VALIDATION_20260919_R1
STATE = PASS_WITH_MAJOR_CAVEATS_C1_LATE_SUPPLEMENT_BOUND_NO_EMPIRICAL_PROMOTION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
```

Two files were supplied after the original R8.0/R8.1 validation and are treated as a late supplement to the same drop:

1. `Nexus-R8-Final-Mistral-Vibe.html`
2. `R8_0_R8_1_CUSTODY_BIND_FINAL_MISTRAL_VIBE_VALIDATED.zip`

This addendum does not rewrite the previous validation. It updates only the evidence scope affected by the late supplement.

## Physical bind

```text
HTML_BYTES = 195838
HTML_SHA256 = 541b4394003b35330a53f9897b9f98d152e59b480aeac406a7ddd9b8a37a78f9

FINAL_ZIP_BYTES = 13030
FINAL_ZIP_SHA256 = 5b7e46f0604f9bddc8d76ecbbc8909f07c928c89e1b2c1bc92ac0807bed839dd

FINAL_ZIP_ENTRIES = 12
ZIP_CRC = PASS
PATH_TRAVERSAL = NONE_FOUND
```

## Relation to the previously validated R8.1 nested package

The previously bound R8.1 ZIP had SHA-256:

`1614a7be408b4fdeb744f35a14375dd00a7e285d7710985d8c6608e5f762a135`

All eight files from that package are byte-identical in the late final ZIP. The late final ZIP adds four files:

- `R8_0_CUSTODY_BIND_FINAL.json`
- `01_INPUT_INVENTORY.json`
- `02_SHA256SUMS.txt`
- `26_PUBLICATION_ELIGIBILITY.json`

Therefore the late ZIP is a packaging/custody extension, not a new empirical raster result.

## Checksum-manifest correction

The earlier outer R8 drop did not contain the referenced `02_SHA256SUMS.txt`. The late supplement **does** contain one.

All 10 files listed by `02_SHA256SUMS.txt` independently rehash MATCH.

However the ZIP contains 12 entries total. Excluding the checksum manifest itself leaves 11 other files, while only 10 are covered. `26_PUBLICATION_ELIGIBILITY.json` is not bound by the manifest.

Correct state:

```text
CHECKSUM_MANIFEST_PRESENT = YES
LISTED_OBJECTS_REHASH = 10_OF_10_MATCH
FULL_NON_SELF_PACKAGE_COVERAGE = 10_OF_11
SEALED_FULL_PACKAGE_MANIFEST = NOT_ESTABLISHED
```

This supersedes only the prior statement that no checksum manifest was supplied; it does not establish a fully sealed package.

## Scientific content

The supplement preserves the correct empirical gate:

```text
B04 = ABSENT
B08 = ABSENT
SCL = ABSENT
SOURCE_IDENTITY = NOT_ESTABLISHED
NDVI = NOT_COMPUTED
PUBLICATION_ELIGIBILITY = NO
```

Those are accepted.

The following defects from the prior R8.1 validation remain unchanged because the underlying eight files are byte-identical:

- `17_REANA_R8_1.yaml` still fails YAML parsing.
- referenced workflow inputs remain absent;
- implementation hashes remain placeholders;
- container digests remain placeholders;
- hard-coded `valid_fraction=0.87` remains an example, not a measurement;
- no physical raster computation or independent raster replication exists.

## New/remaining overclaims

`26_PUBLICATION_ELIGIBILITY.json` correctly blocks publication, but its field

`UNCERTAINTY = ESTABLISHED_MATHEMATICAL_MODEL - Tier optimistic ±0.005 conservative ±0.025 CE90 ±8m`

is not accepted as an established empirical uncertainty result.

The supplied uncertainty model's own first-order equation gives, for its stated Red=0.08, NIR=0.25 and sigma=0.02 per band:

`sigma_NDVI ~= 0.09641436`

For its stated 0.15% relative example:

`sigma_NDVI ~= 0.00077918`

Therefore:

```text
NDVI_UNCERTAINTY = NOT_ESTABLISHED
FIXED_TIER_0_005 = NOT_VALIDATED
FIXED_TIER_0_025 = NOT_VALIDATED
CE90_8M_GENERIC_CURRENT_PRODUCT_CLAIM = NOT_ACCEPTED
```

## HTML visualization status

The HTML is a visualization/reference artifact, not a cryptographic receipt.

It correctly displays the C1/HOLD boundary in several places, but it also contains presentation-only or incorrect values, including abbreviated/fabricated-looking digest strings, a displayed final-custody digest that is not the actual ZIP SHA-256, and a displayed package size of `12.4 MB` although the supplied final ZIP is 13,030 bytes.

It also visualizes run outputs and uncertainty tiers that have not been physically measured.

Therefore:

```text
HTML_AS_VISUAL_RESEARCH_ARTIFACT = ACCEPTED_WITH_CAVEATS
HTML_AS_CANONICAL_HASH_RECEIPT = NO
HTML_AS_EMPIRICAL_RESULT = NO
HTML_PUBLICATION_AS_VALIDATED_SCIENTIFIC_EVIDENCE = NO
```

## Final effect on the existing R8 adjudication

```text
R8_0_CUSTODY_HASH_FACTS = STRENGTHENED
PARTIAL_CHECKSUM_MANIFEST = ESTABLISHED
FULL_SEALED_MANIFEST = NOT_ESTABLISHED
R8_1_PROTOCOL_HOLD = UNCHANGED
R7_2_PHYSICAL_RASTER_HOLD = UNCHANGED
PIXEL_LEVEL = NOT_ESTABLISHED
NDVI = NOT_COMPUTED
NDVI_UNCERTAINTY = NOT_ESTABLISHED
REANA_EXECUTION = NOT_ESTABLISHED
PUBLICATION_OF_VALIDATED_C1_ADDENDUM = YES
RAW_HTML_OR_FINAL_ZIP_PROMOTION = NO
```
