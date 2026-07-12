"""
File Tool.
A narrow, reusable utility for safely writing files and folders to disk.
Used by the Code Generator Agent now, and later by the Debugger Agent
(to patch files) and Documentation Agent (to write the README).

This tool has no knowledge of LLMs, agents, or plans — it only writes
what it's told, with guardrails against unsafe paths.
"""
import os
from pathlib import Path


class FileToolError(Exception):
    """Raised when a file operation is unsafe or fails."""


def _ensure_safe_path(base_dir: Path, relative_path: str) -> Path:
    """
    Resolves relative_path against base_dir and guarantees the result
    stays inside base_dir. Blocks path traversal like '../../etc/passwd'.
    """
    target = (base_dir / relative_path).resolve()
    base_resolved = base_dir.resolve()

    if not str(target).startswith(str(base_resolved)):
        raise FileToolError(f"Unsafe path rejected: {relative_path}")

    return target


def write_file(base_dir: str, relative_path: str, content: str) -> str:
    """
    Writes `content` to `base_dir/relative_path`, creating any
    intermediate directories as needed. Returns the absolute path written.
    """
    base = Path(base_dir)
    target = _ensure_safe_path(base, relative_path)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return str(target)


def ensure_project_dir(base_dir: str, project_name: str) -> str:
    """
    Creates (if missing) and returns the path to a project's output folder.
    """
    project_path = Path(base_dir) / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return str(project_path)