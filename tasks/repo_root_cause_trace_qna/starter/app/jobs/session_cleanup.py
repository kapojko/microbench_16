from __future__ import annotations

from app.store.session_store import SessionStore


def drop_expired_pending_sessions(
    store: SessionStore, now: float, pending_ttl_seconds: float = 1800.0
) -> list[str]:
    dropped: list[str] = []
    for session in store.all_sessions():
        if session.status != "pending":
            continue

        # BUG: pending sessions are purged using issued_at, which ignores recent user activity.
        age_seconds = now - session.issued_at
        if age_seconds > pending_ttl_seconds:
            store.delete(session.session_id)
            dropped.append(session.session_id)
    return dropped
