import base64
import io
import math
import sys
from typing import List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from ..data import RecordNotFoundError, Repository
from ..models import ModuleInternal, ModulePublic, ModuleShort
from ..util import clamp

__all__ = ["modules_router"]

modules_router = APIRouter(prefix="/modules")


async def augment_module(module: ModuleInternal, request: Request, truncated=False) -> ModulePublic:
    config = request.app.state.config
    repository: Repository = request.app.state.repository

    # get output formats from config (if available)
    output_formats = config.get("output_formats", [])

    #
    # Compute maximum number of molecules allowed in a single job
    #

    # based on the user-defined maximum job duration in minutes
    max_job_duration_minutes = config.max_job_duration_minutes

    # We have to solve the following equation
    #  max_job_duration_minutes * 60
    #   >= startup_time_seconds * num_batches + num_molecules * seconds_per_molecule
    #   = startup_time_seconds * (num_molecules / batch_size) + num_molecules * seconds_per_molecule
    #   = num_molecules * (seconds_per_molecule + startup_time_seconds / batch_size)
    # This is an approximation, because num_batches is actually ceil(num_molecules / batch_size).
    # Rearranging gives:
    #   num_molecules <=
    #     max_job_duration_minutes * 60 / (seconds_per_molecule + startup_time_seconds / batch_size)
    seconds_per_molecule = module.seconds_per_molecule
    startup_time_seconds = module.startup_time_seconds
    batch_size = module.batch_size

    # We make sure that the denominator is not (close to) zero to avoid extremely large values.
    denominator = seconds_per_molecule + startup_time_seconds / batch_size
    if denominator <= 0.1:
        denominator = sys.float_info.epsilon

    max_num_molecules = clamp(
        int(max_job_duration_minutes * 60 / denominator),
        # there should be at least one molecule in a job
        1,
        # and at most the module's maximum number of molecules
        config.max_num_molecules_per_job,
    )

    # round down to a readable number
    if max_num_molecules >= 10_000:
        max_num_molecules = (max_num_molecules // 1_000) * 1_000
    elif max_num_molecules >= 1_000:
        max_num_molecules = (max_num_molecules // 100) * 100
    elif max_num_molecules >= 100:
        max_num_molecules = (max_num_molecules // 10) * 10

    #
    # Compute maximum number of molecules allowed in a checkpoint
    #

    # This computation is similar to the one above, but we assume a fixed duration of 30 minutes.
    # That is the amount of computation time we are losing at worst if a failure occurs during
    # processing of a checkpoint (since the checkpoint has to be recomputed).
    checkpoint_duration_minutes = 30
    checkpoint_size = clamp(
        int(checkpoint_duration_minutes * 60 / denominator),
        # there should be at least one molecule in a checkpoint
        1,
        # and at most the module's maximum number of molecules
        config.max_num_molecules_per_job,
    )

    #
    # Compute estimated waiting time
    #

    # skip this (slightly expensive) computation if we only want a truncated module representation
    if not truncated:
        active_jobs = await repository.get_jobs_by_status(["created", "processing"])
        active_jobs_of_module = [job for job in active_jobs if job.job_type == module.id]
        job_sizes = [
            job.num_entries_total if job.num_entries_total is not None else 10
            for job in active_jobs_of_module
        ]

        # the waiting time is an approximation for the following reasons:
        # * it doesn't consider the number of available workers
        # * it uses the total number of molecules in a job, not the remaining number
        waiting_time_per_job = [
            job_size * module.seconds_per_molecule
            + math.ceil(job_size / module.batch_size) * module.startup_time_seconds
            for job_size in job_sizes
        ]
        waiting_time_seconds = sum(waiting_time_per_job)
        waiting_time_minutes = math.ceil(waiting_time_seconds / 60)
    else:
        waiting_time_minutes = -1  # unknown

    return ModulePublic(
        **{
            **module.model_dump(),
            **dict(
                max_num_molecules=max_num_molecules,
                checkpoint_size=checkpoint_size,
                waiting_time_minutes=waiting_time_minutes,
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
        ModuleShort(**(await augment_module(module, request, truncated=True)).model_dump())
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

    return await augment_module(module, request)


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
