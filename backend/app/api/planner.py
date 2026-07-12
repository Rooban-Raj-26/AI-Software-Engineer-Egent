"""
Endpoint to trigger the agent workflow (currently just the Planner).
Replaces the temporary /llm/test endpoint from Phase 2.
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
        result = await graph.ainvoke({"user_request": request.user_request, "plan": ""})
        return {"plan": result["plan"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))