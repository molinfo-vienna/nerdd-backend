import asyncio
import json
import os
from io import BytesIO
from typing import List, Optional
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from nerdd_link import FileSystem

from ..data import RecordNotFoundError, Repository
from ..models import BaseSuccessResponse, Source, SourcePublic

__all__ = ["sources_router", "put_multiple_sources"]

sources_router = APIRouter(prefix="/sources")


@sources_router.put("")
async def put_source(
    file: UploadFile, format: Optional[str] = None, request: Request = None
) -> SourcePublic:
    app = request.app
    repository: Repository = app.state.repository
    filesystem: FileSystem = app.state.filesystem

    # create uuid
    uuid = uuid4()

    # create path to new file
    path = filesystem.get_source_file_path(str(uuid))

    # store file
    async with aiofiles.open(path, "wb") as out_file:
        while content := await file.read(10 * 1024 * 1024):  # read in 10MB chunks
            await out_file.write(content)

    # create media object
    source = Source(
        id=str(uuid),
        format=format,
        filename=file.filename,
    )
    source = await repository.create_source(source)

    return SourcePublic(**source.model_dump())


@sources_router.get("/{uuid}")
async def get_source(uuid: str, request: Request) -> SourcePublic:
    app = request.app
    repository: Repository = app.state.repository
    try:
        source = await repository.get_source_by_id(uuid)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Source not found") from e

    return SourcePublic(**source.model_dump())


@sources_router.delete("/{uuid}")
async def delete_source(uuid: str, request: Request) -> BaseSuccessResponse:
    app = request.app
    repository: Repository = app.state.repository
    filesystem: FileSystem = app.state.filesystem

    try:
        await repository.get_source_by_id(uuid)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Source not found") from e

    # delete file from disk
    path = filesystem.get_source_file_path(str(uuid))
    os.remove(path)

    # delete source from database
    await repository.delete_source_by_id(uuid)

    return BaseSuccessResponse(message="Source deleted successfully")


async def put_multiple_sources(
    inputs: List[str],
    sources: List[str],
    files: List[UploadFile],
    request: Request,
) -> SourcePublic:
    app = request.app
    repository: Repository = app.state.repository

    all_sources = []

    # create source from inputs list
    if len(inputs) > 0:

        async def _put_input(index: int, input: str):
            file_stream = BytesIO(input.encode("utf-8"))
            file = UploadFile(file_stream, filename=f"user_input_{index}")
            return await put_source(file=file, request=request)

        sources_from_inputs = await asyncio.gather(
            *[_put_input(i, input) for i, input in enumerate(inputs)]
        )
        all_sources += sources_from_inputs

    # create source from sources list
    for source_id in sources:
        try:
            source = await repository.get_source_by_id(source_id)
            all_sources.append(source)
        except RecordNotFoundError as e:
            raise HTTPException(status_code=404, detail=f"Source {source_id} not found") from e

    # create source from files list
    sources_from_files = await asyncio.gather(
        *[put_source(file=file, request=request) for file in files]
    )
    all_sources += sources_from_files

    # create one json file referencing all sources
    all_sources_objects = [source.model_dump() for source in all_sources]

    # create a merged file with all sources
    file_stream = BytesIO(json.dumps(jsonable_encoder(all_sources_objects)).encode("utf-8"))
    file = UploadFile(file_stream, filename=None)
    result_source = await put_source(file=file, format="json", request=request)

    return result_source
