import json
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from app.config import settings
from app.tools.file_tools import read_file

# Set once per analysis run by agent.py before the agent is invoked
_current_rules: str = ""


def set_rules(rules: str) -> None:
    global _current_rules
    _current_rules = rules


_ANALYSIS_PROMPT = """\
You are an expert PySpark code reviewer. Analyze the following PySpark code against the given rules.
Return ONLY a JSON array of suggestion objects — no other text, no markdown fences.

Rules:
{rules}

PySpark code (line numbers shown):
{numbered_code}

Each suggestion object must have exactly these fields:
- id: unique string like "sugg_001", "sugg_002", etc.
- file_path: the file path provided
- description: plain English explanation of the issue and how to fix it
- original_code: the exact code snippet being replaced (copy from the numbered code, without line number prefix)
- suggested_code: the full replacement code snippet
- line_start: starting line number (integer, 1-indexed)
- line_end: ending line number (integer, 1-indexed, inclusive)
- rule_reference: which rule this addresses (e.g. "Rule 1: Avoid collect()")

Return [] if no issues are found.
"""


def _number_lines(content: str) -> str:
    return "\n".join(f"{i + 1:4d}: {line}" for i, line in enumerate(content.splitlines()))


@tool
def analyze_pyspark_code(file_path: str) -> str:
    """Analyze a PySpark Python file against the configured rules.
    Returns a JSON array of suggestion objects with id, file_path, description,
    original_code, suggested_code, line_start, line_end, and rule_reference."""
    content = read_file.invoke({"path": file_path})
    if content.startswith("Error:"):
        return json.dumps([])

    numbered_code = _number_lines(content)
    prompt = _ANALYSIS_PROMPT.format(rules=_current_rules, numbered_code=numbered_code)

    llm = ChatAnthropic(
        model=settings.model_name,
        api_key=settings.anthropic_api_key,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )

    response = llm.invoke(prompt)
    raw = response.content.strip()
    print(f"LLM Response: {raw}")

    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(raw)
        for item in data:
            item["file_path"] = file_path  # always override — LLM often returns "" or "unknown"
        return json.dumps(data)
    except json.JSONDecodeError:
        return json.dumps([])
