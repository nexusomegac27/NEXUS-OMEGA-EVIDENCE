# R44-3 resource lease (budget-matching) scientific protocol — design only

## Purpose
Demonstrate independent scientific information gain at equal **total** cost, not "more models won because they spent more". Cost transparency is necessary but not sufficient for science correctness, and no budget/price cap is invented here without observing real runner capabilities and explicit operator approval.

## Contract fields frozen BEFORE revealing tests
- LEASE_ID, study ID, task target, participant or input group; run actor+declared model/provider/version+source lineage; evaluator separate authority.
- Cost caps: monotonic wall seconds; CPU seconds including all child processes; peak RSS MiB; total process starts; total input and output tokens incl hidden reasoning if measurable, model/version/API unit price with timestamp and not-measurable fields explicit; external API calls; network outbound bytes/requests; storage bytes and retention; expected evaluator cost; maximum total currency units with consistent timestamp/exchange source if needed; retries/parallel runs and sampler seeds.
- Exact task examples/source/hash, environment/container hash, budget freeze commit and scorer/hash, original test split and hidden label access.
- Actual measurement: start and end MONOTONIC clock in same origin, separately wall clock, consumed CPU/RSS/tokens/egress/child cost, retries, collection error, completeness, predeclared cost scope. If host has unreliable clock or telemetry, emit UNKNOWN_COST and exclude from matched-cost comparison.
- Branches: lease remaining -> bounded run. Overage/unknown-critical-cost -> BUDGET_EXHAUSTED / HOLD_COMPARISON, safe stop of expensive task and preserve partial output. Never assume negative elapsed cost is performance improvement. Research agent can still write a low-cost private/read-only gap report if authorized.
- Fairness: same total budget across SINGLE_AGENT vs MULTI_AGENT_SHARED_SOURCE vs ACTUALLY_INDEPENDENT_AUTHENTICATED actors, including evaluator and all tool/retry overhead, no hidden free evaluation oracle. Collect repeated trial distributions; source-independent units in CIs rather than tokens as independent data.
- Optimize predeclared verified new falsifiers per cost, precision/recall of true errors, false-PASS/false-HOLD, held-out score and cost distribution; NEVER reward simply number of vulnerabilities/patches, synthetic PASS labels, signer counts or clever prompt length. The "cheapest" invalid result is not a win.
- Privacy-safe public reporting: aggregated budgets and provenance only; never API keys, billed account IDs, private customer samples or credentials.

## Required experiments
1. negative elapsed source case from prior Qwen -15759.254 = invalid duration (not inherently an attack).
2. missing child CPU/egress/retries source receipts = cost-gapped and comparison blocked.
3. group B multi-agent improves apparent result but exceeds true total budget -> NO COMPARATIVE CLAIM.
4. positive valid resource lease measured and source-grounded equal-cost comparison; uncertainty in effect and false-PASS.
5. deliberate budget exhaustion triggers scoped safe suspend, not "Node punished forever."

## Authority
No host quota change, billing plan modification, agent scheduling, paid API invocation or live monitoring installation is authorized by writing this research design. Only an independently approved future experiment may consume actual resources.
