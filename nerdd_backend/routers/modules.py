import base64
import io
from typing import List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from ..data import RecordNotFoundError, Repository
from ..models import ModuleInternal, ModulePublic, ModuleShort

__all__ = ["modules_router"]

modules_router = APIRouter(prefix="/modules")


def augment_module(module: ModuleInternal, request: Request) -> ModulePublic:
    config = request.app.state.config

    output_formats = config.get("output_formats", [])

    return ModulePublic(
        **{
            **module.model_dump(),
            **dict(
                # logo is provided in a different route to speed up loading (and enable caching)
                logo=None,
                module_url=str(request.url_for("get_module", module_id=module.id)),
                output_formats=output_formats,
            ),
        }
    )


@modules_router.get("")
async def get_modules(request: Request) -> List[ModuleShort]:
    app = request.app
    repository: Repository = app.state.repository

    modules = await repository.get_all_modules()
    return [
        ModuleShort(**augment_module(module, request).model_dump())
        for module in modules
        if module.visible
    ]


@modules_router.get("/{module_id}")
async def get_module(module_id: str, request: Request) -> ModulePublic:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    return augment_module(module, request)


@modules_router.get("/{module_id}/logo", include_in_schema=False)
async def get_module_logo(module_id: str, request: Request) -> StreamingResponse:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    if module.logo is None:
        import importlib.resources

        prefix = "data:image/svg+xml;base64,"
        logo_path = importlib.resources.files("assets").joinpath("default_logo.svg")
        with open(logo_path, "rb") as f:
            logo_data_decoded = f.read()
    elif not module.logo.startswith("data:"):
        raise HTTPException(status_code=400, detail="Module logo is not a valid base64 data URL")
    else:
        prefix, logo_data = module.logo.split(",")
        logo_data_decoded = base64.b64decode(logo_data)

    # figure out the mime type
    if prefix == "data:image/svg+xml;base64":
        mime_type = "image/svg+xml"
    else:
        # browsers can distinguish other formats (e.g., png, jpg) by the data itself
        mime_type = None

    return StreamingResponse(io.BytesIO(logo_data_decoded), media_type=mime_type)
