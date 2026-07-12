"""
Temporary test endpoint to verify the LLM provider abstraction works.
This will be removed once the Planner Agent (Phase 3+) exercises
the same code path for real.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm.factory import get_llm_provider

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.post("/llm/test", tags=["LLM"])
async def test_llm(request: PromptRequest) -> dict:
    try:
        provider = get_llm_provider()
        result = await provider.generate(request.prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))