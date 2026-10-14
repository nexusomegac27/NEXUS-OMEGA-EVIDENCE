# Lane C — CPU_NOT_EXECUTED_REASON.md (single scope-specific reason + runnable harness design)

## Reason (single, scope-specific)

NOT_EXECUTED because no authorized live CPU/VPS inference environment (no running Ollama endpoint, no llama.cpp build, no VPS, no paid resources) exists in this EXTERNAL_RESEARCH_ONLY session; the order (C3) prescribes exactly this outcome: deliver harness + measurement manifest, run zero VPS tests, no fabricated numbers.

## C1 — Primary-source confirmations (readback 2026-10-14; version pins UNKNOWN where not fetched)

- Ollama: two levels of concurrent processing; if sufficient memory is available (system memory for CPU inference, VRAM otherwise), multiple models can be loaded simultaneously; insufficient memory queues requests. Source: https://docs.ollama.com/faq (exact Ollama version UNKNOWN).
- llama.cpp: LLM inference in C/C++ with minimal setup across broad hardware; hand-tuned AVX/AVX2/AVX512/NEON assembly for CPU throughput; GGUF quantizations 2/3/4/5/6/8-bit; CPU+GPU hybrid supported. Sources: https://github.com/ggml-org/llama.cpp , https://llama-cpp.com/ , https://qwen.readthedocs.io/en/v1.5/run_locally/llama.cpp.html (version pins UNKNOWN).
- vLLM CPU prerequisites, SGLang CPU tooling, GPUStack Custom Backend overhead, training exclusions: UNKNOWN (not fetched this pass; no claim made).
- The operator's actual VPS cgroup values, CPU steal, memory limits: UNKNOWN and not asserted from any pricing page.

## C2 — Paired-trial harness design (deliverable, not executed)

One-shot paired trial: >= 10 synthetic/compliant tasks, 2 repeat rounds. Arms: (A) null model = existing reported Ollama + deterministic SQLite/FTS5 retrieval; (B) challenger = llama.cpp with identical model file (same GGUF blob SHA-256), identical quantization, pinned context length, pinned concurrency=1, cold and warm phases. Same acceptance oracle for both arms: accepted verifiable facts vs false-source claims, graded blind. Metrics: accepted-task count, false-source claims, TTFT p50/p95, decode tokens/s, peak RSS+swap, CPU time, task latency p50/p95, disk use, timeouts, operator touches; joules only if instrumented.

## C3 — Pre-registered thresholds (fixed before any run)

Null hypothesis: the deterministic SQLite/FTS5 + existing Ollama arm wins or ties on accepted utility per total resource and operator cost. The challenger replaces the null model only if ALL of:
(1) >= +15 percent accepted facts per CPU-hour;
(2) <= 0 false-source claims per 10 tasks in both rounds;
(3) task latency p95 non-regression > 10 percent;
(4) no new resident system dependency (per order C4) and peak RSS within the pre-declared budget;
(5) result reproduces in the second round within pre-registered tolerance.
Otherwise the challenger remains optional research and the null model stands. No LIVE_AUTO claim without uptime+job+input+output proof.

## C4

Inference, fine-tuning, memory retrieval, training and autonomous orchestration remain distinct; nothing in this return claims any of them as executed. Minimum worthwhile change remains: one measured real improvement with no new system dependency.
