import os
from app.tools.base import BaseTool


class ReadFileTool(BaseTool):
    name = "read_file"
    description = (
        "Read the full content of a file at the given path. "
        "Returns the file content as a string, or an error message if the file does not exist."
    )

    def function(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found: {path}"
        except Exception as e:
            return f"Error reading file: {e}"


class ListDirectoryTool(BaseTool):
    name = "list_directory"
    description = (
        "List all Python (.py) files in a directory recursively. "
        "Returns newline-separated relative file paths."
    )

    def function(self, path: str) -> str:
        if not os.path.isdir(path):
            return f"Error: Not a directory: {path}"
        results = []
        for root, _, files in os.walk(path):
            for fname in sorted(files):
                if fname.endswith(".py"):
                    results.append(os.path.join(root, fname))
        if not results:
            return "No Python files found."
        return "\n".join(sorted(results))


class CreateFileTool(BaseTool):
    name = "create_file"
    description = (
        "Create a new file at the given path with the provided content. "
        "Creates parent directories if they do not exist."
    )

    def function(self, path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File created: {path}"
        except Exception as e:
            return f"Error creating file: {e}"
