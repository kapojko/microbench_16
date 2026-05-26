from __future__ import annotations

import json
import shutil
from pathlib import Path

from microbench12.types import TaskSpec


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def tasks_root() -> Path:
    return project_root() / "tasks"


def task_dir(task_id: str) -> Path:
    return tasks_root() / task_id


def manifest_path() -> Path:
    return tasks_root() / "manifest.json"


def load_manifest() -> dict:
    with manifest_path().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_task_ids() -> list[str]:
    manifest = load_manifest()
    return [item["id"] for item in manifest["tasks"]]


def load_task(task_id: str) -> TaskSpec:
    spec_path = task_dir(task_id) / "task.json"
    if not spec_path.exists():
        raise FileNotFoundError(f"Unknown task: {task_id}")
    with spec_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return TaskSpec.from_dict(payload)


def load_prompt(task_id: str) -> str:
    prompt_path = task_dir(task_id) / "prompt.md"
    return prompt_path.read_text(encoding="utf-8")


def public_task_payload(task: TaskSpec) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "difficulty": task.difficulty,
        "family": task.family,
        "task_type": task.task_type,
        "response_type": task.response_type,
        "summary": task.summary,
        "required_tools": task.required_tools,
        "time_budget_sec": task.time_budget_sec,
        "visible_checks": task.visible_checks,
        "expected_artifacts": task.expected_artifacts,
        "fairness_notes": task.fairness_notes,
        "anti_cheat_notes": task.anti_cheat_notes,
        "tags": task.tags,
    }


def materialize_task(task_id: str, out_dir: Path, *, force: bool = False) -> Path:
    task = load_task(task_id)
    source = task_dir(task_id) / task.starter_subdir
    if not source.exists():
        raise FileNotFoundError(f"Starter directory missing for task {task_id}: {source}")

    if out_dir.exists():
        if not force:
            raise FileExistsError(f"Output directory already exists: {out_dir}")
        shutil.rmtree(out_dir)

    shutil.copytree(
        source,
        out_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )

    control_dir = out_dir / ".microbench12"
    control_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "TASK_PROMPT.md").write_text(load_prompt(task_id), encoding="utf-8")
    (control_dir / "task.json").write_text(
        json.dumps(public_task_payload(task), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (control_dir / "task_id.txt").write_text(f"{task_id}\n", encoding="utf-8")
    return out_dir
