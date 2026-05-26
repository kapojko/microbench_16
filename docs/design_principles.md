# Design Principles

MicroBench-12 is intentionally small. The point is not to mimic every public benchmark. The point is to create a trustworthy inner-loop benchmark that is:

- fast enough to rerun frequently
- mixed enough to prevent overfitting to one task style
- strict enough to expose semantic drift
- transparent enough that every failure can be understood

## What It Measures

The benchmark mixes four capabilities:

1. Basic algorithmic competence
2. Exact implementation of numerical semantics
3. Terminal and repository repair behavior
4. Repository understanding without code changes

## What It Does Not Measure

- large-context retrieval at public-benchmark scale
- GPU-heavy training workloads
- web browsing or internet-reliant agents
- human preference or style quality

## Anti-Cheat Stance

Phase 1 does not rely on secrecy alone. Where possible, tasks include semantic anti-cheat checks:

- `pt_kv_cache_generate` counts embedding visits to detect fake caching
- service and query tasks mutate hidden datasets or runtime settings
- QnA is rubric-graded by deterministic checklists rather than string equality

## Scoring

The benchmark uses task-level scores in `[0, 1]`.

- Binary tasks score `1.0` on pass and `0.0` on fail.
- Rubric tasks can award partial credit.
- Aggregate scores are simple means unless you choose a different reporting layer on top.

We intentionally avoid a single magic number inside the benchmark logic itself. The scorer emits the raw pieces so you can report:

- mean score
- family means
- difficulty means
- stability across repeats
- cost and latency overlays

## Repeats

For stochastic agents, use at least 3 repeats.

This benchmark keeps repeats outside the task definition. The same materialized task can be used across multiple repeated attempts, but you should usually rematerialize to avoid state leakage.
