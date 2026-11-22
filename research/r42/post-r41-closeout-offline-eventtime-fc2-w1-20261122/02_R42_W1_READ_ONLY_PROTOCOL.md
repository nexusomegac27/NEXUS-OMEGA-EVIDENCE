# R42 Public BodyTwin witness · frozen read-only contract

URLs:
- https://www.nexus-mobile.de/bodytwin/
- https://www.nexus-mobile.de/bodytwin/live/current.json
- https://www.nexus-mobile.de/research/bodytwin/state.json
- https://www.nexus-mobile.de/bodytwin/updates/

Require two temporally separated raw HTTP reads with status, headers, response body SHA256, body length, ETag, Age, Date, cache directives, MIME, source last-changed, feed generated-at, reducer sequence, Browser DOM/render/embedded SHA comparison. External source updated != producer ticking. A processed text response cannot be called RAW_HTTP_WITNESS. Failed network read is NOT_VERIFIED, never site outage.

Past Cursor-reported STATUS raw hash b49d28a6... differed from embedded d1100955..., LIVE 60674103... and MEMORY 4ccc495e... matched at a historical snapshot. Source last changed was reported 2026-11-07T20:50:02Z; later feed ticks are not new science. E17–E20/W1 report observed a seemingly stale processed text-view, but no actual CDN vs client-layer root cause is proven. Keep STATUS_DIFFERENCE_OPEN, investigation scoped to the existing Issue #397. BodyTwin validation NO, consent OPEN, no new capture, no deploy, no merge, C1 only.
