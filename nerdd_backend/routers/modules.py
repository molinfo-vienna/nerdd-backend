import base64
import math
from functools import lru_cache
from typing import List

from fastapi import HTTPException, Request
from fastapi.responses import Response
from nerdd_module.config import Partner

from ..config import AppConfig
from ..data import RecordNotFoundError, Repository
from ..models import ModuleInternal, ModulePublic, ModuleShort, QueueStats
from ..util import ContentHashedAPIRouter

__all__ = ["modules_router"]

modules_router = ContentHashedAPIRouter(prefix="/modules")


@lru_cache(maxsize=1_024)
def _get_data_url_logo_asset(logo: str) -> tuple[bytes, str | None]:
    if not logo.startswith("data:"):
        raise HTTPException(status_code=400, detail="Module logo is not a valid base64 data URL")

    prefix, logo_data = logo.split(",", maxsplit=1)
    logo_data_decoded = base64.b64decode(logo_data)

    # browsers can distinguish non-SVG formats (e.g., png, jpg) by their contents
    mime_type = "image/svg+xml" if prefix == "data:image/svg+xml;base64" else None
    return logo_data_decoded, mime_type


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
                        modules_router.content_hashed_url_for(
                            request,
                            "get_partner_logo",
                            _get_data_url_logo_asset(partner.logo)[0],
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
            logo=str(
                modules_router.content_hashed_url_for(
                    request,
                    "get_module_logo",
                    _get_data_url_logo_asset(module.logo)[0],
                    module_id=module.id,
                )
            ),
            partners=partners,
            module_url=str(request.url_for("get_module", module_id=module.id)),
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


@modules_router.content_hashed_get("/{module_id}/logo", include_in_schema=False)
async def get_module_logo(request: Request, module_id: str) -> Response:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    logo_data, mime_type = _get_data_url_logo_asset(module.logo)
    return Response(content=logo_data, media_type=mime_type)


@modules_router.content_hashed_get(
    "/{module_id}/partners/{partner_id}/logo", include_in_schema=False
)
async def get_partner_logo(request: Request, module_id: str, partner_id: str) -> Response:
    app = request.app
    repository: Repository = app.state.repository

    try:
        module = await repository.get_module_by_id(module_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e

    try:
        partner_index = int(partner_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Partner ID must be an integer") from e

    if partner_index < 0 or partner_index >= len(module.partners or []):
        raise HTTPException(status_code=404, detail="Partner not found")

    logo_data, mime_type = _get_data_url_logo_asset(module.partners[partner_index].logo)
    return Response(content=logo_data, media_type=mime_type)


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
