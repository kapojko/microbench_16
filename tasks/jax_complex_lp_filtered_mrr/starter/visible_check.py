from complex_lp import complex_score


def main() -> None:
    actual = complex_score([1.0], [2.0], [3.0], [4.0], [5.0], [6.0])
    expected = 35.0
    if abs(actual - expected) > 1e-9:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {actual}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
