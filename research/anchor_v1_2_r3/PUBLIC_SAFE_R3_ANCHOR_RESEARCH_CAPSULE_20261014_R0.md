# NEXUS OMEGA — Anchor Transport R3 Research Capsule (C1)

**Status:** `C1_DESCRIPTIVE_ONLY` · 14 October 2026 · informational research release, not a production security certification.

## Why this matters
External research agents often cannot inspect private repositories. Merely publishing SHA-256 hashes proves consistency **after** a recipient obtains bytes; it neither makes source available nor confirms the publisher's authority. NEXUS separates three operations: (1) public witness, (2) actual content delivery, (3) independent authorized execution. None implies another.

## Independently reported observations
- R3 independent expert review has confirmed publicly accessible, hash-matched research examples without private GitHub credentials. Distinguish each agent's source readback from actual test execution.
- Anchor V1.1 was reported to pass its original 25 security tests; additional adversarial research identified URL-host aliasing, signature representation, replay-state portability and filename/time normalization edge cases. These are engineering-review inputs; no claim of a real system compromise.
- A separate Anchor V1.2 research candidate has passed 16 targeted local security tests and 25 compatibility tests in an isolated sandbox. This confirms only the executed test set. It is **not** a live trusted download broker or a provisioned Operator signer.
- An available private Git channel can carry native binary packages to already-authorized recipients, while an anonymous external research lane must receive only separately reviewed public-safe source. A public hash does not substitute for delivery.

## Operational design principle
Prefer **one verified source envelope, one actual receiver ACK, one final aggregate evidence return**. Let noninterfering read-only checks progress independently when a specific high-risk operation is held. Do not deploy unfounded complexity (GPU infrastructure, extra paid clouds, mandatory cryptographic ceremonies) where existing private Git and public GitHub work.

## Boundaries
No original private R1 ZIP, credentials, raw private evidence, actual signing keys or operational IPs appear here. `PRIVATE_ENCRYPTED` remains unimplemented until a recipient-bound end-to-end test. Runtime Hostinger writes remain `FAIL_CLOSED`. No model output can promote beyond `C1_DESCRIPTIVE_ONLY`. Git branch publication does not mean a public website deployment or a Cursor task auto-start.

This capsule documents a falsification-oriented software transport research step, not a security guarantee or independently verified scientific result.
