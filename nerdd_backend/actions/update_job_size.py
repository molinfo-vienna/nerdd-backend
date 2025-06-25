import logging

from nerdd_link import Action, Channel, LogMessage, SerializationRequestMessage
from omegaconf import DictConfig

from ..data import RecordNotFoundError, Repository
from ..models import JobUpdate

__all__ = ["UpdateJobSize"]

logger = logging.getLogger(__name__)


class UpdateJobSize(Action[LogMessage]):
    def __init__(self, channel: Channel, repository: Repository, config: DictConfig) -> None:
        super().__init__(channel.logs_topic())
        self.repository = repository
        self.config = config

    async def _process_message(self, message: LogMessage) -> None:
        job_id = message.job_id
        if message.message_type == "report_job_size":
            logger.info(
                f"Update job size for job {job_id}: {message.num_entries} entries, "
                f"{message.num_checkpoints} checkpoints"
            )

            try:
                # update job size
                job = await self.repository.update_job(
                    JobUpdate(
                        id=job_id,
                        num_entries_total=message.num_entries,
                        num_checkpoints_total=message.num_checkpoints,
                    )
                )

                # check if all checkpoints have been processed
                # TODO: this is duplicate code from SaveResultCheckpointToDb... try to refactor
                checkpoints = await self.repository.get_result_checkpoints_by_job_id(job_id)
                if len(checkpoints) == job.num_checkpoints_total:
                    # send request to write output files
                    output_formats = self.config.output_formats
                    for output_format in output_formats:
                        await self.channel.serialization_requests_topic().send(
                            SerializationRequestMessage(
                                job_id=message.job_id,
                                job_type=job.job_type,
                                params=job.params,
                                output_format=output_format,
                            )
                        )
            except RecordNotFoundError as e:
                # The job might have been deleted in the meantime.
                logger.warning(f"Job with ID {message.job_id} not found: {e}")

    def _get_group_name(self):
        return "update-job-size"
