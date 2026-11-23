# R42-R2 · Source/Privacy/W1 integrity constraints

Parent W1 issue: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/397
Parent implementation: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/400
Expert research: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/402

The E23 ZIP has real browser/cookie artifacts and 403 challenge bytes. Keep the original private, quarantined and access-controlled. Do NOT commit session cookies, reCAPTCHA data, unredacted raw headers, original sensor records, identifiers, internal CAS values, or auth tokens to this public repo. This PR stores only provenance hashes, findings and safe control descriptions.

Independent public W1 200-body witness is NOT established by TCP connectivity or 403 challenge. Hostinger CDN browser checks may block a fresh automated vantage without proving the application is down. Do not try automated CAPTCHA bypass. Legitimate choices: user-approved public challenge-free read-only mirror with public-safety review, operator-provided pinned snapshots with independent off-host rehash, or browser human-authorized witness. All are PROPOSALS only; no implementation/publication on this issue.

Use two or more snapshots spaced by at least the actual feed cadence when testing tick liveness. Preserve source_changed/source_updated_at distinct from generated_at/reducer seq, and compare raw source bytes + HTML embedded + browser-render projection. Diagnose STATUS≠EMBEDDED only when actual bytes & canonicalization version present. A 304 response requires a validated cached 200 body. Fail reading as NOT_VERIFIED, not SITE_DOWN.

R43 preparation is frozen until new Cursor R42 application implementation return arrives, AXIOM rehashes/verifies its source and tests, and the Operator's hard governance floors remain unchanged.
