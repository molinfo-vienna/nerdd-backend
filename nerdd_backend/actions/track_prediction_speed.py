import logging

import numpy as np
from nerdd_link import Action, Channel, LogMessage
from omegaconf import DictConfig
from sklearn.linear_model import LinearRegression

from ..data import RecordNotFoundError, Repository
from ..models import ModuleInternal, ResultCheckpoint

__all__ = ["TrackPredictionSpeed"]

logger = logging.getLogger(__name__)


class TrackPredictionSpeed(Action[LogMessage]):
    def __init__(self, channel: Channel, repository: Repository, config: DictConfig) -> None:
        super().__init__(channel.logs_topic())
        self.repository = repository
        self.config = config

    async def _process_message(self, message: LogMessage) -> None:
        job_id = message.job_id
        if message.message_type == "all_checkpoints_processed":
            # get job
            try:
                job = await self.repository.get_job_by_id(job_id)
            except RecordNotFoundError:
                # the job might not exist anymore, e.g., if it was deleted
                logger.warning(f"Job {job_id} not found, skipping checkpoint processing")
                return

            # update all checkpoints with their size
            checkpoints = await self.repository.get_result_checkpoints_by_job_id(job_id)
            for checkpoint in checkpoints:
                # compute checkpoint size
                # * all checkpoints (except the last one) have the same size checkpoint_size
                # * size of last checkpoint might be smaller and can be computed by
                #     num_entries_total - checkpoint_id * checkpoint_size
                # * this number is smaller than or equal to checkpoint_size
                # * -> we can use the minimum to compute the size of any checkpoint
                size = min(
                    job.checkpoint_size,
                    job.num_entries_total - checkpoint.checkpoint_id * job.checkpoint_size,
                )

                try:
                    await self.repository.update_result_checkpoint(
                        ResultCheckpoint(
                            **{
                                **checkpoint.model_dump(),
                                "size": size,
                            }
                        )
                    )
                except RecordNotFoundError:
                    continue

            # get module
            try:
                module = await self.repository.get_module_by_id(job.job_type)
            except RecordNotFoundError:
                logger.warning(
                    f"Module {job.job_type} not found for job {job_id}, skipping checkpoint "
                    f"processing"
                )
                return

            checkpoints = [
                c
                for c in await self.repository.get_result_checkpoints_by_module_id(job.job_type)
                if c.size is not None
            ]

            # Calculation of the prediction speed:
            # * each checkpoint is computed in batches (batch size given in module.batch_size)
            # * for each batch, a model has to be loaded before running the prediction
            #   -> batch_time_seconds = startup_time_seconds + prediction_time_seconds
            # * we treat the startup time as a variable that is to be determined
            # * we assume the prediction time depends on the number of molecules in the batch
            #   -> batch_time_seconds = molecules_in_batch * seconds_per_molecule
            # * seconds_per_molecule is the next variable to be determined
            # * we do not need to infer the number of molecules in a batch due to substitution:
            #     checkpoint_time_seconds
            #       =   startup_time_seconds + size_batch1 * seconds_per_molecule
            #         + startup_time_seconds + size_batch2 * seconds_per_molecule
            #         + ...
            #         + startup_time_seconds + size_batchN * seconds_per_molecule
            #       = num_batches * startup_time_seconds
            #         + (size_batch1 + size_batch2 + ... + size_batchN) * seconds_per_molecule
            #       = num_batches * startup_time_seconds + size_checkpoint * seconds_per_molecule
            # * we can divide by num_batches on both sides to get an ordinary linear equation
            # * repeating this for all checkpoints gives us a system of linear equations with
            #   two unknowns:
            #   * startup_time_seconds (the intercept)
            #   * seconds_per_molecule (the slope)

            # the system of linear equations only has a meaningful solution if there are at least
            # two checkpoints with a different number of molecules
            num_unique_checkpoint_sizes = len({c.size for c in checkpoints})
            if num_unique_checkpoint_sizes < 2:
                logger.warning(
                    "Not enough checkpoints with different sizes to compute prediction speed"
                )
                return

            #
            # setup the system of linear equations
            #

            # compute the number of batches for each checkpoint
            # Note: this might be inaccurate because some input molecules are filtered out
            # before batching / prediction. However, we assume that this happens rarely.
            num_batches = np.ceil([c.size / module.batch_size for c in checkpoints])
            y = np.array([c.elapsed_time_seconds for c in checkpoints])
            y_final = y / num_batches

            X = np.array([c.size for c in checkpoints])
            X_final = (X / num_batches).reshape(-1, 1)

            #
            # solve
            #
            model = LinearRegression(fit_intercept=True, positive=True)
            model.fit(X_final, y_final)
            seconds_per_molecule = model.coef_[0]
            startup_time_seconds = model.intercept_

            #
            # update the module with the prediction speed
            #
            logger.info(
                f"Updating module {module.id} with prediction speed: "
                f"{model.coef_[0]:.1f} seconds per molecule, "
                f"startup time of {model.intercept_:.1f} seconds"
            )
            await self.repository.update_module(
                ModuleInternal(
                    **{
                        **module.model_dump(),
                        "seconds_per_molecule": seconds_per_molecule,
                        "startup_time_seconds": startup_time_seconds,
                    }
                )
            )

    def _get_group_name(self):
        return "track-prediction-speed"
