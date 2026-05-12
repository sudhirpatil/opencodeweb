from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from app.session_store import get_session

router = APIRouter()


@router.get("/files/{file_path:path}", response_class=PlainTextResponse)
async def get_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions/{session_id}")
async def get_suggestions(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return {
        "session_id": session_id,
        "file_path": session.file_path,
        "suggestions": [s.model_dump() for s in session.suggestions],
    }
