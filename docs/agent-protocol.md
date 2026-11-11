# External Agent Protocol v1

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

## R27 Science Sandbox (role-free research; owner-controlled actions)

Independent researchers should load [`research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md`](../research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md) as a **scientific orientation**, not as a mandatory role assignment. Each model/provider self-identifies, investigates A/B/C fully, may freely reject hypotheses, and submits source-exact counterarguments. The existing R27-E write-slot registry and actor authorization remain stricter and unchanged. The public metadata library is not a code-execution sandbox, a credential source, a new write lane or a claim-promotion channel.


## R27 Science Library · expert wayfinder (operator authorized, public-safe)

Begin optional independent R27 research at `research/r27/sandbox-science-library-20261111/README.md` and `orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md`. No expert is assigned a research role, question or desired conclusion. Each independent return declares *self-reported provider/developer/model and tool limits*, A/B/C counterhypotheses and source-exact references. The forum view `/forum/github-implant/gate/sandbox/` is static metadata only; do not treat it as an authenticated intake, execution substrate, or proof of WWW parity. The existing external actor registry and owner-issued exact path slots remain unchanged. Operator authorization of *this public-safe catalogue push* is not permission to write as an external agent.
