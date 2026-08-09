from typing import List, Optional

from nerdd_module.config import Module
from pydantic import BaseModel

from ..util import clamp

__all__ = ["ModuleInternal", "ModulePublic", "ModuleShort"]


class ModuleInternal(Module):
    processed_publications: Optional[List[dict]] = None
    seconds_per_molecule: float = 30
    # estimated time the module takes to start up before processing a batch
    startup_time_seconds: float = 5

    def max_num_molecules(
        self,
        max_job_duration_minutes: float,
        max_num_molecules: int,
    ) -> int:
        # We have to solve the following equation
        #  max_job_duration_minutes * 60
        #   >= startup_time_seconds * num_batches + num_molecules * seconds_per_molecule
        #   = startup_time_seconds * (num_molecules / batch_size)
        #     + num_molecules * seconds_per_molecule
        #   = num_molecules * (seconds_per_molecule + startup_time_seconds / batch_size)
        # This is an approximation, because num_batches is actually
        # ceil(num_molecules / batch_size).
        # Rearranging gives:
        #   num_molecules <=
        #     max_job_duration_minutes * 60
        #     / (seconds_per_molecule + startup_time_seconds / batch_size)

        # compute denominator
        total_seconds_per_molecule = (
            self.seconds_per_molecule + self.startup_time_seconds / self.batch_size
        )

        # make sure that denominator is larger than 0
        min_seconds_per_molecule = max_job_duration_minutes * 60 / max_num_molecules
        effective_seconds_per_molecule = max(total_seconds_per_molecule, min_seconds_per_molecule)

        max_num_molecules = clamp(
            int(max_job_duration_minutes * 60 / effective_seconds_per_molecule),
            # there should be at least one molecule in a job
            1,
            # and at most the module's maximum number of molecules
            max_num_molecules,
        )

        # round down to a readable number
        if max_num_molecules >= 10_000:
            max_num_molecules = (max_num_molecules // 1_000) * 1_000
        elif max_num_molecules >= 1_000:
            max_num_molecules = (max_num_molecules // 100) * 100
        elif max_num_molecules >= 100:
            max_num_molecules = (max_num_molecules // 10) * 10

        return max_num_molecules

    def checkpoint_size(
        self,
        max_job_duration_minutes: float,
        max_checkpoint_duration_minutes: float,
        max_num_molecules: int,
    ) -> int:
        # We do a similar computation as in max_num_molecules, but we assume that the duration is
        # given by max_checkpoint_duration_minutes. A checkpoint represents the amount of
        # computation time we are losing at worst if a failure occurs during processing of a
        # checkpoint (since the checkpoint has to be recomputed).

        # compute denominator
        total_seconds_per_molecule = (
            self.seconds_per_molecule + self.startup_time_seconds / self.batch_size
        )

        # make sure that denominator is larger than 0
        min_seconds_per_molecule = max_job_duration_minutes * 60 / max_num_molecules
        effective_seconds_per_molecule = max(total_seconds_per_molecule, min_seconds_per_molecule)

        checkpoint_size = clamp(
            int(max_checkpoint_duration_minutes * 60 / effective_seconds_per_molecule),
            # there should be at least one molecule in a checkpoint
            1,
            # and at most the module's maximum number of molecules
            max_num_molecules,
        )

        return checkpoint_size


# We intentionally do not inherit from ModuleInternal here, to give the chance to hide internal
# fields in the future if needed.
class ModulePublic(Module):
    module_url: str
    output_formats: List[str]


class ModuleShort(BaseModel):
    id: str
    rank: Optional[float] = None
    name: Optional[str] = None
    version: Optional[str] = None
    visible_name: Optional[str] = None
    logo: str
    logo_title: Optional[str] = None
    logo_caption: Optional[str] = None
    module_url: str
    output_formats: List[str]
