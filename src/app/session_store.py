import uuid
from datetime import datetime
from typing import Optional

from app.models.session import Session
from app.models.suggestion import Suggestion

_store: dict[str, Session] = {}


def create_session(file_path: str, suggestions: list[Suggestion]) -> Session:
    sid = str(uuid.uuid4())
    session = Session(
        session_id=sid,
        file_path=file_path,
        created_at=datetime.utcnow(),
        suggestions=suggestions,
    )
    _store[sid] = session
    return session


def get_session(session_id: str) -> Optional[Session]:
    return _store.get(session_id)


def get_suggestions_by_ids(session_id: str, ids: list[str]) -> list[Suggestion]:
    session = get_session(session_id)
    if not session:
        return []
    id_set = set(ids)
    return [s for s in session.suggestions if s.id in id_set]
