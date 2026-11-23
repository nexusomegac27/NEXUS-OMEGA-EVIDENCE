# R43-4 W1 P04 and E23 V3 privacy evidence split

**New P04 original captured pair**: user-supplied source ZIP `NEXUSO~1(5).ZIP` and nested 70866B `R43-3_P04_HTTP_SNAPSHOTS_20261123.zip`, 17/17 hash source matches including README, 2x4 decompressed entity bodies + 2x4 statusless header dumps. `current.json` feed snapshots have producer seq 4476 and 4477, run_utc 09:55:02Z and 10:00:03Z, source_changed=false, last_change_utc 2026-11-07T20:50:02Z, state.json same digest 93e24636dc980c16096c632630cf5ed3dd24eed8ea7857d1d7b0ed76cf245d81. The client's README claims rounds 328 seconds apart; available Date headers are 09:55:30Z and 10:00:54Z (324s), producer run times 301s apart. These are not necessarily contradictory: report individual clock domains and uncertainty; user-provided runner 200 status is not encoded in header files. `Content-Encoding: br` denotes on-wire compressed content; bodies appear already decoded. Clearly identify which bytes each hash binds.

**Read-only accepted URLs** (same four as W1 Issue #397):
https://www.nexus-mobile.de/bodytwin/
https://www.nexus-mobile.de/bodytwin/live/current.json
https://www.nexus-mobile.de/research/bodytwin/state.json
https://www.nexus-mobile.de/bodytwin/updates/

**Remaining acceptance**: (A) immutable copy of HTTP status-line or signed client runtime transport log, (B) request start/end/redirect/headers with raw body and entity decoding provenance, (C) two complete rounds >= actual cadence with measured clock errors, (D) **independent renderer** comparing HTML embedded STATUS/LIVE/MEMORY, state canonical hashes & browser projection, (E) distinct authenticated second observer/fetcher. A single reported 2x4 success with no independent browser does not close W1. Provenance source freshness vs feed generated_at/seq separate. Source unchanged not liveness failure.

**V3 privacy**: 241746B candidate ZIP SHA 07eed5ca1f5dfa5d76941fc83d321336cfc7adb0fd2c72d2e4ad18c65eaedf06, 45 members, 44/44 fresh manifest. Two control GitHub cookie-header files removed relative to V2. A regex/header-key scan found no remaining sensitive header names, but manual/contextual privacy, license and original challenge-trace review is NOT performed by an authorized operator. PUBLIC_PRIVACY_RELEASE stays HOLD. No V3 ZIP/public attachment or raw sensitive header values committed. Publication privacy gate and W1 scientific witness gate are independent noncompensatory acceptances.

**Other external W1 reports**: pinned edge 403 challenge body SHA 69eacef2... and unpinned timeout are legitimate vantage-specific observations. Mis-addressed root-path 404 is a historical request error, NOT proof canonical state/current endpoints were globally deleted. Never bypass CAPTCHA and never assert site down from one network path.
