"""
Shared state schema for the LangGraph agent workflow.
Every node reads from and writes to this same state object.
"""
from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    user_request: str
    plan: str
    generated_files: List[str]
    review_report: List[Dict[str, Any]]
    needs_fixes: bool
    retry_count: int   # tracks how many debugger passes have run, caps the loop