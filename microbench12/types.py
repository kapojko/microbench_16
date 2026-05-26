from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TaskSpec:
    id: str
    title: str
    difficulty: str
    family: str
    task_type: str
    response_type: str
    summary: str
    required_tools: list[str]
    time_budget_sec: int
    starter_subdir: str
    grader_entrypoint: str
    visible_checks: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    fairness_notes: list[str] = field(default_factory=list)
    anti_cheat_notes: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def starter_dir(self) -> Path:
        return Path(self.starter_subdir)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskSpec":
        return cls(
            id=payload["id"],
            title=payload["title"],
            difficulty=payload["difficulty"],
            family=payload["family"],
            task_type=payload["task_type"],
            response_type=payload["response_type"],
            summary=payload["summary"],
            required_tools=list(payload.get("required_tools", [])),
            time_budget_sec=int(payload["time_budget_sec"]),
            starter_subdir=payload.get("starter_subdir", "starter"),
            grader_entrypoint=payload["grader_entrypoint"],
            visible_checks=list(payload.get("visible_checks", [])),
            expected_artifacts=list(payload.get("expected_artifacts", [])),
            fairness_notes=list(payload.get("fairness_notes", [])),
            anti_cheat_notes=list(payload.get("anti_cheat_notes", [])),
            tags=list(payload.get("tags", [])),
        )


@dataclass(slots=True)
class AttemptMetadata:
    task_id: str
    model: str
    harness: str
    repeat: int
    variant: str | None = None
    backend: str | None = None
    reasoning_mode: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "model": self.model,
            "harness": self.harness,
            "repeat": self.repeat,
            "variant": self.variant,
            "backend": self.backend,
            "reasoning_mode": self.reasoning_mode,
            "notes": self.notes,
        }
