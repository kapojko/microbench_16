from rate_limiter import SlidingWindowRateLimiter


def main() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10.0)
    outcomes = [
        limiter.allow("u1", 0.0),
        limiter.allow("u1", 1.0),
        limiter.allow("u1", 2.0),
        limiter.allow("u1", 10.0),
        limiter.allow("u1", 10.0001),
    ]
    expected = [True, True, False, False, True]
    if outcomes != expected:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {outcomes}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
