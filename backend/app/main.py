"""
Application entry point.
"""
from fastapi import FastAPI
from app.core.config import get_settings
from app.api.health import router as health_router
from app.api.planner import router as planner_router
from fastapi.middleware.cors import CORSMiddleware


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Autonomous multi-agent AI software engineering assistant.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(planner_router)

@app.get("/", tags=["System"])
async def root() -> dict:
    return {"message": f"{settings.app_name} is running."}