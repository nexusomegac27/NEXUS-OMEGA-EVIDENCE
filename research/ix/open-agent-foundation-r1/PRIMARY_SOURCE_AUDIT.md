# Primary-source audit — open-agent foundation R1

Audit date: 2026-09-20.

This document records upstream evidence for candidate discovery. An upstream project's own claims
about performance/security are not adopted as NEXUS validation.

## Protocol interoperability

### Model Context Protocol (MCP)

Upstream specification describes MCP as an open protocol for connecting LLM applications to external
data sources and tools.

- Specification: https://modelcontextprotocol.io/
- Repository: https://github.com/modelcontextprotocol/modelcontextprotocol

R1 status: `PRIMARY_SOURCE_CHECKED_CANDIDATE`.

### Agent2Agent (A2A)

The Linux Foundation-hosted A2A project describes an open protocol for interoperability between
independent agent systems and distinguishes it from MCP. The protocol is Apache-2.0 licensed.

- Repository: https://github.com/a2aproject/A2A
- Specification: https://a2a-protocol.org/

R1 status: `PRIMARY_SOURCE_CHECKED_CANDIDATE`.

## Open-weight model candidates

### Qwen3

The Qwen3 upstream repository states that its open-weight models are Apache-2.0 licensed and
documents use through multiple local/open runtimes.

- https://github.com/QwenLM/Qwen3

R1 status: `PRIMARY_SOURCE_CHECKED_CANDIDATE`.

### IBM Granite 4.2

IBM's current Granite 4.2 model documentation/repository states Apache-2.0 licensing for the
language-model family.

- https://github.com/ibm-granite/granite-4.2-language-models
- https://www.ibm.com/granite/docs/models/granite4-2

R1 status: `PRIMARY_SOURCE_CHECKED_CANDIDATE`.

Exact model revision and model-card terms must still be frozen per experiment.

## Runtime and agent-library candidates

- Hugging Face smolagents — Apache-2.0:
  https://github.com/huggingface/smolagents
- vLLM — Apache-2.0 project metadata:
  https://github.com/vllm-project/vllm
- Firecracker — Apache-2.0:
  https://github.com/firecracker-microvm/firecracker
- Temporal server — MIT:
  https://github.com/temporalio/temporal
- NATS server — Apache-2.0:
  https://github.com/nats-io/nats-server
- Open Policy Agent — Apache-2.0:
  https://github.com/open-policy-agent/opa
- OpenBao — MPL-2.0:
  https://github.com/openbao/openbao
- OpenTelemetry Collector — Apache-2.0:
  https://github.com/open-telemetry/opentelemetry-collector
- in-toto:
  https://github.com/in-toto/in-toto
- Sigstore/cosign:
  https://docs.sigstore.dev/cosign/

R1 status for all: candidate only; no NEXUS activation or security assertion.

## Local canonical-data candidates

### SQLite

SQLite upstream states that its core deliverable code/documentation are dedicated to the public
domain.

- https://www.sqlite.org/copyright.html

### DuckDB

DuckDB documentation states the project is MIT-licensed and its core IP is held by the DuckDB
Foundation.

- https://duckdb.org/
- https://github.com/duckdb/duckdb

R1 use: research candidates for portable local metadata/analytical indexing. Canonical evidence
must remain independently reconstructable from content-addressed objects.

## Open scientific / federated resources

### SatNOGS

Libre Space Foundation describes SatNOGS as a global open-source satellite ground-station network.
Its project page lists software under AGPL/GPL-family licensing, hardware under CERN Open Hardware
License and observations/content under CC BY-SA terms. The network states that observations are
public.

- https://www.libre.space/projects/satnogs/
- https://network.satnogs.org/about/

Classification:

```text
OPEN_GROUND_SEGMENT / OPEN_OBSERVATION_RESOURCE
!= FREE_GENERAL_SATELLITE_COMPUTE
```

### CERN Open Data Portal

CERN states that the portal publishes research data together with software/documentation,
uses open licenses and assigns DOIs; the portal terms state metadata/datasets are CC0 while other
content follows its own indicated license.

- https://opendata.cern.ch/
- https://opendata.cern.ch/docs/terms-of-use

Classification: `OPEN_DATA_RESOURCE_ONLY`.

## Candidate-selection law

No upstream license or popularity claim establishes suitability:

```text
OPEN_LICENSE
!= SECURITY_VALIDATION
!= SCIENTIFIC_VALIDITY
!= NEXUS_SELECTION
```

R2 must physically pin and test any component before it can move beyond candidate state.
