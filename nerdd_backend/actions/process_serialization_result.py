import logging

from fastapi import FastAPI
from nerdd_link import SerializationResultMessage

from ..data import RecordNotFoundError
from ..models import JobUpdate
from .action_with_context import ActionWithContext

__all__ = ["ProcessSerializationResult"]

logger = logging.getLogger(__name__)


class ProcessSerializationResult(ActionWithContext[SerializationResultMessage]):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app, app.state.channel.serialization_results_topic())

    async def _process_message(self, message: SerializationResultMessage) -> None:
        job_id = message.job_id
        output_format = message.output_format
        logger.info(f"Received serialization result for job {job_id} in format {output_format}")

        try:
            updated_job = await self.repository.update_job(
                JobUpdate(id=job_id, new_output_formats=[output_format])
            )
        except RecordNotFoundError as e:
            # The job might have been deleted in the meantime.
            logger.warning(f"Job with ID {job_id} not found: {e}")
            return

        #
        # Check if all output formats have been processed.
        #
        # This looks like a race condition, since there are two sequential job updates (one for the
        # output format above and one for the status below). However, since the topic is partitioned
        # by job_id, only one worker will process the serialization result for a given job at a
        # time.
        if len(set(updated_job.output_formats)) == len(set(self.config.output_formats)):
            await self.repository.update_job(JobUpdate(id=job_id, status="completed"))

    def _get_group_name(self) -> str:
        return "process-serialization-result"
