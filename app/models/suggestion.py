from pydantic import BaseModel


class Suggestion(BaseModel):
    id: str
    file_path: str
    description: str
    original_code: str
    suggested_code: str
    line_start: int
    line_end: int
    rule_reference: str


class AnalyzeRequest(BaseModel):
    file_path: str
    rules_prompt_path: str


class AnalyzeResponse(BaseModel):
    session_id: str
    suggestions: list[Suggestion]


class ApplyRequest(BaseModel):
    session_id: str
    selected_suggestion_ids: list[str]


class ApplyResult(BaseModel):
    applied: list[str]
    skipped: list[str]
    message: str
