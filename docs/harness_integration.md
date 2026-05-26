# Harness Integration

MicroBench-12 is harness-agnostic. A harness only needs to support one contract:

1. Receive a materialized workspace.
2. Read `TASK_PROMPT.md`.
3. Edit files in-place or create the requested answer artifact.
4. Stop when done.
5. Let the benchmark runner grade the final workspace.

## Materialized Workspace Contract

When you materialize a task, the output directory contains:

- starter repository contents
- `TASK_PROMPT.md`
- `.microbench12/task.json`

The hidden grader is **not** copied into the workspace.

## Task Types

### Code / Query / Systems Tasks

The harness edits files in-place. The grader evaluates the modified workspace.

### QnA Tasks

The harness must write the requested artifact, usually `answer.md`.

## Optional Telemetry

You can attach a telemetry JSON file at grading time. This is optional but recommended.

Suggested fields:

```json
{
  "wall_time_sec": 182.4,
  "agent_time_sec": 171.2,
  "turns": 14,
  "commands": 31,
  "total_tokens": 48210,
  "input_tokens": 38001,
  "output_tokens": 10209,
  "cache_read_tokens": 0,
  "cache_write_tokens": 0,
  "notes": "equalized profile, no network"
}
```

## Recommended Variant Key

Use a stable identifier per evaluated variant, for example:

`codex__qwen3.6-35b-a3b__vllm__reasoning-high__equalized`

The benchmark CLI stores the fields separately, but a stable variant key makes dashboards and spreadsheets simpler.
