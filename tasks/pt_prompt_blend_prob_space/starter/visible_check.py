import math

from prompt_blend import blend_branch_log_probs


def main() -> None:
    branch_log_probs = [
        [math.log(0.9), math.log(0.1)],
        [math.log(0.1), math.log(0.9)],
    ]
    weights = [0.75, 0.25]
    expected = [math.log(0.7), math.log(0.3)]
    actual = blend_branch_log_probs(branch_log_probs, weights)
    if any(abs(a - e) > 1e-9 for a, e in zip(actual, expected)):
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {actual}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
