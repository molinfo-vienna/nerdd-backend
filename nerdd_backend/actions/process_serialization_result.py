import logging

from nerdd_link import Action, Channel, SerializationResultMessage
from omegaconf import DictConfig

from ..data import RecordNotFoundError, Repository
from ..models import JobUpdate

__all__ = ["ProcessSerializationResult"]

logger = logging.getLogger(__name__)


class ProcessSerializationResult(Action[SerializationResultMessage]):
    def __init__(self, channel: Channel, repository: Repository, config: DictConfig) -> None:
        super().__init__(channel.serialization_results_topic())
        self.repository = repository
        self.config = config

    async def _process_message(self, message: SerializationResultMessage) -> None:
        job_id = message.job_id
        output_format = message.output_format
        logger.info(f"Received serialization result for job {job_id} in format {output_format}")

        try:
            updated_job = await self.repository.update_job(
                JobUpdate(id=job_id, new_output_formats=[output_format])
            )

            #
            # Check if all output formats have been processed.
            #
            # Note that this looks like a race condition here, since there are two sequential job
            # updates (one for the output format and one for the status). For two workers, a
            # situation like this comes to mind:
            #   * Worker 1 receives a serialization result for job 1 in format A
            #   * Worker 2 receives a serialization result for job 1 in format B
            #   * Worker 1 updates the job with output format A (in parallel with Worker 2)
            #   * Worker 2 updates the job with output format B (in parallel with Worker 1)
            #   * Worker 1 checks if all output formats have been processed, which is false
            #     (since it only sees output format A)
            #   * Worker 2 checks if all output formats have been processed, which is false
            #     (since it only sees output format B)
            # However, since the first update (new_output_formats) is atomic, it is guaranteed
            # that one process (here: worker 2) would see all output formats before the next update
            # (new_status) is applied.
            # But more importantly, the topic is partitioned by job ID, so only one worker will
            # process the serialization result for a given job at a time!
            if len(set(updated_job.output_formats)) == len(set(self.config.output_formats)):
                await self.repository.update_job(JobUpdate(id=job_id, status="completed"))
        except RecordNotFoundError as e:
            # The job might have been deleted in the meantime.
            logger.warning(f"Job with ID {job_id} not found: {e}")

    def _get_group_name(self):
        return "save-result-checkpoint-to-db"
