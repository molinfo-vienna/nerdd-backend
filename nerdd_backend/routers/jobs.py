import logging
import math
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Header, HTTPException, Request
from fastapi.responses import FileResponse
from nerdd_link import Channel, FileSystem, JobMessage, Tombstone

from ..data import RecordNotFoundError, Repository
from ..models import (
    BaseSuccessResponse,
    JobCreate,
    JobInternal,
    JobPublic,
    JobWithResults,
    OutputFile,
)
from .users import check_quota, get_user

__all__ = ["jobs_router"]

logger = logging.getLogger(__name__)

jobs_router = APIRouter(prefix="/jobs")


async def augment_job(job: JobWithResults, request: Request) -> JobPublic:
    # The number of processed pages is only valid if the computation has not finished yet. We adapt
    # this number in the if statement below.
    num_pages_processed = job.num_entries_processed // job.page_size
    if job.num_entries_total is not None:
        num_pages_total = math.ceil(job.num_entries_total / job.page_size)

        if job.num_entries_total == job.num_entries_processed:
            num_pages_processed = num_pages_total
    else:
        num_pages_total = None

    # get output files
    output_files = [
        OutputFile(
            format=output_format,
            url=str(request.url_for("get_output_file", job_id=job.id, format=output_format)),
        )
        for output_format in job.output_formats
    ]

    return JobPublic(
        **job.model_dump(),
        job_url=str(request.url_for("get_job", job_id=job.id)),
        results_url=str(request.url_for("get_results", job_id=job.id)),
        num_pages_processed=num_pages_processed,
        num_pages_total=num_pages_total,
        output_files=output_files,
    )


@jobs_router.post("")
async def create_job(
    job: JobCreate = Body(),
    referer: Optional[str] = Header(None, include_in_schema=False),
    request: Request = None,
) -> JobPublic:
    app = request.app
    repository: Repository = app.state.repository
    channel: Channel = app.state.channel

    # create a job id
    job_id = uuid4()

    # get user from request and check quota
    user = await get_user(request)
    await check_quota(user, request)

    # check if module exists
    try:
        module = await repository.get_module_by_id(job.job_type)
    except RecordNotFoundError as e:
        all_modules = await repository.get_all_modules()
        valid_options = [module.id for module in all_modules]
        raise HTTPException(
            status_code=404,
            detail=(
                f"Module {job.job_type} not found. Valid options are: {', '.join(valid_options)}"
            ),
        ) from e

    # check module parameters
    try:
        module.validate_job_parameters(job.params)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid parameters for module {job.job_type}: {str(e)}",
        ) from e

    # add default values for optional parameters
    for job_parameter in module.job_parameters:
        if job_parameter.name not in job.params:
            if job_parameter.default is not None:
                job.params[job_parameter.name] = job_parameter.default

    # get page size (depending on module task)
    task = module.task
    if task == "atom_property_prediction":
        page_size = app.state.config.page_size_atom_property_prediction
    elif task == "derivative_property_prediction":
        page_size = app.state.config.page_size_derivative_property_prediction
    else:
        # task == "molecular_property_prediction" or unknown task
        page_size = app.state.config.page_size_molecular_property_prediction

    # check if source exists
    try:
        await repository.get_source_by_id(job.source_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Source not found") from e

    job_new = JobInternal(
        id=str(job_id),
        user_id=user.id,
        referer=referer,
        job_type=job.job_type,
        source_id=job.source_id,
        params=job.params,
        page_size=page_size,
        status="created",
    )

    # We have to create the job in the database now, because the user will fetch the created job
    # in the next request. There is no time for sending it to Kafka and consuming the job record.
    job_with_results = await repository.create_job(job_new)

    try:
        # send job to kafka
        await channel.jobs_topic().send(
            JobMessage(
                id=str(job_id),
                # user_id=user.id,
                job_type=job.job_type,
                source_id=job.source_id,
                params=job.params,
            )
        )
    except Exception as e:
        # if sending the job to Kafka fails, we delete the job from the database
        try:
            await repository.delete_job_by_id(str(job_id))
        except RecordNotFoundError:
            pass  # ignore if something goes wrong
        except Exception as inner:
            logger.exception(
                f"Failed to delete job {job_id} from database after failure in Kafka send", inner
            )
        raise HTTPException(
            status_code=500,
            detail="Failed to send job to processing queue. Please try again later.",
        ) from e

    # return the response
    return await augment_job(job_with_results, request)


@jobs_router.delete("/{job_id}")
async def delete_job(job_id: str, request: Request) -> BaseSuccessResponse:
    app = request.app
    repository: Repository = app.state.repository
    channel: Channel = app.state.channel

    try:
        job = await repository.get_job_by_id(job_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Job not found") from e

    # delete only the job instance to prevent future access
    await repository.delete_job_by_id(job_id)

    # send tombstone message on jobs topic (DeleteJob action will take care of the rest)
    await channel.jobs_topic().send(Tombstone(JobMessage, id=job_id, job_type=job.job_type))

    return BaseSuccessResponse(message="Job deleted successfully")


@jobs_router.get("/{job_id}/output.{format}")
async def get_output_file(job_id: str, format: str, request: Request) -> FileResponse:
    app = request.app
    repository = app.state.repository
    config = app.state.config
    filesystem: FileSystem = app.state.filesystem

    try:
        job = await repository.get_job_by_id(job_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Job not found") from e

    if format not in config.output_formats:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Format {format} not supported. "
                f"Valid options are: {', '.join(config.output_formats)}"
            ),
        )

    if format not in job.output_formats:
        raise HTTPException(
            status_code=202,
            detail=(
                "Output format not available yet. Please wait until the computation is finished."
            ),
        )

    filepath = filesystem.get_output_file(job_id, format)
    return FileResponse(filepath, filename=f"{job.job_type}-{job_id}.{format}")


@jobs_router.get("/{job_id}")
async def get_job(job_id: str, request: Request) -> JobPublic:
    app = request.app
    repository = app.state.repository

    try:
        job = await repository.get_job_by_id(job_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Job not found") from e

    return await augment_job(job, request)
