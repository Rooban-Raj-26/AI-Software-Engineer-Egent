"""
Application entry point.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.tools.file_tool import FileToolError
from app.tools.terminal_tool import TerminalToolError
from app.api.health import router as health_router
from app.api.planner import router as planner_router

configure_logging()
logger = logging.getLogger(__name__)

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


@app.exception_handler(FileToolError)
@app.exception_handler(TerminalToolError)
async def tool_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Tool error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"A tool operation failed: {str(exc)}"},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Check server logs for details."},
    )


app.include_router(health_router)
app.include_router(planner_router)


@app.get("/", tags=["System"])
async def root() -> dict:
    logger.info("Root endpoint hit")
    return {"message": f"{settings.app_name} is running."}