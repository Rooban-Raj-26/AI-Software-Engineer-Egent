"""
Builds and compiles the LangGraph agent workflow.
Currently: planner -> generator -> END.
Future phases will add Reviewer and Debugger nodes, along with
conditional edges (e.g., Reviewer -> Debugger loop on failure).
"""
from functools import lru_cache
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.planner_agent import planner_node
from app.agents.generator_agent import generator_node


@lru_cache
def get_compiled_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("generator", generator_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "generator")
    graph.add_edge("generator", END)

    return graph.compile()