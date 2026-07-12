"""
Builds and compiles the LangGraph agent workflow.
Currently contains a single node (Planner). Future phases will add
Generator, Reviewer, and Debugger nodes here, along with conditional
edges (e.g., Reviewer -> Debugger loop on failure).
"""
from functools import lru_cache
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.planner_agent import planner_node


@lru_cache
def get_compiled_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", END)

    return graph.compile()