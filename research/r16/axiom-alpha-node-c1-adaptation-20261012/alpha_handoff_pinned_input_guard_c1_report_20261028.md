# NEXUS OMEGA · AXIOM Alpha-Node · externally pinned census bytes V4 · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_PINNED_INPUT_GUARD_20261028_R0
DECISION=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=03fe4c62d3bb82c2ce28e36039d16ce6e086731d
PREDECESSOR_ISSUE93_RECEIPT=6469264130
FROZEN_EVALUATOR_FIRST_COMMIT=3eff12f0cdf6d2aac20092c8fb76d8f0f57cab42
CANDIDATE_SECOND_COMMIT=d90d29bbd139a28b921a40539757a34a63ee69f6
PUBLICATION_MAIN_AND_RECEIPT=PENDING_POSTMERGE_READBACK
```

## One selected contradiction and hypothesis

The immutable V3 census adapter accepts raw JSON census input without binding its physical bytes to an independently obtained SHA-256 pin. An in-transit edit to `automatic` or `receipt_readback` therefore changes the computed metric while the V3 process still exits successfully. The pre-existing `source_manifest_sha256` field is only shape-validated by V2; it does not authenticate the event bytes. This is not evidence of a real-world attack, and the original V3 explicitly states its caller-supplied trust boundary.

**Negative hypothesis:** If an attacker modifies an otherwise valid census payload after a trusted external SHA-256 pin has been established, V3 cannot detect the edit. The isolated V4 wrapper should reject any byte deviation before parsing or reporting a ratio. It must not convert a caller-supplied pin into GitHub authentication or a project-wide coverage claim.

## Source-exact predecessor and independent frozen oracle

- V2 `alpha_handoff_page_census_witness_v2_20261028.py`: 8,528 bytes; SHA-256 `c16806be3d00810b0e6d6ddeefc336c7428c9f6104c050c52815deb725cac8fd`; Git blob `e7882865407d2beb1b522182a86bf3351a7ef824`.
- V3 `alpha_handoff_readback_scope_adapter_v3_20261028.py`: 1,198 bytes; SHA-256 `6f93b45bbaa0f1e7debae7b45e6ea06f4f5a59ceecc9d4fa7b9d34180a84e476`; Git blob `35fea2e9d4b97eb14bb2dacbe1bf9ad17415688f`.
- New frozen subprocess evaluator `frozen_pinned_census_input_oracle_v4_20261028.py`: 4,710 bytes; SHA-256 `d34128355a0f1907935d2c5c259f4a84706e194b0db8ab492576de5313523838`; Git blob `65fc69d88060efa5418264b5145db94c2f4ce453`.
- New isolated V4 candidate `alpha_handoff_pinned_input_guard_v4_20261028.py`: 1,605 bytes; SHA-256 `e629233ecdfbf4fc0f808ed745387ec2d8dcb1d7db5132809bc863a8b5c582ec`; Git blob `538f20a3dc6a2c84ce17f6c914d7faa4ac9354a1`.

The evaluator was committed first to the owner branch, read back by immutable commit, and remained unchanged when the candidate was committed second. Tests ran in a temporary local workspace against independently rehashed copies of the pinned V2/V3 source; no productive code or GitHub security control was modified.

## Executed synthetic tests and falsifiers

| Measure | V3 baseline | Isolated V4 |
|---|---:|---:|
| Altered `automatic` / `receipt_readback` bytes detected with unchanged external pin | 0/2 | 2/2 |
| Frozen subprocess oracle | Not compatible with new pin contract | 14/14 PASS |
| Negative mutant removing digest comparison | N/A | 3 expected failures / 14 |
| Negative mutant promoting sample to project readback | N/A | 1 expected failure / 14 |
| Real eligible project handoff denominator | Unknown | Unknown |

Reproduction (synthetic, local): `python frozen_pinned_census_input_oracle_v4_20261028.py -v` from the existing R16 research directory, with V2 and V3 in the same directory. V4 requires `--expected-sha256` supplied independently of stdin; any absent, malformed or mismatched pin fails closed with exit 2. The oracle includes valid, partial, byte-tampered, missing-pin, invalid UTF-8, duplicate-key, nonfinite, oversized and wrong-repository cases.

**Decisive counterexample to a stronger claim:** an adversary able to alter both stdin and the CLI pin can recompute a matching SHA-256 and be accepted. Neither GitHub API origin nor completeness of `DECLARED_COMPLETE` is authenticated. `input_pin_source_authenticated=false`, `source_completeness_authenticated=false`, and project rates remain `NOT_COMPUTABLE`. This is a byte-binding prototype, not an authenticated census, a production integration, or third-party validation.

## Boundaries and decision

Only three additive files in the already existing R16 Alpha-Node research lane. The existing V2/V3, frozen older oracles, productive Steward, governance, repository order, R27-E actor registry, runtime, Hostinger, WWW, and C1 ceiling remain untouched. An owner-controlled PR/CI/merge, immutable main readback, and append-only Issue #93 receipt are separate publication gates. The 90% automation and 100% project readback targets remain unestablished.
