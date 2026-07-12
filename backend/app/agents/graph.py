"""
Builds and compiles the LangGraph agent workflow.
Currently: planner -> generator -> reviewer -> (conditional) -> END.
If the Reviewer finds critical issues, the graph currently just ends
anyway (needs_fixes is reported but not yet acted on) — the actual
auto-fix loop back to a Debugger node is wired up in Phase 6.
"""
from functools import lru_cache
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.planner_agent import planner_node
from app.agents.generator_agent import generator_node
from app.agents.reviewer_agent import reviewer_node


def _route_after_review(state: AgentState) -> str:
    """
    Decides what happens after review. For now, both paths lead to END —
    this function exists now so Phase 6 only needs to change the mapping,
    not restructure the graph.
    """
    if state.get("needs_fixes"):
        return "needs_fixes"
    return "done"


@lru_cache
def get_compiled_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("generator", generator_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "generator")
    graph.add_edge("generator", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        _route_after_review,
        {
            "needs_fixes": END,  # Phase 6 will change this to point to "debugger"
            "done": END,
        },
    )

    return graph.compile()