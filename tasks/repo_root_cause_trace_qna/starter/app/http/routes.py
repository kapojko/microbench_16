from __future__ import annotations

from app.core.onboarding import resume_or_restart
from app.store.session_store import SessionStore


def handle_continue_link(store: SessionStore, session_id: str, now: float) -> dict[str, str]:
    state = resume_or_restart(store, session_id, now)
    if state["action"] == "restart":
        return {
            "redirect": "/onboarding/welcome",
            "reason": "missing_session",
        }
    return {
        "redirect": f'/onboarding/{state["step"]}',
        "reason": "resume_existing_session",
    }
