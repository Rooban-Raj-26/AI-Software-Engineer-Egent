"""
Shared state schema for the LangGraph agent workflow.
Every node reads from and writes to this same state object.
As new agents are added (Generator, Reviewer, Debugger...),
new keys get added here — never a new, separate state type.
"""
from typing import TypedDict


class AgentState(TypedDict):
    user_request: str        # the original request from the user
    plan: str                # output of the Planner Agent