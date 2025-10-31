import logging

from nerdd_link import JobMessage, SerializationRequestMessage, Tombstone

from .action_with_context import ActionWithContext

__all__ = ["DeleteJob"]

logger = logging.getLogger(__name__)


class DeleteJob(ActionWithContext[JobMessage]):
    def __init__(self, app) -> None:
        super().__init__(app, app.state.channel.jobs_topic())

    async def _process_message(self, message: JobMessage) -> None:
        pass

    async def _process_tombstone(self, message: Tombstone[JobMessage]) -> None:
        job_id = message.id
        logger.info(f"Deleting job with ID {job_id}")

        # delete job (if not already deleted)
        await self.repository.delete_job_by_id(job_id)

        # send tombstone messages on results topic
        # for result in self.repository.get_results_by_job_id(job_id):
        #     await self.channel.results_topic().send(
        #         Tombstone(
        #             ResultMessage,
        #             id=result.id,
        #         )
        #     )

        # delete corresponding results
        await self.repository.delete_results_by_job_id(job_id)

        # send tombstone messages on serialization requests topic
        for output_format in self.config.output_formats:
            await self.channel.serialization_requests_topic().send(
                Tombstone(SerializationRequestMessage, job_id=job_id, output_format=output_format)
            )
