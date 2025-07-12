from fastapi import APIRouter, HTTPException, Request

from ..data import RecordNotFoundError, Repository
from ..models import Module, ModulePublic, ModuleShort

__all__ = ["modules_router"]

modules_router = APIRouter(prefix="/modules")


def augment_module(module: Module, request: Request) -> ModulePublic:
    return ModulePublic(
        **module.model_dump(),
        module_url=str(request.url_for("get_module", module_id=module.id)),
    )


@modules_router.get("")
async def get_modules(request: Request):
    app = request.app
    repository: Repository = app.state.repository

    modules = await repository.get_all_modules()
    return [
        ModuleShort(**augment_module(module, request).model_dump())
        for module in modules
        if module.visible
    ]


@modules_router.get("/{module_id}")
async def get_module(module_id: str, request: Request):
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    return augment_module(module, request)
