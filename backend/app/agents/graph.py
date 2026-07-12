"""
Builds and compiles the LangGraph agent workflow.
Flow: planner -> generator -> reviewer -> (loop w/ debugger until done)
      -> documentation -> git -> END.
"""
from functools import lru_cache
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.planner_agent import planner_node
from app.agents.generator_agent import generator_node
from app.agents.reviewer_agent import reviewer_node
from app.agents.debugger_agent import debugger_node
from app.agents.documentation_agent import documentation_node
from app.agents.git_agent import git_node

MAX_RETRIES = 3


def _route_after_review(state: AgentState) -> str:
    if state.get("needs_fixes") and state.get("retry_count", 0) < MAX_RETRIES:
        return "needs_fixes"
    return "done"


@lru_cache
def get_compiled_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("generator", generator_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("debugger", debugger_node)
    graph.add_node("documentation", documentation_node)
    graph.add_node("git", git_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "generator")
    graph.add_edge("generator", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        _route_after_review,
        {
            "needs_fixes": "debugger",
            "done": "documentation",
        },
    )

    graph.add_edge("debugger", "reviewer")
    graph.add_edge("documentation", "git")
    graph.add_edge("git", END)

    return graph.compile()