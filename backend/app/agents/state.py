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
    retry_count: int
    readme_content: str      # output of the Documentation Agent
    commit_message: str      # output of the Git Agent