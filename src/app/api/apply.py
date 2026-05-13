from fastapi import APIRouter, HTTPException
from app.models.suggestion import ApplyRequest, ApplyResult
from app.session_store import get_suggestions_by_ids, get_session
from app.tools.apply_tool import apply_suggestions

router = APIRouter()


@router.post("/apply", response_model=ApplyResult)
async def apply_endpoint(request: ApplyRequest):
    session = get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session not found: {request.session_id}")

    matched = get_suggestions_by_ids(request.session_id, request.selected_suggestion_ids)
    matched_ids = {s.id for s in matched}
    skipped = [sid for sid in request.selected_suggestion_ids if sid not in matched_ids]

    if not matched:
        return ApplyResult(applied=[], skipped=skipped, message="No matching suggestions to apply.")

    message = apply_suggestions(file_path=session.file_path, suggestions=matched)

    return ApplyResult(
        applied=[s.id for s in matched],
        skipped=skipped,
        message=message,
    )
