# AXIOM Alpha-Node — raw GitHub REST Issue #93 comment census · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_RAW_REST_COMMENT_CENSUS_V1_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = f17196d26faa03650709601f8fecea6c50cc657d  
PREDECESSOR_PR = 244  
PREDECESSOR_ISSUE93_RECEIPT = 6546155375  
FROZEN_ORACLE_FIRST_COMMIT = e487703a46e539c9dd912c72dcb9be6d164ab035  
CANDIDATE_SECOND_COMMIT = 88cb80d31cb8e918e5970cde814e87555d91f495  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Observed source and negative hypothesis

The normalized GitHub connector issue-comment read returned 234 comments but exposed `created_at=null` and `updated_at=null`. Thus that projection alone could not distinguish an edited comment from an unedited one. Negative hypothesis: the raw REST representation contains missing/changed timestamps or omitted pages. Read-only GitHub REST GETs resolved the first gap, without changing the original comments. The GitHub issue metadata declared `comments=234`. Three explicitly paginated REST GETs returned 100+100+34 = **234** comments; all 234 carried timestamps and owner login `nexusomegac27`, all had `created_at == updated_at`, and IDs were strictly increasing. This supports **no edits visible in current GitHub timestamp metadata**, NOT proof that historical content can never be changed or that the GitHub API is independently authenticated.

Raw REST endpoints, fetched on 2026-10-31:
- `GET https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93` (issue count 234)
- `GET https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93/comments?per_page=100&page=1` — 617407 UTF-8 bytes; SHA-256 `62b16817504a91761185d17fd7568e83cbc931cac9d5cbc7b789714e706e00d3`; 100 comments
- `GET https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93/comments?per_page=100&page=2` — 696476 bytes; SHA-256 `75064a2273bb1521b85966c4176e69b076d959d51237e9360c28290600319c96`; 100 comments
- `GET https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93/comments?per_page=100&page=3` — 222400 bytes; SHA-256 `9e025cda7f69e4a9b4ca5329f55f63af070e27d40a16ed520600599bc1f46391`; 34 comments

Body inventory fingerprint: concatenate for each ascending comment ID the ASCII line `<id>:<sha256(UTF-8 body)>\n`; SHA-256 of 17784-byte concatenation = `1517f7b117da884d055213eb17d203f64f5de53210b40cec0287687d627a1ea5`. First ID 6111816879; last ID 6546155375. Hash implementation independently checked against standard `abc` and empty-string SHA-256 vectors. The original full REST page responses were read and hashed in the connected-tool execution, **not committed as byte archives**; future comparisons must re-fetch and not treat this report as archived source bytes.

## Isolated candidate and frozen oracle

The additive Python candidate consumes a caller-supplied raw REST projection, checks page order and 100-item pagination, count against independently fetched issue metadata, unique ascending IDs, actor labels, timestamps, edited-comment evidence, and a body inventory fingerprint. It makes no network calls and does not authenticate its input. Its status is fail-closed for missing timestamps, pagination gaps, duplicate IDs, nonfinite JSON and malformed content. A non-owner comment is counted, never promoted into an independent expert ACK.

A separate Python black-box subprocess evaluator was versioned FIRST and never modified after candidate creation. Local Python 3 execution: **14/14 expected outcomes**, exit 0, including positive scope, edited timestamp, missing count, duplicate ID, missing timestamp, time reversal, missing actor, nonowner, altered body digest, duplicate JSON keys, nonfinite JSON, missing body, and no claim promotion. The technical evaluator is separate from the candidate, but not external third-party validation. A falsifier is an edited comment or missing page accepted as clean, or a modified body producing the same inventory digest.

- Frozen oracle: 3161 UTF-8 bytes, SHA-256 `954dd258b0d2e20fcc7efd23a0e2cde9ae7d588b7dd9675ad50fbd361cc538ba`, Git blob `29d8a20fde6f339dcdb799d887ac01aa39967d25`.
- Candidate: 3548 UTF-8 bytes, SHA-256 `e347d5ea9ac4977c826cb433cf02af10452ef1398b3258e933a78bd852d6932b`, Git blob `427150ce5499f603e1832c135314b137b1a85b8b`.

## Scope, limits and decision

This is a new measurable **source-metadata coverage and edit-detection scaffold**, not proof of an operational rate increase. Baseline normalized timestamp coverage 0/234; raw REST coverage 234/234; observed edited timestamp count 0/234; nonowner comment count 0/234. These figures are bounded to Issue #93 at the stated retrieval. An actor label from GitHub is not a scientific expert ACK. The independent evaluator tested synthetic fixtures; the full 234-comment real payload was checked with a separately implemented source inspection, not executed through the Python candidate. Future edits and concurrent new comments can change the page count/fingerprint; require a new pinned readback.

Project handoff automation and publication full-readback denominators remain `NOT_COMPUTABLE`; 234 comments are NOT that denominator. R10 PR #115 remains OPEN and no independently authenticated expert receiver ACK was observed. No production integration, new automation/worker, GitHub policy change, external actor registration, R10 merge, Cursor dispatch, Hostinger/WWW write or claim promotion. Historical receipts remain untouched.
