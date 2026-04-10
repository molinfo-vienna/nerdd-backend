import logging

from fastapi import FastAPI
from nerdd_link import LogMessage, SerializationRequestMessage

from ..data import RecordNotFoundError
from ..models import JobUpdate
from .action_with_context import ActionWithContext

__all__ = ["StartSerialization"]

logger = logging.getLogger(__name__)


class StartSerialization(ActionWithContext[LogMessage]):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app, app.state.channel.logs_topic())

    async def _process_message(self, message: LogMessage) -> None:
        job_id = message.job_id
        if message.message_type == "all_checkpoints_processed":
            logger.info(f"All checkpoints for {job_id} computed -> starting serialization.")

            try:
                job = await self.repository.get_job_by_id(job_id)
            except RecordNotFoundError as e:
                # The job might have been deleted in the meantime.
                logger.warning(f"Job with ID {message.job_id} not found: {e}")
                return

            # skip serialization if the job is / was already serializing
            if job.status in ("serializing", "completed", "failed"):
                logger.info(f"Job {job_id} has status '{job.status}'. Skipping serialization.")
                return

            # serialize only the output formats that haven't been serialized yet
            output_formats = [
                fmt for fmt in self.config.output_formats if fmt not in job.output_formats
            ]

            for output_format in output_formats:
                await self.channel.serialization_requests_topic().send(
                    SerializationRequestMessage(
                        job_id=job_id,
                        job_type=job.job_type,
                        params=job.params,
                        output_format=output_format,
                    )
                )

            # update status to "serializing" (at the end of the method to avoid problems)
            current_job = await self.repository.get_job_by_id(job_id)
            if current_job.status in ("created", "processing"):
                await self.repository.update_job(
                    JobUpdate(
                        id=job_id,
                        status="serializing",
                    )
                )

    def _get_group_name(self) -> str:
        return "start-serialization"
