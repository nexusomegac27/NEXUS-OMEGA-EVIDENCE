# R2 open-source discovery queue — IX R1 supplement

```text
OBJECT = NEXUS_OMEGA_AXIOM_IX_R1_OPEN_SOURCE_DISCOVERY_SUPPLEMENT_20260920_R0
STATE = PUBLIC_RESEARCH_CANDIDATES_NOT_SELECTED
IX_EXECUTION = NOT_STARTED
ACTIVATION = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
```

This supplement records additional upstream-checked components for R2 falsification. It does not
extend the canonical agent body and does not select a framework.

## Additional framework candidates

### Microsoft AutoGen

The official repository states that AutoGen remains open source under MIT. Its current FAQ also
records a package-chain caveat: the maintainers do not control the historical `pyautogen` package
release path and have moved toward a multi-package design.

- https://github.com/microsoft/autogen

```text
CLASS = OPTIONAL_FRAMEWORK_ADAPTER
LICENSE_UPSTREAM = MIT
CAVEAT = PIN_OFFICIAL_REPO_AND_CURRENT_PACKAGE_NAMES
SELECTED = NO
```

### OpenHands

The current OpenHands repository carries an MIT license. It is relevant as a coding-agent/runtime
candidate, not as NEXUS identity.

- https://github.com/OpenHands/OpenHands

```text
CLASS = OPTIONAL_CODING_AGENT_ADAPTER
LICENSE_UPSTREAM = MIT
SELECTED = NO
```

### LangGraph

The open-source LangGraph core package declares MIT licensing. This must be separated from
LangGraph Platform/server features: historical/current self-hosting and custom-auth surfaces can
have managed/enterprise licensing requirements. R2 must therefore test **core library** and
**platform/service** as different objects.

- https://github.com/langchain-ai/langgraph

```text
LANGGRAPH_CORE = OPEN_SOURCE_CANDIDATE
LANGGRAPH_PLATFORM = SEPARATE_LICENSE_AND_SERVICE_SURFACE
SELECTED = NO
```

This distinction is a concrete example of:

```text
OPEN_LIBRARY != OPEN_PLATFORM
```

## Retrieval-index candidates

### Qdrant

The upstream repository is Apache-2.0 licensed.

- https://github.com/qdrant/qdrant

### pgvector

The upstream extension uses the PostgreSQL license and provides vector similarity search inside
PostgreSQL.

- https://github.com/pgvector/pgvector

Both are classified only as **rebuildable retrieval accelerators**:

```text
VECTOR_INDEX != CANONICAL_MEMORY
VECTOR_INDEX_LOSS != CANON_LOSS
VECTOR_INDEX_MUST_BE_REBUILDABLE_FROM_CANONICAL_OBJECTS
```

## R2 comparison rule

Framework/runtime experiments must compare at least:

```text
STATE_PORTABILITY
RECOVERY_AFTER_TERMINATION
CANONICAL_HEAD_PRESERVATION
PROVENANCE_COMPLETENESS
TOOL_BOUNDARY
POLICY_BOUNDARY
EVIDENCE_DELTA
LOOP_RESISTANCE
UNAUTHORIZED_ACTION_RATE
DEPENDENCY_FOOTPRINT
LICENSE/OPENNESS_VECTOR
```

No “best framework” result may be produced from feature count, popularity, stars or provider brand.

## Queue status

```text
AUTOGEN = CANDIDATE
OPENHANDS = CANDIDATE
LANGGRAPH_CORE = CANDIDATE_WITH_PLATFORM_SEPARATION
QDRANT = OPTIONAL_REBUILDABLE_INDEX_CANDIDATE
PGVECTOR = OPTIONAL_REBUILDABLE_INDEX_CANDIDATE

INSTALLATION = NO
EXECUTION = NO
ACTIVATION = NO
```
