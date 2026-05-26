from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_shortest_path(workspace_path: Path):
    module_path = workspace_path / "shortest_path.py"
    spec = importlib.util.spec_from_file_location("student_shortest_path", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.shortest_path


def grade_workspace(workspace_path: Path, task) -> dict:
    shortest_path = _load_shortest_path(workspace_path)
    checks = []

    weighted = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    checks.append(
        {
            "name": "weighted_graph",
            "passed": shortest_path(weighted, "A", "D") == (4, ["A", "B", "C", "D"]),
            "expected": (4, ["A", "B", "C", "D"]),
            "actual": shortest_path(weighted, "A", "D"),
        }
    )

    tie_graph = {
        "A": [("B", 1), ("C", 1)],
        "B": [("D", 1)],
        "C": [("D", 1)],
        "D": [],
    }
    expected_tie = (2, ["A", "B", "D"])
    actual_tie = shortest_path(tie_graph, "A", "D")
    checks.append(
        {
            "name": "lexicographic_tie_break",
            "passed": actual_tie == expected_tie,
            "expected": expected_tie,
            "actual": actual_tie,
        }
    )

    same_node_graph = {"Z": []}
    checks.append(
        {
            "name": "start_equals_goal",
            "passed": shortest_path(same_node_graph, "Z", "Z") == (0, ["Z"]),
            "expected": (0, ["Z"]),
            "actual": shortest_path(same_node_graph, "Z", "Z"),
        }
    )

    unreachable = {
        "A": [("B", 3)],
        "B": [],
        "C": [],
    }
    checks.append(
        {
            "name": "unreachable_goal",
            "passed": shortest_path(unreachable, "A", "C") is None,
            "expected": None,
            "actual": shortest_path(unreachable, "A", "C"),
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Shortest-path repair graded on weighted, tie-break, same-node, and unreachable cases.",
    }
