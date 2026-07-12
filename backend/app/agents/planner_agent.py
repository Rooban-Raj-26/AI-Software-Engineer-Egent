"""
Planner Agent.
Takes the user's raw software request and produces a structured,
step-by-step development plan using the LLM provider abstraction.
"""
from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

PLANNER_SYSTEM_PROMPT = """You are a senior software architect.
Given a user's software request, produce a clear, numbered, step-by-step
development plan. Include: key features, suggested file/folder structure,
and the order in which components should be built. Be concise but complete.
"""


async def planner_node(state: AgentState) -> AgentState:
    """
    LangGraph node function.
    Receives the current state, calls the LLM, returns state updates.
    """
    provider = get_llm_provider()
    full_prompt = f"{PLANNER_SYSTEM_PROMPT}\n\nUser request:\n{state['user_request']}"

    plan_text = await provider.generate(full_prompt)

    return {"plan": plan_text}