import json
import logging
from typing import Annotated, List, Optional

from fastapi import APIRouter, File, Form, Header, HTTPException, Query, Request, UploadFile
from nerdd_module.config import JobParameter
from pydantic import Field, create_model
from stringcase import pascalcase, snakecase

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

INPUTS_DESCRIPTION = "Molecule representations in any of the formats SMILES, SDF or InChI."
SOURCES_DESCRIPTION = "Optional: List of source IDs to use as input for the job."
FILES_DESCRIPTION = "Optional: List of files to use as input for the job."
SWAGGER_WARNING = '**Uncheck "Send empty value" if sending from Swagger UI.**'


def get_query_param(job_parameter: JobParameter):
    requested_type = job_parameter.type
    actual_type = type_mapping.get(requested_type, str)
    default_value = job_parameter.default or None
    description = job_parameter.help_text or ""
    field = Field(default_value, description=description)
    return Annotated[actual_type, field]


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

    #
    # Generate models for endpoints visible on the generated Swagger UI page
    #

    # convert all job parameters to pydantic fields
    field_definitions = dict(
        **{p.name: get_query_param(p) for p in module.job_parameters},
    )

    # generate the name of the pydantic models (shown in Swagger UI)
    # note: snakecase before pascalcase is necessary (pascalcase("mol-scale") produces "Mocale")
    module_name = pascalcase(snakecase(module.id))
    QueryModelGet = create_model(
        f"{module_name}JobCreate",
        inputs=Annotated[Optional[List[str]], Field(default=None, description=INPUTS_DESCRIPTION)],
        sources=Annotated[
            Optional[List[str]], Field(default=None, description=SOURCES_DESCRIPTION)
        ],
        **field_definitions,
    )
    QueryModelPost = create_model(
        f"{module_name}ComplexJobCreate",
        inputs=Annotated[
            List[str],
            Form(
                # we are using an empty array here (in contrast to above) so Swagger UI does not
                # show a list with empty entries
                default=[],
                description=f"{INPUTS_DESCRIPTION} {SWAGGER_WARNING}",
            ),
        ],
        sources=(
            List[str],
            Field(
                # we are using an empty array here (in contrast to above) so Swagger UI does not
                # show a list with empty entries
                default=[],
                description=f"{SOURCES_DESCRIPTION} {SWAGGER_WARNING}",
            ),
        ),
        files=(
            List[UploadFile],
            File(
                # we are using an empty array here (in contrast to above) so Swagger UI does not
                # show a list with empty entries
                default=[],
                description=f"{FILES_DESCRIPTION} {SWAGGER_WARNING}",
            ),
        ),
        **field_definitions,
    )

    #
    # GET /jobs
    # query parameters:
    #   - inputs: list of strings (SMILES, InCHI)
    #   - sources: list of source IDs
    #   - files: list of files (optional)
    #   - all params from module (e.g. metabolism_phase)
    #
    async def _create_job(
        inputs: Optional[List[str]],
        sources: Optional[List[str]],
        files: Optional[List[UploadFile]],
        params: dict,
        referer: Optional[str] = None,
        request: Request = None,
    ):
        if inputs is None:
            inputs = []
        if sources is None:
            sources = []
        if files is None:
            files = []

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
        # Annotated[QueryModelGet, Query()] converts all model fields to GET parameters
        # a valid request looks like this:
        # /cypstrate/jobs?prediction_mode=best_performance&inputs=CCO&inputs=CC
        job: Annotated[QueryModelGet, Query()],
        referer: Annotated[Optional[str], Header(include_in_schema=False)] = None,
        request: Request = None,
    ):
        params = {k: getattr(job, k) for k in field_definitions}
        return await _create_job(job.inputs, job.sources, None, params, referer, request)

    router.get(f"/{module.id}/jobs")(create_simple_job)

    #
    # POST /jobs
    #
    async def create_complex_job(
        # media_type="multipart/form-data": important for Swagger UI to upload files correctly
        job: Annotated[QueryModelPost, Form(media_type="multipart/form-data")],
        referer: Annotated[Optional[str], Header(include_in_schema=False)] = None,
        request: Request = None,
    ):
        return await _create_job(
            job.inputs,
            job.sources,
            job.files,
            {k: getattr(job, k) for k in field_definitions},
            referer,
            request,
        )

    router.post(f"/{module.id}/jobs")(create_complex_job)

    #
    # GET /jobs/{job_id}
    #
    router.get(f"/{module.id}/jobs/{{job_id}}")(get_job)

    #
    # DELETE /jobs/{job_id}
    #
    router.delete(f"/{module.id}/jobs/{{job_id}}")(delete_job)

    #
    # GET /jobs/{job_id}/results/{page}
    #
    router.get(f"/{module.id}/jobs/{{job_id}}/results")(get_results)

    #
    # websocket endpoints
    #

    # Note: we need the slash-less and slash version of the routes, because fastapi does not
    # redirect from the slash-less version to the slash version (as in normal routes).
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}")(get_job_ws)
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/")(get_job_ws)

    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/results")(get_results_ws)
    router.websocket(f"/websocket/{module.id}/jobs/{{job_id}}/results/")(get_results_ws)

    return router
