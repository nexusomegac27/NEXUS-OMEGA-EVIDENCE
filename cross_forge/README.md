# NEXUS OMEGA Cross-Forge Domain

`cross_forge/` is the canonical control-plane domain for provider-independent repository replication, divergence detection, cross-forge reconciliation, and forge-local validation receipts.

## Scope

This domain may contain:

- cross-forge manifests and state records;
- append-only reconciliation/divergence receipts;
- provider/ref/commit bindings;
- content SHA-256 and byte-count bindings;
- provider-native Git object identifiers as provenance locators;
- CI/pipeline correlation records;
- cross-forge schemas and explicitly scoped control metadata.

It does **not** replace:

- `objects/` + `index/` for scientific evidence;
- `communication/` for communication provenance;
- `research/` for pre-integration research;
- `validation/` for ordinary single-repository validation artifacts.

## Invariants

```text
CLAIM_CEILING = C1
GITHUB_SUCCESS != GITLAB_SUCCESS
GITLAB_SUCCESS != GITHUB_SUCCESS
CROSS_FORGE_MATCH_REQUIRES_EXPLICIT_BINDING = YES
SOURCE_OBJECT_SUBSTITUTION = PROHIBITED
HISTORICAL_REWRITE = PROHIBITED
FORCE_PUSH_FOR_RECONCILIATION = PROHIBITED
BLOCKED_FORGE != BLOCKED_SYSTEM
```

Cross-forge state changes are append-only. A divergence is recorded and adjudicated; it is not silently erased by destructive synchronization.

## Current layout

```text
cross_forge/
├── README.md
├── manifest.json
└── receipts/
    └── ...
```

Provider-local CI must execute independently before a `CI_REPRODUCED` state can be asserted. Content equality alone is not scientific validation or claim promotion.
