# THREAT_AND_COST_REPORT.md — independent opposing viewpoints and next safe step (C1)

## P6 — Threat-to-control matrix (descriptive annotation is never mitigation proof)

1. SSRF / URL fetching by tools: control = allowlist of exact repository/registry endpoints, deny-by-default egress; evidence class of any fetched item recorded in the ledger. Open: egress allowlists are deployment policy, not proven here.
2. DNS rebinding: control = pin resolved identity at request time; not exercised (no MCP runtime) — open.
3. URL redirects on source pages: control = treat post-redirect bytes as a NEW source identity with its own hash; enforced by ledger discipline in this return (every received item hashed by received bytes).
4. Descriptor/symlink swap on artifact path: control = V0.2 NOFOLLOW component anchoring (static-proved; runtime pending).
5. readOnlyHint spoofing: control = adapter I1 (hint != OS capability); executed in validator self-test T8. Residual: a host that ignores the adapter is uncontrolled.
6. Confused deputy (agent acts with operator rights on tool output): control = I3 execution authorization separation + dispatch records; executed T4.
7. Token passthrough / credential reuse by tools: control = per-tool scoped credentials, no shared secrets; not deployed here — open.
8. Session hijacking: control = short-lived sessions, no resident daemon (see P5 default) — open at deployment layer.
9. Tool collision (same tool name, different server): control = CAS key includes tool_profile_digest (P4); stale profile invalid (T7).
10. Dependency poisoning: control = pinned commit + registry metadata read-only; tarball-tree correspondence NOT asserted (L1); installing remains prohibited.
11. Result contamination (injection into agent context): control = six quarantined fixtures (P3) + inert-data rule; executed T10. Residual: a non-conforming consumer remains possible; adapter is fail-closed, consumers must be too.
12. Logging secrets: control = this bundle contains no credentials, tokens or private payloads (L5); future log schemas must redact by field allowlist.

## P5 — Direct CLI vs MCP daemon (risk-adjusted cost model, no installation)

Default: no permanently resident process. Direct CLI invocation: surface exists only during a triage run; smaller token/credential blast radius; per-run process cost (process spawn + model load if any) is bounded and attributable; no persistent listener for description-swap or collision attacks. MCP daemon: persistent listener and persistent tool registry; benefits only if (a) multiple concurrent consumers need the same tools with shared caching, or (b) a defended transport with authentication, allowlists and audit logging exists. Quantified defense threshold for a daemon: >= 2 concurrent regular consumers AND >= 30 percent measured per-task latency improvement for the cached path, with egress allowlist and per-tool credentials; otherwise CLI wins on risk-adjusted cost. Neither was installed or run here (order P5 prohibition respected).

## Opposing viewpoints (independent)

- For the math lane: one could defend the (1-lambda)^2 form as "intended only for lambda >= 0"; the M3 counterexample shows the written universal statement is false, and the correction (|lambda|) or the explicit restriction both repair it — the erratum diff offers both.
- For the forensics lane: the new root-anchor and data-region findings are static; a skeptic may argue the intermediate-symlink scenario requires attacker control of the root's ancestors and is therefore low priority. Counter: the V0.1 docstring claims general POSIX robustness, and the fix is cheap and total; engineering closure is warranted before any reuse.
- For the CPU lane: a pro-llama.cpp position would cite hand-tuned ISAs; but without a paired run on matched model hashes, any advantage claim is marketing (order C1/C3); the null model stands until thresholds are met.

## Differential risk (residual, with explicit conditions)

HIGH (unchanged, conditional): hostile in-place writer atomicity — detection-only semantics until immutable blob/snapshot staging exists. MEDIUM_CONDITIONAL: V0.2 runtime confirmation pending (fixtures delivered; no Python here). MEDIUM: lookalike distribution channel exists publicly (no download performed). LOW: index-count wording correction; Zip64 exact fixture pending.

## Next safe step

One authorized POSIX/Python 3.10+ session executes: 22 compat + 20 delta + 11 new fixtures against V0.2 in a disposable directory; results recorded with ACTUAL_EXECUTED labels and a distinct revision if any fixture fails. Then AXIOM performs the single adjudication. No ping-pong, no re-search of the same ZIP, no autostart.
