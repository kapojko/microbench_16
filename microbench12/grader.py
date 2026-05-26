from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

from microbench12.tasks import task_dir, load_task
from microbench12.types import AttemptMetadata, TaskSpec


def _load_module(module_path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load grader module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_grade(result: dict[str, Any]) -> dict[str, Any]:
    required = {"score", "passed", "checks", "summary"}
    missing = required - set(result)
    if missing:
        raise ValueError(f"Grader result missing keys: {sorted(missing)}")
    return result


def grade_workspace(
    task_id: str,
    workspace: Path,
    metadata: AttemptMetadata,
    telemetry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    task: TaskSpec = load_task(task_id)
    module_path = task_dir(task_id) / task.grader_entrypoint
    grader = _load_module(module_path, f"grader_{task_id}")
    if not hasattr(grader, "grade_workspace"):
        raise AttributeError(f"{module_path} must define grade_workspace(workspace_path, task)")
    raw = grader.grade_workspace(workspace, task)
    graded = _normalize_grade(raw)
    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "difficulty": task.difficulty,
            "family": task.family,
            "task_type": task.task_type,
        },
        "attempt": metadata.to_dict(),
        "result": graded,
        "telemetry": telemetry or {},
    }


def load_telemetry(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
