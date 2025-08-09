import logging
from datetime import datetime, timedelta, timezone

from nerdd_link import Action, Channel, JobMessage, LogMessage, Tombstone
from omegaconf import DictConfig

from ..data import Repository

__all__ = ["DeleteExpiredResources"]

logger = logging.getLogger(__name__)


class DeleteExpiredResources(Action[LogMessage]):
    def __init__(self, channel: Channel, repository: Repository, config: DictConfig) -> None:
        super().__init__(channel.logs_topic())
        self.repository = repository
        self.config = config

    async def _process_message(self, message: LogMessage) -> None:
        if message.message_type == "all_checkpoints_processed":
            #
            # delete expired jobs
            #
            deadline = datetime.now(timezone.utc) - timedelta(days=self.config.job_expiration_days)

            # we limit the time spent in this loop
            # -> track the start time
            t = datetime.now()

            async for expired_job in self.repository.get_expired_jobs(deadline):
                try:
                    logger.info("Deleting expired job %s", expired_job.id)

                    # send tombstone message on jobs topic (DeleteJob action will take care of the
                    # rest)
                    await self.channel.jobs_topic().send(
                        Tombstone(JobMessage, id=expired_job.id, job_type=expired_job.job_type)
                    )
                except Exception as e:
                    logger.error("Error deleting expired job %s", expired_job.id, exc_info=e)

                # check if we have spent too much time in this loop
                if datetime.now() - t > timedelta(minutes=1):
                    break

    def _get_group_name(self):
        return "delete-expired-jobs"
