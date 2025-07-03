from fastapi import APIRouter, HTTPException, Query, WebSocket
from fastapi.encoders import jsonable_encoder

from ..data import RecordNotFoundError, Repository
from .jobs import augment_job

__all__ = ["get_job_ws", "get_results_ws", "websockets_router"]

websockets_router = APIRouter(prefix="/websocket")


@websockets_router.websocket("/jobs/{job_id}")
@websockets_router.websocket("/jobs/{job_id}/")
async def get_job_ws(websocket: WebSocket, job_id: str):
    app = websocket.app
    repository: Repository = app.state.repository

    await websocket.accept()

    async for _, internal_job in repository.get_job_with_result_changes(job_id):
        job = await augment_job(internal_job, websocket)
        await websocket.send_json(jsonable_encoder(job))

    await websocket.close()


@websockets_router.websocket("/jobs/{job_id}/results")
@websockets_router.websocket("/jobs/{job_id}/results/")
async def get_results_ws(websocket: WebSocket, job_id: str, page: int = Query()):
    app = websocket.app
    repository: Repository = app.state.repository

    await websocket.accept()

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

    page_zero_based = page - 1

    # check if page is clearly out of range
    if page_zero_based < 0 or page_zero_based * page_size >= num_entries:
        raise HTTPException(status_code=404, detail="Page out of range")

    first_mol_id = page_zero_based * page_size
    last_mol_id = min(first_mol_id + page_size, num_entries) - 1

    async for _, new in repository.get_result_changes(job_id, first_mol_id, last_mol_id):
        if new is not None:
            await websocket.send_json(jsonable_encoder(new))
