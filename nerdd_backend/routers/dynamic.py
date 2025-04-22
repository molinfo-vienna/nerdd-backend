import json
import logging
from typing import List, Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Header,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from pydantic import create_model, model_validator
from stringcase import pascalcase

from ..models import JobCreate, Module
from .jobs import create_job, delete_job, get_job
from .results import get_results
from .sources import put_multiple_sources
from .websockets import get_job_ws, get_results_ws

__all__ = ["get_dynamic_router"]

logger = logging.getLogger(__name__)


type_mapping = {
    "text": str,
    "bool": bool,
    "small_integer": int,
    "float": float,
    "positive_integer": int,
    "positive_small_integer": int,
    "integer": int,
    "image": str,
}


def get_query_param(job_parameter):
    requested_type = job_parameter.type
    actual_type = type_mapping.get(requested_type, str)
    default_value = job_parameter.default or None
    return (actual_type, default_value)


def validate_to_json(cls, value):
    if isinstance(value, str):
        return cls(**json.loads(value))
    return value


def get_dynamic_router(module: Module):
    logger.info(f"Creating router for module {module.id}")

    # all methods will be available at /module_name e.g. /cypstrate
    # the parameter tags creates a separate group in the swagger ui
    # module will be hidden if visible is set to False
    router = APIRouter(tags=[module.id], include_in_schema=module.visible)

    field_definitions = dict(
        **{p.name: get_query_param(p) for p in module.job_parameters},
    )
    module_name = pascalcase(module.id)
    QueryModelGet = create_model(
        f"{module_name}JobCreate",
        **field_definitions,
    )
    QueryModelPost = create_model(
        f"{module_name}ComplexJobCreate",
        __validators__={"validate_to_json": model_validator(mode="before")(validate_to_json)},
        inputs=(List[str], []),
        sources=(List[str], []),
        **field_definitions,
    )

    #
    # GET /jobs
    # query parameters:
    #   - input: list of strings (SMILES, InCHI)
    #   - all params from module (e.g. metabolism_phase)
    #
    async def _create_job(
        inputs: List[str],
        sources: List[str],
        files: List[UploadFile],
        params: dict,
        referer: Optional[str] = None,
        request: Request = None,
    ):
        if "job_type" in params and params["job_type"] != module.id:
            raise HTTPException(
                status_code=400,
                detail="job_type was specified, but it does not match the module name",
            )

        if len(inputs) == 0 and len(sources) == 0 and len(files) == 0:
            raise HTTPException(
                status_code=400,
                detail="At least one input or source must be provided",
            )

        result_source = await put_multiple_sources(inputs, sources, files, request)

        return await create_job(
            job=JobCreate(
                job_type=module.id,
                source_id=result_source.id,
                params={k: v for k, v in params.items() if k in field_definitions},
            ),
            referer=referer,
            request=request,
        )

    #
    # GET /jobs
    #
    async def create_simple_job(
        inputs: Optional[List[str]] = Query(default=None),
        sources: Optional[List[str]] = Query(default=None),
        params: QueryModelGet = Depends(),
        referer: Optional[str] = Header(None, include_in_schema=False),
        request: Request = None,
    ):
        if inputs is None:
            inputs = []
        if sources is None:
            sources = []
        return await _create_job(inputs, sources, [], params.model_dump(), referer, request)

    router.get(f"/{module.id}/jobs/", include_in_schema=False)(create_simple_job)
    router.get(f"/{module.id}/jobs")(create_simple_job)

    #
    # POST /jobs
    #
    async def create_complex_job(
        files: List[UploadFile] = File(
            default=[],
            description='Files to upload. Uncheck "Send empty value" if sending from Swagger UI.',
        ),
        job: QueryModelPost = Body(),
        referer: Optional[str] = Header(None, include_in_schema=False),
        request: Request = None,
    ):
        # files can be None if no files are uploaded (even though the type suggests otherwise)
        if files is None:
            files = []

        return await _create_job(
            job.inputs,
            job.sources,
            files,
            {k: v for k, v in job.dict().items() if k not in ["inputs", "sources"]},
            referer,
            request,
        )

    router.post(f"/{module.id}/jobs/", include_in_schema=False)(create_complex_job)
    router.post(f"/{module.id}/jobs")(create_complex_job)

    #
    # GET /jobs/{job_id}
    #
    router.get(f"/{module.id}/jobs/{{job_id}}/", include_in_schema=False)(get_job)
    router.get(f"/{module.id}/jobs/{{job_id}}")(get_job)

    #
    # DELETE /jobs/{job_id}
    #
    router.delete(f"/{module.id}/jobs/{{job_id}}/", include_in_schema=False)(delete_job)
    router.delete(f"/{module.id}/jobs/{{job_id}}")(delete_job)

    #
    # GET /jobs/{job_id}/results/{page}
    #
    router.get(f"/{module.id}/jobs/{{job_id}}/results/", include_in_schema=False)(get_results)
    router.get(f"/{module.id}/jobs/{{job_id}}/results")(get_results)

    #
    # websocket endpoints
    #
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}")(get_job_ws)
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/")(get_job_ws)

    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/results")(get_results_ws)
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/results/")(get_results_ws)

    return router
