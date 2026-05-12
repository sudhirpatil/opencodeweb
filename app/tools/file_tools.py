import os
from langchain_core.tools import tool


@tool
def read_file(path: str) -> str:
    """Read the full content of a file at the given path.
    Returns the file content as a string, or an error message if the file does not exist."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def list_directory(path: str) -> str:
    """List all Python (.py) files in a directory recursively.
    Returns newline-separated file paths."""
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


@tool
def create_file(path: str, content: str) -> str:
    """Create a new file at the given path with the provided content.
    Creates parent directories if they do not exist."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File created: {path}"
    except Exception as e:
        return f"Error creating file: {e}"
