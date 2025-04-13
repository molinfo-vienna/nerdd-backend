import logging

from nerdd_link import Action, Channel, LogMessage, SerializationRequestMessage
from omegaconf import DictConfig

from ..data import Repository
from ..models import JobUpdate

__all__ = ["UpdateJobSize"]

logger = logging.getLogger(__name__)


class UpdateJobSize(Action[LogMessage]):
    def __init__(self, channel: Channel, repository: Repository, config: DictConfig) -> None:
        super().__init__(channel.logs_topic())
        self.repository = repository
        self.config = config

    async def _process_message(self, message: LogMessage) -> None:
        if message.message_type == "report_job_size":
            logger.info(f"Update job size {message}")

            # update job size
            job = await self.repository.update_job(
                JobUpdate(
                    id=message.job_id,
                    num_entries_total=message.num_entries,
                    num_checkpoints_total=message.num_checkpoints,
                )
            )

            # check if all checkpoints have been processed
            # TODO: this is duplicate code from SaveResultCheckpointToDb... try to refactor
            unique_checkpoints = set(job.checkpoints_processed)
            if len(unique_checkpoints) == job.num_checkpoints_total:
                # send request to write output files
                output_formats = self.config.output_formats
                for output_format in output_formats:
                    await self.channel.serialization_requests_topic().send(
                        SerializationRequestMessage(
                            job_id=message.job_Id,
                            job_type=job.job_type,
                            params=job.params,
                            output_format=output_format,
                        )
                    )

    def _get_group_name(self):
        return "update-job-size"
