# Open-source / open-resource candidate matrix — R1

Checked against upstream/primary project sources on 2026-09-20. This is a discovery and licensing
matrix, **not a ranking or stack selection**.

| Layer | Candidate | Upstream openness | R1 role | Selection state |
|---|---|---|---|---|
| Tool protocol | Model Context Protocol (MCP) | Open protocol; upstream repository/spec | tool/context interoperability | candidate |
| Agent protocol | Agent2Agent (A2A) | Linux Foundation; Apache-2.0 | agent-to-agent interoperability | candidate |
| Open-weight model | Qwen3 | open-weight models Apache-2.0 | replaceable reasoning engine | candidate |
| Open-weight model | IBM Granite 4.2 | Apache-2.0 | replaceable reasoning engine | candidate |
| Agent library | Hugging Face smolagents | Apache-2.0 | thin framework adapter experiment | candidate |
| Local inference | llama.cpp | permissive open-source implementation | local inference adapter | candidate |
| Inference server | vLLM | Apache-2.0 | high-throughput inference adapter | candidate |
| Local API runtime | LocalAI | open-source local inference project | compatibility/runtime adapter | candidate; exact release/license to pin |
| Embedded state | SQLite | public-domain core | canonical/local metadata index | strong research candidate |
| Analytical state | DuckDB | MIT | local analytical/event queries | strong research candidate |
| Durable execution | Temporal | MIT | optional resumable workflow engine | optional accelerator |
| Messaging | NATS Server | Apache-2.0 | optional event/message transport | optional accelerator |
| Workload identity | SPIFFE/SPIRE | open-source ecosystem | machine/workload identity | candidate |
| Policy | Open Policy Agent | Apache-2.0 | declarative authorization/policy | candidate |
| Secrets | OpenBao | MPL-2.0 | distributed secret management | optional candidate |
| Isolation | Firecracker | Apache-2.0 | Linux microVM sandbox | optional candidate |
| Supply-chain provenance | in-toto | open-source framework | command/file chain evidence | candidate |
| Artifact signing | Sigstore/cosign ecosystem | open-source project | signatures/transparency receipts | candidate |
| Observability | OpenTelemetry Collector | Apache-2.0 | non-authoritative telemetry | candidate |
| Satellite observations | SatNOGS | open software/hardware/data under project-specific copyleft/CC licenses | federated open observation resource | resource only |
| Scientific datasets | CERN Open Data | open data portal with per-content licenses/DOIs | public scientific corpus | resource only |

## Interpretation

“Candidate” means only that an upstream project has a sufficiently open and inspectable surface to
justify a later experiment. It does not mean:

```text
SECURE
SCIENTIFICALLY_VALIDATED
FIT_FOR_NEXUS
PRODUCTION_READY
SELECTED
```

Every R2 experiment must bind the exact version, commit/model revision, license file, build/runtime
environment and relevant upstream terms.

## Framework neutrality

The supplied R1 research report suggested specific frameworks as preferred choices. That preference
is not promoted here. Frameworks are intentionally below the continuity boundary: the experiment
should demonstrate that replacing a framework does not replace NEXUS identity.

## Open-resource neutrality

A resource being free of charge or publicly reachable does not make it open infrastructure.
For example, public datasets and volunteer/community networks are classified separately from
software that can be self-hosted.
