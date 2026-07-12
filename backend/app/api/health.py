"""
Health check endpoint.
Used later by Docker HEALTHCHECK, CI pipelines, and deployment platforms
(Render/Railway) to confirm the service is alive.
"""
from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter()


@router.get("/health", tags=["System"])
async def health_check() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }