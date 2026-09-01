# NEXUS OMEGA GitLab Integration — Standards/Comparator Register R0

Date: 2026-09-01
Claim ceiling: C1

## Selected comparators

### SLSA v1.2
Current approved SLSA specification. NEXUS adopts the separation between Source and Build tracks and uses provenance as verifiable information linking artifacts to source/build process. Target direction: Build L2/L3-compatible evidence where practical, without claiming a level until requirements are independently assessed.

### in-toto Attestation Framework
Use as the neutral envelope/model for software supply-chain claims. NEXUS receipts should remain convertible to structured attestations rather than being forge-specific prose only.

### Sigstore / Rekor
Comparator for identity-bound signing and append-only transparency. NEXUS may use Sigstore-compatible signing/transparency as an additional witness, never as a substitute for source-exact byte binding.

### Software Heritage / SWHID
Comparator for forge-independent intrinsic software identifiers and long-term archive referencing. NEXUS should compute/record SWHIDs only when the corresponding software object/snapshot is actually available and the identifier can be independently recomputed/resolved.

### Reproducible Builds
Gold-standard comparator for independent reproduction: same source, build environment and instructions should permit any party to recreate bit-for-bit identical specified artifacts. NEXUS distinguishes repeatability on one provider from reproducibility across independent providers.

### NIST SSDF SP 800-218
Security-process baseline for integrating secure development practices into the SDLC. Used as a control taxonomy, not as a certification claim.

### FAIR4RS + CodeMeta + RO-Crate
Research-software layer. FAIR4RS guides findability/accessibility/interoperability/reuse; CodeMeta provides interoperable software metadata; RO-Crate provides machine-readable packaging/provenance context for research artifacts.

## NEXUS synthesis

A scientifically stronger architecture than a one-way mirror is:

1. two independent forges;
2. provider-local CI on both;
3. SHA-256 cross-forge content reconciliation;
4. immutable append-only divergence receipts;
5. optional SLSA/in-toto attestations;
6. optional Sigstore/Rekor transparency;
7. Software Heritage archival/SWHID for public stable objects;
8. FAIR4RS/CodeMeta/RO-Crate metadata for research reuse;
9. independent replay before claim promotion.

## Anti-patterns

- Treating mirror success as independent validation.
- Using Git commit SHA alone as scientific content identity.
- Copying a GitHub CI status into GitLab as a GitLab validation result.
- Silently resolving divergence by force-push.
- Treating provider attestations as proof of scientific validity.
- Claiming SLSA, FAIR, reproducibility, or archival status without satisfying their actual requirements.
