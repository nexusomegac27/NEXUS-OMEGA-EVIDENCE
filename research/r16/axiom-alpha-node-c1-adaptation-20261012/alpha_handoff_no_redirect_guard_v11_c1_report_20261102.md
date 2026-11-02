# NEXUS OMEGA · Alpha-Node · HTTP redirect preflight guard V11 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_GITHUB_API_NO_REDIRECT_GUARD_V11_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_LOOPBACK_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=b7f966a886c88e015ac49f32efdf4bf7e31f1fea
PREDECESSOR_PR=282
PREDECESSOR_ISSUE93_RECEIPT=6567269097
FROZEN_EVALUATOR_FIRST_COMMIT=c0f7685377547e3ca9879df23e73d007a8b61f56
CANDIDATE_SECOND_COMMIT=d0cc1b7a79b8ee8e9248f46e47e9a5ffa83cc510
PRODUCTION_INTEGRATION=NO
LIVE_GITHUB_HTTPS_E2E=NOT_EXECUTED
```

## OBSERVE / ORIGINAL_BYTES / PINNED_BASELINE

GitHub main was independently resolved to `b7f966a886c88e015ac49f32efdf4bf7e31f1fea`, immediately following `4e22d346006b67de332bfeb1f0ea68db8412fd70` (PR #282). The original V10 source was fetched by immutable commit and independently reconstructed: `alpha_handoff_github_api_source_guard_v10_20261102.py`, 6,327 bytes, SHA-256 `4ba4e969cf0d8643915185bf5f05ca4ae93acde01854ba7ebc170683dc8ca39a`, Git blob `906614086b2e014e198b2324fe26669cc425607a`. This original is preserved unchanged.

V10 uses `urllib.request.urlopen(req)` and tests `fp.geturl() == url` **after** the HTTP request. Python's standard redirect handler can follow a 302 and perform a second GET before the final-URL check rejects the result. This is a transport-side-effect gap, not evidence of a GitHub server redirect or an actual data exfiltration incident.

## NEGATIVE HYPOTHESIS / ONE CANDIDATE

An unexpected 302 can trigger an outbound second-hop request despite V10's eventual fail-closed result. V11 retains V10's source-byte, commit, path, size, SHA-256, Git-blob and C1 semantics, but builds an opener with `NoRedirect(HTTPRedirectHandler)` returning `None` from `redirect_request`. The 30x is rejected before following the `Location` URL. No user-provided host, secrets, credentials, new worker, runtime change, branch-ruleset mutation or historical rewrite.

The test's synthetic local server returns `302 Location: http://127.0.0.1:<port>/sink`. The frozen evaluator instruments `/sink` and exercises the original and candidate API-readback paths using a local transport adapter. The candidate is an **isolated research scaffold**, not a production API security guarantee.

## FROZEN EVALUATOR / INDEPENDENT TEST

The independent evaluator was committed **before** V11 at `c0f7685377547e3ca9879df23e73d007a8b61f56`: `frozen_alpha_handoff_no_redirect_evaluator_v11_20261102.py`, 7,623 bytes, SHA-256 `14fa9cc6bd8af062e98ce430a290cca7ecb15dd701350976a7737620f0f2c007`, Git blob `304e5d762f931242c841d637f3af72bada17d9fd`. The evaluator was not modified after V11 creation. V11 candidate second commit `d0cc1b7a79b8ee8e9248f46e47e9a5ffa83cc510`: `alpha_handoff_github_api_no_redirect_guard_v11_20261102.py`, 6,651 bytes, SHA-256 `e3586c63265ec4c613341329924ebe0965d6d76c2b358e5de6532900d524384e`, Git blob `17e80fabd6febe21bdd181d15bbe44ce13dfbfd9`. Both blob identities were independently read back from GitHub and matched local originals.

Reproduce from the same directory:

```sh
python frozen_alpha_handoff_no_redirect_evaluator_v11_20261102.py alpha_handoff_github_api_no_redirect_guard_v11_20261102.py alpha_handoff_github_api_source_guard_v10_20261102.py
python -m py_compile alpha_handoff_github_api_no_redirect_guard_v11_20261102.py frozen_alpha_handoff_no_redirect_evaluator_v11_20261102.py
```

The original V10 file must be retrieved from immutable main `b7f966a886c88e015ac49f32efdf4bf7e31f1fea` for reproduction; do not rewrite it. **Observed local loopback result: 9/9 expected tests PASS**, stdout 1,009 bytes, SHA-256 `6b4b741f7db658f8739934cb01e3ede9137ae591d7b641e7bc9a80ac4dda3bef`.

| Measurable outcome | V10 | V11 |
|---|---:|---:|
| Unexpected 302: local `/sink` second-hop GET | 1/1 observed | **0/1** |
| Redirect eventually rejected | Yes, after follow | **Yes, before follow** |
| Candidate independent local evaluator | Baseline replay | **9/9 PASS** |
| Unchanged positive source-byte check | Existing | **PASS in local mocked API** |
| Live GitHub HTTPS end-to-end | NOT_EXECUTED | **NOT_EXECUTED** |

## FALSIFIER / DECISION / BOUNDARIES

A deliberately injected opener can return forged 200 JSON while falsely reporting the original URL; V11's unchanged `check` accepts a co-consistent envelope and returns `LIVE_API_BOUND_C1_BYTES_ONLY`. This is a **mocked transport falsifier**, not a real HTTPS response. Therefore V11 does not authenticate a transport controlled by an attacker, the source actor, event-census completeness, scientific correctness, or a project-wide 90% automation claim. The actual HTTPS path remains untested because local DNS/network access was unavailable. The local HTTP server is loopback-only and no external host was contacted.

Project-wide eligible Handoff denominator and complete publication denominator remain `NOT_COMPUTABLE`; the nine tests are not real handoffs. This run creates at most one isolated candidate, no new pipeline root, no external actor registration, no R10 expert claim, no Cursor/Hostinger/WWW write and no claim promotion. GitHub PR/CI and immutable main readback are required before marking `MAIN_PUBLISHED`; until then this report is a C1 tested candidate only.
