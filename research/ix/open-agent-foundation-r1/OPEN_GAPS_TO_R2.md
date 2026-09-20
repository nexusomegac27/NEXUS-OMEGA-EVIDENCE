# Open gaps carried from IX R1 to R2

R1 publishes architecture and candidate evidence only. It intentionally leaves execution off.

## Required R2 questions

1. Can the same canonical work unit resume after swapping model + inference runtime?
2. Can the Fundus and evidence state be reconstructed without chat history?
3. Which minimum state store is sufficient: content-addressed files + SQLite, DuckDB, or another
   open implementation?
4. Does adding a framework materially improve recovery/auditability, or only complexity?
5. Can MCP and A2A boundaries be adopted without making either a continuity dependency?
6. Can retrieval/vector indexes be destroyed and deterministically rebuilt from canonical objects?
7. How is workload identity preserved across LOCAL/FEDERATED/AUGMENTED modes?
8. Can policy deny one tool/capability while unrelated work continues?
9. Can a quota/runtime failure be resumed with zero loss of scientifically validated state?
10. Can Evidence-Delta detect repeated agent prose that introduces no new evidence?
11. What exact open-weight models fit the available local hardware envelope?
12. What resource adapters are lawful/reproducible for SatNOGS, CERN Open Data and other open
    scientific resources?

## Mandatory R2 controls

```text
NO_ACTIVATION_FROM_R1
NO_PRODUCTION_CLAIM
NO_PROVIDER_RANKING
NO_MODEL_RANKING
NO_SINGLE_GLOBAL_OPENNESS_SCORE
NO_CANON_IN_VECTOR_DATABASE
NO_SECRET_IN_PUBLIC_REPO
NO_EXTERNAL_RESOURCE_BECOMES_AUTHORITY
```

## R2 success condition

R2 succeeds only if it produces reproducible evidence about replaceability, continuity and
recovery. Merely assembling an open-source stack is not sufficient.
