import base64
import io
import math
from typing import List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from nerdd_module.config import Partner

from ..config import AppConfig
from ..data import RecordNotFoundError, Repository
from ..models import ModuleInternal, ModulePublic, ModuleShort, QueueStats
from ..util import clamp

__all__ = ["modules_router"]

modules_router = APIRouter(prefix="/modules")


def augment_module(request: Request | None, module: ModuleInternal) -> ModulePublic:
    if request is None:
        return ModulePublic(
            **module.model_dump(),
            module_url="",
            output_formats=[],
        )

    config: AppConfig = request.app.state.config

    # patch partner logo URLs
    partners = [
        Partner(
            **{
                **partner.model_dump(),
                **dict(
                    logo=str(
                        request.url_for(
                            "get_partner_logo",
                            module_id=module.id,
                            partner_id=i,
                        )
                    )
                ),
            },
        )
        for i, partner in enumerate(module.partners or [])
    ]

    return ModulePublic(**{
        **module.model_dump(),
        **dict(
            max_num_molecules=max_num_molecules,
            checkpoint_size=checkpoint_size,
            # logo is provided in a different route to speed up loading (and enable caching)
            logo=str(request.url_for("get_module_logo", module_id=module.id)),
            # partner logos are also provided in different routes
            partners=partners,
            output_formats=config.output_formats,
        ),
    })


@modules_router.get("")
async def get_modules(request: Request) -> List[ModuleShort]:
    app = request.app
    repository: Repository = app.state.repository

    modules = await repository.get_all_modules()
    return [
        ModuleShort(**augment_module(request, module).model_dump())
        for module in modules
        if module.visible
    ]


@modules_router.get("/{module_id}")
async def get_module(request: Request, module_id: str) -> ModulePublic:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    return augment_module(request, module)


@modules_router.get("/{module_id}/logo", include_in_schema=False)
async def get_module_logo(request: Request, module_id: str) -> StreamingResponse:
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
        with logo_path.open("rb") as f:
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


@modules_router.get("/{module_id}/partners/{partner_id}/logo", include_in_schema=False)
async def get_partner_logo(request: Request, module_id: str, partner_id: str) -> StreamingResponse:
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
        with logo_path.open("rb") as f:
            logo_data_decoded = f.read()
    elif not module.logo.startswith("data:"):
        raise HTTPException(status_code=400, detail="Module logo is not a valid base64 data URL")
    else:
        try:
            partner_index = int(partner_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Partner ID must be an integer") from e

        if partner_index < 0 or partner_index >= len(module.partners or []):
            raise HTTPException(status_code=404, detail="Partner not found")

        prefix, logo_data = module.partners[partner_index].logo.split(",")
        logo_data_decoded = base64.b64decode(logo_data)

    # figure out the mime type
    if prefix == "data:image/svg+xml;base64":
        mime_type = "image/svg+xml"
    else:
        # browsers can distinguish other formats (e.g., png, jpg) by the data itself
        mime_type = None

    return StreamingResponse(io.BytesIO(logo_data_decoded), media_type=mime_type)


@modules_router.get("/{module_id}/publications")
async def get_module_publications(request: Request, module_id: str) -> List[dict]:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    return module.processed_publications or []


@modules_router.get("/{module_id}/queue")
async def get_module_queue(request: Request, module_id: str) -> QueueStats:
    app = request.app
    repository: Repository = app.state.repository
    config: AppConfig = app.state.config

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    #
    # Compute estimated waiting time
    #

    # Fetch all jobs of this module (but use a limit to keep this route responsive)
    horizon = 100
    job_sizes = []
    estimate = "upper_bound"
    async for job in repository.get_jobs_by_status(module_id, ["created", "processing"]):
        job_sizes.append(
            max(job.num_entries_total - job.num_entries_processed, 0)
            if job.num_entries_total is not None
            else 10
        )

        if len(job_sizes) >= horizon:
            estimate = "lower_bound"
            break

    # the waiting time is still an approximation, because it doesn't consider the number of
    # available workers
    waiting_time_per_job = [
        job_size * module.seconds_per_molecule
        + math.ceil(job_size / module.batch_size) * module.startup_time_seconds
        for job_size in job_sizes
    ]
    waiting_time_seconds = sum(waiting_time_per_job)
    waiting_time_minutes = math.ceil(waiting_time_seconds / 60)

    #
    # Get remaining QueueStats parameters from the module configuration
    #
    max_num_molecules = module.max_num_molecules(
        config.max_job_duration_minutes,
        config.max_num_molecules_per_job,
    )
    checkpoint_size = module.checkpoint_size(
        config.max_job_duration_minutes,
        config.max_checkpoint_duration_minutes,
        config.max_num_molecules_per_job,
    )

    return QueueStats(
        module_id=module.id,
        num_active_jobs=len(job_sizes),
        waiting_time_minutes=waiting_time_minutes,
        estimate=estimate,
        seconds_per_molecule=module.seconds_per_molecule,
        startup_time_seconds=module.startup_time_seconds,
        max_num_molecules=max_num_molecules,
        checkpoint_size=checkpoint_size,
    )
