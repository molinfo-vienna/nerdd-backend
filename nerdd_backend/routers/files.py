from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from nerdd_link import FileSystem

__all__ = ["files_router"]

files_router = APIRouter(prefix="")


@files_router.get("/jobs/{job_id}/files/{property}/{record_id}", include_in_schema=False)
async def get_job_file(
    job_id: str, property: str, record_id: str, request: Request = None
) -> FileResponse:
    app = request.app
    filesystem: FileSystem = app.state.filesystem

    path = filesystem.get_property_file_path(job_id, property, record_id)

    # for security reasons, we check if the returned path is really in jobs dir
    jobs_dir = filesystem.get_jobs_dir()
    resolved_path = Path(path).resolve()

    if not resolved_path.is_relative_to(jobs_dir):
        raise HTTPException(status_code=403, detail="Access to this file is forbidden")

    if not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(resolved_path)
