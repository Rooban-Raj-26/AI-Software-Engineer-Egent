"""
Endpoint to trigger the agent workflow:
Planner -> Generator -> Reviewer -> (Debugger loop) -> done.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.graph import get_compiled_graph

router = APIRouter()


class PlanRequest(BaseModel):
    user_request: str


@router.post("/agents/plan", tags=["Agents"])
async def create_plan(request: PlanRequest) -> dict:
    try:
        graph = get_compiled_graph()
        result = await graph.ainvoke({
            "user_request": request.user_request,
            "plan": "",
            "generated_files": [],
            "review_report": [],
            "needs_fixes": False,
            "retry_count": 0,
        })
        return {
            "plan": result["plan"],
            "generated_files": result["generated_files"],
            "review_report": result["review_report"],
            "needs_fixes": result["needs_fixes"],
            "retry_count": result["retry_count"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))