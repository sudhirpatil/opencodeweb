from pydantic import BaseModel
from datetime import datetime
from app.models.suggestion import Suggestion


class Session(BaseModel):
    session_id: str
    file_path: str
    created_at: datetime
    suggestions: list[Suggestion]
