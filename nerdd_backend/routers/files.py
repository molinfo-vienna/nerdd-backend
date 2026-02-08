import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from nerdd_link import Storage

__all__ = ["files_router"]

files_router = APIRouter(prefix="")


@files_router.get("/jobs/{job_id}/files/{property}/{record_id}", include_in_schema=False)
async def get_job_file(
    job_id: str, property: str, record_id: str, request: Request = None
) -> StreamingResponse:
    app = request.app
    storage: Storage = app.state.storage

    path = storage.get_property_file_path(job_id, property, record_id)
    if not await asyncio.to_thread(storage.file_exists, path):
        raise HTTPException(status_code=404, detail="File not found")

    file_handle = await asyncio.to_thread(
        storage.get_property_file_handle, job_id, property, record_id, "rb"
    )

    async def async_file_iterator(chunk_size: int = 65536) -> AsyncGenerator[bytes, None]:
        try:
            while chunk := await asyncio.to_thread(file_handle.read, chunk_size):
                yield chunk
        finally:
            await asyncio.to_thread(file_handle.close)

    return StreamingResponse(
        async_file_iterator(),
        media_type="application/octet-stream",
    )
