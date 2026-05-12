import json
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from app.config import settings
from app.models.suggestion import Suggestion
from app.tools.file_tools import ReadFileTool, ListDirectoryTool, CreateFileTool
from app.tools.analysis_tool import AnalyzePySparkCodeTool, set_rules
from app.tools.apply_tool import ApplyChangesTool
from app.agent.prompts import build_system_prompt, get_rules_content


def _build_langchain_tools() -> list:
    tool_instances = [
        ReadFileTool(),
        ListDirectoryTool(),
        AnalyzePySparkCodeTool(),
        ApplyChangesTool(),
        CreateFileTool(),
    ]
    return [t.to_langchain_tool() for t in tool_instances]


def _build_agent(system_prompt: str):
    llm = ChatAnthropic(
        model=settings.model_name,
        api_key=settings.anthropic_api_key,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )
    tools = _build_langchain_tools()
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )


async def run_analysis(file_path: str, rules_prompt_path: str) -> list[Suggestion]:
    system_prompt = build_system_prompt(rules_prompt_path)
    rules_content = get_rules_content(rules_prompt_path)

    # Make rules available to AnalyzePySparkCodeTool without passing through LLM
    set_rules(rules_content)

    agent = _build_agent(system_prompt)

    task_message = (
        f"Analyze the PySpark file at: {file_path}\n"
        f"Call the analyze_pyspark_code tool with file_path='{file_path}'. "
        f"Return the JSON array result verbatim — no other text."
    )

    result = await agent.ainvoke({"messages": [HumanMessage(content=task_message)]})

    # Extract last AI message content
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
