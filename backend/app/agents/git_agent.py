"""
Git Agent.
Generates a meaningful commit message by summarizing the plan and file
list (LLM call), then initializes a local git repo inside the generated
project folder and makes the first commit (Terminal Tool, no LLM needed).
"""
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider
from app.tools.terminal_tool import run_command, TerminalToolError

GIT_MESSAGE_PROMPT = """You are a senior engineer writing a git commit message.
Given a development plan summary, write ONE concise commit message following
the Conventional Commits format (e.g. "feat: add todo CRUD API with SQLite").

Respond with ONLY the single-line commit message, no quotes, no explanation.
"""

PROJECT_ROOT = "generated_projects/current_run"


async def git_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Generates a commit message, then runs git init/add/commit locally.
    """
    provider = get_llm_provider()

    prompt = f"{GIT_MESSAGE_PROMPT}\n\nPlan summary:\n{state['plan'][:1000]}"
    commit_message = (await provider.generate(prompt)).strip()

    try:
        run_command(["git", "init"], cwd=PROJECT_ROOT)
        run_command(["git", "add", "."], cwd=PROJECT_ROOT)
        run_command(["git", "-c", "user.email=agent@local", "-c", "user.name=AI Software Engineer Agent",
                     "commit", "-m", commit_message], cwd=PROJECT_ROOT)
    except TerminalToolError as e:
        # Non-fatal: still return the commit message even if git isn't
        # available on this machine, so the pipeline doesn't hard-fail.
        return {"commit_message": f"{commit_message} (git init skipped: {e})"}

    return {"commit_message": commit_message}