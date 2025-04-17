from uuid import uuid4

from fastapi import HTTPException

from ..data import RecordNotFoundError, Repository
from ..models import AnonymousUser

__all__ = ["get_user", "check_quota"]


async def get_user(request):
    app = request.app
    repository: Repository = app.state.repository

    # get ip address of the request
    ip_address = request.client.host

    # get user by ip
    try:
        return await repository.get_user_by_ip_address(ip_address)
    except RecordNotFoundError:
        # if user does not exist, create a new anonymous user
        uuid = uuid4()
        return await repository.create_user(AnonymousUser(id=str(uuid), ip_address=ip_address))


async def check_quota(user, request):
    app = request.app
    config = app.state.config
    repository: Repository = app.state.repository

    # get all jobs started in the last 24 hours by the user
    jobs = await repository.get_recent_jobs_by_user(user, 24 * 60 * 60)

    # get fresh jobs (counting of entries not yet started)
    jobs_fresh = [job for job in jobs if job.num_entries_total is None]

    if len(jobs_fresh) > 0:
        raise HTTPException(
            status_code=429,
            detail=(
                "The server is initializing a job you submitted recently. Please wait a few "
                "seconds before submitting a new job."
            ),
        )

    # check if the user has reached the maximum number of molecules per day
    if hasattr(config, "quota_anonymous"):
        num_mols_processed = sum([job.num_entries_total for job in jobs])
        if num_mols_processed >= config.quota_anonymous:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"You have reached the maximum number of molecules ({config.quota_anonymous}) "
                    f"that can be processed per day. Please try again tomorrow."
                ),
            )

    return True
