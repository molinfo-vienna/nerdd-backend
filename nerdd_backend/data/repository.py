from abc import ABC, abstractmethod
from asyncio import Queue, create_task
from datetime import datetime
from typing import Any, AsyncIterable, List, Optional, Tuple

from ..models import (
    AnonymousUser,
    Challenge,
    JobInternal,
    JobUpdate,
    JobWithResults,
    ModuleInternal,
    Result,
    ResultCheckpoint,
    Source,
    User,
)
from ..util import CompressedSet

__all__ = ["Repository"]


class Repository(ABC):
    #
    # INITIALIZATION
    #
    @abstractmethod
    async def initialize(self):
        pass

    #
    # MODULES
    #
    @abstractmethod
    def get_module_changes(
        self,
    ) -> AsyncIterable[Tuple[Optional[ModuleInternal], Optional[ModuleInternal]]]:
        pass

    @abstractmethod
    async def get_all_modules(self) -> List[ModuleInternal]:
        pass

    @abstractmethod
    async def get_module_by_id(self, module_id: str) -> ModuleInternal:
        pass

    @abstractmethod
    async def create_module(self, module: ModuleInternal) -> ModuleInternal:
        pass

    @abstractmethod
    async def update_module(self, module: ModuleInternal) -> ModuleInternal:
        pass

    #
    # JOBS
    #
    async def get_job_with_result_changes(
        self, job_id: str
    ) -> AsyncIterable[Tuple[Optional[JobWithResults], Optional[JobWithResults]]]:
        # The main idea of this method is to merge the changes of job and results. For that we
        # get the current state of the job and update whenever a change occurs.
        job = await self.get_job_by_id(job_id)

        # return the initial state of the job (None indicates that this is the initial state)
        yield None, job

        if job.is_done():
            return

        # We create two tasks that listen to the changes of job and results and put the changes into
        # a queue.
        queue = Queue[Tuple[str, Any]]()

        async def _drain_iterator(aiter: AsyncIterable, event_type: str) -> None:
            async for item in aiter:
                await queue.put((event_type, item))

        drain_tasks = [
            create_task(_drain_iterator(aiter, event_type))
            for aiter, event_type in [
                (self.get_job_changes(job_id), "job_change"),
                (self.get_result_changes(job_id), "results_change"),
            ]
        ]

        while True:
            event_type, (_, new) = await queue.get()
            if event_type == "job_change":
                if new is not None:
                    new_job = JobWithResults(
                        **new.model_dump(),
                        entries_processed=job.entries_processed,
                    )
                    yield job, new_job
                    job = new_job

                    if job.is_done():
                        # job is completed, we can exit the loop
                        break
                else:
                    # job was deleted -> exit the loop
                    break
            elif event_type == "results_change":
                if new is not None:
                    if new.mol_id in job.entries_processed:
                        # result already processed, skip
                        continue

                    old_job_obj = job.model_dump()
                    old_job_obj["entries_processed"] = CompressedSet(
                        old_job_obj["entries_processed"]
                    )
                    old_job_obj["entries_processed"].add(new.mol_id)

                    new_job = JobWithResults(**old_job_obj)

                    yield job, new_job
                    job = new_job

                    if job.is_done():
                        # job is completed, we can exit the loop
                        break
                else:
                    pass

        for task in drain_tasks:
            task.cancel()

    @abstractmethod
    def get_job_changes(
        self, job_id: str
    ) -> AsyncIterable[Tuple[Optional[JobInternal], Optional[JobInternal]]]:
        pass

    @abstractmethod
    async def create_job(self, job: JobInternal) -> JobWithResults:
        pass

    @abstractmethod
    async def update_job(self, job_update: JobUpdate) -> JobInternal:
        pass

    @abstractmethod
    async def get_job_by_id(self, job_id: str) -> JobWithResults:
        pass

    @abstractmethod
    async def delete_job_by_id(self, job_id: str) -> None:
        pass

    @abstractmethod
    async def get_expired_jobs(self, deadline: datetime) -> AsyncIterable[JobInternal]:
        pass

    #
    # SOURCES
    #
    @abstractmethod
    async def create_source(self, source: Source) -> Source:
        pass

    @abstractmethod
    async def get_source_by_id(self, source_id: str) -> Source:
        pass

    @abstractmethod
    async def delete_source_by_id(self, source_id: str) -> None:
        pass

    @abstractmethod
    async def get_expired_sources(self, deadline: datetime) -> AsyncIterable[Source]:
        pass

    #
    # RESULTS
    #
    @abstractmethod
    async def get_results_by_job_id(
        self,
        job_id: str,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> List[Result]:
        pass

    @abstractmethod
    async def create_result(self, result: Result) -> Result:
        pass

    @abstractmethod
    def get_result_changes(
        self,
        job_id,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> AsyncIterable[Tuple[Optional[Result], Optional[Result]]]:
        pass

    @abstractmethod
    async def delete_results_by_job_id(self, job_id: str) -> None:
        pass

    #
    # CHECKPOINTS
    #
    @abstractmethod
    async def create_result_checkpoint(self, checkpoint: ResultCheckpoint) -> ResultCheckpoint:
        pass

    @abstractmethod
    async def get_result_checkpoints_by_job_id(self, job_id: str) -> List[ResultCheckpoint]:
        pass

    @abstractmethod
    async def delete_result_checkpoints_by_job_id(self, job_id: str) -> None:
        pass

    #
    # USERS
    #
    @abstractmethod
    async def get_user_by_ip_address(self, ip_address: str) -> AnonymousUser:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_recent_jobs_by_user(self, user: User, num_seconds: int) -> List[JobInternal]:
        pass

    #
    # CHALLENGES (CAPTCHAS)
    #
    @abstractmethod
    async def get_challenge_by_salt(self, salt: str) -> Challenge:
        pass

    @abstractmethod
    async def create_challenge(self, challenge: Challenge) -> Challenge:
        pass

    @abstractmethod
    async def delete_challenge_by_id(self, id: str) -> None:
        pass

    @abstractmethod
    async def delete_expired_challenges(self, deadline: datetime) -> None:
        pass
