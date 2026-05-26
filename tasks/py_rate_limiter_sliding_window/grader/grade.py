from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_class(workspace_path: Path):
    module_path = workspace_path / "rate_limiter.py"
    spec = importlib.util.spec_from_file_location("student_rate_limiter", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SlidingWindowRateLimiter


def grade_workspace(workspace_path: Path, task) -> dict:
    limiter_cls = _load_class(workspace_path)
    checks = []

    limiter = limiter_cls(limit=2, window_seconds=10.0)
    sequence = [
        limiter.allow("u1", 0.0),
        limiter.allow("u1", 1.0),
        limiter.allow("u1", 2.0),
        limiter.allow("u1", 10.0),
        limiter.allow("u1", 10.0001),
    ]
    expected_sequence = [True, True, False, False, True]
    checks.append(
        {
            "name": "boundary_semantics",
            "passed": sequence == expected_sequence,
            "expected": expected_sequence,
            "actual": sequence,
        }
    )

    multi = limiter_cls(limit=2, window_seconds=5.0)
    sequence_multi = [
        multi.allow("alice", 0.0),
        multi.allow("bob", 0.0),
        multi.allow("alice", 1.0),
        multi.allow("bob", 1.0),
        multi.allow("alice", 2.0),
        multi.allow("bob", 2.0),
    ]
    expected_multi = [True, True, True, True, False, False]
    checks.append(
        {
            "name": "per_key_isolation",
            "passed": sequence_multi == expected_multi,
            "expected": expected_multi,
            "actual": sequence_multi,
        }
    )

    floaty = limiter_cls(limit=3, window_seconds=1.0)
    sequence_floaty = [
        floaty.allow("k", 0.1),
        floaty.allow("k", 0.2),
        floaty.allow("k", 1.1),
        floaty.allow("k", 1.1000001),
    ]
    expected_floaty = [True, True, True, True]
    checks.append(
        {
            "name": "floating_point_expiry",
            "passed": sequence_floaty == expected_floaty,
            "expected": expected_floaty,
            "actual": sequence_floaty,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Sliding-window limiter graded on boundary, per-key, and floating-point cases.",
    }
