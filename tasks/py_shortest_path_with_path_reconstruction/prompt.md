# Task: `py_shortest_path_with_path_reconstruction`

Repair `shortest_path.py`.

The exported function must be:

```python
def shortest_path(graph: dict[str, list[tuple[str, int]]], start: str, goal: str) -> tuple[int, list[str]] | None:
    ...
```

## Requirements

- Edge weights are non-negative integers.
- Return `None` when `goal` is unreachable from `start`.
- When `start == goal`, return `(0, [start])`.
- Otherwise return `(distance, path)` where `path` is the full node sequence from start to goal.
- If multiple shortest paths have the same total distance, return the **lexicographically smallest path** when compared as a list of node ids.
- Use only the Python standard library.

## Visible Check

Run:

```bash
python3 visible_check.py
```
