from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HIDDEN_TEST = r"""
use arena_graph::{ArenaGraph, NodeId};

#[test]
fn hidden_checks() {
    let mut graph = ArenaGraph::new();
    let root = graph.insert_root("root");
    let a = graph.insert_child(root, "a").expect("a");
    let b = graph.insert_child(root, "b").expect("b");
    let c = graph.insert_child(a, "c").expect("c");
    let d = graph.insert_child(a, "d").expect("d");

    assert_eq!(graph.insert_child(NodeId(999), "x"), None);
    assert_eq!(graph.path_to_root(d), Some(vec![root, a, d]));
    assert_eq!(graph.descendants_bfs(root), Some(vec![a, b, c, d]));
    assert_eq!(graph.value(c), Some(&"c"));
}
"""


def grade_workspace(workspace_path: Path, task) -> dict:
    checks = []
    hidden_test_path = workspace_path / "tests" / "mb12_hidden.rs"
    hidden_test_path.write_text(HIDDEN_TEST, encoding="utf-8")

    try:
        result = subprocess.run(
            ["cargo", "test", "--test", "visible_smoke", "--test", "mb12_hidden"],
            cwd=workspace_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        checks.append(
            {
                "name": "cargo_integration_tests",
                "passed": False,
                "expected": 0,
                "actual": "timeout",
                "stdout": (exc.stdout or "")[-4000:],
                "stderr": (exc.stderr or "")[-4000:],
            }
        )
    else:
        checks.append(
            {
                "name": "cargo_integration_tests",
                "passed": result.returncode == 0,
                "expected": 0,
                "actual": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-4000:],
            }
        )
    finally:
        if hidden_test_path.exists():
            hidden_test_path.unlink()

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Arena graph library graded with visible and hidden cargo integration tests.",
    }
