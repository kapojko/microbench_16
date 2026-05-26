from shortest_path import shortest_path


def main() -> None:
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    expected = (4, ["A", "B", "C", "D"])
    actual = shortest_path(graph, "A", "D")
    if actual != expected:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {actual}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
