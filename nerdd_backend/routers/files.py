import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from nerdd_link import FileSystem

__all__ = ["files_router"]

files_router = APIRouter(prefix="")


@files_router.get("/jobs/{job_id}/files/{property}/{record_id}")
async def get_job_file(
    job_id: str, property: str, record_id: str, request: Request = None
) -> FileResponse:
    app = request.app
    filesystem: FileSystem = app.state.filesystem

    path = filesystem.get_property_file_path(job_id, property, record_id)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path)
