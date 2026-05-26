from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "prompt_normalizer.py"
    spec = importlib.util.spec_from_file_location("student_prompt_normalizer", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    normalize_messages = module.normalize_messages
    checks = []

    case_1 = [
        {"role": "system", "content": "A"},
        {"role": "developer", "content": "B", "cache_hint": True},
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "world"},
    ]
    snapshot_1 = [dict(item) for item in case_1]
    expected_1 = [
        {"role": "system", "content": "A\n\nB", "cache_hint": True},
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "world"},
    ]
    actual_1 = normalize_messages(case_1)
    checks.append(
        {
            "name": "leading_system_and_developer_merge",
            "passed": actual_1 == expected_1,
            "expected": expected_1,
            "actual": actual_1,
        }
    )
    checks.append(
        {
            "name": "input_not_mutated",
            "passed": case_1 == snapshot_1,
            "expected": snapshot_1,
            "actual": case_1,
        }
    )

    case_2 = [
        {"role": "user", "content": "first"},
        {"role": "developer", "content": "late policy"},
        {"role": "tool", "content": "tool output"},
        {"role": "system", "content": "late system"},
        {"role": "assistant", "content": "done"},
    ]
    expected_2 = [
        {"role": "system", "content": "late policy\n\nlate system"},
        {"role": "user", "content": "first"},
        {"role": "tool", "content": "tool output"},
        {"role": "assistant", "content": "done"},
    ]
    actual_2 = normalize_messages(case_2)
    checks.append(
        {
            "name": "late_instruction_fragments_hoisted",
            "passed": actual_2 == expected_2,
            "expected": expected_2,
            "actual": actual_2,
        }
    )

    case_3 = [
        {"role": "user", "content": "u"},
        {"role": "assistant", "content": "a"},
    ]
    expected_3 = [
        {"role": "user", "content": "u"},
        {"role": "assistant", "content": "a"},
    ]
    actual_3 = normalize_messages(case_3)
    checks.append(
        {
            "name": "no_instruction_messages_passthrough",
            "passed": actual_3 == expected_3,
            "expected": expected_3,
            "actual": actual_3,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Prompt normalizer graded on fragmented instruction merge semantics, cache-hint preservation, and input immutability.",
    }
