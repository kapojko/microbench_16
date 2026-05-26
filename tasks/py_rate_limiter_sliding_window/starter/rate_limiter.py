from __future__ import annotations

from collections import defaultdict, deque


class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._accepted: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, now: float) -> bool:
        bucket = self._accepted[key]

        # BUG: the lower boundary is inclusive, so entries at exactly
        # now - window_seconds should still count inside the window.
        while bucket and bucket[0] <= now - self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.limit:
            return False

        bucket.append(now)
        return True
