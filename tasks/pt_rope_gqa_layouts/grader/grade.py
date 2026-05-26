from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "rope_gqa.py"
    spec = importlib.util.spec_from_file_location("student_rope_gqa", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _copy_4d(tensor):
    return [
        [
            [list(head_values) for head_values in seq_item]
            for seq_item in batch_item
        ]
        for batch_item in tensor
    ]


def _reference_rotate(vector, cos_row, sin_row, rope_layout):
    if rope_layout == "half_split":
        half = len(cos_row)
        first = vector[:half]
        second = vector[half : half * 2]
        return [
            *(first[i] * cos_row[i] - second[i] * sin_row[i] for i in range(half)),
            *(first[i] * sin_row[i] + second[i] * cos_row[i] for i in range(half)),
        ]
    rotated = []
    for i, (cos_value, sin_value) in enumerate(zip(cos_row, sin_row)):
        even = vector[i * 2]
        odd = vector[i * 2 + 1]
        rotated.extend(
            [even * cos_value - odd * sin_value, even * sin_value + odd * cos_value]
        )
    return rotated


def _reference_apply(q, k, cos, sin, rope_layout):
    q_out = _copy_4d(q)
    k_out = _copy_4d(k)
    rotary_dim = len(cos[0]) * 2
    for tensor_out in (q_out, k_out):
        for batch_index in range(len(tensor_out)):
            for seq_index in range(len(tensor_out[batch_index])):
                for head_index in range(len(tensor_out[batch_index][seq_index])):
                    vector = tensor_out[batch_index][seq_index][head_index]
                    rotated = _reference_rotate(
                        vector[:rotary_dim], cos[seq_index], sin[seq_index], rope_layout
                    )
                    tensor_out[batch_index][seq_index][head_index] = rotated + vector[rotary_dim:]
    return q_out, k_out


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    checks = []

    q = [[[[1.0, 2.0, 3.0, 4.0, 9.0], [2.0, 1.0, 0.0, -1.0, 8.0]]]]
    k = [[[[5.0, 6.0, 7.0, 8.0, 7.5]]]]
    cos = [[0.0, 1.0]]
    sin = [[1.0, 0.0]]

    actual_half = module.apply_rope_gqa(q, k, cos, sin, rope_layout="half_split")
    expected_half = _reference_apply(q, k, cos, sin, "half_split")
    checks.append(
        {
            "name": "half_split_layout",
            "passed": actual_half == expected_half,
            "expected": expected_half,
            "actual": actual_half,
        }
    )

    actual_interleaved = module.apply_rope_gqa(q, k, cos, sin, rope_layout="interleaved")
    expected_interleaved = _reference_apply(q, k, cos, sin, "interleaved")
    checks.append(
        {
            "name": "interleaved_layout",
            "passed": actual_interleaved == expected_interleaved,
            "expected": expected_interleaved,
            "actual": actual_interleaved,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "RoPE implementation graded on half-split and interleaved layouts with tail-dimension preservation.",
    }
