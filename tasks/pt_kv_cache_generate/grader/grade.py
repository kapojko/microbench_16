from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "kv_cache_generate.py"
    spec = importlib.util.spec_from_file_location("student_kv_cache", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    checks = []

    model = module.ToyDecoder.demo()
    expected = module.generate_reference(model, [2, 1, 0], 3)
    model.reset_counters()
    actual = module.generate_cached(model, [2, 1, 0], 3)
    checks.append(
        {
            "name": "matches_reference_generation",
            "passed": actual == expected,
            "expected": expected,
            "actual": actual,
        }
    )

    max_embedding_visits = 6
    checks.append(
        {
            "name": "cache_semantics_embedding_visits",
            "passed": model.embedding_visits <= max_embedding_visits,
            "expected": {"max_embedding_visits": max_embedding_visits},
            "actual": {"embedding_visits": model.embedding_visits},
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "KV-cache generation graded on exact greedy output and embedding-visit anti-cheat semantics.",
    }
