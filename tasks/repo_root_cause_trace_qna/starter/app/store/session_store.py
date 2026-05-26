from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Session:
    session_id: str
    user_id: str
    current_step: str
    status: str
    issued_at: float
    last_seen_at: float


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def save(self, session: Session) -> None:
        self._sessions[session.session_id] = session

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def touch(self, session_id: str, now: float) -> None:
        session = self._sessions.get(session_id)
        if session is not None:
            session.last_seen_at = now

    def all_sessions(self) -> list[Session]:
        return list(self._sessions.values())
