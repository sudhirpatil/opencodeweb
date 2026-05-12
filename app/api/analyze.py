from fastapi import APIRouter, HTTPException
from app.models.suggestion import AnalyzeRequest, AnalyzeResponse
from app.agent.agent import run_analysis
from app.session_store import create_session

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    try:
        suggestions = await run_analysis(request.file_path, request.rules_prompt_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    session = create_session(file_path=request.file_path, suggestions=suggestions)
    return AnalyzeResponse(session_id=session.session_id, suggestions=suggestions)
