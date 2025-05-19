from fastapi import APIRouter, HTTPException, Request

from ..data import RecordNotFoundError, Repository
from ..models import Pagination, ResultSet
from .jobs import augment_job

__all__ = ["results_router"]

results_router = APIRouter(prefix="")


@results_router.get("/jobs/{job_id}/results")
async def get_results(
    job_id: str, page: int = 1, return_incomplete: bool = False, request: Request = None
) -> ResultSet:
    app = request.app
    repository: Repository = app.state.repository

    page_zero_based = page - 1

    try:
        job = await repository.get_job_by_id(job_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail="Job not found") from e

    page_size = job.page_size

    # num_entries might not be available, yet
    # we assume it to be positive infinity in that case
    if job.num_entries_total is None:
        num_entries = float("inf")
    else:
        num_entries = job.num_entries_total

    # check if page is clearly out of range
    if page_zero_based < 0 or page_zero_based * page_size >= num_entries:
        raise HTTPException(status_code=404, detail="Page out of range")

    first_mol_id = page_zero_based * page_size
    last_mol_id = min(first_mol_id + page_size, num_entries) - 1
    results = await repository.get_results_by_job_id(job_id, first_mol_id, last_mol_id)
    is_incomplete = len(results) < last_mol_id - first_mol_id + 1

    # if return_incomplete is not set, then we need to have all results on that page
    if not return_incomplete and is_incomplete:
        raise HTTPException(status_code=202, detail="Results not yet available")

    def page_url(p):
        # page in url is 1-based
        return f"{request.base_url}{job.job_type}/jobs/{job_id}/results?page={p + 1}"

    pagination = Pagination(
        page=page,  # 1-based!
        page_size=page_size,
        is_incomplete=is_incomplete,
        first_mol_id_on_page=first_mol_id,
        last_mol_id_on_page=last_mol_id,
        previous_url=page_url(page_zero_based - 1) if page_zero_based > 0 else None,
        next_url=(page_url(page_zero_based + 1) if last_mol_id < num_entries - 1 else None),
    )

    job_public = await augment_job(job, request)

    return ResultSet(data=results, pagination=pagination, job=job_public)
