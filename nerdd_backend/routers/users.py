import logging
from uuid import uuid4

from fastapi import HTTPException

from ..config import AppConfig
from ..data import RecordNotFoundError, Repository
from ..models import AnonymousUser

__all__ = ["get_user", "check_quota"]

logger = logging.getLogger(__name__)


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
    config: AppConfig = app.state.config
    repository: Repository = app.state.repository

    # get all jobs started in the last 24 hours by the user
    jobs = await repository.get_recent_jobs_by_user(user, 24 * 60 * 60)

    # get fresh jobs (counting of entries not yet started)
    jobs_fresh = [job for job in jobs if job.num_entries_total is None]

    if len(jobs_fresh) > 0:
        if type(user) is AnonymousUser:
            logger.info(
                f"User {user.id} with IP {user.ip_address} has {len(jobs_fresh)} fresh jobs. "
                f"Rejecting new job submission."
            )
        raise HTTPException(
            status_code=429,
            detail=(
                "The server is initializing a job you submitted recently. Please wait a few "
                "seconds before submitting a new job."
            ),
        )

    # get active jobs (job status is not "completed")
    jobs_active = [job for job in jobs if job.status != "completed"]

    if hasattr(config, "quota_active_jobs_anonymous"):
        # check if the user has reached the maximum number of active jobs
        if len(jobs_active) >= config.quota_active_jobs_anonymous:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"You have reached the maximum number of active jobs "
                    f"({config.quota_active_jobs_anonymous}) that can be processed at the same "
                    f"time. Please wait until one of your jobs has finished."
                ),
            )

    # check if the user has reached the maximum number of molecules per day
    if hasattr(config, "quota_mols_per_day_anonymous"):
        num_mols_processed = sum([job.num_entries_total for job in jobs])
        if num_mols_processed >= config.quota_mols_per_day_anonymous:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"You have reached the maximum number of molecules "
                    f"({config.quota_mols_per_day_anonymous}) that can be processed per day. "
                    f"Please try again tomorrow."
                ),
            )

    return True
