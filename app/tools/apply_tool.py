from app.tools.base import BaseTool


class ApplyChangesTool(BaseTool):
    name = "apply_changes"
    description = (
        "Apply a list of code changes to a file. Each change replaces lines "
        "line_start..line_end (1-indexed, inclusive) with suggested_code. "
        "Changes are applied bottom-up to preserve line indices."
    )

    def function(self, file_path: str, changes: list[dict]) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return f"Error: File not found: {file_path}"

        valid_changes = []
        for change in changes:
            s = change.get("line_start", 0)
            e = change.get("line_end", 0)
            if s < 1 or e < s or s > len(lines):
                continue
            valid_changes.append(change)

        # Apply bottom-up so earlier line numbers stay valid
        valid_changes.sort(key=lambda c: c["line_start"], reverse=True)

        applied_count = 0
        for change in valid_changes:
            start_idx = change["line_start"] - 1
            end_idx = change["line_end"]
            replacement_lines = change["suggested_code"].splitlines(keepends=True)
            # Ensure last replacement line ends with newline
            if replacement_lines and not replacement_lines[-1].endswith("\n"):
                replacement_lines[-1] += "\n"
            lines[start_idx:end_idx] = replacement_lines
            applied_count += 1

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return f"Applied {applied_count} change(s) to {file_path}"

    def apply_suggestions(self, file_path: str, suggestions: list) -> str:
        changes = [s.model_dump() for s in suggestions]
        return self.function(file_path=file_path, changes=changes)
