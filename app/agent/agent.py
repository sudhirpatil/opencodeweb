import json
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from app.config import settings
from app.models.suggestion import Suggestion
from app.tools.file_tools import read_file, list_directory, create_file
from app.tools.analysis_tool import analyze_pyspark_code, set_rules
from app.tools.apply_tool import apply_changes
from app.agent.prompts import build_system_prompt, get_rules_content

_TOOLS = [read_file, list_directory, create_file, analyze_pyspark_code, apply_changes]


def _build_agent(system_prompt: str):
    llm = ChatAnthropic(
        model=settings.model_name,
        api_key=settings.anthropic_api_key,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )
    return create_agent(model=llm, tools=_TOOLS, system_prompt=system_prompt)


async def run_analysis(file_path: str, rules_prompt_path: str) -> list[Suggestion]:
    system_prompt = build_system_prompt(rules_prompt_path)
    set_rules(get_rules_content(rules_prompt_path))

    agent = _build_agent(system_prompt)

    task_message = (
        f"Analyze the PySpark file at: {file_path}\n"
        f"Call the analyze_pyspark_code tool with file_path='{file_path}'. "
        f"Return the JSON array result verbatim — no other text."
    )

    result = await agent.ainvoke({"messages": [HumanMessage(content=task_message)]})

    raw_output = "[]"
    for msg in reversed(result.get("messages", [])):
        content = getattr(msg, "content", "")
        if isinstance(content, str) and content.strip():
            raw_output = content.strip()
            break

    if raw_output.startswith("```"):
        raw_output = raw_output.split("```", 2)[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(raw_output)
        suggestions = []
        for item in data:
            item.setdefault("file_path", file_path)
            suggestions.append(Suggestion(**item))
        return suggestions
    except Exception:
        return []
