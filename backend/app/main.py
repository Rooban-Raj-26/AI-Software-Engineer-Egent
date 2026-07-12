"""
Application entry point.
"""
from fastapi import FastAPI
from app.core.config import get_settings
from app.api.health import router as health_router
from app.api.llm_test import router as llm_test_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Autonomous multi-agent AI software engineering assistant.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(llm_test_router)

@app.get("/", tags=["System"])
async def root() -> dict:
    return {"message": f"{settings.app_name} is running."}