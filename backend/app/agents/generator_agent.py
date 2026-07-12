"""
Code Generator Agent.
Takes the Planner's output and the original user request, asks the LLM
to produce structured file contents (JSON), then writes each file to
disk using the File Tool.
"""
import json
import re
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.tools.file_tool import write_file, ensure_project_dir

GENERATOR_SYSTEM_PROMPT = """You are a senior software engineer.
Given a development plan, generate the actual source code files needed.

Respond with ONLY a valid JSON array, no markdown formatting, no explanation.
Each element must be an object with exactly two keys:
- "filepath": a relative path like "app/main.py"
- "content": the full text content of that file

Example format:
[
  {"filepath": "app/main.py", "content": "print('hello')"},
  {"filepath": "requirements.txt", "content": "fastapi\\n"}
]

Generate complete, working code for every file mentioned in the plan.
"""

OUTPUT_BASE_DIR = "generated_projects"


def _extract_json(raw_text: str) -> list:
    """
    LLMs sometimes wrap JSON in markdown code fences despite instructions.
    This strips ```json ... ``` fences if present before parsing.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


async def generator_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Reads state['plan'], generates code, writes files, returns file list.
    """
    provider = get_llm_provider()
    full_prompt = f"{GENERATOR_SYSTEM_PROMPT}\n\nDevelopment plan:\n{state['plan']}"

    raw_response = await provider.generate(full_prompt)

    try:
        files = _extract_json(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Generator Agent did not return valid JSON: {e}\nRaw response: {raw_response[:500]}"
        )

    project_dir = ensure_project_dir(OUTPUT_BASE_DIR, "current_run")

    written_paths = []
    for file_entry in files:
        path = write_file(project_dir, file_entry["filepath"], file_entry["content"])
        written_paths.append(path)

    return {"generated_files": written_paths}