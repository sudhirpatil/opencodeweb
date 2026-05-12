from langchain_core.tools import tool


def _patch_file(file_path: str, changes: list[dict]) -> str:
    """Core patching logic shared by the LLM tool and the API helper."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"

    valid_changes = [
        c for c in changes
        if c.get("line_start", 0) >= 1
        and c.get("line_end", 0) >= c.get("line_start", 0)
        and c.get("line_start", 0) <= len(lines)
    ]

    # Apply bottom-up so earlier line numbers stay valid
    valid_changes.sort(key=lambda c: c["line_start"], reverse=True)

    for change in valid_changes:
        start_idx = change["line_start"] - 1
        end_idx = change["line_end"]
        replacement = change["suggested_code"].splitlines(keepends=True)
        if replacement and not replacement[-1].endswith("\n"):
            replacement[-1] += "\n"
        lines[start_idx:end_idx] = replacement

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return f"Applied {len(valid_changes)} change(s) to {file_path}"


@tool
def apply_changes(file_path: str, changes: list[dict]) -> str:
    """Apply a list of code changes to a file. Each change must have line_start, line_end
    (1-indexed, inclusive), and suggested_code. Changes are applied bottom-up to preserve
    line indices."""
    return _patch_file(file_path, changes)


def apply_suggestions(file_path: str, suggestions: list) -> str:
    """Convenience helper called directly by the /apply API route (not the LLM).
    Accepts Suggestion model instances and delegates to _patch_file."""
    changes = [s.model_dump() for s in suggestions]
    return _patch_file(file_path, changes)
