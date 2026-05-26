from __future__ import annotations

from app.store.session_store import SessionStore


def resume_or_restart(store: SessionStore, session_id: str, now: float) -> dict[str, str]:
    session = store.get(session_id)
    if session is None:
        return {"action": "restart", "step": "welcome"}

    store.touch(session_id, now)
    return {"action": "resume", "step": session.current_step}
