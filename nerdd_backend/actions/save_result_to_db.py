import asyncio
import logging
from asyncio import Lock
from collections import OrderedDict
from typing import List

from nerdd_link import Action, Channel, ResultMessage

from ..data import RecordNotFoundError, Repository
from ..models import Result

__all__ = ["SaveResultToDb"]

logger = logging.getLogger(__name__)


# function that caches sources in memory
cache = OrderedDict()
max_cache_size = 1000
cache_lock = Lock()


async def get_source_by_id(source_id, repository):
    async with cache_lock:
        if source_id in cache:
            # make source_id the most recently used
            cache.move_to_end(source_id)
            # return the cached value
            return cache[source_id]

    # if the source is not in the cache, get it from the database
    try:
        source = await repository.get_source_by_id(source_id)
        filename = source.filename
    except RecordNotFoundError:
        filename = source_id

    async with cache_lock:
        # if the cache is full, remove the least recently used source
        if len(cache) >= max_cache_size:
            cache.popitem(last=False)

        # add the new source to the cache and make it the most recently used
        cache[source_id] = filename
        cache.move_to_end(source_id)

    return filename


class SaveResultToDb(Action[ResultMessage]):
    def __init__(self, channel: Channel, repository: Repository) -> None:
        super().__init__(channel.results_topic(), batch_size=100)
        self.repository = repository

    async def _process_messages(self, messages: List[ResultMessage]) -> None:
        #
        # Validate job ids
        #
        valid_jobs = set()
        invalid_jobs = set()
        valid_messages = []
        for message in messages:
            job_id = message.job_id

            if job_id not in valid_jobs and job_id not in invalid_jobs:
                try:
                    await self.repository.get_job_by_id(job_id)
                    valid_jobs.add(job_id)
                except RecordNotFoundError:
                    logger.warning(f"Job with id {job_id} not found. Ignoring this result.")
                    invalid_jobs.add(job_id)

            if job_id in valid_jobs:
                valid_messages.append(message.model_dump())
            elif job_id in invalid_jobs:
                # If a job was submitted and deleted during processing, results might still be
                # generated. In this case, we ignore the results of the deleted job.
                continue

        # TODO: check if corresponding modules have correct task types
        # (e.g. "derivative_prediction")

        for message in valid_messages:
            job_id = message["job_id"]

            #
            # Map sources to original file names
            #
            if (
                "source" in message
                and message["source"] is not None
                and not isinstance(message["source"], str)
            ):
                translated_sources = await asyncio.gather(
                    *(
                        get_source_by_id(source_id, self.repository)
                        for source_id in message["source"]
                    )
                )
                message["source"] = [s for s in translated_sources if s is not None]

            #
            # Replace all file paths with urls
            #
            for k, v in message.items():
                if isinstance(v, str) and v.startswith("file://"):
                    parts = v.rsplit("/", 1)
                    if len(parts) == 2:
                        record_id = parts[1]
                        message[k] = f"/api/jobs/{job_id}/files/{k}/{record_id}"

            # generate an id for the result
            if "id" not in message:
                logger.info("Generating id for result")
                if hasattr(message, "atom_id"):
                    id = f"{job_id}-{message.mol_id}-{message.atom_id}"
                elif hasattr(message, "derivative_id"):
                    id = f"{job_id}-{message.mol_id}-{message.derivative_id}"
                else:
                    id = f"{job_id}-{message.mol_id}"
                message["id"] = id

        # save results to database
        await self.repository.upsert_results([Result(**message) for message in valid_messages])

    def _get_group_name(self):
        return "save-result-to-db"
