from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "prompt_blend.py"
    spec = importlib.util.spec_from_file_location("student_prompt_blend", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _reference(branch_log_probs, weights):
    total_weight = sum(weights)
    normalized = [weight / total_weight for weight in weights]
    vocab = len(branch_log_probs[0])
    out = []
    for token_index in range(vocab):
        prob = 0.0
        for branch_index, branch in enumerate(branch_log_probs):
            prob += normalized[branch_index] * math.exp(branch[token_index])
        out.append(math.log(prob))
    return out


def _close(actual, expected, tol=1e-9):
    return len(actual) == len(expected) and all(abs(a - e) <= tol for a, e in zip(actual, expected))


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    checks = []

    case_1 = (
        [
            [math.log(0.9), math.log(0.1)],
            [math.log(0.1), math.log(0.9)],
        ],
        [0.75, 0.25],
    )
    expected_1 = _reference(*case_1)
    actual_1 = module.blend_branch_log_probs(*case_1)
    checks.append(
        {
            "name": "asymmetric_two_branch_blend",
            "passed": _close(actual_1, expected_1),
            "expected": expected_1,
            "actual": actual_1,
        }
    )

    case_2 = (
        [
            [math.log(1e-30), math.log(1.0 - 1e-30)],
            [math.log(0.4), math.log(0.6)],
            [math.log(0.8), math.log(0.2)],
        ],
        [1.0, 2.0, 1.0],
    )
    expected_2 = _reference(*case_2)
    actual_2 = module.blend_branch_log_probs(*case_2)
    checks.append(
        {
            "name": "extreme_probability_stability",
            "passed": _close(actual_2, expected_2),
            "expected": expected_2,
            "actual": actual_2,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Prompt blending graded on asymmetric and extreme-probability mixtures.",
    }
