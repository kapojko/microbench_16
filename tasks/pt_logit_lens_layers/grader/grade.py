from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "logit_lens.py"
    spec = importlib.util.spec_from_file_location("student_logit_lens", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _reference(hidden_states, ln_weight, ln_bias, lm_head, k):
    def normalize(vector):
        mean = sum(vector) / len(vector)
        var = sum((value - mean) ** 2 for value in vector) / len(vector)
        scale = math.sqrt(var + 1e-5)
        return [
            ((value - mean) / scale) * weight + bias
            for value, weight, bias in zip(vector, ln_weight, ln_bias)
        ]

    output = []
    for layer_states in hidden_states:
        token = layer_states[-1]
        normalized = normalize(token)
        logits = []
        for token_id, row in enumerate(lm_head):
            logits.append((sum(value * weight for value, weight in zip(normalized, row)), token_id))
        logits.sort(key=lambda item: (-item[0], item[1]))
        output.append([token_id for _, token_id in logits[:k]])
    return output


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    fn = module.logit_lens_topk
    checks = []

    hidden_states_1 = [
        [[1.0, 0.0, -1.0], [0.5, 1.5, -0.5]],
        [[0.0, 2.0, -1.0], [1.0, 0.0, 1.0]],
    ]
    ln_weight_1 = [1.0, 1.0, 1.0]
    ln_bias_1 = [0.0, 0.0, 0.0]
    lm_head_1 = [
        [1.0, 0.0, 0.5],
        [0.0, 1.0, 0.0],
        [-0.5, 0.5, 1.0],
        [0.5, -1.0, 0.0],
    ]
    expected_1 = _reference(hidden_states_1, ln_weight_1, ln_bias_1, lm_head_1, 2)
    actual_1 = fn(hidden_states_1, ln_weight_1, ln_bias_1, lm_head_1, 2)
    checks.append(
        {
            "name": "visible_like_fixture",
            "passed": actual_1 == expected_1,
            "expected": expected_1,
            "actual": actual_1,
        }
    )

    hidden_states_2 = [
        [[2.0, -1.0, 0.0], [0.0, 1.0, 3.0]],
        [[1.0, 1.0, -2.0], [2.5, -0.5, 1.0]],
        [[-1.0, 2.0, 0.5], [3.0, 0.0, -1.0]],
    ]
    ln_weight_2 = [1.5, 0.5, 2.0]
    ln_bias_2 = [0.1, -0.2, 0.3]
    lm_head_2 = [
        [0.5, 1.0, -0.5],
        [1.0, -0.5, 0.5],
        [-1.0, 0.0, 1.5],
        [0.0, 0.5, 0.5],
    ]
    expected_2 = _reference(hidden_states_2, ln_weight_2, ln_bias_2, lm_head_2, 2)
    actual_2 = fn(hidden_states_2, ln_weight_2, ln_bias_2, lm_head_2, 2)
    checks.append(
        {
            "name": "final_token_and_layernorm_semantics",
            "passed": actual_2 == expected_2,
            "expected": expected_2,
            "actual": actual_2,
        }
    )

    hidden_states_3 = [
        [[0.0, 0.0], [1.0, -1.0]],
    ]
    ln_weight_3 = [1.0, 1.0]
    ln_bias_3 = [0.0, 0.0]
    lm_head_3 = [
        [1.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ]
    expected_3 = _reference(hidden_states_3, ln_weight_3, ln_bias_3, lm_head_3, 2)
    actual_3 = fn(hidden_states_3, ln_weight_3, ln_bias_3, lm_head_3, 2)
    checks.append(
        {
            "name": "tie_break_by_token_id",
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
        "summary": "Logit-lens task graded on final-token selection, correct layer norm, projection, and deterministic tie-breaking.",
    }
