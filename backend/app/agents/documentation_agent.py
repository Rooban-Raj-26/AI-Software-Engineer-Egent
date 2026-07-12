"""
Documentation Agent.
Uses the original plan and the list of generated files (already known,
structured facts) to write a real README.md for the generated project.
"""
from pathlib import Path
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.tools.file_tool import write_file

DOC_SYSTEM_PROMPT = """You are a technical writer producing a professional README.

You will be given a development plan and a list of files that were generated
for this project. Write a complete README.md in Markdown format covering:
- Project title and one-paragraph description
- Features
- Project structure (brief)
- Setup instructions (venv, install dependencies, run command)
- API usage notes if applicable

Respond with ONLY the raw Markdown content of the README — no code fences,
no explanation, no commentary before or after.
"""

PROJECT_ROOT = "generated_projects/current_run"


def _file_list_summary(file_paths: list[str], project_root: str) -> str:
    root = Path(project_root)
    names = []
    for path_str in file_paths:
        try:
            names.append(str(Path(path_str).relative_to(root)))
        except ValueError:
            names.append(Path(path_str).name)
    return "\n".join(f"- {name}" for name in names)


async def documentation_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Reads state['plan'] and state['generated_files'], writes README.md.
    """
    provider = get_llm_provider()

    file_summary = _file_list_summary(state["generated_files"], PROJECT_ROOT)
    prompt = (
        f"{DOC_SYSTEM_PROMPT}\n\n"
        f"Development plan:\n{state['plan']}\n\n"
        f"Generated files:\n{file_summary}"
    )

    readme_content = await provider.generate(prompt)

    write_file(PROJECT_ROOT, "README.md", readme_content)

    return {"readme_content": readme_content}