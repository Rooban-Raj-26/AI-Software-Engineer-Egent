"""
Debugger Agent.
Reads the files flagged by the Reviewer's issue list, asks the LLM to
produce corrected versions, and writes them via the File Tool.
Reuses the "structured JSON in, files on disk out" pattern from the
Generator Agent, scoped only to files that have reported issues.
"""
import json
import re
from pathlib import Path
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.tools.file_tool import write_file

DEBUGGER_SYSTEM_PROMPT = """You are a senior software engineer fixing code issues.
You will be given file contents and a list of specific issues found during review.
Fix ONLY the issues described. Do not rewrite unrelated code or restructure the file.

Respond with ONLY a valid JSON array, no markdown formatting, no explanation.
Each element must be an object with exactly two keys:
- "filepath": the relative path of the fixed file (must match an input file)
- "content": the FULL corrected content of that file (not a diff/patch)

Example format:
[
  {"filepath": "app/database.py", "content": "<full fixed file content>"}
]
"""

MAX_FILE_CHARS = 4000


def _extract_json(raw_text: str) -> list:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _affected_files(review_report: list, project_root: str) -> list[Path]:
    """
    Maps issue['file'] entries (relative names like 'database.py' or
    'app/main.py') back to actual files on disk under project_root.
    """
    root = Path(project_root)
    flagged_names = {issue["file"] for issue in review_report if issue.get("severity") in ("critical", "warning")}

    matched = []
    for path in root.rglob("*"):
        if path.is_file() and any(path.name == name or str(path.relative_to(root)) == name for name in flagged_names):
            matched.append(path)
    return matched


def _build_fix_prompt(files: list[Path], review_report: list, project_root: str) -> str:
    root = Path(project_root)
    sections = []
    for path in files:
        relative = path.relative_to(root)
        content = path.read_text(encoding="utf-8")[:MAX_FILE_CHARS]
        sections.append(f"### File: {relative}\n```\n{content}\n```")

    issues_text = json.dumps(review_report, indent=2)

    return (
        f"{DEBUGGER_SYSTEM_PROMPT}\n\n"
        f"Issues found:\n{issues_text}\n\n"
        f"Files to fix:\n" + "\n\n".join(sections)
    )


async def debugger_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Reads flagged files + review_report, asks LLM to fix them, writes
    fixes to disk, increments retry_count.
    """
    provider = get_llm_provider()
    project_root = "generated_projects/current_run"

    files_to_fix = _affected_files(state["review_report"], project_root)

    if not files_to_fix:
        # Nothing matched (e.g. issue['file'] names didn't align with disk paths)
        return {"retry_count": state.get("retry_count", 0) + 1}

    prompt = _build_fix_prompt(files_to_fix, state["review_report"], project_root)
    raw_response = await provider.generate(prompt)

    try:
        fixes = _extract_json(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Debugger Agent did not return valid JSON: {e}\nRaw response: {raw_response[:500]}"
        )

    for fix in fixes:
        write_file(project_root, fix["filepath"], fix["content"])

    return {"retry_count": state.get("retry_count", 0) + 1}