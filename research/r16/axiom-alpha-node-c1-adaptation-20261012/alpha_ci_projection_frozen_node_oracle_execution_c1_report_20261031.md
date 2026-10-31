# AXIOM Alpha-Node — independent frozen Node oracle execution for PR231 CI projection V2 (2026-10-31)

```text
OBJECT = NEXUS_OMEGA_ALPHA_CI_PROJECTION_FROZEN_NODE_ORACLE_EXECUTION_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_PREVIOUSLY_UNEXECUTED_ORACLE_NOW_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 8293dcb57080ec7490aed8893c06e42abb7b3b8c
PREDECESSOR_PR = 235
PREDECESSOR_ISSUE93_RECEIPT = 6540889490
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## One candidate and original-byte provenance

One candidate only: independently execute the already-frozen V1.2 Node subprocess evaluator against the already-published V1 classifier, V2 byte-pinned wrapper and the **real original** PR231 projection. This closes the specifically recorded `FROZEN_NODE_ORACLE=NOT_EXECUTED` gap in the predecessor report; no evaluator, source or candidate is modified. All four files were retrieved from immutable main `8293dcb57080ec7490aed8893c06e42abb7b3b8c` via the connected GitHub API, then reconstituted in an isolated, nonpersistent Linux test directory. Local byte length, SHA-256 and Git blob ID were independently recomputed and matched the previously published values:

| Original file (same existing R16 research lane) | Bytes | SHA-256 | Git blob |
| --- | ---: | --- | --- |
| `alpha_ci_pr_path_filter_projection_v1_20261031.json` | 8685 | `9aad5e271db570dc13b5ad2e7d8a3fbd9bc3db4de2e4b13b96390614dbf2c0fd` | `5da248602def62f7d34c926ccc21bf59ec944bcb` |
| `alpha_ci_pr_path_filter_audit_v1_20261031.js` | 3615 | `0cc5a0d332cfc524582da4a64525a9fecd5df8434756e3a8b4a1bf4cd952e645` | `7d0614759d472cb980809fbbce618556fb02531f` |
| `alpha_ci_projection_trusted_bytes_v2_20261031.js` | 1044 | `d3912d779510b4d04878cf1a98b9ce38ef9b478e3c1558a6ab5dd5b1b76ffda9` | `94c0673f558c060abb69f102d36d7cf54c33a961` |
| `frozen_alpha_ci_projection_integrity_oracle_v1_2_20261031.js` | 2695 | `307385cd3bd886e8aa400f49dec63eceb67652beb362968346bafd34ffbda279` | `ebfbad1c7871ccbbd1989078f50a7556b0fc25e2` |

The oracle's original pre-candidate commit is `57cbfbf298bba8612c7546fdbe837bd80908d2ea`; the V2 candidate was subsequently committed at `fac8252b1b65eadd5b26e7ddd9484ef427c819b7`. Earlier oracle V1/V1.1 preflight defects remain historically visible. This execution uses only frozen V1.2, without changing its expectations.

## Negative hypothesis, independent test and measured delta

H0: The previously reported V8-only success is not reproducible in an actual Node subprocess against the real 8,685-byte pinned source. Falsifier: the frozen V1.2 evaluator returns an assertion failure, a source-pin mismatch, a non-JSON child result, a nonzero process exit, or a different outcome for any negative fixture.

The exact command executed under Node.js `v22.16.0`:

```sh
node frozen_alpha_ci_projection_integrity_oracle_v1_2_20261031.js \
  alpha_ci_pr_path_filter_audit_v1_20261031.js \
  alpha_ci_projection_trusted_bytes_v2_20261031.js \
  alpha_ci_pr_path_filter_projection_v1_20261031.json
```

Process exit code: `0`. Exact stdout:

```json
{"oracle":"FROZEN_REAL_PROJECTION_BLACK_BOX_V1_2","tests":10,"baseline_pass":2,"tampered_same_length_rejected_by_v2":2,"malformed_rejected":2,"byte_variant_rejected_by_v2":1}
```

| Measure | V1 baseline | V2, frozen evaluator |
| --- | ---: | ---: |
| Original real projection accepted | 1/1 | 1/1 |
| Same-length source tamper rejected | 0/2 | 2/2 |
| Terminal LF removal rejected | 0/1 | 1/1 |
| Malformed JSON rejected | 1/1 | 1/1 |
| Independent frozen Node subprocess test outcomes | Previously NOT_EXECUTED | 10/10 PASS |

The evaluator is a separately frozen program spawning V1 and V2 as child processes. Its execution was performed by AXIOM in an isolated container; it is **not** an independent external expert or an independent trust root. No code change, GitHub workflow change, ruleset change, new agent stack, runtime integration, Hostinger deployment or WWW readback occurred.

## Decision and limits

The V2 byte-pinning improvement is now confirmed by the originally frozen real-source Node subprocess evaluator. The result is limited to the four original source files and the specified fixtures; it does not prove all YAML source semantics, branch-protection enforcement, independently authenticated GitHub transport, or scientific validity. A producer who controls the original pin can still mislead the pinning model. The existing published V1/V2/oracle bytes remain untouched; this report is append-only.

Automation goal status: the full authenticated census of **all** eligible routine public handoff attempts (including failures) is unavailable; `AUTOMATION_RATE=NOT_COMPUTABLE`. The full census of project-wide publications including failed or unreadable readbacks is also unavailable; `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. This iteration's new publication, if merged and verified, has a local denominator of 1; it must not be substituted for the project denominator. R10 PR #115 is still an owner-authored PUBLIC_SEND with no independently authenticated receiver ACK in the observed Issue #93/PR discussion; no biological experiment or scientific promotion is implied.
