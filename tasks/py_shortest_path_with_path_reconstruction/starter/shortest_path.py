from __future__ import annotations

from collections import deque


def shortest_path(
    graph: dict[str, list[tuple[str, int]]], start: str, goal: str
) -> tuple[int, list[str]] | None:
    """Return (distance, path) for the cheapest route from start to goal.

    This starter implementation is intentionally wrong:
    - it behaves like BFS even when weights differ
    - it does not handle lexicographic tie-breaking
    - it returns a path in some cases but not all edge cases
    """

    if start not in graph or goal not in graph:
        return None

    queue = deque([(start, 0, [start])])
    seen: set[str] = {start}

    while queue:
        node, dist, path = queue.popleft()
        if node == goal:
            return dist, path
        for neighbor, weight in graph.get(node, []):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((neighbor, dist + weight, path + [neighbor]))

    return None
