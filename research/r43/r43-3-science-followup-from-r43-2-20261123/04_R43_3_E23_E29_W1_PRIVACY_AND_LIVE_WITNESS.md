# R43-3 E29 · Public V2 reseal and W1 witness privacy/causal split

## A. Verified archive integrity, no premature public safe claim
Actual operator uploaded E23_W1~1(2).ZIP 246311 bytes SHA256 c5b6ced5c8ef36713f58200635dcc77269cfe1d630d35117ddb2784925b4751d, ZIP CRC PASS, 47 members. New SHA256SUMS_SEALED.txt sha 764c25635424644ea6ed9f53a5c207bec009eee91e6f363bffe7028831bdc07b has **46 paths matching 46/46**, exactly 45 old retained plus REDACTION_NOTICE.md. Old 48-line manifest is absent; three sensitive browser-cookie/CAPTCHA artifacts are absent. Old public V1 248727 bytes 87b0f829... is superseded. This closes R43-2 REDACTED_DERIVATIVE_MANIFEST_INTEGRITY_ONLY.

Independent conservative content pattern inspection found Cookie/Set-Cookie-like header lines inside:
- snapshot_1/CTRL_GITHUB.headers
- snapshot_2/CTRL_GITHUB.headers

The finding does not establish leaked credentials; but contents have not passed an authorized privacy/reidentification review, and the files may contain volatile session fields or third-party trackers. **NO PUBLIC RELEASE BY AXIOM**. A responsible clearance must enumerate all header keys/values in private, tokenize or remove secret-bearing lines where needed, re-seal with fresh SHA256SUMS, document differential to V2, scan all .json, .headers, body files and challenge/debug material. The included REDACTION_NOTICE.md quotes hashes of excluded private objects; assess whether even these hashes are public-safe under the project privacy policy. Do not use a pattern-scan negative as a guarantee of no PII.

## B. Public W1 endpoint witness — source ≠ challenge
Four URLs only:
1. https://www.nexus-mobile.de/bodytwin/
2. https://www.nexus-mobile.de/bodytwin/live/current.json
3. https://www.nexus-mobile.de/research/bodytwin/state.json
4. https://www.nexus-mobile.de/bodytwin/updates/

Report classes observed from different public observer paths on Nov 23: 200 with self-hosted C1 source data (text-level, no full independent header/body witness); 403 hcdn JS challenge (5768B body hash 69eacef2f355c22ff53745adb39ff0076d2093a767a72e38070ca83c7c5569df); HTTP 000/TCP timeout; and 131-byte HTTP 404-looking page. An independent later observer saw 200 state/current again. These are distinct time/vantage observations, not proofs that state backend changed or site was down. Do not equate response body 403 with scientific source body. No automated CAPTCHA solving. Do not pin a CDN address without a lawful diagnostic mandate and documented Host/Vantage controls.

Required W1 evidence to close: two complete 4-URL snapshots with actual application HTTP200 body+exact SHA256, headers Date/Age/ETag/Last-Modified/Cache-Control/Vary/Redirect/MIME, observer clock/scheme/host and client transport, separated by at least declared producer cadence >=300s plus clock/timing uncertainty. Anchor valid 304 with cached 200. Compare source_updated_at vs generated_at vs reducer seq separately, STATUS/LIVE/MEMORY HTML embedded canonical hashes and browser rendered values. If blocked, classify status only (403 challenge, 404 body, timeout) and keep W1_SECOND_PARTY_RAW_WITNESS=OPEN. A challenge-free public-safe read-only mirror may be proposed for operator review, not deployed in this research phase.

## C. Privacy authority is separate from hash integrity
Archive seal proves byte stability, not consent/publication rights; root website reachability proves transport not semantic truth. E29 must supply private review receipt with reviewer authority and an independent privacy scan, and separate scientific W1 source witness, neither compensating for the other. No new monitor, no live source update, no Hostinger or WWW write.
