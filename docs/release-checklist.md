# Immutable Evidence Release Checklist

1. Freeze the candidate commit and record its full commit SHA.
2. Run the repository test suite and every staging-manifest validation.
3. Scan every public byte for secrets, personal data, local paths, and third-party redistribution restrictions.
4. Confirm `CLAIM_CEILING=C1`, `promotion_authorized=false`, and `deployment_authorized=false`.
5. Create a versioned release tag without moving or replacing an earlier tag.
6. Upload the content-addressed artifact, its manifest, and the release checksum file.
7. Publish the GitHub release as immutable; verify the release and each asset independently.
8. Create at least one independent archival witness through Zenodo or Software Heritage.
9. Publish a new manifest version containing the verified release coordinates and independent witness.
10. Never rewrite an earlier public object; corrections use a new identity and explicit provenance.

Release, signature, attestation, DOI, SWHID, and model agreement prove neither authorship nor scientific truth. They establish only the explicitly verified provenance and byte identity.
