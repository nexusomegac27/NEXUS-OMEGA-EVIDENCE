# Trace matrix

| Lane | Evidence | Verdict |
|------|----------|---------|
| Privacy | private ZIP preserved + redacted ADB | PASS_C1 |
| App L0–L3 | adapters+tests 18/18 | PARTIAL_PASS |
| STOP/deadline | existing gate tests | PASS |
| Build identity | APK hash+signer | PASS_READ_ONLY |
| WWW local | HTTP 200 file markers | PASS_LOCAL |
| Historical R21 | pkg+seg MATCH | PASS_PRIVATE |
| One-shot | filled packet | NOT_AUTHORIZED |
| Capture | — | NO |
| Install | — | NO |
| WWW live | — | NO |
