# MicroBench-12

MicroBench-12 is a small benchmark for comparing coding-agent harnesses on realistic software-engineering tasks with local OpenAI-compatible models.

It includes 16 tasks, deterministic hidden graders, host-side result JSON, and optional one-shot Docker isolation for agent harnesses.

## What is included

```text
microbench12/          Benchmark CLI, materialization, grading, scoring
tasks/                 16 task definitions with prompt.md, starter/, grader/
scripts/               Native host runners for installed harnesses
containerized/         Isolated Docker runners for OpenCode, Pi, Hermes, OpenClaw
containerized/docker/  Minimal harness images
docs/                  Benchmark design notes and harness integration contract
```

## Install

```bash
cd microbench-12-release
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

List tasks:

```bash
python -m microbench12 list
```

Materialize one task manually:

```bash
python -m microbench12 materialize   --task pt_logit_lens_layers   --out materialized/demo-pt-logit-lens
```

Grade a completed workspace manually:

```bash
python -m microbench12 grade   --task pt_logit_lens_layers   --workspace materialized/demo-pt-logit-lens   --model local/Qwen3.6-35B   --harness manual   --repeat 1   --out results/demo-pt-logit-lens.json
```

## Local model server

The runners expect an OpenAI-compatible chat/completions server, for example vLLM or llama.cpp server.

Example model endpoint:

```text
http://192.168.90.17:8080/v1
```

Check it before running:

```bash
curl http://192.168.90.17:8080/v1/models
```

Use model selectors in this form:

```text
provider/model-id
```

Example:

```text
myprovider/Qwen3.6-35B
```

The provider name is only a local label used by the harness config generated for each run. The model id must match the id exposed by `/v1/models`.

## Containerized harness runs

Containerized mode is the recommended isolation mode.

For every task, the runner:

1. creates a fresh materialized workspace from `starter/`;
2. writes `TASK_PROMPT.md` and public `.microbench12/task.json` into that workspace;
3. creates a fresh harness home/state directory;
4. starts the harness inside a one-shot Docker container;
5. mounts only the task workspace and harness home into that container;
6. runs the hidden grader on the host after the container exits.

The task `grader/` directory is never mounted into the harness container. The agent can see the task prompt, starter files, visible checks, and public metadata, but not the hidden grading script.

### Build harness images

These images copy your locally installed harness into a minimal Debian image. Build only the harnesses you want to run.

```bash
containerized/build_harness_image.sh opencode
containerized/build_harness_image.sh pi
containerized/build_harness_image.sh hermes
containerized/build_harness_image.sh openclaw
```

Default expected install paths:

```text
OpenCode: ~/.opencode/bin/opencode
Hermes:   ~/.hermes/hermes-agent
Pi:       ~/.nvm/versions/node/v20.20.2/lib/node_modules/@mariozechner/pi-coding-agent
OpenClaw: ~/.nvm/versions/node/v22.22.3/lib/node_modules/openclaw
```

If your paths differ, set environment variables before building:

```bash
OPENCODE_BIN=/path/to/opencode containerized/build_harness_image.sh opencode
HERMES_AGENT_DIR=/path/to/hermes-agent containerized/build_harness_image.sh hermes
PI_NODE_BIN=/path/to/node PI_AGENT_DIR=/path/to/pi-coding-agent containerized/build_harness_image.sh pi
OPENCLAW_NODE_BIN=/path/to/node OPENCLAW_AGENT_DIR=/path/to/openclaw containerized/build_harness_image.sh openclaw
```

### Run one task

OpenCode:

```bash
python3 containerized/run_containerized_opencode_benchmark.py   --model myprovider/Qwen3.6-35B   --task pt_logit_lens_layers   --openai-compatible-base-url http://192.168.90.17:8080/v1   --task-timeout-sec 1200
```

Pi:

```bash
python3 containerized/run_containerized_pi_benchmark.py   --model myprovider/Qwen3.6-35B   --task pt_logit_lens_layers   --openai-compatible-base-url http://192.168.90.17:8080/v1   --task-timeout-sec 1200
```

Hermes:

```bash
python3 containerized/run_containerized_hermes_benchmark.py   --model myprovider/Qwen3.6-35B   --task pt_logit_lens_layers   --openai-compatible-base-url http://192.168.90.17:8080/v1   --task-timeout-sec 1200
```

OpenClaw:

```bash
python3 containerized/run_containerized_openclaw_benchmark.py   --model myprovider/Qwen3.6-35B   --task pt_logit_lens_layers   --openai-compatible-base-url http://192.168.90.17:8080/v1   --task-timeout-sec 1200
```

Run all tasks by replacing the task flag:

```bash
--task all
```

Results are written to:

```text
results/runs/<timestamp>__<harness>-container__<model>/
```

Materialized task workspaces are written to:

```text
materialized/runs/<timestamp>__<harness>-container__<model>/
```

## Native host runs

If you want to run installed harnesses directly on the host, use:

```bash
python3 scripts/run_harness_benchmark.py   --harness opencode   --model myprovider/Qwen3.6-35B   --task pt_logit_lens_layers   --backend vllm   --task-timeout-sec 1200   --skip-permissions
```

Supported harness names depend on what is installed on your machine and configured in your harness config.

## Result files

Each run stores:

```text
run_metadata.json   Run configuration
run_progress.json   Live progress and current task states
run_summary.json    Final summary
tasks/*/*.log       Harness stdout/stderr
tasks/*/telemetry.json
tasks/*/grade_result.json
tasks/*/task_record.json
```

Task statuses:

```text
passed       Hidden grader passed
failed       Hidden grader ran, but the solution was wrong
runner_error Harness timed out or the benchmark runner failed
infra_error  Harness or environment failed before grading completed
```

Aggregate results:

```bash
python -m microbench12 score   --results-dir results/runs   --out results/summary.json
```

## Notes

- `results/` and `materialized/` are ignored by git.
- Containerized runners are designed to keep hidden graders outside the agent container.
- Visible checks are available for iteration, but only hidden graders decide pass/fail.
- The benchmark does not require a cloud API. Use any local OpenAI-compatible model server that your harness can reach.
