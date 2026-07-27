import asyncio
import logging
from typing import Any, List

from fastapi import FastAPI
from nerdd_link import ResultMessage

from ..data import RecordNotFoundError
from ..models import Result
from .action_with_context import ActionWithContext

__all__ = ["SaveResultToDb"]

logger = logging.getLogger(__name__)


class SaveResultToDb(ActionWithContext[ResultMessage]):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app, app.state.channel.results_topic(), batch_size=200)

    async def _process_messages(self, messages: List[ResultMessage]) -> None:
        #
        # Validate job ids
        #
        valid_jobs = set()
        invalid_jobs = set()
        valid_messages: list[dict[str, Any]] = []
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

        # we cache sources to minimize database lookups
        source_cache: dict[str, str | None] = {}

        async def _get_source(source_id: str) -> str | None:
            if source_id in source_cache:
                return source_cache[source_id]
            try:
                source = await self.repository.get_source_by_id(source_id)
                filename = source.filename
            except RecordNotFoundError:
                filename = source_id
            source_cache[source_id] = filename
            return filename

        for message_dict in valid_messages:
            job_id = message_dict["job_id"]

            #
            # Map sources to original file names
            #
            if (
                "source" in message_dict
                and message_dict["source"] is not None
                and not isinstance(message_dict["source"], str)
            ):
                translated_sources = await asyncio.gather(
                    *(_get_source(source_id) for source_id in message_dict["source"])
                )
                message_dict["source"] = [s for s in translated_sources if s is not None]

            #
            # Replace all file paths with urls
            #
            for k, v in message_dict.items():
                if not isinstance(v, str):
                    continue

                try:
                    property_file = self.storage.parse_property_file_path(v)
                except ValueError:
                    continue

                path = self.app.url_path_for(
                    "get_job_file",
                    job_id=property_file.job_id,
                    property=property_file.property_name,
                    record_id=property_file.record_id,
                )
                root_path = self.config.root_path or ""
                message_dict[k] = f"{root_path.rstrip('/')}{path}"

            # generate an id for the result
            if "id" not in message_dict:
                mol_id = message_dict["mol_id"]
                if "atom_id" in message_dict:
                    atom_id = message_dict["atom_id"]
                    id = f"{job_id}-{mol_id}-{atom_id}"
                elif "derivative_id" in message_dict:
                    derivative_id = message_dict["derivative_id"]
                    id = f"{job_id}-{mol_id}-{derivative_id}"
                else:
                    id = f"{job_id}-{mol_id}"
                message_dict["id"] = id

        # save results to database
        await self.repository.upsert_results(
            [Result(**message_dict) for message_dict in valid_messages]
        )

    def _get_group_name(self) -> str:
        return "save-result-to-db"
