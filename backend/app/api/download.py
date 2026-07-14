"""
Endpoint to download the most recently generated project as a ZIP file.
Zips generated_projects/current_run/ on the fly and streams it back.
"""
import shutil
import tempfile
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

PROJECT_ROOT = "generated_projects/current_run"


@router.get("/agents/download", tags=["Agents"])
async def download_generated_project():
    project_path = Path(PROJECT_ROOT)

    if not project_path.exists() or not any(project_path.iterdir()):
        raise HTTPException(status_code=404, detail="No generated project found. Run the pipeline first.")

    tmp_dir = tempfile.mkdtemp()
    zip_base_path = os.path.join(tmp_dir, "generated_project")

    zip_path = shutil.make_archive(zip_base_path, "zip", root_dir=str(project_path))

    return FileResponse(
        path=zip_path,
        filename="generated_project.zip",
        media_type="application/zip",
    )