_SYSTEM_PROMPT_TEMPLATE = """\
You are an expert PySpark code reviewer. Your job is to analyze PySpark Python files \
and generate precise, actionable suggestions to improve code quality, performance, and correctness.

## Rules for Analysis
{rules_content}

## Your Workflow
1. Use `read_file` to read the target PySpark file.
2. Use `analyze_pyspark_code` with the file_path and the rules text above to extract structured suggestions.
3. After calling `analyze_pyspark_code`, output its JSON result verbatim as your final response. \
   Do NOT add any other text around it.

## Output Format
Your final response must be a valid JSON array of suggestion objects only.
"""


def build_system_prompt(rules_prompt_path: str) -> str:
    with open(rules_prompt_path, "r", encoding="utf-8") as f:
        rules_content = f.read()
    return _SYSTEM_PROMPT_TEMPLATE.format(rules_content=rules_content)


def get_rules_content(rules_prompt_path: str) -> str:
    with open(rules_prompt_path, "r", encoding="utf-8") as f:
        return f.read()
