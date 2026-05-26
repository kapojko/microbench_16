# Task: `py_rate_limiter_sliding_window`

Repair `rate_limiter.py`.

The class API is:

```python
class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float) -> None: ...
    def allow(self, key: str, now: float) -> bool: ...
```

## Required Semantics

- The limiter is per-key.
- A request at time `now` is allowed if fewer than `limit` accepted requests exist in the interval:
  - `[now - window_seconds, now]`
- The lower bound is **inclusive**.
- The upper bound is **inclusive**.
- If allowed, the request becomes part of the accepted history immediately.
- The implementation should not leak old entries forever.

## Visible Check

Run:

```bash
python3 visible_check.py
```
