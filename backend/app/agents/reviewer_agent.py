"""
Reviewer Agent.
Reads all files generated so far, sends their contents to the LLM for
critique, and produces a structured list of issues (severity, file,
description). Does not fix anything itself — that's the Debugger
Agent's job (Phase 6). This agent only judges.
"""
import json
import re
from pathlib import Path
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

REVIEWER_SYSTEM_PROMPT = """You are a senior code reviewer.
You will be given the contents of several source files from one project.
Review them for correctness, security issues, and maintainability.

Respond with ONLY a valid JSON array, no markdown formatting, no explanation.
Each element must be an object with exactly three keys:
- "file": relative filepath the issue applies to
- "severity": one of "critical", "warning", "info"
- "description": a short, specific description of the issue

If there are no issues at all, return an empty array: []
"""

MAX_FILE_CHARS = 4000  # keep review prompt reasonably sized


def _extract_json(raw_text: str) -> list:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _build_review_prompt(file_paths: list[str], project_root: str) -> str:
    root = Path(project_root)
    sections = []
    for path_str in file_paths:
        path = Path(path_str)
        try:
            relative = path.relative_to(root)
        except ValueError:
            relative = path.name

        try:
            content = path.read_text(encoding="utf-8")[:MAX_FILE_CHARS]
        except Exception:
            content = "<could not read file>"

        sections.append(f"### File: {relative}\n```\n{content}\n```")

    return REVIEWER_SYSTEM_PROMPT + "\n\n" + "\n\n".join(sections)


async def reviewer_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Reads state['generated_files'], reviews them, returns issues + a flag.
    """
    provider = get_llm_provider()
    project_root = "generated_projects/current_run"

    prompt = _build_review_prompt(state["generated_files"], project_root)
    raw_response = await provider.generate(prompt)

    try:
        issues = _extract_json(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Reviewer Agent did not return valid JSON: {e}\nRaw response: {raw_response[:500]}"
        )

    has_critical = any(issue.get("severity") == "critical" for issue in issues)

    return {
        "review_report": issues,
        "needs_fixes": has_critical,
    }