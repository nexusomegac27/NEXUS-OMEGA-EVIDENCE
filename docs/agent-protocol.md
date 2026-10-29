# External Agent Protocol v1

## Mandatory expert codex bootstrap (2026-10-29, draft enactment)

Before the `Consume` sequence for each new AXIOM-authored GitHub-enabled expert mandate, retrieve the [NEXUS Expertenkodex V1](governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md) from full commit `b17d38266777bad61178e608d09e41726b9f4769`, path `docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md`, exact 15388 bytes, SHA-256 `adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab`. Independently rehash; if missing/mismatch, mark `SOURCE_GAP_BLOCKED`. Follow the operator-directed [GitHub-only data law](governance/NEXUS_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_V2.md): the Operator delivers pure order text only and transfers no source files. External returns require registered principal, preallocated slot, GitHub fetch/return and independent ACK. No unregistered write authorization is inferred. This draft text is not yet a required CI rule or proof of real external adapter activation.

## Consume

1. Fetch `index/v1/latest.json` from the public repository or Pages view.
2. Fetch the referenced manifest from the immutable release or content-addressed path.
3. Reject duplicate JSON keys; canonicalize according to RFC 8785 where applicable.
4. Verify the asset byte count and SHA-256.
5. Verify every declared semantic scope separately.
6. Verify the GitHub immutable release and release asset.
7. Verify at least one independent witness: Zenodo DOI or Software Heritage SWHID.
8. Preserve every caveat and the C1 claim ceiling.
9. Begin semantic work only after the preceding checks pass.

## Return

Publish a separate content-addressed result and return only:

```text
RETURN_MANIFEST_URL
RETURN_MANIFEST_SHA256
RETURN_ASSET_SHA256
RETURN_ANCHOR_LEVEL
```

Chat content is never a substitute for externally retrieved bytes.

## Failure

Missing or divergent bytes are reported as `SOURCE_NOT_PRESENT`, `NOT_COMPUTABLE`, or `FAIL_CLOSED` as appropriate. Never reconstruct missing evidence from conversation order.

## R27-E canonical GitHub return lane (stricter prospective rule)

For R27-E and later assignments, external agents MUST read the owner-controlled [structural firewall](governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md) and [write slot registry](governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json) before creating any file or PR. No new structure, no top-level directories, no personal return folders, no modifications of existing return files. The current R27-E slot is preallocated under `research/r27/www-extern-wake-isolation-20261011/returns/`. Direct write requires a separately verified/registered GitHub actor, seven exact create-only files, detached manifest and independent AXIOM readback. If GitHub write capability or owner-issued slot is missing, research may still be delivered out-of-band for a **clearly labeled AXIOM bridge intake**, never as an invented direct GitHub SEND. Older public return schemas remain historical; new R27-E return manifest contract is `schema/external-agent-return-r27e-v1.schema.json` and does not promote any historical C1 claim.
