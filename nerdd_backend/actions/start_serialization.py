import logging

from nerdd_link import LogMessage, SerializationRequestMessage

from ..data import RecordNotFoundError
from ..models import JobUpdate
from .action_with_context import ActionWithContext

__all__ = ["StartSerialization"]

logger = logging.getLogger(__name__)


class StartSerialization(ActionWithContext[LogMessage]):
    def __init__(self, app) -> None:
        super().__init__(app, app.state.channel.logs_topic())

    async def _process_message(self, message: LogMessage) -> None:
        job_id = message.job_id
        if message.message_type == "all_checkpoints_processed":
            logger.info(f"All checkpoints for {job_id} computed -> starting serialization.")

            try:
                job = await self.repository.update_job(
                    JobUpdate(
                        id=job_id,
                        status="serializing",
                    )
                )
            except RecordNotFoundError as e:
                # The job might have been deleted in the meantime.
                logger.warning(f"Job with ID {message.job_id} not found: {e}")
                return

            # send request to write output files
            output_formats = self.config.output_formats
            for output_format in output_formats:
                await self.channel.serialization_requests_topic().send(
                    SerializationRequestMessage(
                        job_id=job_id,
                        job_type=job.job_type,
                        params=job.params,
                        output_format=output_format,
                    )
                )

    def _get_group_name(self):
        return "start-serialization"
