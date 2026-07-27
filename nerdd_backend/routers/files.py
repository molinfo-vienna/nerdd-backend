from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from nerdd_link import Storage

from ..util import AsyncStorageWrapper

__all__ = ["files_router"]

files_router = APIRouter(prefix="")


@files_router.get("/jobs/{job_id}/files/{property}/{record_id}", include_in_schema=False)
async def get_job_file(
    job_id: str, property: str, record_id: str, request: Request = None
) -> StreamingResponse:
    app = request.app
    storage: Storage = app.state.storage
    async_storage = AsyncStorageWrapper(storage)

    if not await async_storage.property_file_exists(job_id, property, record_id):
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(
        async_storage.iter_property_file_chunks(job_id, property, record_id, "rb"),
        media_type="application/octet-stream",
    )
